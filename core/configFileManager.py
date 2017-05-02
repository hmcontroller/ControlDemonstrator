# -*- encoding: utf-8 -*-

import json
from core.valueChannel import ValueChannel
from core.command import Command
from core.model.applicationSettings import ApplicationSettings
from core.model.tabDescription import TabDescription

class ConfigFileManager(object):
    def __init__(self, applicationSettings, channels, commands):
        self.applicationSettings = applicationSettings
        self.channels = channels
        self.commands = commands

    def save(self):
        channels = list()
        for channel in self.channels.channels:
            channelDict = dict()
            channelDict["color"] = channel.colorRgbTuple
            channelDict["show"] = channel.show
            channelDict["id"] = channel.id
            channelDict["name"] = channel.name
            channelDict["isRequested"] = channel.isRequested
            channels.append(channelDict)

        commands = list()
        for command in self.commands:
            commandDict = dict()
            commandDict["id"] = command.id
            commandDict["name"] = command.name
            commandDict["displayName"] = command.displayName
            commandDict["min"] = command._lowerLimit
            commandDict["max"] = command._upperLimit
            commandDict["value"] = command._value
            commandDict["pendingMode"] = command._pendingSendMode
            commands.append(commandDict)


        miscSettings = dict()

        miscSettings["controllerLoopCycleTimeInUs"] = self.applicationSettings.controllerLoopCycleTimeInUs
        miscSettings["bufferLength"] = self.applicationSettings.bufferLength
        miscSettings["guiUpdateIntervalLengthInMs"] = self.applicationSettings.guiUpdateIntervalLengthInMs
        miscSettings["receiveMessageIntervalLengthInMs"] = self.applicationSettings.receiveMessageIntervalLengthInMs
        miscSettings["sendMessageIntervalLengthInMs"] = self.applicationSettings.sendMessageIntervalLengthInMs
        miscSettings["computerIP"] = self.applicationSettings.computerIP
        miscSettings["controllerIP"] = self.applicationSettings.controllerIP
        miscSettings["udpPort"] = self.applicationSettings.udpPort
        miscSettings["controllerFrameworkAndInterface"] = self.applicationSettings.controllerFrameworkAndInterface

        tabSettings = list()
        for aTabSetting in self.applicationSettings.tabs:
            tabSettingDict = dict()
            tabSettingDict["pathToClassFile"] = aTabSetting.pathToClassFile
            tabSettingDict["className"] = aTabSetting.className
            tabSettingDict["displayName"] = aTabSetting.displayName
            tabSettings.append(tabSettingDict)
        miscSettings["tabs"] = tabSettings


        everythingDict = dict()
        everythingDict["miscSettings"] = miscSettings
        everythingDict["channels"] = channels
        everythingDict["commands"] = commands


        with open("testConfig.txt", "w") as f:
            f.write(json.dumps(everythingDict, indent=4))

    def open(self, path):
        with open(path, "r") as f:
            content = f.read()
            return json.loads(content)

    def buildModelFromConfigFile(self, pathToConfigFile):
        jsonStuff = self.open(pathToConfigFile)

        newAppSettingsObject = self.makeApplicationSettings(jsonStuff["miscSettings"])



        newChannelObjects = self.makeChannelObjects(jsonStuff["channels"], newAppSettingsObject.bufferLength)
        newCommandObjects = self.makeCommandObjects(jsonStuff["commands"])

        print newAppSettingsObject
        print newChannelObjects
        print newCommandObjects

    def makeChannelObjects(self, channelDescriptions, bufferLength):
        channels = list()
        for channelDescription in channelDescriptions:
            print channelDescription
            channel = ValueChannel(bufferLength)
            channel.colorRgbTuple = channelDescription["color"]
            channel.show = channelDescription["show"]
            channel.id = channelDescription["id"]
            channel.name = channelDescription["name"]
            channel.isRequested = channelDescription["isRequested"]
            channels.append(channel)
        return channels

    def makeCommandObjects(self, commandDescriptions):
        commands = list()
        for commandDescription in commandDescriptions:
            command = Command()
            command.id = commandDescription["id"]
            command.name = commandDescription["name"]
            command.displayName = commandDescription["displayName"]
            command._lowerLimit = commandDescription["min"]
            command._upperLimit = commandDescription["max"]
            command._value = commandDescription["value"]
            command._pendingSendMode = commandDescription["pendingMode"]
            commands.append(command)
        return commands

    def makeApplicationSettings(self, applicationSettingsDescriptions):
        appSettings = ApplicationSettings()

        appSettings.controllerLoopCycleTimeInUs = applicationSettingsDescriptions["controllerLoopCycleTimeInUs"]
        appSettings.bufferLength = applicationSettingsDescriptions["bufferLength"]
        appSettings.guiUpdateIntervalLengthInMs = applicationSettingsDescriptions["guiUpdateIntervalLengthInMs"]
        appSettings.receiveMessageIntervalLengthInMs = applicationSettingsDescriptions["receiveMessageIntervalLengthInMs"]
        appSettings.sendMessageIntervalLengthInMs = applicationSettingsDescriptions["sendMessageIntervalLengthInMs"]
        appSettings.computerIP = applicationSettingsDescriptions["computerIP"]
        appSettings.controllerIP = applicationSettingsDescriptions["controllerIP"]
        appSettings.udpPort = applicationSettingsDescriptions["udpPort"]
        appSettings.controllerFrameworkAndInterface = applicationSettingsDescriptions["controllerFrameworkAndInterface"]

        tabSettingsDescriptions = applicationSettingsDescriptions["tabs"]

        tabDescriptionObjects = list()
        for aTabSetting in tabSettingsDescriptions:
            tabDescription = TabDescription()

            tabDescription.pathToClassFile = aTabSetting["pathToClassFile"]
            tabDescription.className = aTabSetting["className"]
            tabDescription.displayName = aTabSetting["displayName"]

            tabDescriptionObjects.append(tabDescription)

        appSettings.tabs = tabDescriptionObjects


        return appSettings