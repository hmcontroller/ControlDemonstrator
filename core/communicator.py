# -*- encoding: utf-8 -*-

import socket
import errno
import struct

from core.messageData import MessageData

class UdpCommunicator():
    def __init__(self, settings):
        # TODO - check remotePort against txPort or what is more clear
        self.settings = settings
        self.messageSize = None
        self.messageMap = None

        self.sockRX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRX.bind((self.settings.computerIP, self.settings.computerRxPort))
        self.sockRX.setblocking(False)
        self.sockRX.settimeout(0)

        self.sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockTX.bind((self.settings.computerIP, self.settings.controllerRxPort))
        self.sockTX.setblocking(False)
        self.sockTX.settimeout(0)

    def setMessageMap(self, formatList):
        self.messageMap = formatList
        self.messageSize = self.messageMap[-1].positionInBytes + self.messageMap[-1].lengthInBytes
        # print "size", self.messageSize

    def send(self, commandList):
        packedData = self._packCommandList(commandList)
        self.sockTX.sendto(packedData, (self.settings.controllerIP, self.settings.controllerRxPort))

    def _packCommandList(self, commandList):
        formatString = "<{}f".format(len(commandList))
        parameterValues = list()
        for command in commandList:
            parameterValues.append(command.value)
        return struct.pack(formatString, *parameterValues)

    def receive(self):
        bufferContainsData = True
        packets = list()
        isPacketReceived = False
        while bufferContainsData is True:
            try:
                data, address = self.sockRX.recvfrom(self.messageSize)
                isPacketReceived = True
                packets.append(data)
            except socket.timeout:
                bufferContainsData = False
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    bufferContainsData = False
                else:
                    raise

        if isPacketReceived:
            return self._unpack(packets)
        else:
            return None

    def getData(self):
        pass

    def _unpack(self, rawPackets):
        # TODO - think about how to single source the packet configuration
        # TODO at the time being the source is in types.h -> messageOut in the microcontroller code

        unpackedMessages = list()

        for rawPacket in rawPackets:
            message = list()
            for messagePartInfo in self.messageMap:
                messagePart = MessageData()
                rawPart = rawPacket[messagePartInfo.positionInBytes : messagePartInfo.positionInBytes + messagePartInfo.lengthInBytes]

                # only these values are changed, the others are just copied
                messagePart.value = struct.unpack(messagePartInfo.unpackString, rawPart)[0]

                messagePart.positionInBytes = messagePartInfo.positionInBytes
                messagePart.lengthInBytes = messagePartInfo.lengthInBytes
                messagePart.dataType = messagePartInfo.dataType
                messagePart.unpackString = messagePartInfo.unpackString
                messagePart.name = messagePartInfo.name
                messagePart.isUserChannel = messagePartInfo.isUserChannel

                message.append(messagePart)



            unpackedMessages.append(message)

        return unpackedMessages

