# -*- encoding: utf-8 -*-


class MeasurementData(object):
    def __init__(self):
        self.channels = list()
        self.timeValues = None

    def clear(self):
        for i in range(0, len(self.timeValues)):
            self.timeValues.append(0)
        for channel in self.channels:
            for i in range(0, len(self.timeValues)):
                channel.values.append(0)
