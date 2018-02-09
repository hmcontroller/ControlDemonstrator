
#include <mbed.h>

void serialSendCompleteOne(int events);
void serialSendCompleteTwo(int events);
void serialSendCompleteThree(int events);

void receiveMessage();
void readIncomingBytesIntoBuffer();
void appendByteToBuffer(uint8_t inByte);
void shiftGivenPositionToBufferStart(int position);
int seekForFullMessage();
void extractMessage(int messageStartPosition);


Serial mrSerial(USBTX, USBRX, BAUD_RATE); // tx, rx
Ticker serialReceiver;

Timer dutyCycleTimer;
Timer debugTimer;
unsigned long timeOfLastSend = 0;
unsigned long timeOfLastCompletedMessage = 0;

#define OUT_START_BYTE (char)7
#define OUT_STOP_BYTE (char)8

#define IN_MESSAGE_SIZE 8
#define IN_BUFFER_SIZE ((IN_MESSAGE_SIZE+2)*2)

#define IN_START_BYTE (char)7
#define IN_STOP_BYTE (char)8

unsigned char startOut = 7;
unsigned char endOut = 8;


void microRayInit() {
    messageOutBuffer.statusFlags = 0;
    dutyCycleTimer.start();
    serialReceiver.attach(&readIncomingBytesIntoBuffer, 0.00001f);
    // mrSerial.attach(&readIncomingBytesIntoBuffer);
}


event_callback_t serialEventWriteCompleteOne = serialSendCompleteOne;
event_callback_t serialEventWriteCompleteTwo = serialSendCompleteTwo;
event_callback_t serialEventWriteCompleteThree = serialSendCompleteThree;


int debugCounterSend = 0;
void serialSendCompleteOne(int events) {
    mrSerial.write((uint8_t *)&messageOutBuffer, sizeof(messageOutBuffer), serialEventWriteCompleteTwo, SERIAL_EVENT_TX_COMPLETE);
}

void serialSendCompleteTwo(int events) {
    mrSerial.write((uint8_t *)&endOut, 1, serialEventWriteCompleteThree, SERIAL_EVENT_TX_COMPLETE);
}

void serialSendCompleteThree(int events) {
    // timeOfLastCompletedMessage = timeOfLastSend;
    lastMessageSendComplete = true;
}



int serialTransmissionLagCounter = 0;
void sendMessage() {

    // decide wether to send in blocking mode or not
    if(lastMessageSendComplete == false) {
        if (sendMode == RECORD_TRANSMISSION_MODE) {
            while(lastMessageSendComplete == false) {
                // wait
            }
        }
        // flag lastMessageSendComplete will never be set to true, don't know why
        // if ((sendMode == LIVE_MODE) && (MESSAGE_SKIP_MODE == 0)) {
        //     while(lastMessageSendComplete == false) {
        //         // wait
        //     }
        // }
    }


    if(lastMessageSendComplete == true) {
        if (sendMode == LIVE_MODE) {
            prepareOutMessage((unsigned long)dutyCycleTimer.read_high_resolution_us());
        }
        lastMessageSendComplete = false;
        mrSerial.write((uint8_t *)&startOut, 1, serialEventWriteCompleteOne, SERIAL_EVENT_TX_COMPLETE);
    }
    else {
        messageOutBuffer.statusFlags |= (1 << STATUS_SKIPPED);
        serialTransmissionLagCounter++;
        serialTransmissionLag = (float)serialTransmissionLagCounter;
    }
}

uint8_t rawMessageInBuffer[IN_BUFFER_SIZE];
uint8_t rawMessageInBufferTemp[IN_BUFFER_SIZE];
int bufferPosition = 0;

void receiveMessage() {
    int foundMessageStartPosition = seekForFullMessage();
    if(foundMessageStartPosition > -1) {
        extractMessage(foundMessageStartPosition);
        prepareInMessage();
    }
}


void recordMessage() {
    prepareOutMessage((unsigned long)dutyCycleTimer.read_high_resolution_us());
}

void readIncomingBytesIntoBuffer() {
    int i = 0;
    for (i = 0; i < IN_MESSAGE_SIZE; i++) {
        if (mrSerial.readable()) {
            appendByteToBuffer(mrSerial.getc());
        }
        else {
            break;
        }
    }
}

void appendByteToBuffer(uint8_t inByte) {

    // prevent buffer from overfilling
    if(bufferPosition >= IN_BUFFER_SIZE) {
        // shift whole buffer one to the left to free last position
        shiftGivenPositionToBufferStart(1);
    }

    rawMessageInBuffer[bufferPosition] = inByte;
    bufferPosition += 1;
}

void shiftGivenPositionToBufferStart(int position) {
    // copy and shift
    int i;
    for(i = position; i < bufferPosition; i++) {
        rawMessageInBufferTemp[i - position] = rawMessageInBuffer[i];
    }

    // actualize bufferPosition
    bufferPosition = bufferPosition - position;

    // copy back
    for(i = 0; i < bufferPosition; i++) {
        rawMessageInBuffer[i] = rawMessageInBufferTemp[i];
    }

}

int seekForFullMessage() {
    int i;
    for (i = 0; i < bufferPosition - IN_MESSAGE_SIZE; i++) {
        if (rawMessageInBuffer[i] == IN_START_BYTE) {
            int expectedStopBytePosition = i + IN_MESSAGE_SIZE + 1;
            if (rawMessageInBuffer[expectedStopBytePosition] == IN_STOP_BYTE) {
                return i;
            }
        }
    }
    return -1;
}

void extractMessage(int messageStartPosition) {
    memcpy(&messageInBuffer.parameterNumber, &rawMessageInBuffer[messageStartPosition + 1], 4);
    memcpy(&messageInBuffer.parameterValueInt, &rawMessageInBuffer[messageStartPosition + 1 + 4], 4);
    shiftGivenPositionToBufferStart(messageStartPosition + IN_MESSAGE_SIZE + 2);
}
