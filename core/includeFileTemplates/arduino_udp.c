
#include <arduino.h>
#include <SPI.h>
#include <Ethernet2.h>
#include <EthernetUdp2.h>

byte macAddress[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ownIp(192, 168, 0, 15);
IPAddress remoteIp(192, 168, 0, 133);
unsigned int port = 10000;
EthernetUDP Udp;

void microRayInit()
{
    setInitialValues();
    // Bring up the network interface
    Ethernet.begin(macAddress, ownIp);
    Udp.begin(port);
}




void sendMessage()
{
    prepareOutMessage(micros());

    lastTime = micros();
    Udp.beginPacket(remoteIp, port);
    Udp.write((char *)&messageOutBuffer, sizeof(messageOutBuffer));
    Udp.endPacket();
    // sendTimer = (float)(micros() - lastTime);
}


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
