#include <Arduino.h>
#include "microRay.h"

void setup() {
    microRayInit();
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, !digitalRead(13));
    mR_testChannel = mR_testParam;
    mR_incChannel += 1;
    if (mR_incChannel > 1000) {
        mR_incChannel = 0;
    }
    microRayCommunicate();
    delayMicroseconds(100);
}
