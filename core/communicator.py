# -*- encoding: utf-8 -*-

import socket
import errno
import struct
from collections import deque
import datetime

from PyQt4 import QtCore

from core.messageData import MessageData


class CommState(object):
    def __init__(self):
        self.communicationEstablished = False
        self.communicationPaused = False
        self.commTimeOut = False
        self.timeOfLastReceive = datetime.datetime.now() - datetime.timedelta(hours=1000)


class Communicator(QtCore.QObject):

    commStateChanged = QtCore.pyqtSignal(object)
    commandSend = QtCore.pyqtSignal(object)

    def __init__(self, settings):
        super(Communicator, self).__init__()

        self._settings = settings
        self._messageSize = None
        self._messageMap = None

        self._commState = CommState()

        self._directCommandSendBuffer = deque()
        self._pendingCommandSendBuffer = deque()

        self._sendTimer = QtCore.QTimer()
        self._sendTimer.setSingleShot(False)
        self._sendTimer.timeout.connect(self.sendPerTimer)
        self._sendTimer.start(settings.sendMessageIntervalLengthInMs)

        self._commTimeOutChecker = QtCore.QTimer()
        self._commTimeOutChecker.setSingleShot(False)
        self._commTimeOutChecker.timeout.connect(self.checkCommTimeOut)
        self._commTimeOutChecker.start(500)

    def setMessageMap(self, formatList):
        self._messageMap = formatList
        self._messageSize = self._messageMap[-1].positionInBytes + self._messageMap[-1].lengthInBytes

    def connectToController(self):
        raise NotImplementedError()

    def pauseCommunication(self):
        self._commState.communicationPaused = True

    def continueCommunication(self):
        self._commState.communicationPaused = False

    def checkCommTimeOut(self):
        if self._commState.communicationPaused is True:
            return


        if datetime.datetime.now() - self._commState.timeOfLastReceive > datetime.timedelta(seconds=2):
            if self._commState.commTimeOut is True:
                return
            else:
                self._commState.commTimeOut = True
                self.commStateChanged.emit(self._commState)
        else:
            if self._commState.commTimeOut is False:
                return
            else:
                self._commState.commTimeOut = False
                self.commStateChanged.emit(self._commState)



    def send(self, commandList):
        raise NotImplementedError()

    def sendPerTimer(self):
        pass

    def sendPendingCommands(self):
        pass

    def receive(self):
        raise NotImplementedError()

    def _packCommand(self, command):
        return struct.pack("<1i1f", command.id, command.getValue())

    def _unpack(self, rawPackets):
        # TODO - think about how to single source the packet configuration
        # TODO at the time being the source is in types.h -> messageOut in the microcontroller code

        unpackedMessages = list()

        for rawPacket in rawPackets:
            message = list()
            for messagePartInfo in self._messageMap:
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


class UdpCommunicator(Communicator):
    def __init__(self, settings):
        super(UdpCommunicator, self).__init__(settings)
        self._socket = None


    def connectToController(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.bind((self._settings.computerIP, self._settings.udpPort))
            self._socket.setblocking(False)
            self._socket.settimeout(0)
            self._commState.communicationEstablished = True
            self._commState.communicationPaused = False

            self.commStateChanged.emit(self._commState)
        except socket.error, e:
            if e.args[0] == 10049:
                self.pauseCommunication()
                self.commStateChanged(self._commState)

    def send(self, commandList):
        if len(commandList.changedCommands) > 0 \
                and self._commState.communicationEstablished is True \
                and self._commState.communicationPaused is False:

            commandToSend = commandList.changedCommands.popleft()
            packedData = self._packCommand(commandToSend)
            self._socket.sendto(packedData, (self._settings.controllerIP, self._settings.udpPort))
            print "command send", commandToSend.id, commandToSend.name, commandToSend.getValue()
            self.commandSend.emit(commandToSend)

    def sendPerTimer(self):
        pass

    def sendPendingCommands(self):
        pass

    def receive(self):
        packets = list()

        if self._commState.communicationEstablished is False:
            return packets

        if self._commState.communicationPaused is True:
            return packets

        while True:
            try:
                data, address = self._socket.recvfrom(self._messageSize)
                packets.append(data)
            except socket.timeout:
                break
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    break
                elif e.args[0] == 10049:
                    self._pauseComm = True

                else:
                    raise

        if len(packets) > 0:
            self._commState.timeOfLastReceive = datetime.datetime.now()
        return self._unpack(packets)




class UsbHidCommunicator(Communicator):
    def __init__(self, settings):
        super(UsbHidCommunicator, self).__init__(settings)

    def send(self, commandList):
        pass

    def receive(self):
        pass