# -*- encoding: utf-8 -*-

from PyQt4 import QtCore

from core.model.commState import CommState

class CommStateMachine(QtCore.QObject):

    # possible transitions
    CONNECTION_LOST = 0
    CONNECTION_ESTABLISHED = 1
    MALFORMED_DATA_RECEIVED = 2
    WELL_FORMED_DATA_RECEIVED = 3
    CONNECTION_TIMED_OUT = 4
    RECORDING_TRANSMISSION_COMPLETE = 5

    PLAY_MODE_ENABLED = 10
    PLAY_MODE_DISABLED = 11
    DEBUG_MODE_ENABLED = 12
    DEBUG_MODE_DISABLED = 13
    RECORD_MODE_ENABLED = 14
    RECORD_MODE_DISABLED = 15



    def __init__(self, state):
        super(CommStateMachine, self).__init__()

        self.state = state


    def doTransit(self, transition):

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if self.state.state == CommState.UNKNOWN:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


            if transition == self.CONNECTION_LOST:
                self.state.state = CommState.NO_CONN

            elif transition == self.CONNECTION_ESTABLISHED:
                self.state.state = CommState.COMM_OK

            elif transition == self.MALFORMED_DATA_RECEIVED:
                self.state.state = CommState.WRONG_CONFIG

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                self.state.state = CommState.COMM_OK

            elif transition == self.CONNECTION_TIMED_OUT:
                self.state.state = CommState.COMM_TIMEOUT

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                self.state.state = CommState.PAUSE

            elif transition == self.PLAY_MODE_ENABLED:
                self.state.state = CommState.COMM_OK

            elif transition == self.PLAY_MODE_DISABLED:
                self.state.state = CommState.PAUSE

            elif transition == self.DEBUG_MODE_ENABLED:
                self.state.state = CommState.DEBUG

            elif transition == self.DEBUG_MODE_DISABLED:
                self.state.state = CommState.COMM_OK

            elif transition == self.RECORD_MODE_ENABLED:
                self.state.state = CommState.RECORD

            elif transition == self.RECORD_MODE_DISABLED:
                self.state.state = CommState.COMM_OK




        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif self.state.state == CommState.COMM_OK:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            if transition == self.CONNECTION_LOST:
                self.state.state = CommState.NO_CONN

            elif transition == self.CONNECTION_ESTABLISHED:
                pass

            elif transition == self.MALFORMED_DATA_RECEIVED:
                self.state.state = CommState.WRONG_CONFIG

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                pass

            elif transition == self.CONNECTION_TIMED_OUT:
                self.state.state = CommState.COMM_TIMEOUT

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                self.state.state = CommState.PAUSE

            elif transition == self.PLAY_MODE_ENABLED:
                self.state.state = CommState.PLAY

            elif transition == self.PLAY_MODE_DISABLED:
                self.state.state = CommState.PAUSE

            elif transition == self.DEBUG_MODE_ENABLED:
                self.state.state = CommState.DEBUG

            elif transition == self.DEBUG_MODE_DISABLED:
                self.state.state = CommState.PLAY

            elif transition == self.RECORD_MODE_ENABLED:
                self.state.state = CommState.RECORD

            elif transition == self.RECORD_MODE_DISABLED:
                self.state.state = CommState.PLAY

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif self.state.state == CommState.WRONG_CONFIG:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            if transition == self.CONNECTION_LOST:
                self.state.state = CommState.NO_CONN

            elif transition == self.CONNECTION_ESTABLISHED:
                self.state.state = CommState.COMM_OK

            elif transition == self.MALFORMED_DATA_RECEIVED:
                pass

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                self.state.state = CommState.COMM_OK

            elif transition == self.CONNECTION_TIMED_OUT:
                pass

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                pass

            elif transition == self.PLAY_MODE_ENABLED:
                self.state.state = CommState.PLAY

            elif transition == self.PLAY_MODE_DISABLED:
                self.state.state = CommState.PAUSE

            elif transition == self.DEBUG_MODE_ENABLED:
                self.state.state = CommState.DEBUG

            elif transition == self.DEBUG_MODE_DISABLED:
                self.state.state = CommState.PLAY

            elif transition == self.RECORD_MODE_ENABLED:
                self.state.state = CommState.RECORD

            elif transition == self.RECORD_MODE_DISABLED:
                self.state.state = CommState.PLAY



        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif self.state.state == CommState.NO_CONN:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


            if transition == self.CONNECTION_LOST:
                pass

            elif transition == self.CONNECTION_ESTABLISHED:
                self.state.state = CommState.COMM_OK

            elif transition == self.MALFORMED_DATA_RECEIVED:
                self.state.state = CommState.WRONG_CONFIG

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                self.state.state = CommState.COMM_OK

            elif transition == self.CONNECTION_TIMED_OUT:
                pass

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                self.state.state = CommState.PAUSE

            elif transition == self.PLAY_MODE_ENABLED:
                self.state.state = CommState.PLAY

            elif transition == self.PLAY_MODE_DISABLED:
                self.state.state = CommState.PAUSE

            elif transition == self.DEBUG_MODE_ENABLED:
                self.state.state = CommState.DEBUG

            elif transition == self.DEBUG_MODE_DISABLED:
                self.state.state = CommState.PLAY

            elif transition == self.RECORD_MODE_ENABLED:
                self.state.state = CommState.RECORD

            elif transition == self.RECORD_MODE_DISABLED:
                self.state.state = CommState.PLAY




        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif self.state.state == CommState.COMM_TIMEOUT:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            if transition == self.CONNECTION_LOST:
                self.state.state = CommState.NO_CONN

            elif transition == self.CONNECTION_ESTABLISHED:
                self.state.state = CommState.COMM_OK

            elif transition == self.MALFORMED_DATA_RECEIVED:
                self.state.state = CommState.WRONG_CONFIG

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                self.state.state = CommState.COMM_OK

            elif transition == self.CONNECTION_TIMED_OUT:
                pass

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                self.state.state = CommState.PAUSE

            elif transition == self.PLAY_MODE_ENABLED:
                self.state.state = CommState.PLAY

            elif transition == self.PLAY_MODE_DISABLED:
                self.state.state = CommState.PAUSE

            elif transition == self.DEBUG_MODE_ENABLED:
                self.state.state = CommState.DEBUG

            elif transition == self.DEBUG_MODE_DISABLED:
                self.state.state = CommState.PLAY

            elif transition == self.RECORD_MODE_ENABLED:
                self.state.state = CommState.RECORD

            elif transition == self.RECORD_MODE_DISABLED:
                self.state.state = CommState.PLAY






        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif self.state.state == CommState.PLAY:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            if transition == self.CONNECTION_LOST:
                self.state.state = CommState.NO_CONN

            elif transition == self.CONNECTION_ESTABLISHED:
                self.state.state = CommState.COMM_OK

            elif transition == self.MALFORMED_DATA_RECEIVED:
                self.state.state = CommState.WRONG_CONFIG

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                self.state.state = CommState.COMM_OK

            elif transition == self.CONNECTION_TIMED_OUT:
                self.state.state = CommState.COMM_TIMEOUT

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                self.state.state = CommState.PAUSE

            elif transition == self.PLAY_MODE_ENABLED:
                self.state.state = CommState.PLAY

            elif transition == self.PLAY_MODE_DISABLED:
                self.state.state = CommState.PAUSE

            elif transition == self.DEBUG_MODE_ENABLED:
                self.state.state = CommState.DEBUG

            elif transition == self.DEBUG_MODE_DISABLED:
                self.state.state = CommState.PLAY

            elif transition == self.RECORD_MODE_ENABLED:
                self.state.state = CommState.RECORD

            elif transition == self.RECORD_MODE_DISABLED:
                self.state.state = CommState.PLAY





        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif self.state.state == CommState.PAUSE:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            if transition == self.CONNECTION_LOST:
                pass

            elif transition == self.CONNECTION_ESTABLISHED:
                pass

            elif transition == self.MALFORMED_DATA_RECEIVED:
                pass

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                pass

            elif transition == self.CONNECTION_TIMED_OUT:
                pass

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                pass

            elif transition == self.PLAY_MODE_ENABLED:
                self.state.state = CommState.PLAY

            elif transition == self.PLAY_MODE_DISABLED:
                pass

            elif transition == self.DEBUG_MODE_ENABLED:
                self.state.state = CommState.DEBUG

            elif transition == self.DEBUG_MODE_DISABLED:
                pass

            elif transition == self.RECORD_MODE_ENABLED:
                self.state.state = CommState.RECORD

            elif transition == self.RECORD_MODE_DISABLED:
                pass







        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif self.state.state == CommState.DEBUG:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


            if transition == self.CONNECTION_LOST:
                pass

            elif transition == self.CONNECTION_ESTABLISHED:
                pass

            elif transition == self.MALFORMED_DATA_RECEIVED:
                pass

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                pass

            elif transition == self.CONNECTION_TIMED_OUT:
                pass

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                pass

            elif transition == self.PLAY_MODE_ENABLED:
                pass

            elif transition == self.PLAY_MODE_DISABLED:
                pass

            elif transition == self.DEBUG_MODE_ENABLED:
                pass

            elif transition == self.DEBUG_MODE_DISABLED:
                self.state.state = CommState.PLAY

            elif transition == self.RECORD_MODE_ENABLED:
                pass

            elif transition == self.RECORD_MODE_DISABLED:
                pass






        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif self.state.state == CommState.RECORD:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


            if transition == self.CONNECTION_LOST:
                self.state.state = CommState.NO_CONN

            elif transition == self.CONNECTION_ESTABLISHED:
                self.state.state = CommState.COMM_OK

            elif transition == self.MALFORMED_DATA_RECEIVED:
                self.state.state = CommState.WRONG_CONFIG

            elif transition == self.WELL_FORMED_DATA_RECEIVED:
                pass

            elif transition == self.CONNECTION_TIMED_OUT:
                pass

            elif transition == self.RECORDING_TRANSMISSION_COMPLETE:
                self.state.state = CommState.PAUSE

            elif transition == self.PLAY_MODE_ENABLED:
                self.state.state = CommState.PLAY

            elif transition == self.PLAY_MODE_DISABLED:
                self.state.state = CommState.PAUSE

            elif transition == self.DEBUG_MODE_ENABLED:
                self.state.state = CommState.DEBUG

            elif transition == self.DEBUG_MODE_DISABLED:
                self.state.state = CommState.PLAY

            elif transition == self.RECORD_MODE_ENABLED:
                pass

            elif transition == self.RECORD_MODE_DISABLED:
                self.state.state = CommState.PLAY



    # def connectionLost(self):
    #     if self.state.state = CommState.UNKNOWN:
    #         pass
    #     elif self.state.state = CommState.COMM_OK:
    #         pass
    #     elif self.state.state = CommState.COMM_PAUSED:
    #         pass
    #     elif self.state.state = CommState.COMM_TIMEOUT:
    #         pass
    #     elif self.state.state = CommState.WRONG_CONFIG:
    #         pass
    #     elif self.state.state = CommState.NO_CONN:
    #         pass
    #     elif self.state.state = CommState.DEBUG:
    #         pass
    #     elif self.state.state = CommState.RECORD:
    #         pass
