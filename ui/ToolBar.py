#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging

# PyQt5
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QApplication

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """
import appData as app

from ui import uirc as rc

from utilities import utils as func
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
# Get apps info config
APPINFO = func.preset_load_appInfo()

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

class ToolBar(QMainWindow):

    def __init__(self, parent=None):

        super(ToolBar, self).__init__(parent)

        self.appInfo = APPINFO
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        # self.tdToolBar = self.make_toolBar("TD", app.CONFIG_TDS)
        self.tdToolBar = self.make_toolBar("TD", app.CONFIG_TDS)
        self.compToolBar = self.make_toolBar("VFX", app.CONFIG_VFX)
        self.artToolBar = self.make_toolBar("ART", app.CONFIG_ART)

        self.showTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.showCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))
        self.showArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        self.tdToolBar.setVisible(self.showTDToolBar)
        self.compToolBar.setVisible(self.showCompToolBar)
        self.artToolBar.setVisible(self.showArtToolBar)

    def make_toolBar(self, name="", apps=[]):
        toolBar = self.addToolBar(name)
        for key in apps:
            if key in self.appInfo:
                toolBar.addAction(rc.ActionProcess(key, self))
        return toolBar

    def show_hide_TDtoolBar(self, param):
        self.settings.setValue("showTDToolbar", func.bool2str(param))
        self.tdToolBar.setVisible(func.str2bool(param))

    def show_hide_ComptoolBar(self, param):
        self.settings.setValue("showCompToolbar", func.bool2str(param))
        self.compToolBar.setVisible(func.str2bool(param))

    def show_hide_ArttoolBar(self, param):
        self.settings.setValue("showArtToolbar", func.bool2str(param))
        self.artToolBar.setVisible(func.str2bool(param))

    def show_hide_AlltoolBar(self, param):
        self.show_hide_TDtoolBar(param)
        self.show_hide_ComptoolBar(param)
        self.show_hide_ArttoolBar(param)

def main():
    app = QApplication(sys.argv)
    toolBar = ToolBar()
    toolBar.show()
    app.exec_()

if __name__=='__main__':
    main()