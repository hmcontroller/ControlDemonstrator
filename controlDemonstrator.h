#ifndef CONFIG_H
#define CONFIG_H

#define MBED_OS_UDP

// must have parameters
#define loopCycleTimeUs                            5000
#define CHANNELS_AVAILABLE_COUNT                     32
#define CHANNELS_REQUESTED_COUNT                      9
#define CHANNELS_UNREQUESTED_COUNT                   23
#define PARAMETER_COUNT                              59

// All requested channels
#define ANALOG_IN_2                              (messageOutBuffer.channels[0])
#define ANALOG_IN_3                              (messageOutBuffer.channels[1])
#define PID1_ERROR                               (messageOutBuffer.channels[2])
#define PID1_SET_POINT                           (messageOutBuffer.channels[3])
#define SP_GEN_1_OUTPUT                          (messageOutBuffer.channels[4])
#define DEBUG_TIMER                              (messageOutBuffer.channels[5])
#define SEND_TIMER                               (messageOutBuffer.channels[6])
#define RECEIVE_TIMER                            (messageOutBuffer.channels[7])
#define LOOP_DURATION                            (messageOutBuffer.channels[8])

// All unrequested channels
#define ANALOG_IN_0                              (unrequestedChannels[0])
#define ANALOG_IN_1                              (unrequestedChannels[1])
#define ANALOG_IN_4                              (unrequestedChannels[2])
#define ANALOG_IN_5                              (unrequestedChannels[3])
#define PID1_P_PORTION                           (unrequestedChannels[4])
#define PID1_INTEGRAL                            (unrequestedChannels[5])
#define PID1_I_PORTION                           (unrequestedChannels[6])
#define PID1_LAST_ERROR                          (unrequestedChannels[7])
#define PID1_INTERVAL_LENGTH                     (unrequestedChannels[8])
#define PID1_D_PORTION                           (unrequestedChannels[9])
#define PID2_ERROR                               (unrequestedChannels[10])
#define PID2_P_PORTION                           (unrequestedChannels[11])
#define PID2_INTEGRAL                            (unrequestedChannels[12])
#define PID2_I_PORTION                           (unrequestedChannels[13])
#define PID2_LAST_ERROR                          (unrequestedChannels[14])
#define PID2_INTERVAL_LENGTH                     (unrequestedChannels[15])
#define PID2_SET_POINT                           (unrequestedChannels[16])
#define RECEIVED_BYTES_COUNT                     (unrequestedChannels[17])
#define FAST_PWM_ON                              (unrequestedChannels[18])
#define FAST_PWM_PERCENT                         (unrequestedChannels[19])
#define LAST_COMMAND_ID                          (unrequestedChannels[20])
#define LAST_COMMAND_VALUE                       (unrequestedChannels[21])
#define LAST_COMMAND_FROM_ARRAY_VALUE            (unrequestedChannels[22])

// all parameters
#define PID1_KP_SWITCH                           (parameters[0])
#define PID1_KP_VALUE                            (parameters[1])
#define PID1_KI_SWITCH                           (parameters[2])
#define PID1_KI_VALUE                            (parameters[3])
#define PID1_KD_SWITCH                           (parameters[4])
#define PID1_KD_VALUE                            (parameters[5])
#define PID2_KP_SWITCH                           (parameters[6])
#define PID2_KP_VALUE                            (parameters[7])
#define PID2_KI_SWITCH                           (parameters[8])
#define PID2_KI_VALUE                            (parameters[9])
#define PID2_KD_SWITCH                           (parameters[10])
#define PID2_KD_VALUE                            (parameters[11])
#define SP_GEN1_NUMBER                           (parameters[12])
#define SP_GEN1_DIRAC_START_TIME                 (parameters[13])
#define SP_GEN1_DIRAC_NOW                        (parameters[14])
#define SP_GEN1_DIRAC_LOW                        (parameters[15])
#define SP_GEN1_DIRAC_HIGH                       (parameters[16])
#define SP_GEN1_DIRAC_DURATION                   (parameters[17])
#define SP_GEN1_STEP_LOW                         (parameters[18])
#define SP_GEN1_STEP_HIGH                        (parameters[19])
#define SP_GEN1_STEP_STATE                       (parameters[20])
#define SP_GEN1_SIN_AMPLITUDE                    (parameters[21])
#define SP_GEN1_SIN_OMEGA                        (parameters[22])
#define SP_GEN1_SIN_OFFSET                       (parameters[23])
#define SP_GEN1_SQUARE_LOW                       (parameters[24])
#define SP_GEN1_SQUARE_HIGH                      (parameters[25])
#define SP_GEN1_SQUARE_FREQUENCY                 (parameters[26])
#define SP_GEN1_SQUARE_STATE                     (parameters[27])
#define SP_GEN1_SQUARE_LAST_TOGGLE               (parameters[28])
#define SP_GEN1_RAMP_START_TIME                  (parameters[29])
#define SP_GEN1_RAMP_STATE                       (parameters[30])
#define SP_GEN1_RAMP_LAST_STATE                  (parameters[31])
#define SP_GEN1_RAMP_GRADIENT                    (parameters[32])
#define SP_GEN1_RAMP_LOW                         (parameters[33])
#define SP_GEN1_RAMP_HIGH                        (parameters[34])
#define SLOW_PWM_ON                              (parameters[35])
#define SLOW_PWM_PERCENT                         (parameters[36])
#define SP_GEN2_ON                               (parameters[37])
#define SP_GEN2_NUMBER                           (parameters[38])
#define SP_GEN2_DIRAC_NOW                        (parameters[39])
#define SP_GEN2_DIRAC_LOW                        (parameters[40])
#define SP_GEN2_DIRAC_HIGH                       (parameters[41])
#define SP_GEN2_DIRAC_DURATION                   (parameters[42])
#define SP_GEN2_STEP_LOW                         (parameters[43])
#define SP_GEN2_STEP_HIGH                        (parameters[44])
#define SP_GEN2_STEP_STATE                       (parameters[45])
#define SP_GEN2_SIN_AMPLITUDE                    (parameters[46])
#define SP_GEN2_SIN_OMEGA                        (parameters[47])
#define SP_GEN2_SIN_OFFSET                       (parameters[48])
#define SP_GEN2_SQUARE_LOW                       (parameters[49])
#define SP_GEN2_SQUARE_HIGH                      (parameters[50])
#define SP_GEN2_SQUARE_FREQUENCY                 (parameters[51])
#define SP_GEN2_SQUARE_STATE                     (parameters[52])
#define SP_GEN2_RAMP_START_TIME                  (parameters[53])
#define SP_GEN2_RAMP_STATE                       (parameters[54])
#define SP_GEN2_RAMP_GRADIENT                    (parameters[55])
#define SP_GEN2_RAMP_LOW                         (parameters[56])
#define SP_GEN2_RAMP_HIGH                        (parameters[57])
#define PID1_SENSOR_SOURCE                       (parameters[58])

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


#endif