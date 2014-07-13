#!/usr/bin/env python
from __future__ import print_function, division
from collections import Counter
import argparse
import sys
import pickle
import tabulate

sys.path.append("/home/mmachace/diplomka/segranks")

def parse_args():
    parser = argparse.ArgumentParser(
        description="", 
        epilog="Author: Matous Machacek <machacekmatous@gmail.com>")

    parser.add_argument("database",
            help="Pickled systems annotations",
            type=argparse.FileType('rb'),
            )
    
    parser.add_argument("output",
            help="Pickled systems annotations",
            type=argparse.FileType('wb'),
            )

    return parser.parse_args()
args = parse_args()

def main():
    annotations = pickle.load(args.database)
    set_of_systems = set(next(iter(annotations.values()))[0].system_indexed)

    distances = Counter()
    d = {
            -1 : Counter(),
             0 : Counter(),
             1 : Counter(),
        }

    for leaved_system in set_of_systems:

        for annotations_list in annotations.values():
            for annotation in annotations_list:
                rank_cmp, edit_distance, comparisons = annotation.better_worse_without_fuzzy(leaved_system)
                distances[edit_distance] += 1
                d[rank_cmp][edit_distance] += 1

    pickle.dump((distances, d), args.output)
    


if __name__ == '__main__':
    main()
