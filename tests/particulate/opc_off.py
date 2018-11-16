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
    I2C.open(Host.I2C_SENSORS)

    opc = OPCN3(Host.opc_spi_bus(), Host.opc_spi_device())
    print(opc)
    print("-")

    opc.power_off()

except KeyboardInterrupt:
    print("opc_off: KeyboardInterrupt", file=sys.stderr)

finally:
    I2C.close()