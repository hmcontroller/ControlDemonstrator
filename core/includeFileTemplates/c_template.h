
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
