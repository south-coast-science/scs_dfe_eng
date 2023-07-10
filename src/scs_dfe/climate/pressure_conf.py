"""
Created on 9 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"model": "ICP", "altitude": 100}
"""

from scs_core.climate.pressure_conf import PressureConf as AbstractPressureConf

from scs_dfe.climate.icp10101 import ICP10101
from scs_dfe.climate.mpl115a2 import MPL115A2


# --------------------------------------------------------------------------------------------------------------------

class PressureConf(AbstractPressureConf):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_model(cls, model):
        return model in cls.models()


    @classmethod
    def models(cls):
        return ICP10101.NAME, MPL115A2.NAME


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, altitude):
        """
        Constructor
        """
        super().__init__(model, altitude)


    # ----------------------------------------------------------------------------------------------------------------

    def sensor(self, mpl_calib):
        if self.model == ICP10101.NAME:
            return ICP10101(ICP10101.DEFAULT_ADDR)

        if self.model == MPL115A2.NAME:
            c25 = None if mpl_calib is None else mpl_calib.c25
            return MPL115A2(c25)

        raise ValueError(self.model)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PressureConf(dfe):{model:%s, altitude:%s}" % (self.model, self.altitude)
