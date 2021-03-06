
void microRayInit();
void microRayCommunicate();


#include <stdint.h>


#if defined(MBED_OS_SERIAL) || defined(ARDUINO_SERIAL)
    typedef struct MessageOut
    {
//        char startByte;
        uint32_t loopStartTime;
        uint32_t parameterNumber;
        float parameterValue;
        float channels[CHANNELS_REQUESTED_COUNT];
//        char stopByte;
    } MessageOut;
#else
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
