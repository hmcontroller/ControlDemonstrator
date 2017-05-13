# -*- encoding: utf-8 -*-

from collections import deque

from PyQt4 import QtCore

class ApplicationSettings(QtCore.QObject):

    changed = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ApplicationSettings, self).__init__()
        self.guiUpdateIntervalLengthInMs = 0
        self.receiveMessageIntervalLengthInMs = 0
        self.sendMessageIntervalLengthInMs = 0
        self.bufferLength = 1000
        self.recentProjectFilePathes = deque(maxlen=5)

    def addRecentProjektPath(self, path):
        newRecentPathes = deque(maxlen=5)

        for i in range(0, len(self.recentProjectFilePathes)):
            if not self.recentProjectFilePathes[i] == path:
                newRecentPathes.append(self.recentProjectFilePathes[i])

        self.recentProjectFilePathes = newRecentPathes
        self.recentProjectFilePathes.appendleft(path)

        self.changed.emit(self)



