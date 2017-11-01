# -*- encoding: utf-8 -*-

class SerialMessageReader(object):

    START_BYTE = 7
    STOP_BYTE = 8

    def __init__(self):
        self.messageLength = 2
        self.messageInBuffer = list()
        self.messageInBufferTemp = list()
        self.bufferLength = (self.messageLength + 2) * 2
        for i in range(0, self.bufferLength):
            self.messageInBuffer.append(0)
            self.messageInBufferTemp.append(0)

        self.bufferPosition = 0

    def eatTheSerialData(self, theData):
        print "appending", theData
        for i in range(0, len(theData)):
            self.appendToBuffer(theData[i])
        print "after append", self.messageInBuffer, self.bufferPosition

        foundMessageStartPosition = self.seekForFullMessage()
        print "found message at", foundMessageStartPosition
        if foundMessageStartPosition > -1:
            self.extractMessage(foundMessageStartPosition)
            print "after extraction", self.messageInBuffer, self.bufferPosition

        # self.shiftGivenPositionToBufferStart(2)
        # print "after shift ", self.messageInBuffer

    def appendToBuffer(self, aByte):
        if self.bufferPosition >= self.bufferLength:
            self.shiftGivenPositionToBufferStart(1)
        # if self.bufferPosition < self.bufferLength:
        self.messageInBuffer[self.bufferPosition] = aByte
        self.bufferPosition += 1

    def shiftGivenPositionToBufferStart(self, position):
        # copy and shift
        for i in range(position, self.bufferPosition):
            self.messageInBufferTemp[i - position] = self.messageInBuffer[i]

        # adjust bufferPosition
        self.bufferPosition = self.bufferPosition - position

        # copy back
        for i in range(0, self.bufferPosition):
            self.messageInBuffer[i] = self.messageInBufferTemp[i]

    def seekForFullMessage(self):
        for i in range(0, self.bufferPosition - self.messageLength - 1):
            if self.messageInBuffer[i] == self.START_BYTE:
                possibleMessageEnd = i + self.messageLength + 1
                if self.messageInBuffer[possibleMessageEnd] == self.STOP_BYTE:
                    return i
        return -1

    def extractMessage(self, startPosition):
        message = list()
        for i in range(startPosition + 1, startPosition + self.messageLength + 1):
            message.append(self.messageInBuffer[i])
        self.shiftGivenPositionToBufferStart(startPosition + self.messageLength + 2)
        print "extracted message:", message

if __name__ == "__main__":
    reader = SerialMessageReader()
    reader.eatTheSerialData([7, 4, 3, 8])
    reader.eatTheSerialData([3, 4])
    reader.eatTheSerialData([0, 1, 2, 3, 4, 5, 3, 4, 6, 2, 7, 9, 8, 7, 4, 3, 4, 2, 0])
    reader.eatTheSerialData([3, 4])
    reader.eatTheSerialData([5, 6])
    reader.eatTheSerialData([7, 7])
    reader.eatTheSerialData([1, 2])
    reader.eatTheSerialData([8, 7])
    reader.eatTheSerialData([8, 7])
    reader.eatTheSerialData([8, 7])


