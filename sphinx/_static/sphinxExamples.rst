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

HALLO
=====

Aufzählung

* Punkt 1
* Punkt 2
* Punkt 3

**Fett gedruckt**


.. image:: ../_resources/channelSettingsDialog.png

.. warning:: This is something dangerous

.. note:: This might be helpfull


.. role:: red

.red {
    color:red;

}

The following code example shows the basic usage of microRay in your microcontroller code.
The :red:`testparameter` can be controlled from the connected pc and the channelOne variable will be transmitted and
displayed on the pc.
