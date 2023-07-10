#!/usr/bin/env python3

"""
Created on 15 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.particulate.opc_n3.opc_n3 import OPCN3

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    opc = OPCN3(False, Host.opc_spi_dev_path())
    print(opc)
    print("-")

    opc.power_off()

except KeyboardInterrupt:
    print(file=sys.stderr)

finally:
    I2C.Sensors.close()
