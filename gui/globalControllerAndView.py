# -*- encoding: utf-8 -*-

import datetime

from PyQt4 import QtCore, QtGui

from gui.designerfiles.globalControllerAndView import Ui_GlobalControllerAndView
from gui.resources import *
from gui.messageBoard import MessageBoardWidget, MessageBoard

from core.model.commState import CommState
from core.commStateMachine import CommStateMachine

class GlobalControllerAndView(QtGui.QWidget, Ui_GlobalControllerAndView):

    pausePlot = QtCore.pyqtSignal()

    def __init__(self, commandList, communicator, mainWindow, serialMonitor, projectSettings, channels, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.projectSettings = projectSettings
        self.projectSettings.changed.connect(self.projectSettingsChanged)

        self.channels = channels

        self.setMinimumHeight(73)
        self.setMaximumHeight(73)

        self.commStateBlinkTimer = QtCore.QTimer()
        self.commStateBlinkTimer.setSingleShot(True)
        self.commStateBlinkTimer.setInterval(100)
        # self.commStateBlinkTimer.timeout.connect(self.clearCommStateBlink)


        self.commandList = commandList
        self.communicator = communicator
        self.communicator.commStateMachine.state.changed.connect(self.commStateChanged)
        self.communicator.commStateMachine.state.interfaceChanged.connect(self.commInterfaceChanged)
        self.communicator.commandSend.connect(self.reportCommandSend)
        self.communicator.microcontrollerStatus.changed.connect(self.statusFlagsChanged)

        self.serialMonitor = serialMonitor


        if mainWindow is not None:
            self.mainWindow = mainWindow
            self.mainWindow.displayMessage.connect(self.showMessage)

        # self.commToggleButton.clicked.connect(self.toggleComm)




        self.commOkStyleSheet = """
            QLabel { color: black; font-weight: normal; }
            """
        self.commFailureStyleSheet = """
            QLabel { color: red; font-weight: bold; }
            """


        self.sendPendingPixmap = QtGui.QPixmap(sendPendingPath)
        self.sendPendingIcon = QtGui.QIcon(self.sendPendingPixmap)

        self.sendPendingPixmapRed = QtGui.QPixmap(sendPendingRedPath)
        self.sendPendingIconRed = QtGui.QIcon(self.sendPendingPixmapRed)


        self.toolButtonSendPending.setIcon(self.sendPendingIcon)
        self.toolButtonSendPending.setFixedSize(QtCore.QSize(32, 32))
        self.toolButtonSendPending.setIconSize(QtCore.QSize(25, 25))
        self.toolButtonSendPending.clicked.connect(self.sendPendingCommands)



        self.cancelPendingPixmap = QtGui.QPixmap(cancelPendingPath)
        self.cancelPendingIcon = QtGui.QIcon(self.cancelPendingPixmap)
        self.toolButtonCancelPending.setIcon(self.cancelPendingIcon)
        self.toolButtonCancelPending.setFixedSize(QtCore.QSize(32, 32))
        self.toolButtonCancelPending.setIconSize(QtCore.QSize(25, 25))
        self.toolButtonCancelPending.clicked.connect(self.cancelPendingCommands)



        self.serialMonitorPixmap = QtGui.QPixmap(monitorIconPath)
        self.serialIcon = QtGui.QIcon(self.serialMonitorPixmap)
        self.toolButtonSerialMonitor.setIcon(self.serialIcon)
        self.toolButtonSerialMonitor.setFixedSize(QtCore.QSize(32, 32))
        self.toolButtonSerialMonitor.setIconSize(QtCore.QSize(20, 20))
        self.toolButtonSerialMonitor.clicked.connect(self.toggleSerialMonitor)



        self.recordPixmap = QtGui.QPixmap(recordPath)
        self.recordIcon = QtGui.QIcon(self.recordPixmap)

        self.recordDisabledPixmap = QtGui.QPixmap(recordDisabledPath)
        self.recordDisabledIcon = QtGui.QIcon(self.recordDisabledPixmap)

        self.toolButtonRecordMode.setIcon(self.recordDisabledIcon)
        self.toolButtonRecordMode.clicked.connect(self.toggleRecordMode)
        self.toolButtonRecordMode.setFixedSize(QtCore.QSize(32, 32))
        self.toolButtonRecordMode.setIconSize(QtCore.QSize(25, 25))





        self.debugPixmap = QtGui.QPixmap(debugPath)
        self.debugIcon = QtGui.QIcon(self.debugPixmap)

        self.debugDisabledPixmap = QtGui.QPixmap(debugDisabledPath)
        self.debugDisabledIcon = QtGui.QIcon(self.debugDisabledPixmap)

        self.toolButtonDebugMode.setIcon(self.debugDisabledIcon)
        self.toolButtonDebugMode.clicked.connect(self.toggleDebugMode)
        self.toolButtonDebugMode.setFixedSize(QtCore.QSize(32, 32))
        self.toolButtonDebugMode.setIconSize(QtCore.QSize(15, 15))







        self.playPixmap = QtGui.QPixmap(playPath)
        self.playIcon = QtGui.QIcon(self.playPixmap)

        self.pausePixmap = QtGui.QPixmap(pausePath)
        self.pauseIcon = QtGui.QIcon(self.pausePixmap)

        self.toolButtonPlay.setIcon(self.pauseIcon)
        self.toolButtonPlay.clicked.connect(self.togglePlayPause)
        self.toolButtonPlay.setFixedSize(QtCore.QSize(32, 32))
        self.toolButtonPlay.setIconSize(QtCore.QSize(30, 30))


        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, QtCore.Qt.black)
        self.messageTextEdit.setAutoFillBackground(True)
        self.messageTextEdit.setPalette(pal)
        self.messageTextEdit.setCurrentFont(QtGui.QFont("Courier New"))
        self.messageTextEdit.setFontPointSize(12)
        self.messageTextEdit.document().setMaximumBlockCount(5000)
        self.messageTextEdit.setTextColor(QtCore.Qt.darkGreen)

        # self.singleLineTextEdit.setAutoFillBackground(True)
        # self.singleLineTextEdit.setPalette(pal)
        # self.singleLineTextEdit.setCurrentFont(QtGui.QFont("Courier New"))
        # self.singleLineTextEdit.setFontPointSize(12)
        # self.singleLineTextEdit.document().setMaximumBlockCount(3)
        # self.singleLineTextEdit.setTextColor(QtCore.Qt.darkGreen)
        # # self.singleLineTextEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        # self.singleLineTextEdit.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)

        self.messageBoard = MessageBoardWidget(mainWindow)
        self.horizontalLayout.insertWidget(0, self.messageBoard, 0)

        self.commStateChanged(self.communicator.commStateMachine.state)
        self.commInterfaceChanged(self.communicator.commStateMachine.state)
        self.projectSettingsChanged(self.projectSettings)

        self.serialMonitor.signalTogglePlayPause.connect(self.togglePlayPauseFromSerialMonitor)

    def projectSettingsChanged(self, settings):
        if settings.debugMode is True:
            self.toolButtonDebugMode.setIcon(self.debugIcon)
        else:
            self.toolButtonDebugMode.setIcon(self.debugDisabledIcon)

        # if settings.recordMode is True:
        #     self.toolButtonRecordMode.setIcon(self.recordIcon)
        # else:
        #     self.toolButtonRecordMode.setIcon(self.recordDisabledIcon)

    def togglePlayPause(self):
        if self.communicator.commStateMachine.state.play is True:
            self.communicator.disconnectFromController()
            self.communicator.commStateMachine.doTransit(CommStateMachine.PLAY_MODE_DISABLED)
        else:
            self.communicator.connectToController()
            self.communicator.commStateMachine.doTransit(CommStateMachine.PLAY_MODE_ENABLED)

    def togglePlayPauseFromSerialMonitor(self):
        self.togglePlayPause()
        if self.communicator.commStateMachine.state.play is True:
            self.serialMonitor.setPlayButton(False)
        else:
            self.serialMonitor.setPlayButton(True)

    def toggleRecordMode(self):
        pass
        # cmd = self.commandList.getSpecialCommandById(-3)
        # if self.projectSettings.recordMode is True:
        #     self.projectSettings.recordMode = False
        #     cmd.setValue(0)
        #     self.channels.clearWithActualTime()
        #     self.communicator.commStateMachine.doTransit(CommStateMachine.RECORD_MODE_DISABLED)
        # else:
        #     self.projectSettings.recordMode = True
        #     cmd.setValue(1)
        #     self.channels.clearWithActualTime()
        #     self.communicator.commStateMachine.doTransit(CommStateMachine.RECORD_MODE_ENABLED)

    def toggleDebugMode(self):
        if self.projectSettings.debugMode is True:
            self.projectSettings.debugMode = False
            self.communicator.commStateMachine.doTransit(CommStateMachine.DEBUG_MODE_DISABLED)
        else:
            self.projectSettings.debugMode = True
            self.communicator.commStateMachine.doTransit(CommStateMachine.DEBUG_MODE_ENABLED)

    def commStateChanged(self, commState):

        # self.commStateBoxBlink()

        if commState.play is True:
            self.toolButtonPlay.setIcon(self.pauseIcon)
        else:
            self.toolButtonPlay.setIcon(self.playIcon)

        if commState.state == CommState.COMM_OK:
            self.messageBoard.setComStateMessage(MessageBoard.COM_OK)
            self.messageBoard.resetOnceTriggeredFlags()
        elif commState.state == CommState.COMM_TIMEOUT:
            self.messageBoard.setComStateMessage(MessageBoard.TIME_OUT)
        elif commState.state == CommState.WRONG_CONFIG:
            self.messageBoard.setComStateMessage(MessageBoard.WRONG_CONFIG)
        elif commState.state == CommState.NO_CONN:
            self.messageBoard.setComStateMessage(MessageBoard.WAITING)
        elif commState.state == CommState.UNKNOWN:
            self.messageBoard.setComStateMessage(MessageBoard.UNKNOWN)
        elif commState.state == CommState.PLAY:
            self.messageBoard.setComStateMessage(MessageBoard.PLAY)
        elif commState.state == CommState.PAUSE:
            self.messageBoard.setComStateMessage(MessageBoard.PAUSE)
        elif commState.state == CommState.DEBUG:
            self.messageBoard.setComStateMessage(MessageBoard.DEBUG)
        elif commState.state == CommState.RECORD:
            self.messageBoard.setComStateMessage(MessageBoard.RECORD)



    def commInterfaceChanged(self, state):
        self.messageBoard.setComInfo(state.interfaceDescription)

    # def commStateBoxBlink(self):
    #     pal = QtGui.QPalette()
    #     pal.setColor(QtGui.QPalette.Base, QtCore.Qt.red)
    #     # self.singleLineTextEdit.setAutoFillBackground(True)
    #     # self.singleLineTextEdit.setPalette(pal)
    #     self.commStateBlinkTimer.start()
    #
    # def clearCommStateBlink(self):
    #     pal = QtGui.QPalette()
    #     pal.setColor(QtGui.QPalette.Base, QtCore.Qt.black)
    #     # self.singleLineTextEdit.setAutoFillBackground(True)
    #     # self.singleLineTextEdit.setPalette(pal)

    def statusFlagsChanged(self, status):
        if status.badData is True:
            self.messageBoard.badData()
        if status.skippedTransmission is True:
            self.messageBoard.skipped()

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