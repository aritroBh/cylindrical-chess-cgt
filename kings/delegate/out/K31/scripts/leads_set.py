#!/usr/bin/env python3
# reads `tempo profile` output on stdin, prints the set of values of each lead
import sys, re, collections
vals = collections.defaultdict(collections.Counter); head = ''
for l in sys.stdin:
    if l.startswith('PROFILE'): head = l.split(' roots')[0].replace('PROFILE ', '')
    m = re.match(r'  Lw=(-?\d+) Fw=(-?\d+) Lb=(-?\d+) Fb=(-?\d+)\s+(\d+)', l)
    if m:
        for k, v in zip(('Lw', 'Fw', 'Lb', 'Fb'), m.groups()[:4]): vals[k][int(v)] += int(m.group(5))
print(head, {k: dict(sorted(v.items())) for k, v in vals.items()})
