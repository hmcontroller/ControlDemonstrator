# -*- encoding: utf-8 -*-

import datetime

from PyQt4 import QtCore, QtGui

from gui.designerfiles.globalControllerAndView import Ui_GlobalControllerAndView

from core.communicator import CommState

class GlobalControllerAndView(QtGui.QWidget, Ui_GlobalControllerAndView):
    def __init__(self, commandList, communicator, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.commandList = commandList
        self.communicator = communicator
        self.communicator.commStateChanged.connect(self.commStateChanged)
        self.communicator.commandSend.connect(self.reportCommandSend)

        # self.commToggleButton.clicked.connect(self.toggleComm)

        self.pendingSendButton.clicked.connect(self.sendPendingCommands)
        self.pendingCancelButton.clicked.connect(self.cancelPendingCommands)

        self.commOkStyleSheet = """
            QLabel { color: black; font-weight: normal; }
            """
        self.commFailureStyleSheet = """
            QLabel { color: red; font-weight: bold; }
            """

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, QtCore.Qt.black)
        self.messageTextEdit.setAutoFillBackground(True)
        self.messageTextEdit.setPalette(pal)
        self.messageTextEdit.setCurrentFont(QtGui.QFont("Courier New"))
        self.messageTextEdit.setFontPointSize(12)
        self.messageTextEdit.document().setMaximumBlockCount(10000)
        self.messageTextEdit.setTextColor(QtCore.Qt.darkGreen)

        self.singleLineTextEdit.setAutoFillBackground(True)
        self.singleLineTextEdit.setPalette(pal)
        self.singleLineTextEdit.setCurrentFont(QtGui.QFont("Courier New"))
        self.singleLineTextEdit.setFontPointSize(12)
        self.singleLineTextEdit.document().setMaximumBlockCount(1)
        self.singleLineTextEdit.setTextColor(QtCore.Qt.darkGreen)

        self.commStateChanged(self.communicator._commState)

    def commStateChanged(self, commState):
        message = u""
        if commState.state == CommState.COMM_ESTABLISHED:
            message = u"Comm OK"
            self.singleLineTextEdit.setTextColor(QtCore.Qt.darkGreen)
        elif commState.state == CommState.COMM_TIMEOUT:
            message = u"Comm TIMEOUT, waiting..."
            self.singleLineTextEdit.setTextColor(QtCore.Qt.red)
        elif commState.state == CommState.WRONG_CONFIG:
            message = u"config file mismatch"
            self.singleLineTextEdit.setTextColor(QtCore.Qt.red)
        elif commState.state == CommState.NO_CONN:
            message = u"no connection, waiting..."
            self.singleLineTextEdit.setTextColor(QtCore.Qt.red)
        elif commState.state == CommState.UNKNOWN:
            message = u"unknown state"
            self.singleLineTextEdit.setTextColor(QtCore.Qt.red)

        self.singleLineTextEdit.append(message)
        self.singleLineTextEdit.verticalScrollBar().setValue(self.messageTextEdit.verticalScrollBar().maximum())

    def reportCommandSend(self, command):
        now = datetime.datetime.now().strftime("%H:%M:%S.%f")
        name = u""
        if len(command.displayName) > 0:
            name = command.displayName
        else:
            name = command.name
        message = u"{: <15} {: <40} {}".format(now, name, command._value)


        # "#define {:{nameWidth}} {:>{valueWidth}}\n".format

        self.messageTextEdit.append(message)
        self.messageTextEdit.verticalScrollBar().setValue(self.messageTextEdit.verticalScrollBar().maximum())



    # def toggleComm(self):
    #     if self.communicator._commState.communicationPaused is True:
    #         self.communicator.continueCommunication()
    #         self.commToggleButton.setText(u"pause")
    #     else:
    #         self.communicator.pauseCommunication()
    #         self.commToggleButton.setText(u"go")

    def sendPendingCommands(self):
        self.commandList.sendPendingCommands()

    def cancelPendingCommands(self):
        self.commandList.cancelPendingCommands()
