#!/usr/bin/env python3.3
from __future__ import print_function
import argparse
from itertools import zip_longest, count
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Concatenate sentence alighned files to one big file for giza++", 
        epilog="Author: Matous Machacek <machacekmatous@gmail.com>")

    parser.add_argument("--sources",
            help="Source files",
            required=True,
            nargs='*',
            type=argparse.FileType('r'),
            )
    
    parser.add_argument("--targets",
            help="Target files",
            required=True,
            nargs='*',
            type=argparse.FileType('r'),
            )
    
    parser.add_argument("out",
            help="A file where source and target files will by concatenated, omit or '-' for stdout",
            default=sys.stdout,
            type=argparse.FileType('w'),
            )

    parser.add_argument("--splitinfo",
            help="A file where target files will by concatenated",
            required=True,
            type=argparse.FileType('w'),
            )

    return parser.parse_args()

def main():
    args = parse_args()
    for source_file, target_file in zip_longest(args.sources, args.targets): 
        for i, (source_line, target_line) in zip(count(1), zip_longest(source_file, target_file)):
            print(source_line.strip(), target_line.strip(), file=args.out, sep='\t')
        print(i, source_file.name, target_file.name, file=args.splitinfo, sep='\t')

if __name__ == '__main__':
    main()
