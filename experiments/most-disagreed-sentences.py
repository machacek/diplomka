#!/usr/bin/env python
#from itertools import combinations
from collections import namedtuple, Counter
from collections import defaultdict
import csv
import sys
import argparse
import operator
import pickle
import tabulate

sys.path.append('/home/mmachace/diplomka/segranks/')

class HumanRankingsData(object):
    def load_sentence_judgements(self, file_like):
        self.missing_keys = 0
        self.pair_wise_comparisons = list()
        for line in csv.DictReader(file_like):
            direction = line['system1Id'].split('.')[-1]

            if direction != "en-cs":
                continue

            sentence_id = int(line['srcIndex'])

            extract_system = lambda x: '.'.join(x.split('.')[1:3])

            SystemsTuple = namedtuple("SystemTuple", "id rank")
            systems_ranks = [
                SystemsTuple( id = extract_system(line['system1Id']), rank = int(line['system1rank'])),
                SystemsTuple( id = extract_system(line['system2Id']), rank = int(line['system2rank'])),
                SystemsTuple( id = extract_system(line['system3Id']), rank = int(line['system3rank'])),
                SystemsTuple( id = extract_system(line['system4Id']), rank = int(line['system4rank'])),
                SystemsTuple( id = extract_system(line['system5Id']), rank = int(line['system5rank'])),
                ]

            # Extract all tuples of systems, where first system was ranked better than second one
            self.pair_wise_comparisons += [
                    (system1.id, system2.id, sentence_id) 
                    for system1 in systems_ranks 
                    for system2 in systems_ranks 
                    if system1.rank < system2.rank
                    and system1.rank != -1
                    and system2.rank != -1
                ]

    def load_segranks_database(self, file_like):
        self.segment_annotations = defaultdict(list)
        database = pickle.load(file_like)
        for (sentence_id, source_segment), annotations in database.items():
            self.segment_annotations[sentence_id].extend(annotations)

    def disagreed_sentnces(self, count):
        better_sentence = Counter()
        all_sentence = Counter()

        for better_system, worse_system, sentence_id in self.pair_wise_comparisons:
            better_sentence[better_system, sentence_id] += 1
            all_sentence[better_system, sentence_id] += 1
            all_sentence[worse_system, sentence_id] += 1


        better_segment = Counter()
        all_segment = Counter()

        for sentence_id, annotations in self.segment_annotations.iteritems():
            for annotation in annotations:
                comparisons = [
                        (system1, system2)
                        for system1,rank1 in annotation.system_indexed.items()
                        for system2,rank2 in annotation.system_indexed.items()
                        if rank1.rank < rank2.rank
                        ]

                for better_system, worse_system in comparisons:
                    better_segment[better_system, sentence_id] += 1
                    all_segment[better_system, sentence_id] += 1
                    all_segment[worse_system, sentence_id] += 1

        scores_sentence = dict()
        for key in all_sentence:
            scores_sentence[key] = float(better_sentence[key]) / all_sentence[key]
        
        scores_segment = dict()
        for key in all_segment:
            scores_segment[key] = float(better_segment[key]) / all_segment[key]

        rates = Counter()
        self.zero_divisions = 0
        for key in set(scores_segment) & set(scores_sentence):
            try:
                rates[key] = scores_segment[key] / scores_sentence[key]
                # rates[key] = scores_sentence[key] / scores_segment[key]
            except ZeroDivisionError:
                self.zero_divisions += 1


        return rates.most_common(count)

def parse_args():
    parser = argparse.ArgumentParser(
            description="""XXX
            """)

    parser.add_argument("sentence_judgments",
            help="file with sentence human judgments",
            type=argparse.FileType('r'),
            )


    parser.add_argument("segranks_database",
            help="file with pickled segment judgements",
            type=argparse.FileType('rb'),
            )
    
    return parser.parse_args()

config = parse_args()
            

def main():
    
    data = HumanRankingsData()
    data.load_sentence_judgements(config.sentence_judgments)
    data.load_segranks_database(config.segranks_database)
    data.disagreed_sentnces()
    for (system, sentence_id), rate in  data.disagreed_sentnces(40):
        print sentence_id, system, rate

    print "zero divisions:", data.zero_divisions
            
if __name__ == "__main__":
    main()
