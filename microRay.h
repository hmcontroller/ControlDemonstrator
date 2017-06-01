#ifndef CONFIG_H
#define CONFIG_H

#define ARDUINO_SERIAL

// must have parameters
#define loopCycleTimeUs                            5000
#define CHANNELS_AVAILABLE_COUNT                      0
#define CHANNELS_REQUESTED_COUNT                      0
#define CHANNELS_UNREQUESTED_COUNT                    0
#define PARAMETER_COUNT                               0

// All requested channels

// All unrequested channels

// all parameters

void microRayInit();
void microRayCommunicate();


#include <stdint.h>
typedef struct MessageOut
{
    uint32_t loopStartTime;
    uint32_t parameterNumber;
    float parameterValue;
    float channels[CHANNELS_REQUESTED_COUNT];
} MessageOut;


typedef struct MessageIn
{
    uint32_t parameterNumber;
    float value;
} MessageIn;

// storage for channels
extern float unrequestedChannels[CHANNELS_UNREQUESTED_COUNT];

// storage for parameters, that could be set from the pc
extern float parameters[PARAMETER_COUNT];

extern MessageOut messageOutBuffer;


#endif