#!/usr/bin/env python3
"""K44: D-alone versus P agreement tables from key and ref3m files."""
import collections, sys
def run(key, res, tag):
    K = {}
    for l in open(key):
        pos, nm, cn, d = [x.strip() for x in l.rstrip('\n').rsplit(' | ', 3)]; K[pos] = (nm, cn, d)
    tot = collections.Counter(); ag = collections.Counter(); cl = collections.Counter(); cla = collections.Counter()
    for l in open(res):
        pos, x = [t.strip() for t in l.rstrip('\n').rsplit('|', 1)]
        nm, cn, d = K[pos]
        if x == 'X': continue
        for k in (str(len(cn.split())) + ' pairs', 'all'):
            tot[k] += 1; ag[k] += (x == d)
        c = nm.split('=')[0]
        if c in ('+1', '-1', '0', '*', 'tis', 'tisn', 'over', 'under', '{1|0}', '{0|-1}', '{on|off}', 'dud', 'on', 'off'):
            cl[c] += 1; cla[c] += (x == d)
    print(tag)
    for k in sorted(tot): print('   %-10s legal %6d agree %6d  %.1f%%' % (k, tot[k], ag[k], 100.0 * ag[k] / tot[k]))
    print('   named classes (legal, agree):', {c: (cl[c], cla[c]) for c in sorted(cl)})
run('logs/p7.key', 'logs/p7.ref3', 'cyl:7x6, all 34 faithful configurations of the free runs (16 of K20 + 18 with three pairs)')
run('logs/p8.key', 'logs/p8.ref3', 'cyl:8x6, 22 faithful configurations with <= 2 pairs (16 of K20 + 6 new: a2 e2, a2 e3, a2 e4, a3 e3, a3 e4, a4 e4)')
run('logs/p7n.key', 'logs/p7n.ref3', 'cyl:7x6, the 6 NON-faithful two-pair configurations of K20 (adjacent files)')
run('logs/o2.key', 'logs/o2.ref3', 'cyl:10x6, a2 c4 f2 and a2 c4 h4 (the over and under configurations)')
