# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtSql
import pyqtgraph

from gui.idCheckBox import IdColorLabelCheckbox
from gui.constants import *


class PlotWidget(QtGui.QWidget):
    def __init__(self, channels, applicationSettings, projectSettings, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.channels = channels
        self.channels.channelChanged.connect(self.updateCurve)
        self.channels.changed.connect(self.createCurves)

        self.applicationSettings = applicationSettings
        self.projectSettings = projectSettings


        self.movePlot = True

        self.horizontalLayoutPlotArea = QtGui.QHBoxLayout(self)
        self.horizontalLayoutPlotArea.setMargin(0)

        # Enable antialiasing for prettier plots or not
        pyqtgraph.setConfigOptions(antialias=False)

        self.plotWidget = pyqtgraph.PlotWidget()
        self.plotWidget.setXRange(-float(self.applicationSettings.bufferLength)*(self.projectSettings.controllerLoopCycleTimeInUs / float(1000000)), 0)
        self.plotWidget.setYRange(-1000, 1000)
        self.plotWidget.showGrid(x=True, y=True)
        self.horizontalLayoutPlotArea.insertWidget(0, self.plotWidget, 0)

        self.verticalLine = self.plotWidget.addLine(x=-10, movable=True, label="{value}")

        self.verticalLine.setCursor(QtCore.Qt.SizeHorCursor)   # funktioniert nicht


        self.verticalLayoutPlotSwitcher = QtGui.QVBoxLayout()
        self.verticalLayoutPlotSwitcher.setMargin(6)
        self.horizontalLayoutPlotArea.insertLayout(1, self.verticalLayoutPlotSwitcher, 0)

        self.createCurves()

        self.plotUpdateTimer = QtCore.QTimer()
        self.plotUpdateTimer.setSingleShot(False)
        self.plotUpdateTimer.timeout.connect(self.updatePlots)
        self.plotUpdateTimer.start(self.applicationSettings.guiUpdateIntervalLengthInMs)

    def createCurves(self):

        # remove all items from the layout
        while self.verticalLayoutPlotSwitcher.count() > 0:
            item = self.verticalLayoutPlotSwitcher.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # remove all plot curves
        self.plotWidget.clear()


        self.verticalLine = self.plotWidget.addLine(x=0,
                                                    movable=True,
                                                    label="{value} <-->",
                                                    pen=QtGui.QPen(QtCore.Qt.lightGray),
                                                    hoverPen=QtGui.QPen(QtCore.Qt.darkGray))
        self.verticalLine.label.setPosition(0.9)
        self.verticalLine.sigPositionChanged.connect(self.verticalLineMoved)

        self.plotCurves = list()
        self.valueLabels = list()
        for i, channel in enumerate(self.channels.channels):

            # create a plot curve
            colorTuple = channel.colorRgbTuple
            color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
            self.plotCurves.append(self.plotWidget.plot(pen=color, clickable=True))
            self.plotCurves[i].sigClicked.connect(self.curveClicked)

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
            valueLabel = QtGui.QLabel("0.0")
            self.valueLabels.append(valueLabel)
            self.verticalLayoutPlotSwitcher.addWidget(valueLabel)
            spacerItem = QtGui.QSpacerItem(15, 15, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            self.verticalLayoutPlotSwitcher.addItem(spacerItem)


        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayoutPlotSwitcher.addItem(spacerItem)

    def verticalLineMoved(self):
        if self.movePlot is False:
            self.updateValueLabels()
        if self.verticalLine.getXPos() > 0:
            self.verticalLine.setPos(0)

    def curveClicked(self):
        print "curveClick"

    def curveHideShow(self, number, state):
        if state == 2:
            self.plotCurves[number].setVisible(True)
        else:
            self.plotCurves[number].setVisible(False)

    def updatePlots(self):
        if self.movePlot is True and self.isVisible() is True:
            # update all curves
            biggestTime = self.channels.timeValues[self.applicationSettings.bufferLength - 1]
            for i, curve in enumerate(self.plotCurves):
                curve.setData(self.channels.timeValues, self.channels.channels[i])
                curve.setPos(-biggestTime, 0)
            self.updateValueLabels()

    def updateValueLabels(self):
        timeOfVerticalLine = self.verticalLine.getXPos()
        indexAtVerticalLine = int(self.applicationSettings.bufferLength + ((timeOfVerticalLine * 1000000) / self.projectSettings.controllerLoopCycleTimeInUs) - 1)

        for valueLabel, plotCurve in zip(self.valueLabels, self.plotCurves):
            xData, yData = plotCurve.getData()
            if 0 <= indexAtVerticalLine < self.applicationSettings.bufferLength:
                yDataAtIndex = yData[indexAtVerticalLine]
                valueLabel.setText(str(yDataAtIndex))
            else:
                valueLabel.setText(str(0.0))


    def updateCurve(self, timeValues, channel):
        if self.movePlot is True: # and self.isVisible() is True:
            biggestTime = timeValues[self.settings.bufferLength - 1]
            curve = self.plotCurves[channel.id]

            curve.setData(timeValues, channel)
            curve.setPos(-biggestTime, 0)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.movePlot = not self.movePlot
