#include "microRay.h"

void prepareOutMessage();
void prepareInMessage();
void sendMessage();
void receiveMessage();
void recordMessage();

unsigned long lastTime = 0;
bool lastMessageSendComplete = false;

bool record = false;
bool transmitRecordBuffer = false;
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
        if (messageInBuffer.parameterNumber == -3) {
            if (messageInBuffer.parameterValueFloat != specialCommands[(messageInBuffer.parameterNumber + 1) * -1]) {
                if (messageInBuffer.parameterValueFloat > 0.5) {
                    record = true;
                }
                else {
                    record = false;
                    transmitRecordBuffer = true;
                }
            }
        }
        specialCommands[(messageInBuffer.parameterNumber + 1) * -1] = messageInBuffer.parameterValueFloat;
    }
}

void microRayCommunicate()
{
    receiveMessage();

#ifndef mrDEBUG

    if (record) {
        recordMessage();
        recordBuffer[recordingCounter] = messageOutBuffer;
        recordingCounter += 1;
        if (recordingCounter > RECORD_BUFFER_LENGTH) {
            recordingCounter = 0;
        }
    }
    else if (transmitRecordBuffer) {
        // blocks until finished
        transmitRecordBuffer = false;

        for (recordingSendCounter = 0; recordingSendCounter < RECORD_BUFFER_LENGTH; recordingSendCounter++) {
            int nextMessageIndex = recordingSendCounter + recordingCounter;
            if (nextMessageIndex > RECORD_BUFFER_LENGTH){
                nextMessageIndex -= RECORD_BUFFER_LENGTH;
            }
            messageOutBuffer = recordBuffer[nextMessageIndex];
            sendMessage();
            while (!lastMessageSendComplete) {
                // wait
            }
        }
        recordingCounter = 0;
    }
    else {
        sendMessage();
    }

#endif
}
