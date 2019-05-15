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

from pyvantagepro.logger import active_logger
from pyvantagepro.parser import (LoopDataParserRevB, LpsDataParserRevB,
                                 VantageProCRC, pack_datetime,
                                 unpack_datetime, pack_dmp_date_time,
                                 unpack_dmp_date_time)
from pyvantagepro.utils import hex_to_bytes

# active logging for tests
active_logger()


class TestLoopDataParser():
    ''' Test parser.'''

    def __init__(self):
        '''Setup common data.'''
        # self.data = "4C4F4FC4006802547B52031EFF7FFFFFFF7FFFFFFFFFFFFF" \
        #             "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F0000" \
        #             "FFFF000000003C03000000000000FFFFFFFFFFFFFF000000" \
        #             "0000000000000000000000000000008C00060C610183070A" \
        #             "0D2A3C"
        # self.data = "4C4F4F14005408ED744E03474C0302041201FFFFFFFFFFFFFFFFFFFFFF" \
        #             "FFFFFFFF4AFFFFFFFFFFFFFF0000FFB3020000FFFF00001E0775120F005C" \
        #             "01D606FFFFFFFFFFFFFF0000000000000000000000000000000000000803" \
        #             "062D0B00B5040A0D7CF6"
        # self.data = "4C4F4F0001FF7FEF742D0335660305FFE000400042000C003B01FF7FFF" \
        #             "7F4B00FF44FF600057006D000000FF12040000FFFF000000000000350000" \
        #             "00020000C9FF657265721775FF00100B080D100C28160202FF7FFF7FFF7F" \
        #             "FF7FFF7FFF7F0A0DDD2B"

        # self.data = "4C4F4FEC01FF7F95745D033A860305FF3B012300180007003B01FF7FFF" \
        #             "7F4A00FF3CFF65005A0066000000FF78000000FFFF000000000000BF00" \
        #             "0000020000C9FF0E720E72BE74FF07060C0E0D090C39160202FF7FFF7FFF "\
        #             "7FFF7FFF7FFF7F0A0DCBFD"
        # self.bytes = hex_to_bytes(self.data)

        # Dados coletados 15/05/19 às 18:35
        self.data = "4C4F4F1401FF7F9674520349060300FF5E010000000000006801FF7FFF7" \
                    "F4A00FF58FF52004D0051000000FF0000AA009357AA00000000002D00AA" \
                    "00020000C9FF08720872B874FF021114100A040D34170202FF7FFF7FFF7" \
                    "FFF7FFF7FFF7F0A0DCF98"

        self.bytes = hex_to_bytes(self.data)

    def test_check_crc(self):
        '''Test crc verification.'''
        assert VantageProCRC(self.bytes).check()

    def test_check_raw_data(self):
        item = LpsDataParserRevB(self.bytes, datetime.now())
        assert item.raw.replace(' ', '') == self.data
        assert item.raw_bytes == self.bytes

    def test_unpack(self):
        '''Test unpack loop packet.'''
        item = LpsDataParserRevB(self.bytes, datetime.now())

        # assert item['TempIn'] == 85.0
        # assert item['HeatIndex'] == 85.0

        print('Heat', converter_temp(int(item['HeatIndex'])))
        print('Last', item['Last15Rain'])
        print('Dew', converter_temp(int(item['DewPoint'])))
        print('Wind', converter_temp(int(item['WindChill'])))
        print('THSW', converter_temp(int(item['THSWIndex'])))
        print(converter_temp(int(self.data[70:72])))
        print(len(self.bytes))
        # assert converter_temp(int(item['HeatIndex'])) == 27.8
        # assert converter_temp(int(item['DewPoint'])) == 23.3
        # assert converter_temp(int(item['WindChill'])) == 25.0
        # assert converter_temp(int(item['THSWIndex'])) == 27.2





        # assert item['Alarm01HighLeafTemp'] == 0
        # assert item['Alarm01HighLeafWet'] == 0
        # assert item['Alarm01HighSoilMois'] == 0
        # assert item['Alarm01HighSoilTemp'] == 0
        # assert item['Alarm01LowLeafTemp'] == 0
        # assert item['Alarm01LowLeafWet'] == 0
        # assert item['Alarm01LowSoilMois'] == 0
        # assert item['Alarm01LowSoilTemp'] == 0
        # assert item['AlarmEx01HighHum'] == 0
        # assert item['AlarmInFallBarTrend'] == 0
        # assert item['AlarmOut10minAvgSpeed'] == 0
        # assert item['AlarmRain15min'] == 0
        # assert item['BarTrend'] == 196
        # assert item['Barometer'] == 31.572
        # assert item['BatteryStatus'] == 0
        # assert item['BatteryVolts'] == 0.8203125
        # assert item['ETDay'] == 0.0
        # assert item['ETMonth'] == 0.0
        # assert item['ETYear'] == 0.0
        # assert item['ExtraTemps01'] == 255
        # assert item['ForecastIcon'] == 6
        # assert item['ForecastRuleNo'] == 12
        # assert item['HumExtra01'] == 255
        # assert item['HumIn'] == 30
        # assert item['HumOut'] == 255
        # assert item['LeafTemps01'] == 255
        # assert item['LeafWetness01'] == 255
        # assert item['LeafWetness04'] == 0
        # assert item['RainDay'] == 0.0
        # assert item['RainMonth'] == 0.0
        # assert item['RainRate'] == 655.35
        # assert item['RainStorm'] == 0.0
        # assert item['RainYear'] == 8.28
        # assert item['SoilMoist01'] == 255
        # assert item['SolarRad'] == 32767
        # assert item['StormStartDate'] == '2127-15-31'
        # assert item['SunRise'] == '03:53'
        # assert item['SunSet'] == '19:23'
        # assert item['TempIn'] == 85.0
        # assert item['TempOut'] == 3276.7
        # assert item['UV'] == 255
        # assert item['WindDir'] == 32767
        # assert item['WindSpeed'] == 255
        # assert item['WindSpeed10Min'] == 255


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


def converter_temp(temp_f):
    temp_cels = (temp_f - 32) / 1.8
    return round(temp_cels, 1)


teste = TestLoopDataParser()
# teste.test_check_raw_data()
teste.test_check_crc()
teste.test_unpack()
