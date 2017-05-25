# -*- encoding: utf-8 -*-

import serial.tools.list_ports

from PyQt4 import QtGui, QtCore

from gui.designerfiles.projectMiscSettingsDialog import Ui_ProjectMiscSettingsDialog
from core.model.projectSettings import ProjectSettings
from gui.constants import AVAILABLE_FRAMEWORKS


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
        selectedFolder = QtGui.QFileDialog.getExistingDirectory(self)
        if len(selectedFolder) == 0:
            return

        self.settings.pathToControllerCodeFolder = selectedFolder

        self.lineEditPathToControllerCodeFolder.setText(selectedFolder)

    def updateSettings(self):

        # self.settings = ProjectSettings()

        # set settings to form
        # self.lineEditName.setText(self.settings.projectName)
        self.lineEditControllerLoopCycleTime.setText(unicode(self.settings.controllerLoopCycleTimeInUs))
        self.lineEditPathToControllerCodeFolder.setText(self.settings.pathToControllerCodeFolder)

        indexToSelect = 0
        for i, frameworkAndInterfaceDescription in enumerate(AVAILABLE_FRAMEWORKS):
            self.comboBoxFrameworkAndInterface.addItem(frameworkAndInterfaceDescription["displayName"])
            if frameworkAndInterfaceDescription["macroName"] == self.settings.controllerFrameworkAndInterface:
                indexToSelect = i
        self.comboBoxFrameworkAndInterface.setCurrentIndex(indexToSelect)


        self.lineEditComputerIP.setText(self.settings.computerIP)
        self.lineEditControllerIP.setText(self.settings.controllerIP)
        self.lineEditUDPPort.setText(unicode(self.settings.udpPort))

        self.refreshComPortsCombo()
        for i, portDescription in enumerate(self.lastComPortsListing):
            if portDescription == self.settings.comPortDescription:
                self.comboBoxComPort.setCurrentIndex(i)



        answer = self.exec_()

        if answer == QtGui.QDialog.Accepted:
            # self.settings.projectName = unicode(self.lineEditName.text())
            self.settings.controllerLoopCycleTimeInUs = int(self.lineEditControllerLoopCycleTime.text())
            self.settings.pathToControllerCodeFolder = unicode(self.lineEditPathToControllerCodeFolder.text())

            frameworkAndInterfaceDescriptionSelected = unicode(self.comboBoxFrameworkAndInterface.currentText())
            for description in AVAILABLE_FRAMEWORKS:
                if description["displayName"] == frameworkAndInterfaceDescriptionSelected:
                    self.settings.controllerFrameworkAndInterface = description["macroName"]

            self.settings.computerIP = unicode(self.lineEditComputerIP.text())
            self.settings.controllerIP = unicode(self.lineEditControllerIP.text())
            self.settings.udpPort = int(self.lineEditUDPPort.text())
            self.settings.comPortDescription = unicode(self.comboBoxComPort.currentText())
            return QtGui.QDialog.Accepted
        else:
            return QtGui.QDialog.Rejected
