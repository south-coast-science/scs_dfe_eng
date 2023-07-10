#!/usr/bin/env python3

"""
Created on 7 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.average import Average
from scs_core.data.json import JSONify

from scs_core.gas.scd30.scd30_baseline import SCD30Baseline

from scs_dfe.gas.scd30.scd30 import SCD30

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

scd30 = None
sampling_interval = 3

try:
    I2C.Sensors.open()

    baseline = SCD30Baseline.load(Host, skeleton=True)
    print(baseline)

    scd30 = SCD30(baseline)
    print(scd30)

    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # scd30...

    # TODO: power to gases

    # scd30.reset()

    firmware = scd30.get_firmware_version()
    print("firmware: %s" % str(firmware), file=sys.stderr)


    serial = scd30.get_serial_no()
    print("serial: %s" % str(serial), file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # temperature_offset...

    temperature_offset = scd30.get_temperature_offset()
    print("old temperature_offset: %s" % temperature_offset, file=sys.stderr)

    scd30.set_temperature_offset(0.0)

    temperature_offset = scd30.get_temperature_offset()
    print("new temperature_offset: %s" % temperature_offset, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # altitude...

    altitude = scd30.get_altitude()
    print("old altitude: %s" % altitude, file=sys.stderr)

    scd30.set_altitude(100)

    altitude = scd30.get_altitude()
    print("new altitude: %s" % altitude, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # forced_calib...

    forced_calib = scd30.get_forced_calib()
    print("old forced_calib: %s" % forced_calib, file=sys.stderr)

    scd30.set_forced_calib(1000)

    forced_calib = scd30.get_forced_calib()
    print("new forced_calib: %s" % forced_calib, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # auto_self_calib...

    auto_self_calib = scd30.get_auto_self_calib()
    print("old auto_self_calib: %s" % auto_self_calib, file=sys.stderr)

    scd30.set_auto_self_calib(True)

    auto_self_calib = scd30.get_auto_self_calib()
    print("new auto_self_calib: %s" % auto_self_calib, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # ready...

    ready = scd30.get_data_ready()
    print("ready: %s" % ready, file=sys.stderr)
    print("-", file=sys.stderr)

    if ready:
        measurement = scd30.read_measurement()         # discard reading from previous test


    # ----------------------------------------------------------------------------------------------------------------
    # interval...

    interval = scd30.get_measurement_interval()
    print("old interval: %s" % interval, file=sys.stderr)

    scd30.set_measurement_interval(sampling_interval)

    interval = scd30.get_measurement_interval()
    print("new interval: %s" % interval, file=sys.stderr)
    print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    scd30.stop_periodic_measurement()

    for pressure in (90, 100, 110, None):
        print("pressure: %s" % pressure, file=sys.stderr)

        average = Average()

        scd30.start_periodic_measurement(ambient_pressure_kpa=pressure)

        for _ in range(10):
            start_time = time.time()

            while not scd30.get_data_ready():
                time.sleep(0.1)

            measurement = scd30.read_measurement()
            end_time = time.time() - start_time

            print("%0.1f: %s" % (end_time, JSONify.dumps(measurement.as_json())))
            sys.stdout.flush()

            average.append(measurement)

            scd30.start_periodic_measurement(ambient_pressure_kpa=pressure)

        print("average: %s" % average.mid())
        print("-", file=sys.stderr)


except KeyboardInterrupt:
    print()

finally:
    if scd30:
        scd30.stop_periodic_measurement()

    I2C.Sensors.close()
