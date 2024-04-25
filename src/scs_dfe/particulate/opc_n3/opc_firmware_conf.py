"""
Created on 13 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Example:
{"bin-boundaries": [14, 40, 80, 120, 145, 215, 340, 590, 846, 1363, 2029, 2848, 4119, 5527, 7076, 8624, 10204, 11815,
13457, 15897, 18305, 20698, 22966, 25140, 27158],
"bin-boundaries-diameter": [35, 46, 66, 100, 130, 170, 230, 300, 400, 520, 650, 800, 1000, 1200, 1400, 1600, 1800,
2000, 2200, 2500, 2800, 3100, 3400, 3700, 4000],
"bin-weightings": [165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165,
165, 165, 165, 165, 165],
"pm-diameter-a": 100, "pm-diameter-b": 250, "pm-diameter-c": 1000, "max-tof": 4095,
"am-sampling-interval-count": 1, "am-middle-interval-count": 0, "am-max-data_arrays-in-file": 61798,
"am-only-save-pm-data": false, "am-fan-on-in-idle": false, "am-laser-on-in-idle": false,
"tof-to-sfr-factor": 56, "pvp": 48, "bin-weighting-index": 2}
"""

from collections import OrderedDict

from scs_core.data.datum import Decode, Encode
from scs_core.data.json import JSONReport


# --------------------------------------------------------------------------------------------------------------------

class OPCFirmwareConf(JSONReport):
    """
    classdocs
    """

    CHARS = 168

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, chars):
        if len(chars) != cls.CHARS:
            raise ValueError(chars)

        bin_boundaries = [Decode.unsigned_int(chars[i:i + 2], '<') for i in range(0, 50, 2)]
        bin_boundaries_diameter = [Decode.unsigned_int(chars[i:i + 2], '<') for i in range(50, 100, 2)]
        bin_weightings = [Decode.unsigned_int(chars[i:i + 2], '<') for i in range(100, 148, 2)]

        pm_diameter_a = Decode.unsigned_int(chars[148:150], '<')
        pm_diameter_b = Decode.unsigned_int(chars[150:152], '<')
        pm_diameter_c = Decode.unsigned_int(chars[152:154], '<')

        max_tof = Decode.unsigned_int(chars[154:156], '<')

        am_sampling_interval_count = Decode.unsigned_int(chars[156:158], '<')
        am_middle_interval_count = Decode.unsigned_int(chars[158:160], '<')

        am_max_data_arrays_in_file = Decode.unsigned_int(chars[160:162], '<')

        am_only_save_pm_data = chars[162]
        am_fan_on_in_idle = chars[163]
        am_laser_on_in_idle = chars[164]

        tof_to_sfr_factor = chars[165]
        pvp = chars[166]
        bin_weighting_index = chars[167]

        return cls(bin_boundaries, bin_boundaries_diameter, bin_weightings,
                   pm_diameter_a, pm_diameter_b, pm_diameter_c,
                   max_tof, am_sampling_interval_count, am_middle_interval_count,
                   am_max_data_arrays_in_file, am_only_save_pm_data,
                   am_fan_on_in_idle, am_laser_on_in_idle,
                   tof_to_sfr_factor, pvp, bin_weighting_index)


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if jdict is None:
            return None

        bin_boundaries = jdict.get('bin-boundaries')
        bin_boundaries_diameter = jdict.get('bin-boundaries-diameter')
        bin_weightings = jdict.get('bin-weightings')

        pm_diameter_a = jdict.get('pm-diameter-a')
        pm_diameter_b = jdict.get('pm-diameter-b')
        pm_diameter_c = jdict.get('pm-diameter-c')

        max_tof = jdict.get('max-tof')

        am_sampling_interval_count = jdict.get('am-sampling-interval-count')
        am_middle_interval_count = jdict.get('am-middle-interval-count')

        am_max_data_arrays_in_file = jdict.get('am-max-data_arrays-in-file')

        am_only_save_pm_data = jdict.get('am-only-save-pm-data')
        am_fan_on_in_idle = jdict.get('am-fan-on-in-idle')
        am_laser_on_in_idle = jdict.get('am-laser-on-in-idle')

        tof_to_sfr_factor = jdict.get('tof-to-sfr-factor')
        pvp = jdict.get('pvp')
        bin_weighting_index = jdict.get('bin-weighting-index')

        return cls(bin_boundaries, bin_boundaries_diameter, bin_weightings,
                   pm_diameter_a, pm_diameter_b, pm_diameter_c,
                   max_tof, am_sampling_interval_count, am_middle_interval_count,
                   am_max_data_arrays_in_file, am_only_save_pm_data,
                   am_fan_on_in_idle, am_laser_on_in_idle,
                   tof_to_sfr_factor, pvp, bin_weighting_index)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, bin_boundaries, bin_boundaries_diameter, bin_weightings,
                 pm_diameter_a, pm_diameter_b, pm_diameter_c,
                 max_tof, am_sampling_interval_count, am_middle_interval_count,
                 am_max_data_arrays_in_file, am_only_save_pm_data,
                 am_fan_on_in_idle, am_laser_on_in_idle,
                 tof_to_sfr_factor, pvp, bin_weighting_index):
        """
        Constructor
        """
        self.__bin_boundaries = bin_boundaries                                          # 25 element array of int
        self.__bin_boundaries_diameter = bin_boundaries_diameter                        # 25 element array of int
        self.__bin_weightings = bin_weightings                                          # 24 element array of int

        self.__pm_diameter_a = int(pm_diameter_a)                                       # 16-bit int
        self.__pm_diameter_b = int(pm_diameter_b)                                       # 16-bit int
        self.__pm_diameter_c = int(pm_diameter_c)                                       # 16-bit int

        self.__max_tof = int(max_tof)                                                   # 16-bit int

        self.__am_sampling_interval_count = int(am_sampling_interval_count)             # 16-bit int
        self.__am_middle_interval_count = int(am_middle_interval_count)                 # 16-bit int

        self.__am_max_data_arrays_in_file = int(am_max_data_arrays_in_file)             # 16-bit int

        self.__am_only_save_pm_data = bool(am_only_save_pm_data)                        # bool
        self.__am_fan_on_in_idle = bool(am_fan_on_in_idle)                              # bool
        self.__am_laser_on_in_idle = bool(am_laser_on_in_idle)                          # bool

        self.__tof_to_sfr_factor = int(tof_to_sfr_factor)                               # 8-bit int
        self.__pvp = int(pvp)                                                           # 8-bit int
        self.__bin_weighting_index = int(bin_weighting_index)                           # 8-bit int


    def __eq__(self, other):
        try:
            return self.bin_boundaries == other.bin_boundaries and \
               self.bin_boundaries_diameter == other.bin_boundaries_diameter and \
               self.bin_weightings == other.bin_weightings and \
               self.pm_diameter_a == other.pm_diameter_a and \
               self.pm_diameter_b == other.pm_diameter_b and \
               self.pm_diameter_c == other.pm_diameter_c and \
               self.max_tof == other.max_tof and \
               self.am_sampling_interval_count == other.am_sampling_interval_count and \
               self.am_middle_interval_count == other.am_middle_interval_count and \
               self.am_max_data_arrays_in_file == other.am_max_data_arrays_in_file and \
               self.am_only_save_pm_data == other.am_only_save_pm_data and \
               self.am_fan_on_in_idle == other.am_fan_on_in_idle and \
               self.am_laser_on_in_idle == other.am_laser_on_in_idle and \
               self.tof_to_sfr_factor == other.tof_to_sfr_factor and \
               self.pvp == other.pvp and \
               self.bin_weighting_index == other.bin_weighting_index

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_chars(self):
        chars = []

        for bin_boundary in self.bin_boundaries:
            chars.extend(Encode.unsigned_int(bin_boundary, '<'))

        for bin_boundaries_diameter in self.bin_boundaries_diameter:
            chars.extend(Encode.unsigned_int(bin_boundaries_diameter, '<'))

        for bin_weighting in self.bin_weightings:
            chars.extend(Encode.unsigned_int(bin_weighting, '<'))

        chars.extend(Encode.unsigned_int(self.pm_diameter_a, '<'))
        chars.extend(Encode.unsigned_int(self.pm_diameter_b, '<'))
        chars.extend(Encode.unsigned_int(self.pm_diameter_c, '<'))

        chars.extend(Encode.unsigned_int(self.max_tof, '<'))

        chars.extend(Encode.unsigned_int(self.am_sampling_interval_count, '<'))
        chars.extend(Encode.unsigned_int(self.am_middle_interval_count, '<'))

        chars.extend(Encode.unsigned_int(self.am_max_data_arrays_in_file, '<'))

        chars.append(Encode.bool(self.am_only_save_pm_data))
        chars.append(Encode.bool(self.am_fan_on_in_idle))
        chars.append(Encode.bool(self.am_laser_on_in_idle))

        chars.append(self.tof_to_sfr_factor)
        chars.append(self.pvp)

        # bin_weighting_index should be handled elsewhere - see OPCN3.set_firmware_conf(..)

        return chars

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['bin-boundaries'] = self.bin_boundaries
        jdict['bin-boundaries-diameter'] = self.bin_boundaries_diameter
        jdict['bin-weightings'] = self.bin_weightings

        jdict['pm-diameter-a'] = self.pm_diameter_a
        jdict['pm-diameter-b'] = self.pm_diameter_b
        jdict['pm-diameter-c'] = self.pm_diameter_c

        jdict['max-tof'] = self.max_tof

        jdict['am-sampling-interval-count'] = self.am_sampling_interval_count
        jdict['am-middle-interval-count'] = self.am_middle_interval_count

        jdict['am-max-data_arrays-in-file'] = self.am_max_data_arrays_in_file
        jdict['am-only-save-pm-data'] = self.am_only_save_pm_data

        jdict['am-fan-on-in-idle'] = self.am_fan_on_in_idle
        jdict['am-laser-on-in-idle'] = self.am_laser_on_in_idle

        jdict['tof-to-sfr-factor'] = self.tof_to_sfr_factor
        jdict['pvp'] = self.pvp
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
    def pm_diameter_a(self):
        return self.__pm_diameter_a


    @property
    def pm_diameter_b(self):
        return self.__pm_diameter_b


    @property
    def pm_diameter_c(self):
        return self.__pm_diameter_c


    @property
    def max_tof(self):
        return self.__max_tof


    @property
    def am_sampling_interval_count(self):
        return self.__am_sampling_interval_count


    @property
    def am_middle_interval_count(self):
        return self.__am_middle_interval_count


    @property
    def am_max_data_arrays_in_file(self):
        return self.__am_max_data_arrays_in_file


    @property
    def am_only_save_pm_data(self):
        return self.__am_only_save_pm_data


    @property
    def am_fan_on_in_idle(self):
        return self.__am_fan_on_in_idle


    @property
    def am_laser_on_in_idle(self):
        return self.__am_laser_on_in_idle


    @property
    def tof_to_sfr_factor(self):
        return self.__tof_to_sfr_factor


    @property
    def pvp(self):
        return self.__pvp


    @property
    def bin_weighting_index(self):
        return self.__bin_weighting_index


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPCFirmwareConf:{bin_boundaries:%s, bin_boundaries_diameter:%s, bin_weightings:%s " \
               "pm_diameter_a:%s, pm_diameter_b:%s, pm_diameter_c:%s, " \
               "max_tof:%s, am_sampling_interval_count:%s, am_middle_interval_count:%s, " \
               "am_max_data_arrays_in_file:%s, am_only_save_pm_data:%s, " \
               "am_fan_on_in_idle:%s, am_laser_on_in_idle:%s, " \
               "tof_to_sfr_factor:%s, pvp:%s, bin_weighting_index:%s}" % \
               (self.bin_boundaries, self.bin_boundaries_diameter, self.bin_weightings,
                self.pm_diameter_a, self.pm_diameter_b, self.pm_diameter_c,
                self.max_tof, self.am_sampling_interval_count, self.am_middle_interval_count,
                self.am_max_data_arrays_in_file, self.am_only_save_pm_data,
                self.am_fan_on_in_idle, self.am_laser_on_in_idle,
                self.tof_to_sfr_factor, self.pvp, self.bin_weighting_index)
