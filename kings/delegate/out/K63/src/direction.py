"""K63: direction of each disagreement (P result against the D-sum prediction, White's view, L < D < W) and the split
separated (all context pawns on file h) / not separated. usage: python3 direction.py <tag>"""
import re
import sys
from collections import Counter

O = {'L': 0, 'D': 1, 'W': 2}
c = Counter(); ctxs = {}
for l in open('logs/ctx_%s_table.txt' % sys.argv[1]):
    m = re.match(r'^(ctx\d+) \[(.*)\] (q?[AB] [bw]): P (\w), prediction (\w)', l)
    if not m:
        continue
    name, ctx, lab, p, pr = m.groups()
    sep = all(x[1] == 'h' for x in ctx.split())
    d = 'better for White' if O[p] > O[pr] else 'better for Black'
    c[('separated (file h only)' if sep else 'not separated', d)] += 1
    ctxs.setdefault('separated' if sep else 'not separated', set()).add(name)
for k, v in sorted(c.items()):
    print('%-26s %-18s %d positions' % (k[0], k[1], v))
for k, v in ctxs.items():
    print('%s: %d contexts with a disagreement' % (k, len(v)))
