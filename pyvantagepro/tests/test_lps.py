from __future__ import unicode_literals

from datetime import datetime
from unittest import TestCase

from pyvantagepro.parser import (LpsDataParserRevB,
                                 VantageProCRC)
from pyvantagepro.utils import hex_to_bytes


class TestLps(TestCase):

    def setUp(self):
        self.data = "4C4F4FEC01FF7F95745D033A860305FF3B012300180007003B01FF7FFF" \
                    "7F4A00FF3CFF65005A0066000000FF78000000FFFF000000000000BF00" \
                    "0000020000C9FF0E720E72BE74FF07060C0E0D090C39160202FF7FFF7FFF " \
                    "7FFF7FFF7FFF7F0A0DCBFD"

        self.bytes = hex_to_bytes(self.data)

        self.item = LpsDataParserRevB(self.bytes, datetime.now())

    def test_check_crc(self):
        '''Test crc verification.'''
        self.assertTrue(VantageProCRC(self.bytes).check())

    def test_heat_index(self):
        self.assertEqual(converter_temp(self.item['HeatIndex']), 38.3)

    def test_wind_chill(self):
        self.assertEqual(converter_temp(self.item['WindChill']), 32.2)

    def test_thsw_index(self):
        self.assertEqual(converter_temp(self.item['THSWIndex']), 38.9)


# Convert F to Cel
def converter_temp(temp_f):
    temp_cels = (temp_f - 32) / 1.8
    return round(temp_cels, 1)
