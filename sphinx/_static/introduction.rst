Introduction
============

What is microRay ?
------------------

The microRay is a program, that sends commands to a microcontroller
and displays or stores measurement data, that arrives from the microcontroller.

It communicates over serial, usb or ethernet, depending on which interface you select.

It generates a C-library, that you have to include in your microcontroller code. Supported combinations of controller
and interface are:

* Arduino via

  * Serial
  * EthernetShield
  * WifiShield

* Mbed via

  * Serial
  * Ethernet
  * Usb

The following code example shows the basic usage of the microRay in your microcontroller code.
The testparameter can be controlled from the connected pc and the channelOne variable will be transmitted and
displayed on the pc.

.. code-block:: c
   :linenos:

    #include "microRay.h"

    int main() {
        microRayInit();
        while(1) {
            if (testparameter > 0.5f) {
                channelOne = 12.0f;
            }
            else {
                channelOne = 11.0f;
            }
            communicate();
        }
    }


microRay SuperApp
-----------------

Bla guggu das ist ein Testtext.

=================================== ======================================================================
PlotDataItem(xValues, yValues)      x and y values may be any sequence (including ndarray) of real numbers
PlotDataItem(yValues)               y values only -- x will be automatically set to range(len(y))
PlotDataItem(x=xValues, y=yValues)  x and y given by keyword arguments
PlotDataItem(ndarray(Nx2))          numpy array with shape (N, 2) where x=data[:,0] and y=data[:,1]
=================================== ======================================================================

example::

    from core.settings import *
    doWrite(gaga)
    print "Hallo"
    for i in range(0, 10):
        pass