# -*- coding: utf-8 -*-
"""

Script Name: NetworkManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
import collections, html, typing, attr, prompt

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QCoreApplication, QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply

from PLM.cores import Loggers


HOSTBLOCK_ERROR_STRING = '%HOSTBLOCK%'
_proxy_auth_cache = {}  # type: typing.Dict[ProxyId, prompt.AuthInfo]


@attr.s(frozen=True)
class ProxyId:

    """Information identifying a proxy server."""

    type = attr.ib()
    hostname = attr.ib()
    port = attr.ib()


class NetworkManager(QNetworkAccessManager):
    
    key = 'NetworkManager'
    shutting_down = pyqtSignal()
    logger = Loggers(key)

    def __init__(self, *, win_id, tab_id, private, parent=None):
        self.logger.debug("Initializing NetworkManager")
        with self.logger.disable_qt_msghandler():
            super().__init__(parent)
        self.logger.debug("NetworkManager init done")
        self.adopted_downloads = 0
        self._win_id = win_id
        self._tab_id = tab_id
        self._private = private
        self._scheme_handlers = {'qute': webkitqutescheme.handler, 'file': filescheme.handler, }
        self._set_cookiejar()
        self._set_cache()
        self.sslErrors.connect(self.on_ssl_errors)  # type: ignore
        self._rejected_ssl_errors = collections.defaultdict(
            list)  # type: _SavedErrorsType
        self._accepted_ssl_errors = collections.defaultdict(
            list)  # type: _SavedErrorsType
        self.authenticationRequired.connect(  # type: ignore
            self.on_authentication_required)
        self.proxyAuthenticationRequired.connect(  # type: ignore
            self.on_proxy_authentication_required)
        self.netrc_used = False

    def _set_cookiejar(self):
        """Set the cookie jar of the NetworkManager correctly."""
        if self._private:
            cookie_jar = cookies.ram_cookie_jar
        else:
            cookie_jar = cookies.cookie_jar
        assert cookie_jar is not None

        # We have a shared cookie jar - we restore its parent so we don't
        # take ownership of it.
        self.setCookieJar(cookie_jar)
        app = QCoreApplication.instance()
        cookie_jar.setParent(app)

    def _set_cache(self):
        """Set the cache of the NetworkManager correctly."""
        if self._private:
            return
        # We have a shared cache - we restore its parent so we don't take
        # ownership of it.
        app = QCoreApplication.instance()
        self.setCache(cache.diskcache)
        cache.diskcache.setParent(app)

    def _get_abort_signals(self, owner=None):
        """Get a list of signals which should abort a question."""
        abort_on = [self.shutting_down]
        if owner is not None:
            abort_on.append(owner.destroyed)
        # This might be a generic network manager, e.g. one belonging to a
        # DownloadManager. In this case, just skip the webview thing.
        if self._tab_id is not None:
            assert self._win_id is not None
            tab = objreg.get('tab', scope='tab', window=self._win_id,
                             tab=self._tab_id)
            abort_on.append(tab.load_started)
        return abort_on

    def shutdown(self):
        """Abort all running requests."""
        self.setNetworkAccessible(QNetworkAccessManager.NotAccessible)
        self.shutting_down.emit()

    def on_ssl_errors(self, reply, errors):

        errors = [certificateerror.CertificateErrorWrapper(e) for e in errors]
        log.webview.debug("Certificate errors: {!r}".format(
            ' / '.join(str(err) for err in errors)))
        try:
            host_tpl = urlutils.host_tuple(
                reply.url())  # type: typing.Optional[urlutils.HostTupleType]
        except ValueError:
            host_tpl = None
            is_accepted = False
            is_rejected = False
        else:
            assert host_tpl is not None
            is_accepted = set(errors).issubset(
                self._accepted_ssl_errors[host_tpl])
            is_rejected = set(errors).issubset(
                self._rejected_ssl_errors[host_tpl])

        log.webview.debug("Already accepted: {} / "
                          "rejected {}".format(is_accepted, is_rejected))

        if is_rejected:
            return
        elif is_accepted:
            reply.ignoreSslErrors()
            return

        abort_on = self._get_abort_signals(reply)
        ignore = shared.ignore_certificate_errors(reply.url(), errors,
                                                  abort_on=abort_on)
        if ignore:
            reply.ignoreSslErrors()
            err_dict = self._accepted_ssl_errors
        else:
            err_dict = self._rejected_ssl_errors
        if host_tpl is not None:
            err_dict[host_tpl] += errors

    def clear_all_ssl_errors(self):
        self._accepted_ssl_errors.clear()
        self._rejected_ssl_errors.clear()

    @pyqtSlot(QUrl)
    def clear_rejected_ssl_errors(self, url):

        try:
            del self._rejected_ssl_errors[url]
        except KeyError:
            pass

    @pyqtSlot('QNetworkReply*', 'QAuthenticator*')
    def on_authentication_required(self, reply, authenticator):
        url = reply.url()
        log.network.debug("Authentication requested for {}, netrc_used {}"
                          .format(url.toDisplayString(), self.netrc_used))

        netrc_success = False
        if not self.netrc_used:
            self.netrc_used = True
            netrc_success = shared.netrc_authentication(url, authenticator)

        if not netrc_success:
            log.network.debug("Asking for credentials")
            abort_on = self._get_abort_signals(reply)
            shared.authentication_required(url, authenticator,
                                           abort_on=abort_on)

    @pyqtSlot('QNetworkProxy', 'QAuthenticator*')
    def on_proxy_authentication_required(self, proxy, authenticator):
        proxy_id = ProxyId(proxy.type(), proxy.hostName(), proxy.port())
        if proxy_id in _proxy_auth_cache:
            authinfo = _proxy_auth_cache[proxy_id]
            authenticator.setUser(authinfo.user)
            authenticator.setPassword(authinfo.password)
        else:
            msg = '<b>{}</b> says:<br/>{}'.format(
                html.escape(proxy.hostName()),
                html.escape(authenticator.realm()))
            abort_on = self._get_abort_signals()
            answer = message.ask(
                title="Proxy authentication required", text=msg,
                mode=usertypes.PromptMode.user_pwd, abort_on=abort_on)
            if answer is not None:
                authenticator.setUser(answer.user)
                authenticator.setPassword(answer.password)
                _proxy_auth_cache[proxy_id] = answer

    @pyqtSlot()
    def on_adopted_download_destroyed(self):
        """Check if we can clean up if an adopted download was destroyed.
        See the description for adopted_downloads for details.
        """
        self.adopted_downloads -= 1
        log.downloads.debug("Adopted download destroyed, {} left.".format(
            self.adopted_downloads))
        assert self.adopted_downloads >= 0
        if self.adopted_downloads == 0:
            self.deleteLater()

    @pyqtSlot(object)  # DownloadItem
    def adopt_download(self, download):

        self.adopted_downloads += 1
        log.downloads.debug("Adopted download, {} adopted.".format(
            self.adopted_downloads))
        download.destroyed.connect(self.on_adopted_download_destroyed)
        download.adopt_download.connect(self.adopt_download)

    def set_referer(self, req, current_url):

        referer_header_conf = config.val.content.headers.referer

        try:
            if referer_header_conf == 'never':
                req.setRawHeader('Referer'.encode('ascii'), QByteArray())
            elif (referer_header_conf == 'same-domain' and
                  not urlutils.same_domain(req.url(), current_url)):
                req.setRawHeader('Referer'.encode('ascii'), QByteArray())

        except urlutils.InvalidUrlError:
            pass

    @utils.prevent_exceptions(False)
    def createRequest(self, op, req, outgoing_data):

        if proxymod.application_factory is not None:
            proxy_error = proxymod.application_factory.get_error()
            if proxy_error is not None:
                return networkreply.ErrorNetworkReply(
                    req, proxy_error, QNetworkReply.UnknownProxyError,
                    self)

        for header, value in shared.custom_headers(url=req.url()):
            req.setRawHeader(header, value)

        current_url = QUrl()

        if self._tab_id is not None:
            assert self._win_id is not None
            try:
                tab = objreg.get('tab', scope='tab', window=self._win_id,
                                 tab=self._tab_id)
                current_url = tab.url()
            except (KeyError, RuntimeError):

                current_url = QUrl()

        request = interceptors.Request(first_party_url=current_url,
                                       request_url=req.url())
        interceptors.run(request)
        if request.is_blocked:
            return networkreply.ErrorNetworkReply(
                req, HOSTBLOCK_ERROR_STRING, QNetworkReply.ContentAccessDenied,
                self)

        if 'log-requests' in objects.debug_flags:
            operation = debug.qenum_key(QNetworkAccessManager, op)
            operation = operation.replace('Operation', '').upper()
            log.webview.debug("{} {}, first-party {}".format(
                operation,
                req.url().toDisplayString(),
                current_url.toDisplayString()))

        scheme = req.url().scheme()
        if scheme in self._scheme_handlers:
            result = self._scheme_handlers[scheme](req, op, current_url)
            if result is not None:
                result.setParent(self)
                return result

        self.set_referer(req, current_url)
        return super().createRequest(op, req, outgoing_data)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/13/2020 - 12:31 AM
# © 2017 - 2019 DAMGteam. All rights reserved