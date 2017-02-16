# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtSql
import pyqtgraph

from gui.idCheckBox import IdColorLabelCheckbox
from gui.constants import *


class PlotWidget(QtGui.QWidget):
    def __init__(self, channels, settings, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.channels = channels
        self.settings = settings

        self.movePlot = True

        self.horizontalLayoutPlotArea = QtGui.QHBoxLayout(self)
        self.horizontalLayoutPlotArea.setMargin(0)

        # Enable antialiasing for prettier plots or not
        pyqtgraph.setConfigOptions(antialias=False)

        self.plotWidget = pyqtgraph.PlotWidget()
        self.plotWidget.setXRange(-float(self.settings.bufferLength)*(self.settings.controllerLoopCycleTime / float(1000000)), 0)
        self.plotWidget.setYRange(0, 60000)
        self.horizontalLayoutPlotArea.insertWidget(0, self.plotWidget, 0)

        self.verticalLayoutPlotSwitcher = QtGui.QVBoxLayout()
        self.verticalLayoutPlotSwitcher.setMargin(0)
        self.horizontalLayoutPlotArea.insertLayout(1, self.verticalLayoutPlotSwitcher, 0)

        self.plotCurves = list()
        for i, channel in enumerate(self.channels.channels):

            # create a plot curve
            colorTuple = channel.colorRgbTuple
            color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
            self.plotCurves.append(self.plotWidget.plot(pen=color))

            # add a check box to show/hide the curve next to the plot window
            box = IdColorLabelCheckbox(id=i, color=color)
            box.setFont(CHECK_BOX_FONT)
            box.setObjectName("checkBox{}".format(i))
            box.setText(channel.name)
            # box.setStyleSheet("""border: 3px solid rgb({})""".format(colorStrings[i % len(colorStrings)]))
            box.setChecked(True)
            box.changed.connect(self.curveHideShow)
            self.verticalLayoutPlotSwitcher.addWidget(box)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayoutPlotSwitcher.addItem(spacerItem)


    def curveHideShow(self, number, state):
        if state == 2:
            self.plotCurves[number].setVisible(True)
        else:
            self.plotCurves[number].setVisible(False)

    def updatePlots(self, channels):
        if self.movePlot is True:
            # update all curves
            biggestTime = channels.timeValues[self.settings.bufferLength - 1]
            for i, curve in enumerate(self.plotCurves):
                curve.setData(channels.timeValues, channels.channels[i])
                curve.setPos(-biggestTime, 0)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.movePlot = not self.movePlot
