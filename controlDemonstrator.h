#ifndef CONFIG_H
#define CONFIG_H

#define ARDUINO_SERIAL

// must have parameters
#define loopCycleTimeUs                           10000
#define CHANNELS_AVAILABLE_COUNT                     19
#define CHANNELS_REQUESTED_COUNT                     12
#define CHANNELS_UNREQUESTED_COUNT                    7
#define PARAMETER_COUNT                               2

// All requested channels
#define analogIn0                                (messageOutBuffer.channels[0])
#define dummy1                                   (messageOutBuffer.channels[1])
#define testParameterChannel                     (messageOutBuffer.channels[2])
#define superSinusFunction                       (messageOutBuffer.channels[3])
#define loopDuration                             (messageOutBuffer.channels[4])
#define sendTimer                                (messageOutBuffer.channels[5])
#define receiveTimer                             (messageOutBuffer.channels[6])
#define paramNumber                              (messageOutBuffer.channels[7])
#define paramValue                               (messageOutBuffer.channels[8])
#define startPosition                            (messageOutBuffer.channels[9])
#define endPosition                              (messageOutBuffer.channels[10])
#define searchPositionDebug                      (messageOutBuffer.channels[11])

// All unrequested channels
#define analogIn1                                (unrequestedChannels[0])
#define analogIn2                                (unrequestedChannels[1])
#define analogIn3                                (unrequestedChannels[2])
#define analogIn4                                (unrequestedChannels[3])
#define analogIn5                                (unrequestedChannels[4])
#define dummy2                                   (unrequestedChannels[5])
#define debugTimer                               (unrequestedChannels[6])

// all parameters
#define testParameter                            (parameters[0])
#define anotherTestParameter                     (parameters[1])

void initControlDemonstrator();
void communicate();


#ifdef ARDUINO_SERIAL
#include <stdint.h>
typedef struct MessageOut
{
    uint32_t loopStartTime;
    uint32_t parameterNumber;
    float parameterValue;
    float channels[CHANNELS_REQUESTED_COUNT];
} MessageOut;

#else
#include <stdint.h>
typedef struct MessageOut
{
    uint32_t loopStartTime;
    uint32_t parameterNumber;
    float parameterValue;
    float channels[CHANNELS_REQUESTED_COUNT];
} MessageOut;
#endif


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