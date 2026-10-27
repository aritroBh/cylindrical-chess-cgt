import sys
sys.path.insert(0, '.')
from growlib import *
from collections import Counter, defaultdict
seeds = [parse(l.split('\t')[0]) for l in open('seeds_all.txt')]
tot = Counter(); allc = set(); first = {}
per = []
for s in seeds:
    cs = {}
    cnt = Counter()
    for name, q in neighbours(s):
        c = canon(q)
        if c not in cs:
            cs[c] = name; cnt[name] += 1
    per.append((len(s), len(cs)))
    for c, name in cs.items():
        if c not in first: first[c] = name
    tot.update(cnt)
    print(len(s), fmt(s)[:40], len(cs), dict(cnt))
print('sum of per-seed distinct', sum(p[1] for p in per), 'global distinct', len(first))
print(Counter(first.values()))
print(Counter(len(c) for c in first))
