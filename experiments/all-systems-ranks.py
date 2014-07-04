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

    win = Counter()
    win_loose = Counter()

    for annotations_list in annotations.values():
        for annotation in annotations_list:
            for better, worse in annotation.better_worse_system_comparisons():
                win[better] += 1
                win_loose[better] += 1
                win_loose[worse] += 1

    results = Counter()
    for system in win_loose:
        results[system] = win[system] / win_loose[system]

    print(tabulate.tabulate(
        results.most_common(),
        headers=["system", "score"],
        floatfmt=".4f",
        ))


if __name__ == '__main__':
    main()
