# coding: utf8
'''
    pyvantagepro.tests.test_link
    ----------------------------

    The pyvantagepro test suite.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import unicode_literals
from datetime import datetime
import struct
from unittest import TestCase
from parameterized import parameterized

from pyvantagepro.logger import active_logger
from pyvantagepro.parser import (LoopDataParserRevB, LpsDataParserRevB,
                                 VantageProCRC, pack_datetime,
                                 unpack_datetime, pack_dmp_date_time,
                                 unpack_dmp_date_time)
from pyvantagepro.utils import hex_to_bytes

# active logging for tests
active_logger()


class TestLoopDataParser(object):
    """Test parser."""

    # Dados coletados 15/05/19 às 18:35
    data = (
        "4C4F4F1401FF7F9674520349060300FF5E010000000000006801FF7FFF7"
        "F4A00FF58FF52004D0051000000FF0000AA009357AA00000000002D00AA"
        "00020000C9FF08720872B874FF021114100A040D34170202FF7FFF7FFF7"
        "FFF7FFF7FFF7F0A0DCF98"
    )
    bytes = hex_to_bytes(data)

    lps = LpsDataParserRevB(bytes)

    def test_check_crc(self):
        """Test crc verification."""
        assert VantageProCRC(self.bytes).check()

    def test_check_raw_data(self):
        assert self.lps.raw.replace(' ', '') == self.data
        assert self.lps.raw_bytes == self.bytes

    UNPACKED = [
        ('AbsoluteBarometricPressure', 29192),
        ('AltimeterSetting', 29880),
        ('BarTrend', 20),
        ('Barometer', 29846),
        ('BarometricReductionMethod', 2),
        ('BarometricSensorRawReading', 29192),
        ('Barometriccalibrationnumber', 65481),
        ('CR', 13),
        ('CRC', 39119),
        ('DailyET', 45),
        # ('DailyRain', 'H'),
        # ('DewPoint', 'H'),
        ('HeatIndex', 82),
        # ('IndextotheMinutewithinanHour', 'B'),
        ('InsideHumidity', 73),
        ('InsideTemperature', 85),
        # ('LF', 'B'),
        # ('Last15minRain', 'H'),
        # ('Last24HourRain', 'H'),
        # ('LastHourRain', 'H'),
        # ('Next10minWindSpeedGraphPointer', 'B'),
        # ('Next15minWindSpeedGraphPointer', 'B'),
        # ('NextDailyWindSpeedGraphPointer', 'B'),
        # ('NextHourlyWindSpeedGraphPointer', 'B'),
        # ('NextMinuteRainGraphPointer', 'B'),
        # ('NextMonthlyRain', 'B'),
        # ('NextRainStormGraphPointer', 'B'),
        # ('NextSeasonalRain', 'B'),
        # ('NextYearlyRain', 'B'),
        # ('OutsideHumidity', 255),
        ('OutsideTemperature', 774),
        # ('PacketType', 'B'),
        # ('RainRate', 'H'),
        # ('SolarRadiation', 'H'),
        # ('StartDateofcurrentStorm', 'H'),
        # ('StormRain', 'H'),
        # ('THSWIndex', 133.33),
        ('UV', 255),
        # ('UserenteredBarometricOffset', 'H'),
        ('WindChill', 77),
        ('WindDirection', 350),
        # ('WindDirectionforthe10MinWindGuest', 'H'),
        ('WindSpeed', 0),
        # ('_10MinAvgWindSpeed', 'H'),
        # ('_10MinWindGust', 'H'),
        # ('_2MinAvgWindSpeed', 'H')
    ]

    @parameterized.expand(UNPACKED)
    def test_unpack(self, name, expected):
        lps = self.lps
        assert getattr(lps, name) == expected


def test_datetime_parser():
    '''Test pack and unpack datetime.'''
    data = hex_to_bytes("25 35 0A 07 06 70 60 BA")
    assert VantageProCRC(data).check()
    date = unpack_datetime(data)
    assert date == datetime(2012, 6, 7, 10, 53, 37)
    assert data == pack_datetime(date)


def test_dump_date_time():
    d = datetime(2012, 10, 26, 10, 10)
    packed = pack_dmp_date_time(d)
    date, time, _ = struct.unpack(b"HHH", packed)
    assert d == unpack_dmp_date_time(date, time)

