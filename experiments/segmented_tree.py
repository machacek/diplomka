#!/usr/bin/env python
from __future__ import print_function
from nltk.tree import Tree
from nltk.align import Alignment
from itertools import izip, count
import argparse

class SegmentedTree(Tree):
    def segments_with_indexes(self, max_length):
        last_index = 0
        for segment in self.segments(max_length):
            new_last_index = last_index + len(segment)
            yield (segment, list(range(last_index, new_last_index)))
            last_index = new_last_index

    def segments(self, max_length):
        if self.covers() <= max_length:
            yield list(self.leaves())
        else:
            for child in self:
                if isinstance(child, SegmentedTree):
                    for segment in child.segments(max_length):
                        yield segment
                else:
                    yield [child]

    def covers(self):
        return len(self.leaves())

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generates segments of MT output to anotate.", 
        epilog="Author: Matous Machacek <machacekmatous@gmail.com>")

    parser.add_argument("--parsed",
            help="A file with parsed source sentences",
            required=True,
            type=argparse.FileType('r'),
            )
    
    parser.add_argument("--align",
            help="A file with source-target alignment",
            required=True,
            type=argparse.FileType('r'),
            dest="ali")
    
    parser.add_argument("--target",
            help="A file with tokenized MT output",
            required=True,
            type=argparse.FileType('r'),
            )
    
    parser.add_argument("--source",
            help="A file with tokenized source",
            required=True,
            type=argparse.FileType('r'),
            )
    
    parser.add_argument("--reference",
            help="A file with reference translation",
            required=True,
            type=argparse.FileType('r'),
            )
    
    parser.add_argument("--maxlength",
            help="Maximal length of a segment",
            default=4,
            metavar='N',
            type=int,
            dest="max_length")
    
    parser.add_argument("--minlength",
            help="Minimal length of a segment",
            default=2,
            metavar='N',
            type=int,
            dest="min_length")

    return parser.parse_args()

def main():
    args = parse_args()
    for i, parse_str, ali_str, target_str, reference_str, source_str in izip(count(1), args.parsed, args.ali, args.target, args.reference, args.source):
        tree = SegmentedTree.convert(Tree(parse_str))
        target_tokenized = target_str.split()
        source_tokenized = source_str.split()
        reference_str = reference_str.strip()
        alignment = Alignment(ali_str)
        for segment, indexes in tree.segments_with_indexes(args.max_length):
            if len(segment) < args.min_length:
                continue
            source_segment = [source_tokenized[index] for index in indexes]
            mapped_indexes = alignment.range(indexes)
            mapped_segment = [target_tokenized[index] for index in mapped_indexes] 
            print(i, " ".join(source_tokenized), reference_str, " ".join(source_segment), " ".join(mapped_segment), sep='\t')



if __name__ == '__main__':
    main()
