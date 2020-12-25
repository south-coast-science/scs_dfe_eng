#!/usr/bin/env python3

"""
Created on 12 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.interface.pzhb.pzhb_mcu_t1_f1 import PZHBMCUt1f1

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

header = PZHBMCUt1f1(PZHBMCUt1f1.DEFAULT_ADDR)
print(header)


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    ident = header.version_ident()
    print("ident: [%s]" % ident)

    tag = header.version_tag()
    print("tag: [%s]" % tag)

    print("-")

    v_batt = header.read_batt_v()
    print("v_batt: %0.1f V" % v_batt)

    c_current = header.read_current_count()
    print("c_current: %d" % c_current)

    print("-")

    header.button_enable()

    count = 0

    while True:
        time.sleep(1)

        button_pressed = header.button_pressed()

        if button_pressed:
            print("button pressed: %d" % count)
            break

        count += 1

finally:
    I2C.Sensors.close()
