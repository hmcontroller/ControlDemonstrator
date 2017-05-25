Create your microcontroller code
================================


Arduino
-------

.. code-block:: c
   :linenos:

    #include <arduino.h>
    #include "controlDemonstrator.h"

    unsigned long loopStart = micros();
    unsigned long lastLoopDuration = 0;

    void setup() {
        initControlDemonstrator();
        while(1)
        {
            loopStart = micros();
            loop();
            lastLoopDuration = micros() - loopStart;
            while(micros() - loopStart < loopCycleTimeUs)
            {
                // do nothing
            }
        }
    }

    void loop() {
        analogIn0 = analogRead(A0);
        superSinusFunction = 1000.0f * (float)sin(0.001f * millis());
        testParameterChannel = testParameter;
        loopDuration = (float)lastLoopDuration;
        communicate();
    }


Mbed
----

.. code-block:: c
   :linenos:

    #include <arduino.h>
    #include "controlDemonstrator.h"

    unsigned long loopStart = micros();
    unsigned long lastLoopDuration = 0;

    void setup() {
        initControlDemonstrator();
        while(1)
        {
            loopStart = micros();
            loop();
            lastLoopDuration = micros() - loopStart;
            while(micros() - loopStart < loopCycleTimeUs)
            {
                // do nothing
            }
        }
    }

    void loop() {
        analogIn0 = analogRead(A0);
        superSinusFunction = 1000.0f * (float)sin(0.001f * millis());
        testParameterChannel = testParameter;
        loopDuration = (float)lastLoopDuration;
        communicate();
    }


