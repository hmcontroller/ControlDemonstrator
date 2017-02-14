# -*- encoding: utf-8 -*-
import os
import logging
import collections

import struct
import socket
import errno
import time

from PyQt4 import QtCore, QtGui, QtSql
import pyqtgraph


from gui.designerfiles.main_window import Ui_MainWindow
import gui.graphicItems
import gui.controllerConsole
from gui.idCheckBox import IdColorLabelCheckbox

from gui.constants import *

from core.modelMaker import ModelMaker
from core.communicator import UdpCommunicator
from core.messageInterpreter import MessageInterpreter

class ControlDemonstratorMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, rootFolder):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        # show a splash image
        splashImagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Regelkreis.gif")
        splashMap = QtGui.QPixmap(splashImagePath)
        splashScreen = QtGui.QSplashScreen(splashMap)
        splashScreen.show()
        QtGui.qApp.processEvents()
        splashScreen.showMessage(u"Regulator wird geladen...", QtCore.Qt.AlignCenter)
        QtGui.qApp.processEvents()

        # time.sleep(1)

        # generate model objects according to the config file
        configFilePath = os.path.join(rootFolder, "config.txt")
        modelMaker = ModelMaker(configFilePath)
        self.sensorMapping = modelMaker.getSensorMapping()
        self.settings = modelMaker.getMiscSettings()

        # TODO it is dirty how the messageData list will be generated in model maker - check single source problem
        self.messageFormat = modelMaker.getMessageFormatList()






        # TODO - do not differentiate between analog channels and fastParameterChannels
        # TODO remove sensorMapping from the config file
        self.measurementData = modelMaker.getMeasurementDataModel()

        self.plotWidget = pyqtgraph.PlotWidget()
        self.plotWidget.setXRange(-float(self.settings.bufferLength)*(self.settings.controllerLoopCycleTime / float(1000000)), 0)
        self.plotWidget.setYRange(0, 60000)
        self.plotCurves = list()
        for i, channel in enumerate(self.measurementData.channels):
            # create a plot curve
            colorTuple = CHANNEL_COLORS[i % len(CHANNEL_COLORS)]
            color = QtGui.QColor(colorTuple[0], colorTuple[1], colorTuple[2])
            self.plotCurves.append(self.plotWidget.plot(pen=color))

            # add a check box to show/hide the curve next to the plot window
            box = IdColorLabelCheckbox(parent=self.frame, id=i, color=color)
            box.setFont(CHECK_BOX_FONT)
            box.setObjectName("checkBox{}".format(i))
            box.setText(channel.name)
            # box.setStyleSheet("""border: 3px solid rgb({})""".format(colorStrings[i % len(colorStrings)]))
            box.setChecked(True)
            box.changed.connect(self.curveHideShow)
            self.verticalLayout.addWidget(box)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.totalChannelCount = len(self.measurementData.channels)

        self.commands = modelMaker.getCommands()
        self.parameterCount = len(self.commands)

        self.myControllerClass = gui.controllerConsole.MyController(self.commands, self.measurementData)
        self.verticalLayout_2.insertWidget(0, self.myControllerClass, 0)

        # self.myControllerClass.parameterChanged.connect(self.parameterChangedFromController)

        logging.info("GUI load complete")

        # Enable antialiasing for prettier plots or not
        pyqtgraph.setConfigOptions(antialias=False)

        self.horizontalLayout_3.insertWidget(0, self.plotWidget, 0)

        self.parameterCounter = 0


        # ownIP = '192.168.178.20'
        ownIP = '192.168.0.133'
        remoteIP = '192.168.0.10'
        portRX = 10000
        portTX = 10001
        messageSize = self.totalChannelCount * 4 + 16

        self.communicator = UdpCommunicator(ownIP, remoteIP, portRX, portTX)
        self.communicator.setMessageMap(self.messageFormat)

        # print 'UDP Server Running at ', self.sockRX.getsockname()# socket.gethostbyname(socket.gethostname())

        self.loopDurationMin = 1000000
        self.loopDurationMax = 0
        self.loopDurationAverage = 0
        self.loopDurationSum = 0
        self.loopDurationCounter = 0

        self.parametersReceived = list()
        self.parametersToSend = list()

        self.parametersReceived = [0.0] * self.parameterCount
        self.parametersToSend = range(0, self.parameterCount)




        for curve in self.plotCurves:
            curve.setPos(-self.settings.bufferLength, 0)

        self.movePlot = True
        self.plotTimer = QtCore.QTimer()
        self.plotTimer.setSingleShot(False)
        self.connect(self.plotTimer, QtCore.SIGNAL("timeout()"), self.updatePlot)
        self.plotTimer.start(self.settings.plotUpdateTimeSpanInMs)

        self.controllerTimer = QtCore.QTimer()
        self.controllerTimer.setSingleShot(False)
        self.connect(self.controllerTimer, QtCore.SIGNAL("timeout()"), self.updateController)
        self.controllerTimer.start(self.settings.controlUpdateTimeSpanInMs)

        self.loopReportTimer = QtCore.QTimer()
        self.loopReportTimer.setSingleShot(False)
        self.connect(self.loopReportTimer, QtCore.SIGNAL("timeout()"), self.printLoopPerformance)
        self.loopReportTimer.start(5000)


        splashScreen.finish(self)

    def curveHideShow(self, number, state):
        if state == 2:
            self.plotCurves[number].setVisible(True)
        else:
            self.plotCurves[number].setVisible(False)

    def updatePlot(self):
        self.receive()

        if self.movePlot is True:
            # update all curves
            biggestTime = self.measurementData.timeValues[self.settings.bufferLength - 1]
            for i, curve in enumerate(self.plotCurves):
                curve.setData(self.measurementData.timeValues,
                              self.measurementData.channels[i])
                curve.setPos(-biggestTime, 0)

    def updateController(self):
        # tankLevel0 = (self.measurementData.channels[0][self.settings.bufferLength-1]/65536.0) * 100
        # self.myControllerClass.tankGauge.setValue(tankLevel0)
        self.myControllerClass.scene.update()

    def printLoopPerformance(self):
        print "min", self.loopDurationMin, "max", self.loopDurationMax, "avg", self.loopDurationAverage

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.movePlot = not self.movePlot


    def receive(self):
        messages = self.communicator.receive()
        if messages is None:
            return

        MessageInterpreter.mapUserChannels(self.measurementData, messages)

        loopCycleDuration = MessageInterpreter.getLoopCycleDuration(messages[-1])
        for message in messages:
            commandConfirmation = MessageInterpreter.getCommandConfirmation(message)
            self.commands[commandConfirmation.id].checkConfirmation(commandConfirmation)

        self.communicator.send(self.commands)

        # calculate some statistics
        if loopCycleDuration < self.loopDurationMin:
            self.loopDurationMin = loopCycleDuration
        elif loopCycleDuration > self.loopDurationMax:
            self.loopDurationMax = loopCycleDuration

        self.loopDurationSum += loopCycleDuration
        self.loopDurationCounter += 1
        self.loopDurationAverage = self.loopDurationSum / float(self.loopDurationCounter)

