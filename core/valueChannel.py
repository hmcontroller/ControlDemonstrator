# -*- encoding: utf-8 -*-
from collections import deque

from PyQt4 import QtCore


class ValueChannel(QtCore.QObject):

    newValueArrived = QtCore.pyqtSignal(object)

    def __init__(self, bufferLength):
        super(ValueChannel, self).__init__()
        self.id = 0
        self.name = ""
        self._values = deque(maxlen=bufferLength)
        self.show = True
        self.colorRgbTuple = (0, 0, 0)

    def append(self, value, suppressSignal=False):
        self._values.append(value)
        if suppressSignal is False:
            self.newValueArrived.emit(value)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def __getitem__(self, index):
        return self._values[index]
