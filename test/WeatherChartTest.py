# -*- coding: utf-8 -*-
__author__ = 'takeo'

import unittest
from jma.jmx import WeatherChart
import xml.etree.ElementTree as ET
import geojson



class WeatherChartTestCase(unittest.TestCase):


    isobar_part = """<?xml version="1.0" encoding="UTF-8"?>
<Report xmlns:jmx="http://xml.kishou.go.jp/jmaxml1/" xmlns:jmx_add="http://xml.kishou.go.jp/jmaxml1/addition1/" xmlns="http://xml.kishou.go.jp/jmaxml1/">
    <Body xmlns:jmx_eb="http://xml.kishou.go.jp/jmaxml1/elementBasis1/" xmlns="http://xml.kishou.go.jp/jmaxml1/body/meteorology1/">
     <IsobarPart>
           <jmx_eb:Pressure type="気圧" unit="hPa">988</jmx_eb:Pressure>
           <jmx_eb:Line type="位置（度）">+39.24+135.44/+39.21+135.31/+39.17+135.19/+39.14+135.08/+39.10+134.96/+39.06+134.84/+39.01+134.73/+38.96+134.62/+38.92+134.51/+38.87+134.40/+38.81+134.29/+38.76+134.18/+38.70+134.08/+38.65+133.98/+38.59+133.87/+38.53+133.77/+38.47+133.67/+38.41+133.57/+38.35+133.48/+38.28+133.38/+38.22+133.29/+38.16+133.19/+38.09+133.10/+38.02+133.01/+37.96+132.92/+37.89+132.83/+37.82+132.74/+37.75+132.65/+37.68+132.57/+37.61+132.48/+37.53+132.40/+37.46+132.32/+37.38+132.25/+37.30+132.17/+37.23+132.10/+37.14+132.03/+37.06+131.97/+36.98+131.91/+36.89+131.86/+36.80+131.81/+36.71+131.77/+36.62+131.73/+36.52+131.71/+36.43+131.69/+36.33+131.68/+36.23+131.67/+36.14+131.68/+36.04+131.69/+35.95+131.71/+35.85+131.73/+35.76+131.76/+35.67+131.80/+35.58+131.84/+35.49+131.89/+35.40+131.94/+35.32+132.00/+35.24+132.06/+35.16+132.12/+35.07+132.18/+34.99+132.24/+34.91+132.29/+34.82+132.35/+34.74+132.41/+34.66+132.46/+34.57+132.51/+34.48+132.56/+34.40+132.60/+34.31+132.65/+34.22+132.69/+34.13+132.72/+34.04+132.75/+33.95+132.78/+33.85+132.81/+33.76+132.83/+33.67+132.86/+33.58+132.88/+33.48+132.90/+33.39+132.93/+33.30+132.95/+33.21+132.98/+33.12+133.01/+33.03+133.05/+32.95+133.10/+32.86+133.14/+32.79+133.21/+32.72+133.29/+32.65+133.36/+32.59+133.44/+32.52+133.52/+32.46+133.61/+32.40+133.69/+32.35+133.78/+32.30+133.88/+32.25+133.97/+32.22+134.07/+32.18+134.18/+32.16+134.28/+32.13+134.39/+32.11+134.49/+32.10+134.60/+32.08+134.71/+32.07+134.82/+32.06+134.93/+32.05+135.04/+32.04+135.15/+32.07+135.25/+32.11+135.35/+32.14+135.45/+32.18+135.55/+32.21+135.65/+32.25+135.76/+32.29+135.86/+32.33+135.96/+32.37+136.06/+32.41+136.16/+32.45+136.25/+32.49+136.35/+32.54+136.45/+32.58+136.54/+32.63+136.64/+32.69+136.73/+32.74+136.82/+32.79+136.91/+32.85+137.00/+32.91+137.08/+32.98+137.17/+33.04+137.25/+33.11+137.32/+33.18+137.39/+33.26+137.46/+33.33+137.53/+33.41+137.60/+33.48+137.66/+33.56+137.73/+33.64+137.79/+33.72+137.85/+33.80+137.91/+33.88+137.97/+33.96+138.03/+34.05+138.08/+34.13+138.14/+34.21+138.19/+34.30+138.23/+34.40+138.25/+34.49+138.27/+34.59+138.27/+34.68+138.26/+34.77+138.24/+34.87+138.21/+34.95+138.17/+35.04+138.12/+35.12+138.06/+35.21+138.00/+35.29+137.94/+35.37+137.88/+35.45+137.82/+35.54+137.78/+35.64+137.75/+35.73+137.75/+35.83+137.76/+35.92+137.79/+36.01+137.81/+36.11+137.84/+36.20+137.88/+36.29+137.91/+36.38+137.95/+36.48+137.99/+36.57+138.03/+36.66+138.06/+36.75+138.10/+36.84+138.14/+36.94+138.18/+37.03+138.21/+37.12+138.25/+37.22+138.29/+37.31+138.32/+37.40+138.35/+37.50+138.38/+37.59+138.41/+37.69+138.44/+37.79+138.46/+37.88+138.47/+37.98+138.48/+38.08+138.47/+38.18+138.46/+38.27+138.43/+38.36+138.38/+38.45+138.32/+38.54+138.27/+38.62+138.21/+38.71+138.14/+38.80+138.08/+38.88+138.01/+38.96+137.93/+39.03+137.85/+39.10+137.76/+39.16+137.66/+39.22+137.55/+39.27+137.44/+39.31+137.33/+39.34+137.21/+39.37+137.08/+39.38+136.96/+39.39+136.83/+39.40+136.70/+39.39+136.57/+39.39+136.44/+39.38+136.32/+39.36+136.19/+39.35+136.06/+39.33+135.94/+39.31+135.81/+39.29+135.68/+39.27+135.56/+39.24+135.44/</jmx_eb:Line>
      </IsobarPart>
      </Body>
</Report>
"""


    high_part = """<?xml version="1.0" encoding="UTF-8"?>
<Report xmlns:jmx="http://xml.kishou.go.jp/jmaxml1/" xmlns:jmx_add="http://xml.kishou.go.jp/jmaxml1/addition1/" xmlns="http://xml.kishou.go.jp/jmaxml1/">
    <Body xmlns:jmx_eb="http://xml.kishou.go.jp/jmaxml1/elementBasis1/" xmlns="http://xml.kishou.go.jp/jmaxml1/body/meteorology1/">
             <Item>
                    <Kind>
                        <Property>
                            <Type>高気圧</Type>
                            <CenterPart>
                                <jmx_eb:Coordinate type="中心位置（度）">+48.67+123.55/</jmx_eb:Coordinate>
                                <jmx_eb:Direction condition="不定" type="移動方向" unit="度（真方位）"/>
                                <jmx_eb:Speed description="ほとんど停滞" type="移動速度" unit="km/h"/>
                                <jmx_eb:Speed description="ＡＬＭＯＳＴ　ＳＴＮＲ" type="移動速度" unit="ノット"/>
                                <jmx_eb:Pressure type="中心気圧" unit="hPa">1016</jmx_eb:Pressure>
                            </CenterPart>
                        </Property>
                    </Kind>
                </Item>
      </Body>
</Report>
"""


    def test_parse(self):
        chart = WeatherChart()
        geo = chart.parse('./data/70_58_01_130523_VZSA50.xml')
        print geojson.dumps(geo)


    def test_isobar_part(self):
        chart = WeatherChart()
        ip = ET.fromstring(self.isobar_part)
        result = chart.isobar_part(ip)
        print geojson.dumps(result)
        pass

    def test_high_part(self):
        chart = WeatherChart()
        cp = ET.fromstring(self.high_part)
        result = chart.center_part(cp)
        print geojson.dumps(result)
        pass



if __name__ == '__main__':
    unittest.main()



