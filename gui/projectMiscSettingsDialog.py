# -*- encoding: utf-8 -*-

import os
import serial.tools.list_ports

from PyQt4 import QtGui, QtCore

from gui.designerfiles.projectMiscSettingsDialog import Ui_ProjectMiscSettingsDialog
from core.model.projectSettings import ProjectSettings
from gui.constants import AVAILABLE_FRAMEWORKS
from core.hardwareInterfaces import SerialInterface


class ProjectMiscSettingsDialog(QtGui.QDialog, Ui_ProjectMiscSettingsDialog):
    def __init__(self, settings, parent=None):
        super(ProjectMiscSettingsDialog, self).__init__(parent)
        self.settings = settings
        self.setupUi(self)


        self.lineEditControllerLoopCycleTime.setValidator(QtGui.QIntValidator())
        self.lineEditUDPPort.setValidator(QtGui.QIntValidator(0, 49151))

        self.comboBoxFrameworkAndInterface.currentIndexChanged.connect(self.showHideLowerSettings)

        self.toolButtonSelectControllerCodeFolder.clicked.connect(self.getFolderPath)

        self.pollComPortsTimer = QtCore.QTimer()
        self.pollComPortsTimer.setSingleShot(False)
        self.pollComPortsTimer.timeout.connect(self.pollForComPorts)
        self.pollComPortsTimer.start(100)

        self.lastComPortsListing = list()

        self.buttonBox.accepted.connect(self.verifyInput)
        self.buttonBox.rejected.connect(self.dialogRejected)

        self.openedDialog = None

    # def nameEditTextChanged(self):
    #     if len(self.lineEditName.text()) == 0:
    #         self.lineEditName.setStyleSheet("QLineEdit {background-color: red;}")
    #         self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
    #     else:
    #         self.lineEditName.setStyleSheet("QLineEdit {background-color: white;}")
    #         self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)

    @staticmethod
    def updateSettings(settings, portChanged=False):

        dialog = ProjectMiscSettingsDialog(settings)

        # set settings to form
        # dialog.lineEditName.setText(dialog.settings.projectName)
        dialog.lineEditControllerLoopCycleTime.setText(unicode(dialog.settings.controllerLoopCycleTimeInUs))
        dialog.lineEditPathToControllerCodeFolder.setText(dialog.settings.pathToControllerCodeFolder)

        indexToSelect = 0
        for i, frameworkAndInterfaceDescription in enumerate(AVAILABLE_FRAMEWORKS):
            dialog.comboBoxFrameworkAndInterface.addItem(frameworkAndInterfaceDescription["displayName"])
            if frameworkAndInterfaceDescription["macroName"] == dialog.settings.controllerFrameworkAndInterface:
                indexToSelect = i
        dialog.comboBoxFrameworkAndInterface.setCurrentIndex(indexToSelect)

        baudRateIndexToSelect = 0
        for i, baudrate in enumerate(SerialInterface.AVAILABLE_BAUD_RATES):
            dialog.comboBoxBaudRate.addItem(str(baudrate))
            if baudrate == dialog.settings.comPortBaudRate:
                baudRateIndexToSelect = i
        dialog.comboBoxBaudRate.setCurrentIndex(baudRateIndexToSelect)

        dialog.lineEditComputerIP.setText(dialog.settings.computerIP)
        dialog.lineEditControllerIP.setText(dialog.settings.controllerIP)
        dialog.lineEditUDPPort.setText(unicode(dialog.settings.udpPort))

        dialog.checkBoxParamConfSuppression.setChecked(dialog.settings.suppressParameterConfirmation)

        dialog.checkBoxDebugMode.setChecked(dialog.settings.debugMode)

        dialog.checkBoxMessageSkipMode.setChecked(dialog.settings.messageSkipMode)
        dialog.lineEditRecordBufferLength.setText(str(dialog.settings.recordBufferLength))
        dialog.checkBoxPauseAfterRecord.setChecked(dialog.settings.pauseAfterRecord)

        dialog.refreshComPortsCombo()
        for i, portDescription in enumerate(dialog.lastComPortsListing):
            if portDescription == dialog.settings.comPortDescription:
                dialog.comboBoxComPort.setCurrentIndex(i)


        if portChanged is True:
            dialog.portChangedLabel.setStyleSheet("QLabel {  color : red; }")
            dialog.portChangedLabel.setVisible(True)
        else:
            dialog.portChangedLabel.setVisible(False)


        answer = dialog.exec_()

        if answer == QtGui.QDialog.Accepted:
            # dialog.settings.projectName = unicode(dialog.lineEditName.text())
            dialog.settings.controllerLoopCycleTimeInUs = int(dialog.lineEditControllerLoopCycleTime.text())
            dialog.settings.pathToControllerCodeFolder = unicode(dialog.lineEditPathToControllerCodeFolder.text())

            frameworkAndInterfaceDescriptionSelected = unicode(dialog.comboBoxFrameworkAndInterface.currentText())
            for description in AVAILABLE_FRAMEWORKS:
                if description["displayName"] == frameworkAndInterfaceDescriptionSelected:
                    dialog.settings.controllerFrameworkAndInterface = description["macroName"]

            baudRateSelected = int(dialog.comboBoxBaudRate.currentText())
            dialog.settings.comPortBaudRate = baudRateSelected


            dialog.settings.computerIP = unicode(dialog.lineEditComputerIP.text())
            dialog.settings.controllerIP = unicode(dialog.lineEditControllerIP.text())
            dialog.settings.udpPort = int(dialog.lineEditUDPPort.text())
            dialog.settings.comPortDescription = unicode(dialog.comboBoxComPort.currentText())

            dialog.settings.suppressParameterConfirmation = dialog.checkBoxParamConfSuppression.isChecked()

            dialog.settings.debugMode = dialog.checkBoxDebugMode.isChecked()

            dialog.settings.messageSkipMode = dialog.checkBoxMessageSkipMode.isChecked()
            try:
                dialog.settings.recordBufferLength = int(dialog.lineEditRecordBufferLength.text())
            except:
                dialog.settings.recordBufferLength = 1
            dialog.settings.pauseAfterRecord = dialog.checkBoxPauseAfterRecord.isChecked()

            return QtGui.QDialog.Accepted
        else:
            return QtGui.QDialog.Rejected


    def verifyInput(self):
        # if len(self.lineEditName.text()) == 0:
        #     return

        self.accept()

    def dialogRejected(self):
        self.reject()

    def showHideLowerSettings(self):
        self.groupBoxSerial.hide()
        self.groupBoxUdp.hide()

        index = self.comboBoxFrameworkAndInterface.currentIndex()
        if "Serial" in AVAILABLE_FRAMEWORKS[index]["displayName"]:
            self.groupBoxSerial.show()
        if "UDP" in AVAILABLE_FRAMEWORKS[index]["displayName"]:
            self.groupBoxUdp.show()

    def pollForComPorts(self):
        ports = serial.tools.list_ports.comports()

        refresh = False

        if len(self.lastComPortsListing) != len(ports):
            refresh = True
        else:
            for i, port in enumerate(ports):
                if port.description != self.lastComPortsListing[i]:
                    refresh = True


        if refresh is True:
            self.refreshComPortsCombo()

    def refreshComPortsCombo(self):
        self.lastComPortsListing = list()
        for port in serial.tools.list_ports.comports():
            self.lastComPortsListing.append(port.description)

        self.comboBoxComPort.clear()
        for portDescription in self.lastComPortsListing:
            self.comboBoxComPort.addItem(portDescription)


    def getFolderPath(self):
        folderSuggestion = u""
        if os.path.isdir(self.settings._pathToControllerCodeFolder):
            folderSuggestion = self.settings._pathToControllerCodeFolder
        elif os.path.isdir(self.settings._openedFrom):
            folderSuggestion = self.settings._openedFrom
        else:
            folderSuggestion = os.path.expanduser("~")

        selectedFolder = QtGui.QFileDialog.getExistingDirectory(self, "Select source code folder", folderSuggestion)
        if len(selectedFolder) == 0:
            return

        self.settings.pathToControllerCodeFolder = selectedFolder

        self.lineEditPathToControllerCodeFolder.setText(selectedFolder)

