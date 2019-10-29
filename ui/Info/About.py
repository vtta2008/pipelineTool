# -*- coding: utf-8 -*-
"""
Script Name: AboutPlt.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This is a layout which have info about pipeline tools

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from functools import partial

# PtQt5
from PyQt5.QtWidgets                import QApplication, QScrollArea

# Plm
from appData                        import ABOUT
from ui.uikits.Widget               import Widget
from ui.uikits.Button               import Button
from ui.uikits.Label                import Label
from ui.uikits.GridLayout           import GridLayout


# -------------------------------------------------------------------------------------------------------------
""" About Layout """

class About(Widget):

    key = 'About'

    def __init__(self, parent=None):
        super(About, self).__init__(parent)

        # self.setWindowTitle(self.key)
        # self.setWindowIcon(AppIcon(32, self.key))

        self.layout                 = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        # self.resize(800, 600)

    def buildUI(self):
        self.scrollArea             = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content                = Label({'txt':ABOUT, 'alg':'left', 'link': True})

        self.content.setGeometry(0, 0, 800, 600)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt': 'Close', 'tt': 'Close window', 'cl': partial(self.signals.showLayout.emit, self.key, 'hide')})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def main():
    app = QApplication(sys.argv)
    about_layout = About()
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()