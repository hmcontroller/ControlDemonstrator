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

    **Data initialization arguments:** (x,y data only)
            =================================== ======================================
            PlotDataItem(xValues, yValues)      x and y values may be any sequence (including ndarray) of real numbers
            PlotDataItem(yValues)               y values only -- x will be automatically set to range(len(y))
            PlotDataItem(x=xValues, y=yValues)  x and y given by keyword arguments
            PlotDataItem(ndarray(Nx2))          numpy array with shape (N, 2) where x=data[:,0] and y=data[:,1]
            =================================== ======================================

    """

    def __init__(self, command):


        super(Gain, self).__init__(command)

        self.lineEdit = LineEditDoubleClickSpecial()

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


        # timer needed to stop a started userInputWarning
        self.clearUserInputWarningTimer = QtCore.QTimer()
        self.clearUserInputWarningTimer.setSingleShot(True)
        self.clearUserInputWarningTimer.timeout.connect(self.clearUserInputWarning)
        self.userInputWarningDuration = 1000

        # self.differentValueReceived()
        self.lineEdit.setText(str(self.command.getValue()))

    def editFinished(self):
        self.lineEditProxy.clearFocus()

        text = self.lineEdit.text()
        # print "Editfinished", text

        if text == "":
            self.lineEdit.setText(str(self.command.getLowerLimit()))
            self.command.setValue(self.command.getLowerLimit(), self)
            self.activateUserInputWarning()
        else:

            text = text.replace(",", ".")

            number = float(text)
            if number < self.command.getLowerLimit():
                self.lineEdit.setText(str(self.command.getLowerLimit()))
                self.command.setValue(self.command.getLowerLimit(), self)
                self.activateUserInputWarning()
            elif number > self.command.getUpperLimit():
                self.lineEdit.setText(str(self.command.getUpperLimit()))
                self.command.setValue(self.command.getUpperLimit(), self)
                self.activateUserInputWarning()
            else:
                # self.clearUserInputWarning()
                self.command.setValue(number, self)
        self.update()

    def activateUserInputWarning(self):
        super(Gain, self).activateUserInputWarning()
        self.clearUserInputWarningTimer.start(self.userInputWarningDuration)


    def valueChangedPerWidget(self, widgetInstance):
        if widgetInstance is self:
            pass
        else:
            self.lineEdit.setText(str(self.command.getValue()))

    def differentValueReceived(self):
        super(Gain, self).differentValueReceived()
        self.lineEdit.setText(str(self.command.getValue()))
        self.update()

    @property
    def inCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 30))

    @property
    def outCoordinates(self):
        return self.mapToScene(QtCore.QPoint(70, 30))

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # if self.showHoverIndication is True and self.lineEditProxy.hasFocus() is False:
        if self.isUnderMouse() is True:
            QPainter.fillPath(self.path, self.hoverBrush)

        # draw wrong user input warning
        if self.showUserInputWarning is True:
            QPainter.fillPath(self.path, self.userInputWarningBrush)

        # draw confirmation timeout warning
        if self.showCommFailureWarning is True:
            QPainter.fillPath(self.path, self.commFailureWarningBrush)

        # draw negative confirmation warning in front of all other colors
        if self.showDifferentValueReceivedWarning is True:
            QPainter.fillPath(self.path, self.differentValueReceivedWarningBrush)

        # draw the triangle
        QPainter.setPen(self.cablePen)
        QPainter.drawPath(self.path)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 70, 60)

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.showHoverIndication = True
        QtGui.QGraphicsItem.hoverEnterEvent(self, QGraphicsSceneMouseEvent)
        self.update()

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.showHoverIndication = False
        QtGui.QGraphicsItem.hoverLeaveEvent(self, QGraphicsSceneMouseEvent)
        self.update()

    def mousePressEvent(self, mouseEvent):
        QtGui.QGraphicsItem.mousePressEvent(self, mouseEvent)
        self.lineEditProxy.setFocus(True)
        textLength = len(self.lineEdit.text())
        self.lineEdit.setSelection(textLength, textLength)
        self.update()

    def mouseDoubleClickEvent(self, mouseEvent):
        QtGui.QGraphicsItem.mouseDoubleClickEvent(self, mouseEvent)
        self.lineEditProxy.setFocus(True)
        self.lineEdit.selectAll()
        self.update()






