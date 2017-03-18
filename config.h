#ifndef CONFIG_H
#define CONFIG_H

// must have parameters
#define LOOP_CYCLE_TIME_US                         5000
#define AVAILABLE_CHANNEL_COUNT                      32
#define REQUESTED_CHANNEL_COUNT                       9
#define AVAILABLE_PARAMETER_COUNT                    62
#define REQUESTED_PARAMETER_COUNT                    56

// All available channels
// Define names for parameters, that can be send to the connected pc.
// These names are referred to in the whole code.
// The list is generated automatically from a python script.
// On the controller all values are stored in "float channels[AVAILABLE_CHANNEL_COUNT]."
#define ANALOG_IN_0                                   0
#define ANALOG_IN_1                                   1
#define ANALOG_IN_2                                   2
#define ANALOG_IN_3                                   3
#define ANALOG_IN_4                                   4
#define ANALOG_IN_5                                   5
#define PID1_ERROR                                    6
#define PID1_P_PORTION                                7
#define PID1_INTEGRAL                                 8
#define PID1_I_PORTION                                9
#define PID1_LAST_ERROR                              10
#define PID1_INTERVAL_LENGTH                         11
#define PID1_D_PORTION                               12
#define PID1_SET_POINT                               13
#define PID2_ERROR                                   14
#define PID2_P_PORTION                               15
#define PID2_INTEGRAL                                16
#define PID2_I_PORTION                               17
#define PID2_LAST_ERROR                              18
#define PID2_INTERVAL_LENGTH                         19
#define PID2_SET_POINT                               20
#define LOOP_DURATION                                21
#define RECEIVED_BYTES_COUNT                         22
#define FAST_PWM_ON                                  23
#define FAST_PWM_PERCENT                             24
#define SP_GEN_1_OUTPUT                              25
#define LAST_COMMAND_ID                              26
#define LAST_COMMAND_VALUE                           27
#define LAST_COMMAND_FROM_ARRAY_VALUE                28
#define DEBUG_TIMER                                  29
#define SEND_TIMER                                   30
#define RECEIVE_TIMER                                31

// all available parameters
// Define names for parameters, that can be set from the connected pc.
// These names are referred to in the whole code.
// The list is generated automatically from a python script.
// On the controller all values are stored in "float parameters[AVAILABLE_PARAMETER_COUNT]."
#define PID1_KP_SWITCH                                0
#define PID1_KP_VALUE                                 1
#define PID1_KI_SWITCH                                2
#define PID1_KI_VALUE                                 3
#define PID1_KD_SWITCH                                4
#define PID1_KD_VALUE                                 5
#define PID2_KP_SWITCH                                6
#define PID2_KP_VALUE                                 7
#define PID2_KI_SWITCH                                8
#define PID2_KI_VALUE                                 9
#define PID2_KD_SWITCH                               10
#define PID2_KD_VALUE                                11
#define SP_GEN1_NUMBER                               12
#define SP_GEN1_DIRAC_START_TIME                     13
#define SP_GEN1_DIRAC_NOW                            14
#define SP_GEN1_DIRAC_LOW                            15
#define SP_GEN1_DIRAC_HIGH                           16
#define SP_GEN1_DIRAC_DURATION                       17
#define SP_GEN1_STEP_LOW                             18
#define SP_GEN1_STEP_HIGH                            19
#define SP_GEN1_STEP_STATE                           20
#define SP_GEN1_SIN_AMPLITUDE                        21
#define SP_GEN1_SIN_OMEGA                            22
#define SP_GEN1_SIN_OFFSET                           23
#define SP_GEN1_SQUARE_LOW                           24
#define SP_GEN1_SQUARE_HIGH                          25
#define SP_GEN1_SQUARE_FREQUENCY                     26
#define SP_GEN1_SQUARE_STATE                         27
#define SP_GEN1_SQUARE_LAST_TOGGLE                   28
#define SP_GEN1_RAMP_START_TIME                      29
#define SP_GEN1_RAMP_STATE                           30
#define SP_GEN1_RAMP_LAST_STATE                      31
#define SP_GEN1_RAMP_GRADIENT                        32
#define SP_GEN1_RAMP_LOW                             33
#define SP_GEN1_RAMP_HIGH                            34
#define SLOW_PWM_ON                                  35
#define SLOW_PWM_PERCENT                             36
#define SP_GEN2_ON                                   37
#define SP_GEN2_NUMBER                               38
#define SP_GEN2_DIRAC_START_TIME                     39
#define SP_GEN2_DIRAC_NOW                            40
#define SP_GEN2_DIRAC_LOW                            41
#define SP_GEN2_DIRAC_HIGH                           42
#define SP_GEN2_DIRAC_DURATION                       43
#define SP_GEN2_STEP_LOW                             44
#define SP_GEN2_STEP_HIGH                            45
#define SP_GEN2_STEP_STATE                           46
#define SP_GEN2_SIN_AMPLITUDE                        47
#define SP_GEN2_SIN_OMEGA                            48
#define SP_GEN2_SIN_OFFSET                           49
#define SP_GEN2_SQUARE_LOW                           50
#define SP_GEN2_SQUARE_HIGH                          51
#define SP_GEN2_SQUARE_FREQUENCY                     52
#define SP_GEN2_SQUARE_STATE                         53
#define SP_GEN2_SQUARE_LAST_TOGGLE                   54
#define SP_GEN2_RAMP_START_TIME                      55
#define SP_GEN2_RAMP_STATE                           56
#define SP_GEN2_RAMP_LAST_STATE                      57
#define SP_GEN2_RAMP_GRADIENT                        58
#define SP_GEN2_RAMP_LOW                             59
#define SP_GEN2_RAMP_HIGH                            60
#define PID1_SENSOR_SOURCE                           61

extern int requestedChannels[REQUESTED_CHANNEL_COUNT];
extern int requestedParameters[REQUESTED_PARAMETER_COUNT];
#endif