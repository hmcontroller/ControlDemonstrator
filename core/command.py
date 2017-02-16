# -*- encoding: utf-8 -*-
import datetime

from PyQt4 import QtCore

# TODO make a good list inheritance
class CommandList(QtCore.QObject):

    confirmationTimeOut = QtCore.pyqtSignal(object)

    def __init__(self):
        super(CommandList, self).__init__()

        self.cmdList = list()

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

    def __len__(self):
        return len(self.cmdList)

    def __iter__(self):
        return iter(self.cmdList)

    def __getitem__(self, index):
        return self.cmdList[index]

    def __delitem__(self, index):
        self.cmdList.pop(index)





class Command(QtCore.QObject):

    confirmationTimeOut = QtCore.pyqtSignal(object)
    confirmation = QtCore.pyqtSignal(object)
    negativeConfirmation = QtCore.pyqtSignal(object)

    def __init__(self):
        super(Command, self).__init__()
        self.id = None
        self._value = 0.0
        self.name = ""
        self.isConfirmed = False
        self.timeOfSend = None

        self.lowerLimit = 0
        self.upperLimit = 2
        self.smallNumber = 0.00001
        self.negativeConfirmationCounter = 0
        self.timeOfLastResponse = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.valueOfLastResponse = 0.0

        self.confirmationTimer = QtCore.QTimer()
        self.timeOutDuration = 1000
        self.confirmationTimer.setSingleShot(True)
        self.confirmationTimer.timeout.connect(self.confirmationTimeout)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.lowerLimit <= value <= self.upperLimit:
            self._value = value
            self.isConfirmed = False
            self.confirmationTimer.start(self.timeOutDuration)
            print "Command change id {} name {} value {}".format(self.id, self.name, self.value)
        else:
            raise ValueError("value out of allowed range {} - {}".format(self.lowerLimit, self.upperLimit))

    @QtCore.pyqtSlot(object)
    def setValue(self, value):
        self.value = value

    def checkConfirmation(self, commandConfirmation):
        self.timeOfLastResponse = datetime.datetime.now()
        self.valueOfLastResponse = commandConfirmation.returnValue

        if abs(commandConfirmation.returnValue - self._value) < self.smallNumber:
            self.isConfirmed = True
            self.confirmationTimer.stop()
            self.confirmation.emit(self)

    def confirmationTimeout(self):
        now = datetime.datetime.now()
        if now - self.timeOfLastResponse < datetime.timedelta(milliseconds=self.timeOutDuration):
            self.value = self.valueOfLastResponse
            self.negativeConfirmation.emit(self)
        else:
            self.confirmationTimeOut.emit(self)


# TODO do i really need this class
class CommandConfirmation():
    def __init__(self):
        self.id = None
        self.returnValue = 0.0
        self.timeOfReceive = None

