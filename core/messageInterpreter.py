# -*- encoding: utf-8 -*-

from core.command import CommandConfirmation


class MessageInterpreter():
    def __init__(self):
        pass

    @staticmethod
    def mapUserChannels(measurementDataModel, messages):

        for message in messages:

            # check here if the controller has been reset and if so clear all buffers
            newestTimeInSec = None
            for messagePart in message:
                if messagePart.name == "loopStartTime":
                    newestTimeInSec = float(messagePart.value) / 1000000.0

            lastTime = measurementDataModel.timeValues[len(measurementDataModel.timeValues) - 1]

            if measurementDataModel.isEmpty or newestTimeInSec < lastTime:
                measurementDataModel.clear(newestTimeInSec)
                measurementDataModel.isEmpty = False

            # append incoming values to buffers
            for i in range(0, len(message)):
                if message[i].isUserChannel is True:
                    measurementDataModel.channels[i].append(message[i].value)
                elif message[i].name == "loopStartTime":
                    measurementDataModel.timeValues.append(float(message[i].value) / 1000000.0)

    @staticmethod
    def getLoopCycleDuration(messages):
        for i, message in enumerate(messages):
            if message.name == "lastLoopDuration":
                return message.value
        return None

    @staticmethod
    def getCommandConfirmation(message):
        cmd = CommandConfirmation()
        for i, messagePart in enumerate(message):
            if messagePart.name == "parameterNumber":
                cmd.id = messagePart.value
            if messagePart.name == "parameterValue":
                cmd.returnValue = messagePart.value
        return cmd

