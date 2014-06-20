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

    parser.add_argument("--annotated",
            help="Pickled segment annotations",
            required=True,
            type=argparse.FileType('rb'),
            )
    
    parser.add_argument("--systems",
            help="Segments file with systems",
            required=True,
            type=argparse.FileType('r'),
            )

    return parser.parse_args()
args = parse_args()

def main():
    annotations = pickle.load(args.annotated)

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
    
    set_of_systems = set(next(iter(annotations.values()))[0].system_indexed)

    # Check the annotations have all the systems
    #for annotation_list in annotations.values():
    #    for annotation in annotation_list:
    #        annotation_systems = set(annotation.system_indexed)
    #        assert annotation_systems <= set_of_systems
    #        if annotation_systems != set_of_systems:
    #            print("id:", annotation.sentence_id, "source:", annotation.source_segment, "missing:", set_of_systems - annotation_systems)

    for leaved_system in set_of_systems:
        win = Counter()
        win_loose = Counter()

        for annotations_list in annotations.values():
            for annotation in annotations_list:
                for better, worse in annotation.better_worse_without_fuzzy(leaved_system):
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
            ))


if __name__ == '__main__':
    main()
