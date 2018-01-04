# -*- encoding: utf-8 -*-

import datetime

from PyQt4 import QtCore, QtGui

from gui.designerfiles.serialMonitor import Ui_SerialMonitor
from gui.resources import *


class SerialMonitor(QtGui.QWidget, Ui_SerialMonitor):

    commandInput = QtCore.pyqtSignal(object)
    signalTogglePlayPause = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.scrollAutomatically = True

        self.palGray = QtGui.QPalette()
        self.palGray.setColor(QtGui.QPalette.Base, QtCore.Qt.black)
        self.palGray.setColor(QtGui.QPalette.Text, QtCore.Qt.lightGray)

        self.palGreen = QtGui.QPalette()
        self.palGreen.setColor(QtGui.QPalette.Base, QtCore.Qt.black)
        self.palGreen.setColor(QtGui.QPalette.Text, QtCore.Qt.darkGreen)


        self.plainTextEdit.setAutoFillBackground(True)
        self.plainTextEdit.setPalette(self.palGray)
        self.plainTextEdit.setFont(QtGui.QFont("Courier New", 12))
        self.plainTextEdit.setMaximumBlockCount(100)

        # self.plainTextEdit.setFontPointSize(12)
        # self.plainTextEdit.setTextColor(QtCore.Qt.lightGray)

        self.checkBoxAutoScroll.setChecked(True)
        self.checkBoxAutoScroll.stateChanged.connect(self.setAutoscrollMode)

        self.pushButtonSend.clicked.connect(self.sendCommand)

        self.playPixmap = QtGui.QPixmap(playPath)
        self.playIcon = QtGui.QIcon(self.playPixmap)

        self.pausePixmap = QtGui.QPixmap(pausePath)
        self.pauseIcon = QtGui.QIcon(self.pausePixmap)

        self.toolButtonPlay.setIcon(self.pauseIcon)
        self.toolButtonPlay.clicked.connect(self.togglePlayPause)
        self.toolButtonPlay.setFixedSize(QtCore.QSize(23, 23))
        self.toolButtonPlay.setIconSize(QtCore.QSize(30, 30))



    def showMessage(self, message, green=False):
        now = datetime.datetime.now().strftime("%H:%M:%S.%f")
        messageToShow = "{} {}\n".format(now, message)
        if green is False:
            self.plainTextEdit.setPalette(self.palGray)
            # self.plainTextEdit.setTextColor(QtCore.Qt.lightGray)
            color = "LightGray"
        else:
            self.plainTextEdit.setPalette(self.palGreen)
            # self.plainTextEdit.setTextColor(QtCore.Qt.darkGreen)
            color = "DarkGreen"

        # html = '<font style="font-size:12pt" face="Courier New" color="{}">{}</font>'.format(color, messageToShow)

        self.plainTextEdit.moveCursor(QtGui.QTextCursor.End)
        # self.plainTextEdit.append(messageToShow)
        self.plainTextEdit.appendPlainText(messageToShow)
        # self.plainTextEdit.insertHtml(html)
        # self.plainTextEdit.insertPlainText(QtCore.QChar(0x2028))
        # self.plainTextEdit.moveCursor(QtGui.QTextCursor.End)

        # self.plainTextEdit.document().setMaximumBlockCount(10)

        # self.plainTextEdit.setMaximumBlockCount(100)

        if self.scrollAutomatically is True:
            self.plainTextEdit.verticalScrollBar().setValue(self.plainTextEdit.verticalScrollBar().maximum())

    def setAutoscrollMode(self, checkState):
        if checkState == QtCore.Qt.Checked:
            self.scrollAutomatically = True
            self.plainTextEdit.verticalScrollBar().setValue(self.plainTextEdit.verticalScrollBar().maximum())
        else:
            self.scrollAutomatically = False

    def sendCommand(self):
        try:
            command = str(self.lineEditCommand.text())
            self.commandInput.emit(command)
            self.showMessage(command, green=True)
        except:
            self.showMessage("not an ASCII command", green=True)
        # command = command.encode('utf-8')

        self.lineEditCommand.clear()

    def togglePlayPause(self):
        self.signalTogglePlayPause.emit()

    def setPlayButton(self, newState):
        if newState is True:
            self.toolButtonPlay.setIcon(self.playIcon)
        else:
            self.toolButtonPlay.setIcon(self.pauseIcon)

    def keyPressEvent(self, QKeyEvent):

        if QKeyEvent.key() == QtCore.Qt.Key_Enter or QKeyEvent.key() == QtCore.Qt.Key_Return:
            self.sendCommand()

        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.togglePlayPause()
