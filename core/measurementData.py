# -*- encoding: utf-8 -*-

from PyQt4 import QtCore


class MeasurementData(QtCore.QObject):

    channelChanged = QtCore.pyqtSignal(object, object)

    def __init__(self):
        super(MeasurementData, self).__init__()
        self.isEmpty = True
        self.channels = list()
        self.timeValues = None

    def clear(self, time):
        bufferSize = len(self.timeValues)
        for i in range(0, bufferSize):
            self.timeValues.appendSilently(time)
        for channel in self.channels:
            for i in range(0, bufferSize):
                channel.appendSilently(0.0)

    def addChannel(self, channel):
        self.channels.append(channel)
        # channel.newValueArrived.connect(self.channelUpdated)

    def channelUpdated(self, channel):
        self.channelChanged.emit(self.timeValues, channel)

    def getChannelById(self, id):
        for channel in self.channels:
            if channel.id == id:
                return channel

    def getChannelByName(self, name):
        for channel in self.channels:
            if channel.name == name:
                return channel
