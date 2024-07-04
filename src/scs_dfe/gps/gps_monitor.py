"""
Created on 25 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.data.average import Average

from scs_core.position.gps_datum import GPSDatum
from scs_core.position.nmea.gpgga import GPGGA

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_core.sys.filesystem import Filesystem
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class GPSMonitor(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, gps, conf):
        return cls(gps, conf.sample_interval, Average(conf.tally), conf.report_file(Host), conf.debug)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gps, sample_interval, averaging, report_file, debug):
        """
        Constructor
        """
        self.__logger = Logging.getLogger()
        self.__logging_specification = Logging.specification()

        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__gps = gps                                            # GPS

        self.__sample_interval = int(sample_interval)               # int seconds
        self.__averaging = averaging                                # Average
        self.__report_file = report_file                            # string

        self.__debug = bool(debug)                                  # bool


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def start(self):
        try:
            self.__gps.power_on()
            self.__gps.open()

            self.__averaging.reset()

            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            super().stop()

            self.__gps.close()
            Filesystem.rm(self.__report_file)

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    def run(self):
        Logging.replicate(self.__logging_specification)

        # default report...
        datum = GPSDatum.null_datum()

        with self._lock:
            datum.as_list(self._value)

        # sample...
        try:
            timer = IntervalTimer(self.__sample_interval)

            while timer.true():
                # position...
                gga = self.__gps.report(GPGGA)

                if self.__debug:
                    print("GPSMonitor - gga: %s" % gga, file=sys.stderr)
                    sys.stderr.flush()

                datum = GPSDatum.construct_from_gga(gga)

                if datum is None:
                    datum = GPSDatum.null_datum()           # loss of contact with receiver = quality null

                datum.save(self.__report_file)

                # average...
                if datum.quality:
                    self.__averaging.append(datum)          # only append valid positional fixes

                report = self.__averaging.mid()

                if report is None:
                    report = datum                          # provide current datum when there is no average

                report.quality = datum.quality              # quality is current quality, not average quality

                # report...
                with self._lock:
                    report.as_list(self._value)

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # data retrieval for client process...

    def sample(self):
        with self._lock:
            datum = GPSDatum.construct_from_jdict(OrderedDict(self._value))

        return datum


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSMonitor:{value:%s, sample_interval:%s, averaging:%s, gps:%s, report_file:%s, debug:%s}" % \
               (self._value, self.__sample_interval, self.__averaging, self.__gps, self.__report_file, self.__debug)
