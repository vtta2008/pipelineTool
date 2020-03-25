# -*- coding: utf-8 -*-
"""

Script Name: Transform.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                import QTransform

# PLM
from PLM.commons                import SignalManager, SettingManager


class Transform(QTransform):

    Type                        = 'DAMGTRANSFORM'
    key                         = 'Transform'
    _name                       = 'DAMG Transform'
    _copyright                  = __copyright__()

    def __init__(self, *args, **kwargs):
        QTransform.__init__(*args, **kwargs)

        self.signals            = SignalManager(self)
        self.settings           = SettingManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 1:48 AM
# © 2017 - 2018 DAMGteam. All rights reserved