# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.designerfiles.globalControllerAndView import Ui_GlobalControllerAndView


class GlobalControllerAndView(QtGui.QWidget, Ui_GlobalControllerAndView):
    def __init__(self, commandList, communicator, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.commandList = commandList
        self.communicator = communicator
        self.communicator.commStateChanged.connect(self.commStateChanged)
        self.communicator.commandSend.connect(self.reportCommandSend)

        self.commToggleButton.clicked.connect(self.toggleComm)
        self.pendingSendButton.clicked.connect(self.sendPendingCommands)
        self.pendingCancelButton.clicked.connect(self.cancelPendingCommands)

        self.commOkStyleSheet = """
            QLabel { color: black; font-weight: normal; }
            """
        self.commFailureStyleSheet = """
            QLabel { color: red; font-weight: bold; }
            """

    def commStateChanged(self, commState):
        if commState.communicationEstablished:
            self.commLabel.setText(u"Comm OK")
            self.commLabel.setStyleSheet(self.commOkStyleSheet)
        if commState.communicationEstablished is False:
            self.commLabel.setText(u"Comm FAILURE")
            self.commLabel.setStyleSheet(self.commFailureStyleSheet)
        if commState.commTimeOut is True:
            self.commLabel.setText(u"Comm TIMEOUT")
            self.commLabel.setStyleSheet(self.commFailureStyleSheet)

    def reportCommandSend(self, command):
        self.messageTextEdit.append(u"Command send: id {} name {} value {}".format(command.id, command.name, command._value))
        self.messageTextEdit.verticalScrollBar().setValue(self.messageTextEdit.verticalScrollBar().maximum())



    def toggleComm(self):
        if self.communicator._commState.communicationPaused is True:
            self.communicator.continueCommunication()
            self.commToggleButton.setText(u"pause")
        else:
            self.communicator.pauseCommunication()
            self.commToggleButton.setText(u"go")

    def sendPendingCommands(self):
        self.commandList.sendPendingCommands()

    def cancelPendingCommands(self):
        self.commandList.cancelPendingCommands()
