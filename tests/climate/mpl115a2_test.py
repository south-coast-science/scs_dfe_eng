#!/usr/bin/env python3

"""
Created on 19 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.climate.mpl115a2_calib import MPL115A2Calib
from scs_core.data.json import JSONify

from scs_dfe.climate.mpl115a2 import MPL115A2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------


try:
    I2C.open(Host.I2C_SENSORS)

    # with calib & altitude...
    calib = MPL115A2Calib(None, MPL115A2Calib.DEFAULT_C25)

    barometer = MPL115A2(calib)

    barometer.init()
    print(barometer)

    datum = barometer.sample(1000)

    print(datum)
    print(JSONify.dumps(datum))

    print("-")

    # with calib...
    calib = MPL115A2Calib(None, MPL115A2Calib.DEFAULT_C25)

    barometer = MPL115A2(calib)

    barometer.init()
    print(barometer)

    datum = barometer.sample()

    print(datum)
    print(JSONify.dumps(datum))

    print("-")

    # no calib...
    calib = None

    barometer = MPL115A2(calib)

    barometer.init()
    print(barometer)

    datum = barometer.sample()

    print(datum)
    print(JSONify.dumps(datum))

finally:
    I2C.close()