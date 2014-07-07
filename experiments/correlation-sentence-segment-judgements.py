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

    def compute_correlations(self):
        better_agree_counts = Counter()
        better_disagree_counts = Counter()
        worse_agree_counts = Counter()
        worse_disagree_counts = Counter()
        for better_system, worse_system, sentence_id in self.pair_wise_comparisons:
            for annotation in self.segment_annotations[sentence_id]:
                try:
                    if annotation.system_indexed[better_system].rank < annotation.system_indexed[worse_system].rank:
                        better_agree_counts[better_system] += 1
                        worse_agree_counts[worse_system] += 1
                    elif annotation.system_indexed[better_system].rank > annotation.system_indexed[worse_system].rank:
                        better_disagree_counts[better_system] += 1
                        worse_disagree_counts[worse_system] += 1
                except KeyError:
                    self.missing_keys += 1



        nontie_agree_counts = better_agree_counts + worse_agree_counts
        nontie_disagree_counts = better_disagree_counts + worse_disagree_counts

        better_kendall_taus = self.compute_kendall_taus(better_agree_counts, better_disagree_counts)
        worse_kendall_taus = self.compute_kendall_taus(worse_agree_counts, worse_disagree_counts)
        nontie_kendall_taus = self.compute_kendall_taus(nontie_agree_counts, nontie_disagree_counts)

        return better_kendall_taus, worse_kendall_taus, nontie_kendall_taus

    def compute_kendall_taus(self, agree_counts, disagree_counts):
        kendall_taus = Counter()
        for system in set(agree_counts) | set(disagree_counts):
            kendall_taus[system] = float(agree_counts[system] - disagree_counts[system]) / float(agree_counts[system] + disagree_counts[system])
        return kendall_taus.most_common()

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
    better_kendall_taus, worse_kendall_taus, nontie_kendall_taus = data.compute_correlations()

    for results, name in zip((better_kendall_taus, worse_kendall_taus, nontie_kendall_taus), ("better", "worse", "nontie")):
        print name + ":"
        print tabulate.tabulate(results, headers = ["system","kendall_tau"], tablefmt = "simple", floatfmt = ".4f")
        print ""

    print "missing:", data.missing_keys
            
if __name__ == "__main__":
    main()
