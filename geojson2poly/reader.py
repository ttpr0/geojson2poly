import json
import os
import logging
import unittest
from geojson2poly import Polygon, int_to_ordinal

def read_polygons_from_geojson(inputfile:str) -> list[Polygon]:
    """reads in list of polygons from geojson-file\n
    notes:
        - geojson content needs to be on top-level node of json file\n
        - inner and outer rings of same polygon share one name\n
        - polygons should close the ring explicitly (first and last point are the same)\n
    
    params:
        inputfile -> file containing geojson polygons

    returns:
        -> list of polygons
    """
    infile = open(inputfile, "r")
    geojson = json.loads(infile.read())
    infile.close()
    polygons:list[Polygon] = []
    count = 1
    assert geojson["type"] == "FeatureCollection", logging.error("failed to read geojson")
    for feature in geojson["features"]:
        geom = feature["geometry"]
        if geom["type"] == "Polygon":
            name = int_to_ordinal(count)
            polygon = geom["coordinates"]
            for i in range(0, len(polygon)):
                coords = []
                for coord in polygon[i]:
                    coords.append((coord[0], coord[1]))
                if i == 0:
                    inner = False
                else:
                    inner = True
                polygons.append(Polygon(coords, name, inner))
            count += 1
        if geom["type"] == "MultiPolygon":
            subcount = 1
            for polygon in geom["coordinates"]:
                name = int_to_ordinal(count) + "_" + str(subcount)
                for i in range(0, len(polygon)):
                    coords = []
                    for coord in polygon[i]:
                        coords.append((coord[0], coord[1]))
                    if i == 0:
                        inner = False
                    else:
                        inner = True
                    polygons.append(Polygon(coords, name, inner))
                subcount += 1
            count += 1
    return polygons

def read_polygons_from_poly(inputfile:str) -> list[Polygon]:
    """reads in list of polygons from poly-file\n
    notes:
        - inner and outer rings of same polygon share one name\n
        - polygons do not need do be closed explicitly\n
    
    params:
        inputfile -> input .poly-file

    returns:
        -> list of polygons
    """
    infile = open(inputfile, "r")
    infile.readline()
    polygons:list[Polygon] = []
    name = infile.readline().rstrip()
    if name[0] == '!':
        inner = True
        name = name[1:len(name)]
    inner = False
    coords = []
    while True:
        line = infile.readline().rstrip()
        if line == 'END':
            if coords[0] != coords[-1]:
                coords.append(coords[0])
            polygons.append(Polygon(coords, name, inner))
            name = infile.readline().rstrip()
            if name == 'END': break
            if name[0] == '!':
                inner = True
                name = name[1:len(name)]
            else:
                inner = False
            coords = []
            continue
        coord = line.split()
        coords.append((float(coord[0]), float(coord[1])))
    infile.close()
    return polygons