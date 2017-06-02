Introduction
============

Have you ever written code like that?

.. code-block:: c

    Serial.print(last_time_in_sec);
    Serial.print(";");
    Serial.print(offset_time);
    Serial.print(";");
    Serial.print(temp_raw);
    Serial.print(";");
    Serial.print(temp_actual);
    Serial.print(";");
    Serial.print(temp_target);
    Serial.print(";");
    Serial.print(heat * 100);
    Serial.println(";");

Don't much like it? Continue reading...

What is microRay ?
------------------

microRay is a program, that sends commands to a microcontroller
and displays or stores measurement data, that arrives from the microcontroller.

It communicates over serial, usb or ethernet, depending on which interface you select.

It generates a C-library, that you can include in your microcontroller code. The communication
between the microcontroller and the connected pc is realized via this include file.

Supported combinations of controller and interface are:

* Arduino via

  * Serial
  * EthernetShield
  * WifiShield

* Mbed via

  * Serial
  * Ethernet
  * Usb

The following code example shows the basic usage of microRay in your microcontroller code.
The **testparameter** can be controlled from the connected pc and the **channelOne** variable will be transmitted via
the selected interface and displayed on the pc.

.. code-block:: c

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
            microRayCommunicate();
        }
    }


