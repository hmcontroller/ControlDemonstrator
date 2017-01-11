#ifndef CONFIG_H
#define CONFIG_H

// must have parameters
#define LOOP_CYCLE_TIME_US                        10000
#define SENSOR_COUNT                                  4
#define REQUESTED_SENSOR_COUNT                        3
#define FAST_PARAMETER_COUNT                         19
#define REQUESTED_FAST_PARAMETER_COUNT                6
#define CONTROLLED_PARAMETER_COUNT                   23
#define REQUESTED_CONTROLLED_PARAMETER_COUNT         22

// all available fast parameters
// define names for parameters, that can be send to the connected pc.
// These names are referred to in the whole code.
// The list is generated automatically from a python script
// On the controller all values are stored in "float fastParams[FAST_PARAMETER_COUNT]"
#define PID1_ERROR                                    0
#define PID1_P_PORTION                                1
#define PID1_INTEGRAL                                 2
#define PID1_I_PORTION                                3
#define PID1_LAST_ERROR                               4
#define PID1_INTERVAL_LENGTH                          5
#define PID1_D_PORTION                                6
#define PID1_SET_POINT                                7
#define PID2_ERROR                                    8
#define PID2_P_PORTION                                9
#define PID2_INTEGRAL                                10
#define PID2_I_PORTION                               11
#define PID2_LAST_ERROR                              12
#define PID2_INTERVAL_LENGTH                         13
#define PID2_SET_POINT                               14
#define LOOP_DURATION                                15
#define RECEIVED_BYTES_COUNT                         16
#define FAST_PWM_ON                                  17
#define FAST_PWM_PERCENT                             18

// all available controlled parameters
// define names for parameters, that can be set from the connected pc.
// These names are referred to in the whole code.
// The list is generated automatically from a python script
// On the controller all values are stored in "float controlledParams[CONTROLLED_PARAMETER_COUNT]"
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
#define SP_GEN1_STEP_NOW                             13
#define SP_GEN1_STEP_LOW                             14
#define SP_GEN1_STEP_HIGH                            15
#define SP_GEN1_STEP_STATE                           16
#define SP_GEN1_DIRAC_NOW                            17
#define SP_GEN1_DIRAC_LOW                            18
#define SP_GEN1_DIRAC_HIGH                           19
#define SP_GEN1_DIRAC_DURATION                       20
#define SLOW_PWM_ON                                  21
#define SLOW_PWM_PERCENT                             22

// sensor channels, that will be measured
// [0]: switchCase for aquisition method, see "void aquireSensordata()"
// [1]: a parameter for the aquistion method
// [2]: storage destination (also used for messageOut position)
// if storage destination is <0, the channel will not be send to the pc
int sensorMapping[SENSOR_COUNT][3] = 
{{1, 0, 1}, {1, 1, 1}, {1, 2, 0}, {1, 3, 1}};

// parameters that will be send to the pc at every loop cycle
int requestedFastParameters[REQUESTED_FAST_PARAMETER_COUNT] = {
    PID1_SET_POINT,
    PID1_P_PORTION,
    FAST_PWM_ON,
    FAST_PWM_PERCENT,
    LOOP_DURATION,
    RECEIVED_BYTES_COUNT
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
    PID2_KD_SWITCH,
    PID2_KD_VALUE,
    SP_GEN1_NUMBER,
    SP_GEN1_STEP_NOW,
    SP_GEN1_STEP_STATE,
    SP_GEN1_STEP_LOW,
    SP_GEN1_STEP_HIGH,
    SP_GEN1_DIRAC_NOW,
    SP_GEN1_DIRAC_LOW,
    SP_GEN1_DIRAC_HIGH,
    SP_GEN1_DIRAC_DURATION,
    SLOW_PWM_ON,
    SLOW_PWM_PERCENT
};

#endif