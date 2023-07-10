#!/usr/bin/env python3

"""
Created on 30 Nov 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify
from scs_core.sample.climate_sample import ClimateSample
from scs_core.sys.logging import Logging

from scs_dfe.climate.pressure_conf import PressureConf
from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.led.io_led import IOLED

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

SLEEP_TIME = 3.0

sht = None
barometer = None


def set_colour(colour):
    led.colour = colour
    logger.error("colour: %s" % colour)


# --------------------------------------------------------------------------------------------------------------------
# logging...

Logging.config('ring_test')
logger = Logging.getLogger()

try:
    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    I2C.Utilities.open()

    # SHTConf...
    sht_conf = SHTConf.load(Host)

    if sht_conf is None:
        logger.error("SHTConf not available.")
        exit(1)

    logger.info(sht_conf)

    # SHT...
    sht = sht_conf.ext_sht()
    logger.info(sht)

    # PressureConf...
    pressure_conf = PressureConf.load(Host)

    if pressure_conf is not None:
        logger.info(pressure_conf)

        # barometer...
        barometer = pressure_conf.sensor(None)
        logger.info(barometer)

    else:
        barometer = None

except OSError as ex:
    logger.error("resources: %s" % repr(ex))
    exit(1)

finally:
    I2C.Utilities.close()

try:
    # ----------------------------------------------------------------------------------------------------------------
    # climate...

    I2C.Utilities.open()

    try:
        sht.reset()
    except OSError as ex:
        logger.error("SHT: %s" % repr(ex))
        exit(1)

    if barometer:
        try:
            barometer.init()
        except OSError as ex:
            logger.error("barometer: %s" % repr(ex))
            barometer = None

    sht_sample = sht.sample() if sht else None
    barometer_sample = barometer.sample(include_temp=True) if barometer else None
    recorded = LocalizedDatetime.now().utc()

    print(JSONify.dumps(ClimateSample(None, recorded, sht_sample, barometer_sample)))

except OSError as ex:
    logger.error("resources: %s" % repr(ex))
    exit(1)

finally:
    logger.error("-")
    I2C.Utilities.close()

try:
    # ----------------------------------------------------------------------------------------------------------------
    # LED...

    I2C.Utilities.open()

    led = IOLED()

    set_colour('G')
    time.sleep(SLEEP_TIME)

    set_colour('R')
    time.sleep(SLEEP_TIME)

    set_colour('A')
    time.sleep(SLEEP_TIME)

    set_colour('0')

except OSError as ex:
    logger.error("LED: %s" % repr(ex))
    exit(1)

finally:
    I2C.Utilities.close()
