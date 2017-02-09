# -*- encoding: utf-8 -*-
import collections


class MeasurementValues(object):
    def __init__(self, bufferLength):
        self.channels = list()
        self.timeValues = collections.deque(maxlen=bufferLength)