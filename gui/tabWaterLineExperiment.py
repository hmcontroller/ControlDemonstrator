# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtSql

from gui.constants import *
from gui.designerfiles.tabWaterLineExperiment import Ui_tabWaterLineExperiment
from gui.controllerWaterLineExperiment import ControllerWaterLineExperiment
from gui.plotWidget import PlotWidget


class TabWaterLineExperiment(QtGui.QWidget, Ui_tabWaterLineExperiment):

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

        self.controller = ControllerWaterLineExperiment(self.commands, self.channels)
        self.verticalLayoutCommandView.insertWidget(0, self.controller, 0)

        self.plotter = PlotWidget(self.channels, self.settings)
        self.horizontalLayoutPlotArea.insertWidget(0, self.plotter, 0)


    def curveHideShow(self, number, state):
        if state == 2:
            self.plotCurves[number].setVisible(True)
        else:
            self.plotCurves[number].setVisible(False)

    def updateTab(self, channels):
        self.plotter.updatePlots(channels)
        self.controller.updateSymbols()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.movePlot = not self.movePlot




