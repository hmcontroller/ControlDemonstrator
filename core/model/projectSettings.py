# -*- encoding: utf-8 -*-

from PyQt4 import QtCore

from core.model.tabDescription import TabDescription

class ProjectSettings(QtCore.QObject):

    changed = QtCore.pyqtSignal(object)
    frameworkAndInterfaceChanged = QtCore.pyqtSignal(object)
    debugModeChanged = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ProjectSettings, self).__init__()
        self._controllerLoopCycleTimeInUs = 5000
        self._computerIP = "192.168.0.133"
        self._controllerIP = "192.168.0.15"
        self._udpPort = 10000
        self._comPortDescription = ""
        self._comPortBaudRate = 115200
        self._controllerFrameworkAndInterface = "ARDUINO_SERIAL"
        self._tabSettingsDescriptions = [TabDescription()]
        self._pathToControllerCodeFolder = u""
        self._openedFrom = u""
        self._unsavedChanges = False
        self._suppressParameterConfirmation = False
        self._debugMode = False
        self._messageSkipMode = False
        self._recordBufferLength = 1
        self._pauseAfterRecord = False

        # self.debugModeChanged.emit(self)

    def somethingChanged(self):
        self._unsavedChanges = True
        self.changed.emit(self)

    # @property
    # def projectName(self):
    #     return self._projectName
    #
    # @projectName.setter
    # def projectName(self, value):
    #     self._projectName = value
    #     self.somethingChanged()

    @property
    def controllerLoopCycleTimeInUs(self):
        return self._controllerLoopCycleTimeInUs

    @controllerLoopCycleTimeInUs.setter
    def controllerLoopCycleTimeInUs(self, value):
        self._controllerLoopCycleTimeInUs = value
        self.somethingChanged()

    @property
    def computerIP(self):
        return self._computerIP

    @computerIP.setter
    def computerIP(self, value):
        self._computerIP = value
        self.somethingChanged()

    @property
    def controllerIP(self):
        return self._controllerIP

    @controllerIP.setter
    def controllerIP(self, value):
        self._controllerIP = value
        self.somethingChanged()

    @property
    def udpPort(self):
        return self._udpPort

    @udpPort.setter
    def udpPort(self, value):
        self._udpPort = value
        self.somethingChanged()

    @property
    def comPortDescription(self):
        return self._comPortDescription

    @comPortDescription.setter
    def comPortDescription(self, value):
        self._comPortDescription = value
        self.somethingChanged()

    @property
    def controllerFrameworkAndInterface(self):
        return self._controllerFrameworkAndInterface

    @controllerFrameworkAndInterface.setter
    def controllerFrameworkAndInterface(self, value):
        self._controllerFrameworkAndInterface = value
        self.somethingChanged()
        self.frameworkAndInterfaceChanged.emit(self)

    @property
    def comPortBaudRate(self):
        return self._comPortBaudRate

    @comPortBaudRate.setter
    def comPortBaudRate(self, value):
        self._comPortBaudRate = value
        self.somethingChanged()
        self.frameworkAndInterfaceChanged.emit(self)

    @property
    def tabSettingsDescriptions(self):
        return self._tabSettingsDescriptions

    @tabSettingsDescriptions.setter
    def tabSettingsDescriptions(self, value):
        self._tabSettingsDescriptions = value
        self.somethingChanged()

    @property
    def pathToControllerCodeFolder(self):
        return self._pathToControllerCodeFolder

    @pathToControllerCodeFolder.setter
    def pathToControllerCodeFolder(self, value):
        self._pathToControllerCodeFolder = value
        self.somethingChanged()

    @property
    def suppressParameterConfirmation(self):
        return self._suppressParameterConfirmation

    @suppressParameterConfirmation.setter
    def suppressParameterConfirmation(self, value):
        self._suppressParameterConfirmation = value
        self.somethingChanged()

    @property
    def debugMode(self):
        return self._debugMode

    @debugMode.setter
    def debugMode(self, value):
        self._debugMode = value
        self.somethingChanged()
        self.debugModeChanged.emit(self)

    @property
    def messageSkipMode(self):
        return self._messageSkipMode

    @messageSkipMode.setter
    def messageSkipMode(self, value):
        self._messageSkipMode = value
        self.somethingChanged()

    @property
    def recordBufferLength(self):
        return self._recordBufferLength

    @recordBufferLength.setter
    def recordBufferLength(self, value):
        self._recordBufferLength = value
        self.somethingChanged()

    @property
    def pauseAfterRecord(self):
        return self._pauseAfterRecord

    @pauseAfterRecord.setter
    def pauseAfterRecord(self, value):
        self._pauseAfterRecord = value
        self.somethingChanged()

    @property
    def openedFrom(self):
        return self._openedFrom

    @openedFrom.setter
    def openedFrom(self, value):
        self._openedFrom = value
        self.somethingChanged()

    @property
    def unsavedChanges(self):
        return self._unsavedChanges

    @unsavedChanges.setter
    def unsavedChanges(self, value):
        self._unsavedChanges = value

        # prevent setting unsavedChanges to True ;)
        self.changed.emit(self)
