"""
Created on 16 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which GPS receiver is present, if any, plus sample interval, tally and verbosity

example JSON:
{"model": "PAM7Q", "sample-interval": 10, "tally": 1, "debug": true}
"""

from scs_core.gps.gps_conf import GPSConf as AbstractGPSConf

from scs_dfe.gps.gps_monitor import GPSMonitor
from scs_dfe.gps.pam_7q import PAM7Q
from scs_dfe.gps.sam_m8q import SAMM8Q


# --------------------------------------------------------------------------------------------------------------------

class GPSConf(AbstractGPSConf):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_model(cls, model):
        return model in (PAM7Q.SOURCE, SAMM8Q.SOURCE)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, sample_interval, tally, debug):
        """
        Constructor
        """
        super().__init__(model, sample_interval, tally, debug)


    # ----------------------------------------------------------------------------------------------------------------

    def gps_monitor(self, interface, host):
        gps = self.gps(interface, host)

        return GPSMonitor.construct(gps, self)


    def gps(self, interface, host):
        if self.model is None:
            return None

        if self.model == PAM7Q.SOURCE:
            return PAM7Q(interface, host.gps_device())

        elif self.model == SAMM8Q.SOURCE:
            return SAMM8Q(interface, host.gps_device())

        else:
            raise ValueError('unknown model: %s' % self.model)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSConf(dfe):{model:%s, sample_interval:%s, tally:%s, report_file:%s, debug:%s}" % \
               (self.model, self.sample_interval, self.tally, self.report_file, self.debug)
