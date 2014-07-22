#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from difflib import SequenceMatcher
from termcolor import colored
import random

def parse_args():
    parser = argparse.ArgumentParser(
        description="""This script is used to manually evaluate machine
        translation. It randomly select given count of sentences. User is shown
        a sentence from baseline and corresponding sentence from candidate
        translation and select the better translation each time. Collected
        anntations are then evaluated.""", 
        epilog="Author: Matous Machacek <machacekmatous@gmail.com>")
    
    parser.add_argument("baseline",
            help="File with baseline translations",
            type=argparse.FileType('r'),
            )

    parser.add_argument("candidate",
            help="File with candidate translations",
            type=argparse.FileType('r'),
            )
    
    parser.add_argument("--count",
            help="A size of a generated sample to evaluate",
            type=int,
            default=100,
            )
    
    parser.add_argument("--rseed",
            help="Random seed used to randomly select a sample",
            type=int,
            default=None,
            )

    return parser.parse_args()

def main():
    args = parse_args()

    random.seed(args.rseed)

    baseline = (line.decode('utf8').strip() for line in args.baseline)
    candidate = (line.decode('utf8').strip() for line in args.candidate)
    tuples = list(zip(baseline, candidate))
    all = len(tuples)

    tuples = list(filter(lambda x: x[0] != x[1], tuples))
    unequal = len(tuples)

    sample = random.sample(tuples, args.count)

    counts = [0,0,0]
    for baseline_sent, candidate_sent in sample:
        result = compare_sentences(baseline_sent, candidate_sent)
        counts[result] +=1


    total = sum(counts)

    print 100 * "\n"
    print "Results"
    print "Better:", counts[2], "(%.1f %%)" % (100 * counts[2] / float(total))
    print "Equal:", counts[0], "(%.1f %%)" % (100 * counts[0] / float(total))
    print "Worse:", counts[1], "(%.1f %%)" % (100 * counts[1] / float(total))
    print "Total:", total, "(%.1f %%)" % (100 * total / float(total))
    print "\n"
    print "Unequal:", unequal, "(%.1f %%)" % (100*unequal / float(all)), "of", all




def compare_sentences(sent1, sent2):

    colored1 = ""
    colored2 = ""
    sm = SequenceMatcher(a=sent1, b=sent2, autojunk=False)
    for op, i1, j1, i2, j2 in sm.get_opcodes():
        if op == 'equal':
            colored1 += sent1[i1:j1]
            colored2 += sent2[i2:j2]
        elif op == 'delete':
            colored1 += colored(sent1[i1:j1], 'green')
        elif op == 'insert':
            colored2 += colored(sent2[i2:j2], 'green')
        elif op == 'replace':
            colored1 += colored(sent1[i1:j1], 'red')
            colored2 += colored(sent2[i2:j2], 'red')


    swaped = random.choice([True, False])
    if swaped:
        colored1, colored2 = colored2, colored1

    print 100 * "\n"
    # print "reference:", reference
    print "   veta 1:", colored1
    print "   veta 2:", colored2
    print "\n"
    
    answer = -1
    while not 0 <= answer <= 2:
        print "Zadej cislo vety, ktera je lepsi. Pokud jsou obe stejne, zadej 0."
        try:
            answer = int(raw_input('--> '))
        except EOFError:
            pass
        except ValueError:
            pass

    if swaped:
        if answer == 1:
            answer = 2
        elif answer == 2:
            answer = 1
    
    return answer

if __name__ == '__main__':
    main()
