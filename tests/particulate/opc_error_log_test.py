#!/usr/bin/env python3

"""
Created on 9 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.particulate.opc_error_log import OPCErrorLog, OPCErrorLogEntry

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

log = OPCErrorLog.load(Host)
print("rows: %s" % OPCErrorLog.rows(Host))

if log:
    print("log: %s" % log)
    print("len: %s" % len(log))
    print("last_modified: %s" % log.last_modified)

    print("trim... 5")
    OPCErrorLog.trim(Host, 5)

    log = OPCErrorLog.load(Host)
    print("rows: %s" % OPCErrorLog.rows(Host))

    print("log: %s" % log)
    print("len: %s" % len(log))
print("-")



# --------------------------------------------------------------------------------------------------------------------

rec = LocalizedDatetime.now()
error = ValueError("checksum error")

entry = OPCErrorLogEntry(rec, str(error))
print("entry: %s" % entry)

OPCErrorLog.save_entry(Host, entry, trim=True)
