"""
Created on 2 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from abc import ABC, abstractmethod

from scs_core.sys.logging import Logging

from scs_host.sys.host_serial import HostSerial


# --------------------------------------------------------------------------------------------------------------------

class GPS(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def baud_rate(cls):
        pass


    @classmethod
    @abstractmethod
    def boot_time(cls):
        pass


    @classmethod
    @abstractmethod
    def serial_lock_timeout(cls):
        pass


    @classmethod
    @abstractmethod
    def serial_comms_timeout(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, uart):
        """
        Constructor
        """
        self.__interface = interface

        self._serial = HostSerial(uart, self.baud_rate())
        self._logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        self.__interface.power_gps(True)
        time.sleep(self.boot_time())


    def power_off(self):
        self.__interface.power_gps(False)


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        self._serial.open(self.serial_lock_timeout(), self.serial_comms_timeout())


    def close(self):
        self._serial.close()


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def report(self, message_class):
        pass


    @abstractmethod
    def report_all(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{interface:%s, serial:%s}" % \
               (self.__interface, self._serial)

