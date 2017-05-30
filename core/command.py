# -*- encoding: utf-8 -*-


"""
Hallo, das sollte in der Hilfe erscheinen.
"""


import datetime
from collections import deque

from PyQt4 import QtCore


# TODO make a good list inheritance
class CommandList(QtCore.QObject):
    """
    Hallo, schöne CommandList.
    """

    """kommt das auch ?"""
    changed = QtCore.pyqtSignal(object)

    def __init__(self):
        """
        schöne Init-Methode ?
        """
        super(CommandList, self).__init__()

        self.cmdList = list()
        self.changedCommands = deque()
        self.pendingCommands = deque()

    def append(self, cmd):
        """
        schöne append-Methode ?
        """
        cmd.valueChanged.connect(self.commandChanged)
        self.cmdList.append(cmd)
        self.changed.emit(self)

    def removeCommand(self, command):
        for i in range(0, len(self.cmdList)):
            if command.id == self.cmdList[i].id:
                self.cmdList.pop(i)
                self.changed.emit(self)
                break


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
        if command.getPendingSendMode() is True:
            self.pendingCommands.append(command)
        else:
            self.changedCommands.append(command)

    def sendPendingCommands(self):
        while len(self.pendingCommands) > 0:
            cmd = self.pendingCommands.popleft()
            if cmd._pendingValue is not None:
                cmd._value = cmd._pendingValue
                cmd.clearPendingValue()
                self.changedCommands.append(cmd)

    def cancelPendingCommands(self):
        while len(self.pendingCommands) > 0:
            cmd = self.pendingCommands.pop()
            cmd.clearPendingValue()

    def sendInitialValues(self):
        for command in self.cmdList:
            command.setValue(command.initialValue)

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
    pendingModeChanged = QtCore.pyqtSignal(object)
    pendingValueCanceled = QtCore.pyqtSignal(object)
    inputMethodChanged = QtCore.pyqtSignal(object)

    # These signals allow the gui elements to signalize the user an uncommanded value change.
    commTimeOut = QtCore.pyqtSignal(object)
    sameValueReceived = QtCore.pyqtSignal(object)
    differentValueReceived = QtCore.pyqtSignal(object)

    VALUE_INPUT = 1
    SWITCH_INPUT = 2
    TOGGLE_INPUT = 3

    def __init__(self):
        super(Command, self).__init__()
        self.id = None
        self.name = "New"
        self.displayName = ""
        self.timeOfSend = datetime.datetime.now()
        self._pendingSendMode = False
        self._pendingValue = None
        self._isSelectedAsActive = True
        self.timeOutDuration = 1000

        self._lowerLimit = 0
        self._upperLimit = 1
        self._value = 0.0
        self.initialValue = 0.0
        self.rawArgumentString = None

        self._inputMethod = Command.VALUE_INPUT

        # This is needed to handle the inaccuracy of float types.
        self.smallNumber = 0.00001

        # On init set the following to something in the past, that is beyond the commCheckTimeOutDuration.
        self.timeOfLastResponse = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.valueOfLastResponse = 0.0

        self.differentValueSuppressionDuration = datetime.timedelta(seconds=1)

        # this timer is reset on each call to checkMicroControllerReturnValue
        self.commCheckTimeOutDuration = 1000
        self.commCheckTimer = QtCore.QTimer()
        self.commCheckTimer.setSingleShot(False)
        self.commCheckTimer.timeout.connect(self.commCheckTimeout)
        self.commCheckTimer.start(self.commCheckTimeOutDuration)

    def getValue(self):
        return self._value

    def setValue(self, value, widgetInstance=None):
        if self._pendingSendMode is True:
            self._setPendingValue(value)
        else:
            self._setDirectValue(value)

        self.valueChanged.emit(self)

        self.valueChangedPerWidget.emit(widgetInstance)

    def _setDirectValue(self, value):
        if self._lowerLimit <= value <= self._upperLimit:
            self._value = value
            self.timeOfSend = datetime.datetime.now()
            # print "Command change id {} name {} value {}".format(self.id, self.name, self._value)
        else:
            raise ValueError("value {} out of allowed range {} - {} for command {}".format(
                value, self._lowerLimit, self._upperLimit, self.name))

    def _setPendingValue(self, value):
        if self._lowerLimit <= value <= self._upperLimit:
            self._pendingValue = value
            # print "Command change pending: id {} name {} value {}".format(self.id, self.name, self._pendingValue)
        else:
            raise ValueError("pending value {} out of allowed range {} - {} for command {}".format(
                value, self._lowerLimit, self._upperLimit, self.name))

    def getPendingValue(self):
        return self._pendingValue

    def clearPendingValue(self):
        self._pendingValue = None
        self.pendingValueCanceled.emit(self)

    def getLowerLimit(self):
        return self._lowerLimit

    def setLowerLimit(self, value, widgetInstance=None):
        self._lowerLimit = value

        # adapt the value to still fit in the limits
        if self._value < self._lowerLimit:
            self.setValue(self._lowerLimit)

            # # This is a bit dirty, as the value is changed from here, but it takes care of the gui elements to update.
            # self.valueChangedPerWidget.emit(self)

            # self.valueChanged.emit(self)
        self.minChangedPerWidget.emit(widgetInstance)

    def getUpperLimit(self):
        return self._upperLimit

    def setUpperLimit(self, value, widgetInstance=None):
        self._upperLimit = value

        # adapt the value to still fit in the limits
        if self._value > self._upperLimit:
            self.setValue(self._upperLimit)

            # # This is a bit dirty, as the value is changed from here, but it takes care of the gui elements to update.
            # self.valueChangedPerWidget.emit(self)
            #
            # self.valueChanged.emit(self)

        self.maxChangedPerWidget.emit(widgetInstance)

    def getPendingSendMode(self):
        return self._pendingSendMode

    def setPendingSendMode(self, value):
        if isinstance(value, bool):
            self._pendingSendMode = value

            # clear a pending value if exists
            if value is False:
                self._pendingValue = None

            self.pendingModeChanged.emit(self)

    def getInputMethod(self):
        return self._inputMethod

    def setInputMethod(self, inputMethod):
        self._inputMethod = inputMethod
        self.inputMethodChanged.emit(self)

    def getIsSelectedAsActive(self):
        return self._isSelectedAsActive

    def setIsSelectedAsActive(self, value):
        self._isSelectedAsActive = value

    def checkMicroControllerReturnValue(self, commandConfirmation):
        self.timeOfLastResponse = datetime.datetime.now()
        self.valueOfLastResponse = commandConfirmation.returnValue

        # check if the returned value equals the own value
        if abs(commandConfirmation.returnValue - self._value) < self.smallNumber:
            self.sameValueReceived.emit(self)
        else:
            if datetime.datetime.now() - self.timeOfSend < self.differentValueSuppressionDuration:
                pass
            else:
                # the value coming from the controller will be set to the gui
                self.adaptLimitsToValue(commandConfirmation.returnValue)
                self._value = commandConfirmation.returnValue
                self.differentValueReceived.emit(self)

    def setValueWithLimitsAdaptation(self, value):
        self.adaptLimitsToValue(value)
        self.setValue(value)

    def commCheckTimeout(self):
        now = datetime.datetime.now()
        if now - self.timeOfLastResponse > datetime.timedelta(milliseconds=self.timeOutDuration):
            self.commTimeOut.emit(self)

    def adaptLimitsToValue(self, value):
        # adjust the allowed limits of the command, so that the given value is inside the limits
        # this is needed, when the user sets limits but the controller sends command values outside these limits.
        if self._lowerLimit > value:
            self._lowerLimit = value
            self.minChangedPerWidget.emit(self)
        if self._upperLimit < value:
            self._upperLimit = value
            self.maxChangedPerWidget.emit(self)


# TODO do i really need this class
class CommandConfirmation():
    def __init__(self):
        self.id = None
        self.returnValue = 0.0
        self.timeOfReceive = None



class CommandProto(QtCore.QObject):
    def __init__(self):
        super(CommandProto, self).__init__()

        self.id = None
        self.value = 0.0
        self.pendingSendMode = False
        self.commandTypeId = None


