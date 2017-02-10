# -*- encoding: utf-8 -*-

from PyQt4 import QtCore


class Command():

    confirmationTimeOut = QtCore.pyqtSignal(object)

    def __init__(self):
        self.id = None
        self._value = 0.0
        self.isConfirmed = False
        self.timeOfSend = None
        self.smallNumber = 0.00000001
        self.confirmationTimer = QtCore.QTimer()
        self.confirmationTimer.setSingleShot(True)
        self.confirmationTimer.timeout.connect(self.confirmationTimeout)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.isConfirmed = False
        self.confirmationTimer.start(1000)

    def checkConfirmation(self, commandConfirmation):
        if abs(commandConfirmation.returnValue - self._value) < self.smallNumber:
            self.isConfirmed = True
            self.confirmationTimer.stop()

    def confirmationTimeout(self):
        self.confirmationTimeOut.emit(self)


class CommandConfirmation():
    def __init__(self):
        self.id = None
        self.returnValue = 0.0
        self.timeOfReceive = None

