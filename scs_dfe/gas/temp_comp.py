"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Ox TempComp(3, 'kp_t',  [ 0.1,   0.1,    0.2,    0.3,    0.7,    1.0,    1.7,    3.0,    4.0]), # from On 2017-02-22
"""

from scs_dfe.gas.sensor import Sensor


# --------------------------------------------------------------------------------------------------------------------

class TempComp(object):
    """
    classdocs
    """

    __MIN_TEMP =        -30
    __MAX_TEMP =         50
    __INTERVAL =         10

    __COMP = None


    # ----------------------------------------------------------------------------------------------------------------

    #                                   ºC:  -30    -20     -10      0       10      20     30       40      50

    @classmethod
    def init(cls):
        cls.__COMP = {
            Sensor.CODE_CO:    TempComp(1, 'n_t', [1.0, 1.0, 1.0, 1.0, -0.2, -0.9, -1.5, -1.5, -1.5]),
            Sensor.CODE_H2S:   TempComp(2, 'k_t', [-1.5, -1.5, -1.5, -0.5, 0.5, 1.0, 0.8, 0.5, 0.3]),
            Sensor.CODE_NO:    TempComp(3, 'kp_t', [0.7, 0.7, 0.7, 0.7, 0.8, 1.0, 1.2, 1.4, 1.6]),
            Sensor.CODE_NO2:   TempComp(1, 'n_t', [0.8, 0.8, 1.0, 1.2, 1.6, 1.8, 1.9, 2.5, 3.6]),
            Sensor.CODE_OX:    None,
            Sensor.CODE_SO2:   TempComp(4, 'kpp_t', [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 25.0, 45.0])
        }


    @classmethod
    def find(cls, sensor_code):
        if sensor_code not in cls.__COMP:
            raise ValueError("TempComp.find: unrecognised sensor code: %s." % sensor_code)

        return cls.__COMP[sensor_code]


    @classmethod
    def in_range(cls, temp):
        if temp < cls.__MIN_TEMP or temp > cls.__MAX_TEMP:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, algorithm, factor, values):
        """
        Constructor
        """
        length = (TempComp.__MAX_TEMP - TempComp.__MIN_TEMP) // TempComp.__INTERVAL + 1

        if len(values) != length:
            raise ValueError("TempComp: value count should be %d." % length)

        self.__algorithm = algorithm    # int
        self.__factor = factor          # string
        self.__values = values          # array of float


    # ----------------------------------------------------------------------------------------------------------------

    def correct(self, calib, temp, we_t, ae_t):
        """
        Find corrected we.
        """
        if not TempComp.in_range(temp):
            return None

        if self.__algorithm == 1:
            return self.__eq1(temp, we_t, ae_t)

        if self.__algorithm == 2:
            return self.__eq2(temp, we_t, ae_t, calib.we_cal_mv, calib.ae_cal_mv)

        if self.__algorithm == 3:
            return self.__eq3(temp, we_t, ae_t, calib.we_cal_mv, calib.ae_cal_mv)

        if self.__algorithm == 4:
            return self.__eq4(temp, we_t, calib.we_cal_mv)

        raise ValueError("TempComp.conv: unrecognised algorithm: %d." % self.__algorithm)


    # ----------------------------------------------------------------------------------------------------------------

    def __eq1(self, temp, we_t, ae_t):
        n_t = self.cf_t(temp)

        return we_t - n_t * ae_t


    def __eq2(self, temp, we_t, ae_t, we_cal_mv, ae_cal_mv):
        k_t = self.cf_t(temp)

        return we_t - k_t * (we_cal_mv / ae_cal_mv) * ae_t


    def __eq3(self, temp, we_t, ae_t, we_cal_mv, ae_cal_mv):
        kp_t = self.cf_t(temp)

        return we_t - kp_t * (we_cal_mv - ae_cal_mv) * ae_t


    def __eq4(self, temp, we_t, we_cal_mv):
        kpp_t = self.cf_t(temp)

        # print("we_t: %f" % we_t)
        # print("we_cal_mv: %f" % we_cal_mv)

        return we_t - we_cal_mv - kpp_t


    # ----------------------------------------------------------------------------------------------------------------

    def cf_t(self, temp):
        """
        Find the linear-interpolated temperature compensation factor.
        """
        index = int((temp - TempComp.__MIN_TEMP) // TempComp.__INTERVAL)        # index of start of interval

        # on boundary...
        if temp % TempComp.__INTERVAL == 0:
            return self.__values[index]

        # all others...
        y1 = self.__values[index]                                               # y value at start of interval
        y2 = self.__values[index + 1]                                           # y value at end of interval

        delta_y = y2 - y1

        delta_x = (temp % TempComp.__INTERVAL) / TempComp.__INTERVAL            # proportion of interval

        return y1 + (delta_y * delta_x)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def algorithm(self):
        return self.__algorithm


    @property
    def factor(self):
        return self.__factor


    @property
    def values(self):
        return self.__values


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TempComp:{algorithm:%d, factor:%s, values:%s}" % (self.algorithm, self.factor, self.values)
