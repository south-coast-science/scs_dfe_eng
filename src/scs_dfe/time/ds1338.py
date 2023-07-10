"""
Created on 16 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: time shall always be stored as UTC, then localized on retrieval.
"""

from scs_core.data.rtc_datetime import RTCDatetime

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class DS1338(object):
    """
    Maxim Integrated DS1338 serial real-time clock
    """
    __ADDR =                        0x68

    __REG_SECONDS =                 0x00
    __REG_MINUTES =                 0x01
    __REG_HOURS =                   0x02
    __REG_DAY =                     0x03
    __REG_DATE =                    0x04
    __REG_MONTH =                   0x05
    __REG_YEAR =                    0x06
    __REG_CONTROL =                 0x07

    __RAM_START_ADDR =              0x08
    __RAM_MAX_ADDR =                0xff        # 247 bytes

    __SECONDS_MASK_CLOCK_HALT =     0x80        # ---- 1000 0000

    __HOURS_MASK_24_HOUR =          0x40        # ---- 0100 0000

    __CONTROL_MASK_OSC_STOPPED =    0x20        # ---- 0010 0000
    __CONTROL_MASK_SQW_EN =         0x10        # ---- 0001 0000


    # ----------------------------------------------------------------------------------------------------------------

    __LOCK_TIMEOUT =                2.0


    # ----------------------------------------------------------------------------------------------------------------
    # RTC...

    @classmethod
    def init(cls, enable_square_wave=False):
        try:
            cls.obtain_lock()

            # use 24 hour...
            hours = cls.__read_reg(cls.__REG_HOURS)
            hours &= ~cls.__HOURS_MASK_24_HOUR

            cls.__write_reg(cls.__REG_HOURS, hours)

            # enable square wave output...
            control = cls.__read_reg(cls.__REG_CONTROL)
            control = control | cls.__CONTROL_MASK_SQW_EN if enable_square_wave \
                else control & ~cls.__CONTROL_MASK_SQW_EN

            cls.__write_reg(cls.__REG_CONTROL, control)

        finally:
            cls.release_lock()


    @classmethod
    def get_time(cls):
        try:
            cls.obtain_lock()

            # read RTC...
            second = cls.__read_reg_decimal(cls.__REG_SECONDS)
            minute = cls.__read_reg_decimal(cls.__REG_MINUTES)
            hour = cls.__read_reg_decimal(cls.__REG_HOURS)

            weekday = cls.__read_reg_decimal(cls.__REG_DAY)

            day = cls.__read_reg_decimal(cls.__REG_DATE)
            month = cls.__read_reg_decimal(cls.__REG_MONTH)
            year = cls.__read_reg_decimal(cls.__REG_YEAR)

        finally:
            cls.release_lock()

        rtc_datetime = RTCDatetime(year, month, day, weekday, hour, minute, second)

        return rtc_datetime


    @classmethod
    def set_time(cls, rtc_datetime):
        try:
            cls.obtain_lock()

            # update RTC...
            cls.__write_reg_decimal(cls.__REG_SECONDS, rtc_datetime.second)
            cls.__write_reg_decimal(cls.__REG_MINUTES, rtc_datetime.minute)
            cls.__write_reg_decimal(cls.__REG_HOURS, rtc_datetime.hour)

            cls.__write_reg_decimal(cls.__REG_DAY, rtc_datetime.weekday)

            cls.__write_reg_decimal(cls.__REG_DATE, rtc_datetime.day)
            cls.__write_reg_decimal(cls.__REG_MONTH, rtc_datetime.month)
            cls.__write_reg_decimal(cls.__REG_YEAR, rtc_datetime.year)

        finally:
            cls.release_lock()


    @classmethod
    def get_ctrl(cls):
        return cls.__read_reg(cls.__REG_CONTROL)


    # ----------------------------------------------------------------------------------------------------------------
    # RAM...

    @classmethod
    def read(cls, addr):
        if addr < 0 or addr > cls.__RAM_MAX_ADDR:
            raise IndexError("RAM address out of range: %d" % addr)

        return cls.__read_reg(cls.__RAM_START_ADDR + addr)


    @classmethod
    def write(cls, addr, val):
        if addr < 0 or addr > cls.__RAM_MAX_ADDR:
            raise IndexError("RAM address out of range: %d" % addr)

        cls.__write_reg(cls.__RAM_START_ADDR + addr, val)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read_reg_decimal(cls, addr):
        return cls.__as_decimal(cls.__read_reg(addr))


    @classmethod
    def __read_reg(cls, addr):
        try:
            I2C.Sensors.start_tx(cls.__ADDR)
            value = I2C.Sensors.read_cmd(addr, 1)
        finally:
            I2C.Sensors.end_tx()

        return value


    @classmethod
    def __write_reg_decimal(cls, addr, value):
        return cls.__write_reg(addr, cls.__as_bcd(value))


    @classmethod
    def __write_reg(cls, addr, value):
        try:
            I2C.Sensors.start_tx(cls.__ADDR)
            I2C.Sensors.write(addr, value)
        finally:
            I2C.Sensors.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__lock_name(), DS1338.__LOCK_TIMEOUT)


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__lock_name())


    @classmethod
    def __lock_name(cls):
        return "%s-0x%02x" % (cls.__name__, cls.__ADDR)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __as_decimal(cls, bcd):
        msb = bcd >> 4
        lsb = bcd & 0x0f

        return msb * 10 + lsb


    @classmethod
    def __as_bcd(cls, decimal):
        msb = decimal // 10
        lsb = decimal % 10

        return msb << 4 | lsb
