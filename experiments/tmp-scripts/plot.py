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

    distances, d = pickle.load(args.database)
    results = []

    worse_array = []
    equal_array = []
    better_array = []
    

    range_ = list(range(1, 18))

    for distance in range_:
        worse = d[1][distance]
        equal = d[0][distance]
        better = d[-1][distance]

        sum = float(worse + equal + better)
        results.append((distance, distances[distance], worse/sum, equal/sum, better/sum))

        worse_array.append(worse/sum)
        equal_array.append(equal/sum)
        better_array.append(better/sum)

    print(tabulate.tabulate(
        results,
        headers=["Edit Distance", "Count", "Worse", "Equal", "Better"],
        floatfmt=".3f",
        tablefmt="simple",
        ))

    plt.plot(range_, equal_array, 'o-', label="Equal")
    plt.plot(range_, better_array, 'o-', label="Better")
    plt.plot(range_, worse_array, 'o-', label="Worse")
    plt.ylabel("Relative frequency")
    plt.xlabel("Edit distance")
    plt.legend(loc=7)
    plt.savefig('foo.pdf')

if __name__ == '__main__':
    main()
