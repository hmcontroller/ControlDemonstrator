# -*- encoding: utf-8 -*-

from PyQt4 import QtCore


class UnsavedChecker(QtCore.QObject):

    unsavedChanges = QtCore.pyqtSignal(object)

    def __init__(self, projectSettings):
        super(UnsavedChecker, self).__init__()

        self.projectSettings = projectSettings

        self.checkTimer = QtCore.QTimer()
        self.checkTimer.setSingleShot(True)
        self.checkTimer.setInterval(1000)
        self.checkTimer.timeout.connect(self.check)


    def check(self):
        pass