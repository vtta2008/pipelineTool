# -*- coding: utf-8 -*-
"""

Script Name: ProjectManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from cores.Task                         import Task
from cores.Project                      import Project
from cores.Team                         import Team
from cores.Organisation                 import Organisation
from cores.Temporary                    import Temporary

from cores.base                         import DateLine
from ui.base import BaseInfo, BaseDetails
from functools                          import partial
from toolkits.Widgets                   import (Widget, Button, VBoxLayout, HBoxLayout, AppIcon)

class BaseManager(Widget):

    key                                 = 'BaseManager'

    def __init__(self, baseType=None, parent=None):
        super(BaseManager, self).__init__(parent)

        self.parent                     = parent
        self.baseType                   = baseType

        if self.baseType == 'TaskManager':
            self.setWindowTitle('Task Manager')
        elif self.baseType == 'ProjectManager':
            self.setWindowTitle('Project Manager')
        elif self.baseType == 'OrganisationManager':
            self.setWindowTitle('Organisation Manager')
        elif self.baseType == 'TeamManager':
            self.setWindowTitle('Team Manager')
        else:
            self.setWindowTitle('Temporary Window')

        self.key = self.baseType
        self.setWindowIcon(AppIcon(32, self.key))

        self.layout = VBoxLayout()
        self.layout.addLayout(self.buildLine1())
        self.layout.addLayout(self.buildLine2())
        self.setLayout(self.layout)

    def buildLine1(self):
        self.baseInfo       = BaseInfo()
        self.baseDetails    = BaseDetails()
        return VBoxLayout({'addWidget': [self.baseInfo, self.baseDetails]})

    def buildLine2(self):
        self.okButton       = Button({'txt': 'Ok', 'cl': self.createNewBaseType})
        self.editButton     = Button({'txt': 'Edit', 'cl': self.editData})
        self.cancelButton   = Button({'txt': 'Cancel', 'cl': partial(self.signals.emit, 'showLayout', self.key, 'hide')})
        return HBoxLayout({'addWidget': [self.okButton, self.editButton, self.cancelButton]})

    def createNewBaseType(self):

        h                   = int(self.baseInfo.hourS.text())
        m                   = int(self.baseInfo.minuteS.text())
        s                   = int(self.baseInfo.secondS.text())
        y                   = int(self.baseInfo.yearS.text())
        mo                  = int(self.baseInfo.monthS.text())
        d                   = int(self.baseInfo.dayS.text())

        startdate           = DateLine(h, m, s, d, mo, y)

        h                   = int(self.baseInfo.hourE.text())
        m                   = int(self.baseInfo.minuteE.text())
        s                   = int(self.baseInfo.secondE.text())
        y                   = int(self.baseInfo.yearE.text())
        mo                  = int(self.baseInfo.monthE.text())
        d                   = int(self.baseInfo.dayE.text())

        enddate             = DateLine(h, m, s, d, mo, y)

        id                  = self.baseInfo.id.text()
        name                = self.baseInfo.name.text()
        mode                = self.baseDetails.mode
        type                = self.baseDetails.type

        teamID              = self.baseInfo.teamID.text()
        projectID           = self.baseInfo.projectID.text()
        organisationID      = self.baseInfo.organisationID.text()

        details             = self.baseDetails.taskDetails.toPlainText()

        if self.baseType == 'TaskManager':
            new             = Task(id, name, mode, type, teamID, projectID, organisationID, startdate, enddate, details)
        elif self.baseType == 'ProjectManager':
            new             = Project(id, name, mode, type, teamID, projectID, organisationID, startdate, enddate, details)
        elif self.baseType == 'OrganisationManager':
            new             = Organisation(id, name, mode, type, teamID, projectID, organisationID, startdate, enddate, details)
        elif self.baseType == 'TeamManager':
            new             = Team(id, name, mode, type, teamID, projectID, organisationID, startdate, enddate, details)
        else:
            new             = Temporary(id, name, mode, type, teamID, projectID, organisationID, startdate, enddate, details)

        self.newDataEvent(new)
        return new

    def editData(self, newData):
        pass

    def newDataEvent(self, newData):
        print(newData)
        self.hide()

    def resizeEvent(self, event):
        h = self.height() - 25
        self.baseInfo.setMaximumHeight(h*2/5)
        self.baseDetails.setMaximumHeight(h*3/5)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 2:02 PM
# © 2017 - 2018 DAMGteam. All rights reserved