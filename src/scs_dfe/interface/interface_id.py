"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"vendor": null, "product": null, "product_id": null, "product_ver": null, "uuid": null}
"""

from os import path

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class InterfaceID(JSONable):
    """
    classdocs
    """
    # TODO: put __DIR on Host

    __DIR =         "/proc/device-tree/hat/"                   # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read(cls, field):
        field_path = cls.__DIR + field

        # check...
        if not path.isfile(field_path):
            return None

        # read...
        file = open(field_path)
        content = file.readline()
        file.close()

        return content.strip("\0")


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__name = self.__read('name')

        self.__vendor = self.__read('vendor')
        self.__product = self.__read('product')
        self.__product_id = self.__read('product_id')
        self.__product_ver = self.__read('product_ver')
        self.__uuid = self.__read('uuid')


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
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
        return "InterfaceID:{name:%s, product:%s, product_id:%s, product_ver:%s, uuid:%s, vendor:%s}" % \
                    (self.name, self.product, self.product_id, self.product_ver, self.uuid, self.vendor)
