# -*- encoding: utf-8 -*-
import ConfigParser

from core.model.applicationSettings import ApplicationSettings
from core.command import Command
from core.command import CommandList
from core.messageData import MessageData
from core.measurementData import MeasurementData
from core.valueChannel import ValueChannel
from core.communicator import *
from core.constants import *
from core.commandArgumentsParser import CommandArgumentsParser
from core.model.tabDescription import TabDescription
from core.model.projectSettings import ProjectSettings

class ModelMaker():
    def __init__(self, configFilePath):
        self.configFilePath = configFilePath
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config.optionxform = str
        self.config.read(self.configFilePath)


    def getCommands(self):
        commandList = CommandList()

        settings = self.getApplicationSettings()

        parameters = self.config.options('parameters')


        for i, name in enumerate(parameters):

            cmd = Command()
            cmd.id = i
            cmd.name = name

            if cmd.name in parameters:
                cmd.setIsSelectedAsActive(True)

            # cmd.displayName = args.displayName

            # cmd.value = 0.0
            cmd.timeOutDuration = 1000 #int(float(settings.controllerLoopCycleTimeInUs * len(configSections) * 5) / float(1000))

            # after appending the cmd, value changes are possible
            commandList.append(cmd)

            try:
                argsString = self.config.get("parameters", name)
                cmd.rawArgumentString = argsString
                parser = CommandArgumentsParser(cmd)
                cmd = parser.setCommandAttributesFromConfigFileArguments()
            except ConfigParser.NoOptionError:
                # no args exist
                pass

        return commandList


    def getMeasurementDataModel(self):

        bufferLength = self.config.getint("misc", "bufferSizePC")

        model = MeasurementData(bufferLength)

        for i, channelName in enumerate(self.config.options('requestedChannels')):
            channel = ValueChannel(bufferLength)
            channel.id = i
            channel.name = channelName
            channel.colorRgbTuple = CHANNEL_COLORS[i % len(CHANNEL_COLORS)]
            model.addChannel(channel)
            for n in range(0, bufferLength):
                channel.appendSilently(0.0)

        model.timeValues = ValueChannel(bufferLength)
        for i in range(0, bufferLength):
            model.timeValues.appendSilently(0.0)

        return model

    def getCommunicator(self):
        settings = self.getApplicationSettings()

        serialCases = ["arduino_serial"]
        udpCases = ["mbed_OS_udp", "arduino_udp"]

        if settings.controllerFrameworkAndInterface in serialCases:
            return SerialCommunicator(settings)
        elif settings.controllerFrameworkAndInterface in udpCases:
            return UdpCommunicator(settings)
        else:
            raise Exception("parameter 'controllerFrameworkAndInterface' not valid.")

    def getMessageFormatList(self):
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
        for i, channelName in enumerate(self.config.options('requestedChannels')):
            messageData = MessageData()
            # messageData.id = i
            messageData.positionInBytes = positionCounter
            messageData.lengthInBytes = 4
            messageData.dataType = float
            messageData.unpackString = "<f"
            messageData.name = channelName
            messageData.isUserChannel = True
            messageData.userChannelId = i
            messagePartsList.append(messageData)
            positionCounter += messageData.lengthInBytes
            channelCounter += 1

        return messagePartsList

    def getApplicationSettings(self):
        settings = ApplicationSettings()
        settings.controllerLoopCycleTimeInUs = self.config.getint("misc", "loopCycleTimeUS")
        settings.bufferLength = self.config.getint("misc", "bufferSizePC")
        settings.guiUpdateIntervalLengthInMs = self.config.getint("misc", "guiUpdateIntervalLengthInMs")
        settings.receiveMessageIntervalLengthInMs = self.config.getint("misc", "receiveMessageIntervalLengthInMs")
        settings.sendMessageIntervalLengthInMs = self.config.getint("misc", "sendMessageIntervalLengthInMs")
        settings.computerIP = self.config.get("misc", "computerIP")
        settings.controllerIP = self.config.get("misc", "controllerIP")
        settings.udpPort = self.config.getint("misc", "udpPort")
        settings.controllerFrameworkAndInterface = self.config.get("misc", "microcontrollerFrameworkAndInterface")

        settings.tabs = self.getTabConfigList()

        return settings

    def getProjectMiscSettings(self):
        settings = ProjectSettings()
        settings.controllerLoopCycleTimeInUs = self.config.getint("misc", "loopCycleTimeUS")
        settings.bufferLength = self.config.getint("misc", "bufferSizePC")
        settings.guiUpdateIntervalLengthInMs = self.config.getint("misc", "guiUpdateIntervalLengthInMs")
        settings.receiveMessageIntervalLengthInMs = self.config.getint("misc", "receiveMessageIntervalLengthInMs")
        settings.sendMessageIntervalLengthInMs = self.config.getint("misc", "sendMessageIntervalLengthInMs")
        settings.computerIP = self.config.get("misc", "computerIP")
        settings.controllerIP = self.config.get("misc", "controllerIP")
        settings.udpPort = self.config.getint("misc", "udpPort")
        settings.controllerFrameworkAndInterface = self.config.get("misc", "microcontrollerFrameworkAndInterface")

        settings.tabs = self.getTabConfigList()

        return settings


    def getTabDescriptions(self):
        tabs = list()
        tabEntries = self.config.options('tabs')
        for tabEntry in tabEntries:
            options = self.config.get("tabs", tabEntry)
            tabs.append((tabEntry, options))

        return tabs


    def getTabConfigList(self):


        tabDescriptions = self.getTabDescriptions()

        tabConfigList = list()

        for givenTab in tabDescriptions:
            tabDescription = TabDescription()

            tabDescription.pathToClassFile = givenTab[0]

            arguments = givenTab[1].split(";")
            for arg in arguments:
                arg = arg.strip()

            if arguments is None or len(arguments) != 2:
                raise Exception("Please specify the class name and a display name separated "
                                "by a ';' for the entry {} in the config file under section tabs".format(tabDescription.pathToClassFile))

            tabDescription.className = arguments[0]
            tabDescription.displayName = arguments[1].decode('utf-8')

            tabConfigList.append(tabDescription)

        return tabConfigList


