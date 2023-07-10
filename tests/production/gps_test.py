#!/usr/bin/env python3

"""
Created on 30 Nov 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

$GNRMC,103953.00,A,5049.38023,N,00007.38608,W,0.195,,310119,,,D*72
$GNGGA,103953.00,5049.38023,N,00007.38608,W,2,07,1.48,54.2,M,45.4,M,,0000*62
"""

import time

from scs_core.data.json import JSONify

from scs_core.position.gps_datum import GPSDatum
from scs_core.position.nmea.gpgga import GPGGA
from scs_core.position.nmea.gprmc import GPRMC

from scs_core.sys.logging import Logging

from scs_dfe.gps.sam_m8q import SAMM8Q
from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

gps = None

# --------------------------------------------------------------------------------------------------------------------
# logging...

Logging.config('gps_test')
logger = Logging.getLogger()


try:
    I2C.Utilities.open()

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    conf = InterfaceConf.load(Host)
    interface = conf.interface()
    logger.info(interface)

    gps = SAMM8Q(interface, Host.gps_device())
    logger.info(gps)

    # ----------------------------------------------------------------------------------------------------------------

    logger.error("power up...")
    gps.power_on()

    time.sleep(1.0)

    gps.open()
    logger.info(gps)


    # ----------------------------------------------------------------------------------------------------------------

    logger.error("reports...")

    rmc = gps.report(GPRMC)

    if rmc is None:
        exit(1)

    gga = gps.report(GPGGA)

    if gga is None:
        exit(1)

    logger.info("RMC: %s" % rmc)
    logger.info("GGA: %s" % gga)
    logger.info("-")

    logger.info("RMC position: %s, %s  time: %s" % (rmc.loc.deg_lat(), rmc.loc.deg_lng(), rmc.datetime.as_iso8601()))
    logger.info("GGA position: %s, %s" % (gga.loc.deg_lat(), gga.loc.deg_lng()))
    logger.info("-")

    print(JSONify.dumps(GPSDatum.construct_from_gga(gga)))

    # ----------------------------------------------------------------------------------------------------------------

except RuntimeError as ex:
    logger.error(repr(ex))

finally:
    if gps:
        gps.close()
        gps.power_off()

    I2C.Utilities.close()
