# -*- encoding: utf-8 -*-
import os
import logging
from importlib import import_module
import json
import pickle

from PyQt4 import QtCore, QtGui

from core.modelMaker import ModelMaker
from core.communicator import UdpCommunicator
from core.communicator import SerialCommunicator
from core.messageInterpreter import MessageInterpreter
from core.configFileManager import ConfigFileManager
from core.applicationSettingsManager import ApplicationSettingsManager


from gui.constants import *
# from gui.TabWaterLineExperiment import TabWaterLineExperiment
# from gui.TabGenericView import TabGenericView
# from gui.TabSmallGenericView import TabSmallGenericView

class ControlDemonstratorMainWindow(QtGui.QMainWindow):
    def __init__(self, rootFolder):
        QtGui.QMainWindow.__init__(self)
        self.setupUi()

        self.setWindowTitle("ControlDemonstrator")

        self.screenRect = QtGui.QApplication.desktop().screenGeometry()
        self.setGeometry(self.screenRect.width() * 0.05, self.screenRect.height() * 0.05,
                         self.screenRect.width() * 0.9, self.screenRect.height() * 0.9)


        # show the application on the second monitor as maximized window
        self.screenRectSecondMonitor = QtGui.QApplication.desktop().screenGeometry(1)
        self.setGeometry(self.screenRect.width(), 0,
                         self.screenRectSecondMonitor.width() * 0.9, self.screenRectSecondMonitor.height() * 0.9)
        self.showMaximized()


        # show a splash image
        splashImagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Regelkreis.gif")
        splashMap = QtGui.QPixmap(splashImagePath)
        splashScreen = QtGui.QSplashScreen(splashMap)
        splashScreen.show()
        QtGui.qApp.processEvents()
        QtGui.qApp.processEvents()








        # generate model objects according to the config file


        configFilePath = os.path.join(rootFolder, "config.txt")
        modelMaker = ModelMaker(configFilePath)


        appSettingsManager = ApplicationSettingsManager("testAppConfig.json")
        self.applicationSettings = appSettingsManager.restoreSettingsFromFile()

        projectConfigManager = ConfigFileManager(self.applicationSettings)
        self.projectSettings, self.channels, self.commands, self.messageFormatList = projectConfigManager.buildModelFromConfigFile("testProjectConfig.json")



        # TODO it is ugly how the messageData list will be generated in model maker - check single source problem

        self.communicator = modelMaker.getCommunicator()
        self.communicator.setMessageMap(self.messageFormatList)
        self.communicator.connectToController()

        self.addTabs(self.projectSettings.tabs)















        # setup a timer, that triggers to read from the controller
        self.receiveTimer = QtCore.QTimer()
        self.receiveTimer.setSingleShot(False)
        self.receiveTimer.timeout.connect(self.receiveAndSend)
        self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

        # # setup a timer, that triggers to send to the controller
        # self.sendTimer = QtCore.QTimer()
        # self.sendTimer.setSingleShot(False)
        # self.sendTimer.timeout.connect(self.send)
        # self.sendTimer.start(self.settings.sendMessageIntervalLengthInMs)

        # setup a timer, that runs a loop to update the gui
        self.guiUpdateTimer = QtCore.QTimer()
        self.guiUpdateTimer.setSingleShot(False)
        self.guiUpdateTimer.timeout.connect(self.refreshGui)
        self.guiUpdateTimer.start(self.applicationSettings.guiUpdateIntervalLengthInMs)

        # for debugging purpose
        self.loopReportTimer = QtCore.QTimer()
        self.loopReportTimer.setSingleShot(False)
        self.connect(self.loopReportTimer, QtCore.SIGNAL("timeout()"), self.printLoopPerformance)
        self.loopReportTimer.start(5000)

        # some calculations for debugging purpose
        self.loopDurationMin = 1000000
        self.loopDurationMax = 0
        self.loopDurationAverage = 0
        self.loopDurationSum = 0
        self.loopDurationCounter = 0

        splashScreen.finish(self)
        logging.info("GUI load complete")





    def setupUi(self):
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        self.centralWidgetLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.centralWidgetLayout.setMargin(0)
        self.centralWidgetLayout.setSpacing(0)

        self.setCentralWidget(self.centralwidget)


        self.setupMainMenu()


    def addTabs(self, tabs):


        if len(tabs) == 1:
            self.addOnlyOneWidget(tabs)
            return

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")

        self.centralWidgetLayout.addWidget(self.tabWidget)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)


        for givenTab in tabs:
            tab = QtGui.QWidget()
            tab.setFont(font)
            tabLayout = QtGui.QHBoxLayout(tab)
            tabLayout.setSpacing(0)
            tabLayout.setMargin(0)
            self.tabWidget.addTab(tab, givenTab.displayName)

            tabContentClass = getattr(import_module(givenTab.pathToClassFile), givenTab.className)
            tabContentClassInstance = tabContentClass(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator)

            tabLayout.addWidget(tabContentClassInstance)

    def addOnlyOneWidget(self, tabs):
        tab = tabs[0]

        tabContentClass = getattr(import_module(tab.pathToClassFile), tab.className)
        tabContentClassInstance = tabContentClass(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator)

        self.centralWidgetLayout.addWidget(tabContentClassInstance)


    def setupMainMenu(self):
        newProjectAction = QtGui.QAction(u"Neues Projekt...", self)
        newProjectAction.setShortcut("Ctrl+N")
        newProjectAction.setStatusTip(u"Legt ein neues Projekt an.")
        newProjectAction.triggered.connect(self.newProject)

        openAction = QtGui.QAction(u"Öffnen...", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.open)

        saveAction = QtGui.QAction(u"Speichern", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.save)

        saveAsAction = QtGui.QAction(u"Speichern unter...", self)
        saveAsAction.setShortcut("Shift+Ctrl+N")
        saveAsAction.triggered.connect(self.saveAs)

        closeAction = QtGui.QAction(u"Programm beenden...", self)
        closeAction.setShortcut("Ctrl+Q")
        closeAction.triggered.connect(self.close)




        showHelpAction = QtGui.QAction(u"Hilfe anzeigen...", self)
        showHelpAction.setShortcut("Ctrl+H")
        showHelpAction.setStatusTip(u"todo")
        showHelpAction.triggered.connect(self.showHelp)

        aboutAction = QtGui.QAction(u"Über das Programm...", self)
        aboutAction.triggered.connect(self.showAboutWindow)




        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Datei")
        fileMenu.addAction(newProjectAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(closeAction)

        helpMenu = mainMenu.addMenu("Hilfe")
        helpMenu.addAction(showHelpAction)
        helpMenu.addAction(aboutAction)

    def newProject(self):
        print "new Project"

    def open(self):
        print "open"

    def save(self):
        print "save"

    def saveAs(self):
        print "save AS"

    def close(self):
        print "close"

    def showHelp(self):
        print "Help"

    def showAboutWindow(self):
        print "About"

    def receiveAndSend(self):
        self.receive()
        self.send()

    def receive(self):
        messages = self.communicator.receive()
        for message in messages:
            self.handleNewData(message)
            self.calculateSomeStuff(message)

    def send(self):
        self.communicator.send(self.commands)

    def refreshGui(self):
        pass
        # self.tabWaterLineExperiment.updateTab(self.channels)
        # self.tabGeneric.updateTab(self.channels)

    def handleNewData(self, message):
        MessageInterpreter.mapUserChannels(self.channels, message)
        returnedCommand = MessageInterpreter.getMicroControllerCommandReturned(message)
        self.commands[returnedCommand.id].checkMicroControllerReturnValue(returnedCommand)

    def calculateSomeStuff(self, message):
        loopCycleDuration = MessageInterpreter.getLoopCycleDuration(message)
        # calculate some statistics
        if loopCycleDuration < self.loopDurationMin:
            self.loopDurationMin = loopCycleDuration
        elif loopCycleDuration > self.loopDurationMax:
            self.loopDurationMax = loopCycleDuration

        self.loopDurationSum += loopCycleDuration
        self.loopDurationCounter += 1
        self.loopDurationAverage = self.loopDurationSum / float(self.loopDurationCounter)

    def printLoopPerformance(self):
        pass
        # print "min", self.loopDurationMin, "max", self.loopDurationMax, "avg", self.loopDurationAverage

    def closeEvent(self, *args, **kwargs):
        print "bye bye"
        QtGui.QApplication.quit()

