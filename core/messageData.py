# -*- encoding: utf-8 -*-


class Message():
    def __init__(self):
        self._messageData = list()
        self.messageLengthInBytes = 0

    def append(self, messageData):
        self._messageData.append(messageData)

    def __len__(self):
        return len(self._messageData)

    def __iter__(self):
        return iter(self._messageData)

    def __getitem__(self, index):
        return self._messageData[index]

    def __delitem__(self, index):
        self._messageData.pop(index)

class MessageData():
    def __init__(self):
        self.positionInBytes = 0
        self.lengthInBytes = 4
        self.dataType = float
        self.unpackString = "<i"
        self.name = None
        self.value = 0
        self.rawValue = 0
        self.isUserChannel = False
        self.userChannelId = None
