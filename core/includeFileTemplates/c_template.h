
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

typedef struct MessageOutSerial
{
    uint8_t startByte;
    uint32_t loopStartTime;
    uint32_t parameterNumber;
    float parameterValue;
    float channels[CHANNELS_REQUESTED_COUNT];
    uint8_t stopByte;
} MessageOutSerial;


typedef struct MessageIn
{
    int32_t parameterNumber;
    float value;
} MessageIn;

// storage for channels
extern float unrequestedChannels[CHANNELS_UNREQUESTED_COUNT];

// storage for parameters, that could be set from the pc
extern float parameters[PARAMETER_COUNT];
extern float specialCommands[SPECIAL_COMMANDS_COUNT];

//extern MessageOutSerial messageOutBuffer;
extern MessageOut messageOutBuffer;
