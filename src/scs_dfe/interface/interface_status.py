"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class InterfaceStatus(JSONable):
    """
    classdocs
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, temp):
        """
        Constructor
        """
        self.__temp = Datum.float(temp, 1)          # temperature             °C


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['tmp'] = self.temp

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def temp(self):
        return self.__temp


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "InterfaceStatus:{temp:%0.1f}" % self.temp
