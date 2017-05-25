#ifndef CONFIG_H
#define CONFIG_H

#define MBED_2_UDP

// must have parameters
#define loopCycleTimeUs                            5000
#define CHANNELS_AVAILABLE_COUNT                      6
#define CHANNELS_REQUESTED_COUNT                      5
#define CHANNELS_UNREQUESTED_COUNT                    1
#define PARAMETER_COUNT                               4

// All requested channels
#define old2                                     (messageOutBuffer.channels[0])
#define old3                                     (messageOutBuffer.channels[1])
#define old4                                     (messageOutBuffer.channels[2])
#define new                                      (messageOutBuffer.channels[3])
#define guggu                                    (messageOutBuffer.channels[4])

// All unrequested channels
#define super                                    (unrequestedChannels[0])

// all parameters
#define uno                                      (parameters[0])
#define due                                      (parameters[1])
#define New                                      (parameters[2])
#define New                                      (parameters[3])

void initControlDemonstrator();
void communicate();


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