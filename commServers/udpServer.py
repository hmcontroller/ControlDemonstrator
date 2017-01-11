import socket
import signal
import sys
import struct
import threading
import collections
import time

import numpy

class DataAquisitionServerUDP(threading.Thread):
    def __init__(self):
        super(DataAquisitionServerUDP, self).__init__()
        self.ringBuffers = None
        self.bufferCount = 0
        self.bufferLength = None
        self.channelCount = None
        self.rotatingCounter = 1

        # self.ip = '192.168.178.20'
        self.ip = '192.168.0.133'
        # self.controllerIP = '192.168.178.59'
        self.controllerIP = '192.168.0.10'
        self.portRX = 10000
        self.portTX = 10001

        self.sockRX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRX.bind((self.ip, self.portRX))
        #self.sock.settimeout(1)

        print 'UDP Server Running at ', self.sockRX.getsockname()# socket.gethostbyname(socket.gethostname())

        self.sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockTX.bind((self.ip, self.portTX))

        self.keepRunning = True

        self.loopDurationMin = 1000000
        self.loopDurationMax = 0
        self.loopDurationAverage = 0
        self.loopDurationSum = 0
        self.loopDurationCounter = 0

        self.parametersReceived = list()
        self.parametersToSend = list()
        self.parameterCount = 0

        self.timeValues = None

        self.configured = False


    def configure(self, buffers, channelCount, parameterCount, timeValues):
        self.ringBuffers = buffers
        self.bufferCount = len(self.ringBuffers)
        self.parameterCount = parameterCount
        self.timeValues = timeValues

        if self.bufferCount > 0:
            self.bufferLength = len(self.ringBuffers[0])
        else:
            raise Exception("Need at least one buffer")
        self.channelCount = channelCount
        self.parametersReceived = [0.0] * self.parameterCount
        self.parametersToSend = range(0, self.parameterCount)

        self.configured = True



    def run(self):
        if self.configured is False:
            raise Exception("UDP-Server not configured, use method configure(...)")
        parameterCounter = 0
        # messageSize = (channelCount + fastParameterCount) * 4 + 16
        messageSize = self.channelCount * 4 + 16


        while self.keepRunning is True:
            # print "waiting for UDP data packet..."
            data, address = self.sockRX.recvfrom(messageSize)

            loopStartTime = struct.unpack("<i", data[messageSize - 16:messageSize - 12])[0]
            loopDuration = struct.unpack("<i", data[messageSize - 12:messageSize - 8])[0]
            if loopDuration < self.loopDurationMin :
                self.loopDurationMin = loopDuration
            elif loopDuration > self.loopDurationMax :
                self.loopDurationMax = loopDuration



            self.loopDurationSum += loopDuration
            self.loopDurationCounter += 1
            self.loopDurationAverage = self.loopDurationSum / float(self.loopDurationCounter)

            with threading.Lock():
                self.timeValues.append(loopStartTime)# / 1000000.0)
                for i in range(0, self.channelCount):
                    self.ringBuffers[i].append(struct.unpack("<f", data[i*4:i*4+4])[0])

            # print "times", self.timeValues
            # print "values", self.ringBuffers[2]

            parameterNumber = struct.unpack("<i", data[messageSize - 8:messageSize - 4])[0]
            parameterValue = struct.unpack("<f", data[messageSize - 4:messageSize])[0]

            #print "received parameters", parameterNumber, parameterValue

            self.parametersReceived[parameterNumber] = parameterValue

            message = None

            # struct.pack_into("<if", message, 0, parameterCounter, self.parametersToSend[parameterCounter])

            # packer = struct.Struct("i f")
            packed_data = struct.pack("< i f", parameterCounter, self.parametersToSend[parameterCounter])
            self.sockTX.sendto(packed_data, (self.controllerIP, self.portTX))
            #print parameterCounter, self.parametersToSend[parameterCounter]

            parameterCounter += 1
            if parameterCounter >= len(self.parametersToSend):
                parameterCounter = 0


        print "UDP Server stopped"

    def stop(self):
        self.keepRunning = False


if __name__ == "__main__":
    bufferOne = collections.deque(maxlen=10)
    ringBuffers = [bufferOne]
    server = DataAquisitionServerUDP(ringBuffers)
    server.start()
    print "Thread started"
    time.sleep(1)
    server.stop()
    print "finish"
