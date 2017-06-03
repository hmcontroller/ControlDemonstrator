Create your microcontroller code
================================


Arduino example
---------------

.. code-block:: c

    #include <arduino.h>
    #include "microRay.h"

    unsigned long loopStart = micros();
    unsigned long lastLoopDuration = 0;

    void setup() {
        microRayInit();
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
        microRayCommunicate();
    }


Mbed example
------------

.. code-block:: c

    #include "mbed.h"
    #include "microRay.h"

    Timer loopTimer;

    int main()
    {
        init();

        while(1)
        {
            loopTimer.start();
            loop();
            while(loopTimer.read_us() < loopCycleTimeUs)
            {
                // do nothing
            }
            loopTimer.reset();
        }
    }

    void init()
    {
        initControlDemonstrator();
        ...
    }

    void loop()
    {
        analogIn0 = analogRead(A0);
        superSinusFunction = 1000.0f * (float)sin(0.001f * millis());
        testParameterChannel = testParameter;
        loopDuration = (float)lastLoopDuration;
        microRayCommunicate();
    }

