"""
Created on 11 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

settings for OPCMonitor

example JSON:
{"model": "R1", "sample-period": 10, "power-saving": false, "spi-bus": 0, "spi-device": 0}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.particulate.opc_monitor import OPCMonitor

from scs_dfe.particulate.opc_n2.opc_n2 import OPCN2
from scs_dfe.particulate.opc_n3.opc_n3 import OPCN3
from scs_dfe.particulate.opc_r1.opc_r1 import OPCR1


# --------------------------------------------------------------------------------------------------------------------

class OPCConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "opc_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        model = jdict.get('model')
        sample_period = jdict.get('sample-period')
        power_saving = jdict.get('power-saving')

        spi_bus = jdict.get('spi-bus')
        spi_device = jdict.get('spi-device')

        return OPCConf(model, sample_period, power_saving, spi_bus, spi_device)


    @classmethod
    def is_valid_model(cls, model):
        return model in (OPCN2.SOURCE, OPCN3.SOURCE, OPCR1.SOURCE)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_period, power_saving, spi_bus, spi_device):
        """
        Constructor
        """
        super().__init__()

        self.__model = model
        self.__sample_period = int(sample_period)
        self.__power_saving = bool(power_saving)

        self.__spi_bus = spi_bus
        self.__spi_device = spi_device


    # ----------------------------------------------------------------------------------------------------------------

    def opc_monitor(self, host):
        opc = self.opc(host)

        return OPCMonitor(opc, self)


    def opc(self, host):
        if self.model == OPCN2.SOURCE:
            return OPCN2(self.opc_spi_bus(host), self.opc_spi_device(host))

        elif self.model == OPCN3.SOURCE:
            return OPCN3(self.opc_spi_bus(host), self.opc_spi_device(host))

        elif self.model == OPCR1.SOURCE:
            return OPCR1(self.opc_spi_bus(host), self.opc_spi_device(host))

        else:
            raise ValueError('unknown model: %s' % self.model)


    # ----------------------------------------------------------------------------------------------------------------

    def opc_spi_bus(self, host):
        try:
            return int(self.__spi_bus)

        except TypeError:
            return host.opc_spi_bus()


    def opc_spi_device(self, host):
        try:
            return int(self.__spi_device)

        except TypeError:
            return host.opc_spi_device()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def sample_period(self):
        return self.__sample_period


    @property
    def power_saving(self):
        return self.__power_saving


    @property
    def spi_bus(self):
        return self.__spi_bus


    @property
    def spi_device(self):
        return self.__spi_device


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__model
        jdict['sample-period'] = self.__sample_period
        jdict['power-saving'] = self.__power_saving

        jdict['spi-bus'] = self.__spi_bus
        jdict['spi-device'] = self.__spi_device

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCConf:{model:%s, sample_period:%s, power_saving:%s, spi_bus:%s, spi_device:%s}" %  \
               (self.model, self.sample_period, self.power_saving, self.spi_bus, self.spi_device)
