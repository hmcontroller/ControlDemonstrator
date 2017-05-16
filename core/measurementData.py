# -*- encoding: utf-8 -*-

from core.valueChannel import ValueChannel

from PyQt4 import QtCore


class MeasurementData(QtCore.QObject):

    channelChanged = QtCore.pyqtSignal(object, object)

    changed = QtCore.pyqtSignal(object)

    def __init__(self, bufferLength):
        super(MeasurementData, self).__init__()
        self.bufferLength = bufferLength
        self.isEmpty = True
        self.channels = list()
        self.timeValues = ValueChannel(self.bufferLength)


    def clear(self, time):
        for i in range(0, self.bufferLength):
            self.timeValues.appendSilently(time)
        for channel in self.channels:
            for i in range(0, self.bufferLength):
                channel.appendSilently(0.0)

    def addChannel(self, channel):
        self.channels.append(channel)
        self.changed.emit(self)

    def removeChannel(self, channel):
        for i in range(0, len(self.channels)):
            if self.channels[i].id == channel.id:
                self.channels.pop(i)
                break
        self.changed.emit(self)

    def channelUpdated(self, channel):
        self.channelChanged.emit(self.timeValues, channel)

    def getChannelById(self, id):
        for channel in self.channels:
            if channel.id == id:
                return channel
        raise Exception("no channel available with id {}".format(id))

    def getChannelByName(self, name):
        for channel in self.channels:
            if channel.name == name:
                return channel
        raise Exception("no channel available with name {}".format(name))

