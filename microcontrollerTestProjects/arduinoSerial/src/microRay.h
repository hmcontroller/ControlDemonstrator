#ifndef CONFIG_H
#define CONFIG_H

#define ARDUINO_SERIAL

// must have parameters
#define loopCycleTimeUs                          1000000
#define CHANNELS_AVAILABLE_COUNT                      2
#define CHANNELS_REQUESTED_COUNT                      2
#define CHANNELS_UNREQUESTED_COUNT                    0
#define PARAMETER_COUNT                               1
#define SPECIAL_COMMANDS_COUNT                        3
#define BAUD_RATE                                115200
#define INT_TYPE                                      1
#define FLOAT_TYPE                                    2
#define RECORD_BUFFER_LENGTH                          1
#define PAUSE_AFTER_RECORD                            0
#define MESSAGE_SKIP_MODE                             0

// All requested channels
#define mR_testChannel                           (messageOutBuffer.channels[0])
#define mR_incChannel                            (messageOutBuffer.channels[1])

// All unrequested channels

// all parameters
#define mR_testParam                             (parameters[0]).valueFloat

// all special parameters
#define loopCycleTimeExceededByUs                (specialCommands[0])
#define serialTransmissionLag                    (specialCommands[1])
#define mrRecordModeEnable                       (specialCommands[2])


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
    uint16_t statusFlags;
    uint16_t parameterNumber;
#if !defined(SUPPRESS_PARAM_CONFIRMATION)
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
extern int specialCommands[SPECIAL_COMMANDS_COUNT];


// storage for unrequested channels
// requested channels are stored in messageOutBuffer
extern float unrequestedChannels[CHANNELS_UNREQUESTED_COUNT];

#define RECORD_MODE 0
#define RECORD_TRANSMISSION_MODE 1
#define LIVE_MODE 2
#define RECORD_WAIT_MODE 3
#define WAIT_MODE 4

#define STATUS_BAD_DATA 0
#define STATUS_SKIPPED 1
#endif