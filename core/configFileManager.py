# -*- encoding: utf-8 -*-

import json
from core.valueChannel import ValueChannel
from core.command import Command
from core.model.tabDescription import TabDescription
from core.measurementData import MeasurementData
from core.model.projectSettings import ProjectSettings
from core.command import CommandList
from core.messageData import MessageData, Message
from core.communicator import Communicator

class ConfigFileManager(object):
    def __init__(self, applicationSettings):
        self.applicationSettings = applicationSettings
        # self.projectSettings = projectSettings
        # self.channels = channels
        # self.commands = commands

    def save(self, projectSettings, channels, commands, newPath=None):
        channelDescriptions = list()
        for channel in channels.channels:
            channelDict = dict()
            channelDict["color"] = channel.colorRgbTuple
            channelDict["show"] = channel.show
            channelDict["id"] = channel.id
            channelDict["name"] = channel.name
            channelDict["displayName"] = channel.displayName
            channelDict["displayScaleFactor"] = channel.displayScaleFactor

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
            commandDict["initialValue"] = command.initialValue
            commandDict["pendingMode"] = command._pendingSendMode
            commandDict["inputMethod"] = command._inputMethod
            commandDict["valueType"] = command._valueType
            commandDict["history"] = list(command.history)
            commandDescriptions.append(commandDict)


        projectSettingsDescriptions = dict()

        # projectSettingsDescriptions["projectName"] = projectSettings.projectName
        projectSettingsDescriptions["controllerLoopCycleTimeInUs"] = projectSettings.controllerLoopCycleTimeInUs
        projectSettingsDescriptions["computerIP"] = projectSettings.computerIP
        projectSettingsDescriptions["controllerIP"] = projectSettings.controllerIP
        projectSettingsDescriptions["udpPort"] = projectSettings.udpPort
        projectSettingsDescriptions["controllerFrameworkAndInterface"] = projectSettings.controllerFrameworkAndInterface
        projectSettingsDescriptions["pathToControllerCodeFolder"] = projectSettings.pathToControllerCodeFolder
        projectSettingsDescriptions["comPortDescription"] = projectSettings.comPortDescription
        projectSettingsDescriptions["comPortBaudRate"] = projectSettings.comPortBaudRate
        projectSettingsDescriptions["suppressParameterConfirmation"] = projectSettings.suppressParameterConfirmation
        projectSettingsDescriptions["debugMode"] = projectSettings.debugMode
        projectSettingsDescriptions["messageSkipMode"] = projectSettings.messageSkipMode
        projectSettingsDescriptions["recordBufferLength"] = projectSettings.recordBufferLength
        projectSettingsDescriptions["pauseAfterRecord"] = projectSettings.pauseAfterRecord

        tabSettings = list()
        for aTabSetting in projectSettings.tabSettingsDescriptions:
            tabSettingDict = dict()
            tabSettingDict["pathToClassFile"] = aTabSetting.pathToClassFile
            tabSettingDict["className"] = aTabSetting.className
            tabSettingDict["displayName"] = aTabSetting.displayName
            tabSettings.append(tabSettingDict)
        projectSettingsDescriptions["tabs"] = tabSettings


        everythingDict = dict()
        everythingDict["miscSettings"] = projectSettingsDescriptions
        everythingDict["channels"] = channelDescriptions
        everythingDict["commands"] = commandDescriptions

        path = ""
        if newPath is None:
            path = projectSettings.openedFrom
        else:
            path = newPath
            projectSettings.openedFrom = newPath

        with open(path, "w") as f:
            f.write(json.dumps(everythingDict, indent=4))

    def saveAs(self, path, projectSettings, channels, commands):
        self.save(projectSettings, channels, commands, newPath=path)

    def open(self, path):
        with open(path, "r") as f:
            content = f.read()
            return json.loads(content)


    def buildEmptyModel(self):
        newProjectMiscSettings = ProjectSettings()
        newChannelObjects = MeasurementData(self.applicationSettings.bufferLength)
        newCommandObjects = CommandList()
        newMessageFormatList = list()

        communicator = self.makeCommunicator(newProjectMiscSettings, newMessageFormatList, newCommandObjects)


        return newProjectMiscSettings, newChannelObjects, newCommandObjects, newMessageFormatList, communicator

    def buildModelFromConfigFile(self, pathToConfigFile):
        jsonStuff = self.open(pathToConfigFile)

        newProjectMiscSettings = self.makeProjectMiscSettings(jsonStuff["miscSettings"])
        newProjectMiscSettings.openedFrom = pathToConfigFile

        newChannelObjects = self.makeChannelObjects(jsonStuff["channels"], self.applicationSettings.bufferLength)
        newCommandObjects = self.makeCommandObjects(jsonStuff["commands"])

        newMessageFormatList = self.getMessageFormatList(jsonStuff["channels"], jsonStuff["miscSettings"])


        communicator = self.makeCommunicator(newProjectMiscSettings, newMessageFormatList, newCommandObjects)

        return newProjectMiscSettings, newChannelObjects, newCommandObjects, newMessageFormatList, communicator

    def makeCommunicator(self, projectMiscSettings, messageFormatList, commands):
        return Communicator(self.applicationSettings, projectMiscSettings, messageFormatList, commands)


    def makeChannelObjects(self, channelDescriptions, bufferLength):

        model = MeasurementData(bufferLength)

        if isinstance(channelDescriptions, MeasurementData):
            for oldChannel in channelDescriptions.channels:
                channel = ValueChannel(bufferLength)
                channel.colorRgbTuple = oldChannel.colorRgbTuple
                channel.show = oldChannel.show
                channel.id = oldChannel.id
                channel.name = oldChannel.name
                channel.displayName = oldChannel.displayName
                channel.displayScaleFactor =  oldChannel.displayScaleFactor
                channel.isRequested = oldChannel.isRequested

                model.addChannel(channel)
        else:
            for channelDescription in channelDescriptions:
                channel = ValueChannel(bufferLength)
                if "color" in channelDescription:
                    channel.colorRgbTuple = channelDescription["color"]
                if "show" in channelDescription:
                    channel.show = channelDescription["show"]
                if "id" in channelDescription:
                    channel.id = channelDescription["id"]
                if "name" in channelDescription:
                    channel.name = channelDescription["name"]
                if "displayName" in channelDescription:
                    channel.displayName = channelDescription["displayName"]
                if "displayScaleFactor" in channelDescription:
                    channel.displayScaleFactor = channelDescription["displayScaleFactor"]
                if "isRequested" in channelDescription:
                    channel.isRequested = channelDescription["isRequested"]

                model.addChannel(channel)

        return model



    def makeCommandObjects(self, commandDescriptions):
        commandList = CommandList()
        for commandDescription in commandDescriptions:
            command = Command()

            # add it to the commandList before setting values so that value changes will be transmitted
            commandList.append(command)

            if "id" in commandDescription:
                command.id = commandDescription["id"]

            if "name" in commandDescription:
                command.name = commandDescription["name"]

            if "displayName" in commandDescription:
                command.displayName = commandDescription["displayName"]

            if "min" in commandDescription:
                command._lowerLimit = commandDescription["min"]

            if "max" in commandDescription:
                command._upperLimit = commandDescription["max"]

            if "initialValue" in commandDescription:
                command.initialValue = commandDescription["initialValue"]
                command._value = command.initialValue

            if "pendingMode" in commandDescription:
                command._pendingSendMode = commandDescription["pendingMode"]

            if "inputMethod" in commandDescription:
                command.setInputMethod(commandDescription["inputMethod"])

            if "valueType" in commandDescription:
                command.setValueType(commandDescription["valueType"])

            if "history" in commandDescription:
                for aValue in commandDescription["history"]:
                    command.history.appendleft(aValue)

        return commandList

    def makeProjectMiscSettings(self, settingsDescriptions):
        projectMiscSettings = ProjectSettings()

        # if "projectName" in settingsDescriptions:
        #     projectMiscSettings.projectName = settingsDescriptions["projectName"]

        if "controllerLoopCycleTimeInUs" in settingsDescriptions:
            projectMiscSettings.controllerLoopCycleTimeInUs = settingsDescriptions["controllerLoopCycleTimeInUs"]

        if "pathToControllerCodeFolder" in settingsDescriptions:
            projectMiscSettings.pathToControllerCodeFolder = settingsDescriptions["pathToControllerCodeFolder"]

        if "computerIP" in settingsDescriptions:
            projectMiscSettings.computerIP = settingsDescriptions["computerIP"]

        if "controllerIP" in settingsDescriptions:
            projectMiscSettings.controllerIP = settingsDescriptions["controllerIP"]

        if "udpPort" in settingsDescriptions:
            projectMiscSettings.udpPort = settingsDescriptions["udpPort"]

        if "controllerFrameworkAndInterface" in settingsDescriptions:
            projectMiscSettings.controllerFrameworkAndInterface = settingsDescriptions["controllerFrameworkAndInterface"]

        if "comPortDescription" in settingsDescriptions:
            projectMiscSettings.comPortDescription = settingsDescriptions["comPortDescription"]

        if "comPortBaudRate" in settingsDescriptions:
            projectMiscSettings.comPortBaudRate = settingsDescriptions["comPortBaudRate"]

        if "suppressParameterConfirmation" in settingsDescriptions:
            projectMiscSettings.suppressParameterConfirmation = settingsDescriptions["suppressParameterConfirmation"]

        if "debugMode" in settingsDescriptions:
            projectMiscSettings.debugMode = settingsDescriptions["debugMode"]

        if "messageSkipMode" in settingsDescriptions:
            projectMiscSettings.messageSkipMode = settingsDescriptions["messageSkipMode"]

        if "recordBufferLength" in settingsDescriptions:
            projectMiscSettings.recordBufferLength = settingsDescriptions["recordBufferLength"]

        if "pauseAfterRecord" in settingsDescriptions:
            projectMiscSettings.pauseAfterRecord = settingsDescriptions["pauseAfterRecord"]

        tabSettingsDescriptions = settingsDescriptions["tabs"]

        tabDescriptionObjects = list()
        for aTabSetting in tabSettingsDescriptions:
            tabDescription = TabDescription()

            tabDescription.pathToClassFile = aTabSetting["pathToClassFile"]
            tabDescription.className = aTabSetting["className"]
            tabDescription.displayName = aTabSetting["displayName"]

            tabDescriptionObjects.append(tabDescription)

        projectMiscSettings.tabSettingsDescriptions = tabDescriptionObjects

        return projectMiscSettings


    def getMessageFormatList(self, channelDescriptionsOrMeasurementData, projectSettingsOrDescriptions):
        messagePartsList = list()

        messageInformation = Message()


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
        mData.unpackString = "<I"   # unsigned int
        mData.name = "loopStartTime"
        messageInformation.append(mData)

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
        # messageInformation.append(mData1)


        # status first byte
        mData2 = MessageData()
        # mData2.id = channelCounter
        channelCounter += 1
        mData2.positionInBytes = positionCounter
        mData2.lengthInBytes = 2
        # mData2.lengthInBytes = 2
        positionCounter += mData2.lengthInBytes
        mData2.dataType = str
        # mData2.unpackString = "<I"  # unsigned int
        mData2.unpackString = "<h"
        mData2.name = "statusFlagsOne"
        messageInformation.append(mData2)

        # # status second byte
        # mData3 = MessageData()
        # # mData3.id = channelCounter
        # channelCounter += 1
        # mData3.positionInBytes = positionCounter
        # mData3.lengthInBytes = 1
        # # mData3.lengthInBytes = 1
        # positionCounter += mData3.lengthInBytes
        # mData3.dataType = str
        # # mData3.unpackString = "<I"  # unsigned int
        # mData3.unpackString = "<c" # char
        # mData3.name = "statusFlagsTwo"
        # messageInformation.append(mData3)

        # parameterNumber
        mData4 = MessageData()
        # mData4.id = channelCounter
        channelCounter += 1
        mData4.positionInBytes = positionCounter
        mData4.lengthInBytes = 2
        # mData4.lengthInBytes = 2
        positionCounter += mData4.lengthInBytes
        mData4.dataType = int
        # mData4.unpackString = "<I"  # unsigned int
        mData4.unpackString = "<h" # signed short
        mData4.name = "parameterNumber"
        messageInformation.append(mData4)


        suppressParameterConfirmation = False
        if isinstance(projectSettingsOrDescriptions, ProjectSettings):
            if projectSettingsOrDescriptions.suppressParameterConfirmation is True:
                suppressParameterConfirmation = True
            else:
                suppressParameterConfirmation = False
        else:
            if "suppressParameterConfirmation" in projectSettingsOrDescriptions:
                if projectSettingsOrDescriptions["suppressParameterConfirmation"] is True:
                    suppressParameterConfirmation = True
                else:
                    suppressParameterConfirmation = False


        if suppressParameterConfirmation is False:


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
            messageInformation.append(mData3)

        # channels
        if isinstance(channelDescriptionsOrMeasurementData, MeasurementData):
            for i, channel in enumerate(channelDescriptionsOrMeasurementData.channels):
                if not channel.isRequested:
                    continue
                messageData = MessageData()
                # messageData.id = i
                messageData.positionInBytes = positionCounter
                messageData.lengthInBytes = 4
                messageData.dataType = float
                messageData.unpackString = "<f"
                messageData.name = channel.name
                messageData.isUserChannel = True
                messageData.userChannelId = i
                messageInformation.append(messageData)
                positionCounter += messageData.lengthInBytes
                channelCounter += 1
        else:
            for i, channelDescription in enumerate(channelDescriptionsOrMeasurementData):
                if not channelDescription["isRequested"]:
                    continue
                messageData = MessageData()
                # messageData.id = i
                messageData.positionInBytes = positionCounter
                messageData.lengthInBytes = 4
                messageData.dataType = float
                messageData.unpackString = "<f"
                messageData.name = channelDescription["name"]
                messageData.isUserChannel = True
                messageData.userChannelId = i
                messageInformation.append(messageData)
                positionCounter += messageData.lengthInBytes
                channelCounter += 1

        messageInformation.messageLengthInBytes = positionCounter

        return messageInformation

