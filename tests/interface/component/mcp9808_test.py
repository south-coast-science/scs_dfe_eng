#!/usr/bin/env python3

"""
Created on 6 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.interface.component.mcp9808 import MCP9808

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    temp = MCP9808(False)
    print(temp)

    temp.running = True

    datum = temp.sample()
    print(datum)

    print(temp)

finally:
    I2C.Sensors.close()
