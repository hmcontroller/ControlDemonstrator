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
from gui.idCheckBox import IdCheckbox

from core.modelMaker import ModelMaker

class ControlDemonstratorMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        splashImagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Regelkreis.gif")
        splashMap = QtGui.QPixmap(splashImagePath)
        splashScreen = QtGui.QSplashScreen(splashMap)
        splashScreen.show()
        QtGui.qApp.processEvents()
        splashScreen.showMessage(u"Regulator wird geladen...", QtCore.Qt.AlignCenter)
        QtGui.qApp.processEvents()

        time.sleep(1)


        thisDir = os.path.dirname(os.path.realpath(__file__))
        configFilePath = os.path.join(thisDir, "config.txt")
        modelMaker = ModelMaker(configFilePath)
        self.sensorMapping = modelMaker.getSensorMapping()
        self.settings = modelMaker.getMiscSettings()


        self.plotUpdateTimeSpanInMs = 50
        self.controlUpdateTimeSpanInMs = 50



        font = QtGui.QFont()
        font.setPointSize(8)

        self.colors = list()
        self.colors.append((230, 0, 0))
        self.colors.append((0, 150, 0))
        self.colors.append((0, 153, 255))
        self.colors.append((255, 165, 0))

        colorStrings = list()
        for color in self.colors:
            colorStrings.append("{}, {}, {}".format(color[0], color[1], color[2]))

        self.plotWidget = pyqtgraph.PlotWidget()
        self.plotWidget.setXRange(-float(self.settings.bufferLength)*(self.settings.controllerLoopCycleTime / float(1000000)), 0)
        self.plotWidget.setYRange(0, 60000)


        self.valueChannels = list()

        for channelMap in self.sensorMapping:
            if channelMap[2] == 1:
                self.valueChannels.append(ValueChannel())

        for i, channel in enumerate(self.valueChannels):
            channel.curve = self.plotWidget.plot(pen=self.colors[i % len(self.colors)])
            channel.name = "Analog {}".format(i)
            channel.show = True
            channel.id = i
            box = IdCheckbox(parent=self.frame, id=i, channelType=ValueChannel.VALUE_TYPE)
            box.setFont(font)
            box.setObjectName("checkBox{}".format(i))
            box.setText(channel.name)
            box.setStyleSheet("""border: 3px solid rgb({})""".format(colorStrings[i % len(colorStrings)]))
            box.setChecked(True)
            box.changed.connect(self.curveHideShow)
            channel.checkBox = box
            self.verticalLayout.addWidget(channel.checkBox)



        #self.parameterChannels = list()

        alreadyThereChannelsCount = len(self.valueChannels)

        for i, section in enumerate(self.config.options('requestedFastParameters')):
            self.valueChannels.append(ValueChannel())
            chan = self.valueChannels[alreadyThereChannelsCount + i]
            chan.curve = self.plotWidget.plot(pen=self.colors[(alreadyThereChannelsCount + i) % len(self.colors)], connect='all')
            # chan.curve = self.plotWidget.plot(pen=None,
            #                                   symbol='o',
            #                                   symbolPen=None,
            #                                   symbolSize=1,
            #                                   symbolBrush=QtGui.QBrush(self.colors[(alreadyThereChannelsCount + i) % len(self.colors)]))
            channel.name = section
            channel.show = True
            channel.id = alreadyThereChannelsCount + i
            box = IdCheckbox(parent=self.frame, id=alreadyThereChannelsCount + i, channelType=ValueChannel.PARAMETER_TYPE)
            box.setFont(font)
            box.setObjectName("checkBox{}".format(alreadyThereChannelsCount + i))
            box.setText(channel.name)
            box.setStyleSheet("""border: 3px solid rgb({})""".format(colorStrings[(alreadyThereChannelsCount + i) % len(colorStrings)]))
            box.setChecked(True)
            box.changed.connect(self.curveHideShow)
            channel.checkBox = box
            self.verticalLayout.addWidget(channel.checkBox)


        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)




        self.totalChannelCount = len(self.valueChannels) # + len(self.parameterChannels)




        self.params = dict()
        for i, section in enumerate(self.config.options('requestedControlledParameters')):
            self.params[section] = i

        print self.params
        self.parameterCount = len(self.params)




        self.timeValues = collections.deque(maxlen=self.settings.bufferLength)
        self.ringBuffers = []
        for i in range(0, self.totalChannelCount):
            self.ringBuffers.append(collections.deque(maxlen=self.settings.bufferLength))



        # self.udpServer = udpServer
        # self.udpServer.configure(self.ringBuffers, self.totalChannelCount, self.paramCount, self.timeValues)
        # #self.udpServer = DataAquisitionServerUDP(self.ringBuffers)
        # self.udpServer.start()


        self.myControllerClass = gui.controllerConsole.MyController(self.params)
        self.verticalLayout_2.insertWidget(0, self.myControllerClass, 0)

        self.myControllerClass.parameterChanged.connect(self.parameterChangedFromController)

        # self.myPlotterClass = MyPlotter()
        # self.horizontalLayout_3.insertWidget(0, self.myPlotterClass, 0)

        logging.info("GUI load complete")

        # self.plotView = pyqtgraph.GraphicsView(useOpenGL=True)


        # self.plotView.addItem(self.plotWidget)

        # Enable antialiasing for prettier plots or not
        pyqtgraph.setConfigOptions(antialias=False)


        self.horizontalLayout_3.insertWidget(0, self.plotWidget, 0)


        self.parameterCounter = 0
        # messageSize = (channelCount + fastParameterCount) * 4 + 16
        self.messageSize = self.totalChannelCount * 4 + 16
        self.ip = '192.168.0.133'
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




        for channel in self.valueChannels:
            channel.curve.setPos(-len(self.ringBuffers[0]), 0)
        # for channel in self.parameterChannels:
        #     channel.curve.setPos(-len(self.ringBuffers[0]), 0)


        # self.testData = []
        # for i in range(0, self.settings.bufferLength):
        #     if i < 100:
        #         self.testData.append(3000)
        #     else:
        #         self.testData.append(10000)


        self.movePlot = True
        self.plotTimer = QtCore.QTimer()
        self.plotTimer.setSingleShot(False)
        #self.timer.setTimerType(QtCore.QTimer.PreciseTimer)
        self.connect(self.plotTimer, QtCore.SIGNAL("timeout()"), self.updatePlot)
        self.plotTimer.start(self.plotUpdateTimeSpanInMs)

        self.controllerTimer = QtCore.QTimer()
        self.controllerTimer.setSingleShot(False)
        #self.timer.setTimerType(QtCore.QTimer.PreciseTimer)
        self.connect(self.controllerTimer, QtCore.SIGNAL("timeout()"), self.updateController)
        self.controllerTimer.start(self.controlUpdateTimeSpanInMs)

        self.loopReportTimer = QtCore.QTimer()
        self.loopReportTimer.setSingleShot(False)
        #self.timer.setTimerType(QtCore.QTimer.PreciseTimer)
        self.connect(self.loopReportTimer, QtCore.SIGNAL("timeout()"), self.printLoopPerformance)
        self.loopReportTimer.start(5000)


        splashScreen.finish(self)

    def curveHideShow(self, number, state):
        if state == 2:
            self.valueChannels[number].curve.setVisible(True)
        else:
            self.valueChannels[number].curve.setVisible(False)

    def updatePlot(self):
        self.receive()

        if self.movePlot is True and len(self.timeValues) > 0:
            # update all curves
            biggestTime = self.timeValues[len(self.timeValues) - 1]
            for i, channel in enumerate(self.valueChannels):
                # channel.curve.setData(self.ringBuffers[i])
                channel.curve.setData(self.timeValues, self.ringBuffers[i])
                # if len(self.ringBuffers[0]) < self.settings.bufferLength:
                    # channel.curve.setPos(-len(self.ringBuffers[0]), 0)
                channel.curve.setPos(-biggestTime, 0)

    def updateController(self):
        lengthRingBuffer = len(self.ringBuffers[0])
        if lengthRingBuffer > 0:
            self.myControllerClass.tankWidget0.setLevel((self.ringBuffers[0][lengthRingBuffer-1]/65536.0)*100)
            self.myControllerClass.tankWidget1.setLevel((self.ringBuffers[1][lengthRingBuffer-1]/65536.0)*100)
            self.myControllerClass.tankWidget2.setLevel((self.ringBuffers[2][lengthRingBuffer-1]/65536.0)*100)
            #self.myControllerClass.tankWidget3.setLevel((self.ringBuffers[3][lengthRingBuffer-1]/65536.0)*100)
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
