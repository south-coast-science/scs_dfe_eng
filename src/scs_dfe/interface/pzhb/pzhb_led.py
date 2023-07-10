"""
Created on 31 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.led.led import LED


# --------------------------------------------------------------------------------------------------------------------

class PZHBLED(LED):
    """
    classdocs
    """
    __MAPPING = {'0': [False, False], 'R': [True, True], 'A': [True, True], 'G': [True, True]}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_colour(cls, colour):
        return colour in cls.STATES


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mcu):
        """
        Constructor
        """
        self.__mcu = mcu
        self.__colour = None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def colour(self):
        return self.__colour


    @colour.setter
    def colour(self, colour):
        if not self.is_valid_colour(colour):
            raise ValueError(colour)

        self.__colour = colour

        states = self.__MAPPING[colour]

        self.__mcu.led1(states[0])
        self.__mcu.led2(states[1])


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PZHBLED:{colour:%s, mcu:%s}" % (self.__colour, self.__mcu)
