
#include <arduino.h>

void receiveMessage();
void readIncomingBytesIntoBuffer();
void appendByteToBuffer(uint8_t inByte);
void shiftGivenPositionToBufferStart(int position);
int seekForFullMessage();
void extractMessage(int messageStartPosition);
void applyExtractedInMessage();

#define OUT_START_BYTE (char)7
#define OUT_STOP_BYTE (char)8

#define IN_MESSAGE_SIZE 8
#define IN_BUFFER_SIZE ((IN_MESSAGE_SIZE+2)*2)

#define IN_START_BYTE (char)7
#define IN_STOP_BYTE (char)8

void microRayInit() {
    setInitialValues();
    Serial.begin(BAUD_RATE);
}


void sendMessage() {
    prepareOutMessage(micros());
    // check, if there is still data not send from the previous loop
    #ifdef SERIAL_TX_BUFFER_SIZE
        int bytesStillInBuffer = SERIAL_TX_BUFFER_SIZE - Serial.availableForWrite();
        if (bytesStillInBuffer > 1) {
            serialTransmissionLag = bytesStillInBuffer;
        }
    #endif
    Serial.write(7);
    Serial.write((byte *)&messageOutBuffer, sizeof(messageOutBuffer));
    Serial.write(8);
}








uint8_t rawMessageInBuffer[IN_BUFFER_SIZE];
uint8_t rawMessageInBufferTemp[IN_BUFFER_SIZE];
int16_t bufferPosition = 0;

void receiveMessage() {
    readIncomingBytesIntoBuffer();
    int foundMessageStartPosition = seekForFullMessage();

    // Serial.print("found message at ");
    // Serial.print(foundMessageStartPosition);
    // Serial.println();

    if(foundMessageStartPosition > -1) {
        extractMessage(foundMessageStartPosition);
        applyExtractedInMessage();
    }
}


void readIncomingBytesIntoBuffer() {
    while (Serial.available()) {
        char inChar = Serial.read();
        appendByteToBuffer(inChar);

        // mR_testChannel = (float)inChar;
        // mR_incChannel = bufferPosition;
    }

    // Serial.print("[");
    // int i = 0;
    // for(i=0; i< IN_BUFFER_SIZE; i++) {
    //     Serial.print(rawMessageInBuffer[i]);
    //     Serial.print(", ");
    // }
    // Serial.print("] ");
    // Serial.println(bufferPosition);
}

// void readIncomingBytesIntoBuffer() {
//     while (Serial.available()) {
//         appendByteToBuffer(Serial.read());
//     }
// }

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
    memcpy(&messageInBuffer.value, &rawMessageInBuffer[messageStartPosition + 1 + 4], 4);
    shiftGivenPositionToBufferStart(messageStartPosition + IN_MESSAGE_SIZE + 2);

    // Serial.print("P_num ");
    // Serial.print(messageInBuffer.parameterNumber);
    // Serial.print(" P_val ");
    // Serial.println(messageInBuffer.value);
}

void applyExtractedInMessage() {
    if (messageInBuffer.parameterNumber >= 0) {
        parameters[messageInBuffer.parameterNumber] = messageInBuffer.value;
    }
    else {
        specialCommands[(messageInBuffer.parameterNumber + 1) * -1] = messageInBuffer.value;
    }

    // Serial.print("P_val_saved ");
    // Serial.println(parameters[messageInBuffer.parameterNumber]);
}
