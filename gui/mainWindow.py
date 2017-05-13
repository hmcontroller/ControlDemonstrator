# -*- encoding: utf-8 -*-
import os
import logging
from importlib import import_module
import json
import pickle
import collections
import webbrowser

from PyQt4 import QtCore, QtGui
import sip

from core.modelMaker import ModelMaker
from core.communicator import UdpCommunicator
from core.communicator import SerialCommunicator
from core.messageInterpreter import MessageInterpreter
from core.configFileManager import ConfigFileManager
from core.applicationSettingsManager import ApplicationSettingsManager
from core.model.projectSettings import ProjectSettings

from gui.aboutDialog import AboutDialog
from gui.projectMiscSettingsDialog import ProjectMiscSettingsDialog
from gui.channelSettingsDialog import ChannelSettingsDialog
from gui.commandSettingsDialog import CommandSettingsDialog

from gui.constants import *
# from gui.TabWaterLineExperiment import TabWaterLineExperiment
# from gui.TabGenericView import TabGenericView
# from gui.TabSmallGenericView import TabSmallGenericView

class ControlDemonstratorMainWindow(QtGui.QMainWindow):
    def __init__(self, rootFolder):
        QtGui.QMainWindow.__init__(self)

        self.appSettingsManager = ApplicationSettingsManager(PATH_TO_APPLICATION_SETTINGS)
        self.applicationSettings = self.appSettingsManager.restoreSettingsFromFile()
        self.applicationSettings.changed.connect(self.appSettingsChanged)

        # setup a timer, that triggers to read from the controller
        self.receiveTimer = QtCore.QTimer()
        self.receiveTimer.setSingleShot(False)
        self.receiveTimer.timeout.connect(self.receiveAndSend)


        self.projectConfigManager = ConfigFileManager(self.applicationSettings)


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









        if len(self.applicationSettings.recentProjectFilePathes) > 0:
            self.loadProject(self.applicationSettings.recentProjectFilePathes[0])












        # self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)


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

        mainMenu = self.menuBar()
        self.fileMenu = mainMenu.addMenu("Datei")
        self.fileMenu.addAction(newProjectAction)
        self.fileMenu.addAction(openAction)

        self.openRecentMenu = self.fileMenu.addMenu("Letze Projekte...")
        self.refreshRecentProjectsMenu()

        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(saveAsAction)
        self.fileMenu.addAction(closeAction)


        editProjectMiscSettingsAction = QtGui.QAction(u"Projekteinstellungen...", self)
        editProjectMiscSettingsAction.triggered.connect(self.editProjectMiscSettings)

        editChannelsAction = QtGui.QAction(u"Kanaleinstellungen...", self)
        editChannelsAction.triggered.connect(self.editChannels)

        editCommandsAction = QtGui.QAction(u"Parametereinstellungen...", self)
        editCommandsAction.triggered.connect(self.editCommands)



        editMenu = mainMenu.addMenu("Bearbeiten")
        editMenu.addAction(editProjectMiscSettingsAction)
        editMenu.addAction(editChannelsAction)
        editMenu.addAction(editCommandsAction)


        showHelpAction = QtGui.QAction(u"Hilfe anzeigen...", self)
        showHelpAction.setShortcut("Ctrl+H")
        showHelpAction.setStatusTip(u"todo")
        showHelpAction.triggered.connect(self.showHelp)

        aboutAction = QtGui.QAction(u"Über das Programm...", self)
        aboutAction.triggered.connect(self.showAboutWindow)

        helpMenu = mainMenu.addMenu("Hilfe")
        helpMenu.addAction(showHelpAction)
        helpMenu.addAction(aboutAction)

    def refreshRecentProjectsMenu(self):
        self.openRecentMenu.clear()
        for i, recentPath in enumerate(self.applicationSettings.recentProjectFilePathes):
            displayPath = recentPath
            displayPath = displayPath.split("/")
            displayPath = displayPath[-1]
            displayPath = displayPath.replace(".json", "")
            action = QtGui.QAction(u"{}".format(displayPath), self)
            action.triggered.connect(self.openRecent)
            action.setData(QtCore.QVariant(recentPath))
            self.openRecentMenu.addAction(action)


    def newProject(self):

        tempProjectSettings = ProjectSettings()
        accepted = self.editProjectMiscSettings(self.projectSettings)

        if accepted == QtGui.QDialog.Accepted:
            self.closeCurrentProject()
            self.makeEmptyProject()
            self.projectSettings = tempProjectSettings
            self.projectSettings.changed.connect(self.projectSettingsChanged)
            self.saveAs()


    def makeEmptyProject(self):
        self.projectSettings, self.channels, self.commands, self.messageFormatList, self.communicator = self.projectConfigManager.buildEmptyModel()
        self.projectSettings.changed.connect(self.projectSettingsChanged)

    def closeCurrentProject(self):
        while self.centralWidgetLayout.count() > 0:
            item = self.centralWidgetLayout.takeAt(0)
            item.widget().deleteLater()
        self.receiveTimer.stop()

    def open(self):
        print "open"

        folderPath = "D:\\00 eigene Daten\\000 FH\\S 4\\Regelungstechnik\\Regelungsversuch\\ControlDemonstratorProjects\\"



        projectFilePath = QtGui.QFileDialog.getOpenFileName(self,
                                                              "Open project file",
                                                              folderPath,
                                                              "Project Settings (*.json)")
        projectFilePath = str(projectFilePath)
        if projectFilePath == "":
            print "no project file given"
            return
        else:
            self.loadProject(projectFilePath)

    def openRecent(self, *args):
        recentPath = str(self.sender().data().toString())
        self.loadProject(recentPath)

    def loadProject(self, pathToProjectFile):

        self.closeCurrentProject()

        self.projectSettings, self.channels, self.commands, self.messageFormatList, self.communicator = self.projectConfigManager.buildModelFromConfigFile(pathToProjectFile)
        self.projectSettings.changed.connect(self.projectSettingsChanged)

        self.communicator.setMessageMap(self.messageFormatList)
        self.communicator.connectToController()

        self.addTabs(self.projectSettings.tabSettingsDescriptions)

        self.applicationSettings.addRecentProjektPath(pathToProjectFile)

        displayPath = pathToProjectFile
        displayPath = displayPath.split("/")
        displayPath = displayPath[-1]
        displayPath = displayPath.replace(".json", "")

        self.setWindowTitle(u"ControlDemonstrator - {}".format(self.projectSettings.projectName))
        self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

    def projectSettingsChanged(self, newSettings):
        newWindowTitle = self.projectSettings.projectName
        if self.projectSettings.unsavedChanges is True:
            newWindowTitle += u" (unsaved)"
        self.setWindowTitle(u"ControlDemonstrator - {}".format(newWindowTitle))


    def save(self):
        self.projectConfigManager.save(self.projectSettings, self.channels, self.commands)
        self.projectSettings.unsavedChanges = False

    def saveAs(self):
        folder = os.path.dirname(self.projectSettings.openedFrom)
        projectFilePath = QtGui.QFileDialog.getSaveFileName(self,
                                                              "Projekt speichern unter...",
                                                              folder,
                                                              "Project Settings (*.json)")
        projectFilePath = str(projectFilePath)
        if projectFilePath == "":
            print "cancel"
            return
        else:
            self.projectConfigManager.saveAs(projectFilePath, self.projectSettings, self.channels, self.commands)

        self.loadProject(projectFilePath)

    def close(self):
        if self.projectSettings.unsavedChanges is True:
            print "SAVE ?"
        else:
            QtCore.QCoreApplication.quit()

    def showHelp(self):
        pathToIndexHtml = os.path.abspath(os.path.join(os.getcwd(), "docs/sphinxHtml/index.html"))
        url = "file://" + pathToIndexHtml
        webbrowser.open(url)

    def showAboutWindow(self):
        aboutDialog = AboutDialog()
        aboutDialog.exec_()

    def editProjectMiscSettings(self, settings):
        if settings is False or None:
            # happens when this function is called from a signal
            settings = self.projectSettings

        dialog = ProjectMiscSettingsDialog(settings)
        return dialog.updateSettings()


    def editChannels(self, settings):
        dialog = ChannelSettingsDialog(self.channels, self.applicationSettings)
        dialog.updateSettings()

    def editCommands(self):
        dialog = CommandSettingsDialog(self.commands)
        dialog.updateSettings()

    def appSettingsChanged(self, settings):
        self.refreshRecentProjectsMenu()

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

