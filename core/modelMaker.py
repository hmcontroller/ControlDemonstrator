# -*- encoding: utf-8 -*-
import ConfigParser
import json

from core.settingsModel import Settings
from core.command import Command
from core.messageData import MessageData


class ModelMaker():
    def __init__(self, configFilePath):
        self.configFilePath = configFilePath
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config.optionxform = str
        self.config.read(self.configFilePath)

    def getCommands(self):
        commands = dict()
        for i, name in enumerate(self.config.options('requestedControlledParameters')):
            cmd = Command()
            cmd.value = 0
            cmd.id = i
            cmd.name = name
            commands[name] = cmd
        return commands

    def getMeasurementDataModel(self):
        pass

    def getMessageFormatList(self):
        messageDataList = list()

        # value channels
        for i, channelName in enumerate(self.config.options('requestedFastParameters')):
            messageData = MessageData()
            messageData.position = i
            messageData.dataType = float
            messageData.name = channelName
            messageDataList.append(messageData)

        # TODO dirty get the additional message stuff from some single source

        # loopStartTime
        mData = MessageData()
        mData.id = len(messageDataList) + 1
        mData.dataType = int
        mData.name = "loopStartTime"
        messageDataList.append(mData)

        # lastLoopDuration
        mData1 = MessageData()
        mData1.id = len(messageDataList) + 2
        mData1.dataType = int
        mData1.name = "lastLoopDuration"
        messageDataList.append(mData1)

        # parameterNumber
        mData2 = MessageData()
        mData2.id = len(messageDataList) + 3
        mData2.dataType = int
        mData2.name = "parameterNumber"
        messageDataList.append(mData2)

        # parameterValue
        mData3 = MessageData()
        mData3.id = len(messageDataList) + 4
        mData3.dataType = float
        mData3.name = "parameterValue"
        messageDataList.append(mData3)

        return messageDataList

    def getSensorMapping(self):
        mappingString = self.config.get("Sensors", "mapping")
        mappingString = mappingString.replace("\n", "").replace(" ", "")
        return json.loads(mappingString)

    def getMiscSettings(self):
        settingsModel = Settings()
        settingsModel.controllerLoopCycleTime = self.config.getint("misc", "loopCycleTimeUS")
        settingsModel.bufferLength = self.config.getint("misc", "bufferSizePC")
        return settingsModel

