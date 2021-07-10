"""
Created on 27 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

South Coast Science PID Digital Single Interface (DSI) Type 1

Compatible with:
https://github.com/south-coast-science/scs_dsi_t1_f1
"""

import time

from scs_core.data.datum import Decode

from scs_dfe.gas.isi.dsi import DSI

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class PIDDSIt1(DSI):
    """
    South Coast Science PID DSI Type 1 microcontroller
    """

    DEFAULT_ADDR =          0x3c

    CONVERSION_TIME =       0.05                # seconds


    # ----------------------------------------------------------------------------------------------------------------

    __RESPONSE_ACK =        1
    __RESPONSE_NACK =       2

    __SEND_WAIT_TIME =      0.010               # seconds
    __LOCK_TIMEOUT =        2.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        super().__init__(addr)


    # ----------------------------------------------------------------------------------------------------------------

    def power_sensor(self, on):
        cmd = '1' if on else '0'
        response = self.__cmd(ord(cmd), 1)

        if response != self.__RESPONSE_ACK:
            raise RuntimeError("response: %s" % response)


    def start_conversion(self):
        response = self.__cmd(ord('s'), 1)

        if response != self.__RESPONSE_ACK:
            raise RuntimeError("response: %s" % response)


    def read_conversion_count(self):
        response = self.__cmd(ord('c'), 2)

        count = Decode.unsigned_int(response[0:2], '<')

        return count


    def read_conversion_voltage(self):
        response = self.__cmd(ord('v'), 4)

        v = Decode.float(response[0:4], '<')

        return round(v, 5)


    def version_ident(self):
        response = self.__cmd(ord('i'), 40)

        return ''.join([chr(byte) for byte in response]).strip()


    def version_tag(self):
        response = self.__cmd(ord('t'), 11)

        return ''.join([chr(byte) for byte in response]).strip()


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self, cmd, response_size):
        try:
            self.obtain_lock()
            I2C.Sensors.start_tx(self.addr)

            response = I2C.Sensors.read_cmd(cmd, response_size, self.__SEND_WAIT_TIME)

            time.sleep(self.__SEND_WAIT_TIME)

            return response

        finally:
            I2C.Sensors.end_tx()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return "%s-0x%02x" % (self.__class__.__name__, self.addr)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDDSIt1:{addr:0x%0.2x}" % self.addr
