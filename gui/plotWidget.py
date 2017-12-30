# -*- encoding: utf-8 -*-

from PyQt4 import QtCore
import pyqtgraph

from gui.idCheckBox import IdColorLabelCheckbox
from gui.constants import *
from gui.resources import *


class PlotWidget(QtGui.QWidget):
    def __init__(self, channels, applicationSettings, projectSettings, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.channels = channels
        self.channels.channelChanged.connect(self.updateCurve)
        self.channels.changed.connect(self.createCurves)
        self.channels.channelConfigChanged.connect(self.createCurves)
        self.channels.bufferLengthChanged.connect(self.adjustScaleToBufferLength)

        self.applicationSettings = applicationSettings
        self.applicationSettings.changed.connect(self.applicationSettingsChanged)
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
        self.horizontalLayoutPlotArea.addWidget(self.plotWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.plotWidget.setSizePolicy(sizePolicy)

        self.verticalLine = self.plotWidget.addLine(x=-10, movable=True, label="{value}")
        # folgendes funktioniert nicht
        self.verticalLine.setCursor(QtCore.Qt.SizeHorCursor)

        self.listLayout = QtGui.QVBoxLayout()
        self.listLayout.setMargin(0)

        self.toggleMovePlotButton = QtGui.QToolButton()

        self.playPixmap = QtGui.QPixmap(playPath)
        self.playIcon = QtGui.QIcon(self.playPixmap)

        self.pausePixmap = QtGui.QPixmap(pausePath)
        self.pauseIcon = QtGui.QIcon(self.pausePixmap)

        self.toggleMovePlotButton.setIcon(self.pauseIcon)
        self.toggleMovePlotButton.setIconSize(QtCore.QSize(25, 25))

        self.toggleMovePlotButton.clicked.connect(self.togglePlayPause)
        self.listLayout.addWidget(self.toggleMovePlotButton)

        self.listWidget = QtGui.QListWidget()
        self.listWidget.setAlternatingRowColors(True)
        self.listLayout.addWidget(self.listWidget)

        self.horizontalLayoutPlotArea.insertLayout(1, self.listLayout, 0)

        self.createCurves()

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.listWidget.setSizePolicy(sizePolicy)


        self.plotUpdateTimer = QtCore.QTimer()
        self.plotUpdateTimer.setSingleShot(False)
        self.plotUpdateTimer.timeout.connect(self.updatePlots)
        self.plotUpdateTimer.start(self.applicationSettings.guiUpdateIntervalLengthInMs)

    def adjustScaleToBufferLength(self, newBufferLength):
        self.plotWidget.setXRange(-float(newBufferLength)*(self.projectSettings.controllerLoopCycleTimeInUs / float(1000000)), 0)
        self.plotWidget.setYRange(-1000, 1000)

    def applicationSettingsChanged(self, settings=None):
        self.plotUpdateTimer.start(self.applicationSettings.guiUpdateIntervalLengthInMs)

    def createCurves(self):

        # remove all items from the layout

        # self.channelControllerList.clearChannels()
        self.listWidget.clear()

        # remove all plot curves
        self.plotWidget.clear()


        self.verticalLine = self.plotWidget.addLine(x=0,
                                                    movable=True,
                                                    label="{value} <-->",
                                                    pen=QtGui.QPen(QtCore.Qt.lightGray),
                                                    hoverPen=QtGui.QPen(QtCore.Qt.darkGray))
        self.verticalLine.label.setPosition(0.9)
        self.verticalLine.sigPositionChanged.connect(self.verticalLineMoved)


        self.channelControllers = dict()

        self.valueLabels = list()
        for i, channel in enumerate(self.channels.channels):

            channel.showChanged.connect(self.showOrHideCurve)

            # create a plot curve
            colorTuple = channel.colorRgbTuple
            color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
            curve = self.plotWidget.plot(pen=color, clickable=True)
            # curve.setClickable(True, 5)   # only in new version ?? did i change something in the source code ??
            curve.sigClicked.connect(self.curveClicked)

            # add a check box to show/hide the curve next to the plot window
            box = IdColorLabelCheckbox(channel=channel, id=channel.id, color=color)
            box.setFont(CHECK_BOX_FONT)
            box.setObjectName("checkBox{}".format(channel.id))

            self.channelControllers[channel.id] = dict()
            self.channelControllers[channel.id]["plotCurve"] = curve
            self.channelControllers[channel.id]["controllerBox"] = box


            if len(channel.displayName) > 0:
                box.setText(channel.displayName)
            else:
                box.setText(channel.name)

            box.changed.connect(self.curveHideShow)
            if channel.show is True:
                box.setChecked(True)
                curve.setVisible(True)
            else:
                box.setChecked(False)
                curve.setVisible(False)

            box.setRequested(channel.isRequested)

            if channel.isRequested is False:
                box.setChecked(False)
                curve.setVisible(False)


            box.keyPressed.connect(self.keyPressEvent)
            # self.channelControllerList.addChannel(box)


            listWidgetItem = QtGui.QListWidgetItem()
            listWidgetItem.setSizeHint(box.size())

            # listWidgetItem.setBackgroundColor(QtCore.Qt.red)
            self.listWidget.addItem(listWidgetItem)
            self.listWidget.setItemWidget(listWidgetItem, box)

        # self.channelControllerList.addSpacer()
        # spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        # self.verticalLayoutPlotSwitcher.addItem(spacerItem)

        # self.channelScrollArea.setWidth(20)

        self.updateVisibilityOfCurves()


    def updateVisibilityOfCurves(self):
        for id, something in self.channelControllers.iteritems():
            channel = self.channels.getChannelById(id)
            if channel.show is True and channel.isRequested is True:
                something["plotCurve"].setVisible(True)
            else:
                something["plotCurve"].setVisible(False)

    @QtCore.pyqtSlot()
    def verticalLineMoved(self):
        if self.movePlot is False:
            self.updateValueLabels()
        if self.verticalLine.getXPos() > 0:
            self.verticalLine.setPos(0)

    @QtCore.pyqtSlot()
    def curveClicked(self, curve):
        print "curve clicked"

    def showOrHideCurve(self, channel):
        pass

    def curveHideShow(self, number, state):
        if state == 2:
            self.channelControllers[number]["plotCurve"].setVisible(True)
            self.channels.getChannelById(number).show = True
        else:
            self.channelControllers[number]["plotCurve"].setVisible(False)
            self.channels.getChannelById(number).show = False

    def updatePlots(self):
        if self.movePlot is True and self.isVisible() is True:
            # update all curves

            valuesCount = len(self.channels.timeValues)
            biggestTime = self.channels.timeValues[valuesCount - 1]
            # print biggestTime
            # biggestTime = self.channels.timeValues[self.applicationSettings.bufferLength - 1]
            for id, controller in self.channelControllers.iteritems():
                # controller["plotCurve"].setData(self.channels.timeValues, self.channels.getChannelById(id), noUpdate=1, antialias=False)
                controller["plotCurve"].setData(self.channels.timeValues, self.channels.getChannelById(id), antialias=False)
                # controller["plotCurve"].setPos(0, 0)
                controller["plotCurve"].setPos(-biggestTime, 0)
            # self.plotWidget.update()
            self.updateValueLabels()

    def updateValueLabels(self):
        timeOfVerticalLine = self.verticalLine.getXPos()

        # timeOfVerticalLineUs = timeOfVerticalLine * 1000000

        firstCurve = None
        for key, something in self.channelControllers.iteritems():
            firstCurve = something["plotCurve"]

        xData, yData = firstCurve.getData()
        highestTime = xData[-1]
        timeOfVerticalLine += highestTime

        # search for index 
        indexAtVerticalLine = 0
        for i in range(len(xData)):
            if xData[i] > timeOfVerticalLine:
                indexAtVerticalLine = i - 1
                break

        valuesCount = len(self.channels.timeValues)
        # indexAtVerticalLine = int(self.applicationSettings.bufferLength + ((timeOfVerticalLine * 1000000) / self.projectSettings.controllerLoopCycleTimeInUs) - 1)
        # indexAtVerticalLine = int(valuesCount + ((timeOfVerticalLine * 1000000) / self.projectSettings.controllerLoopCycleTimeInUs) -1 )



        for key, something in self.channelControllers.iteritems():
            xData, yData = something["plotCurve"].getData()
            # if 0 <= indexAtVerticalLine < self.applicationSettings.bufferLength:
            if 0 <= indexAtVerticalLine < valuesCount:
                yDataAtIndex = yData[indexAtVerticalLine]
                something["controllerBox"].setValue(str(yDataAtIndex))
            else:
                something["controllerBox"].setValue(str(0.0))


    def updateCurve(self, timeValues, channel):
        if self.movePlot is True: # and self.isVisible() is True:

            valuesCount = len(self.channels.timeValues)
            biggestTime = timeValues[valuesCount - 1]
            # biggestTime = timeValues[self.settings.bufferLength - 1]

            curve = self.channelControllers[channel.id]["plotCurve"]

            curve.setData(timeValues, channel)
            curve.setPos(0, 0)
            # curve.setPos(-biggestTime, 0)

    def togglePlayPause(self):
        self.movePlot = not self.movePlot
        if self.movePlot is True:
            self.toggleMovePlotButton.setIcon(self.pauseIcon)
        else:
            self.toggleMovePlotButton.setIcon(self.playIcon)

    def pause(self):
        self.movePlot = False
        self.toggleMovePlotButton.setIcon(self.playIcon)


    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.togglePlayPause()



class ChannelControllerList(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ChannelControllerList, self).__init__(parent)

        self.maxExtendX = 0
        self.maxExtendY = 0

        self.verticalLayoutPlotSwitcher = QtGui.QVBoxLayout(self)
        self.verticalLayoutPlotSwitcher.setMargin(6)
        self.verticalLayoutPlotSwitcher.setSpacing(15)

        self.verticalLayoutPlotSwitcher.setAlignment(QtCore.Qt.AlignLeft)
        self.channels = list()

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtCore.Qt.green)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

    def addChannel(self, channelBox):
        self.verticalLayoutPlotSwitcher.addWidget(channelBox)
        self.channels.append(channelBox)

        for box in self.channels:
            boxWidth = box.size().width()
            boxHeight = box.size().height()

            if boxWidth > self.maxExtendX:
                self.maxExtendX = boxWidth

            if boxHeight > self.maxExtendY:
                self.maxExtendY = boxHeight


        # spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        # self.verticalLayoutPlotSwitcher.addItem(spacerItem)

        self.maxExtendY += 5

        self.setMinimumSize(self.maxExtendX, self.maxExtendY + 100)

        # self.resize(self.maxExtendX, self.maxExtendY)
        # self.setGeometry(0, 0, self.maxExtendX, self.maxExtendY)

    def addSpacer(self):
        return
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayoutPlotSwitcher.addItem(spacerItem)
        # self.resize(self.maxExtendX, self.maxExtendY)

    def clearChannels(self):
        self.maxExtendX = 0
        self.maxExtendY = 0
        self.channels = list()

        while self.verticalLayoutPlotSwitcher.count() > 0:
            item = self.verticalLayoutPlotSwitcher.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def sizeHint(self):
        return QtCore.QSize(self.maxExtendX, self.maxExtendY)