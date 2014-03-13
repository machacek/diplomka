#!/usr/bin/env python
from __future__ import print_function
import argparse
from itertools import izip_longest, izip, count

def parse_args():
    parser = argparse.ArgumentParser(
        description="Concatenate sentence alighned files to one big file for giza++", 
        epilog="Author: Matous Machacek <machacekmatous@gmail.com>")

    parser.add_argument("--outputs",
            help="Output files",
            required=True,
            nargs='*',
            type=argparse.FileType('w'),
            dest="outputs")
    
    parser.add_argument("--input",
            help="Input file",
            required=True,
            type=argparse.FileType('r'),
            dest="input")

    parser.add_argument("--splitinfo",
            help="A file with split information",
            required=True,
            type=argparse.FileType('r'),
            dest="split_info")

    return parser.parse_args()

def main():
    args = parse_args()

    input_iterator = iter(args.input)

    for output_file, n_lines in izip_longest(args.outputs, args.split_info): 

        if output_file is None or n_lines is None:
            raise ValueError("Number of output files does not match the number of records in split info")

        n_lines = int(n_lines)

        for _ in xrange(n_lines):

            try:
                line = next(input_iterator)
            except StopIteration:
                raise ValueError("The input file is shorter than expected")

            print(line.rstrip("\n"), file=output_file)

    # Make sure, that the input iterator is empty
    try:
        next(input_iterator)
        raise ValueError("The input file is longer than expected")
    except StopIteration:
        pass

if __name__ == '__main__':
    main()
