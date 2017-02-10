# -*- encoding: utf-8 -*-

import socket
import errno
import struct

class UdpCommunicator():
    def __init__(self, ownIp, remoteIp, rxPort, txPort):
        # TODO - check remotePort against txPort or what is more clear
        self.ownIp = ownIp
        self.remoteIp = remoteIp
        self.rxPort = rxPort
        self.txPort = txPort
        self.messageSize = None
        self.messageMap = None

        self.sockRX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRX.bind((self.ownIp, self.rxPort))
        self.sockRX.setblocking(False)
        self.sockRX.settimeout(0)

        self.sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockTX.bind((self.ownIp, self.txPort))
        self.sockTX.setblocking(False)
        self.sockTX.settimeout(0)

    def setMessageMap(self, formatList):
        self.messageMap = formatList
        self.messageSize = self.messageMap[-1].bitPosition + self.messageMap[-1].lengthInBytes
        # print "size", self.messageSize


    def send(self, commandList):
        packedData = self._packCommandList(commandList)
        self.sockTX.sendto(packedData, (self.remoteIp, self.txPort))

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
            except socket.timeout:
                bufferContainsData = False
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    bufferContainsData = False
                else:
                    raise
            else:
                packets.append(data)
        if isPacketReceived:
            self._unpack(packets)
            return self.messageMap
        else:
            return None

    def getData(self):
        pass

    def _unpack(self, rawPackets):
        # TODO - think about how to single source the packet configuration
        # TODO at the time being the source is in types.h -> messageOut in the microcontroller code

        for rawPacket in rawPackets:
            for mData in self.messageMap:
                rawPart = rawPacket[mData.bitPosition : mData.bitPosition + mData.lengthInBytes]
                mData.value = struct.unpack(mData.unpackString, rawPart)[0]


