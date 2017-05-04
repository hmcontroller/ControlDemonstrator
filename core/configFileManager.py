# -*- encoding: utf-8 -*-

import json
from core.valueChannel import ValueChannel
from core.command import Command
from core.model.applicationSettings import ApplicationSettings
from core.model.tabDescription import TabDescription
from core.measurementData import MeasurementData
from core.model.projectSettings import ProjectSettings
from core.command import CommandList
from core.messageData import MessageData

class ConfigFileManager(object):
    def __init__(self, applicationSettings):
        self.applicationSettings = applicationSettings
        # self.projectSettings = projectSettings
        # self.channels = channels
        # self.commands = commands

    def save(self, pathToFile, projectSettings, channels, commands):
        channelDescriptions = list()
        for channel in channels.channels:
            channelDict = dict()
            channelDict["color"] = channel.colorRgbTuple
            channelDict["show"] = channel.show
            channelDict["id"] = channel.id
            channelDict["name"] = channel.name
            channelDict["isRequested"] = channel.isRequested
            channelDescriptions.append(channelDict)

        commandDescriptions = list()
        for command in commands:
            commandDict = dict()
            commandDict["id"] = command.id
            commandDict["name"] = command.name
            commandDict["displayName"] = command.displayName
            commandDict["min"] = command._lowerLimit
            commandDict["max"] = command._upperLimit
            commandDict["value"] = command._value
            commandDict["pendingMode"] = command._pendingSendMode
            commandDescriptions.append(commandDict)


        projectSettingsDescriptions = dict()

        projectSettingsDescriptions["controllerLoopCycleTimeInUs"] = projectSettings.controllerLoopCycleTimeInUs
        projectSettingsDescriptions["computerIP"] = projectSettings.computerIP
        projectSettingsDescriptions["controllerIP"] = projectSettings.controllerIP
        projectSettingsDescriptions["udpPort"] = projectSettings.udpPort
        projectSettingsDescriptions["controllerFrameworkAndInterface"] = projectSettings.controllerFrameworkAndInterface

        tabSettings = list()
        for aTabSetting in projectSettings.tabs:
            tabSettingDict = dict()
            tabSettingDict["pathToClassFile"] = aTabSetting.pathToClassFile
            tabSettingDict["className"] = aTabSetting.className
            tabSettingDict["displayName"] = aTabSetting.displayName
            tabSettings.append(tabSettingDict)
        projectSettingsDescriptions["tabs"] = tabSettings


        everythingDict = dict()
        everythingDict["miscSettings"] = projectSettingsDescriptions
        everythingDict["channels"] = channels
        everythingDict["commands"] = commands


        with open(pathToFile, "w") as f:
            f.write(json.dumps(everythingDict, indent=4))

    def open(self, path):
        with open(path, "r") as f:
            content = f.read()
            return json.loads(content)


    def buildModelFromConfigFile(self, pathToConfigFile):
        jsonStuff = self.open(pathToConfigFile)

        newProjectMiscSettings = self.makeProjectMiscSettings(jsonStuff["miscSettings"])

        newChannelObjects = self.makeChannelObjects(jsonStuff["channels"], self.applicationSettings.bufferLength)
        newCommandObjects = self.makeCommandObjects(jsonStuff["commands"])

        newMessageFormatList = self.getMessageFormatList(jsonStuff["channels"])


        return newProjectMiscSettings, newChannelObjects, newCommandObjects, newMessageFormatList

    def makeChannelObjects(self, channelDescriptions, bufferLength):

        model = MeasurementData()

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
            for n in range(0, bufferLength):
                channel.appendSilently(0.0)

        model.channels = channels

        model.timeValues = ValueChannel(bufferLength)
        for i in range(0, bufferLength):
            model.timeValues.appendSilently(0.0)

        return model

    def makeCommandObjects(self, commandDescriptions):
        commandList = CommandList()
        for commandDescription in commandDescriptions:
            command = Command()

            # add it to the commandList before setting values so that value changes will be transmitted
            commandList.append(command)

            command.id = commandDescription["id"]
            command.name = commandDescription["name"]
            command.displayName = commandDescription["displayName"]
            command._lowerLimit = commandDescription["min"]
            command._upperLimit = commandDescription["max"]
            command._value = commandDescription["value"]
            command._pendingSendMode = commandDescription["pendingMode"]

        return commandList

    def makeProjectMiscSettings(self, settingsDescriptions):
        projectMiscSettings = ProjectSettings()

        projectMiscSettings.controllerLoopCycleTimeInUs = settingsDescriptions["controllerLoopCycleTimeInUs"]
        projectMiscSettings.computerIP = settingsDescriptions["computerIP"]
        projectMiscSettings.controllerIP = settingsDescriptions["controllerIP"]
        projectMiscSettings.udpPort = settingsDescriptions["udpPort"]
        projectMiscSettings.controllerFrameworkAndInterface = settingsDescriptions["controllerFrameworkAndInterface"]

        tabSettingsDescriptions = settingsDescriptions["tabs"]

        tabDescriptionObjects = list()
        for aTabSetting in tabSettingsDescriptions:
            tabDescription = TabDescription()

            tabDescription.pathToClassFile = aTabSetting["pathToClassFile"]
            tabDescription.className = aTabSetting["className"]
            tabDescription.displayName = aTabSetting["displayName"]

            tabDescriptionObjects.append(tabDescription)

        projectMiscSettings.tabs = tabDescriptionObjects

        return projectMiscSettings


    def getMessageFormatList(self, channelDescriptions):
        messagePartsList = list()

        positionCounter = 0
        channelCounter = 0



        # TODO dirty get the fix message stuff from some single source place
        # TODO maybe put the typedefs in the config.c file

        # loopStartTime
        mData = MessageData()
        # mData.id = channelCounter
        channelCounter += 1
        mData.positionInBytes = positionCounter
        # mData.lengthInBytes = 2
        mData.lengthInBytes = 4
        positionCounter += mData.lengthInBytes
        mData.dataType = int
        # mData.unpackString = "<h"
        mData.unpackString = "<I"
        mData.name = "loopStartTime"
        messagePartsList.append(mData)

        # # lastLoopDuration
        # mData1 = MessageData()
        # # mData1.id = channelCounter
        # channelCounter += 1
        # mData1.positionInBytes = positionCounter
        # mData1.lengthInBytes = 2
        # # mData1.lengthInBytes = 4
        # positionCounter += mData1.lengthInBytes
        # mData1.dataType = int
        # mData1.unpackString = "<h"
        # # mData1.unpackString = "<i"
        # mData1.name = "lastLoopDuration"
        # messagePartsList.append(mData1)

        # parameterNumber
        mData2 = MessageData()
        # mData2.id = channelCounter
        channelCounter += 1
        mData2.positionInBytes = positionCounter
        mData2.lengthInBytes = 4
        # mData2.lengthInBytes = 4
        positionCounter += mData2.lengthInBytes
        mData2.dataType = int
        mData2.unpackString = "<I"
        # mData2.unpackString = "<i"
        mData2.name = "parameterNumber"
        messagePartsList.append(mData2)

        # parameterValue
        mData3 = MessageData()
        # mData3.id = channelCounter
        channelCounter += 1
        mData3.positionInBytes = positionCounter
        mData3.lengthInBytes = 4
        positionCounter += mData3.lengthInBytes
        mData3.dataType = float
        mData3.unpackString = "<f"
        mData3.name = "parameterValue"
        messagePartsList.append(mData3)

        # channels

        for i, channelDescription in enumerate(channelDescriptions):
            messageData = MessageData()
            # messageData.id = i
            messageData.positionInBytes = positionCounter
            messageData.lengthInBytes = 4
            messageData.dataType = float
            messageData.unpackString = "<f"
            messageData.name = channelDescription["name"]
            messageData.isUserChannel = True
            messageData.userChannelId = i
            messagePartsList.append(messageData)
            positionCounter += messageData.lengthInBytes
            channelCounter += 1

        return messagePartsList

