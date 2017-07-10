#!/usr/bin/env python3

"""
Created on 9 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.python.org/3/library/multiprocessing.html#sharing-state-between-processes
http://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing/
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

from scs_dfe.particulate.opc_n2 import OPCN2
from scs_dfe.particulate.opc_monitor import OPCMonitor

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------
# run...

if __name__ == '__main__':

    monitor = None

    try:
        I2C.open(Host.I2C_SENSORS)

        monitor = OPCMonitor(OPCN2(), 5)
        print("main: %s" % monitor)

        proc = monitor.start()

        timer = IntervalTimer(20)

        while timer.true():
            datum = monitor.sample()

            print("main: %s" % datum)

            print(JSONify.dumps(datum))

            print("main: -")
            sys.stdout.flush()

            # if datum is not None:
            #     proc.terminate()

            if not proc.is_alive():
                break

    except KeyboardInterrupt:
        pass

    finally:
        if monitor:
            monitor.off()

        I2C.close()
