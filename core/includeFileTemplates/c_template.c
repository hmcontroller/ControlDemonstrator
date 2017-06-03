


#ifdef ARDUINO_UDP

#include <arduino.h>
#include <SPI.h>
#include <Ethernet2.h>
#include <EthernetUdp2.h>

byte macAddress[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ownIp(192, 168, 0, 15);
IPAddress remoteIp(192, 168, 0, 133);
unsigned int port = 10000;
EthernetUDP Udp;

#elif defined(ARDUINO_SERIAL)
#include <arduino.h>
#define BAUD_RATE 115200

void dumpOldMessages();
void copyOldMessageToIncomingBuffer();
void readIncomingBytesIntoBuffer();
void processMessage(int);
int findMessageAndProcess();
void storeForNextLoop(int);


#elif defined(MBED_2_USBHID)

#elif defined(MBED_OS_UDP)

#include "EthernetInterface.h"
#include "SocketAddress.h"

#define SERVER_IP       "192.168.0.133"
#define OWN_IP          "192.168.0.15"
#define PORT            10000
#define NET_MASK        "255.255.0.0"
#define GATEWAY         "192.168.0.1"

EthernetInterface eth;
UDPSocket socket;
SocketAddress udp_server_address(SERVER_IP, PORT);
SocketAddress dump_address(SERVER_IP, PORT);

Timer dutyCycleTimer;
Timer debugTimer;
Serial pcSerialPort(USBTX, USBRX);

DigitalOut greenLed(LED1);
DigitalOut blueLed(LED2);
DigitalOut redLed(LED3);

#elif defined(MBED_OS_SERIAL)
#endif

void prepareOutMessage();
void sendMessage();
void receiveMessage();

unsigned long lastTime = 0;

// storage for unrequested channels
float unrequestedChannels[CHANNELS_UNREQUESTED_COUNT];

// storage for parameters, that could be set from the pc
float parameters[PARAMETER_COUNT] = {0.0f};
float specialCommands[SPECIAL_COMMANDS_COUNT] = {0.0f};

int parameterSendCounter = 0;
int receivedBytesCount = 0;
int sendBytesCount = 0;

MessageOut messageOutBuffer;
MessageIn messageInBuffer;


#ifdef ARDUINO_UDP
void microRayInit()
{
    setInitialValues();
    // Bring up the network interface
    Ethernet.begin(macAddress, ownIp);
    Udp.begin(port);
}
#elif defined(ARDUINO_SERIAL)
void microRayInit() {
    setInitialValues();
    Serial.begin(BAUD_RATE);
}

#elif defined(MBED_2_USBHID)
void microRayInit() {
    setInitialValues();
}

#elif defined(MBED_OS_UDP)
void microRayInit() {
    setInitialValues();

    // Bring up the network interface

    // laut Dokumentation Initialisierung mit static IP eigentlich möglich bei mbed OS, geht aber nicht
    // es gibt wohl einen Branch von mbed mit einem Patch
    //// eth.init(&ownIP, &mask, &Gateway);

    // Ethernetconnection with DHCP
    eth.set_network(OWN_IP, NET_MASK, GATEWAY);
    eth.connect();
    const char *ip = eth.get_ip_address();
    const char *mac = eth.get_mac_address();

    pcSerialPort.printf("IP address is: %s\n", ip ? ip : "No IP");
    pcSerialPort.printf("MAC address is: %s\n", mac ? mac : "No MAC");

    socket.open(&eth);
    socket.bind(PORT);
    socket.set_blocking(false);

    // the timer is used for duty cycle duration measurement
    dutyCycleTimer.reset();
    dutyCycleTimer.start();
}

#else
void microRayInit() {
    setInitialValues();
}
#endif

void prepareOutMessage()
{
#ifdef ARDUINO_SERIAL
    messageOutBuffer.loopStartTime = micros();

#elif defined(ARDUINO_UDP)
    messageOutBuffer.loopStartTime = micros();

#elif defined(MBED_OS_UDP)
    messageOutBuffer.loopStartTime = dutyCycleTimer.read_us();

#else
#endif

    // TODO - check what happens on timer overflow (after approx. 30min)




    // map rotating parameters
    // on each cycle, only one of the "controlled parameters" is send to the pc

    if (parameterSendCounter < 0) {
        messageOutBuffer.parameterNumber = parameterSendCounter;
        //messageOutBuffer.parameterValue = parameters[requestedControlledParameters[parameterSendCounter]];
        messageOutBuffer.parameterValue = specialCommands[(parameterSendCounter + 1) * -1];
    }
    else {
        messageOutBuffer.parameterNumber = parameterSendCounter;
        //messageOutBuffer.parameterValue = parameters[requestedControlledParameters[parameterSendCounter]];
        messageOutBuffer.parameterValue = parameters[parameterSendCounter];
    }

    // increment the counter for sending the "slow parameters"
    parameterSendCounter += 1;
    if (parameterSendCounter >= PARAMETER_COUNT)
    {
        parameterSendCounter = SPECIAL_COMMANDS_COUNT * -1;
    }
}


void microRayCommunicate()
{
    sendMessage();
    receiveMessage();
}

#ifdef ARDUINO_UDP
void sendMessage()
{
    prepareOutMessage();

    lastTime = micros();
    Udp.beginPacket(remoteIp, port);
    Udp.write((char *)&messageOutBuffer, sizeof(messageOutBuffer));
    Udp.endPacket();
    // sendTimer = (float)(micros() - lastTime);
}

#elif defined(ARDUINO_SERIAL)
void sendMessage() {
    prepareOutMessage();
    lastTime = micros();

    // Serial.write(messageOutBuffer.loopStartTime);
    // Serial.write(messageOutBuffer.lastLoopDuration);
    // Serial.write(messageOutBuffer.parameterNumber);
    // Serial.write(messageOutBuffer.parameterValue);
    //
    // int i = 0;
    // for (i; i < CHANNELS_REQUESTED_COUNT; i++) {
    //     Serial.write(messageOutBuffer.channels[i]);
    // }

    // check, if there is still data not send from the previous loop

    int bytesStillInBuffer = SERIAL_TX_BUFFER_SIZE - Serial.availableForWrite();
    if (bytesStillInBuffer > 1) {
        serialTransmissionLag = SERIAL_TX_BUFFER_SIZE - Serial.availableForWrite();
    }

    Serial.write(7);
    Serial.write((byte *)&messageOutBuffer, sizeof(messageOutBuffer));
    Serial.write(8);

    // sendTimer = (float)(micros() - lastTime);
}

#elif defined(MBED_2_USBHID)
void sendMessage() {
}

#elif defined(MBED_OS_UDP)
void sendMessage() {
    prepareOutMessage();

    // send data to the pc via Ethernet with mbed os
    debugTimer.reset();
    debugTimer.start();
    sendBytesCount = socket.sendto(udp_server_address, (char *)&messageOutBuffer, sizeof(messageOutBuffer));
    SEND_TIMER = (float)debugTimer.read_us();

    #ifdef DEBUG
    pcSerialPort.printf("SEND: %d %d %f\n", sendBytesCount, messageOutBuffer.parameterNumber, messageOutBuffer.parameterValue);
    #endif
}

#else
void sendMessage() {
}
#endif

#ifdef ARDUINO_UDP
void receiveMessage() {
    // receive a command
    lastTime = micros();
    int availableBytes = Udp.parsePacket();
    if (availableBytes > 0) {
        Udp.read((char *)&messageInBuffer, sizeof(messageInBuffer));
        if (messageInBuffer.parameterNumber >= 0) {
            parameters[messageInBuffer.parameterNumber] = messageInBuffer.value;
        }
        else {
            specialCommands[(messageInBuffer.parameterNumber + 1) * -1] = messageInBuffer.value;
    }
    }
    else {
    }

    // receiveTimer = (float)(micros() - lastTime);
}
#elif defined(ARDUINO_SERIAL)

#define START_BYTE (char)7
#define STOP_BYTE (char)57
#define IN_MESSAGE_SIZE 8
#define BUFFER_SIZE ((IN_MESSAGE_SIZE+2)*2)

int16_t availableBytes = 0;

uint8_t remainderBuffer[BUFFER_SIZE];
int16_t bytesInRemainderBuffer = 0;

uint8_t dataToProcess[BUFFER_SIZE];
int16_t bytesInDataToProcess = 0;
int16_t dataToProcessPosition = 0;
int16_t searchPosition = 0;
int16_t lastPositionProcessed = -1;


void receiveMessage() {
    lastTime = micros();
    //dumpOldMessages();
    copyOldMessageToIncomingBuffer();
    readIncomingBytesIntoBuffer();
    lastPositionProcessed = findMessageAndProcess();
    storeForNextLoop(lastPositionProcessed);
    // receiveTimer = (float)(micros() - lastTime);
}


void dumpOldMessages() {
    while(Serial.available() > BUFFER_SIZE) {
        Serial.read();
    }
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
    if (Serial.available() < (IN_MESSAGE_SIZE + 2)) {
        return;
    }
    while ((Serial.available() > 0) && (dataToProcessPosition < BUFFER_SIZE)) {
        dataToProcess[dataToProcessPosition] = Serial.read();
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

#elif defined(MBED_2_USBHID)
void receiveMessage() {
}

#elif defined(MBED_OS_UDP)
void receiveMessage() {
    // receive a command
    debugTimer.reset();
    debugTimer.start();
    RECEIVED_BYTES_COUNT = (float)socket.recvfrom(&dump_address, (char *)&messageInBuffer, sizeof(messageInBuffer));
    RECEIVE_TIMER = (float)debugTimer.read_us();
    // if a command has been received
    if (RECEIVED_BYTES_COUNT > 0.5f)
    {

        if (messageInBuffer.parameterNumber >= 0) {
            parameters[messageInBuffer.parameterNumber] = messageInBuffer.value;
        }
        else {
            specialCommands[(messageInBuffer.parameterNumber + 1) * -1] = messageInBuffer.value;
        }
        // for debugging
        LAST_COMMAND_ID = messageInBuffer.parameterNumber;
        LAST_COMMAND_VALUE = messageInBuffer.value;
        // blue led blinkiblinki on successfull receive
        blueLed = 1;
    }
    else
    {
        // red led on until next loop cycle
        redLed = 1;
    }

    #ifdef DEBUG
    pcSerialPort.printf("RECV: %f %d %f\n", RECEIVED_BYTES_COUNT, messageInBuffer.parameterNumber, messageInBuffer.value);
    #endif
}

#else
void receiveMessage() {
}
#endif
