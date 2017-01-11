import socket
import signal
import sys
import struct
import threading
import collections
import time

class DataAquisitionServerUDP(threading.Thread):
    def __init__(self, ringBufferList):
        super(DataAquisitionServerUDP, self).__init__()
        self.ringBuffers = ringBufferList

        self.ip = '192.168.178.20'
        self.port = 10000

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

        print 'UDP Server Running at ', socket.gethostbyname(socket.gethostname())

        self.keepRunning = True

    def run(self):
        while self.keepRunning is True:
            # print "waiting for UDP data packet..."
            data, address = self.sock.recvfrom(111)
            # analogs = []
            # for i in range(0, 6):
            #     val = struct.unpack("!H", data[i:i+2])[0]
            #     analogs.append(val)
            #     if i == 0:
            #         with threading.Lock():
            #             self.ringBuffers[0].append(val)

            # print self.ringBuffers[0]

            # print data, address

            self.sock.sendto(data, address)
            #time.sleep(0.1)
            #print "Received packet from", address, "with data", analogs#, struct.unpack("!H", data)[0]

            # print "Sending  packet back to client"
            # sock.sendto(data, address)

    def stop(self):
        self.keepRunning = False

if __name__ == "__main__":
    bufferOne = collections.deque(maxlen=10)
    ringBuffers = [bufferOne]
    server = DataAquisitionServerUDP(ringBuffers)
    server.start()
    print "Thread started"
    while True:
        pass
    time.sleep(1)
    server.stop()
    print "finish"
