import sys, re, glob, os
sys.path.insert(0, '.')
from growlib import *

R = '../..'
src = {}   # canonical -> list of sources

def add(s, tag):
    r = parse(s) if isinstance(s, str) else s
    c = canon(r)
    src.setdefault(c, []).append(tag)

for n in (8, 10, 12, 14):
    add(Q(n), 'Q_%d' % n)
add("W5 B7 W4 W4B7 B6 W3B6 W2 B5", 'C8 ring (task)')
for i, l in enumerate(open('../seeds_star3.txt')):
    if l.strip():
        add(l.strip(), 'seeds_star3.txt:%d' % (i + 1))
for l in open('../wall_results.tsv'):
    f = l.rstrip('\n').split('\t')
    if len(f) >= 4 and f[3] == 'NNNPNNNN':
        add(f[2], 'wall_results.tsv:%s' % f[0])

def flat(line, n):
    m = re.match(r'W: (.*?) / B: (.*?)\t', line)
    ws = m.group(1).split(); bs = m.group(2).split()
    w = [[] for _ in range(n)]; b = [[] for _ in range(n)]
    for t in ws: w['abcdefgh'.index(t[0])].append(int(t[1]))
    for t in bs: b['abcdefgh'.index(t[0])].append(int(t[1]))
    return tuple((tuple(sorted(w[i])), tuple(sorted(b[i]))) for i in range(n))

for path, n, tag in ((R + '/star26_rings/c7/p10_5_5', 7, 'C7 p10_5_5 hits'), ):
    for fn in sorted(glob.glob(path + '/*.hits.tsv')):
        for l in open(fn):
            if l.rstrip('\n').endswith('N,3'):
                add(flat(l, n), tag)
for l in open(R + '/star26_rings/c8/p10_5_5_hits.tsv'):
    if l.rstrip('\n').endswith('N,3'):
        add(flat(l, 8), 'C8 p10_5_5_hits.tsv')

with open('seeds_all.txt', 'w') as o:
    for c, t in sorted(src.items(), key=lambda kv: (len(kv[0]), kv[0])):
        o.write('%s\t%s\n' % (fmt(c), ';'.join(sorted(set(t)))))
print(len(src), 'distinct seeds (canonical)')
from collections import Counter
print(Counter(len(c) for c in src))
