# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.designerfiles.globalControllerAndView import Ui_GlobalControllerAndView


class GlobalControllerAndView(QtGui.QWidget, Ui_GlobalControllerAndView):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.commToggleButton.clicked.connect(self.toggleComm)
        self.pendingSendButton.clicked.connect(self.sendPendingCommands)
        self.pendingCancelButton.clicked.connect(self.cancelPendingCommands)

    def toggleComm(self):
        print "Comm on/off"

    def sendPendingCommands(self):
        print "sending pending commands"

    def cancelPendingCommands(self):
        print "pending commands canceled"
