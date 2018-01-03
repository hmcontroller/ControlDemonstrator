# -*- encoding: utf-8 -*-

import datetime

from PyQt4 import QtCore



class CommState(QtCore.QObject):

    changed = QtCore.pyqtSignal(object)
    interfaceChanged = QtCore.pyqtSignal(object)

    UNKNOWN = 0
    COMM_OK = 1
    WRONG_CONFIG = 2
    NO_CONN = 3
    COMM_TIMEOUT = 4

    PLAY = 10
    PAUSE = 11
    DEBUG = 12
    RECORD = 13

    def __init__(self, projectSettings):
        super(CommState, self).__init__()
        self.projectSettings = projectSettings
        self._play = True
        self._state = self.PLAY
        self._interfaceDescription = u""
        self.timeOfLastReceive = datetime.datetime.now() - datetime.timedelta(hours=1000)
        self._specialFailures = u""

        self.projectSettings.changed.connect(self.debugModeChanged)
        self.debugModeChanged(self.projectSettings)

    def debugModeChanged(self, projectSettings):
        if self.projectSettings.debugMode is True:
            self.state = self.DEBUG
        else:
            self.state = self.UNKNOWN

    @property
    def play(self):
        return self._play

    @play.setter
    def play(self, value):
        if value != self._play:
            self._play = value
            self.changed.emit(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value != self._state:
            self._state = value
            self.changed.emit(self)

    @property
    def interfaceDescription(self):
        return self._interfaceDescription

    @interfaceDescription.setter
    def interfaceDescription(self, value):
        if value != self._interfaceDescription:
            self._interfaceDescription = value
            self.changed.emit(self)

    @property
    def specialFailures(self):
        return self._specialFailures

    @specialFailures.setter
    def specialFailures(self, value):
        if value != self._specialFailures:
            self._specialFailures = value
            self.changed.emit(self)
