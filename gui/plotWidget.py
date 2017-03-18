# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtSql
import pyqtgraph

from gui.idCheckBox import IdColorLabelCheckbox
from gui.constants import *


class PlotWidget(QtGui.QWidget):
    def __init__(self, channels, settings, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.channels = channels
        self.channels.channelChanged.connect(self.updateCurve)
        self.settings = settings

        self.movePlot = True

        self.horizontalLayoutPlotArea = QtGui.QHBoxLayout(self)
        self.horizontalLayoutPlotArea.setMargin(0)

        # Enable antialiasing for prettier plots or not
        pyqtgraph.setConfigOptions(antialias=False)

        self.plotWidget = pyqtgraph.PlotWidget()
        self.plotWidget.setXRange(-float(self.settings.bufferLength)*(self.settings.controllerLoopCycleTimeInUs / float(1000000)), 0)
        self.plotWidget.setYRange(0, 60000)
        self.horizontalLayoutPlotArea.insertWidget(0, self.plotWidget, 0)

        self.verticalLayoutPlotSwitcher = QtGui.QVBoxLayout()
        self.verticalLayoutPlotSwitcher.setMargin(6)
        self.horizontalLayoutPlotArea.insertLayout(1, self.verticalLayoutPlotSwitcher, 0)

        self.plotCurves = dict()
        for channel in self.channels.channels:

            # create a plot curve
            colorTuple = channel.colorRgbTuple
            color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
            self.plotCurves[channel.id] = self.plotWidget.plot(pen=color)

            # add a check box to show/hide the curve next to the plot window
            box = IdColorLabelCheckbox(id=channel.id, color=color)
            box.setFont(CHECK_BOX_FONT)
            box.setObjectName("checkBox{}".format(channel.id))
            box.setText(channel.name)
            # box.setStyleSheet("""border: 3px solid rgb({})""".format(colorStrings[i % len(colorStrings)]))
            box.setChecked(True)
            box.changed.connect(self.curveHideShow)
            box.keyPressed.connect(self.keyPressEvent)
            self.verticalLayoutPlotSwitcher.addWidget(box)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayoutPlotSwitcher.addItem(spacerItem)

        self.plotUpdateTimer = QtCore.QTimer()
        self.plotUpdateTimer.setSingleShot(False)
        self.plotUpdateTimer.timeout.connect(self.updatePlots)
        self.plotUpdateTimer.start(self.settings.guiUpdateIntervalLengthInMs)

    def curveHideShow(self, number, state):
        if state == 2:
            self.plotCurves[number].setVisible(True)
        else:
            self.plotCurves[number].setVisible(False)

    def updatePlots(self):
        if self.movePlot is True and self.isVisible() is True:
            # update all curves
            biggestTime = self.channels.timeValues[self.settings.bufferLength - 1]
            for id, curve in self.plotCurves.items():
                curve.setData(self.channels.timeValues, self.channels.channels[id])
                curve.setPos(-biggestTime, 0)

    def updateCurve(self, timeValues, channel):
        if self.movePlot is True: # and self.isVisible() is True:
            biggestTime = timeValues[self.settings.bufferLength - 1]
            curve = self.plotCurves[channel.id]

            curve.setData(timeValues, channel)
            curve.setPos(-biggestTime, 0)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.movePlot = not self.movePlot
