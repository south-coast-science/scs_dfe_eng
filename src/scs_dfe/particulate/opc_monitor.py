"""
Created on 9 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.particulate.opc_datum import OPCDatum

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess


# TODO: power cycle OPC if all zeros / nulls returned

# TODO: should be able to start and stop the OPC on very long sampling intervals

# TODO: add power cycle monitor - check for all 0

# --------------------------------------------------------------------------------------------------------------------

class OPCMonitor(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, opc, conf):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__opc = opc
        self.__conf = conf


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        self.__opc.sample()     # reset counts

        try:
            timer = IntervalTimer(self.__conf.sample_period)

            while timer.true():
                datum = self.__opc.sample()

                with self._lock:
                    datum.as_list(self._value)

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        with self._lock:
            value = self._value

        print("opc sample value: %s" % value)

        return OPCDatum.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            self.__opc.power_on()
            self.__opc.operations_on()

            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            super().stop()

            self.__opc.operations_off()
            self.__opc.power_off()

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCMonitor:{sample:%s, opc:%s, conf:%s}" % (self.sample(), self.__opc, self.__conf)
