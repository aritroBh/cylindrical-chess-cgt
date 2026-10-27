#!/usr/bin/env python3
"""Aggregate out/*.res into tables.  usage: summarize.py [outdir] [--hits]"""
import sys, glob, os, re, collections
outdir = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'out'
def classify(sig):
    if sig in ('TABLEFULL', 'BUDGET'): return sig
    fn = next((i for i, c in enumerate(sig) if c != 'N'), None)
    if fn is None: return 'allN'
    if sig[fn] == 'P': return '*%d' % fn
    return 'nonnim_h0' if fn == 0 else ('nonnim_h1' if fn == 1 else 'nonnim_h2+')
CLS = ['*0','*1','*2','*3','*4','*5','*6','*7','allN','nonnim_h0','nonnim_h1','nonnim_h2+','TABLEFULL','BUDGET']
cells = collections.defaultdict(lambda: collections.defaultdict(lambda: {'ex_sh': set(), 'ex_n': 0, 'ex_tot': 0, 'smp_n': 0, 'ex_hist': collections.Counter(), 'smp_hist': collections.Counter(), 'trunc': 0, 'jobs': 0, 'ex_ntrunc':0}))
hits = []; sigcount = collections.Counter(); total = 0; tf = []
for f in sorted(glob.glob(os.path.join(outdir, '*.res'))):
    base = f[:-4]
    if not os.path.exists(base + '.done'): continue
    job = None; hist = collections.Counter(); done = None; fh = []
    for line in open(f):
        line = line.rstrip('\n')
        if line.startswith('#JOB'): job = line.split('\t')[1].split()
        elif line.startswith('#H\t'): _, s, n = line.split('\t'); hist[s] += int(n)
        elif line.startswith('#DONE'): done = dict(kv.split('=') for kv in line.split('\t')[1:])
        elif line.startswith('HIT\t'): fh.append(line.split('\t'))
        elif line.startswith('TABLEFULL') or line.startswith('BUDGET'): tf.append((job[0], line))
    if job is None or done is None: continue
    _, mode, w, p, L, ph, a1, a2 = job; w, p, L, ph = int(w), int(p), int(L), int(ph)
    key = (L, ph); c = cells[(w, p)][key]
    c['jobs'] += 1
    n = int(done['evaluated'])
    if done['status'] != 'complete': c['trunc'] += 1
    if mode == 'E':
        c['ex_sh'].add((int(a1), int(a2))); c['ex_n'] += n; c['ex_tot'] = int(a2)
        for s, k in hist.items(): c['ex_hist'][classify(s)] += k
        if done['status'] != 'complete': c['ex_ntrunc'] += 1
    else:
        c['smp_n'] += n
        for s, k in hist.items(): c['smp_hist'][classify(s)] += k
    for h in fh:
        hits.append((w, p, L, ph, mode, h[1], h[2]))
    for s, k in hist.items(): sigcount[s] += k
    total += n
print('TOTAL evaluated: %d' % total)
def fmt(h, n):
    return ' '.join('%s=%d' % (k, h[k]) for k in CLS if h[k])
print('\nPer cell (w,p) / variant (L,phase): mode, evaluated, class counts')
for (w, p) in sorted(cells):
    for key in sorted(cells[(w, p)]):
        c = cells[(w, p)][key]
        L, ph = key
        if c['ex_n']:
            comp = (len(c['ex_sh']) == c['ex_tot'] and c['ex_ntrunc'] == 0)
            print('w=%d p=%2d L=%d ph=%d  EXHAUSTIVE%s %d shards %d/%d: n=%d  %s' % (w, p, L, ph, '' if comp else ' (PARTIAL)', len(c['ex_sh']), len(c['ex_sh']), c['ex_tot'], c['ex_n'], fmt(c['ex_hist'], c['ex_n'])))
        if c['smp_n']:
            print('w=%d p=%2d L=%d ph=%d  SAMPLE n=%d  %s' % (w, p, L, ph, c['smp_n'], fmt(c['smp_hist'], c['smp_n'])))
if '--hits' in sys.argv:
    print('\nHITS (first non-N at index >= 3, or nimber *3+):')
    seen = set()
    for h in hits:
        if h[6].startswith('NNN') or h[6].startswith('PN') and False:
            print(h)
print('\nsig counts for first-non-N >= 2:')
for s, k in sorted(sigcount.items()):
    if s.startswith('NN'): print(' ', s, k)
if tf: print('\nTABLEFULL/BUDGET positions:', len(tf))
