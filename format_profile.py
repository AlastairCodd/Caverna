if __name__ != "__main__":
    raise InvalidOperationError("Don't import profile formatter")

from argparse import ArgumentParser
import pstats
import pathlib

parser = ArgumentParser(prog="Format profile output")
parser.add_argument('filename', type=pathlib.Path)
filename = str(parser.parse_args().filename)

pstats.Stats(filename) \
    .strip_dirs() \
    .sort_stats(pstats.SortKey.TIME) \
    .print_stats(.1)
