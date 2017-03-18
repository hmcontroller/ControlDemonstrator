# -*- encoding: utf-8 -*-

import errno
import time
import socket
import struct

lastLoopStart = 0
sendDurationMin = 10000000
sendDurationMax = 0
sendDurationAverage = 0
sendDurationSum = 0
sendDurationCounter = 0

receiveDurationMin = 1000000
receiveDurationMax = 0
receiveDurationAverage = 0
receiveDurationCounter = 0
receiveDurationSum = 0


def calculateLoopTimes(data):
    global sendDurationMin
    global sendDurationMax
    global sendDurationAverage
    global sendDurationCounter
    global sendDurationSum

    global receiveDurationMin
    global receiveDurationMax
    global receiveDurationAverage
    global receiveDurationCounter
    global receiveDurationSum



    sendDuration = data[1]
    # calculate some statistics
    if sendDuration < sendDurationMin:
        sendDurationMin = sendDuration
    elif sendDuration > sendDurationMax:
        sendDurationMax = sendDuration

    sendDurationSum += sendDuration
    sendDurationCounter += 1
    sendDurationAverage = sendDurationSum / float(sendDurationCounter)

    receiveDuration = data[2]
    # calculate some statistics
    if receiveDuration < receiveDurationMin:
        receiveDurationMin = receiveDuration
    elif receiveDuration > receiveDurationMax:
        receiveDurationMax = receiveDuration

    receiveDurationSum += receiveDuration
    receiveDurationCounter += 1
    receiveDurationAverage = receiveDurationSum / float(receiveDurationCounter)




def unpackData(data):
    loopTimePart = data[0:4]
    sendTimePart = data[4:8]
    receiveTimePart = data[8:12]


    floats = list()
    for i in range(3, 33):
        rawPart = data[i*4:i*4+4]
        floats.append(struct.unpack("<f", rawPart)[0])

    loopTime = struct.unpack("<i", loopTimePart)[0]
    sendTime = struct.unpack("<i", sendTimePart)[0]
    receiveTime = struct.unpack("<i", receiveTimePart)[0]


    return loopTime, sendTime, receiveTime, floats

def printUnpackedData(data):
    print data

def printReport(lastData, incomingPacketCounter):
    global sendDurationMin
    global sendDurationMax
    global sendDurationAverage
    global sendDurationCounter
    global sendDurationSum

    global receiveDurationMin
    global receiveDurationMax
    global receiveDurationAverage
    global receiveDurationCounter
    global receiveDurationSum

    print "SEND min: {} max: {} avg: {}".format(sendDurationMin, sendDurationMax, sendDurationAverage)
    print "RECV min: {} max: {} avg: {}".format(receiveDurationMin, receiveDurationMax, receiveDurationAverage)
    print "lastData:", lastData
    print "packages received: {}".format(incomingPacketCounter)
    print "==========                   =================               =================             ==============="


ECHO_PORT = 10000

print 'Server Running at ', socket.gethostbyname(socket.gethostname())
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



data = struct.pack("<2f", 3.2, 4.5)
controllerAddressAndPort = ("192.168.0.12", 10000)
ownAddressAndPort = ("192.168.0.133", 10000)

# sock.bind(('', 10000))
sock.bind(ownAddressAndPort)
sock.setblocking(False)
sock.settimeout(0)

incomingPacketCounter = 0
lastData = None
loopLastTime = int(time.time())
while True:
    try:
        data, address = sock.recvfrom(132)
        lastData = unpackData(data)
        calculateLoopTimes(lastData)
        incomingPacketCounter += 1
    except socket.timeout:
        pass
    except socket.error, e:
        if e.args[0] == errno.EWOULDBLOCK:
            pass
        else:
            raise

    now = int(time.time())
    if loopLastTime != now:
        loopLastTime = now

        if now % 1 == 0: # haha
            # print "Sending packet to client"
            sock.sendto(data, controllerAddressAndPort)
            printReport(lastData, incomingPacketCounter)
            incomingPacketCounter = 0


    time.sleep(0.001)