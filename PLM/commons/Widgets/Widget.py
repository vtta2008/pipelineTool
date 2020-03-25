# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__

# PyQt5
from PyQt5.QtWidgets                        import QWidget

# PLM
from PLM.commons.Gui.Icon                   import AppIcon
from PLM.commons.SignalManager              import SignalManager
from PLM.commons.SettingManager             import SettingManager


class Widget(QWidget):

    Type                                    = 'DAMGWIDGET'
    key                                     = 'Widget'
    _name                                   = 'DAMG Widget'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)

        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/08/2018 - 4:12 AM
# © 2017 - 2018 DAMGteam. All rights reserved