# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtSql

from gui.constants import *
from gui.designerfiles.tabGenericView import Ui_tabGenericView
from gui.controllerSmallGeneric import ControllerSmallGeneric
from gui.plotWidget import PlotWidget


class TabSmallGenericView(QtGui.QWidget, Ui_tabGenericView):

    changingName = QtCore.pyqtSignal(str)

    def __init__(self, commands, channels, settings, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.commands = commands
        self.channels = channels
        self.settings = settings

        self.movePlot = True

        # disable dummy labels in qt designer file
        self.label_1.setVisible(False)
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        self.label_4.setVisible(False)

        self.controller = ControllerSmallGeneric(self.commands, self.channels)

        self.headerLayout = QtGui.QHBoxLayout()

        self.sendButton = QtGui.QPushButton("send now")
        self.headerLayout.insertWidget(0, self.sendButton, 0)

        self.cancelSendButton = QtGui.QPushButton("cancel")
        self.headerLayout.insertWidget(1, self.cancelSendButton, 0)

        self.headerLayout.insertStretch(2, 0)


        self.commandViewLayout.insertLayout(0, self.headerLayout, 0)

        self.commandViewLayout.insertWidget(1, self.controller, 0)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.controller.setSizePolicy(sizePolicy)

        self.plotter = PlotWidget(self.channels, self.settings)
        self.plotLayout.insertWidget(0, self.plotter, 0)

        self.splitter.splitterMoved.connect(self.splitterMoved)


    def curveHideShow(self, number, state):
        if state == 2:
            self.plotCurves[number].setVisible(True)
        else:
            self.plotCurves[number].setVisible(False)

    def updateTab(self, channels):
        pass
        # self.plotter.updatePlots(channels)
        # self.controller.updateSymbols()

    def splitterMoved(self, pos, index):
        self.controller.arrangeItems()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.movePlot = not self.movePlot




