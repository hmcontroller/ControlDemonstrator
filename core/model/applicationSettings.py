# -*- encoding: utf-8 -*-


class ApplicationSettings():
    def __init__(self):
        self.controllerLoopCycleTimeInUs = 0
        self.bufferLength = 0
        self.guiUpdateIntervalLengthInMs = 0
        self.receiveMessageIntervalLengthInMs = 0
        self.sendMessageIntervalLengthInMs = 0
        self.computerIP = ""
        self.controllerIP = ""
        self.computerRxPort = 1
        self.controllerRxPort = 1