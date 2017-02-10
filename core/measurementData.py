# -*- encoding: utf-8 -*-


class MeasurementData(object):
    def __init__(self):
        self.isEmpty = True
        self.channels = list()
        self.timeValues = None

    def clear(self, time):
        bufferSize = len(self.timeValues)
        for i in range(0, bufferSize):
            self.timeValues.append(time)
        for channel in self.channels:
            for i in range(0, bufferSize):
                channel.values.append(0.0)
