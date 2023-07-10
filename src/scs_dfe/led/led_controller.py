"""
Created on 30 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.led.led_state import LEDState
from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

class LEDController(SynchronisedProcess):
    """
    classdocs
    """

    __STATE0_PERIOD =   0.7             # seconds - short period
    __STATE1_PERIOD =   0.3             # seconds - long period

    __WAIT_FOR_STOP =   2.0             # seconds


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, led):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__led = led


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def stop(self):
        try:
            time.sleep(self.__WAIT_FOR_STOP)

            super().stop()                          # allow time for the sub-process to complete its last task

            self.__led.colour = 'A'                 # set default mode on stop

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    def run(self):
        try:
            timer = IntervalTimer(self.__STATE0_PERIOD + self.__STATE1_PERIOD)

            while timer.true():
                # values...
                with self._lock:
                    state = LEDState.construct_from_jdict(OrderedDict(self._value))

                if state is None or not state.is_valid():
                    continue

                # state 0 (short)...
                if state.colour0 != self.__led.colour:
                    self.__led.colour = state.colour0

                time.sleep(self.__STATE0_PERIOD)

                # state 1 (long)...
                if state.colour1 != self.__led.colour:
                    self.__led.colour = state.colour1

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # setter for client process...

    def set_state(self, state):
        with self._lock:
            state.as_list(self._value)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LEDController:{value:%s, led:%s}" % (self._value, self.__led)
