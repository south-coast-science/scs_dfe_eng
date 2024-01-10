"""
Created on 11 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

settings for OPCMonitor

example JSON:
{"model": "N3", "sample-period": 10, "restart-on-zeroes": true, "power-saving": false,
"custom-dev-path": "/dev/spi/by-connector/H3"}
"""

from scs_core.particulate.opc_conf import OPCConf as AbstractOPCConf

from scs_dfe.particulate.opc_monitor import OPCMonitor

from scs_dfe.particulate.opc_n2.opc_n2 import OPCN2
from scs_dfe.particulate.opc_n3.opc_n3 import OPCN3
from scs_dfe.particulate.opc_r1.opc_r1 import OPCR1

from scs_dfe.particulate.sps_30.sps_30 import SPS30


# --------------------------------------------------------------------------------------------------------------------

class OPCConf(AbstractOPCConf):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_model(cls, model):
        return model in (OPCN2.source(), OPCN3.source(), OPCR1.source(), SPS30.source())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_period, restart_on_zeroes, power_saving, custom_dev_path, name=None):
        """
        Constructor
        """
        super().__init__(model, sample_period, restart_on_zeroes, power_saving, custom_dev_path, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def opc_monitor(self, manager, interface):
        opc = self.opc(interface)

        return OPCMonitor(manager, opc, self)


    def opc(self, interface):
        if self.model == OPCN2.source():
            return OPCN2(interface, self.dev_path)

        elif self.model == OPCN3.source():
            return OPCN3(interface, self.dev_path)

        elif self.model == OPCR1.source():
            return OPCR1(interface, self.dev_path)

        elif self.model == SPS30.source():
            return SPS30(interface, SPS30.DEFAULT_ADDR)

        raise ValueError('unknown model: %s' % self.model)


    def uses_spi(self):
        if self.model == OPCN2.source():
            return OPCN2.uses_spi()

        elif self.model == OPCN3.source():
            return OPCN3.uses_spi()

        elif self.model == OPCR1.source():
            return OPCR1.uses_spi()

        elif self.model == SPS30.source():
            return SPS30.uses_spi()

        raise ValueError('unknown model: %s' % self.model)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCConf(dfe):{name:%s, model:%s, sample_period:%s, restart_on_zeroes:%s, power_saving:%s, " \
               "custom_dev_path:%s}" %  \
               (self.name, self.model, self.sample_period, self.restart_on_zeroes, self.power_saving,
                self.custom_dev_path)
