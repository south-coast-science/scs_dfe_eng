#!/usr/bin/env python3

"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.pid.pid_calib import PIDCalib, PIDTestCalib


# --------------------------------------------------------------------------------------------------------------------

serial_number = "143456789"
sensor_type = "PIDNH"

pidELC = 275
pidSENS = 0.321
bumpSENS = 0.9

# --------------------------------------------------------------------------------------------------------------------

calib = PIDCalib(serial_number, sensor_type, pidELC, pidSENS, PIDTestCalib(bumpSENS, LocalizedDatetime.now()))
print(calib)
print("-")

jstr = JSONify.dumps(calib)
print(jstr)
print("-")
