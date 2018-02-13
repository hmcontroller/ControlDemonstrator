
// #include <mbed.h>
#include <EthernetInterface.h>
#include <SocketAddress.h>

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
Serial mRserial(USBTX, USBRX);

// DigitalOut greenLed(LED1);
// DigitalOut blueLed(LED2);
// DigitalOut redLed(LED3);



void microRayInit() {
    messageOutBuffer.statusFlags = 0;
    // Bring up the network interface

    // laut Dokumentation Initialisierung mit static IP eigentlich möglich bei mbed OS, geht aber nicht
    // es gibt wohl einen Branch von mbed mit einem Patch
    //// eth.init(&ownIP, &mask, &Gateway);

    // Ethernetconnection with DHCP
    eth.set_network(OWN_IP, NET_MASK, GATEWAY);
    eth.connect();
    const char *ip = eth.get_ip_address();
    const char *mac = eth.get_mac_address();

    mRserial.printf("IP address is: %s\n", ip ? ip : "No IP");
    mRserial.printf("MAC address is: %s\n", mac ? mac : "No MAC");

    socket.open(&eth);
    socket.bind(PORT);
    socket.set_blocking(false);

    // the timer is used for duty cycle duration measurement
    dutyCycleTimer.reset();
    dutyCycleTimer.start();
}


void sendMessage() {
    if (sendMode == LIVE_MODE) {
        prepareOutMessage((unsigned long)dutyCycleTimer.read_high_resolution_us());
    }

    // send data to the pc via Ethernet with mbed os
    debugTimer.reset();
    debugTimer.start();
    lastMessageSendComplete = false;
    sendBytesCount = socket.sendto(udp_server_address, (char *)&messageOutBuffer, sizeof(messageOutBuffer));
    lastMessageSendComplete = true;
//    SEND_TIMER = (float)debugTimer.read_us();

    // #ifdef DEBUG
    // mRserial.printf("SEND: %d %d %f\n", sendBytesCount, messageOutBuffer.parameterNumber, messageOutBuffer.parameterValue);
    // #endif
}



void receiveMessage() {
    // receive a command
    debugTimer.reset();
    debugTimer.start();
    int receivedBytesCount = (float)socket.recvfrom(&dump_address, (char *)&messageInBuffer, sizeof(messageInBuffer));
//    RECEIVE_TIMER = (float)debugTimer.read_us();

    if (receivedBytesCount > 0) {
        prepareInMessage();
    }

    // // if a command has been received
    // if (RECEIVED_BYTES_COUNT > 0.5f)
    // {
    //
    //     if (messageInBuffer.parameterNumber >= 0) {
    //         parameters[messageInBuffer.parameterNumber] = messageInBuffer.parameterValueInt;
    //     }
    //     else {
    //         specialCommands[(messageInBuffer.parameterNumber + 1) * -1] = messageInBuffer.parameterValueInt;
    //     }
    //     // for debugging
    //     // LAST_COMMAND_ID = messageInBuffer.parameterNumber;
    //     // LAST_COMMAND_VALUE = messageInBuffer.parameterValueInt;
    //     // blue led blinkiblinki on successfull receive
    //     // blueLed = 1;
    // }
    // else
    // {
    //     // red led on until next loop cycle
    //     // redLed = 1;
    // }
    //
    // #ifdef DEBUG
    // mRserial.printf("RECV: %f %d %f\n", RECEIVED_BYTES_COUNT, messageInBuffer.parameterNumber, messageInBuffer.value);
    // #endif
}

void recordMessage() {
    prepareOutMessage((unsigned long)dutyCycleTimer.read_high_resolution_us());
}
