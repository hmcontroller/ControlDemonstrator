# -*- encoding: utf-8 -*-


from PyQt4 import QtGui, QtCore

from gui.constants import *


class BaseCommand(QtGui.QGraphicsObject):

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, command):
        super(BaseCommand, self).__init__()

        self.command = command
        self.showWrongUserInputWarning = False
        self.showHoverIndication = False
        self.showConfirmationFailure = True
        self.isCommandConfirmed = False

        self.warningBrush = QtGui.QBrush(USER_INPUT_WARNING_COLOR)
        self.hoverBrush = QtGui.QBrush(HOVER_COLOR)
        self.unconfirmedBrush = QtGui.QBrush(CONFIRMATION_WARNING_COLOR)

        self.cablePen = CABLE_PEN

        self.hoverBrush = QtGui.QBrush(HOVER_COLOR)

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

    def showUserInputWarning(self):
        self.showWrongUserInputWarning = True
        self.clearWarningTimer.start(200)
        # self.update()

    def clearUserInputWarning(self):
        self.showWrongUserInputWarning = False
        # self.update()

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
        self.value = value
        self.valueChanged.emit(self.value)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        raise NotImplementedError("abstract class paint must be overwritten")

    def boundingRect(self):
        raise NotImplementedError("abstract class boundingRect must be overwritten")
