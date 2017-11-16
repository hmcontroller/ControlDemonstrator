#ifndef CONFIG_H
#define CONFIG_H

#define MBED_OS_SERIAL

// must have parameters
#define loopCycleTimeUs                            3000
#define CHANNELS_AVAILABLE_COUNT                      2
#define CHANNELS_REQUESTED_COUNT                      2
#define CHANNELS_UNREQUESTED_COUNT                    0
#define PARAMETER_COUNT                               2
#define SPECIAL_COMMANDS_COUNT                        2
#define BAUD_RATE                                115200
#define INT_TYPE                                      1
#define FLOAT_TYPE                                    2
#define BAUD_RATE                                115200

// All requested channels
#define mR_testChannel                           (messageOutBuffer.channels[0])
#define mR_incChannel                            (messageOutBuffer.channels[1])

// All unrequested channels

// all parameters
#define mR_testParamInt                          (parameters[0]).valueInt
#define mR_testParamFloat                        (parameters[1]).valueFloat

// all special parameters
#define loopCycleTimeExceededByUs                (specialCommands[0])
#define serialTransmissionLag                    (specialCommands[1])


void microRayInit();
void microRayCommunicate();


#include <stdint.h>


typedef struct MessageIn
{
    int32_t parameterNumber;
    union {
        int32_t parameterValueInt;
        float parameterValueFloat;
    };
} MessageIn;

typedef struct MessageOut
{
    uint32_t loopStartTime;
#if !defined(SUPPRESS_PARAM_CONFIRMATION)
    uint32_t parameterNumber;
    union {
        int32_t parameterValueInt;
        float parameterValueFloat;
    };
#endif
    float channels[CHANNELS_REQUESTED_COUNT];
} MessageOut;

extern MessageOut messageOutBuffer;



typedef struct Parameter {
    uint8_t dataType;
    union {
        int32_t valueInt;
        float valueFloat;
    };
} Parameter;

extern Parameter parameters[PARAMETER_COUNT];
extern float specialCommands[SPECIAL_COMMANDS_COUNT];


// storage for unrequested channels
// requested channels are stored in messageOutBuffer
extern float unrequestedChannels[CHANNELS_UNREQUESTED_COUNT];
#endif