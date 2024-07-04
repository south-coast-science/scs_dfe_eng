"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONReport

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class PCA8574(object):
    """
    NXP PCA8574 remote 8-bit I/O expander
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, addr, directory, file):
        device = PCA8574(addr, directory, file)

        try:
            state = device.read()                           # test whether PCA8574 is present
            return None if state is None else device

        except OSError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr, directory, file):
        """
        Constructor
        """
        self.__addr = addr
        self.__directory = directory
        self.__file = file


    # ----------------------------------------------------------------------------------------------------------------

    def read(self):
        try:
            I2C.Sensors.start_tx(self.__addr)
            byte = I2C.Sensors.read(1)

        except RuntimeError:
            return None

        finally:
            I2C.Sensors.end_tx()

        return byte


    def write(self, byte):
        try:
            I2C.Sensors.start_tx(self.__addr)
            I2C.Sensors.write(byte)

        finally:
            I2C.Sensors.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def state(self):
        return PCA8574State.load(os.path.join(self.__directory, self.__file))


    @state.setter
    def state(self, byte):
        state = PCA8574State.load(os.path.join(self.__directory, self.__file))

        state.byte = byte
        state.save(self.__file)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PCA8574:{addr:0x%02x, directory:%s, file:%s}" % (self.__addr, self.__directory, self.__file)


# --------------------------------------------------------------------------------------------------------------------

class PCA8574State(JSONReport):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        byte = int(jdict.get('byte') if jdict else '0xff', 16)

        return PCA8574State(byte)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, byte):
        """
        Constructor
        """
        self.__byte = byte                  # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['byte'] = "0x%02x" % self.__byte

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def byte(self):
        return self.__byte


    @byte.setter
    def byte(self, byte):
        self.__byte = byte


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        binary = bin(self.__byte)

        return "PCA8574State:{byte:%s}" % binary
