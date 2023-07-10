#!/usr/bin/env python3

"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import logging
import sys

from scs_core.position.gps_datum import GPSDatum

from scs_core.position.nmea.gpgga import GPGGA
from scs_core.position.nmea.gpgll import GPGLL
from scs_core.position.nmea.gpgsa import GPGSA
from scs_core.position.nmea.gpgsv import GPGSV
from scs_core.position.nmea.gprmc import GPRMC
from scs_core.position.nmea.gpvtg import GPVTG

from scs_core.sys.logging import Logging

from scs_dfe.gps.pam_7q import PAM7Q
from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

Logging.config('pam_7q_test', level=logging.DEBUG)
logger = Logging.getLogger()

I2C.Utilities.open()


# --------------------------------------------------------------------------------------------------------------------

conf = InterfaceConf.load(Host)
interface = conf.interface()
print(interface)
print("-")

gps = PAM7Q(interface, Host.gps_device())
print(gps)
print("-")

try:
    # ----------------------------------------------------------------------------------------------------------------

    print("power up...")
    gps.power_on()

    print("open...")
    gps.open()
    print(gps)
    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    print("report...")

    gga = gps.report(GPGGA)
    print(gga)
    print("-")

    gll = gps.report(GPGLL)
    print(gll)
    print("-")

    gsv = gps.report(GPGSV)
    print(gsv)
    print("-")

    gsa = gps.report(GPGSA)
    print(gsa)
    print("-")

    rmc = gps.report(GPRMC)
    print(rmc)
    print("-")

    vtg = gps.report(GPVTG)
    print(vtg)
    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    print("report all...")

    msgs = gps.report_all()

    for msg in msgs:
        print(msg)
        print("-")

    print("=")


    # ----------------------------------------------------------------------------------------------------------------

    if rmc is not None:
        print("RMC position: %s, %s  time: %s" % (rmc.loc.deg_lat(), rmc.loc.deg_lng(), rmc.datetime.as_iso8601()))
        print("GGA position: %s, %s" % (gga.loc.deg_lat(), gga.loc.deg_lng()))

        location = GPSDatum.construct_from_gga(gga)
        print("GGA location: %s" % str(location))

        print("=")


# ----------------------------------------------------------------------------------------------------------------

except KeyboardInterrupt:
    print(file=sys.stderr)

finally:
    print("close...")
    gps.close()
    print(gps)
    print("=")

    # print("power down...")
    # gps.power_off()

    I2C.Utilities.close()
