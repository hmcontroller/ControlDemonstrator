# -*- encoding: utf-8 -*-

import datetime

from PyQt4 import QtCore, QtGui

from gui.designerfiles.globalControllerAndView import Ui_GlobalControllerAndView
from gui.resources import *


from core.communicator import CommState

class GlobalControllerAndView(QtGui.QWidget, Ui_GlobalControllerAndView):
    def __init__(self, commandList, communicator, mainWindow, serialMonitor, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.commStateBlinkTimer = QtCore.QTimer()
        self.commStateBlinkTimer.setSingleShot(True)
        self.commStateBlinkTimer.setInterval(100)
        self.commStateBlinkTimer.timeout.connect(self.clearCommStateBlink)


        self.commandList = commandList
        self.communicator = communicator
        self.communicator.commStateChanged.connect(self.commStateChanged)
        self.communicator.commandSend.connect(self.reportCommandSend)

        self.serialMonitor = serialMonitor


        if mainWindow is not None:
            self.mainWindow = mainWindow
            self.mainWindow.displayMessage.connect(self.showMessage)

        # self.commToggleButton.clicked.connect(self.toggleComm)


        self.pushButtonSerialMonitor.clicked.connect(self.toggleSerialMonitor)

        self.pendingSendButton.clicked.connect(self.sendPendingCommands)
        self.pendingCancelButton.clicked.connect(self.cancelPendingCommands)

        self.commOkStyleSheet = """
            QLabel { color: black; font-weight: normal; }
            """
        self.commFailureStyleSheet = """
            QLabel { color: red; font-weight: bold; }
            """


        self.playPixmap = QtGui.QPixmap(playPath)
        self.playIcon = QtGui.QIcon(self.playPixmap)

        self.pausePixmap = QtGui.QPixmap(pausePath)
        self.pauseIcon = QtGui.QIcon(self.pausePixmap)

        self.toolButton.setIcon(self.pauseIcon)
        self.toolButton.clicked.connect(self.togglePlayPause)
        self.toolButton.setIconSize(QtCore.QSize(25, 25))


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
        self.singleLineTextEdit.document().setMaximumBlockCount(3)
        self.singleLineTextEdit.setTextColor(QtCore.Qt.darkGreen)
        # self.singleLineTextEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.singleLineTextEdit.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)



        self.commStateChanged(self.communicator.commState)

    def togglePlayPause(self):
        if self.communicator.commState._play is True:
            self.communicator.disconnectFromController()
        else:
            self.communicator.connectToController()

    def commStateChanged(self, commState):

        self.commStateBoxBlink()

        if commState.play is True:
            self.toolButton.setIcon(self.pauseIcon)
        else:
            self.toolButton.setIcon(self.playIcon)

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
        elif commState.state == CommState.COMM_PAUSED:
            message = u"Com paused"
            self.singleLineTextEdit.setTextColor(QtCore.Qt.darkGreen)

        self.singleLineTextEdit.append(message)

        self.singleLineTextEdit.setTextColor(QtCore.Qt.darkGreen)
        self.singleLineTextEdit.append(commState.interfaceDescription)

        self.singleLineTextEdit.setTextColor(QtCore.Qt.red)
        self.singleLineTextEdit.append(commState.specialFailures)

        # if commState.specialFailures

        self.singleLineTextEdit.verticalScrollBar().setValue(self.singleLineTextEdit.verticalScrollBar().minimum())

        self.showMessage(message, kindOfMessage="softWarning")


    def commStateBoxBlink(self):
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, QtCore.Qt.red)
        self.singleLineTextEdit.setAutoFillBackground(True)
        self.singleLineTextEdit.setPalette(pal)
        self.commStateBlinkTimer.start()

    def clearCommStateBlink(self):
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, QtCore.Qt.black)
        self.singleLineTextEdit.setAutoFillBackground(True)
        self.singleLineTextEdit.setPalette(pal)


    def reportCommandSend(self, command):

        name = u""
        if len(command.displayName) > 0:
            name = command.displayName
        else:
            name = command.name
        message = u"{: <40} {}".format(name, command._value)


        # "#define {:{nameWidth}} {:>{valueWidth}}\n".format

        self.showMessage(message)

    def sendPendingCommands(self):
        self.commandList.sendPendingCommands()

    def cancelPendingCommands(self):
        self.commandList.cancelPendingCommands()

    def showMessage(self, message, kindOfMessage="normal"):
        now = datetime.datetime.now().strftime("%H:%M:%S.%f")
        messageToShow = u"{} {}".format(now, message)
        if kindOfMessage == "normal":
            self.messageTextEdit.setTextColor(QtCore.Qt.darkGreen)
        elif kindOfMessage == "softWarning":
            self.messageTextEdit.setTextColor(QtGui.QColor(255, 140, 0))
        elif kindOfMessage == "warning":
            self.messageTextEdit.setTextColor(QtCore.Qt.red)
        else:
            self.messageTextEdit.setTextColor(QtCore.Qt.lightGray)

        self.messageTextEdit.append(messageToShow)
        self.messageTextEdit.verticalScrollBar().setValue(self.messageTextEdit.verticalScrollBar().maximum())

    def toggleSerialMonitor(self):
        if self.serialMonitor.isVisible():
            self.serialMonitor.hide()
        else:
            self.serialMonitor.show()