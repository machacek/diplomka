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

    return parser.parse_args()
args = parse_args()

def main():
    annotations = pickle.load(args.database)
    
    set_of_systems = set(next(iter(annotations.values()))[0].system_indexed)

    for leaved_system in set_of_systems:
        win = Counter()
        win_loose = Counter()

        for annotations_list in annotations.values():
            for annotation in annotations_list:
                rank_cmp, distance, comparisons = annotation.better_worse_without_fuzzy(leaved_system)
                for better, worse in comparisons:
                    win[better] += 1
                    win_loose[better] += 1
                    win_loose[worse] += 1

        results = Counter()
        for system in win_loose:
            results[system] = win[system] / win_loose[system]

        print("\nExcluded system:", leaved_system)
        print(tabulate.tabulate(
            results.most_common(),
            headers=["system", "score"],
            floatfmt=".3f",
            tablefmt="latex",
            ))


if __name__ == '__main__':
    main()
