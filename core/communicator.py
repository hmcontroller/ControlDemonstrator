# -*- encoding: utf-8 -*-

import socket
import errno
import struct
from collections import deque
import datetime

from PyQt4 import QtCore

from core.messageData import MessageData


class CommState(object):

    UNKNOWN = 0
    COMM_ESTABLISHED = 1
    COMM_PAUSED = 2
    COMM_TIMEOUT = 3
    WRONG_CONFIG = 4
    NO_CONN = 5

    def __init__(self):
        self.state = self.UNKNOWN
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
        self._commState.state = CommState.UNKNOWN

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

        self._connectionPollTimer = QtCore.QTimer()
        self._connectionPollTimer.setSingleShot(True)
        self._connectionPollTimer.timeout.connect(self.connectToController)

    def setMessageMap(self, formatList):
        self._messageMap = formatList
        self._messageSize = self._messageMap[-1].positionInBytes + self._messageMap[-1].lengthInBytes

    def connectToController(self):
        raise NotImplementedError()

    def pauseCommunication(self):
        self._commState.state = CommState.COMM_PAUSED

    def continueCommunication(self):
        self._commState.state = CommState.COMM_ESTABLISHED

    def checkCommTimeOut(self):
        if self._commState.state == CommState.COMM_PAUSED:
            return


        if datetime.datetime.now() - self._commState.timeOfLastReceive > datetime.timedelta(seconds=2):
            if self._commState.state == CommState.COMM_TIMEOUT:
                return
            else:
                self._commState.state = CommState.COMM_TIMEOUT
                self.commStateChanged.emit(self._commState)
        else:
            if self._commState.state != CommState.COMM_ESTABLISHED:
                self._commState.state = CommState.COMM_ESTABLISHED
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
            self._commState.state = CommState.COMM_ESTABLISHED
            self.commStateChanged.emit(self._commState)
        except socket.error, e:
            if e.args[0] == errno.WSAEADDRNOTAVAIL:
                self._commState.state = CommState.NO_CONN
                self.commStateChanged.emit(self._commState)
                self._connectionPollTimer.start(1000)

    def send(self, commandList):
        if len(commandList.changedCommands) > 0 and self._commState.state == CommState.COMM_ESTABLISHED:
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

        # if self._commState.state != CommState.COMM_ESTABLISHED:
        #     return packets

        while True:
            try:
                data, address = self._socket.recvfrom(self._messageSize)
                packets.append(data)
            except socket.timeout:
                break
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    pass
                elif e.args[0] == errno.WSAEADDRNOTAVAIL:
                    self._commState.state = CommState.NO_CONN
                    self.commStateChanged.emit(self._commState)
                    self._connectionPollTimer.start(1000)
                elif e.args[0] == errno.WSAEMSGSIZE:
                    self._commState.state = CommState.WRONG_CONFIG
                    self.commStateChanged.emit(self._commState)
                elif e.args[0] == errno.WSAEINVAL:
                    self._commState.state = CommState.NO_CONN
                    self.commStateChanged.emit(self._commState)
                    self._connectionPollTimer.start(1000)
                else:
                    raise
                break

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


class SerialCommunicator(Communicator):
    def __init__(self, settings):
        super(SerialCommunicator, self).__init__(settings)

    def send(self, commandList):
        pass

    def receive(self):
        pass