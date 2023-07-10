#!/usr/bin/env python3

"""
Created on 1 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

from scs_dfe.interface.dfe.dfe import DFE
from scs_dfe.particulate.sps_30.sps_30 import SPS30

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    opc = SPS30(DFE(), SPS30.DEFAULT_ADDR)
    print(opc)
    print("-")

    print("reset...")
    opc.reset()

    # print("version...")
    # version = opc.version()
    # print("version: %s" % version)
    # print("-")

    print("serial_no...")
    sn = opc.serial_no()
    print("sn: %s" % sn)
    print("-")

    time.sleep(1)

    # print("set cleaning_interval...")
    # opc.set_cleaning_interval(0)
    # print("-")

    print("get cleaning_interval...")
    interval = opc.cleaning_interval
    print("interval: %s" % interval)
    print("-")

    time.sleep(1)

    print("operations_on...")
    opc.operations_on()
    print("-")

    print("clean...")
    opc.clean()
    print("-")


    timer = IntervalTimer(5)

    for i in timer.range(20):
        ready =  opc.data_ready()
        print("ready: %s" % ready)

        sample = opc.sample()
        print(JSONify.dumps(sample))

        ready =  opc.data_ready()
        print("ready: %s" % ready)
        print("-")

    print("operations_off...")
    opc.operations_off()
    print("-")


except KeyboardInterrupt:
    print(file=sys.stderr)

except ValueError as ex:
    print(repr(ex))

finally:
    I2C.Sensors.close()
