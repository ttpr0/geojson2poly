import argparse
import unittest
import logging
from geojson2poly import *

def main(args):
    if not os.path.isfile(args.input):
        logging.error("pls specify a valid input")
        return
    infiletype = os.path.splitext(args.input)[1]
    outdir = ""
    outname = ''.join(os.path.basename(args.input).split(".")[0:-1])
    if infiletype == ".poly": outfiletype = ".json"
    if infiletype in [".json", ".geojson"]: outfiletype = ".poly"
    if args.output != None:
        outdir, outfile = os.path.split(os.path.abspath(args.output))
        if not os.path.isdir(outdir):
            logging.error("pls specify a valid output location")
            return
        outname, outfiletype = os.path.splitext(outfile)

    if infiletype in [".geojson", ".json"]:
        polygons = read_polygons_from_geojson(args.input)
    elif infiletype == ".poly":
        polygons = read_polygons_from_poly(args.input)
    else:
        logging.error("the given input is in the wrong format")
        return

    if outfiletype == ".poly":
        with open(os.path.join(outdir, outname + outfiletype), "w") as outfile:
            outfile.write(polygons_to_poly(polygons))
    elif outfiletype in [".geojson", ".json"]:
        with open(os.path.join(outdir, outname + outfiletype), "w") as outfile:
            outfile.write(polygons_to_geojson(polygons))
    else:
        logging.error("the given output-file has the wrong type")
        return

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(description="converts geojson to osmosis poly-file and vice versa")

    parser.add_argument(
        'input',
        action='store',
        type=str,
        help="specify path to input file (.poly, .json, .geojson)",
    )

    parser.add_argument(
        '-o',
        '--output',
        action='store',
        type=str,
        help="specify name of output-file (.poly, .json, .geojson)",
    )

    args = parser.parse_args()

    main(args)