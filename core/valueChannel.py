# -*- encoding: utf-8 -*-
from collections import deque
import random

from PyQt4 import QtCore

from core.messageData import MessageData

class ValueChannel(QtCore.QObject):

    newValueArrived = QtCore.pyqtSignal(object)
    changed = QtCore.pyqtSignal(object)
    showChanged = QtCore.pyqtSignal(object)
    requestedChanged = QtCore.pyqtSignal(object)
    colorChanged = QtCore.pyqtSignal(object)
    scaleFactorChanged = QtCore.pyqtSignal(object)

    def __init__(self, bufferLength):
        super(ValueChannel, self).__init__()
        self.debugCounter = 0
        self._id = 0
        self._name = "new"
        self._displayName = u""
        self._values = deque(maxlen=bufferLength)
        self._displayScaleFactor = 1.0
        self._show = True
        self._colorRgbTuple = (random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
        self._isRequested = True
        self._messageData = MessageData()

        for n in range(0, bufferLength):
            self.appendSilently(0.0)

    def append(self, value):
        self.appendSilently(value)
        self.newValueArrived.emit(self)
        self.debugCounter += 1
        if self.debugCounter > 1000:
            self.debugCounter = 0

    def appendSilently(self, value):
        self._values.append(value)

    def setBufferLength(self, length):
        self._values = deque(maxlen=length)
        # for i in range(0, length):
        #     self.appendSilently(0.0)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        self.changed.emit(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.changed.emit(self)

    @property
    def displayName(self):
        return self._displayName

    @displayName.setter
    def displayName(self, value):
        self._displayName = value
        self.changed.emit(self)

    @property
    def displayScaleFactor(self):
        return self._displayScaleFactor

    @displayScaleFactor.setter
    def displayScaleFactor(self, value):
        self._displayScaleFactor = value
        self.scaleFactorChanged.emit(self)

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, value):
        self._show = value
        self.showChanged.emit(self)

    @property
    def colorRgbTuple(self):
        return self._colorRgbTuple

    @colorRgbTuple.setter
    def colorRgbTuple(self, value):
        self._colorRgbTuple = value
        self.colorChanged.emit(self)

    @property
    def isRequested(self):
        return self._isRequested

    @isRequested.setter
    def isRequested(self, value):
        self._isRequested = value
        self.changed.emit(self)
        self.requestedChanged.emit(self)

    @property
    def messageData(self):
        return self._messageData

    @messageData.setter
    def messageData(self, value):
        self._messageData = value
        self.changed.emit(self)



    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def __getitem__(self, index):
        return self._values[index]
