"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Firmware report:
OPC-N2 FirmwareVer=OPC-018.1..............................BD
"""

import time

from scs_dfe.particulate.alphasense_opc import AlphasenseOPC
from scs_dfe.particulate.opc_n2.opc_n2_datum import OPCN2Datum


# --------------------------------------------------------------------------------------------------------------------

class OPCN2(AlphasenseOPC):
    """
    classdocs
    """
    SOURCE =                            'N2'

    MIN_SAMPLE_PERIOD =                  5.0        # seconds
    MAX_SAMPLE_PERIOD =                 10.0        # seconds
    DEFAULT_SAMPLE_PERIOD =             10.0        # seconds

    DEFAULT_BUSY_TIMEOUT =               5.0        # seconds

    # ----------------------------------------------------------------------------------------------------------------

    __BOOT_TIME =                        4.0        # seconds
    __START_TIME =                       5.0        # seconds
    __STOP_TIME =                        2.0        # seconds
    __POWER_CYCLE_TIME =                10.0        # seconds

    __MAX_PERMITTED_ZERO_READINGS =     4

    __FAN_UP_TIME =                     10
    __FAN_DOWN_TIME =                   2

    __CMD_POWER =                       0x03
    __CMD_POWER_ON =                    0x00
    __CMD_POWER_OFF =                   0x01

    __CMD_CHECK_STATUS =                0xcf
    __CMD_READ_HISTOGRAM =              0x30
    __CMD_GET_FIRMWARE =                0x3f

    __CMD_CHECK =                       0xcf

    __RESPONSE_BUSY =                   0x31
    __RESPONSE_NOT_BUSY =               (0x00, 0xff, 0xf3)

    __SPI_CLOCK =                       326000      # Minimum speed for OPCube
    __SPI_MODE =                        1

    __DELAY_TRANSFER =                  0.001
    __DELAY_CMD =                       0.010
    __DELAY_BUSY =                      0.100

    __LOCK_TIMEOUT =                    20.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def source(cls):
        return cls.SOURCE


    @classmethod
    def lock_timeout(cls):
        return cls.__LOCK_TIMEOUT


    @classmethod
    def boot_time(cls):
        return cls.__BOOT_TIME


    @classmethod
    def power_cycle_time(cls):
        return cls.__POWER_CYCLE_TIME


    @classmethod
    def max_permitted_zero_readings(cls):
        return cls.__MAX_PERMITTED_ZERO_READINGS


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, dev_path):
        """
        Constructor
        """
        super().__init__(interface, dev_path, self.__SPI_MODE, self.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------

    def operations_on(self):
        try:
            self.obtain_lock()
            self._spi.open()

            # start...
            self.__cmd_power(self.__CMD_POWER_ON)

            time.sleep(self.__START_TIME)

        finally:
            self._spi.close()
            self.release_lock()


    def operations_off(self):
        try:
            self.obtain_lock()
            self._spi.open()

            self.__cmd_power(self.__CMD_POWER_OFF)

            time.sleep(self.__STOP_TIME)

        finally:
            self._spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        try:
            self.obtain_lock()
            self._spi.open()

            # command...
            self.__cmd(self.__CMD_READ_HISTOGRAM)
            chars = self.__read_bytes(OPCN2Datum.CHARS)

            # report...
            return OPCN2Datum.construct(chars)

        finally:
            self._spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def serial_no(self):
        return None


    def firmware(self):
        try:
            self.obtain_lock()
            self._spi.open()

            # command...
            self.__cmd(self.__CMD_GET_FIRMWARE)
            chars = self.__read_bytes(60)

            # report...
            report = ''.join(chr(byte) for byte in chars)

            return report.strip('\0\xff')       # \0 - Raspberry Pi, \xff - BeagleBone

        finally:
            self._spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def get_firmware_conf(self):
        raise NotImplementedError


    def set_firmware_conf(self, jdict):
        raise NotImplementedError


    def commit_firmware_conf(self):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    def __wait_while_busy(self, specified_timeout=None):
        timeout = self.DEFAULT_BUSY_TIMEOUT if specified_timeout is None else specified_timeout
        timeout_time = time.time() + timeout

        self.__cmd(self.__CMD_CHECK)

        while self.__read_byte() == self.__RESPONSE_BUSY:
            if time.time() > timeout_time:
                raise TimeoutError()

            time.sleep(self.__DELAY_BUSY)


    def __cmd_power(self, cmd):
        try:
            self._spi.open()

            while True:
                response = self._spi.xfer([self.__CMD_POWER])
                time.sleep(self.__DELAY_CMD)

                # print(["0x%02x" % char for char in response], file=sys.stderr)
                # sys.stderr.flush()

                if response[0] in self.__RESPONSE_NOT_BUSY:
                    break

            self._spi.xfer([cmd])
            time.sleep(self.__DELAY_TRANSFER)

        finally:
            self._spi.close()


    def __cmd(self, cmd):
        self._spi.xfer([cmd])
        time.sleep(self.__DELAY_CMD)


    def __read_bytes(self, count):
        return [self.__read_byte() for _ in range(count)]


    def __read_byte(self):
        read_bytes = self._spi.read_bytes(1)
        time.sleep(self.__DELAY_TRANSFER)

        return read_bytes[0]
