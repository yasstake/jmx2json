# -*- coding: utf-8 -*-
__author__ = 'takeo'

import unittest
from jma.jmx import JMX
import geojson;

class MyTestCase(unittest.TestCase):
    def test_parse(self):
        jmx = JMX()

        jmx.parse('./data/70_58_01_130523_VZSA50.xml')




    def test_lineOrPolygon(self):
        jmx = JMX()

        l = jmx.lineOrPolygon('+59.27+151.99/+59.24+151.79/+59.21+151.60/');

        self.assertEqual(l, geojson.loads('{"coordinates": [[151.99, 59.27], [151.79, 59.24], [151.6, 59.21]], "type": "LineString"}'))

        l2 = jmx.lineOrPolygon('+59.27+151.99/+59.24+151.79/+59.21+151.60/+59.27+151.99/');
        self.assertEqual(l2, geojson.loads('{"coordinates": [[151.99, 59.27], [151.79, 59.24], [151.6, 59.21], [151.99, 59.27]], "type": "Polygon"}'))

    def test_coordinate_xy(self):
        jmx = JMX()
        [x, y] = jmx.coordinate_xy('/+100.1+10.2/')
        self.assertEqual(x, 10.2)
        self.assertEqual(y, 100.1)

    def test_polyline(self):
        jmx = JMX()

        polyline = jmx.polyline('+59.27+151.99/+59.24+151.79/+59.21+151.60/')

        self.assertEqual(polyline, [[151.99, 59.27], [151.79, 59.24], [151.6, 59.21]])

if __name__ == '__main__':
    unittest.main()
