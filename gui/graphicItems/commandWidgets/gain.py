# -*- encoding: utf-8 -*-
import re
from PyQt4 import QtGui, QtCore

from gui.constants import *


class Gain(QtGui.QGraphicsObject):

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, command):
        super(Gain, self).__init__()

        self.command = command

        self.lowerLimit = self.command.lowerLimit
        self.upperLimit = self.command.upperLimit


        self.showWrongUserInputWarning = False
        self.showHoverIndication = False
        self.showConfirmationFailure = False

        self.isCommandConfirmed = False

        self.setAcceptHoverEvents(True)


        self.lineEdit = MyLineEdit()
        self.lineEdit.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.lineEdit.setFixedSize(50, 40)
        p = QtGui.QPalette()
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(0,0,0,0)))
        self.lineEdit.setStyleSheet("""border: none; background-color: rgba(0, 0, 0, 0);""")     #; margin-top: 8px """)
        self.lineEdit.setPalette(p)
        self.lineEdit.move(1, 10)
        self.lineEdit.setText("0.0")
        self.lineEdit.setMaxLength(6)
        self.lineEdit.setFont(QtGui.QFont("sans-serif", 10))


        self.valli = MyFloatValidator(ur"\A[-]{0,1}\d{0,}[\.,]{0,1}\d{0,}\Z", self.lowerLimit, self.upperLimit)
        self.lineEdit.setValidator(self.valli)

        self.lineEdit.editingFinished.connect(self.editFinished)

        self.lineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.lineEditProxy.setWidget(self.lineEdit)


        self.pen = QtGui.QPen()
        self.pen.setColor(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)

        self.warningBrush = QtGui.QBrush(USER_INPUT_WARNING_COLOR)
        self.hoverBrush = QtGui.QBrush(HOVER_COLOR)
        self.unconfirmedBrush = QtGui.QBrush(CONFIRMATION_WARNING_COLOR)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(0, 0)
        self.path.lineTo(0, 60)
        self.path.lineTo(70, 30)
        self.path.closeSubpath()

        self.clearWarningTimer = QtCore.QTimer()
        self.clearWarningTimer.setSingleShot(True)
        self.clearWarningTimer.timeout.connect(self.clearUserInputWarning)

        self.confirmationWarningTimer = QtCore.QTimer()
        self.confirmationWarningTimer.setSingleShot(False)
        self.confirmationWarningTimer.timeout.connect(self.toggleConfirmationFailureIndication)
        self.confirmationWarningBlinkInterval = 200
        self.confirmationWarningTimer.start(self.confirmationWarningBlinkInterval)

        self.setValue(self.command.value)
        self.valueChanged.connect(self.command.setValue)
        self.command.confirmationTimeOut.connect(self.confirmationTimeOut)
        self.command.confirmation.connect(self.confirmation)


    def editFinished(self):
        self.lineEditProxy.clearFocus()

        text = self.lineEdit.text()
        print "Editfinished", text

        if text == "":
            self.lineEdit.setText(str(self.lowerLimit))
            self.valueChanged.emit(self.lowerLimit)
            self.showUserInputWarning()
            return

        text = text.replace(",", ".")

        number = float(text)
        if number < self.lowerLimit:
            self.lineEdit.setText(str(self.lowerLimit))
            self.valueChanged.emit(self.lowerLimit)
            self.showUserInputWarning()
        elif number > self.upperLimit:
            self.valueChanged.emit(self.upperLimit)
            self.lineEdit.setText(str(self.upperLimit))
            self.showUserInputWarning()
        else:
            self.valueChanged.emit(number)

    def showUserInputWarning(self):
        self.showWrongUserInputWarning = True
        self.clearWarningTimer.start(200)
        self.update()

    def clearUserInputWarning(self):
        self.showWrongUserInputWarning = False
        self.update()

    def confirmationTimeOut(self):
        self.isCommandConfirmed = False
        self.confirmationWarningTimer.start(self.confirmationWarningBlinkInterval)

    def confirmation(self):
        self.confirmationWarningTimer.stop()
        self.isCommandConfirmed = True
        self.showConfirmationFailure = False

    def toggleConfirmationFailureIndication(self):
        self.showConfirmationFailure = not self.showConfirmationFailure

    def setValue(self, value):
        self.lineEdit.setText(str(value))

    @property
    def inCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 30))

    @property
    def outCoordinates(self):
        return self.mapToScene(QtCore.QPoint(70, 30))

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self.showHoverIndication is True and self.lineEditProxy.hasFocus() is False:
            QPainter.fillPath(self.path, self.hoverBrush)

        # draw red in front of gray
        if self.showWrongUserInputWarning is True:
            QPainter.fillPath(self.path, self.warningBrush)

        # draw confirmation warning in front of all other colors
        if self.showConfirmationFailure is True:
            QPainter.fillPath(self.path, self.unconfirmedBrush)

        # draw the triangle
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.path)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 70, 60)

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.showHoverIndication = True
        QtGui.QGraphicsItem.hoverEnterEvent(self, QGraphicsSceneMouseEvent)

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.showHoverIndication = False
        QtGui.QGraphicsItem.hoverLeaveEvent(self, QGraphicsSceneMouseEvent)

    def mousePressEvent(self, mouseEvent):
        QtGui.QGraphicsItem.mousePressEvent(self, mouseEvent)
        self.lineEditProxy.setFocus(True)
        textLength = len(self.lineEdit.text())
        self.lineEdit.setSelection(textLength, textLength)

    def mouseDoubleClickEvent(self, mouseEvent):
        QtGui.QGraphicsItem.mouseDoubleClickEvent(self, mouseEvent)
        self.lineEditProxy.setFocus(True)
        self.lineEdit.selectAll()


class MyFloatValidator(QtGui.QDoubleValidator):

    valueAboveLimit = QtCore.pyqtSignal(float)
    valueBelowLimit = QtCore.pyqtSignal(float)

    def __init__(self, expression, bottom, top):
        super(MyFloatValidator, self).__init__()
        self.expression = re.compile(expression)

    def validate(self, qString, p_int):
        text = str(qString)
        # print "in Validator", text

        if text == "":
            return QtGui.QValidator.Acceptable, p_int

        if self.expression.search(text):
            return QtGui.QValidator.Acceptable, p_int
        else:
            return QtGui.QValidator.Invalid, p_int




class MyLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.selectAll()