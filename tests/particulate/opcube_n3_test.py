#!/usr/bin/env python3

"""
Created on 24 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer
from scs_dfe.interface.interface_conf import InterfaceConf
from scs_dfe.particulate.opc_n3.opc_n3 import OPCN3
from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

opc = None

try:
    I2C.Sensors.open()

    # Interface...
    interface_conf = InterfaceConf.load(Host)
    interface = interface_conf.interface()

    # OPC...
    opc = OPCN3(interface, Host.opc_spi_dev_path())
    print(opc)
    print("-")

    print("booting...")
    opc.power_on()

    # print("status...")
    # status = opc.status()
    # print(status)
    # print("-")
    #
    # print("firmware...")
    # firmware = opc.firmware()
    # print(firmware)
    # print("-")
    #
    # print("version...")
    # version = opc.version()
    # print("major:[%d] minor:[%d]" % version)
    # print("-")
    #
    # print("serial...")
    # serial = opc.serial_no()
    # print("serial_no:%s" % serial)
    # print("-")
    #
    # print("firmware_conf...")
    # conf = opc.get_firmware_conf()
    # print(JSONify.dumps(conf))
    # print("-")

    print("on...")
    input("> start:")
    opc.operations_on()
    print("-")

    # print("sleep...")
    # time.sleep(5)

    print("running...")

    print("status...")
    status = opc.status()
    print(status)
    print("-")

    timer = IntervalTimer(10.0)

    print("clear histograms...")
    opc.sample()                    # clear histograms and timer
    print("-")

    for _ in timer.range(3):
        datum = opc.sample()

        print(JSONify.dumps(datum))
        sys.stdout.flush()

except KeyboardInterrupt:
    print(file=sys.stderr)

except ValueError as ex:
    print(repr(ex))

finally:
    if opc:
        print("off...")
        opc.operations_off()

        print("status...")
        status = opc.status()
        print(status)
        print("-")

        print("shutdown...")
        opc.power_off()
        print("-")

    I2C.Sensors.close()
