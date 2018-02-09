#include <mbed.h>
#include "microRay.h"

Timer loopTimer;
Timer dutyTimer;
DigitalOut greenLed(LED1);
DigitalOut blueLed(LED2);
//DigitalOut redLed(LED3);
AnalogIn aIn(A1);


int debugCounter = 0;

void init();
void loop();


// void duda() {
//     greenLed = !greenLed;
// }

int main()
{
    // mrSerial.attach(&duda);
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
    dutyTimer.start();
}

void loop()
{
    debugCounter += 1;
    if (debugCounter > 100) {
        debugCounter = 0;
        blueLed = !blueLed;
        messageOutBuffer.statusFlags &= ~(1 << STATUS_SKIPPED);
    }
    if (debugCounter == 50) {
        messageOutBuffer.statusFlags |= (1 << STATUS_SKIPPED);
    }

    mR_testChannel = mR_testParamFloat;
    if (mR_testParamInt) {
        mR_incChannel += 0.01;
        if (mR_incChannel > 1.0) {
            mR_incChannel = 0;
        }
    }
    mR_analog_in = aIn.read();
    mR_sin_test = 0.2 * (float)sin(5 * dutyTimer.read()) + 0.4;
    microRayCommunicate();
}
