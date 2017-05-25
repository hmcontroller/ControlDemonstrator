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


