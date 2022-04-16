import json
import logging
import unittest
from geojson2poly import Polygon, fortran_format


def polygons_to_poly(polygons:list[Polygon]) -> str:
    """converts list of Polygons to string representing .poly file content\n
    notes:
        - inner polygons should have same name as their outer polygon\n
        - inner polygons without matching outer polygon are left of of .poly string\n
        - if multiple outer polygons share same name they are left out of .poly string\n
        - tabs are used as white-spaces\n
    
    params:
        polygons -> list of Polygons

    returns:
        -> string representing .poly file content
    """
    polydict:dict[str, list[Polygon]] = {}
    for polygon in polygons:
        if polydict.get(polygon.name) == None:
            polydict[polygon.name] = []
        polydict[polygon.name].append(polygon)
    out = ""
    eol = "\n"
    ws = "\t"
    out += "poly_from_geojson" + eol
    for _, value in polydict.items():
        outer = [polygon for polygon in value if not polygon.inner]
        inner = [polygon for polygon in value if polygon.inner]
        if len(outer) == 0 or len(outer) > 1:
            continue
        for polygon in outer:
            out += polygon.name + eol
            for coord in polygon.coords:
                out += ws + fortran_format(coord[0]) + ws + fortran_format(coord[1]) + eol
            out += "END" + eol
        for polygon in inner:
            out += "!" + polygon.name + eol
            for coord in polygon.coords:
                out += ws + fortran_format(coord[0]) + ws + fortran_format(coord[1]) + eol
            out += "END" + eol
    out += "END"
    return out

def polygons_to_geojson(polygons:list[Polygon]) -> str:
    """converts list of Polygons to string representing of geojson polygons\n
    notes:
        - inner polygons should have same name as their outer polygon\n
        - inner polygons without matching outer polygon are left of of .poly string\n
        - if multiple outer polygons share same name they are left out of .poly string\n
    
    params:
        polygons -> list of Polygons

    returns:
        -> string representing geojson polygons
    """
    polydict:dict[str, list[Polygon]] = {}
    for polygon in polygons:
        if polydict.get(polygon.name) == None:
            polydict[polygon.name] = []
        polydict[polygon.name].append(polygon)
    geojson = {"type": "FeatureCollection", "features": []}
    for key, value in polydict.items():
        feature = {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": []}, "properties": {"name": key}}
        outer = [polygon for polygon in value if not polygon.inner]
        inner = [polygon for polygon in value if polygon.inner]
        if len(outer) == 0 or len(outer) > 1:
            continue
        for polygon in outer:
            feature["geometry"]["coordinates"].append(polygon.coords)
        for polygon in inner:
            feature["geometry"]["coordinates"].append(polygon.coords)
        geojson["features"].append(feature)
    return json.dumps(geojson)