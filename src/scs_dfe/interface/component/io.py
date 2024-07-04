"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.interface.component.pca8574 import PCA8574

from scs_host.lock.lock import Lock
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class IO(object):
    """
    NXP PCA8574 remote 8-bit I/O expander
    """

    ADDR =                  0x3f

    # ----------------------------------------------------------------------------------------------------------------

    __MASK_GPS =            0x01            # 0000 0001
    __MASK_OPC =            0x02            # 0000 0010
    __MASK_NDIR =           0x04            # 0000 0100

    __MASK_LED_RED =        0x40            # 0100 0000
    __MASK_LED_GREEN =      0x80            # 1000 0000

    __LOCK =                "DFE_IO"
    __LOCK_TIMEOUT =        2.0


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =            "dfe_io.json"

    @classmethod
    def filename(cls, manager):
        return manager.tmp_file(cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __lock_name(cls, func):
        return "%s-%s" % (cls.__name__, func)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, active_high):
        """
        Constructor
        """
        self.__active_high = active_high

        self.__device = PCA8574.construct(IO.ADDR, Host.lock_dir(), self.filename(Host))


    # ----------------------------------------------------------------------------------------------------------------
    # power outputs...

    @property
    def gps_power(self):
        level = self.__get_output(IO.__MASK_GPS)

        if level is None:
            return None

        return not (level ^ self.__active_high)             # active high or low



    @gps_power.setter
    def gps_power(self, on):
        level = not (on ^ self.__active_high)               # active high or low

        self.__set_output(IO.__MASK_GPS, level)


    @property
    def opc_power(self):
        level = self.__get_output(IO.__MASK_OPC)

        if level is None:
            return None

        return not (level ^ self.__active_high)             # active high or low


    @opc_power.setter
    def opc_power(self, on):
        level = not (on ^ self.__active_high)               # active high or low

        self.__set_output(IO.__MASK_OPC, level)


    @property
    def ndir_power(self):
        level = self.__get_output(IO.__MASK_NDIR)

        if level is None:
            return None

        return not (level ^ self.__active_high)             # active high or low


    @ndir_power.setter
    def ndir_power(self, on):
        level = not (on ^ self.__active_high)               # active high or low

        self.__set_output(IO.__MASK_NDIR, level)


    # ----------------------------------------------------------------------------------------------------------------
    # LED outputs...

    @property
    def led_red(self):                                      # always active high
        return self.__get_output(IO.__MASK_LED_RED)


    @led_red.setter
    def led_red(self, on):
        self.__set_output(IO.__MASK_LED_RED, on)


    @property
    def led_green(self):                                    # always active high
        return self.__get_output(IO.__MASK_LED_GREEN)


    @led_green.setter
    def led_green(self, on):
        self.__set_output(IO.__MASK_LED_GREEN, on)


    # ----------------------------------------------------------------------------------------------------------------

    def __get_output(self, mask):
        if self.__device is None:
            return None

        Lock.acquire(IO.__lock_name(IO.__LOCK), IO.__LOCK_TIMEOUT)

        try:
            byte = self.__device.state.byte

            return bool(byte & mask)

        finally:
            Lock.release(IO.__lock_name(IO.__LOCK))


    def __set_output(self, mask, level):
        if self.__device is None:
            return

        Lock.acquire(IO.__lock_name(IO.__LOCK), IO.__LOCK_TIMEOUT)

        try:
            byte = self.__device.state.byte

            if level:
                byte |= mask
            else:
                byte &= ~mask

            self.__device.write(byte)
            self.__device.state = byte

        finally:
            Lock.release(IO.__lock_name(IO.__LOCK))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IO:{active_high:%s, device:%s}" % (self.__active_high, self.__device)
