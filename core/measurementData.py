# -*- encoding: utf-8 -*-


class MeasurementData(object):
    def __init__(self):
        self.isEmpty = True
        self.channels = list()
        self.timeValues = None

    def clear(self, time):
        bufferSize = len(self.timeValues)
        for i in range(0, bufferSize):
            self.timeValues.append(time, suppressSignal=True)
        for channel in self.channels:
            for i in range(0, bufferSize):
                channel.append(0.0, suppressSignal=True)

    def getChannelById(self, id):
        for channel in self.channels:
            if channel.id == id:
                return channel

    def getChannelByName(self, name):
        for channel in self.channels:
            if channel.name == name:
                return channel
