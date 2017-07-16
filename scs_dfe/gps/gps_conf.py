"""
Created on 16 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which GPS receiver is present, if any

example JSON:
{"model": null}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_dfe.gps.pam7q import PAM7Q


# --------------------------------------------------------------------------------------------------------------------

class GPSConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "gps_conf.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return GPSConf(None)

        model = jdict.get('model')

        return GPSConf(model)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model):
        """
        Constructor
        """
        self.__model = model


    # ----------------------------------------------------------------------------------------------------------------

    def gps(self):
        if self.model is None:
            return None

        if self.model == 'PAM7Q':
            return PAM7Q()

        raise ValueError('unknown model: %s' % self.model)


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__model

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSConf:{model:%s}" % self.model