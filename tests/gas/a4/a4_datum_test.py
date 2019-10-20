#!/usr/bin/env python3

"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_core.gas.a4.a4_datum import A4Datum


# --------------------------------------------------------------------------------------------------------------------

a4 = A4Datum(0.1234567, 0.6543210)
print(a4)
print("-")

jstr = JSONify.dumps(a4)
print(jstr)
print("-")

