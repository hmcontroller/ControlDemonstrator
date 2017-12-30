# -*- encoding: utf-8 -*-

from core.valueChannel import ValueChannel

from PyQt4 import QtCore


class MeasurementData(QtCore.QObject):

    channelChanged = QtCore.pyqtSignal(object, object)

    channelConfigChanged = QtCore.pyqtSignal(object)

    changed = QtCore.pyqtSignal(object)

    bufferLengthChanged = QtCore.pyqtSignal(object)

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

    def clearWithActualTime(self):
        try:
            latest = self.timeValues[len(self.timeValues) - 1]
        except:
            latest = 0.0
        self.clear(latest)
        for channel in self.channels:
            self.channelChanged.emit(self.timeValues, channel)

    def addChannel(self, channel):
        self.channels.append(channel)
        channel.changed.connect(self.channelConfigurationChanged)
        self.changed.emit(self)

    def removeChannel(self, channel):
        for i in range(0, len(self.channels)):
            if self.channels[i].id == channel.id:
                self.channels.pop(i)
                break
        self.changed.emit(self)

    def channelUpdated(self, channel):
        self.channelChanged.emit(self.timeValues, channel)

    def channelConfigurationChanged(self, channel):
        self.channelConfigChanged.emit(channel)

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

    def actualizeBufferLength(self, length):
        self.bufferLength = length

        oldBiggestTime = self.timeValues[-1]

        self.timeValues.setBufferLength(self.bufferLength)
        for channel in self.channels:
            channel.setBufferLength(self.bufferLength)

        self.clear(oldBiggestTime)

        # TODO attention dirty hack
        # if doing so, the message interpreter sets correct zero values on next message arrival
        self.isEmpty = True


        self.bufferLengthChanged.emit(self.bufferLength)

