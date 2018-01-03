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

from core.hardwareInterfaces import UdpInterface, UsbHidInterface, SerialInterface
from core.model.microcontrollerStatus import MicrocontrollerStatus
from core.commStateMachine import CommStateMachine
from core.model.commState import CommState

from gui.constants import AVAILABLE_FRAMEWORKS


class Communicator(QtCore.QObject):

    commandSend = QtCore.pyqtSignal(object)
    commStateChanged = QtCore.pyqtSignal(object)

    def __init__(self, applicationSettings, projectSettings, messageMap, commands):
        super(Communicator, self).__init__()

        self._applicationSettings = applicationSettings
        self._projectSettings = projectSettings
        self._commands = commands
        self._messageSize = None
        self._messageMap = None

        self.microcontrollerStatus = MicrocontrollerStatus()
        self.commStateMachine = CommStateMachine(CommState(projectSettings))
        # self.commStateMachine.state.changed.emit(self.commStateMachine.state)

        self.interface = SerialInterface(applicationSettings, projectSettings, commands, self.commStateMachine)
        self.setInterface(messageMap)

        # self.commState = CommState()
        # self.commState.changed.connect(self.commStateChanged)

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

    def sendRawCommand(self, command):
        self.interface.sendRawCommand(command)


    def setInterface(self, messageMap):
        self.disconnectFromController()
        self.microcontrollerStatus.clear()
        for availableFramework in AVAILABLE_FRAMEWORKS:
            if self._projectSettings.controllerFrameworkAndInterface == availableFramework["macroName"]:
                if availableFramework["interface"] == "UDP":
                    self.interface = UdpInterface(self._applicationSettings, self._projectSettings, self._commands, self.commStateMachine)
                    self.interface.setMessageMap(messageMap)
                    self.interface.commStateMachine.state.changed.connect(self.commStateChanged)
                    self.interface.commandSend.connect(self.commandSend)
                    self.connectToController()
                    return
                elif availableFramework["interface"] == "SERIAL":
                    self.interface = SerialInterface(self._applicationSettings, self._projectSettings, self._commands, self.commStateMachine)
                    self.interface.setMessageMap(messageMap)
                    self.interface.commStateMachine.state.changed.connect(self.commStateChanged)
                    self.interface.commandSend.connect(self.commandSend)
                    self.connectToController()
                    return



    def setMessageMap(self, formatList):
        self.interface.setMessageMap(formatList)

    def connectToController(self):
        self.interface.connectToController()

    def disconnectFromController(self):
        self.interface.disconnectFromController()

    def toggleCommunication(self):
        self.interface.toggleCommunication()

    def checkCommTimeOut(self):
        self.interface.checkCommTimeOut()

    def send(self, commandList):
        self.interface.send(commandList)

    def sendPerTimer(self):
        self.interface.sendPerTimer()

    def sendPendingCommands(self):
        self.interface.sendPendingCommands()

    def receive(self):
        return self.interface.receive()

    @property
    def commState(self):
        return self.interface._commState

    @commState.setter
    def commState(self, value):
        self.interface._commState = value