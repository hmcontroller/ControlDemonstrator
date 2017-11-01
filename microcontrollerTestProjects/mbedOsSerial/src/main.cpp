#include <mbed.h>
#include "microRay.h"

Timer loopTimer;
//DigitalOut greenLed(LED1);
DigitalOut blueLed(LED2);
//DigitalOut redLed(LED3);

int debugCounter = 0;

void init();
void loop();

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

void init() {
    microRayInit();
}

void loop()
{
    debugCounter += 1;
    if (debugCounter > 10) {
        debugCounter = 0;
        blueLed = !blueLed;
    }
    //mR_testChannel = mR_testParam;
    // mR_incChannel += 1;
    // if (mR_incChannel > 1000) {
    //     mR_incChannel = 0;
    // }
    microRayCommunicate();
}
