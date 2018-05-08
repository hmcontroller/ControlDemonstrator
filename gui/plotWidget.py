# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import pyqtgraph

from gui.idCheckBox import IdColorLabelCheckbox
from gui.constants import *
from gui.resources import *


class PlotWidget(QtGui.QWidget):
    def __init__(self, channels, applicationSettings, projectSettings, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.mousePositionInPlotCoordinatesX = 0
        self.mousePositionInPlotCoordinatesY = 0


        self.channels = channels
        self.channels.channelChanged.connect(self.updateCurve)
        self.channels.changed.connect(self.createCurves)


        # self.channels.channelConfigChanged.connect(self.createCurves)
        # self.channels.channelConfigChanged.connect(self.updateCurve)

        self.channels.bufferLengthChanged.connect(self.adjustScaleToBufferLength)

        self.applicationSettings = applicationSettings
        self.applicationSettings.changed.connect(self.applicationSettingsChanged)
        self.projectSettings = projectSettings


        self.movePlot = True


        # Enable antialiasing for prettier plots or not
        pyqtgraph.setConfigOptions(antialias=False)

        self.plotWidget = pyqtgraph.PlotWidget()
        self.plotWidget.setXRange(-float(self.applicationSettings.bufferLength)*(self.projectSettings.controllerLoopCycleTimeInUs / float(1000000)), 0)
        self.plotWidget.setYRange(-1, 1)
        self.plotWidget.showGrid(x=True, y=True)

        # for catching the mouse position in plot coordinates
        self.proxy = pyqtgraph.SignalProxy(self.plotWidget.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.verticalLine = self.plotWidget.addLine(x=-10, movable=True, label="{value}")
        # folgendes funktioniert nicht (Mauszeiger als quer liegenden Pfeil darstellen)
        self.verticalLine.setCursor(QtCore.Qt.SizeHorCursor)

        self.verticalLine1 = self.plotWidget.addLine(x=-10, movable=True, label="{value}")
        # folgendes funktioniert nicht (Mauszeiger als quer liegenden Pfeil darstellen)
        self.verticalLine1.setCursor(QtCore.Qt.SizeHorCursor)


        self.toggleMovePlotButton = QtGui.QToolButton()

        self.playPixmap = QtGui.QPixmap(playPath)
        self.playIcon = QtGui.QIcon(self.playPixmap)

        self.pausePixmap = QtGui.QPixmap(pausePath)
        self.pauseIcon = QtGui.QIcon(self.pausePixmap)

        self.toggleMovePlotButton.setIcon(self.pauseIcon)
        self.toggleMovePlotButton.setIconSize(QtCore.QSize(25, 25))
        self.toggleMovePlotButton.clicked.connect(self.togglePlayPause)




        self.time0Label = QtGui.QLabel()
        self.time1Label = QtGui.QLabel()
        self.deltaTLabel = QtGui.QLabel()
        self.frequencyLabel = QtGui.QLabel()

        self.time0Label.setText(u"t1 0 s")
        self.time1Label.setText(u"t1 0 s")
        self.deltaTLabel.setText(u"Δt 0 s")
        self.frequencyLabel.setText(u"f 0 Hz")

        self.listWidget = QtGui.QListWidget()
        self.listWidget.setAlternatingRowColors(True)


        ####################################################

        self.topVerticalLayoutRight = QtGui.QVBoxLayout()
        self.topVerticalLayoutRight.setMargin(0)
        self.topVerticalLayoutRight.addWidget(self.time0Label)
        self.topVerticalLayoutRight.addWidget(self.time1Label)
        self.topVerticalLayoutRight.addWidget(self.deltaTLabel)
        self.topVerticalLayoutRight.addWidget(self.frequencyLabel)

        self.topHorizontalLayout = QtGui.QHBoxLayout()
        self.topHorizontalLayout.setMargin(0)
        self.topHorizontalLayout.addWidget(self.toggleMovePlotButton)
        self.topHorizontalLayout.addLayout(self.topVerticalLayoutRight)
        self.topHorizontalLayout.setAlignment(self.toggleMovePlotButton, QtCore.Qt.AlignTop)


        self.listLayout = QtGui.QVBoxLayout()
        self.listLayout.setMargin(0)
        self.listLayout.addLayout(self.topHorizontalLayout)
        self.listLayout.addWidget(self.listWidget)

        self.horizontalLayoutPlotArea = QtGui.QHBoxLayout(self)
        self.horizontalLayoutPlotArea.setMargin(0)
        self.horizontalLayoutPlotArea.addWidget(self.plotWidget)
        self.horizontalLayoutPlotArea.addLayout(self.listLayout)


        # muchas importante:
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.listWidget.setSizePolicy(sizePolicy)







        ####################################################

        self.createCurves()



        self.plotUpdateTimer = QtCore.QTimer()
        self.plotUpdateTimer.setSingleShot(False)
        self.plotUpdateTimer.timeout.connect(self.updatePlots)
        self.plotUpdateTimer.start(self.applicationSettings.guiUpdateIntervalLengthInMs)


    def mouseMoved(self, event):
        # get the plot coordinates from pyqtgraph and store them for reference
        plotItem = self.plotWidget.plotItem
        self.mousePositionInPlotCoordinatesX = plotItem.vb.mapSceneToView(event[0]).x()
        self.mousePositionInPlotCoordinatesY = plotItem.vb.mapSceneToView(event[0]).y()

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
                                                    label="{value} <1>",
                                                    pen=QtGui.QPen(QtCore.Qt.lightGray),
                                                    hoverPen=QtGui.QPen(QtCore.Qt.darkGray))
        self.verticalLine.label.setPosition(0.95)
        self.verticalLine.sigPositionChanged.connect(self.verticalLineMoved)


        leftestTime = -(self.projectSettings.controllerLoopCycleTimeInUs * self.applicationSettings.bufferLength) / 1000000.0
        self.verticalLine1 = self.plotWidget.addLine(x=leftestTime,
                                                    movable=True,
                                                    label="{value} <2>",
                                                    pen=QtGui.QPen(QtCore.Qt.lightGray),
                                                    hoverPen=QtGui.QPen(QtCore.Qt.darkGray))
        self.verticalLine1.label.setPosition(0.9)
        self.verticalLine1.sigPositionChanged.connect(self.verticalLine1Moved)


        self.channelControllers = dict()

        self.valueLabels = list()
        for i, channel in enumerate(self.channels.channels):

            channel.showChanged.connect(self.showOrHideCurve)
            channel.colorChanged.connect(self.channelColorChanged)

            # create a plot curve
            colorTuple = channel.colorRgbTuple
            color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
            curve = self.plotWidget.plot(pen=color, clickable=True)
            # curve.setClickable(True, 5)   # only in new version ?? did i change something in the source code ??
            curve.sigClicked.connect(self.curveClicked)

            # add a check box to show/hide the curve next to the plot window
            box = IdColorLabelCheckbox(channel=channel, id=channel.id, color=color)
            # channel.scaleFactorChanged.connect(box.setScale)
            box.setScale(channel)
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
            if channel.isRequested is True:
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
    def verticalLine1Moved(self):
        if self.movePlot is False:
            self.updateValueLabels()
        if self.verticalLine1.getXPos() > 0:
            self.verticalLine1.setPos(0)

    @QtCore.pyqtSlot()
    def curveClicked(self, curve):
        print "curve clicked"

    def refreshTimeLabels(self, time0, time1):
        deltaT = time1 - time0
        if deltaT < 0.0:
            deltaT *= -1
        if deltaT == 0.0:
            frequency = 0
        else:
            frequency = 1.0 / deltaT

        self.time0Label.setText(u"t1 {} s".format(time0))
        self.time1Label.setText(u"t2 {} s".format(time1))
        self.deltaTLabel.setText(u"Δt {} s".format(deltaT))
        self.frequencyLabel.setText(u"f {} Hz".format(frequency))


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
        relativeTime = timeOfVerticalLine

        if timeOfVerticalLine == 0:
            indexAtVerticalLine = -1
        else:
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






        timeOfVerticalLine1 = self.verticalLine1.getXPos()
        relativeTimeOne = timeOfVerticalLine1

        if timeOfVerticalLine1 == 0:
            indexAtVerticalLine1 = -1
        else:
            # timeOfVerticalLine1Us = timeOfVerticalLine1 * 1000000

            firstCurve = None
            for key, something in self.channelControllers.iteritems():
                firstCurve = something["plotCurve"]

            xData, yData = firstCurve.getData()
            highestTime = xData[-1]
            timeOfVerticalLine1 += highestTime

            # search for index
            indexAtVerticalLine1 = 0
            for i in range(len(xData)):
                if xData[i] > timeOfVerticalLine1:
                    indexAtVerticalLine1 = i - 1
                    break



        for key, something in self.channelControllers.iteritems():
            xData, yData = something["plotCurve"].getData()
            # if 0 <= indexAtVerticalLine < self.applicationSettings.bufferLength:
            if -1 <= indexAtVerticalLine < valuesCount:
                yDataAtIndex = yData[indexAtVerticalLine]
                something["controllerBox"].setValue(str(yDataAtIndex))
            else:
                something["controllerBox"].setValue(str(0.0))


        # for key, something in self.channelControllers.iteritems():
        #     xData, yData = something["plotCurve"].getData()
        #     # if 0 <= indexAtVerticalLine < self.applicationSettings.bufferLength:
        #     if -1 <= indexAtVerticalLine1 < valuesCount:
        #         yDataAtIndex = yData[indexAtVerticalLine1]
        #         something["controllerBox"].setValue(str(yDataAtIndex))
        #     else:
        #         something["controllerBox"].setValue(str(0.0))

        self.refreshTimeLabels(relativeTime, relativeTimeOne)

    def updateCurve(self, timeValues, channel):
        curve = self.channelControllers[channel.id]["plotCurve"]
        if self.movePlot is True: # and self.isVisible() is True:

            valuesCount = len(self.channels.timeValues)
            biggestTime = timeValues[valuesCount - 1]
            # biggestTime = timeValues[self.settings.bufferLength - 1]


            colorTuple = channel.colorRgbTuple
            color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
            curve.pen = color
            curve.setData(timeValues, channel)
            curve.setPos(0, 0)
            # curve.setPos(-biggestTime, 0)

        else:
            colorTuple = channel.colorRgbTuple
            color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
            curve.setPen(color)

    def channelColorChanged(self, channel):
        curve = self.channelControllers[channel.id]["plotCurve"]
        colorTuple = channel.colorRgbTuple
        color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
        curve.setPen(color)
        # self.channelControllers[channel.id]["controllerBox"].

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

        if QKeyEvent.key() == QtCore.Qt.Key_1:
            # print "pos = {}, {}".format(self.mousePositionInPlotCoordinatesX, self.mousePositionInPlotCoordinatesY)
            self.verticalLine.setPos(self.mousePositionInPlotCoordinatesX)

        if QKeyEvent.key() == QtCore.Qt.Key_2:
            self.verticalLine1.setPos(self.mousePositionInPlotCoordinatesX)

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