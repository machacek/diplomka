#!/usr/bin/env python

import matplotlib.pyplot as plt

exact_match = [
    0.1350,
    0.0496,
    0.0970,
    0.0508,
    0.0768,
    0.1014,
    0.2347,
    0.2759,
    0.3185,
    0.5140,
    0.3984,
    0.4612,
    0.3996,
    0.4325,
    0.5161,
    0.5746,
    0.5165,
    0.5063,
    0.5169,
    0.5168,
]

penalize_unknown = [
    0.1350,
    0.0513,
    0.4830,
    0.6038,
    0.6859,
    0.6976,
    0.7050,
    0.7058,
]

penalize_unknown_range = list(range(1,1+len(penalize_unknown)))
exact_match_range = list(range(1,1+len(exact_match)))

print penalize_unknown_range
print exact_match_range

plt.plot(penalize_unknown_range, penalize_unknown, 'o-', label="PenalizeUnknown")
plt.plot(exact_match_range, exact_match, 'o-', label="ExactMatch")
plt.ylabel("Hit rate")
plt.xlabel("MERT Iteration")
plt.legend(loc=4)
plt.savefig('foo.pdf')
