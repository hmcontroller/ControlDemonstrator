# -*- encoding: utf-8 -*-

import socket
import errno
import struct
import serial
import serial.tools.list_ports
from collections import deque
import datetime

from PyQt4 import QtCore

from core.messageData import MessageData
from core.commStateMachine import CommStateMachine
from core.model.receivedData import ReceivedData

class HardwareInterface(QtCore.QObject):

    commandSend = QtCore.pyqtSignal(object)

    def __init__(self, applicationSettings, projectSettings, commands, commStateMachine):
        super(HardwareInterface, self).__init__()

        self._applicationSettings = applicationSettings
        self._projectSettings = projectSettings
        self._commands = commands
        self._messageSize = None
        self._messageMap = None

        self.commStateMachine = commStateMachine

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

    def checkCommTimeOut(self):
        if datetime.datetime.now() - self.commStateMachine.state.timeOfLastReceive > datetime.timedelta(seconds=2):
            self.commStateMachine.doTransit(CommStateMachine.CONNECTION_TIMED_OUT)

    def send(self, commandList):
        raise NotImplementedError()

    def sendPerTimer(self):
        pass

    def sendPendingCommands(self):
        pass

    def receive(self):
        raise NotImplementedError()

    def _packCommand(self, command):
        if command.getValueType() == command.INT_TYPE:
            return struct.pack("<1i1i", command.id, int(command.getValue()))
        if command.getValueType() == command.FLOAT_TYPE:
            return struct.pack("<1i1f", command.id, float(command.getValue()))

    def _unpack(self, rawPackets):
        # TODO - think about how to single source the packet configuration

        unpackedMessages = list()

        for rawPacket in rawPackets:
            if len(rawPacket) != self._messageMap.messageLengthInBytes:
                self.commStateMachine.doTransit(CommStateMachine.MALFORMED_DATA_RECEIVED)
                return unpackedMessages

            currentParameterNumber = 0
            message = list()
            for messagePartInfo in self._messageMap:
                messagePart = MessageData()


                rawPart = rawPacket[messagePartInfo.positionInBytes : messagePartInfo.positionInBytes + messagePartInfo.lengthInBytes]

                messagePart.rawValue = rawPart

                # ATTENTION: dirty HACK ahead
                # unpacking of parameter confirmation takes place at MessageInterpreter.getMicroControllerCommandReturned
                # here, the value is extracted as float

                # if messagePartInfo.name == "parameterNumber":
                #     messagePart.value = struct.unpack(messagePartInfo.unpackString, rawPart)[0]
                #     currentParameterNumber = messagePart.value
                # elif messagePartInfo.name == "parameterValue":
                #     if currentParameterNumber < 0:
                #         messagePart.value = struct.unpack("<f", rawPart)[0]
                #     elif self._commands.getCommandById(currentParameterNumber).getValueType() == \
                #             self._commands.getCommandById(currentParameterNumber).FLOAT_TYPE:
                #         messagePart.value = struct.unpack("<f", rawPart)[0]
                #     elif self._commands.getCommandById(currentParameterNumber).getValueType() == \
                #             self._commands.getCommandById(currentParameterNumber).INT_TYPE:
                #         messagePart.value = struct.unpack("<i", rawPart)[0]
                # else:
                #     messagePart.value = struct.unpack(messagePartInfo.unpackString, rawPart)[0]
                #

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
            self.commStateMachine.doTransit(CommStateMachine.WELL_FORMED_DATA_RECEIVED)
        return unpackedMessages



















class UdpInterface(HardwareInterface):
    def __init__(self, applicationSettings, projectSettings, commands, commState):
        super(UdpInterface, self).__init__(applicationSettings, projectSettings, commands, commState)
        self._socket = None

    def sendRawCommand(self, command):
        pass


    def connectToController(self):
        self.commStateMachine.state.interfaceDescription = u"{}\n{}".format(self._projectSettings.controllerIP, self._projectSettings.udpPort)

        self.commStateMachine.state.play = True

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.bind((self._projectSettings.computerIP, self._projectSettings.udpPort))
            self._socket.setblocking(False)
            self._socket.settimeout(0)
            self.commStateMachine.doTransit(CommStateMachine.CONNECTION_ESTABLISHED)
        except socket.error, e:
            if e.args[0] == errno.WSAEADDRNOTAVAIL:
                self.commStateMachine.doTransit(CommStateMachine.CONNECTION_LOST)
                if self._connectionPollTimer.isActive() is False:
                    self._connectionPollTimer.start(1000)

    def disconnectFromController(self):
        self.commStateMachine.state.play = False
        self._socket.close()

    def send(self, commandList):
        if len(commandList.changedCommands) > 0: # and self._commState.play is True:
            commandToSend = commandList.changedCommands.popleft()
            packedData = self._packCommand(commandToSend)
            self._socket.sendto(packedData, (self._projectSettings.controllerIP, self._projectSettings.udpPort))
            self.commandSend.emit(commandToSend)

    def sendPerTimer(self):
        pass

    def sendPendingCommands(self):
        pass

    def receive(self):
        receivedData = ReceivedData()
        packets = list()

        if self.commStateMachine.state.play is False:
            return receivedData

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
                    self.commStateMachine.doTransit(CommStateMachine.CONNECTION_LOST)
                    if self._connectionPollTimer.isActive() is False:
                        self._connectionPollTimer.start(1000)
                elif e.args[0] == errno.WSAEMSGSIZE:
                    self.commStateMachine.doTransit(CommStateMachine.MALFORMED_DATA_RECEIVED)
                elif e.args[0] == errno.WSAEINVAL:
                    self.commStateMachine.doTransit(CommStateMachine.CONNECTION_LOST)
                    if self._connectionPollTimer.isActive() is False:
                        self._connectionPollTimer.start(1000)
                elif e.args[0] == errno.EBADF:
                    return receivedData
                else:
                    raise
                break

        if len(packets) > 0:
            self.commStateMachine.state.timeOfLastReceive = datetime.datetime.now()

        receivedData.messages = self._unpack(packets)
        for aPacket in packets:
            for aChar in aPacket:
                receivedData.messageAsChars += struct.unpack('c', aChar)[0]
        return receivedData

























class UsbHidInterface(HardwareInterface):
    def __init__(self, applicationSettings, projectSettings, commands, commState):
        super(UsbHidInterface, self).__init__(applicationSettings, projectSettings, commands, commState)

    def send(self, commandList):
        pass

    def receive(self):
        pass






#
# class ODriveInterface(HardwareInterface):
#     def __init__(self, applicationSettings, projectSettings, commands, commState):
#         super(ODriveInterface, self).__init__(applicationSettings, projectSettings, commands, commState)
#
#     def connectToController(self):
#         import core.oDriveLib.core as odrive
#
#         my_drive = odrive.find_any(consider_usb=True, consider_serial=False)
#         print(dir(my_drive.motor0))
#
#     def disconnectFromController(self):
#         pass
#
#     def send(self, commandList):
#         pass
#
#     def receive(self):
#         pass
#
#
#
#








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

    def __init__(self, applicationSettings, projectSettings, commands, commState):
        super(SerialInterface, self).__init__(applicationSettings, projectSettings, commands, commState)



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

        self.outputToRawMonitor = True


    def sendRawCommand(self, command):
        if hasattr(self, "ser"):
            if self.ser.is_open:
                self.ser.write(command)


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

        self.commStateMachine.state.play = True

        if self.ser is not None:
            if self.ser.isOpen():
                self.ser.close()
                # time.sleep(1)

        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            self.commStateMachine.doTransit(CommStateMachine.CONNECTION_LOST)
            if self._connectionPollTimer.isActive() is False:
                self._connectionPollTimer.start(1000)
            return

        portToConnectTo = None
        for port in ports:
            if port.description == self._projectSettings.comPortDescription:
                portToConnectTo = port
                self.commStateMachine.state.interfaceDescription = u"{}".format(port.device)

        if portToConnectTo is None:
            self.commStateMachine.doTransit(CommStateMachine.CONNECTION_LOST)
            if self._connectionPollTimer.isActive() is False:
                self._connectionPollTimer.start(1000)
            return


        self.ser.baudrate = self.projectSettings.comPortBaudRate # 921600 # 115200
        self.ser.port = portToConnectTo.device
        self.ser.timeout = 0.1

        # prohibits restart of the controller
        self.ser.dtr = False

        try:
            self.ser.open()
            self.commStateMachine.doTransit(CommStateMachine.CONNECTION_ESTABLISHED)
        except serial.SerialException:
            self.commStateMachine.doTransit(CommStateMachine.CONNECTION_LOST)
            if self._connectionPollTimer.isActive() is False:
                self._connectionPollTimer.start(1000)

    def getOpenPorts(self):
        return serial.tools.list_ports.comports()

    def disconnectFromController(self):
        self._connectionPollTimer.stop()
        self.commStateMachine.state.play = False
        self.ser.close()

    def send(self, commandList):
        if not self.ser.is_open:
            return

        if len(commandList.changedCommands) > 0:
            commandToSend = commandList.changedCommands.popleft()

            # startByte = struct.pack("<1B", 7)
            packedData = self._packCommand(commandToSend)
            # stopByte = struct.pack("<1B", 57)

            self.ser.write(self.outStartByte)
            for aChar in packedData:
                self.ser.write(aChar)
                # time.sleep(0.0005)
            self.ser.write(self.outStopByte)

            self.commandSend.emit(commandToSend)

    def receive(self):
        receivedData = ReceivedData()
        messages = list()
        messagePositions = list()

        if self.commStateMachine.state.play is False:
            return receivedData

        rawMessageAsChars = ""
        try:
            if self.ser.in_waiting > 0:

                incomingMessage = self.ser.read(self.ser.in_waiting)

                for aByte in incomingMessage:
                    receivedData.messageAsChars += struct.unpack('c', aByte)[0]

                messageToProcess = self.lastMessageRemainder + incomingMessage

                unpackedBytes = self.unpackAsBytes(messageToProcess)
                backupedUnpackedBytes = self.unpackAsBytes(messageToProcess)


                messagePositions.append(self.findNextFullMessagePosition(0, unpackedBytes))



                # message still too short or no message inside, store it for next try
                if len(messageToProcess) < self._messageSize + 2 or messagePositions[0][0] == -1:
                    self.lastMessageRemainder = messageToProcess

                    # prevent overfill of 'buffer'
                    if len(self.lastMessageRemainder) > self._messageMap.messageLengthInBytes * 3:
                        self.lastMessageRemainder = b""
                        self.commStateMachine.doTransit(CommStateMachine.MALFORMED_DATA_RECEIVED)

                    return receivedData


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
            self.commStateMachine.doTransit(CommStateMachine.CONNECTION_LOST)
            if self._connectionPollTimer.isActive() is False:
                self._connectionPollTimer.start(1000)
            return receivedData


        receivedData.messages = self._unpack(messages)

        if len(receivedData.messages) > 0:
            self.commStateMachine.state.timeOfLastReceive = datetime.datetime.now()


        return receivedData



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