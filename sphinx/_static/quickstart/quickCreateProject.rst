Create a microRay project
=========================

Create a new microRay project under "Datei" -> "Neues Projekt...".

* Go to "Bearbeiten" -> "Projekteinstellungen"
* Select some options and specify the controller and interface you want to use
* click Ok

**Add channels**



* Go to "Bearbeiten" -> "Kanaleinstellungen"

.. image:: ../../_resources/channelSettingsDialog.png

* click the green plus symbol in the upper right corner to add a variable,
  that will be send from the controller on every loop cycle
* edit the variable name and its display name and click the checkbox "active", so that the variable will be transmitted.
  This is intended as if later you have too many of them to be transmitted in time, that you can deselect some without loosing reference in your code

.. warning:: The choosen variable names will be macros in the generated C-Code. Consider, that they might conflict
             with macros allready defined somewhere else.

**Add parameters**

* Go to "Bearbeiten" -> "Parametereinstellungen"
* add a parameter, that allows you to set values from within microRay

.. image:: ../../_resources/parameterSettingsDialog.png


**Generate include files**

* Click on "Bearbeiten" -> "CCode generieren"
* the include files will be generated in the folder you have specified in "Projekteinstellungen" or if not so, in the program root folder.
  and will be named

  * microRay.h
  * microRay.cpp


