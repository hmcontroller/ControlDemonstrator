# -*- encoding: utf-8 -*-

import socket
import errno
import struct

from core.messageData import MessageData


class Communicator(object):
    def __init__(self, settings):
        self.settings = settings
        self.messageSize = None
        self.messageMap = None

        self.commandSendBuffer = list()

    def setMessageMap(self, formatList):
        self.messageMap = formatList
        self.messageSize = self.messageMap[-1].positionInBytes + self.messageMap[-1].lengthInBytes
        # print "size", self.messageSize

    def send(self, commandList):
        raise NotImplementedError()

    def receive(self):
        raise NotImplementedError()


class UdpCommunicator(Communicator):
    def __init__(self, settings):
        super(UdpCommunicator, self).__init__(settings)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.settings.computerIP, self.settings.udpPort))
        self.socket.setblocking(False)
        self.socket.settimeout(0)

    def send(self, commandList):
        if len(commandList.changedCommands) > 0:
            commandToSend = commandList.changedCommands.popleft()
            packedData = self._packCommand(commandToSend)
            self.socket.sendto(packedData, (self.settings.controllerIP, self.settings.udpPort))
            print "command send", commandToSend.id, commandToSend.name, commandToSend.getValue()
        # packedData = self._packCommandList(commandList)
        # self.sockTX.sendto(packedData, (self.settings.controllerIP, self.settings.controllerRxPort))

    def _packCommandList(self, commandList):
        formatString = "<{}f".format(len(commandList))
        parameterValues = list()
        for command in commandList:
            parameterValues.append(command.getValue())
        return struct.pack(formatString, *parameterValues)

    def _packCommand(self, command):
        return struct.pack("<1i1f", command.id, command.getValue())

    def receive(self):
        packets = list()
        while True:
            try:
                data, address = self.socket.recvfrom(self.messageSize)
                packets.append(data)
            except socket.timeout:
                break
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    break
                else:
                    raise

        return self._unpack(packets)

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
                messagePart.userChannelId = messagePartInfo.userChannelId

                message.append(messagePart)



            unpackedMessages.append(message)

        return unpackedMessages



class UsbHidCommunicator(Communicator):
    def __init__(self, settings):
        super(UsbHidCommunicator, self).__init__(settings)

        self.settings = settings
        self.messageSize = None
        self.messageMap = None

        self.commandSendBuffer = list()

    def send(self, commandList):
        pass

    def receive(self):
        pass