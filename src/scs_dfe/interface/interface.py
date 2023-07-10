"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract system interface
"""

from abc import ABC, abstractmethod

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib


# --------------------------------------------------------------------------------------------------------------------

class Interface(ABC):
    """
    classdocs
    """


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def _gas_sensors(cls, host):
        afe_calib = AFECalib.load(host)

        if afe_calib is None:
            return []

        afe_baseline = AFEBaseline.load(host, skeleton=True)
        sensors = afe_calib.sensors(afe_baseline)

        return sensors


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def status(self):
        pass


    @abstractmethod
    def null_datum(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def gas_sensor_interface(self, host):
        pass


    @abstractmethod
    def pt1000(self, host):
        pass


    @abstractmethod
    def pt1000_adc(self, gain, rate):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def led(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def power_gases(self, on):                  # switches digital component only
        pass


    @abstractmethod
    def power_gps(self, on):
        pass


    @abstractmethod
    def power_modem(self, on):
        pass


    @abstractmethod
    def power_ndir(self, on):
        pass


    @abstractmethod
    def power_opc(self, on):
        pass
