Generate include files
======================

* Click on "Bearbeiten" -> "CCode generieren"
* The include files will be generated in the folder you have specified in "Projekteinstellungen" or if not so,
  in the program root folder, and will be named

  * microRay.h
  * microRay.cpp

* Recompile and upload your code to the controller.
* If you are working with a serial interface, microRay automatically stops the communication and
  releases the used com port, so that you can upload your new code. You then can restart the
  communication by clicking the play button in the upper left area of microRay.

.. note:: When working with the Arduino IDE, it might be necessary, to restart the IDE after code generation,
  because this program does eventually not realize changes to included files made from outside.