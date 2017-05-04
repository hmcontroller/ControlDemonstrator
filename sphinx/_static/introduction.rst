Introduction
============

What is a ControlDemonstrator ?
-------------------------------

The Control Demonstrator is a program, that sends commands to a microcontroller
and displays or stores measurement data, that arrives from the microcontroller.

It communicates over serial or ethernet, depending on which Schnittstelle you select.

It generates a C-library, that you have to include in your microcontroller code. Supported are

- Arduino with Serial and Ethernet Udp
- Mbed with Serial and Udp

The following code example shows the basic usage of the ControlDemonstrator in your microcontroller code.
The testparameter can be controlled from the connected pc and the channelOne variable will be transmitted and
displayed on the pc.

example::

    #include "ControlDemonstrator.h"

    int main() {
        initControlDemonstrator();
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