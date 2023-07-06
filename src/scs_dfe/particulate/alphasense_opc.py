"""
Created on 2 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC
from subprocess import Popen

from scs_core.particulate.opc_datum import OPCDatum
from scs_core.sys.logging import Logging

from scs_dfe.particulate.opc import OPC

from scs_host.bus.spi import SPI


# TODO: fix lock_name()
# --------------------------------------------------------------------------------------------------------------------

class AlphasenseOPC(OPC, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def uses_spi(cls):
        return True


    @classmethod
    def datum_class(cls):
        return OPCDatum


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, dev_path, spi_mode, spi_clock):
        """
        Constructor
        """
        super().__init__(interface)

        self._spi = SPI(dev_path, spi_mode, spi_clock)
        self._logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def clean(self):
        pass


    @property
    def cleaning_interval(self):
        return None


    @cleaning_interval.setter
    def cleaning_interval(self, interval):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def data_ready(self):
        return True


    # ----------------------------------------------------------------------------------------------------------------

    def _set_spi_mode_always_on(self):              # should be used immediately after turning on the OPC power
        self.__set_device_mode('always-on')         # (BeagleBone only)


    def _set_spi_mode_auto_enabled(self):           # should be used immediately before turning off the OPC power
        self.__set_device_mode('auto-enabled')      # (BeagleBone only)


    def __set_device_mode(self, mode):
        try:
            self._logger.debug('set_device_mode: %s' % mode)
            p = Popen(['spi-pm-ctrl', '--path', self.dev_path, '--set-device-mode', mode])
            p.wait()

        except FileNotFoundError:
            self._logger.debug('set_device_mode: %s: spi-pm-ctrl not available' % mode)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dev_path(self):
        return self._spi.dev_path


    @property
    def bus(self):
        raise NotImplementedError


    @property
    def address(self):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lock_name(self):
        return self.__class__.__name__


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{interface:%s, spi:%s}" %  (self.interface, self._spi)
