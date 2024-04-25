"""
Created on 14 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Example:
{"bin-boundaries": [0, 27, 57, 95, 140, 205, 296, 473, 682, 920, 1184, 1473, 1786, 2123, 2481, 2861, 4095],
"bin-boundaries-diameter": [0.35, 0.7, 1.1, 1.5, 1.9, 2.4, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 12.4],
"bin-weightings": [1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65, 1.65],
"gain-scaling-coefficient": 1.0, "sample-flow-rate": 3.7, "tof-to-sfr-factor": 87,
"pm-concentration-a": 1.0, "pm-concentration-b": 2.5, "pm-concentration-c": 10.0,
"pvp": 48, "power-status": 0, "max-tof": 4095, "laser-dac": 150, "bin-weighting-index": 2}
"""

from collections import OrderedDict

from scs_core.data.datum import Decode, Encode
from scs_core.data.json import JSONReport


# --------------------------------------------------------------------------------------------------------------------

class OPCFirmwareConf(JSONReport):
    """
    classdocs
    """

    CHARS = 193

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, chars):
        if len(chars) != cls.CHARS:
            raise ValueError(chars)

        # print(chars)

        bin_boundaries = [Decode.unsigned_int(chars[i:i + 2], '<') for i in range(0, 34, 2)]
        bin_boundaries_diameter = [Decode.float(chars[i:i + 4], '<') for i in range(34, 102, 4)]
        bin_weightings = [Decode.float(chars[i:i + 4], '<') for i in range(102, 166, 4)]

        gain_scaling_coefficient = Decode.float(chars[166:170], '<')
        sample_flow_rate = Decode.float(chars[170:174], '<')

        tof_to_sfr_factor = chars[174]

        pm_concentration_a = Decode.float(chars[175:179], '<')
        pm_concentration_b = Decode.float(chars[179:183], '<')
        pm_concentration_c = Decode.float(chars[183:187], '<')

        pvp = chars[187]
        power_status = chars[188]
        max_tof = Decode.unsigned_int(chars[189:191], '<')
        laser_dac = chars[191]

        bin_weighting_index = chars[192]

        return cls(bin_boundaries, bin_boundaries_diameter, bin_weightings,
                   gain_scaling_coefficient, sample_flow_rate, tof_to_sfr_factor,
                   pm_concentration_a, pm_concentration_b, pm_concentration_c,
                   pvp, power_status, max_tof, laser_dac, bin_weighting_index)


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if jdict is None:
            return None

        bin_boundaries = jdict.get('bin-boundaries')
        bin_boundaries_diameter = jdict.get('bin-boundaries-diameter')
        bin_weightings = jdict.get('bin-weightings')

        gain_scaling_coefficient = jdict.get('gain-scaling-coefficient')
        sample_flow_rate = jdict.get('sample-flow-rate')

        tof_to_sfr_factor = jdict.get('tof-to-sfr-factor')

        pm_concentration_a = jdict.get('pm-concentration-a')
        pm_concentration_b = jdict.get('pm-concentration-b')
        pm_concentration_c = jdict.get('pm-concentration-c')

        pvp = jdict.get('pvp')
        power_status = jdict.get('power-status')
        max_tof = jdict.get('max-tof')
        laser_dac = jdict.get('laser-dac')

        bin_weighting_index = jdict.get('bin-weighting-index')

        return cls(bin_boundaries, bin_boundaries_diameter, bin_weightings,
                   gain_scaling_coefficient, sample_flow_rate, tof_to_sfr_factor,
                   pm_concentration_a, pm_concentration_b, pm_concentration_c,
                   pvp, power_status, max_tof, laser_dac, bin_weighting_index)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, bin_boundaries, bin_boundaries_diameter, bin_weightings,
                 gain_scaling_coefficient, sample_flow_rate, tof_to_sfr_factor,
                 pm_concentration_a, pm_concentration_b, pm_concentration_c,
                 pvp, power_status, max_tof, laser_dac, bin_weighting_index):
        """
        Constructor
        """
        self.__bin_boundaries = bin_boundaries                                          # 17 element array of 16-bit int
        self.__bin_boundaries_diameter = bin_boundaries_diameter                        # 17 element array of float
        self.__bin_weightings = bin_weightings                                          # 16 element array of float

        self.__gain_scaling_coefficient = float(gain_scaling_coefficient)               # float
        self.__sample_flow_rate = float(sample_flow_rate)                               # float

        self.__tof_to_sfr_factor = int(tof_to_sfr_factor)                               # 8-bit int

        self.__pm_concentration_a = float(pm_concentration_a)                           # float
        self.__pm_concentration_b = float(pm_concentration_b)                           # float
        self.__pm_concentration_c = float(pm_concentration_c)                           # float

        self.__pvp = int(pvp)                                                           # 8-bit int
        self.__power_status = int(power_status)                                         # 8-bit int
        self.__max_tof = int(max_tof)                                                   # 16-bit int
        self.__laser_dac = int(laser_dac)                                               # 8-bit int

        self.__bin_weighting_index = int(bin_weighting_index)                           # 8-bit int


    def __eq__(self, other):
        try:
            return self.bin_boundaries == other.bin_boundaries and \
               self.bin_boundaries_diameter == other.bin_boundaries_diameter and \
               self.bin_weightings == other.bin_weightings and \
               self.gain_scaling_coefficient == other.gain_scaling_coefficient and \
               self.sample_flow_rate == other.sample_flow_rate and \
               self.tof_to_sfr_factor == other.tof_to_sfr_factor and \
               self.pm_concentration_a == other.pm_concentration_a and \
               self.pm_concentration_b == other.pm_concentration_b and \
               self.pm_concentration_c == other.pm_concentration_c and \
               self.pvp == other.pvp and \
               self.power_status == other.power_status and \
               self.max_tof == other.max_tof and \
               self.laser_dac == other.laser_dac and \
               self.bin_weighting_index == other.bin_weighting_index

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_chars(self):
        chars = []

        for bin_boundary in self.bin_boundaries:
            chars.extend(Encode.unsigned_int(bin_boundary, '<'))

        for bin_boundaries_diameter in self.bin_boundaries_diameter:
            chars.extend(Encode.float(bin_boundaries_diameter, '<'))

        for bin_weighting in self.bin_weightings:
            chars.extend(Encode.float(bin_weighting, '<'))

        chars.extend(Encode.float(self.gain_scaling_coefficient, '<'))

        chars.extend(Encode.float(self.pm_concentration_a, '<'))
        chars.extend(Encode.float(self.pm_concentration_b, '<'))
        chars.extend(Encode.float(self.pm_concentration_c, '<'))

        chars.append(self.tof_to_sfr_factor)

        chars.append(self.pvp)

        chars.extend(Encode.unsigned_int(self.max_tof, '<'))

        return chars

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['bin-boundaries'] = [round(value, 3) for value in self.bin_boundaries]
        jdict['bin-boundaries-diameter'] = [round(value, 3) for value in self.bin_boundaries_diameter]
        jdict['bin-weightings'] = [round(value, 3) for value in self.bin_weightings]

        jdict['gain-scaling-coefficient'] = round(self.gain_scaling_coefficient, 3)
        jdict['sample-flow-rate'] = round(self.sample_flow_rate, 3)

        jdict['tof-to-sfr-factor'] = self.tof_to_sfr_factor

        jdict['pm-concentration-a'] = round(self.pm_concentration_a, 3)
        jdict['pm-concentration-b'] = round(self.pm_concentration_b, 3)
        jdict['pm-concentration-c'] = round(self.pm_concentration_c, 3)

        jdict['pvp'] = self.pvp
        jdict['power-status'] = self.power_status
        jdict['max-tof'] = self.max_tof
        jdict['laser-dac'] = self.laser_dac

        jdict['bin-weighting-index'] = self.bin_weighting_index

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def bin_boundaries(self):
        return self.__bin_boundaries


    @property
    def bin_boundaries_diameter(self):
        return self.__bin_boundaries_diameter


    @property
    def bin_weightings(self):
        return self.__bin_weightings

    @property
    def gain_scaling_coefficient(self):
        return self.__gain_scaling_coefficient


    @property
    def sample_flow_rate(self):
        return self.__sample_flow_rate


    @property
    def tof_to_sfr_factor(self):
        return self.__tof_to_sfr_factor


    @property
    def pm_concentration_a(self):
        return self.__pm_concentration_a


    @property
    def pm_concentration_b(self):
        return self.__pm_concentration_b


    @property
    def pm_concentration_c(self):
        return self.__pm_concentration_c


    @property
    def pvp(self):
        return self.__pvp


    @property
    def power_status(self):
        return self.__power_status


    @property
    def max_tof(self):
        return self.__max_tof


    @property
    def laser_dac(self):
        return self.__laser_dac


    @property
    def bin_weighting_index(self):
        return self.__bin_weighting_index


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCFirmwareConf:{bin_boundaries:%s, bin_boundaries_diameter:%s, bin_weightings:%s " \
               "gain_scaling_coefficient:%s, sample_flow_rate:%s, tof_to_sfr_factor:%s, " \
               "pm_concentration_a:%s, pm_concentration_b:%s, pm_concentration_c:%s, " \
               "pvp:%s, power_status:0x%02x, max_tof:%s, laser_dac:0x%02x, bin_weighting_index:%s}" % \
               (self.bin_boundaries, self.bin_boundaries_diameter, self.bin_weightings,
                self.gain_scaling_coefficient, self.sample_flow_rate, self.tof_to_sfr_factor,
                self.pm_concentration_a, self.pm_concentration_b, self.pm_concentration_c,
                self.pvp, self.power_status, self.max_tof, self.laser_dac, self.bin_weighting_index)
