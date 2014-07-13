#!/usr/bin/env python
from __future__ import print_function, division
from collections import Counter
import argparse
import sys
import pickle
import tabulate

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

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

    distances = pickle.load(args.database)
    
    range_ = list(range(1, 18))
    
    colors = cm.rainbow(np.linspace(0, 1, len(distances)))
    colors =[
            '#800000',
            '#FF0000',
            '#800080',
            '#FF00FF',
            '#008000',
            '#808000',
            '#FFFF00',
            '#000080',
            '#008080',
            '#00FF00',
            ]

    for system, color in zip(sorted(distances), colors):
        array = [ distances[system][x] for x in range_]
        plt.plot(range_, array, 'o-', label=system.split('.')[0], color=color)


    plt.ylabel("Frequency")
    plt.xlabel("Edit distance")
    plt.legend()
    plt.savefig('foo.pdf')

if __name__ == '__main__':
    main()
