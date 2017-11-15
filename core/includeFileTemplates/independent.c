#include "microRay.h"

void prepareOutMessage();
void prepareInMessage();
void sendMessage();
void receiveMessage();

unsigned long lastTime = 0;

// storage for unrequested channels
float unrequestedChannels[CHANNELS_UNREQUESTED_COUNT];

int parameterSendCounter = 0;
int receivedBytesCount = 0;
int sendBytesCount = 0;

MessageOut messageOutBuffer;
MessageIn messageInBuffer;

void prepareOutMessage(unsigned long loopStartTime)
{
    // map rotating parameters
    // on each cycle, only one of the "controlled parameters" is send to the pc

    messageOutBuffer.loopStartTime = loopStartTime;
    messageOutBuffer.parameterNumber = parameterSendCounter;

    if (parameterSendCounter < 0) {
        messageOutBuffer.parameterValueFloat = specialCommands[(parameterSendCounter + 1) * -1];
    }
    else {
        switch (parameters[parameterSendCounter].dataType) {
            case INT_TYPE:
                messageOutBuffer.parameterValueInt = parameters[parameterSendCounter].valueInt;
                break;
            case FLOAT_TYPE:
                messageOutBuffer.parameterValueFloat = parameters[parameterSendCounter].valueFloat;
                break;
            default:
                break;
        }
    }

    // increment the counter for sending the "slow parameters"
    parameterSendCounter += 1;
    if (parameterSendCounter >= PARAMETER_COUNT)
    {
        parameterSendCounter = SPECIAL_COMMANDS_COUNT * -1;
    }
}

void prepareInMessage() {
    if (messageInBuffer.parameterNumber >= 0) {
        switch (parameters[messageInBuffer.parameterNumber].dataType) {
            case INT_TYPE:
                parameters[messageInBuffer.parameterNumber].valueInt = messageInBuffer.parameterValueInt;
                break;
            case FLOAT_TYPE:
                parameters[messageInBuffer.parameterNumber].valueFloat = messageInBuffer.parameterValueFloat;
                break;
            default:
                break;
        }
    }
    else {
        specialCommands[(messageInBuffer.parameterNumber + 1) * -1] = messageInBuffer.parameterValueFloat;
    }
}

void microRayCommunicate()
{
    sendMessage();
    receiveMessage();
}
