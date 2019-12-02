# -*- coding: utf-8 -*-
"""

Script Name: Project.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# Python
import os, json
from playsound import playsound

# PyQt5
from PyQt5.QtCore                       import QDateTime

# PLM
from cores.base                         import BaseType
from appData                            import SOUND_DIR, TASK_DIR, PRJ_DIR, ORG_DIR, TEAM_DIR, TMP_DIR


class Project(BaseType):

    key                                 = 'Project'

    def __init__(self, id=None, name=None, mode=None, type=None,
                       teamID=None, projectID=None, organisationID=None,
                       startdate=None, enddate=None, details={}):
        super(Project, self).__init__(id, name, mode, type, teamID, projectID, organisationID, startdate, enddate, details)

        if self.startdate is None:
            self.start = QDateTime(self.date.currentDate(), self.time.currentTime())
        else:
            self.start = self.startdate.endDate

        self.end = self.enddate.endDate

        self.update()

        format = self.countter_format()
        self.timer.timeout.connect(self.update)
        self.timer.start(format)

    def update(self):
        self.days = self.start.daysTo(self.end)

        self.hours = self.end.time().hour() - self.start.time().hour()
        if self.hours <= 0:
            if self.days > 0:
                self.days = self.days - 1
                self.hours = self.hours + 24

        self.minutes = self.end.time().minute() - self.start.time().minute()
        if self.minutes <= 0:
            if self.hours > 0:
                self.hours = self.hours - 1
                self.minutes = self.minutes + 60

        self.seconds = self.end.time().second() - self.start.time().second()
        if self.seconds <= 0:
            if self.minutes > 0:
                self.minutes = self.minutes - 1
                self.seconds = self.seconds + 60

        self._status = self.get_status()

        if self.days == 0:
            if self.hours == 0:
                if self.minutes == 0:
                    if self.seconds <= 30:
                        pth = os.path.join(SOUND_DIR, 'bell.wav')
                        if not self.play_alarm:
                            playsound(pth)
                            self.play_alarm = True
        if self.days != 0:
            hrs = self.hours + self.days * 24
        else:
            hrs = self.hours

        countdown = '{0}:{1}:{2}'.format(hrs, self.minutes, self.seconds)
        self.countdown.emit(countdown)

        self._start = self.start.toString('dd/MM/yy - hh:mm:ss')
        self._startdate = self.start.date().toString('dd/MM/yy')
        self._starttime = self.start.time().toString('hh:mm:ss')

        self._end = self.end.toString('dd/MM/yy - hh:mm:ss')
        self._enddate = self.end.date().toString('dd/MM/yy')
        self._endtime = self.end.time().toString('hh:mm:ss')

        self.updateData()

    def updateData(self):

        self.dataForm.add('name', self._name)
        self.dataForm.add('id', self._id)
        self.dataForm.add('mode', self._mode)
        self.dataForm.add('type', self._type)
        self.dataForm.add('status', self.get_status())

        self.dataForm.add('teamID', self.teamID)
        self.dataForm.add('projectID', self.projectID)
        self.dataForm.add('organisationID', self.organisationID)

        self.dataForm.add('start', self._start)
        self.dataForm.add('startDate', self._startdate)
        self.dataForm.add('startTime', self._starttime)

        self.dataForm.add('end', self._end)
        self.dataForm.add('enddate', self._enddate)
        self.dataForm.add('endtime', self._endtime)

        self.dataForm.add('details', self.details)

        filePth = os.path.join(PRJ_DIR, '{0}.prj'.format(self._id)).replace('\\', '/')

        with open(filePth, 'w') as f:
            self.dataForm = json.dump(self.dataForm, f, indent=4)

        return self.dataForm

    def get_status(self):
        if self.days < 0:
            self._status = 'Overdued'
        elif self.days == 0:
            if self.hours < 0:
                self._status = 'Overdued'
            elif self.hours == 0:
                if self.minutes <= 0:
                    self._status = 'Overdued'
                else:
                    self._status = 'Urgent'
            else:
                self._status = 'Urgent'
        elif self.days <= 2:
            self._status = 'Tomorrow'
        elif self.days > 2 and self.days < 7:
            self._status = '{0} days'.format(self.days)
        elif self.days == 7:
            self._status = '1 Week'
        else:
            self._status = '{0} days'.format(self.days)

        return self._status


    def dateline(self):
        return self._dateline

    def enddate(self):
        return self._enddate

    def endtime(self):
        return self._endtime

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 1:46 PM
# © 2017 - 2018 DAMGteam. All rights reserved