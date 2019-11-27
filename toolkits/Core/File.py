# -*- coding: utf-8 -*-
"""

Script Name: File.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os, sys

from PyQt5.QtCore           import QFile

from toolkits                               import getCopyright, getSetting, getSignals
from appData                                import QSS_DIR

class FileBase(QFile):

    Type                                    = 'DAMGFILE'
    key                                     = 'FileBase'
    _name                                   = 'DAMG File Base'
    _copyright                              = getCopyright()
    _filePath                               = None

    def __init__(self):
        super(FileBase, self).__init__()

        self.signals                        = getSignals(self)
        self.settings                       = getSetting(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                          = val

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, val):
        self._filePath                      = val

class QssFile(FileBase):

    key                                     = 'QssFile'

    qssPths = dict(dark                     = os.path.join(QSS_DIR, 'darkstyle.qss'),
                   chacoal                  = os.path.join(QSS_DIR, 'chacoal.qss'),
                   bright                   = os.path.join(QSS_DIR, 'brightstyle.qss'),
                   nuker                    = os.path.join(QSS_DIR, 'nuker.qss'),
                   )

    def __init__(self, style):
        super(QssFile, self).__init__()

        self._style = style
        self._filePath = self.qssPths[self._style]
        self.setFileName(self._filePath)

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, val):
        self._style                         = val

class File(FileBase):

    key                                     = 'File'

    def __init__(self, filePth=None):

        self._filePath                      = filePth
        self.setFileName(self._filePath)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/11/2019 - 4:56 PM
# © 2017 - 2018 DAMGteam. All rights reserved