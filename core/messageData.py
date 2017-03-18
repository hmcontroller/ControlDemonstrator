# -*- encoding: utf-8 -*-


class MessageData():
    def __init__(self):
        self.positionInBytes = 0
        self.lengthInBytes = 4
        self.dataType = float
        self.unpackString = "<i"
        self.name = None
        self.value = 0
        self.isUserChannel = False
        self.userChannelId = None
