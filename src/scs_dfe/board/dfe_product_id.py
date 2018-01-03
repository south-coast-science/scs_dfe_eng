"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os.path

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DFEProductID(JSONable):
    """
    classdocs
    """
    # TODO: put __DIR on Host

    __DIR =         "/proc/device-tree/hat/"                   # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read(cls, field):
        path = cls.__DIR + field

        # check...
        if not os.path.isfile(path):
            return None

        # read...
        file = open(path, "r")
        content = file.readline()
        file.close()

        return content.strip("\0")


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__name = DFEProductID.__read('name')

        self.__vendor = DFEProductID.__read('vendor')
        self.__product = DFEProductID.__read('product')
        self.__product_id = DFEProductID.__read('product_id')
        self.__product_ver = DFEProductID.__read('product_ver')
        self.__uuid = DFEProductID.__read('uuid')


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['vendor'] = self.vendor
        jdict['product'] = self.product
        jdict['product_id'] = self.product_id
        jdict['product_ver'] = self.product_ver
        jdict['uuid'] = self.uuid

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def product(self):
        return self.__product


    @property
    def product_id(self):
        return self.__product_id


    @property
    def product_ver(self):
        return self.__product_ver


    @property
    def uuid(self):
        return self.__uuid


    @property
    def vendor(self):
        return self.__vendor


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DFEProductID:{name:%s, product:%s, product_id:%s, product_ver:%s, uuid:%s, vendor:%s}" % \
                    (self.name, self.product, self.product_id, self.product_ver, self.uuid, self.vendor)
