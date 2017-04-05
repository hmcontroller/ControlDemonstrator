#include "controlDemonstrator.h"

#ifdef ARDUINO_UDP

#include <SPI.h>
#include <Ethernet2.h>
#include <EthernetUdp2.h>

byte macAddress[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ownIp(192, 168, 0, 15);
IPAddress remoteIp(192, 168, 0, 133);
unsigned int port = 10000;
EthernetUDP Udp;

#elif defined(ARDUINO_SERIAL)

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

int parameterSendCounter = 0;
int receivedBytesCount = 0;
int sendBytesCount = 0;

MessageOut messageOutBuffer;
MessageIn messageInBuffer;


#ifdef ARDUINO_UDP
void initControlDemonstrator()
{
    // Bring up the network interface
    Ethernet.begin(macAddress, ownIp);
    Udp.begin(port);
}
#elif defined(ARDUINO_SERIAL)
void initControlDemonstrator() {
}

#elif defined(MBED_2_USBHID)
void initControlDemonstrator() {
}

#elif defined(MBED_OS_UDP)
void initControlDemonstrator() {

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
void initControlDemonstrator() {
}
#endif

void prepareOutMessage()
{
    // now overwrite messageOutBuffer.loopStartTime with the actual loop start time

#ifdef ARDUINO_UDP
    messageOutBuffer.loopStartTime = micros();
#elif defined(MBED_OS_UDP)
    messageOutBuffer.loopStartTime = dutyCycleTimer.read_us();
#else
#endif

    // TODO - check what happens on timer overflow (after approx. 30min)




    // map rotating parameters
    // on each cycle, only one of the "controlled parameters" is send to the pc
    messageOutBuffer.parameterNumber = parameterSendCounter;
    //messageOutBuffer.parameterValue = parameters[requestedControlledParameters[parameterSendCounter]];
    messageOutBuffer.parameterValue = parameters[parameterSendCounter];

    // increment the counter for sending the "slow parameters"
    parameterSendCounter += 1;
    if (parameterSendCounter >= PARAMETER_COUNT)
    {
        parameterSendCounter = 0;
    }
}


void communicate()
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
    sendTimer = (float)(micros() - lastTime);
}
#elif defined(ARDUINO_SERIAL)
void sendMessage() {
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
        parameters[messageInBuffer.parameterNumber] = messageInBuffer.value;
    }
    else {
    }

    receiveTimer = (float)(micros() - lastTime);
}
#elif defined(ARDUINO_SERIAL)
void receiveMessage() {
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
        parameters[messageInBuffer.parameterNumber] = messageInBuffer.value;

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
