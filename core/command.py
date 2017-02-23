# -*- encoding: utf-8 -*-
import datetime
from collections import deque

from PyQt4 import QtCore

# TODO make a good list inheritance
class CommandList(QtCore.QObject):
    def __init__(self):
        super(CommandList, self).__init__()

        self.cmdList = list()
        self.changedCommands = deque()

    def append(self, cmd):
        self.cmdList.append(cmd)

    def getCommandById(self, id):
        for cmd in self.cmdList:
            if cmd.id == id:
                return cmd
        raise Exception("Command with id {} not found. Maybe you have to edit the config file.".format(id))

    def getCommandByName(self, name):
        for cmd in self.cmdList:
            if cmd.name == name:
                return cmd
        raise Exception("Command {} not found. Maybe you have to edit the config file.".format(name))

    def commandChanged(self, command):
        self.changedCommands.append(command)

    def __len__(self):
        return len(self.cmdList)

    def __iter__(self):
        return iter(self.cmdList)

    def __getitem__(self, index):
        return self.cmdList[index]

    def __delitem__(self, index):
        self.cmdList.pop(index)





class Command(QtCore.QObject):

    # This signal is intended for the communicator, so that he can send a new value to the microcontroller,
    # It carries an instance of this class.
    valueChanged = QtCore.pyqtSignal(object)

    # These signals should allow all gui elements to update their views, if the values changed per other gui elements.
    # They are intended to serve for the synchronization of all gui elements.
    #
    # The signals carry an instance of the widget, that initiated the command.
    #
    # The widget, that initiated a value change should break a possible loop condition. For that it can check, whether
    # the instance delivered with this signal is its own one.
    valueChangedPerWidget = QtCore.pyqtSignal(object)
    minChangedPerWidget = QtCore.pyqtSignal(object)
    maxChangedPerWidget = QtCore.pyqtSignal(object)

    # These signals allow the gui elements to signalize the user an uncommanded value change.
    commTimeOut = QtCore.pyqtSignal(object)
    sameValueReceived = QtCore.pyqtSignal(object)
    differentValueReceived = QtCore.pyqtSignal(object)

    def __init__(self):
        super(Command, self).__init__()
        self.id = None
        self.name = ""
        self.displayName = None
        self.timeOfSend = None

        self._lowerLimit = 0
        self._upperLimit = 1

        # This is needed to handle the fact, that float values may change a bit during send and receive.
        self.smallNumber = 0.00001

        # On init set the following to something in the past, that is beyond the commCheckTimeOutDuration.
        self.timeOfLastResponse = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.valueOfLastResponse = 0.0

        # This timer is needed, as communication is asynchronous and a command confirmation might take a while.
        # During this time, some old values may arrive from the controller, because of latency.
        self.differentValueSuppressionDuration = 1000
        self.differentValueSuppressionTimer = QtCore.QTimer()
        self.differentValueSuppressionTimer.setSingleShot(True)
        # self.differentValueSuppressionTimer.timeout.connect(self.differentValueSuppressionTimeout)

        # this timer is reset on each call to checkMicroControllerReturnValue
        self.commCheckTimeOutDuration = 1000
        self.commCheckTimer = QtCore.QTimer()
        self.commCheckTimer.setSingleShot(False)
        self.commCheckTimer.timeout.connect(self.commCheckTimeout)
        self.commCheckTimer.start(self.commCheckTimeOutDuration)

        # set this at last
        self._value = 0.0


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.lowerLimit <= value <= self.upperLimit:
            self._value = value
            self.differentValueSuppressionTimer.start(self.differentValueSuppressionDuration)
            print "Command change id {} name {} value {}".format(self.id, self.name, self.value)
        else:
            raise ValueError("value {} out of allowed range {} - {} for command {}".format(
                value, self.lowerLimit, self.upperLimit, self.name))
        self.valueChanged.emit(self)

    @property
    def lowerLimit(self):
        return self._lowerLimit

    @lowerLimit.setter
    def lowerLimit(self, value):
        self._lowerLimit = value

        # adapt the value to still fit in the limits
        if self.value < self._lowerLimit:
            self.value = self.lowerLimit

            # This is a bit dirty, as the value is changed from here, but it takes care of the gui elements to update.
            self.valueChangedPerWidget.emit(self)

            self.valueChanged.emit(self)

    @property
    def upperLimit(self):
        return self._upperLimit

    @upperLimit.setter
    def upperLimit(self, value):
        self._upperLimit = value

        # adapt the value to still fit in the limits
        if self.value > self.upperLimit:
            self.value = self.upperLimit

            # This is a bit dirty, as the value is changed from here, but it takes care of the gui elements to update.
            self.valueChangedFromController.emit(self)

            self.valueChanged.emit(self)

    # @QtCore.pyqtSlot(object)
    # def setValue(self, value):
    #     # this slot is needed, because Signals cannot set properties
    #     # TODO check if anybody still uses this slot
    #     self.value = value

    def checkMicroControllerReturnValue(self, commandConfirmation):
        self.timeOfLastResponse = datetime.datetime.now()
        self.valueOfLastResponse = commandConfirmation.returnValue

        if abs(commandConfirmation.returnValue - self._value) < self.smallNumber:
            self.differentValueSuppressionTimer.stop()
            self.sameValueReceived.emit(self)
        else:
            if self.differentValueSuppressionTimer.isActive():
                pass
            else:
                # the value coming from the controller will be set to the gui
                self.adaptLimitsToValue(commandConfirmation.returnValue)
                self._value = commandConfirmation.returnValue
                self.differentValueReceived.emit(self)

    def commCheckTimeout(self):
        now = datetime.datetime.now()
        if now - self.timeOfLastResponse > datetime.timedelta(milliseconds=self.timeOutDuration):
            self.commTimeOut.emit(self)

    def differentValueSuppressionTimeout(self):
        return
        now = datetime.datetime.now()
        if now - self.timeOfLastResponse < datetime.timedelta(milliseconds=self.timeOutDuration):
            self.adaptLimitsToValue(self.valueOfLastResponse)
            self._value = self.valueOfLastResponse
            self.differentValueReceived.emit(self)

    def adaptLimitsToValue(self, value):
        # adjust the allowed limits of the command, that the given value is inside the limits
        # this is needed, when the user sets limits but the controller sends command values outside these limits.
        if self.lowerLimit > value:
            self.lowerLimit = value
            self.minChangedPerWidget.emit(self)
        if self.upperLimit < value:
            self.upperLimit = value
            self.maxChangedPerWidget.emit(self)


# TODO do i really need this class
class CommandConfirmation():
    def __init__(self):
        self.id = None
        self.returnValue = 0.0
        self.timeOfReceive = None

