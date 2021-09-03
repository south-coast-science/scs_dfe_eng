"""
Created on 9 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import copy
import sys
import time

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_dfe.particulate.opc import OPC

from scs_host.lock.lock_timeout import LockTimeout


# --------------------------------------------------------------------------------------------------------------------

class OPCMonitor(SynchronisedProcess):
    """
    classdocs
    """
    __FATAL_ERROR =                     -1


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, opc: OPC, conf):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__opc = opc
        self.__conf = conf

        self.__first_reading = True
        self.__zero_count = 0
        self.__datum_class = self.__opc.datum_class()


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def start(self):
        try:
            self.__opc.power_on()
            self.__opc.operations_on()

            self.__first_reading = True
            self.__zero_count = 0

            super().start()

        except (KeyboardInterrupt, SystemExit):
            pass


    def stop(self):
        try:
            super().stop()

            self.__opc.operations_off()
            self.__opc.power_off()

        except (KeyboardInterrupt, LockTimeout, OSError, SystemExit):
            pass


    def run(self):
        try:
            # clean...
            self.__opc.clean()

            # sample...
            timer = IntervalTimer(self.__conf.sample_period)

            self.__zero_count = 0
            max_permitted_zero_readings = self.__opc.max_permitted_zero_readings()

            while timer.true():
                try:
                    if not self.__opc.data_ready():
                        print("OPCMonitor.run: data not ready.", file=sys.stderr)
                        sys.stderr.flush()

                        self.__empty()
                        continue

                    datum = self.__opc.sample()

                    if self.__conf.restart_on_zeroes and datum.is_zero():
                        self.__zero_count += 1

                        if self.__zero_count > max_permitted_zero_readings:
                            raise ValueError("zero reading")

                        if not self.__first_reading:
                            print("OPCMonitor.run: zero reading %d of %d" %
                                  (self.__zero_count, max_permitted_zero_readings), file=sys.stderr)
                            sys.stderr.flush()

                    else:
                        self.__zero_count = 0

                    if not self.__first_reading:
                        with self._lock:
                            datum.as_list(self._value)

                except LockTimeout as ex:
                    print("OPCMonitor.run: %s" % ex, file=sys.stderr)
                    sys.stderr.flush()

                    self.__empty()

                except ValueError as ex:
                    print("OPCMonitor.run: %s" % ex, file=sys.stderr)
                    sys.stderr.flush()

                    self.__empty()
                    self.__power_cycle()

                except OSError as ex:
                    print("OPCMonitor.run: %s" % ex, file=sys.stderr)
                    sys.stderr.flush()

                    self.__error(self.__FATAL_ERROR)
                    break

                if self.__first_reading:
                    self.__first_reading = False

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess special operations...

    def __error(self, code):
        with self._lock:
            del self._value[:]
            self._value.append(code)


    def __empty(self):
        with self._lock:
            del self._value[:]


    def __power_cycle(self):
        print("OPCMonitor: power cycle", file=sys.stderr)
        sys.stderr.flush()

        # noinspection PyBroadException

        try:
            # off...
            self.__opc.operations_off()
            self.__opc.power_off()

            time.sleep(self.__opc.power_cycle_time())

            # on...
            self.__opc.power_on()
            self.__opc.operations_on()

            self.__first_reading = True
            self.__zero_count = 0

        except Exception:
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # data retrieval for client process...

    def operations_on(self):
        self.__opc.operations_on()


    def operations_off(self):
        self.__opc.operations_off()


    def firmware(self):
        return self.__opc.firmware()


    def sample(self):
        with self._lock:
            value = copy.deepcopy(self._value)

        if len(value) == 1 and value[0] == self.__FATAL_ERROR:
            raise StopIteration()

        return self.__datum_class.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def opc(self):
        return self.__opc


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCMonitor:{value:%s, opc:%s, conf:%s, first_reading:%s}" % \
               (self._value, self.__opc, self.__conf, self.__first_reading)
