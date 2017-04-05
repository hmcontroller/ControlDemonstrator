void initControlDemonstrator();
void communicate();


typedef struct MessageOut
{
    int loopStartTime;
    int lastLoopDuration;
    int parameterNumber;
    float parameterValue;
    float channels[CHANNELS_REQUESTED_COUNT];
} MessageOut;

typedef struct MessageIn
{
    int parameterNumber;
    float value;
} MessageIn;

// storage for channels
extern float unrequestedChannels[CHANNELS_UNREQUESTED_COUNT];

// storage for parameters, that could be set from the pc
extern float parameters[PARAMETER_COUNT];

extern MessageOut messageOutBuffer;
