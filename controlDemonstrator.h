#ifndef CONFIG_H
#define CONFIG_H

#define ARDUINO_UDP

// must have parameters
#define LOOP_CYCLE_TIME_US                         5000
#define AVAILABLE_CHANNEL_COUNT                      32
#define REQUESTED_CHANNEL_COUNT                       9
#define PARAMETER_COUNT                              62

// All available channels
// Define names for parameters, that can be send to the connected pc.
// These names are referred to in the whole code.
// The list is generated automatically from a python script.
// On the controller all values are stored in "float channels[AVAILABLE_CHANNEL_COUNT]."
#define ANALOG_IN_0                              (channels[0])
#define ANALOG_IN_1                              (channels[1])
#define ANALOG_IN_2                              (channels[2])
#define ANALOG_IN_3                              (channels[3])
#define ANALOG_IN_4                              (channels[4])
#define ANALOG_IN_5                              (channels[5])
#define PID1_ERROR                               (channels[6])
#define PID1_P_PORTION                           (channels[7])
#define PID1_INTEGRAL                            (channels[8])
#define PID1_I_PORTION                           (channels[9])
#define PID1_LAST_ERROR                          (channels[10])
#define PID1_INTERVAL_LENGTH                     (channels[11])
#define PID1_D_PORTION                           (channels[12])
#define PID1_SET_POINT                           (channels[13])
#define PID2_ERROR                               (channels[14])
#define PID2_P_PORTION                           (channels[15])
#define PID2_INTEGRAL                            (channels[16])
#define PID2_I_PORTION                           (channels[17])
#define PID2_LAST_ERROR                          (channels[18])
#define PID2_INTERVAL_LENGTH                     (channels[19])
#define PID2_SET_POINT                           (channels[20])
#define LOOP_DURATION                            (channels[21])
#define RECEIVED_BYTES_COUNT                     (channels[22])
#define FAST_PWM_ON                              (channels[23])
#define FAST_PWM_PERCENT                         (channels[24])
#define SP_GEN_1_OUTPUT                          (channels[25])
#define LAST_COMMAND_ID                          (channels[26])
#define LAST_COMMAND_VALUE                       (channels[27])
#define LAST_COMMAND_FROM_ARRAY_VALUE            (channels[28])
#define DEBUG_TIMER                              (channels[29])
#define SEND_TIMER                               (channels[30])
#define RECEIVE_TIMER                            (channels[31])

// all available parameters
// Define names for parameters, that can be set from the connected pc.
// These names are referred to in the whole code.
// The list is generated automatically from a python script.
// On the controller all values are stored in "float parameters[AVAILABLE_PARAMETER_COUNT]."
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
#define SP_GEN2_DIRAC_START_TIME                 (parameters[39])
#define SP_GEN2_DIRAC_NOW                        (parameters[40])
#define SP_GEN2_DIRAC_LOW                        (parameters[41])
#define SP_GEN2_DIRAC_HIGH                       (parameters[42])
#define SP_GEN2_DIRAC_DURATION                   (parameters[43])
#define SP_GEN2_STEP_LOW                         (parameters[44])
#define SP_GEN2_STEP_HIGH                        (parameters[45])
#define SP_GEN2_STEP_STATE                       (parameters[46])
#define SP_GEN2_SIN_AMPLITUDE                    (parameters[47])
#define SP_GEN2_SIN_OMEGA                        (parameters[48])
#define SP_GEN2_SIN_OFFSET                       (parameters[49])
#define SP_GEN2_SQUARE_LOW                       (parameters[50])
#define SP_GEN2_SQUARE_HIGH                      (parameters[51])
#define SP_GEN2_SQUARE_FREQUENCY                 (parameters[52])
#define SP_GEN2_SQUARE_STATE                     (parameters[53])
#define SP_GEN2_SQUARE_LAST_TOGGLE               (parameters[54])
#define SP_GEN2_RAMP_START_TIME                  (parameters[55])
#define SP_GEN2_RAMP_STATE                       (parameters[56])
#define SP_GEN2_RAMP_LAST_STATE                  (parameters[57])
#define SP_GEN2_RAMP_GRADIENT                    (parameters[58])
#define SP_GEN2_RAMP_LOW                         (parameters[59])
#define SP_GEN2_RAMP_HIGH                        (parameters[60])
#define PID1_SENSOR_SOURCE                       (parameters[61])

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

#endif