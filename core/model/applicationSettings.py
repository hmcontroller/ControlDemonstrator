# -*- encoding: utf-8 -*-

from collections import deque

from PyQt4 import QtCore

class ApplicationSettings(QtCore.QObject):

    changed = QtCore.pyqtSignal(object)

    bufferLengthChanged = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ApplicationSettings, self).__init__()
        self.currentVersion = 1
        self._guiUpdateIntervalLengthInMs = 40
        self.receiveMessageIntervalLengthInMs = 15
        self.sendMessageIntervalLengthInMs = 10
        self._bufferLength = 5000
        self.maxRecentPathesCount = 10
        self.recentProjectFilePathes = deque(maxlen=self.maxRecentPathesCount)
        self.autoSaveAfterCodeGeneration = True

    @property
    def bufferLength(self):
        return self._bufferLength

    @bufferLength.setter
    def bufferLength(self, value):
        oldLength = self._bufferLength
        self._bufferLength = value
        if oldLength != self._bufferLength:
            self.bufferLengthChanged.emit(self)

    @property
    def guiUpdateIntervalLengthInMs(self):
        return self._guiUpdateIntervalLengthInMs

    @guiUpdateIntervalLengthInMs.setter
    def guiUpdateIntervalLengthInMs(self, value):
        self._guiUpdateIntervalLengthInMs = value
        self.changed.emit(self)

    def addRecentProjectPath(self, path):
        newRecentPathes = deque(maxlen=10)

        for i in range(0, len(self.recentProjectFilePathes)):
            if not self.recentProjectFilePathes[i] == path:
                newRecentPathes.append(self.recentProjectFilePathes[i])

        self.recentProjectFilePathes = newRecentPathes
        self.recentProjectFilePathes.appendleft(path)

        self.changed.emit(self)



