"""
Created on 10 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Analog Front-End (AFE)

Warning: If an Ox sensor is present, the NO2 sensor must have a lower sensor number (SN) than the Ox sensor,
otherwise the NO2 cross-sensitivity concentration will not be found.
"""

import time

from scs_core.data.str import Str
from scs_core.gas.afe.afe_datum import AFEDatum

from scs_dfe.gas.afe.ads1115 import ADS1115
from scs_dfe.gas.afe.mcp342x import MCP342X
from scs_dfe.gas.gas_sensor_interface import GasSensorInterface


# --------------------------------------------------------------------------------------------------------------------

class AFE(GasSensorInterface):
    """
    Alphasense Analogue Front-End (AFE) with Ti ADS1115 ADC (gases), Microchip Technology MCP342X ADC (Pt1000 temp)
    """

    __SRC = 'AFE'               # Alphasense analogue front end

    @classmethod
    def src(cls):
        return cls.__SRC

    # ----------------------------------------------------------------------------------------------------------------

    __RATE = ADS1115.RATE_8
    __MUX = (ADS1115.MUX_A3_GND, ADS1115.MUX_A2_GND, ADS1115.MUX_A1_GND, ADS1115.MUX_A0_GND)

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __no2_sample(cls, samples):
        for sample in samples:
            if sample[0] == 'NO2':
                return sample[1]

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, pt1000, sensors):
        """
        Constructor
        """
        self.__pt1000 = pt1000
        self.__sensors = sensors

        self.__wrk_adc = None if not sensors else ADS1115(ADS1115.ADDR_WRK, AFE.__RATE)
        self.__aux_adc = None if not sensors else ADS1115(ADS1115.ADDR_AUX, AFE.__RATE) if sensors else None

        self.__pt1000_adc = None if pt1000 is None else interface.pt1000_adc(MCP342X.GAIN_4, MCP342X.RATE_15)

        self.__tconv = None if self.__wrk_adc is None else self.__wrk_adc.tconv


    # ----------------------------------------------------------------------------------------------------------------
    # business methods...

    def adc_versions(self):
        return tuple('ADS1115', )


    def sample(self, sht_datum=None):
        # temperature...
        pt1000_datum = self.sample_pt1000()
        temp = self.sample_temp(sht_datum)

        # gases...
        samples = []
        no2_sample = None

        for sensor_index in range(len(self.__sensors)):
            sensor = self.__sensors[sensor_index]

            if sensor is None:
                continue

            # cross-sensitivity sample...
            if sensor.has_no2_cross_sensitivity():
                no2_sample = AFE.__no2_sample(samples)

            # sample...
            sample = sensor.sample(self, temp, sensor_index, no2_sample)

            samples.append((sensor.gas_name, sample))

        return AFEDatum(pt1000_datum, *samples)


    def sample_station(self, sn, sht_datum=None):
        # temperature...
        pt1000_datum = self.sample_pt1000()
        temp = self.sample_temp(sht_datum)

        # gas...
        index = sn - 1

        sensor = self.__sensors[index]

        if sensor is None:
            return AFEDatum(pt1000_datum)

        # cross-sensitivity sample...
        if sensor.has_no2_cross_sensitivity():
            no2_index, no2_sensor = self.__no2_sensor()
            no2_sample = no2_sensor.sample(self, temp, no2_index)
        else:
            no2_sample = None

        # sample...
        sample = sensor.sample(self, temp, index, no2_sample)

        return AFEDatum(pt1000_datum, (sensor.gas_name, sample))


    def null_datum(self):
        pt1000_datum = self.sample_pt1000()

        samples = []

        for sensor_index in range(len(self.__sensors)):
            sensor = self.__sensors[sensor_index]

            if sensor is None:
                continue

            samples.append((sensor.gas_name, sensor.null_datum()))

        return AFEDatum(pt1000_datum, *samples)


    def sample_temp(self, sht_datum):
        if sht_datum is not None:
            return sht_datum.temp

        pt1000_datum = self.sample_pt1000()

        return None if pt1000_datum is None else pt1000_datum.temp


    def sample_pt1000(self):
        if self.__pt1000 is None:
            return None

        try:
            return self.__pt1000.sample(self)

        except OSError:
            return self.__pt1000.null_datum()


    # ----------------------------------------------------------------------------------------------------------------
    # electrochem callbacks...

    def sample_raw_wrk_aux(self, sensor_index, gain_index):
        try:
            gain = ADS1115.gain(gain_index)

            mux = AFE.__MUX[sensor_index]

            self.__wrk_adc.start_conversion(mux, gain)
            self.__aux_adc.start_conversion(mux, gain)

            time.sleep(self.__tconv)

            we_v = self.__wrk_adc.read_conversion()
            ae_v = self.__aux_adc.read_conversion()

            return we_v, ae_v

        finally:
            self.__wrk_adc.release_lock()
            self.__aux_adc.release_lock()


    def sample_raw_wrk(self, sensor_index, gain_index):
        try:
            gain = ADS1115.gain(gain_index)

            mux = AFE.__MUX[sensor_index]

            self.__wrk_adc.start_conversion(mux, gain)

            time.sleep(self.__tconv)

            we_v = self.__wrk_adc.read_conversion()

            return we_v

        finally:
            self.__wrk_adc.release_lock()


    def sample_raw_tmp(self):
        if self.__pt1000_adc is None:
            return None

        try:
            self.__pt1000_adc.start_conversion()

            time.sleep(self.__pt1000_adc.tconv)

            return self.__pt1000_adc.read_conversion()

        finally:
            self.__pt1000_adc.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __no2_sensor(self):
        for index in range(len(self.__sensors)):
            if self.__sensors[index].gas_name == 'NO2':
                return index, self.__sensors[index]

        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sensors(self):
        return self.__sensors


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        sensors = Str.collection(self.__sensors)

        return "AFE:{pt1000:%s, sensors:%s, tconv:%0.3f, wrk_adc:%s, aux_adc:%s, pt1000_adc:%s}" % \
            (self.__pt1000, sensors, self.__tconv, self.__wrk_adc, self.__aux_adc, self.__pt1000_adc)
