# -*- coding: utf-8 -*-

import sys
import re
import xml.etree.ElementTree as ET

from geojson import LineString
from geojson import Polygon
from geojson import Feature
from geojson import FeatureCollection


class Pressure():
    def __init__(self, pressure, line):
        self.pressure = pressure
        self.line = line

    @property
    def __geo_interface__(self):
        return {
        "type": "Feature",
        "properties": {"pressure": (self.pressure)},
        "geometry": self.line
        }

class JMX:
    def __init__(self):
        self.ns = {'jmx': 'http://xml.kishou.go.jp/jmaxml1/',
                   'jmx_add': 'http://xml.kishou.go.jp/jmaxml1/addition1/',
                   'jmx_eb': 'http://xml.kishou.go.jp/jmaxml1/elementBasis1/',
                   'jmx_head': 'http://xml.kishou.go.jp/jmaxml1/informationBasis1/',
                   'jmx_body': 'http://xml.kishou.go.jp/jmaxml1/body/meteorology1/'
                   }

        self.re_number = re.compile('[\+\-]\d+\.\d+')


    def parse(self, file):
        root = ET.parse(file)
        self.report(root)

        return

    def report(self, r):
        c = r.find('jmx:Control', self.ns)
        if (c != None):
            self.control(c)

        h = r.find('jmx_head:Head', self.ns)
        if (h != None):
            self.head(h)

        b = r.find('jmx_body:Body', self.ns)
        if (b != None):
            self.body(b)

        return

    def control(self, report):
        return

    def head(self, h):
        self.title = self.getText(h.find('jmx_head:Title', self.ns))
        self.reportTime = self.getText(h.find('jmx_head:ReportDateTime', self.ns))
        self.targetTime = self.getText(h.find('jmx_head:TargetDateTime', self.ns))
        self.eventId = self.getText(h.find('jmx_head:EventID', self.ns))
        self.infoType = self.getText(h.find('jmx_head:InfoType', self.ns))
        self.serial = self.getText(h.find('jmx_head:Serial', self.ns))
        self.inforKind = self.getText(h.find('jmx_head:InfoKind', self.ns))
        self.infoKindVersion = self.getText(h.find('jmx_head:InfoKindVersion', self.ns))
        self.headLine = self.getText(h.find('jmx_head:HeadLine/jmx_head:Text', self.ns))



        #        <Title>地上実況図</Title>
        #        <ReportDateTime>2013-04-06T23:13:00+09:00</ReportDateTime>
        #        <TargetDateTime>2013-04-06T21:00:00+09:00</TargetDateTime>
        #        <EventID/>
        #        <InfoType>発表</InfoType>
        #        <Serial/>
        #        <InfoKind>天気図情報</InfoKind>
        #        <InfoKindVersion>1.1_1</InfoKindVersion>
        #        <Headline>
        #            <Text/>
        #        </Headline>
        return


    def body(self, b):

        minfos = b.findall('jmx_body:MeteorologicalInfos', self.ns)
        for minfo in minfos:
            self.meteo_info(minfo)

        return

    def meteo_info(self, mi):
        items = mi.findall('jmx_body:Item', self.ns)

        for item in items:
            self.item_info(item)

        return

    def item_info(self, item):
        return


    def lineOrPolygon(self, polyline_string):
        line = self.polyline(polyline_string)

        length = len(line)

        if (0 < length):
            first = line[0]
            last = line[length - 1]
        else:
            return None

        if (first == last):
            return Polygon([line])
        else:
            return LineString([line])

    def polyline(self, polyline_string):
        lines = []

        points = polyline_string.split('/')

        for point in points:
            line = self.coordinate_xy(point)

            if (line != None):
                lines.append(line)

        return lines

    def coordinate_xy(self, coordinate_string):
        coordinate = self.re_number.findall(coordinate_string)
        if (coordinate == []):
            return None
        [y, x] = coordinate

        return [float(x), float(y)]

    def getText(self, element):
        result = ''
        if (element != None):
            result = element.text

        if (result == None):
            return ''

        return result


class WeatherChart(JMX):
    def dummy(self):
        pass

    def center_part(self, cp):
        pass


    def isobar_part(self, ip):
        part = ip.find(".//jmx_body:IsobarPart", self.ns)

        pressure_item = part.find("jmx_eb:Pressure", self.ns)
        pressure = pressure_item.text

        line_item = part.find("jmx_eb:Line", self.ns)
        line = line_item.text

        return Pressure(pressure, self.lineOrPolygon(line))



    def item_info(self, mi):




        return
