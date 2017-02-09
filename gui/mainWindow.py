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


        colorStrings = list()
        for color in COLORS:
            colorStrings.append("{}, {}, {}".format(color[0], color[1], color[2]))

        self.plotWidget = pyqtgraph.PlotWidget()
        self.plotWidget.setXRange(-float(self.settings.bufferLength)*(self.settings.controllerLoopCycleTime / float(1000000)), 0)
        self.plotWidget.setYRange(0, 60000)


        # TODO - do not differentiate between analog channels and fastParameterChannels
        # TODO remove sensorMapping from the config file


        self.measurementData = modelMaker.getMeasurementDataModel()

        self.plotCurves = list()

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

        for i, channel in enumerate(self.measurementData.channels):
            # create a plot curve
            colorTuple = COLORS[i % len(COLORS)]
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
            box.setSizePolicy(sizePolicy)
            self.verticalLayout.addWidget(box)



        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.totalChannelCount = len(self.measurementData.channels)

        self.commands = modelMaker.getCommands()
        self.parameterCount = len(self.commands)

        self.myControllerClass = gui.controllerConsole.MyController(self.commands)
        self.verticalLayout_2.insertWidget(0, self.myControllerClass, 0)

        self.myControllerClass.parameterChanged.connect(self.parameterChangedFromController)

        logging.info("GUI load complete")

        # Enable antialiasing for prettier plots or not
        pyqtgraph.setConfigOptions(antialias=False)

        self.horizontalLayout_3.insertWidget(0, self.plotWidget, 0)

        self.parameterCounter = 0
        self.messageSize = self.totalChannelCount * 4 + 16
        self.ip = '192.168.178.20'
        # self.ip = '192.168.0.133'
        # self.controllerIP = '192.168.178.59'
        self.controllerIP = '192.168.0.10'
        self.portRX = 10000
        self.portTX = 10001

        self.sockRX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRX.bind((self.ip, self.portRX))
        self.sockRX.setblocking(False)
        self.sockRX.settimeout(0)

        print 'UDP Server Running at ', self.sockRX.getsockname()# socket.gethostbyname(socket.gethostname())

        self.sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockTX.bind((self.ip, self.portTX))
        self.sockTX.setblocking(False)
        self.sockTX.settimeout(0)


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

        if self.movePlot is True and len(self.measurementData.channels) > 0:
            # update all curves
            biggestTime = self.measurementData.channels[0].timeValues[self.settings.bufferLength - 1]
            for i, curve in enumerate(self.plotCurves):
                curve.setData(self.measurementData.channels[i].timeValues,
                              self.measurementData.channels[i].values)
                curve.setPos(-biggestTime, 0)

    def updateController(self):
        self.myControllerClass.tankWidget0.setLevel((self.measurementData.channels[0].values[self.settings.bufferLength-1]/65536.0)*100)
        self.myControllerClass.tankWidget1.setLevel((self.measurementData.channels[1].values[self.settings.bufferLength-1]/65536.0)*100)
        self.myControllerClass.tankWidget2.setLevel((self.measurementData.channels[2].values[self.settings.bufferLength-1]/65536.0)*100)
        self.myControllerClass.scene.update()

    def printLoopPerformance(self):
        print "min", self.loopDurationMin, "max", self.loopDurationMax, "avg", self.loopDurationAverage
        print "rec:", self.parametersReceived
        print "snd:", self.parametersToSend


    def stopServer(self):
        pass
        # self.udpServer.stop()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            try:
                print self.ringBuffers[0]
            except:
                pass
            self.movePlot = not self.movePlot

    def parameterChangedFromController(self, parameterNumber, value):
        print "you are controlling nicely", parameterNumber, value
        self.parametersToSend[parameterNumber] = value

    def receive(self):
        # print "waiting for UDP data packet..."
        bufferContainsData = True
        while bufferContainsData is True:
            try:
                data, address = self.sockRX.recvfrom(self.messageSize)
            except socket.timeout:
                bufferContainsData = False
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    bufferContainsData = False
                else:
                    raise
            else:


                loopStartTime = struct.unpack("<i", data[self.messageSize - 16:self.messageSize - 12])[0]
                loopDuration = struct.unpack("<i", data[self.messageSize - 12:self.messageSize - 8])[0]
                if loopDuration < self.loopDurationMin:
                    self.loopDurationMin = loopDuration
                elif loopDuration > self.loopDurationMax:
                    self.loopDurationMax = loopDuration

                self.loopDurationSum += loopDuration
                self.loopDurationCounter += 1
                self.loopDurationAverage = self.loopDurationSum / float(self.loopDurationCounter)
                loopStartTimeInSec = loopStartTime / 1000000.0
                if len(self.timeValues) > 0:
                    if loopStartTimeInSec < self.timeValues[-1]:
                        # clear all values
                        self.timeValues.clear()
                        for aBuffer in self.ringBuffers:
                            aBuffer.clear()

                self.timeValues.append(loopStartTimeInSec)
                for i in range(0, self.totalChannelCount):
                    self.ringBuffers[i].append(struct.unpack("<f", data[i*4:i*4+4])[0])

                parameterNumber = struct.unpack("<i", data[self.messageSize - 8:self.messageSize - 4])[0]
                parameterValue = struct.unpack("<f", data[self.messageSize - 4:self.messageSize])[0]

                self.parametersReceived[parameterNumber] = parameterValue

                # send parameters
                formatString = "<{}f".format(self.parameterCount)
                packed_data = struct.pack(formatString, *self.parametersToSend)
                self.sockTX.sendto(packed_data, (self.controllerIP, self.portTX))

                self.parameterCounter += 1
                if self.parameterCounter >= len(self.parametersToSend):
                    self.parameterCounter = 0




class ValueChannel(object):
    VALUE_TYPE = 1
    PARAMETER_TYPE = 2

    def __init__(self):
        self.curve = None
        self.name = None
        self.show = False
        self.checkBox = None
