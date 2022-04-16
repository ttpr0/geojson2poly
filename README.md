[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
![GitHub](https://img.shields.io/github/license/ttpr0/geojson2poly)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ttpr0/geojson2poly)

# geojson2poly
Convert between GeoJSON Polygons/Multipolygons and Osmosis Polygon Filter File Format.

## Usage

### Command-Line Arguments:
| argument | type | description |
| -------------------- | ----------- | ------------ |
| input | Required | path to input poly or geojson file |
| -o <value\>, --output <value\> | Optional | path to output, if nothing specified output will be created in current directory |

### Example:
To use the tool from command-line either run 
```
$ python3 geojson2poly.py file.json -o file.poly
```
or use the standalone executable (on Windows)
```
$ geojson2poly file.json -o file.poly
```
