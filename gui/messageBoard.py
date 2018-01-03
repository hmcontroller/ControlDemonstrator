# -*- encoding: utf-8 -*-
import datetime

from PyQt4 import QtCore

from gui.constants import *
from gui.graphicItems.commandWidgets.genericCommand import GenericCommandWithoutMinMaxEdit


class MessageBoardWidget(QtGui.QWidget):

    parameterChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, mainWindow, parent=None):
        super(MessageBoardWidget, self).__init__(parent)

        self.mainWindow = mainWindow

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)

        self.mainLayout = QtGui.QHBoxLayout(self)
        self.mainLayout.setMargin(0)


        self.graphicsView = QtGui.QGraphicsView()
        self.mainLayout.addWidget(self.graphicsView)

        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)


        self.graphicsView.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.black))
        self.graphicsView.setStyleSheet("""
            .ControllerGeneric {
                border-style: none;
                }
            """)

        self.scene = QtGui.QGraphicsScene()


        self.boardItem = MessageBoard()
        self.scene.addItem(self.boardItem)
        self.graphicsView.setScene(self.scene)

        # self.mainWindow.skippedData.connect(self.boardItem.skipped)
        # self.mainWindow.badData.connect(self.boardItem.badData)

        # if i open a window here to let the user edit some properties, it needs to be updated to show
        #  warnings, if some are active.
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.setSingleShot(False)
        self.updateTimer.timeout.connect(self.update)
        self.updateTimer.start(100)

        # self.resize(300, 81)
        # self.setGeometry(0, 0, 250, 75)

    def resetOnceTriggeredFlags(self):
        self.boardItem.resetOnceTriggeredFlags()
        self.skippedTriggeredOnce = False
        self.badDataTriggeredOnce = False
        self.update()

    # def skipped(self, count):
    #     self.skippedTriggeredOnce = True
    #     self.lastTriggerOfSkip = datetime.datetime.now()
    #     self.update()
    #
    # def badData(self):
    #     self.badDataTriggeredOnce = True
    #     self.lastTriggerOfBadData = datetime.datetime.now()
    #     self.update()

    def skipped(self):
        self.boardItem.skipped()

    def badData(self):
        self.boardItem.badData()

    def setComStateMessage(self, boardMessage):
        self.boardItem.setComStateMessage(boardMessage)
        # self.update()

    def setComInfo(self, text):
        self.boardItem.setComInfo(text)

    def update(self):
        self.scene.setSceneRect(0, -10, 301, 81)
        self.scene.update()
        # self.resize(302, 79)
        super(MessageBoardWidget, self).update()

    # def resizeEvent(self, QResizeEvent):
    #     super(TestMessageBoardWidget, self).resizeEvent(QResizeEvent)

    # def size(self):
    #     return QtCore.QSize(303, 80)























class BoardMessage(object):
    def __init__(self, text, pen):
        self.text = text
        self.pen = pen

class MessageBoard(QtGui.QGraphicsObject):

    COM_OK = BoardMessage("Com ok", QtGui.QPen(QtCore.Qt.darkGreen))
    WAITING = BoardMessage("No connection,\nwaiting...", QtGui.QPen(QtCore.Qt.red))
    WRONG_CONFIG = BoardMessage("wrong\nconfig", QtGui.QPen(QtCore.Qt.red))
    TIME_OUT = BoardMessage("Timeout,\nwaiting...", QtGui.QPen(QtCore.Qt.red))
    UNKNOWN = BoardMessage("Unknown\nstate", QtGui.QPen(QtGui.QColor(255, 140, 0)))
    PLAY = BoardMessage("connecting", QtGui.QPen(QtGui.QColor(255, 140, 0)))
    PAUSE = BoardMessage("Com paused", QtGui.QPen(QtGui.QColor(255, 140, 0)))
    DEBUG = BoardMessage("Debug mode", QtGui.QPen(QtGui.QColor(255, 140, 0)))
    RECORD = BoardMessage("recording...", QtGui.QPen(QtGui.QColor(255, 140, 0)))


    BAD_DATA = BoardMessage("Bad data", QtGui.QPen(QtCore.Qt.red))
    SKIPPED = BoardMessage("Skipped", QtGui.QPen(QtGui.QColor(255, 140, 0)))

    def __init__(self):
        super(MessageBoard, self).__init__()

        self.blinkInterval = 300

        self.darkGrayPen = QtGui.QPen(QtGui.QColor(70, 70, 70))

        self.greenPen = QtGui.QPen(QtCore.Qt.darkGreen)

        self.separatorPen = QtGui.QPen(QtCore.Qt.darkGray)
        self.separatorPen.setCosmetic(True)
        self.separatorPen.setWidth(1)

        self.comStateShowInverted = False
        self.comInfoShowInverted = False
        self.skippedShowInverted = False
        self.badDataShowInverted = False

        self.comStateCancelShowInvertedTimer = QtCore.QTimer()
        self.comStateCancelShowInvertedTimer.setSingleShot(True)
        self.comStateCancelShowInvertedTimer.timeout.connect(self.cancelComStateInvert)

        self.comInfoCancelShowInvertedTimer = QtCore.QTimer()
        self.comInfoCancelShowInvertedTimer.setSingleShot(True)
        self.comInfoCancelShowInvertedTimer.timeout.connect(self.cancelComInfoInvert)

        self.skippedCancelShowInvertedTimer = QtCore.QTimer()
        self.skippedCancelShowInvertedTimer.setSingleShot(True)
        self.skippedCancelShowInvertedTimer.timeout.connect(self.cancelSkippedInvert)

        self.badDataCancelShowInvertedTimer = QtCore.QTimer()
        self.badDataCancelShowInvertedTimer.setSingleShot(True)
        self.badDataCancelShowInvertedTimer.timeout.connect(self.cancelBadDataInvert)


        self.skippedTriggeredOnce = False
        self.badDataTriggeredOnce = False

        self.timeOfLastSkippedTriggerBlinkStart = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.timeOfLastBadDataTriggerBlinkStart = datetime.datetime.now() - datetime.timedelta(hours=1)

        self.width = 300
        self.height = 70
        self.upperHeight = 45
        self.lowerHeight = self.height - self.upperHeight
        self.upperLeftRect = QtCore.QRect(0, 0, self.width / 2, self.upperHeight)
        self.upperRightRect = QtCore.QRect(self.width / 2, 0, self.width / 2, self.upperHeight)
        self.lowerLeftRect = QtCore.QRect(0, self.upperHeight, self.width / 2, self.lowerHeight)
        self.lowerRightRect = QtCore.QRect(self.width / 2, self.upperHeight, self.width / 2, self.lowerHeight)

        self.smallUpperLeftRect = QtCore.QRect(2, 2, self.width / 2 - 3, self.upperHeight - 3)
        self.smallUpperRightRect = QtCore.QRect(self.width / 2 + 2, 2, self.width / 2 - 3, self.upperHeight - 3)
        self.smallLowerLeftRect = QtCore.QRect(2, self.upperHeight + 2, self.width / 2 - 3, self.lowerHeight - 3)
        self.smallLowerRightRect = QtCore.QRect(self.width / 2 + 2, self.upperHeight + 2, self.width / 2 - 3, self.lowerHeight - 3)


        self.comStateMessage = self.WAITING

        self.comInfoText  = "..."

    @QtCore.pyqtSlot()
    def resetOnceTriggeredFlags(self):
        self.skippedTriggeredOnce = False
        self.badDataTriggeredOnce = False

    @QtCore.pyqtSlot()
    def skipped(self):
        self.skippedTriggeredOnce = True
        if datetime.datetime.now() - self.timeOfLastSkippedTriggerBlinkStart > datetime.timedelta(milliseconds=self.blinkInterval * 2):
            self.skippedShowInverted = True
            self.skippedCancelShowInvertedTimer.start(self.blinkInterval)
            self.timeOfLastSkippedTriggerBlinkStart = datetime.datetime.now()

    @QtCore.pyqtSlot()
    def badData(self):
        self.badDataTriggeredOnce = True
        if datetime.datetime.now() - self.timeOfLastBadDataTriggerBlinkStart > datetime.timedelta(milliseconds=self.blinkInterval * 2):
            self.badDataShowInverted = True
            self.badDataCancelShowInvertedTimer.start(self.blinkInterval)
            self.timeOfLastBadDataTriggerBlinkStart = datetime.datetime.now()

    @QtCore.pyqtSlot()
    def setComStateMessage(self, boardMessage):
        self.comStateShowInverted = True
        self.comStateCancelShowInvertedTimer.start(self.blinkInterval)
        if isinstance(boardMessage, BoardMessage):
            self.comStateMessage = boardMessage
        else:
            raise Exception("need value of type BoardMessage")
        # self.update()

    @QtCore.pyqtSlot()
    def setComInfo(self, text):
        self.comInfoText = text
        self.comInfoShowInverted = True
        self.comInfoCancelShowInvertedTimer.start(self.blinkInterval)

    @QtCore.pyqtSlot()
    def cancelComStateInvert(self):
        self.comStateShowInverted = False

    @QtCore.pyqtSlot()
    def cancelComInfoInvert(self):
        self.comInfoShowInverted = False

    @QtCore.pyqtSlot()
    def cancelSkippedInvert(self):
        self.skippedShowInverted = False

    @QtCore.pyqtSlot()
    def cancelBadDataInvert(self):
        self.badDataShowInverted = False


    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        # QPainter.setRenderHint(QtGui.QPainter.Antialiasing)


        QPainter.setFont(QtGui.QFont("Courier New", 12))

        if self.comStateShowInverted is True:
            QPainter.fillRect(self.smallUpperLeftRect, QtCore.Qt.red)
            QPainter.setPen(QtGui.QPen(QtCore.Qt.black))

            QPainter.drawText(self.upperLeftRect,
                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                             QtCore.QString(self.comStateMessage.text))
        else:
            QPainter.fillRect(self.smallUpperLeftRect, QtCore.Qt.black)
            QPainter.setPen(self.comStateMessage.pen)

            QPainter.drawText(self.upperLeftRect,
                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                             QtCore.QString(self.comStateMessage.text))


        if self.badDataTriggeredOnce is False:
            QPainter.setPen(self.darkGrayPen)
        else:
            QPainter.setPen(self.BAD_DATA.pen)

        QPainter.drawText(self.lowerRightRect,
                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                         QtCore.QString(self.BAD_DATA.text))

        if self.skippedShowInverted is True:
            QPainter.fillRect(self.smallLowerLeftRect, QtGui.QColor(255, 140, 0))
            QPainter.setPen(QtGui.QPen(QtCore.Qt.black))
        else:
            if self.skippedTriggeredOnce is False:
                QPainter.setPen(self.darkGrayPen)
            else:
                QPainter.setPen(self.SKIPPED.pen)

        QPainter.drawText(self.lowerLeftRect,
                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                         QtCore.QString(self.SKIPPED.text))


        if self.comInfoShowInverted is True:
            QPainter.fillRect(self.smallUpperRightRect, QtGui.QColor(255, 140, 0))
            QPainter.setPen(QtGui.QPen(QtCore.Qt.black))
        else:
            QPainter.setPen(self.greenPen)


        QPainter.drawText(self.upperRightRect,
                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                         QtCore.QString(self.comInfoText))

        QPainter.setPen(self.separatorPen)
        QPainter.drawRect(self.upperLeftRect)
        QPainter.drawRect(self.upperRightRect)
        QPainter.drawRect(self.lowerLeftRect)
        QPainter.drawRect(self.lowerRightRect)


    def boundingRect(self):
        return QtCore.QRectF(0, 0, 301, 80)

    # def resizeEvent(self, QResizeEvent):
    #     super(TestMessageBoard, self).resizeEvent(QResizeEvent)
    #     self.setSceneRect(0, 0, 300, 80)
