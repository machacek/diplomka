#!/usr/bin/env python3
import sys
from collections import Counter

n = int(sys.argv[1])
c = Counter()

for line in sys.stdin:
    line = line.split()
    n_grams = zip(*[line[i:] for i in range(n)])
    c.update(n_grams)

for n_gram, count in c.most_common():
    print(" ".join(n_gram), count, sep='\t')
