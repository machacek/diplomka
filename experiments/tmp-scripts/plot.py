#!/usr/bin/env python
from __future__ import print_function, division
from collections import Counter
import argparse
import sys
import pickle
import tabulate

import matplotlib.pyplot as plt

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

    d = pickle.load(args.database)

    results = []

    worse_total = 0
    equal_total = 0
    better_total = 0

    for system in sorted(d):

        worse = d[system][1]
        equal = d[system][0]
        better = d[system][-1]

        worse_total += worse
        equal_total += equal
        better_total += better

        sum = float(worse + equal + better)
        results.append((system, 100*worse/sum, 100*equal/sum, 100*better/sum))
        
    sum = float(worse_total + equal_total + better_total)
    results.append(("All", 100* worse_total/sum, 100* equal_total/sum, 100* better_total/sum))

    print(tabulate.tabulate(
        results,
        headers=["System", "Worse", "Equal", "Better"],
        floatfmt=".1f",
        tablefmt="latex",
        ))


if __name__ == '__main__':
    main()
