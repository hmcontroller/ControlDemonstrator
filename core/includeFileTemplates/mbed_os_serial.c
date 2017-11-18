
#include <mbed.h>

void serialSendCompleteOne(int events);
void serialSendCompleteTwo(int events);
void serialSendCompleteThree(int events);
void serialReadComplete(int events);

void receiveMessage();
void readIncomingBytesIntoBuffer();
void appendByteToBuffer(uint8_t inByte);
void shiftGivenPositionToBufferStart(int position);
int seekForFullMessage();
void extractMessage(int messageStartPosition);


Serial mRserial(USBTX, USBRX, BAUD_RATE); // tx, rx

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


event_callback_t serialEventWriteCompleteOne = serialSendCompleteOne;
event_callback_t serialEventWriteCompleteTwo = serialSendCompleteTwo;
event_callback_t serialEventWriteCompleteThree = serialSendCompleteThree;
event_callback_t serialEventReceiveComplete = serialReadComplete;


int debugCounterSend = 0;
void serialSendCompleteOne(int events) {
    mRserial.write((uint8_t *)&messageOutBuffer, sizeof(messageOutBuffer), serialEventWriteCompleteTwo, SERIAL_EVENT_TX_COMPLETE);
}

void serialSendCompleteTwo(int events) {
    mRserial.write((uint8_t *)&endOut, 1, serialEventWriteCompleteThree, SERIAL_EVENT_TX_COMPLETE);
}

void serialSendCompleteThree(int events) {
    timeOfLastCompletedMessage = timeOfLastSend;
}


uint8_t singleInBuffer = 0;
void serialReadComplete(int events) {
    appendByteToBuffer(singleInBuffer);

    // retrigger async receive of serial data
    mRserial.read(&singleInBuffer, 1, serialEventReceiveComplete);
}

void microRayInit() {
    dutyCycleTimer.start();
    //serialEventWriteComplete.attach(serialSendComplete);
    //serialEventReceiveComplete.attach(serialReadComplete);

    // start async receive of serial data
    mRserial.read(&singleInBuffer, 1, serialEventReceiveComplete);

    //mRserial.set_dma_usage_tx(1);
    //mRserial.set_dma_usage_rx(1);
}

int serialTransmissionLagCounter = 0;
void sendMessage() {


    prepareOutMessage((unsigned long)dutyCycleTimer.read_high_resolution_us());

    if(timeOfLastCompletedMessage == timeOfLastSend) {
        timeOfLastSend = (unsigned long)messageOutBuffer.loopStartTime;
        mRserial.write((uint8_t *)&startOut, 1, serialEventWriteCompleteOne, SERIAL_EVENT_TX_COMPLETE);
        //mRserial.write((uint8_t *)&messageOutBuffer, sizeof(messageOutBuffer), 0, 0);
        //mRserial.write((uint8_t *)&endOut, 1, serialEventWriteComplete, SERIAL_EVENT_TX_COMPLETE);
        //mRserial.putc(OUT_STOP_BYTE);
    }
    else {
        serialTransmissionLagCounter++;
        serialTransmissionLag = (float)serialTransmissionLagCounter;
        timeOfLastSend = (unsigned long)messageOutBuffer.loopStartTime;
    }
}

uint8_t rawMessageInBuffer[IN_BUFFER_SIZE];
uint8_t rawMessageInBufferTemp[IN_BUFFER_SIZE];
int16_t bufferPosition = 0;

void receiveMessage() {
    //readIncomingBytesIntoBuffer();
    int foundMessageStartPosition = seekForFullMessage();

    if(foundMessageStartPosition > -1) {
        extractMessage(foundMessageStartPosition);
        prepareInMessage();
    }
}

void readIncomingBytesIntoBuffer() {
    appendByteToBuffer(singleInBuffer);
}

void appendByteToBuffer(uint8_t inByte) {
    // prevent buffer from overfilling
    // shift whole buffer one to the left to free last position
    if(bufferPosition >= IN_BUFFER_SIZE) {
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


