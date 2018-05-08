# -*- encoding: utf-8 -*-

import struct

from core.command import CommandConfirmation


class MessageInterpreter():
    def __init__(self):
        pass

    @staticmethod
    def mapUserChannels(measurementDataModel, message):
        # check here if the controller has been reset and if so clear all buffers
        newestTimeInSec = None
        for messagePart in message:
            if messagePart.name == "loopStartTime":
                newestTimeInSec = float(messagePart.value) / 1000000.0

        lastTime = measurementDataModel.timeValues[len(measurementDataModel.timeValues) - 1]
        # lastTime = measurementDataModel.timeValues[-1]

        if measurementDataModel.isEmpty or newestTimeInSec < lastTime:
            measurementDataModel.clear(newestTimeInSec)
            measurementDataModel.isEmpty = False

        # append incoming values to buffers
        for i in range(0, len(message)):
            if message[i].isUserChannel is True:
                userChannelId = message[i].userChannelId
                measurementDataModel.channels[userChannelId].append(message[i].value * measurementDataModel.channels[userChannelId].displayScaleFactor)
            elif message[i].name == "loopStartTime":
                measurementDataModel.timeValues.append(float(message[i].value) / 1000000.0)


    @staticmethod
    def getLoopCycleDuration(messages):
        for i, message in enumerate(messages):
            if message.name == "lastLoopDuration":
                return message.value
        return 0

    @staticmethod
    def getMicroControllerCommandReturned(message, commands):
        cmd = CommandConfirmation()
        for i, messagePart in enumerate(message):
            if messagePart.name == "parameterNumber":
                cmd.id = messagePart.value
            if messagePart.name == "parameterValue":
                # cmd.returnValue = messagePart.value


                if cmd.id < 0:
                    messagePart.value = struct.unpack("<f", messagePart.rawValue)[0]
                elif commands.getCommandById(cmd.id).getValueType() == commands.getCommandById(cmd.id).FLOAT_TYPE:
                    messagePart.value = struct.unpack("<f", messagePart.rawValue)[0]
                elif commands.getCommandById(cmd.id).getValueType() == commands.getCommandById(cmd.id).INT_TYPE:
                    messagePart.value = struct.unpack("<i", messagePart.rawValue)[0]
                else:
                    pass

                cmd.returnValue = messagePart.value

        return cmd



    @staticmethod
    def checkStatusFlags(status, messages):
        for i, message in enumerate(messages):
            if message.name == "statusFlagsOne":
                statusBytes = int(message.value)
                firstFlag = statusBytes & (1 << 0)
                secondFlag = statusBytes & (1 << 1)
                thirdFlag = statusBytes & (1 << 2)

                if firstFlag > 0:
                    status.badData = True
                else:
                    status.badData = False

                if secondFlag > 0:
                    status.skippedTransmission = True
                else:
                    status.skippedTransmission = False

            if message.name == "statusFlagsTwo":
                pass

        return 0