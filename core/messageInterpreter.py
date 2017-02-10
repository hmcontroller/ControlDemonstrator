# -*- encoding: utf-8 -*-

from core.command import CommandConfirmation


class MessageInterpreter():
    def __init__(self):
        pass

    @staticmethod
    def mapUserChannels(measurementDataModel, messages):


        # check here if the controller has been reset and if so clear all buffers
        newestTimeInSec = None
        for message in messages:
            if message.name == "loopStartTime":
                newestTimeInSec = float(message.value) / 1000000.0


        lastTime = measurementDataModel.timeValues[len(measurementDataModel.timeValues) - 1]

        if measurementDataModel.isEmpty is True or newestTimeInSec < lastTime:
            measurementDataModel.clear(newestTimeInSec)
            measurementDataModel.isEmpty = False


        # if newestTimeInSec < lastTime:
        #
        #     measurementDataModel.clear(newestTimeInSec)

        # append incoming values to buffers
        for i in range(0, len(messages)):
            if messages[i].isUserChannel is True:
                measurementDataModel.channels[i].values.append(messages[i].value)
            elif messages[i].name == "loopStartTime":
                measurementDataModel.timeValues.append(float(messages[i].value) / 1000000.0)

    @staticmethod
    def getLoopCycleDuration(messages):
        for i, message in enumerate(messages):
            if message.name == "lastLoopDuration":
                return message.value
        return None

    @staticmethod
    def getCommandConfirmation(messages):
        cmd = CommandConfirmation()
        for i, message in enumerate(messages):
            if message.name == "parameterNumber":
                cmd.id = message.value
            if message.name == "parameterValue":
                cmd.returnValue = message.value
        return cmd

