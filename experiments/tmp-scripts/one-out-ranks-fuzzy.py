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
            help="Pickled systems annotations",
            type=argparse.FileType('rb'),
            )

    return parser.parse_args()
args = parse_args()

def main():
    annotations = pickle.load(args.database)
    
    set_of_systems = set(next(iter(annotations.values()))[0].system_indexed)

    all_edit_distance_sum = 0
    all_count = 0

    results2 = []

    all_closest_type = Counter()

    for leaved_system in set_of_systems:
        win = Counter()
        win_loose = Counter()

        edit_distance_sum = 0
        count = 0
    
        closest_type = Counter()

        for annotations_list in annotations.values():
            for annotation in annotations_list:
                rank_cmp, edit_distance, comparisons = annotation.better_worse_without_fuzzy(leaved_system)
                for better, worse in comparisons:
                    win[better] += 1
                    win_loose[better] += 1
                    win_loose[worse] += 1
                
                edit_distance_sum += edit_distance
                count += 1

                if edit_distance > 0:
                    closest_type[rank_cmp] += 1


        results = Counter()
        for system in win_loose:
            results[system] = win[system] / win_loose[system]

        avg_edit_distance = float(edit_distance_sum) / count

        #print("\\subfloat[%s, avg. dist.: %.1f]{" % (leaved_system, avg_edit_distance))
        
        #print(tabulate.tabulate(
        #    results.most_common(),
        #    headers=["system", "score"],
        #    floatfmt=".3f",
        #    tablefmt="latex",
        #    ))

        #print("}")

        all_edit_distance_sum += edit_distance_sum
        all_count += count

        closest_type_sum = float(sum(closest_type.values()))
        results2.append((leaved_system, closest_type[1]/closest_type_sum, closest_type[0]/closest_type_sum, closest_type[-1]/closest_type_sum))
        
        
        all_closest_type += closest_type

    #print("Overall average edit distance:", float(all_edit_distance_sum) / all_count)

    closest_type = all_closest_type
    closest_type_sum = float(sum(closest_type.values()))
    results2.append(("total", 100 * closest_type[1]/closest_type_sum, 100 * closest_type[0]/closest_type_sum, 100 * closest_type[-1]/closest_type_sum))

    print(tabulate.tabulate(
        results2,
        headers=["Unseen system", "Worse", "Equal", "Better"],
        floatfmt=".1f \%",
        tablefmt="latex",
        ))


    


if __name__ == '__main__':
    main()
