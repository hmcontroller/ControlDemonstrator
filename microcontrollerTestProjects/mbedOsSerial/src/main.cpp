#include <mbed.h>
#include "microRay.h"

Timer loopTimer;

void init();
void loop();

int main()
{
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
    mR_testChannel = mR_testParam;
    microRayCommunicate();
}
