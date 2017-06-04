# -*- encoding: utf-8 -*-

from collections import deque

from PyQt4 import QtCore

class ApplicationSettings(QtCore.QObject):

    changed = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ApplicationSettings, self).__init__()
        self.currentVersion = 1
        self.guiUpdateIntervalLengthInMs = 40
        self.receiveMessageIntervalLengthInMs = 15
        self.sendMessageIntervalLengthInMs = 10
        self.bufferLength = 5000
        self.recentProjectFilePathes = deque(maxlen=10)
        self.autoSaveAfterCodeGeneration = True

    def addRecentProjectPath(self, path):
        newRecentPathes = deque(maxlen=10)

        for i in range(0, len(self.recentProjectFilePathes)):
            if not self.recentProjectFilePathes[i] == path:
                newRecentPathes.append(self.recentProjectFilePathes[i])

        self.recentProjectFilePathes = newRecentPathes
        self.recentProjectFilePathes.appendleft(path)

        self.changed.emit(self)



