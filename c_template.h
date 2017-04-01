void initControlDemonstrator();
void communicate();

// storage for channels
extern float channels[AVAILABLE_CHANNEL_COUNT];

// storage for parameters, that could be set from the pc
extern float parameters[PARAMETER_COUNT];

typedef struct MessageOut
{
    int loopStartTime;
    int lastLoopDuration;
    int parameterNumber;
    float parameterValue;
    float channels[REQUESTED_CHANNEL_COUNT];
} MessageOut;

typedef struct MessageIn
{
    int parameterNumber;
    float value;
} MessageIn;