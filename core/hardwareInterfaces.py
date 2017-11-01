# -*- encoding: utf-8 -*-

import socket
import errno
import struct
import serial
import serial.tools.list_ports
import time
from collections import deque
import datetime

from PyQt4 import QtCore

from core.messageData import MessageData
from core.model.commState import CommState

class HardwareInterface(QtCore.QObject):

    commandSend = QtCore.pyqtSignal(object)

    def __init__(self, applicationSettings, projectSettings):
        super(HardwareInterface, self).__init__()

        self._applicationSettings = applicationSettings
        self._projectSettings = projectSettings
        self._messageSize = None
        self._messageMap = None

        self._commState = CommState()

        self._directCommandSendBuffer = deque()
        self._pendingCommandSendBuffer = deque()

        self._sendTimer = QtCore.QTimer()
        self._sendTimer.setSingleShot(False)
        self._sendTimer.timeout.connect(self.sendPerTimer)
        self._sendTimer.start(self._applicationSettings.sendMessageIntervalLengthInMs)

        self._commTimeOutChecker = QtCore.QTimer()
        self._commTimeOutChecker.setSingleShot(False)
        self._commTimeOutChecker.timeout.connect(self.checkCommTimeOut)
        self._commTimeOutChecker.start(500)

        self._connectionPollTimer = QtCore.QTimer()
        self._connectionPollTimer.setSingleShot(True)
        self._connectionPollTimer.timeout.connect(self.connectToController)

    def setMessageMap(self, formatList):
        self._messageMap = formatList
        if len(formatList) > 0:
            self._messageSize = self._messageMap[-1].positionInBytes + self._messageMap[-1].lengthInBytes
        else:
            self._messageSize = 0

    def connectToController(self):
        raise NotImplementedError()

    def disconnectFromController(self):
        raise NotImplementedError()

    def toggleCommunication(self):
        if self._commState.play is False:
            self._commState.play = True
            self.connectToController()
        else:
            self._commState.play = False
            self.disconnectFromController()

    def checkCommTimeOut(self):
        if self._commState.state == CommState.COMM_ESTABLISHED:
            if datetime.datetime.now() - self._commState.timeOfLastReceive > datetime.timedelta(seconds=2):
                if self._commState.state == CommState.COMM_TIMEOUT:
                    return
                else:
                    self._commState.state = CommState.COMM_TIMEOUT
                    # if self._connectionPollTimer.isActive() is False:
                    #     self._connectionPollTimer.start(1000)
            else:
                if self._commState.state != CommState.COMM_ESTABLISHED:
                    self._commState.state = CommState.COMM_ESTABLISHED

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

        unpackedMessages = list()

        for rawPacket in rawPackets:
            if len(rawPacket) != self._messageMap.messageLengthInBytes:
                self._commState.state = CommState.WRONG_CONFIG
                return unpackedMessages
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

        if len(unpackedMessages) > 0:
            self._commState.state = CommState.COMM_ESTABLISHED
        return unpackedMessages


class UdpInterface(HardwareInterface):
    def __init__(self, applicationSettings, projectSettings):
        super(UdpInterface, self).__init__(applicationSettings, projectSettings)
        self._socket = None


    def connectToController(self):

        self._commState.play = True
        self._commState.interfaceDescription = u"UDP via IP {} Port {}".format(self._projectSettings.computerIP, self._projectSettings.udpPort)

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.bind((self._projectSettings.computerIP, self._projectSettings.udpPort))
            self._socket.setblocking(False)
            self._socket.settimeout(0)
            self._commState.state = CommState.COMM_ESTABLISHED
        except socket.error, e:
            if e.args[0] == errno.WSAEADDRNOTAVAIL:
                self._commState.state = CommState.NO_CONN
                if self._connectionPollTimer.isActive() is False:
                    self._connectionPollTimer.start(1000)

    def disconnectFromController(self):

        self._commState.play = False

        self._socket.close()
        self._commState.state = CommState.COMM_PAUSED

    def send(self, commandList):
        if len(commandList.changedCommands) > 0 and self._commState.play is True:
            commandToSend = commandList.changedCommands.popleft()
            packedData = self._packCommand(commandToSend)
            self._socket.sendto(packedData, (self._projectSettings.controllerIP, self._projectSettings.udpPort))
            # print "command send", commandToSend.id, commandToSend.name, commandToSend.getValue()
            self.commandSend.emit(commandToSend)

    def sendPerTimer(self):
        pass

    def sendPendingCommands(self):
        pass

    def receive(self):
        packets = list()

        if self._commState.play is False:
            return packets

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
                    if self._connectionPollTimer.isActive() is False:
                        self._connectionPollTimer.start(1000)
                elif e.args[0] == errno.WSAEMSGSIZE:
                    self._commState.state = CommState.WRONG_CONFIG
                elif e.args[0] == errno.WSAEINVAL:
                    self._commState.state = CommState.NO_CONN
                    if self._connectionPollTimer.isActive() is False:
                        self._connectionPollTimer.start(1000)
                elif e.args[0] == errno.EBADF:
                    return packets
                else:
                    raise
                break

        if len(packets) > 0:
            self._commState.timeOfLastReceive = datetime.datetime.now()
        return self._unpack(packets)




class UsbHidInterface(HardwareInterface):
    def __init__(self, applicationSettings, projectSettings):
        super(UsbHidInterface, self).__init__(applicationSettings, projectSettings)

    def send(self, commandList):
        pass

    def receive(self):
        pass


class SerialInterface(HardwareInterface):

    AVAILABLE_BAUD_RATES = [
        9600,
        38400,
        115200,
        128000,
        230400,
        256000,
        460800,
        921600
    ]

    def __init__(self, applicationSettings, projectSettings):
        super(SerialInterface, self).__init__(applicationSettings, projectSettings)



        projectSettings.changed.connect(self.projectSettingsChanged)
        self.projectSettings = projectSettings

        # self.messageLength = 42

        self.lastMessageRemainder = b""

        self.inStartByte = 7
        self.inStopByte = 8

        self.outStartByte = struct.pack("<1B", 7)
        self.outStopByte = struct.pack("<1B", 8)

        self.noMessageInsideCounter = 0

        self.ser = serial.Serial()


    @QtCore.pyqtSlot(object)
    def projectSettingsChanged(self, newSettings):
        ports = self.getOpenPorts()
        for port in ports:
            if port.description == newSettings.comPortDescription:
                if self.ser.port == port.device:
                    return
        else:
            self.connectToController()

    @QtCore.pyqtSlot(object)
    def connectToController(self):

        self._commState.play = True

        if self.ser is not None:
            if self.ser.isOpen():
                self.ser.close()
                # time.sleep(1)

        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            self._commState.state = CommState.NO_CONN
            if self._connectionPollTimer.isActive() is False:
                self._connectionPollTimer.start(1000)
            return

        # portToConnectTo = ports[0]
        portToConnectTo = None
        for port in ports:
            if port.description == self._projectSettings.comPortDescription:
                portToConnectTo = port
                self._commState.interfaceDescription = u"{}".format(port.description)

        if portToConnectTo is None:
            self._commState.state = CommState.NO_CONN
            if self._connectionPollTimer.isActive() is False:
                self._connectionPollTimer.start(1000)
            return


        # datt müssma nochmal sauber neu machen

        # if portToConnectTo is None and self._portOfferingInProgress is False:
        #     # self.alternatePortAvailable.emit(1)
        #     # self._commState.state = CommState.NO_CONN
        #     self._portOfferingInProgress = True
        # else:
        #     if self._portOfferingInProgress is True:
        #         # self.reEstablishedWantedPort.emit(1)
        #         self._portOfferingInProgress = False
        #
        # if portToConnectTo is None:
        #     return



        self.ser.baudrate = self.projectSettings.comPortBaudRate # 921600 # 115200
        self.ser.port = portToConnectTo.device
        self.ser.timeout = 0.1

        # prohibits restart of the controller
        self.ser.dtr = False

        try:
            self.ser.open()
            self._commState.state = CommState.COMM_ESTABLISHED
        except serial.SerialException:
            self._commState.state = CommState.NO_CONN
            if self._connectionPollTimer.isActive() is False:
                self._connectionPollTimer.start(1000)

    def getOpenPorts(self):
        return serial.tools.list_ports.comports()

    def disconnectFromController(self):

        self._connectionPollTimer.stop()

        self._commState.play = False

        self.ser.close()
        self._commState.state = CommState.COMM_PAUSED

    def send(self, commandList):
        # return
        if len(commandList.changedCommands) > 0 and self._commState.play is True:
            commandToSend = commandList.changedCommands.popleft()

            # startByte = struct.pack("<1B", 7)
            packedData = self._packCommand(commandToSend)
            # stopByte = struct.pack("<1B", 57)

            self.ser.write(self.outStartByte)
            # time.sleep(0.0005)
            for aChar in packedData:
                self.ser.write(aChar)
                # print aChar
                # time.sleep(0.0005)
            self.ser.write(self.outStopByte)
            # self.ser.write(packedData)

            # print "command send", commandToSend.id, commandToSend.name, commandToSend.getValue(), packedData, len(packedData)

            self.commandSend.emit(commandToSend)

    def receive(self):
        messages = list()
        messagePositions = list()

        if self._commState.play is False:
            return messages

        try:
            if self.ser.in_waiting > 0:
                incomingMessage = self.ser.read(self.ser.in_waiting)

                messageToProcess = self.lastMessageRemainder + incomingMessage

                unpackedBytes = self.unpackAsBytes(messageToProcess)
                backupedUnpackedBytes = self.unpackAsBytes(messageToProcess)

                # print incomingMessage

                messagePositions.append(self.findNextFullMessagePosition(0, unpackedBytes))



                # message still too short or no message inside, store it for next try
                if len(messageToProcess) < self._messageSize + 2 or messagePositions[0][0] == -1:
                    self.lastMessageRemainder = messageToProcess

                    # prevent overfill of 'buffer'
                    if len(self.lastMessageRemainder) > self._messageMap.messageLengthInBytes * 3:
                        self.lastMessageRemainder = b""
                        self._commState.state = CommState.WRONG_CONFIG

                    return messages


                while True:
                    lastStopPosition = messagePositions[-1][1]
                    newPosition = self.findNextFullMessagePosition(lastStopPosition, unpackedBytes)
                    if newPosition[0] > -1:
                        messagePositions.append(newPosition)
                    else:
                        self.lastMessageRemainder = messageToProcess[lastStopPosition : ]
                        break

                for messagePosition in messagePositions:
                    start = messagePosition[0]
                    stop = messagePosition[1]
                    messages.append(messageToProcess[start : stop])

        except serial.SerialException:
            # self._commState.state = CommState.NO_CONN
            if self._connectionPollTimer.isActive() is False:
                self._connectionPollTimer.start(1000)
            return list()


        unpackedMessages = self._unpack(messages)

        if len(unpackedMessages) > 0:
            self._commState.timeOfLastReceive = datetime.datetime.now()


        return unpackedMessages



    def findNextPossibleStartByte(self, startPosition, bytes):
        for i, unpackedByte in enumerate(bytes):
            if i < startPosition:
                continue
            if unpackedByte == self.inStartByte:
                return i
        return -1

    def findFirstPossibleStopByte(self, bytes):
        for i, unpackedByte in enumerate(bytes):
            if unpackedByte == self.inStopByte:
                return i
        return -1

    def findFirstMessageBorderPosition(self, bytes):
        for i, unpackedByte in enumerate(bytes):
            if unpackedByte == self.inStopByte:
                if i + 1 < len(bytes):
                    if bytes[i + 1] == self.inStartByte:
                        return i
        return -1

    def findNextFullMessagePosition(self, startPosition, bytes):
        start = -1
        stop = -1
        startBytePos = self.findNextPossibleStartByte(startPosition, bytes)
        if startBytePos > -1:
            remainingBytes = bytes[startBytePos:]
            if len(remainingBytes) > (self._messageSize + 1):
                expectedStopBytePos = startBytePos + self._messageSize + 1
                if bytes[expectedStopBytePos] == self.inStopByte:
                    start = startBytePos + 1
                    stop = expectedStopBytePos
        return start, stop

    def getRemainderOfLastMessagePosition(self, bytes):
        messageBorder = self.findFirstMessageBorderPosition(bytes)
        if messageBorder > -1:
            return 0, messageBorder
        else:
            return 0, len(bytes) - 1

    def unpackAsBytes(self, byteArray):
        unpackedBytes = list()
        for aByte in byteArray:
            unpackedBytes.append(struct.unpack("B", aByte)[0])
        return unpackedBytes