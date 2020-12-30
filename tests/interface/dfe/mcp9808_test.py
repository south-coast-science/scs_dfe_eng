#!/usr/bin/env python3

"""
Created on 9 Dec 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.interface.dfe.dfe import MCP9808

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    sensor = MCP9808(True)
    print(sensor)
    print("-")

    datum = sensor.sample()
    print(datum)
    print("-")

finally:
    I2C.Sensors.close()
