"""
Created on 23 Jan 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from abc import ABC, abstractmethod

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class OPC(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def source(cls):
        pass


    @classmethod
    @abstractmethod
    def uses_spi(cls):
        pass


    @classmethod
    @abstractmethod
    def datum_class(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def lock_timeout(cls):
        pass


    @classmethod
    @abstractmethod
    def boot_time(cls):
        pass


    @classmethod
    @abstractmethod
    def power_cycle_time(cls):
        pass


    @classmethod
    @abstractmethod
    def max_permitted_zero_readings(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface):
        """
        Constructor
        """
        self.__interface = interface


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        self.__interface.power_opc(True)
        self._set_spi_mode_always_on()

        time.sleep(self.boot_time())


    def power_off(self):
        self._set_spi_mode_auto_enabled()
        self.__interface.power_opc(False)


    # ----------------------------------------------------------------------------------------------------------------

    def _set_spi_mode_always_on(self):            # should be used immediately after turning on the OPC power
        pass                                      # (BeagleBone only)


    def _set_spi_mode_auto_enabled(self):         # should be used immediately before turning off the OPC power
        pass                                      # (BeagleBone only)


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def operations_on(self):
        pass


    @abstractmethod
    def operations_off(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def clean(self):
        pass


    @property
    @abstractmethod
    def cleaning_interval(self):
        pass


    @cleaning_interval.setter
    @abstractmethod
    def cleaning_interval(self, interval):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def data_ready(self):
        pass


    @abstractmethod
    def sample(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def serial_no(self):
        pass


    @abstractmethod
    def firmware(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def get_firmware_conf(self):
        pass


    @abstractmethod
    def set_firmware_conf(self, jdict):
        pass


    @abstractmethod
    def commit_firmware_conf(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interface(self):
        return self.__interface


    @property
    @abstractmethod
    def dev_path(self):
        pass


    @property
    @abstractmethod
    def bus(self):
        pass


    @property
    @abstractmethod
    def address(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.lock_name, self.lock_timeout())


    def release_lock(self):
        Lock.release(self.lock_name)


    @property
    @abstractmethod
    def lock_name(self):
        pass
