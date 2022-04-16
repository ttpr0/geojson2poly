import unittest
from geojson2poly import *

class TestHelpers(unittest.TestCase):

    def test_fortran_format(self):
        self.assertEqual(fortran_format(127.938), '1.2793800E+02')
        self.assertEqual(fortran_format(-127.938), '-1.2793800E+02')
        self.assertEqual(fortran_format(0.00293), '2.9300000E-03')
        self.assertEqual(fortran_format(-0.00723855), '-7.2385500E-03')
        self.assertEqual(fortran_format(1.27), '1.2700000E+00')

    def test_int_to_oridinal(self):
        self.assertEqual(int_to_ordinal(1), '1st')
        self.assertEqual(int_to_ordinal(2), '2nd')
        self.assertEqual(int_to_ordinal(120), '120th')
        self.assertEqual(int_to_ordinal(203), '203rd')
        self.assertEqual(int_to_ordinal(1045), '1045th')

class TestReaders(unittest.TestCase):

    def setUp(self):
        self.testpolys = []
        self.testpolys.append(Polygon([(40.11,40.54),(20.66,45.39),(45.28,30.75),(40.11,40.54)], "1st_1", False))
        self.testpolys.append(Polygon([(20.64,35.82),(10.64,30.81),(10.85,10.86),(30.94,5.23),(45.96,20.86),(20.64,35.82)], "1st_2", False))
        self.testpolys.append(Polygon([(30.95,20.92),(20.75,15.85),(20.75,25.61),(30.95,20.92)], "1st_2", True))
        self.testpolys.append(Polygon([(62.21,17.13),(-30.94,60.92),(-52.82,-36.21),(40.72,-41.58),(62.21,17.13)], "2nd", False))
        self.testpolys.append(Polygon([(18.83,15.93),(-11.82,23.1),(-24.96,-16.31),(18.83,15.93)], "2nd", True))
        self.testpolys.append(Polygon([(33.95,-8.74),(6.29,-7.55),(12.06,-32.23),(17.23,-15.31),(33.95,-8.74)], "2nd", True))

    def tearDown(self):
        return super().tearDown()

    def test_read_polygons_from_poly(self):
        polys = read_polygons_from_poly("tests/test_data/test.poly")
        for i in range(len(polys)):
            poly = polys[i]
            testpoly = self.testpolys[i]
            self.assertEqual(poly.coords, testpoly.coords)
            self.assertEqual(poly.name, testpoly.name)
            self.assertEqual(poly.inner, testpoly.inner)

    def test_read_polygons_from_geojson(self):
        polys = read_polygons_from_geojson("tests/test_data/test.json")
        for i in range(len(polys)):
            poly = polys[i]
            testpoly = self.testpolys[i]
            self.assertEqual(poly.coords, testpoly.coords)
            self.assertEqual(poly.name, testpoly.name)
            self.assertEqual(poly.inner, testpoly.inner)
    
class TestWriters(unittest.TestCase):

    def setUp(self):
        self.testpolys = []
        self.testpolys.append(Polygon([(40.11,40.54),(20.66,45.39),(45.28,30.75),(40.11,40.54)], "1st_1", False))
        self.testpolys.append(Polygon([(30.95,20.92),(20.75,15.85),(20.75,25.61),(30.95,20.92)], "1st_2", True))
        self.testpolys.append(Polygon([(18.83,15.93),(-11.82,23.1),(-24.96,-16.31),(18.83,15.93)], "2nd", True))
        self.testpolys.append(Polygon([(33.95,-8.74),(6.29,-7.55),(12.06,-32.23),(17.23,-15.31),(33.95,-8.74)], "2nd", True))
        self.testpolys.append(Polygon([(62.21,17.13),(-30.94,60.92),(-52.82,-36.21),(40.72,-41.58),(62.21,17.13)], "2nd", False))

        self.testgeojson = json.dumps({
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": { 
                        "type": "Polygon",
                        "coordinates": [
                            [[40.11000, 40.54], [20.66, 45.39], [45.28, 30.75], [40.11, 40.54]]
                        ]
                    },
                    "properties": {
                        "name": "1st_1"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": { 
                        "type": "Polygon",
                        "coordinates": [
                            [[62.21, 17.13], [-30.94, 60.92], [-52.82, -36.21], [40.72, -41.58], [62.21, 17.13]],
                            [[18.83, 15.93], [-11.82, 23.1], [-24.96, -16.31], [18.83, 15.93]],
                            [[33.95, -8.74], [6.29, -7.55], [12.06, -32.23], [17.23, -15.31], [33.95, -8.74]]
                        ]
                    },
                    "properties": {
                        "name": "2nd"
                    }
                }
            ]
        })

        self.testpoly = """poly_from_geojson
1st_1
\t4.0110000E+01\t4.0540000E+01
\t2.0660000E+01\t4.5390000E+01
\t4.5280000E+01\t3.0750000E+01
\t4.0110000E+01\t4.0540000E+01
END
2nd
\t6.2210000E+01\t1.7130000E+01
\t-3.0940000E+01\t6.0920000E+01
\t-5.2820000E+01\t-3.6210000E+01
\t4.0720000E+01\t-4.1580000E+01
\t6.2210000E+01\t1.7130000E+01
END
!2nd
\t1.8830000E+01\t1.5930000E+01
\t-1.1820000E+01\t2.3100000E+01
\t-2.4960000E+01\t-1.6310000E+01
\t1.8830000E+01\t1.5930000E+01
END
!2nd
\t3.3950000E+01\t-8.7400000E+00
\t6.2900000E+00\t-7.5500000E+00
\t1.2060000E+01\t-3.2230000E+01
\t1.7230000E+01\t-1.5310000E+01
\t3.3950000E+01\t-8.7400000E+00
END
END"""

    def tearDown(self):
        return super().tearDown()

    def test_polygons_to_poly(self):
        poly = polygons_to_poly(self.testpolys)
        self.maxDiff = None
        self.assertEqual(poly, self.testpoly)

    def test_polygons_to_geojson(self):
        geojson = polygons_to_geojson(self.testpolys)
        self.maxDiff = None
        self.assertEqual(geojson, self.testgeojson)