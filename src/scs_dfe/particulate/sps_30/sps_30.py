"""
Created on 1 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.sensirion.com/en/environmental-sensors/particulate-matter-sensors-pm25/
https://bytes.com/topic/python/answers/171354-struct-ieee-754-internal-representation

Firmware report:
89667EE8A8B34BC0
"""

import time

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Decode, Encode

from scs_core.particulate.sps_datum import SPSDatum, SPSDatumCounts

from scs_dfe.particulate.opc import OPC

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class SPS30(OPC):
    """
    classdocs
    """
    SOURCE =                            'S30'

    MIN_SAMPLE_PERIOD =                  1.0        # seconds
    MAX_SAMPLE_PERIOD =                 10.0        # seconds
    DEFAULT_SAMPLE_PERIOD =             10.0        # seconds

    DEFAULT_ADDR =                      0x69


    # ----------------------------------------------------------------------------------------------------------------

    __BOOT_TIME =                       4.0         # seconds
    __POWER_CYCLE_TIME =                2.0         # seconds

    __FAN_START_TIME =                  2.0         # seconds
    __FAN_STOP_TIME =                   2.0         # seconds

    __CLEANING_TIME =                  10.0         # seconds

    __MAX_PERMITTED_ZERO_READINGS =     4

    __CMD_START_MEASUREMENT =           0x0010
    __CMD_STOP_MEASUREMENT =            0x0104
    __CMD_READ_DATA_READY_FLAG =        0x0202
    __CMD_READ_MEASURED_VALUES =        0x0300
    __CMD_AUTO_CLEANING_INTERVAL =      0x8004
    __CMD_START_FAN_CLEANING =          0x5607
    __CMD_READ_ARTICLE_CODE =           0xd025
    __CMD_READ_SERIAL_NUMBER =          0xd033
    __CMD_RESET =                       0xd304

    __POST_WRITE_DELAY =                0.020       # seconds

    __LOCK_TIMEOUT =                    2.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def source(cls):
        return cls.SOURCE


    @classmethod
    def uses_spi(cls):
        return False


    @classmethod
    def datum_class(cls):
        return SPSDatum


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __decode(cls, chars):
        decoded = []

        for i in range(0, len(chars), 3):
            group = chars[i:i + 2]
            decoded.extend(group)

            actual_crc = chars[i + 2]
            required_crc = cls.__crc(group)

            if actual_crc != required_crc:
                raise ValueError("bad checksum: required: 0x%02x actual: 0x%02x" % (required_crc, actual_crc))

        return decoded


    @classmethod
    def __encode(cls, chars):
        encoded = []

        for i in range(0, len(chars), 2):
            group = chars[i:i + 2]

            encoded.extend(group)
            encoded.append(cls.__crc(group))

        return encoded


    @staticmethod
    def __crc(data):
        crc = 0xff

        for datum in data:
            crc ^= datum

            for bit in range(8, 0, -1):
                crc = ((crc << 1) ^ 0x31 if crc & 0x80 else (crc << 1)) & 0xff

        return crc


    # ----------------------------------------------------------------------------------------------------------------

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

    def __init__(self, interface, i2c_addr):
        """
        Constructor
        """
        super().__init__(interface)

        self.__i2c_addr = i2c_addr


    # ----------------------------------------------------------------------------------------------------------------

    def operations_on(self):
        self.__write(self.__CMD_START_MEASUREMENT, self.__FAN_START_TIME, 0x03, 0x00)


    def operations_off(self):
        self.__read(self.__CMD_STOP_MEASUREMENT, self.__FAN_STOP_TIME)


    def reset(self):
        self.__read(self.__CMD_RESET, self.__BOOT_TIME)


    # ----------------------------------------------------------------------------------------------------------------

    def clean(self):
        self.__read(self.__CMD_START_FAN_CLEANING, self.__CLEANING_TIME)


    @property
    def cleaning_interval(self):
        r = self.__read(self.__CMD_AUTO_CLEANING_INTERVAL, 0, 6)
        interval = Decode.unsigned_long(r[0:4], '>')

        return interval


    @cleaning_interval.setter
    def cleaning_interval(self, interval):
        values = Encode.unsigned_long(interval, '>')
        self.__write(self.__CMD_AUTO_CLEANING_INTERVAL, self.__POST_WRITE_DELAY, *values)


    # ----------------------------------------------------------------------------------------------------------------

    def data_ready(self):
        chars = self.__read(self.__CMD_READ_DATA_READY_FLAG, 0, 3)

        return chars[1] == 0x01


    def sample(self):
        r = self.__read(self.__CMD_READ_MEASURED_VALUES, 0, 60)

        # density...
        pm1 = Decode.float(r[0:4], '>')
        pm2p5 = Decode.float(r[4:8], '>')
        pm4 = Decode.float(r[8:12], '>')
        pm10 = Decode.float(r[12:16], '>')

        # count...
        pm0p5_count = Decode.float(r[16:20], '>')
        pm1_count = Decode.float(r[20:24], '>')
        pm2p5_count = Decode.float(r[24:28], '>')
        pm4_count = Decode.float(r[28:32], '>')
        pm10_count = Decode.float(r[32:36], '>')

        # typical size...
        tps = Decode.float(r[36:40], '>')

        # time...
        rec = LocalizedDatetime.now().utc()

        # report...
        counts = SPSDatumCounts(pm0p5_count, pm1_count, pm2p5_count, pm4_count, pm10_count)

        return SPSDatum(self.SOURCE, rec, pm1, pm2p5, pm4, pm10, counts, tps)


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        r = self.__read(self.__CMD_READ_ARTICLE_CODE, 0, 48)
        version = ''.join(chr(byte) for byte in r)

        return version


    def serial_no(self):
        r = self.__read(self.__CMD_READ_SERIAL_NUMBER, 0, 48)
        serial_no = ''.join(chr(byte) for byte in r)

        return serial_no


    def firmware(self):
        return self.serial_no()


    # ----------------------------------------------------------------------------------------------------------------

    def get_firmware_conf(self):
        raise NotImplementedError


    def set_firmware_conf(self, jdict):
        raise NotImplementedError


    def commit_firmware_conf(self):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dev_path(self):
        raise NotImplementedError


    @property
    def bus(self):
        return I2C.Sensors.bus


    @property
    def address(self):
        return self.__i2c_addr


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lock_name(self):
        return self.__class__.__name__ + '-' + str(I2C.Sensors.bus) + '-' + ("0x%02x" % self.__i2c_addr)


    # ----------------------------------------------------------------------------------------------------------------

    def __read(self, command, wait, count=0):
        try:
            self.obtain_lock()

            try:
                I2C.Sensors.start_tx(self.__i2c_addr)

                encoded = I2C.Sensors.read_cmd16(command, count)
                values = self.__decode(encoded)

            finally:
                I2C.Sensors.end_tx()

            time.sleep(wait)
            return values

        finally:
            self.release_lock()


    def __write(self, command, wait, *values):
        try:
            self.obtain_lock()

            try:
                I2C.Sensors.start_tx(self.__i2c_addr)

                encoded = self.__encode(values)
                I2C.Sensors.write_addr16(command, *encoded)

            finally:
                I2C.Sensors.end_tx()

            time.sleep(wait)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SPS30:{interface:%s, i2c_addr:0x%02x}" % \
               (self.interface, self.__i2c_addr)
