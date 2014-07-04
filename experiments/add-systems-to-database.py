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
            help="Pickled segment annotations",
            type=argparse.FileType('rb'),
            )
    
    parser.add_argument("systems",
            help="Segments file with systems",
            type=argparse.FileType('r'),
            )
    
    parser.add_argument("output",
            help="Pickled segment annotations",
            type=argparse.FileType('wb'),
            )

    return parser.parse_args()
args = parse_args()

def main():
    annotations = pickle.load(args.database)

    split_lines = (line.decode('utf-8').strip().split('\t') for line in args.systems)

    for sentence_id, source_segment, system, candidate_segment, _ in split_lines:
        sentence_id = int(sentence_id)

        try:
            for annotation in annotations[sentence_id, source_segment]:
                success = annotation.add_system_segment(system, candidate_segment)
                if not success:
                    pass
                    #print(sentence_id, "=", source_segment, "=",  candidate_segment, "->","|".join(annotation.segment_indexed.keys()), file=sys.stderr)
        except KeyError:
            pass

    pickle.dump(annotations, args.output)
    


if __name__ == '__main__':
    main()
