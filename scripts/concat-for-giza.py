#!/usr/bin/env python
from __future__ import print_function
import argparse
from itertools import izip, izip_longest, count

def parse_args():
    parser = argparse.ArgumentParser(
        description="Concatenate sentence alighned files to one big file for giza++", 
        epilog="Author: Matous Machacek <machacekmatous@gmail.com>")

    parser.add_argument("--sources",
            help="Source files",
            required=True,
            nargs='*',
            type=argparse.FileType('r'),
            dest="sources")
    
    parser.add_argument("--targets",
            help="Target files",
            required=True,
            nargs='*',
            type=argparse.FileType('r'),
            dest="targets")
    
    parser.add_argument("--source-out",
            help="A file where source files will by concatenated",
            default="concatenated.source",
            type=argparse.FileType('w'),
            dest="source_out")
    
    parser.add_argument("--target-out",
            help="A file where target files will by concatenated",
            default="concatenated.target",
            type=argparse.FileType('w'),
            dest="target_out")

    parser.add_argument("--splitinfo",
            help="A file where target files will by concatenated",
            default="split.info",
            type=argparse.FileType('w'),
            dest="split_info")

    return parser.parse_args()

def main():
    args = parse_args()
    for source_file, target_file in izip_longest(args.sources, args.targets): 
        for i, (source_line, target_line) in izip(count(1), izip_longest(source_file, target_file)):
            print(source_line.strip(), file=args.source_out)
            print(target_line.strip(), file=args.target_out)
        print(i, file=args.split_info)

if __name__ == '__main__':
    main()
