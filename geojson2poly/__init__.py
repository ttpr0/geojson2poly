class Polygon():
    """polygon class used by functions in this package\n
    notes:
        - contains list of coordinates (Tuple(lon, lat))\n
        - polygon ring should be explicitly closed (first point = last point)\n
    """
    __slots__ = "coords", "name", "inner"
    def __init__(self, coords:list[tuple[float, float]], name:str, inner:bool = False):
        self.coords:list[tuple[float, float]] = coords
        self.name:str = name
        self.inner:bool = inner

from geojson2poly.helpers import *
from geojson2poly.reader import *
from geojson2poly.writer import *
