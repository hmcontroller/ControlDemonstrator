Create a microRay project
=========================

* Create a new microRay project under "Datei" -> "Neues Projekt...".

**First define some general settings**

* Go to "Bearbeiten" -> "Projekteinstellungen"
* Select some options and specify the controller and interface you want to use
* click Ok

**Then add channels**



* Go to "Bearbeiten" -> "Kanaleinstellungen"

.. image:: ../../_resources/channelSettingsDialog.png

* Click the green plus symbol in the upper right corner to add a variable,
  that will be send from the controller on every loop cycle.
* Edit the variable name and, if you like, its display name and check the "active" checkbox, so that the variable will be transmitted.
  The "active" option is intended as if when your project grows, you have too many channels to be transmitted just in
  time, that you can deselect some without loosing reference to them in your code.

.. warning:: The choosen variable names will be macros in the generated C-Code. Consider, that they might conflict
             with macros already defined somewhere else.

**You can also add parameters**

* Go to "Bearbeiten" -> "Parametereinstellungen"
* add a parameter, that allows you to set values from within microRay directly on the controller

.. image:: ../../_resources/parameterSettingsDialog.png





