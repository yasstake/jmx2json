# -*- coding: utf-8 -*-

import sys
import re
import xml.etree.ElementTree as ET

from geojson import LineString
from geojson import Polygon
from geojson import Point
from geojson import Feature
from geojson import FeatureCollection
import geojson


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
        return self.report(root)

    def report(self, r):

        properties = {}
        features = []

        c = r.find('jmx:Control', self.ns)
        if (c != None):
            self.control(c)

        h = r.find('jmx_head:Head', self.ns)
        if (h != None):
            properties = self.head(h)

        b = r.find('jmx_body:Body', self.ns)
        if (b != None):
            features = self.body(b)

        return FeatureCollection(*features)

    def control(self, report):
        return

    def head(self, h):
        property = {}
        property["Title"] = self.getText(h.find('jmx_head:Title', self.ns))
        property["ReportDateTime"] = self.getText(h.find('jmx_head:ReportDateTime', self.ns))
        property["TargetDateTime"] = self.getText(h.find('jmx_head:TargetDateTime', self.ns))
        property["EventID"] = self.getText(h.find('jmx_head:EventID', self.ns))
        property["InfoType"] = self.getText(h.find('jmx_head:InfoType', self.ns))
        property["Serial"] = self.getText(h.find('jmx_head:Serial', self.ns))
        property["InfoKind"] = self.getText(h.find('jmx_head:InfoKind', self.ns))
        property["InfoKindVersion"] = self.getText(h.find('jmx_head:InfoKindVersion', self.ns))
        property["Text"] = self.getText(h.find('jmx_head:HeadLine/jmx_head:Text', self.ns))

        return property


    def body(self, b):

        info = []

        minfos = b.findall('jmx_body:MeteorologicalInfos', self.ns)
        for minfo in minfos:
            info.append(self.meteo_info(minfo))

        return info

    def meteo_info(self, mi):
        items = mi.findall('.//jmx_body:Item', self.ns)

        item_infos = []

        for item in items:
            iteminfo = self.item_info(item)
            if(iteminfo != None):
                item_infos.append(iteminfo)

        return item_infos

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
            return LineString(line)

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

        return (float(x), float(y))

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

    def center_part(self, cp, properties = {}):
        center = cp.find(".//jmx_body:CenterPart", self.ns)

        coordinate_item = center.find(".//jmx_eb:Coordinate", self.ns)
        [x, y] = self.coordinate_xy(coordinate_item.text);

        direction_item  = center.find(".//jmx_eb:Direction", self.ns)
        if(direction_item.text):
            direction = int(direction_item.text);
            properties['Direction'] = direction

        speed_items      = center.findall('.//jmx_eb:Speed', self.ns)

        for speed_item in speed_items:
            if(speed_item.get('unit') == u'ノット'):
                if(speed_item.text):
                    knot = int(speed_item.text)
                    properties['knot'] = knot

            if(speed_item.get('unit') == 'km/h'):
                if(speed_item.text):
                    kmh = int(speed_item.text)
                    properties['kmh'] = kmh

        pressure_item = center.find('.//jmx_eb:Pressure', self.ns)
        pressure = int(pressure_item.text);
        properties["Pressure"] = pressure

        return Feature(geometry = Point((x, y)), properties = properties)


    def isobar_part(self, ip, properties = {}):
        part = ip.find(".//jmx_body:IsobarPart", self.ns)

        pressure_item = part.find("jmx_eb:Pressure", self.ns)
        pressure = pressure_item.text
        properties["PresssureLevel"] = pressure

        line_item = part.find(".//jmx_eb:Line", self.ns)
        line = line_item.text

        return Feature(geometry = self.lineOrPolygon(line), properties= properties)


    def corrdinate_part(self, cp, properties = {}):
        line_item = cp.find(".//jmx_eb:Line", self.ns)
        line = line_item.text

        return Feature(geometry = self.lineOrPolygon(line), properties= properties)


    def item_info(self, item):
        item_type = item.find(".//jmx_body:Type", self.ns).text

        if item_type == u'等圧線':
            property = {"LinePart": "isobar"}
            return self.isobar_part(item, property)

        elif item_type == u'低気圧':
            property = {"CenterType": "low"}
            return self.center_part(item, property)

        elif item_type == u'高気圧':
            property = {"CenterType": "high"}
            return self.center_part(item, property)

        elif item_type == u'寒冷前線':
            property = {"LinePart": "coldfront"}
            return self.corrdinate_part(item, property)

            pass
        elif item_type == u'温暖前線':
            property = {"LinePart": "warmfront"}
            return self.corrdinate_part(item, property)
            pass
        else:
            print "WARN:TYpe Missing", item_type
            pass

        return


if __name__ == '__main__':
        chart = WeatherChart()
        geo = chart.parse('./test/data/70_58_01_130523_VZSA50.xml')
        print geojson.dumps(geo)
