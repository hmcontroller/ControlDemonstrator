# -*- encoding: utf-8 -*-


from PyQt4 import QtGui, QtCore

from gui.constants import *

## @package baseCommand
#  This is the documentation for the baseCommand namespace, hm but it is only one class.
#
# Here are all the details about the baseCommand NAMESPACE and its thousands of classes.
#

## The BaseCommand class is the base class of all command widgets.
#
#  It sets up all needed signal slot connections to the core.command.Command class and
#  implements flags, that indicate the state of a command.
#
#  The state of a command can be



class BaseCommand(QtGui.QGraphicsObject):
    def __init__(self, command):
        super(BaseCommand, self).__init__()

        ## holds the command model from core.command.Command
        self.command = command

        # just for convenience, as these settings or values are needed often
        self.cablePen = CABLE_PEN
        self.setAcceptHoverEvents(True)

        # react on the case, that other widgets changed our own command
        self.command.valueChangedPerWidget.connect(self.valueChangedPerWidget)
        self.command.minChangedPerWidget.connect(self.minChangedPerWidget)
        self.command.maxChangedPerWidget.connect(self.maxChangedPerWidget)

        # use these parameters to paint your warnings
        self.showHoverIndication = False
        self.showUserInputWarning = False
        self.showCommFailureWarning = False
        self.showDifferentValueReceivedWarning = False

        # set all flags defined above according to the different warning states
        self.command.sameValueReceived.connect(self.sameValueReceived)
        self.command.differentValueReceived.connect(self.differentValueReceived)
        self.command.commTimeOut.connect(self.commTimeOut)

        # here brushes are defined to give a constant look of all warnings
        self.userInputWarningBrush = QtGui.QBrush(USER_INPUT_WARNING_COLOR)
        self.commFailureWarningBrush = QtGui.QBrush(CONFIRMATION_TIMEOUT_WARNING_COLOR)
        self.differentValueReceivedWarningBrush = QtGui.QBrush(NEGATIVE_CONFIRMATION_WARNING_COLOR)
        self.hoverBrush = QtGui.QBrush(HOVER_COLOR)

        # timer needed to stop a started userInputWarning
        self.clearUserInputWarningTimer = QtCore.QTimer()
        self.clearUserInputWarningTimer.setSingleShot(True)
        self.clearUserInputWarningTimer.timeout.connect(self.clearUserInputWarning)
        self.userInputWarningDuration = 200

        # this timer generates a blink effect for the concerned warning
        self.commFailureWarningBlinkTimer = QtCore.QTimer()
        self.commFailureWarningBlinkTimer.setSingleShot(False)
        self.commFailureWarningBlinkTimer.timeout.connect(self.toggleCommFailureIndication)
        self.commFailureWarningBlinkInterval = 200
        self.commFailureWarningBlinkTimer.start(self.commFailureWarningBlinkInterval)

        # this timer generates a blink effect for the concerned warning
        self.differentValueReceivedWarningBlinkTimer = QtCore.QTimer()
        self.differentValueReceivedWarningBlinkTimer.setSingleShot(False)
        self.differentValueReceivedWarningBlinkTimer.timeout.connect(self.toggleDifferentValueReceivedWarningIndication)
        self.differentValueReceivedBlinkInterval = 200

        # this timer stops a started warning after some time
        self.clearDifferentValueReceivedWarningTimer = QtCore.QTimer()
        self.clearDifferentValueReceivedWarningTimer.setSingleShot(True)
        self.clearDifferentValueReceivedWarningTimer.timeout.connect(self.clearDifferentValueReceivedWarning)
        self.differentValueReceivedWarningDuration = 2000

    def activateUserInputWarning(self):
        self.showUserInputWarning = True
        self.clearUserInputWarningTimer.start(self.userInputWarningDuration)

    def clearUserInputWarning(self):
        self.showUserInputWarning = False

    def sameValueReceived(self):
        self.commFailureWarningBlinkTimer.stop()
        self.showCommFailureWarning = False

    def differentValueReceived(self):
        self.differentValueReceivedWarningBlinkTimer.start(self.differentValueReceivedBlinkInterval)
        self.clearDifferentValueReceivedWarningTimer.start(self.differentValueReceivedWarningDuration)

    def toggleDifferentValueReceivedWarningIndication(self):
        self.showDifferentValueReceivedWarning = not self.showDifferentValueReceivedWarning

    def clearDifferentValueReceivedWarning(self):
        self.differentValueReceivedWarningBlinkTimer.stop()
        self.showDifferentValueReceivedWarning = False

    def commTimeOut(self):
        self.commFailureWarningBlinkTimer.start(self.commFailureWarningBlinkInterval)

    def toggleCommFailureIndication(self):
        self.showCommFailureWarning = not self.showCommFailureWarning

    def valueChangedPerWidget(self, widgetInstance):
        """
        You must overwrite this method in your derived class.
        """
        raise NotImplementedError("abstract method valueChangedPerWidget must be overwritten")

    def minChangedPerWidget(self, widgetInstance):
        """
        If needed, overwrite this method in your derived class.
        """
        pass

    def maxChangedPerWidget(self, widgetInstance):
        """
        If needed, overwrite this method in your derived class.
        """
        pass

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        raise NotImplementedError("abstract method paint must be overwritten")

    def boundingRect(self):
        raise NotImplementedError("abstract method boundingRect must be overwritten")

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.showHoverIndication = True

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.showHoverIndication = False
