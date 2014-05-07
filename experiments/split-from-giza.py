#!/usr/bin/env python3.3
import argparse
from itertools import count

def parse_args():
    parser = argparse.ArgumentParser(
        description="Split the big alignment file to multiple alignment files specified in split info", 
        epilog="Author: Matous Machacek <machacekmatous@gmail.com>")

    parser.add_argument("--change-prefix",
            help="Change the directory of output files",
            required=True,
            dest="prefix",
            )
    
    parser.add_argument("input",
            help="Input file",
            required=True,
            type=argparse.FileType('r'),
            dest="input",
            )

    parser.add_argument("--splitinfo",
            help="A file with split information",
            required=True,
            type=argparse.FileType('r'),
            dest="split_info",
            )

    return parser.parse_args()

def main():
    args = parse_args()

    input_iterator = iter(args.input)

    for info_line in args.split_info: 

        n_lines, src_file, tgt_file = info_line.split('\t')
        n_lines = int(n_lines)

        path_list = tgt_file.split('/')
        path_list[0] = args.prefix
        dest_file_name = '/'.join(path_list)

        with open(dest_file_name,'w') as output_file: 
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
