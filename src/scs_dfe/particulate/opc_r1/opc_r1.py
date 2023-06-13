"""
Created on 23 Jan 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Firmware report:
OPC-R1 FirmwareVer=2.10...................................BS
"""

import time

from scs_dfe.particulate.alphasense_opc import AlphasenseOPC

from scs_dfe.particulate.opc_r1.opc_firmware_conf import OPCFirmwareConf
from scs_dfe.particulate.opc_r1.opc_r1_datum import OPCR1Datum


# --------------------------------------------------------------------------------------------------------------------

class OPCR1(AlphasenseOPC):
    """
    classdocs
    """
    MIN_SAMPLE_PERIOD =                  5.0        # seconds
    MAX_SAMPLE_PERIOD =                 10.0        # seconds
    DEFAULT_SAMPLE_PERIOD =             10.0        # seconds

    DEFAULT_BUSY_TIMEOUT =               5.0        # seconds


    # ----------------------------------------------------------------------------------------------------------------

    __BOOT_TIME =                       4.0         # seconds
    __POWER_CYCLE_TIME =               10.0         # seconds

    __FAN_START_TIME =                  3.0         # seconds
    __FAN_STOP_TIME =                   3.0         # seconds

    __MAX_PERMITTED_ZERO_READINGS =     30

    __CMD_POWER =                       0x03
    __CMD_PERIPHERALS_ON =              0x07
    __CMD_PERIPHERALS_OFF =             0x00

    __CMD_READ_HISTOGRAM =              0x30

    __CMD_GET_FIRMWARE =                0x3f
    __CMD_GET_VERSION =                 0x12
    __CMD_GET_SERIAL =                  0x10

    __CMD_GET_CONF =                    0x3c
    __CMD_SET_CONF =                    0x3a
    __CMD_SET_BIN_WEIGHTING_INDEX =     0x05

    __CMD_SAVE_CONF =                   0x43
    __CMD_SAVE_CONF_SEQUENCE =          (0x3F, 0x3c, 0x3f, 0x3c, 0x43)

    __CMD_CHECK =                       0xcf

    __CMD_RESET =                       0x06

    __RESPONSE_BUSY =                   0x31
    __RESPONSE_NOT_BUSY =               (0x00, 0xff, 0xf3)

    __SPI_CLOCK =                       326000      # Minimum speed for OPCube
    __SPI_MODE =                        1

    __DELAY_TRANSFER =                  0.020
    __DELAY_CMD =                       0.020
    __DELAY_BUSY =                      0.100

    __LOCK_TIMEOUT =                    20.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def source(cls):
        return OPCR1Datum.SOURCE


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

            # peripherals...
            self.__cmd_power(self.__CMD_PERIPHERALS_ON)
            time.sleep(self.__FAN_START_TIME)

        finally:
            self.release_lock()


    def operations_off(self):
        try:
            self.obtain_lock()

            # peripherals...
            self.__cmd_power(self.__CMD_PERIPHERALS_OFF)
            time.sleep(self.__FAN_STOP_TIME)

        finally:
            self.release_lock()


    def reset(self):
        try:
            self.obtain_lock()
            self._spi.open()

            # command...
            self.__wait_while_busy()
            self.__cmd(self.__CMD_RESET)

        finally:
            self._spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        try:
            self.obtain_lock()
            self._spi.open()

            # command...
            self.__wait_while_busy()
            self.__cmd(self.__CMD_READ_HISTOGRAM)
            chars = self.__read_bytes(OPCR1Datum.CHARS)

            # report...
            return OPCR1Datum.construct(chars)

        finally:
            self._spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def serial_no(self):
        try:
            self.obtain_lock()
            self._spi.open()

            # command...
            self.__wait_while_busy()
            self.__cmd(self.__CMD_GET_SERIAL)
            chars = self.__read_bytes(60)

            # report...
            report = ''.join(chr(byte) for byte in chars)
            pieces = report.split(' ')

            if len(pieces) < 2:
                return None

            return pieces[1]

        finally:
            self._spi.close()
            self.release_lock()


    def version(self):
        try:
            self.obtain_lock()
            self._spi.open()

            # command...
            self.__wait_while_busy()
            self.__cmd(self.__CMD_GET_VERSION)

            # report...
            major = int(self.__read_byte())
            minor = int(self.__read_byte())

            return major, minor

        finally:
            self._spi.close()
            self.release_lock()


    def firmware(self):
        try:
            self.obtain_lock()
            self._spi.open()

            # command...
            self.__wait_while_busy()
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
        try:
            self.obtain_lock()
            self._spi.open()

            # command...
            self.__wait_while_busy()
            self.__cmd(self.__CMD_GET_CONF)
            chars = self.__read_bytes(OPCFirmwareConf.CHARS)

            # report...
            conf = OPCFirmwareConf.construct(chars)

            return conf

        finally:
            self._spi.close()
            self.release_lock()


    def set_firmware_conf(self, jdict):
        raise NotImplementedError                       # set found to be unsafe


    def commit_firmware_conf(self):
        raise NotImplementedError                      # commit found to be unsafe


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

            for _ in range(2):
                self._spi.xfer([self.__CMD_POWER])
                time.sleep(self.__DELAY_CMD)

                # print(["0x%02x" % char for char in response], file=sys.stderr)
                # sys.stderr.flush()

            self._spi.xfer([cmd])
            time.sleep(self.__DELAY_TRANSFER)

        finally:
            self._spi.close()


    def __cmd(self, cmd):
        self._spi.xfer([cmd])
        time.sleep(self.__DELAY_CMD)

        self._spi.xfer([cmd])
        time.sleep(self.__DELAY_TRANSFER)


    def __read_bytes(self, count):
        return (self.__read_byte() for _ in range(count))


    def __read_byte(self):
        chars = self._spi.read_bytes(1)
        time.sleep(self.__DELAY_TRANSFER)

        return chars[0]


    def __write_bytes(self, chars):
        for char in chars:
            self.__write_byte(char)


    def __write_byte(self, char):
        self._spi.xfer([char])
        time.sleep(self.__DELAY_CMD)
