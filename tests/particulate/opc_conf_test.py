#!/usr/bin/env python3

"""
Created on 23 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

conf = OPCConf("N3", 10, True, False, None)
print(conf)
print("-")

print(JSONify.dumps(conf.as_json()))
print("-")

# conf.save(Host)
conf = OPCConf.load(Host)
print(conf)

print("custom_dev_path: %s" % conf.custom_dev_path)
print("default_dev_path: %s" % conf.default_dev_path)
print("dev_path: %s" % conf.dev_path)

