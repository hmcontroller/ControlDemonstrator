# -*- encoding: utf-8 -*-
from PyQt4 import QtCore

from baseCommand import BaseCommand
from gui.graphicItems.floatValidator import FloatValidator
from gui.constants import *
from gui.graphicItems.lineEditDoubleClickSpecial import LineEditDoubleClickSpecial


class Gain(BaseCommand):
    """
    This class uses some variables of the super class.
    The checks whether the microcontroller receives a given command or not are all done in the super class.
    In this class, concerning the mentioned checks, only the relevant visualisation is implemented.
    """
    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, command):

        # first of all create a line edit because a value will be set to it during super class init phase
        self.lineEdit = LineEditDoubleClickSpecial()

        super(Gain, self).__init__(command)

        self.suppressValueChangedSignal = False

        self.setAcceptHoverEvents(True)

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


        self.valli = FloatValidator()
        self.lineEdit.setValidator(self.valli)

        self.lineEdit.editingFinished.connect(self.editFinished)

        self.lineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.lineEditProxy.setWidget(self.lineEdit)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(0, 0)
        self.path.lineTo(0, 60)
        self.path.lineTo(70, 30)
        self.path.closeSubpath()

    def editFinished(self):
        self.lineEditProxy.clearFocus()

        text = self.lineEdit.text()
        print "Editfinished", text

        if text == "":
            self.lineEdit.setText(str(self.command.lowerLimit))
            self.valueChanged.emit(self.command.lowerLimit)
            self.showUserInputWarning()
            return

        text = text.replace(",", ".")

        number = float(text)
        if number < self.command.lowerLimit:
            self.lineEdit.setText(str(self.command.lowerLimit))
            self.valueChanged.emit(self.command.lowerLimit)
            self.showUserInputWarning()
        elif number > self.command.upperLimit:
            self.valueChanged.emit(self.command.upperLimit)
            self.lineEdit.setText(str(self.command.upperLimit))
            self.showUserInputWarning()
        else:
            if self.suppressValueChangedSignal is True:
                self.suppressValueChangedSignal = False
            else:
                self.valueChanged.emit(number)

    # overwrites method of base command
    def setValue(self, value):
        self.lineEdit.setText(str(value))
        # thereafter editingFinished is called automatically

    @property
    def inCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 30))

    @property
    def outCoordinates(self):
        return self.mapToScene(QtCore.QPoint(70, 30))

    # overwrites method of super class
    def negativeConfirmation(self):
        self.negativeConfirmationWarningBlinkTimer.start(self.negativeConfirmationBlinkInterval)
        # don't emit value changed, because otherwise the checks are triggered again and the
        # negativeConfirmationWarning phase will be aborted
        self.suppressValueChangedSignal = True
        self.setValue(self.command.value)


    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self.showHoverIndication is True and self.lineEditProxy.hasFocus() is False:
            QPainter.fillPath(self.path, self.hoverBrush)

        # draw wrong user input warning
        if self.showUserInputWarning is True:
            QPainter.fillPath(self.path, self.userInputWarningBrush)

        # draw confirmation timeout warning
        if self.showConfirmationTimeoutWarning is True:
            QPainter.fillPath(self.path, self.unconfirmedWarningBrush)

        # draw negative confirmation warning in front of all other colors
        if self.showNegativeConfirmationWarning is True:
            QPainter.fillPath(self.path, self.negativeConfirmedWarningBrush)

        # draw the triangle
        QPainter.setPen(self.cablePen)
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






