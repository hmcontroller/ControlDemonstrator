#ifndef CONFIG_H
#define CONFIG_H

// must have parameters
#define LOOP_CYCLE_TIME_US                         5000
#define FAST_PARAMETER_COUNT                         30
#define REQUESTED_FAST_PARAMETER_COUNT               12
#define CONTROLLED_PARAMETER_COUNT                   40
#define REQUESTED_CONTROLLED_PARAMETER_COUNT         40

// all available fast parameters
// define names for parameters, that can be send to the connected pc.
// These names are referred to in the whole code.
// The list is generated automatically from a python script
// On the controller all values are stored in "float fastParameterValues[FAST_PARAMETER_COUNT]"
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

// all available controlled parameters
// define names for parameters, that can be set from the connected pc.
// These names are referred to in the whole code.
// The list is generated automatically from a python script
// On the controller all values are stored in "float controlledParameterValues[CONTROLLED_PARAMETER_COUNT]"
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
#define SLOW_PWM_ON                                  24
#define SLOW_PWM_PERCENT                             25
#define SP_GEN2_ON                                   26
#define SP_GEN2_NUMBER                               27
#define SP_GEN2_DIRAC_START_TIME                     28
#define SP_GEN2_DIRAC_NOW                            29
#define SP_GEN2_DIRAC_LOW                            30
#define SP_GEN2_DIRAC_HIGH                           31
#define SP_GEN2_DIRAC_DURATION                       32
#define SP_GEN2_STEP_LOW                             33
#define SP_GEN2_STEP_HIGH                            34
#define SP_GEN2_STEP_STATE                           35
#define SP_GEN2_SIN_AMPLITUDE                        36
#define SP_GEN2_SIN_OMEGA                            37
#define SP_GEN2_SIN_OFFSET                           38
#define PID1_SENSOR_SOURCE                           39

// parameters that will be send to the pc at every loop cycle
int requestedFastParameters[REQUESTED_FAST_PARAMETER_COUNT] = {
    ANALOG_IN_2,
    ANALOG_IN_3,
    PID1_ERROR,
    FAST_PWM_ON,
    FAST_PWM_PERCENT,
    LOOP_DURATION,
    RECEIVED_BYTES_COUNT,
    SP_GEN_1_OUTPUT,
    LAST_COMMAND_ID,
    LAST_COMMAND_VALUE,
    LAST_COMMAND_FROM_ARRAY_VALUE,
    DEBUG_TIMER
};

// parameters that will be set from the pc
int requestedControlledParameters[CONTROLLED_PARAMETER_COUNT] = {
    PID1_KP_SWITCH,
    PID1_KP_VALUE,
    PID1_KI_SWITCH,
    PID1_KI_VALUE,
    PID1_KD_SWITCH,
    PID1_KD_VALUE,
    PID2_KP_SWITCH,
    PID2_KP_VALUE,
    PID2_KI_SWITCH,
    PID2_KI_VALUE,
    PID2_KD_SWITCH,
    PID2_KD_VALUE,
    SP_GEN1_NUMBER,
    SP_GEN1_DIRAC_START_TIME,
    SP_GEN1_DIRAC_NOW,
    SP_GEN1_DIRAC_LOW,
    SP_GEN1_DIRAC_HIGH,
    SP_GEN1_DIRAC_DURATION,
    SP_GEN1_STEP_LOW,
    SP_GEN1_STEP_HIGH,
    SP_GEN1_STEP_STATE,
    SP_GEN1_SIN_AMPLITUDE,
    SP_GEN1_SIN_OMEGA,
    SP_GEN1_SIN_OFFSET,
    SLOW_PWM_ON,
    SLOW_PWM_PERCENT,
    SP_GEN2_ON,
    SP_GEN2_NUMBER,
    SP_GEN2_DIRAC_START_TIME,
    SP_GEN2_DIRAC_NOW,
    SP_GEN2_DIRAC_LOW,
    SP_GEN2_DIRAC_HIGH,
    SP_GEN2_DIRAC_DURATION,
    SP_GEN2_STEP_LOW,
    SP_GEN2_STEP_HIGH,
    SP_GEN2_STEP_STATE,
    SP_GEN2_SIN_AMPLITUDE,
    SP_GEN2_SIN_OMEGA,
    SP_GEN2_SIN_OFFSET,
    PID1_SENSOR_SOURCE
};

#endif