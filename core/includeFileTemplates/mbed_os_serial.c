
#include <mbed.h>

void dumpOldMessages();
void copyOldMessageToIncomingBuffer();
void readIncomingBytesIntoBuffer();
void processMessage(int);
int findMessageAndProcess();
void storeForNextLoop(int);

Serial mRserial(USBTX, USBRX, BAUD_RATE); // tx, rx
Serial mRserialExtern(PB_10, PB_11, BAUD_RATE); // tx, rx

Timer dutyCycleTimer;
Timer debugTimer;
unsigned long timeOfLastSend = 0;
unsigned long timeOfLastCompletedMessage = 0;

DigitalOut redLed(LED3);
DigitalOut greenLed(LED1);

#define START_BYTE (char)7
#define STOP_BYTE (char)8
#define IN_MESSAGE_SIZE 8
#define BUFFER_SIZE ((IN_MESSAGE_SIZE+2)*2)

event_callback_t serialEventWriteComplete;
int debugCounterSend = 0;
void serialSendComplete(int events) {
    mRserial.putc(STOP_BYTE);
    timeOfLastCompletedMessage = timeOfLastSend;
    // mRserialExtern.putc(STOP_BYTE);
    // debugCounterSend += 1;
    // if (debugCounterSend > 10) {
    //     debugCounterSend = 0;
    //     redLed = !redLed;
    // }
}


void microRayInit() {
    setInitialValues();
    dutyCycleTimer.start();
//    messageOutBuffer.startByte = 7;
//    messageOutBuffer.stopByte = 8;
    serialEventWriteComplete.attach(serialSendComplete);

    //mRserial.set_dma_usage_tx(1);
    //mRserial.set_dma_usage_rx(1);
}

int serialTransmissionLagCounter = 0;
void sendMessage() {

    prepareOutMessage((unsigned long)dutyCycleTimer.read_high_resolution_us());

    if(timeOfLastCompletedMessage == timeOfLastSend) {
        timeOfLastSend = (unsigned long)messageOutBuffer.loopStartTime;
        mRserial.putc(START_BYTE);
        mRserial.write((uint8_t *)&messageOutBuffer, sizeof(messageOutBuffer), serialEventWriteComplete, SERIAL_EVENT_TX_COMPLETE);
        //mRserial.putc(STOP_BYTE);
    }
    else {
        serialTransmissionLagCounter++;
        serialTransmissionLag = (float)serialTransmissionLagCounter;
        timeOfLastSend = (unsigned long)messageOutBuffer.loopStartTime;
    }

    // mRserialExtern.putc(START_BYTE);
    // mRserialExtern.write((uint8_t *)&messageOutBuffer, sizeof(messageOutBuffer), serialEventWriteComplete, SERIAL_EVENT_TX_COMPLETE);
    //mRserial.putc(STOP_BYTE);



//     // autsch (geht aber):
//     mRserial.putc(START_BYTE);
//     uint8_t sendCounter = 0;
//     uint8_t * pointerToOutMessage  = (uint8_t *)&messageOutBuffer;
//     for(sendCounter=0; sendCounter < sizeof(messageOutBuffer); sendCounter++) {
//         mRserial.putc(*pointerToOutMessage);
//         pointerToOutMessage++;
//     }
//     mRserial.putc(STOP_BYTE);
}

int16_t availableBytes = 0;

uint8_t remainderBuffer[BUFFER_SIZE];
int16_t bytesInRemainderBuffer = 0;

uint8_t dataToProcess[BUFFER_SIZE];
int16_t bytesInDataToProcess = 0;
int16_t dataToProcessPosition = 0;
int16_t searchPosition = 0;
int16_t lastPositionProcessed = -1;


void receiveMessage() {
    lastTime = debugTimer.read_us();
    //dumpOldMessages();
    copyOldMessageToIncomingBuffer();
    readIncomingBytesIntoBuffer();
    lastPositionProcessed = findMessageAndProcess();
    storeForNextLoop(lastPositionProcessed);
    // receiveTimer = (float)(micros() - lastTime);
}


void dumpOldMessages() {
    // funktioniert bei mbed so iwi nicht, weil man die Länge des Buffers nicht abfragen kann
    //while(mRserial.readable() > BUFFER_SIZE) {
    //    mRserial.read();
    //}
}

void copyOldMessageToIncomingBuffer() {
    for (dataToProcessPosition = 0; dataToProcessPosition < bytesInRemainderBuffer; dataToProcessPosition++) {
        dataToProcess[dataToProcessPosition] = remainderBuffer[dataToProcessPosition];
        bytesInDataToProcess++;
    }
    bytesInRemainderBuffer = 0;
}

void readIncomingBytesIntoBuffer() {
//    dataToProcessPosition = bytesInDataToProcess;
//    if (Serial.available() < (IN_MESSAGE_SIZE + 2)) {
//        return;
//    }

    while (mRserial.readable() && (dataToProcessPosition < BUFFER_SIZE)) {
        dataToProcess[dataToProcessPosition] = mRserial.getc();
        dataToProcessPosition++;
        bytesInDataToProcess++;
    }
}

int findMessageAndProcess() {
    for (searchPosition = 0; searchPosition < bytesInDataToProcess; searchPosition++) {
        if (dataToProcess[searchPosition] == START_BYTE) {
            int expectedStopBytePosition = searchPosition + IN_MESSAGE_SIZE + 1;
            if (expectedStopBytePosition < BUFFER_SIZE) {
                if (dataToProcess[expectedStopBytePosition] == STOP_BYTE) {
                    processMessage(searchPosition + 1);
                    return expectedStopBytePosition;
                }
            }
            else {
                // do something meaningful
            }
        }
    }
    return -1;
}

void processMessage(int messageStartPosition) {
    memcpy(&messageInBuffer.parameterNumber, &dataToProcess[messageStartPosition], 4);
    memcpy(&messageInBuffer.value, &dataToProcess[messageStartPosition + 4], 4);
    if (messageInBuffer.parameterNumber >= 0) {
        parameters[messageInBuffer.parameterNumber] = messageInBuffer.value;
    }
    else {
        specialCommands[(messageInBuffer.parameterNumber + 1) * -1] = messageInBuffer.value;
    }

}



void storeForNextLoop(int lastPositionProcessed) {
    int positionResidueBuffer = 0;
    int positionInBuffer = lastPositionProcessed + 1;
    while (positionInBuffer < bytesInDataToProcess) {
        remainderBuffer[positionResidueBuffer] = dataToProcess[positionInBuffer];
        bytesInRemainderBuffer++;
        positionResidueBuffer++;
        positionInBuffer++;
    }
    bytesInDataToProcess = 0;
}
