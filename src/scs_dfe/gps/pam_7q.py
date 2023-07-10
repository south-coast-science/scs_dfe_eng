"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.u-blox.com/en/product/pam-7q-module

example sentence set:
$GPGLL,5049.38388,N,00007.37172,W,113111.00,A,A*7E
$GPRMC,113112.00,A,5049.38381,N,00007.37173,W,0.017,,201119,,,A*60
$GPVTG,,T,,M,0.017,N,0.032,K,A*24
$GPGGA,113112.00,5049.38381,N,00007.37173,W,1,04,2.48,36.5,M,45.4,M,,*7F
$GPGSA,A,3,07,19,06,23,,,,,,,,,4.22,2.48,3.41*06
$GPGSV,2,1,08,06,66,247,39,07,24,164,47,09,,,33,17,04,214,39*48
$GPGSV,2,2,08,19,15,227,50,23,57,066,33,24,,,30,26,,,29*76
"""

from scs_core.position.nmea.gpgga import GPGGA
from scs_core.position.nmea.gpgll import GPGLL
from scs_core.position.nmea.gpgsa import GPGSA
from scs_core.position.nmea.gpgsv import GPGSV
from scs_core.position.nmea.gprmc import GPRMC
from scs_core.position.nmea.gpvtg import GPVTG
from scs_core.position.nmea.nmea_report import NMEAReport

from scs_dfe.gps.gps import GPS


# --------------------------------------------------------------------------------------------------------------------

class PAM7Q(GPS):
    """
    u-blox 7 GPS Antenna Module
    """

    SOURCE =                    "PAM7Q"

    # ----------------------------------------------------------------------------------------------------------------

    __BAUD_RATE =               9600
    __BOOT_DELAY =              0.500           # seconds

    __SERIAL_LOCK_TIMEOUT =     6.0
    __SERIAL_COMMS_TIMEOUT =    5.0

    __EOL =                     "\r\n"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def baud_rate(cls):
        return cls.__BAUD_RATE


    @classmethod
    def boot_time(cls):
        return cls.__BOOT_DELAY


    @classmethod
    def serial_lock_timeout(cls):
        return cls.__SERIAL_LOCK_TIMEOUT


    @classmethod
    def serial_comms_timeout(cls):
        return cls.__SERIAL_COMMS_TIMEOUT


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, uart):
        super().__init__(interface, uart)


    # ----------------------------------------------------------------------------------------------------------------

    def report(self, message_class):
        self._serial.flush_input()

        while True:
            try:
                sentence = self.__sentence()
            except TimeoutError:
                return None

            if sentence.message_id in message_class.MESSAGE_IDS:
                return message_class.construct(sentence)


    def report_all(self):
        self._serial.flush_input()

        reports = []

        # find start...
        while True:
            sentence = self.__sentence()

            if sentence.message_id in GPGLL.MESSAGE_IDS:
                break

        reports.append(GPGLL.construct(sentence))

        reports.append(GPRMC.construct(self.__sentence()))
        reports.append(GPVTG.construct(self.__sentence()))
        reports.append(GPGGA.construct(self.__sentence()))
        reports.append(GPGSA.construct(self.__sentence()))

        # find end...
        while True:
            sentence = self.__sentence()

            if sentence.message_id not in GPGSV.MESSAGE_IDS:
                break

            reports.append(GPGSV.construct(sentence))

        return reports


    # ----------------------------------------------------------------------------------------------------------------

    def __sentence(self):
        while True:
            try:
                line = self._serial.read_line(eol=self.__EOL, timeout=self.__SERIAL_COMMS_TIMEOUT)
                self._logger.debug("sentence:[%s]" % line)

                return NMEAReport.construct(line)

            except (IndexError, UnicodeDecodeError, ValueError):
                continue
