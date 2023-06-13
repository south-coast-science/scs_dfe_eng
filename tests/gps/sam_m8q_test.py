#!/usr/bin/env python3

"""
Created on 31 Jan 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

$GNRMC,103953.00,A,5049.38023,N,00007.38608,W,0.195,,310119,,,D*72
$GNVTG,,T,,M,0.195,N,0.361,K,D*31
$GNGGA,103953.00,5049.38023,N,00007.38608,W,2,07,1.48,54.2,M,45.4,M,,0000*62
$GNGSA,A,3,02,09,05,07,13,28,30,,,,,,2.28,1.48,1.73*1E
$GNGSA,A,3,,,,,,,,,,,,,2.28,1.48,1.73*1C
$GPGSV,3,1,12,02,15,220,48,05,71,253,39,07,45,060,35,09,14,091,22*7D
$GPGSV,3,2,12,13,42,273,34,15,08,278,16,21,09,332,33,27,02,033,*77
$GPGSV,3,3,12,28,20,140,31,30,74,110,26,36,25,141,,49,32,173,47*7D
$GLGSV,1,1,00*65
$GNGLL,5049.38023,N,00007.38608,W,103953.00,A,D*6D
"""

import logging
import sys
import time

from scs_core.position.gps_datum import GPSDatum

from scs_core.position.nmea.gpgga import GPGGA
from scs_core.position.nmea.gpgll import GPGLL
from scs_core.position.nmea.gpgsa import GPGSA
from scs_core.position.nmea.gpgsv import GPGSV
from scs_core.position.nmea.gprmc import GPRMC
from scs_core.position.nmea.gpvtg import GPVTG

from scs_core.sys.logging import Logging

from scs_dfe.gps.sam_m8q import SAMM8Q
from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

Logging.config('sam_m8q_test', level=logging.DEBUG)
logger = Logging.getLogger()

I2C.Utilities.open()


# --------------------------------------------------------------------------------------------------------------------

conf = InterfaceConf.load(Host)
interface = conf.interface()
print(interface)
print("-")


gps = SAMM8Q(interface, Host.gps_device())
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

    while True:
        print("reports...")

        gga = gps.report(GPGGA)
        print("GGA: %s" % gga)
        print("-")

        gll = gps.report(GPGLL)
        print("GLL: %s" % gll)
        print("-")

        gsv = gps.report(GPGSV)
        print("GSV: %s" % gsv)
        print("-")

        gsa = gps.report(GPGSA)
        print("GSA: %s" % gsa)
        print("-")

        rmc = gps.report(GPRMC)
        print("RMC: %s" % rmc)
        print("-")

        vtg = gps.report(GPVTG)
        print("VTG: %s" % vtg)
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

        time.sleep(4)

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
