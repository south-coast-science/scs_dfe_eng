#!/usr/bin/env python3

"""
Created on 25 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.interface.component.at24mac402 import AT24MAC402

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

Host.enable_eeprom_access()


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    eeprom = AT24MAC402()
    print(eeprom)

finally:
    I2C.Sensors.close()
