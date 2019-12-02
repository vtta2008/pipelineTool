# -*- coding: utf-8 -*-
"""

Script Name: Team.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals



from cores.base                         import BaseType
from PyQt5.QtCore                       import QDateTime


class Team(BaseType):

    key                                 = 'Team'

    def __init__(self, id=None, name=None, mode=None, type=None,
                       teamID=None, projectID=None, organisationID=None,
                       startdate=None, enddate=None, details={}):
        super(Team, self).__init__(id, name, mode, type, teamID, projectID, organisationID, startdate, enddate, details)

        if self.startdate is None:
            self.start = QDateTime(self.date.currentDate(), self.time.currentTime())
        else:
            self.start = self.startdate.endDate

        self.end = self.enddate.endDate

        self.update()

        format = self.countter_format()
        self.timer.timeout.connect(self.update)
        if self.key in ['Project', 'Task']:
            self.timer.start(format)

    def dateline(self):
        return self._dateline

    def enddate(self):
        return self._enddate

    def endtime(self):
        return self._endtime

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 4:41 PM
# © 2017 - 2018 DAMGteam. All rights reserved