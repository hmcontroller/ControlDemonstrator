# -*- encoding: utf-8 -*-

import socket
import errno

class UdpCommunicator():
    def __init__(self, ownIp, remoteIp, rxPort, txPort, messageSize):
        # TODO - check remotePort against txPort or what is more clear
        self.ownIp = ownIp
        self.remoteIp = remoteIp
        self.rxPort = rxPort
        self.txPort = txPort
        self.messageSize = messageSize

        self.sockRX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRX.bind((self.ownIp, self.rxPort))
        self.sockRX.setblocking(False)
        self.sockRX.settimeout(0)

        self.sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockTX.bind((self.ownIp, self.txPort))
        self.sockTX.setblocking(False)
        self.sockTX.settimeout(0)



    def send(self, packedData):
        self.sockTX.sendto(packedData, (self.remoteIp, self.txPort))

    def receive(self):
        bufferContainsData = True
        packets = list()
        while bufferContainsData is True:
            try:
                data, address = self.sockRX.recvfrom(self.messageSize)
            except socket.timeout:
                bufferContainsData = False
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    bufferContainsData = False
                else:
                    raise
            else:
                packets.append(data)
        return packets

    def getData(self):
        pass

    def _unpack(self):
        # TODO - think about how to single source the packet configuration
        # TODO at the time being, the source is types.h -> messageOut in the microcontroller code
        pass
