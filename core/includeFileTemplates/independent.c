#include "microRay.h"

void prepareOutMessage();
void prepareInMessage();
void sendMessage();
void receiveMessage();
void record();
void recordMessage();
void transmitRecordings();

unsigned long lastTime = 0;
volatile bool lastMessageSendComplete = true;

int sendMode = LIVE_MODE;
int recordingCounter = 0;
int recordingSendCounter = 0;


// storage for unrequested channels
float unrequestedChannels[CHANNELS_UNREQUESTED_COUNT];

#if !defined(SUPPRESS_PARAM_CONFIRMATION)
int parameterSendCounter = 0;
#endif

int receivedBytesCount = 0;
int sendBytesCount = 0;

MessageOut messageOutBuffer;
MessageIn messageInBuffer;

MessageOut recordBuffer[RECORD_BUFFER_LENGTH];

void prepareOutMessage(unsigned long loopStartTime)
{
    // map rotating parameters
    // on each cycle, only one of the "controlled parameters" is send to the pc

    messageOutBuffer.loopStartTime = loopStartTime;

    #if !defined(SUPPRESS_PARAM_CONFIRMATION)
    messageOutBuffer.parameterNumber = parameterSendCounter;
    if (parameterSendCounter < 0) {
        messageOutBuffer.parameterValueInt = specialCommands[(parameterSendCounter + 1) * -1];
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
#endif
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
        // toggle recording mode
        if (messageInBuffer.parameterNumber == -3) {
            if (messageInBuffer.parameterValueInt != specialCommands[(messageInBuffer.parameterNumber + 1) * -1]) {
                if (messageInBuffer.parameterValueInt == 1) {
                    sendMode = RECORD_MODE;
                }
                else if (messageInBuffer.parameterValueInt == 0) {
                    sendMode = RECORD_TRANSMISSION_MODE;
                }
            }
        }
        specialCommands[(messageInBuffer.parameterNumber + 1) * -1] = messageInBuffer.parameterValueInt;
    }
}

void microRayCommunicate()
{
    receiveMessage();

#ifndef mrDEBUG
    switch (sendMode) {
        case RECORD_MODE:
            record();
            break;
        case RECORD_TRANSMISSION_MODE:
            transmitRecordings();
            break;
        case LIVE_MODE:
            sendMessage();
            break;
        case WAIT_MODE:
            break;
        default:
            break;
    }
#endif
}

void record() {
    recordMessage();
    recordBuffer[recordingCounter] = messageOutBuffer;
    recordingCounter += 1;
    if (recordingCounter > RECORD_BUFFER_LENGTH) {
        recordingCounter = 0;
    }
}

void transmitRecordings() {
    // blocks until finished
    for (recordingSendCounter = 0; recordingSendCounter < RECORD_BUFFER_LENGTH; recordingSendCounter++) {
        int nextMessageIndex = recordingSendCounter + recordingCounter;
        if (nextMessageIndex > RECORD_BUFFER_LENGTH){
            nextMessageIndex -= RECORD_BUFFER_LENGTH;
        }
        messageOutBuffer = recordBuffer[nextMessageIndex];
        sendMessage();
        receiveMessage();
        // while (lastMessageSendComplete == false) {
            // wait
        // }
    }
    recordingCounter = 0;
    sendMode = WAIT_MODE;
}
