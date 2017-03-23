import traceback

# #
# #Simple example on how to send and receive data to the Mbed over USB (on windows) using pywinusb
# #
# import pywinusb.hid as hid
# from time import sleep
# import random
# import struct
#
# # handler called when a report is received
# def rx_handler(data):
#
#     # time = int(data[1] | data[2] << 8 | data[3] << 16 | data[4] << 24)
#     # time1 = int(data[10] | data[11] << 8 | data[12] << 16 | data[13] << 24)
#     #
#     # joinedBytes = ''.join(chr(i) for i in [data[5], data[6], data[7], data[8]])
#     # floati = struct.unpack("<f", joinedBytes)[0]
#
#     print 'recv: ', data
#     # print "time", time, time1, floati
#
# def findHIDDevice(mbed_usage, mbed_vendor_id):
#     # Find all devices connected
#     all_devices = hid.HidDeviceFilter(vendor_id = mbed_vendor_id).get_devices()
#
#     if not all_devices:
#         print "No device connected"
#     else:
#         # search for the Mbed
#         for HIDdevice in all_devices:
#             HIDdevice.open()
#             # browse output reports
#             for report in HIDdevice.find_output_reports():
#                 if mbed_usage in report:
#
#                     #MBED found
#                     print 'Mbed detected'
#
#                     #Attach a custom handler when a data is received
#                     HIDdevice.set_raw_data_handler(rx_handler)
#
#                     buffer = [0xFF]*65
#                     buffer[0] = 0
#                     buffer[64] = 214
#
#                     # report.set_raw_data(buffer)
#
#
#                     #send a report each 0.2 second. The report is a random array of 8 bytes
#                     while True:
#                         # for i in range(0, 64):
#                         # report[0] = 63
#                         # report[63] = 250
#                         for i in range(8):
#                             report[mbed_usage][i] = random.randint(0, 255)
#                         report.send()
#                         sleep(0.5)
#                 HIDdevice.close()
#
#
# if __name__ == '__main__':
#     # The vendor ID used in the Mbed program
#     mbed_vendor_id = 0x1234
#
#     # Vendor page and usage_id = 2
#     mbed_usage = hid.get_full_usage_id(0xffab, 0x02)
#
#     # Search the Mbed, attach rx handler and send data
#     findHIDDevice(mbed_usage, mbed_vendor_id)


#
#Simple example on how to send and receive data to the Mbed over USB (on windows) using pywinusb
#
import pywinusb.hid as hid
from time import sleep
import random

# handler called when a report is received
def rx_handler(data):
    print 'recv: ', data

def findHIDDevice(mbed_usage, mbed_vendor_id):
    # Find all devices connected
    all_devices = hid.HidDeviceFilter(vendor_id = mbed_vendor_id).get_devices()

    if not all_devices:
        print "No device connected"
    else:
        # search for the Mbed
        for HIDdevice in all_devices:
            try:
                HIDdevice.open()
                # browse output reports
                for report in HIDdevice.find_output_reports():
                    if mbed_usage in report:

                        #MBED found
                        print 'Mbed detected'

                        buffer = list()
                        buffer.append(0)
                        for i in range(1, 9):
                            buffer.append(i-1)

                        print report

                        #Attach a custom handler when a data is received
                        HIDdevice.set_raw_data_handler(rx_handler)

                        #send a report each 0.2 second. The report is a random array of 8 bytes
                        while True:
                            for i in range(8):
                                report[mbed_usage][i] = random.randint(0, 255)
                            report.send(buffer)
                            # HIDdevice.send_output_report(buffer)
                            print "send:", buffer #report[mbed_usage].value
                            sleep(0.2)
            except:
                print 'close'
                print traceback.format_exc()
                HIDdevice.close()


if __name__ == '__main__':
    # The vendor ID used in the Mbed program
    mbed_vendor_id = 0x1234

    # Vendor page and usage_id = 2
    mbed_usage = hid.get_full_usage_id(0xffab, 0x02)

    # Search the Mbed, attach rx handler and send data
    findHIDDevice(mbed_usage, mbed_vendor_id)









# import usb.core
# import usb.util
#
# vendorId = 0x1234
# productId = 0x6
#
# dev = usb.core.find(idVendor=vendorId, idProduct=productId)
# # dev = usb.core.find(find_all=True)
#
# # print dev
#
#
# config = dev.get_active_configuration()
# dev.set_configuration(config)
#
#
# interface = config[(0,0)]
#
# endpoint_OUT = usb.util.find_descriptor(
#            interface,
#            # match the first OUT endpoint
#            custom_match = \
#            lambda e: \
#            usb.util.endpoint_direction(e.bEndpointAddress) == \
#            usb.util.ENDPOINT_OUT)
#
#
# endpoint_IN = usb.util.find_descriptor(
#            interface,
#            # match the first OUT endpoint
#            custom_match = \
#            lambda e: \
#            usb.util.endpoint_direction(e.bEndpointAddress) == \
#            usb.util.ENDPOINT_IN)
#
# assert endpoint_OUT is not None
#
# print endpoint_OUT
#
# buffer = [0xFF]*8
# buffer[0] = 0x1
# buffer[2] = 0x2
# buffer[7] = 0x3
#
# data = [0x5] * 8
#
# while True:
#     print endpoint_IN.read(64)
#
#     # write the data
#     print "send {} bytes".format(endpoint_OUT.write(data))
#
#     # dev.write(0x1, data)
#
#     sleep(1.0)
