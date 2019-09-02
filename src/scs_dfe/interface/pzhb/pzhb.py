"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A Pi Zero Header Breakout sensor interface
"""

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib

from scs_dfe.gas.iei import IEI

from scs_dfe.interface.interface import Interface


# --------------------------------------------------------------------------------------------------------------------

class PZHB(Interface):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mcu):
        """
        Constructor
        """
        self.__mcu = mcu                            # PZHBMCU


    # ----------------------------------------------------------------------------------------------------------------

    def temp(self):
        return None


    def null_datum(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def gas_sensors(self, host):
        # sensors...
        afe_calib = AFECalib.load(host)
        afe_baseline = AFEBaseline.load(host)

        sensors = afe_calib.sensors(afe_baseline)

        return IEI(sensors)


    def pt1000(self, host):
        return None


    def pt1000_adc(self, gain, rate):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def led(self):
        return self.__mcu.led()


    def power_gases(self, enable):
        return self.__mcu.power_gases(enable)


    def power_gps(self, enable):
        return self.__mcu.power_gps(enable)


    def power_modem(self, enable):
        return self.__mcu.power_modem(enable)


    def power_ndir(self, enable):
        return self.__mcu.power_ndir(enable)


    def power_opc(self, enable):
        return self.__mcu.power_opc(enable)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PZHB:{mcu:%s}" % self.__mcu
