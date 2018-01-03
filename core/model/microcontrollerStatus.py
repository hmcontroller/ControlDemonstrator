# -*- encoding: utf-8 -*-

from PyQt4 import QtCore

class MicrocontrollerStatus(QtCore.QObject):

    changed = QtCore.pyqtSignal(object)

    def __init__(self):
        super(MicrocontrollerStatus, self).__init__()
        self._badData = False
        self._skippedTransmission = False

    # def setStatus(self, rawStatusValue):
    #     pass

    def clear(self):
        self.badData = False
        self.skippedTransmission = False

    @property
    def badData(self):
        return self._badData

    @badData.setter
    def badData(self, value):
        if value != self._badData:
            self._badData = value
            self.changed.emit(self)

    @property
    def skippedTransmission(self):
        return self._skippedTransmission

    @skippedTransmission.setter
    def skippedTransmission(self, value):
        if value != self._skippedTransmission:
            self._skippedTransmission = value
            self.changed.emit(self)
