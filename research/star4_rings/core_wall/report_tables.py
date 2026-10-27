#!/usr/bin/env python3
"""Markdown tables from out/*.res (only jobs with a .done file)."""
import glob, os, collections, sys
outdir = 'out'
def classify(sig):
    if sig in ('TABLEFULL', 'BUDGET'): return 'unres'
    fn = next((i for i, c in enumerate(sig) if c != 'N'), None)
    if fn is None: return 'allN'
    if sig[fn] == 'P': return '*%d' % fn if fn <= 4 else '*5+'
    return 'nn_h0' if fn == 0 else ('nn_h1' if fn == 1 else 'nn_h2+')
COLS = ['*0','*1','*2','*3','*4','*5+','allN','nn_h0','nn_h1','nn_h2+','unres']
# key: (w,p,L,ph,mode) -> dict
retry = {}
if os.path.exists('retry_out.txt'):
    for l in open('retry_out.txt'):
        p = l.rstrip('\n').split('\t')
        if len(p) >= 2: retry[p[0]] = p[1]
agg = collections.defaultdict(lambda: {'n':0,'h':collections.Counter(),'shards':set(),'tot':0,'trunc':0,'jobs':0})
for f in sorted(glob.glob(outdir + '/*.res')):
    if not os.path.exists(f[:-4] + '.done'): continue
    job = None; hist = collections.Counter(); done = None
    for line in open(f):
        line = line.rstrip('\n')
        if line.startswith('#JOB'): job = line.split('\t')[1].split()
        elif line.startswith('#H\t'): _, s, n = line.split('\t'); hist[classify(s)] += int(n)
        elif line.startswith('#DONE'): done = dict(kv.split('=') for kv in line.split('\t')[1:])
    _, mode, w, p, L, ph, a1, a2 = job
    rp = f[:-4] + '.retry'
    if os.path.exists(rp):
        for r in open(rp):
            r = r.strip()
            if r and r in retry and hist['unres'] > 0:
                hist['unres'] -= 1; hist[classify(retry[r])] += 1
    a = agg[(int(w), int(p), int(L), int(ph), mode)]
    a['n'] += int(done['evaluated']); a['jobs'] += 1
    for k, v in hist.items(): a['h'][k] += v
    if done['status'] != 'complete': a['trunc'] += 1
    if mode == 'E': a['shards'].add(int(a1)); a['tot'] = int(a2)
def row(label, a):
    return '| %s | %d | ' % (label, a['n']) + ' | '.join(str(a['h'][c]) for c in COLS) + ' |'
hdr = '| cell | evaluated | ' + ' | '.join(COLS) + ' |\n|' + '---|' * (len(COLS) + 2)
# per (w,p) summary rows, exhaustive and sampled separately
print('### Per (w, p), summed over the three wall variants (L=4 ph0, L=5 ph0, L=5 ph1)\n')
print(hdr)
cellsets = collections.defaultdict(list)
for (w, p, L, ph, mode), a in agg.items(): cellsets[(w, p, mode)].append(((L, ph), a))
tot = {'n':0,'h':collections.Counter()}
for (w, p, mode) in sorted(cellsets):
    S = {'n':0,'h':collections.Counter()}
    for _, a in cellsets[(w, p, mode)]:
        S['n'] += a['n']
        for k, v in a['h'].items(): S['h'][k] += v
    full = all(len(a['shards']) == a['tot'] and a['trunc'] == 0 for _, a in cellsets[(w, p, mode)]) if mode == 'E' else None
    nvar = len(cellsets[(w, p, mode)])
    lab = 'w=%d p=%d %s' % (w, p, ('exhaustive' + ('' if (full and nvar == 3) else ' (%d/3 variants%s)' % (nvar, '' if full else ', partial'))) if mode == 'E' else 'random sample')
    print(row(lab, S))
    tot['n'] += S['n']
    for k, v in S['h'].items(): tot['h'][k] += v
print(row('**ALL**', tot))
print('\n### Per variant\n')
print(hdr)
for (w, p, L, ph, mode) in sorted(agg):
    a = agg[(w, p, L, ph, mode)]
    lab = 'w=%d p=%d L=%d ph=%d %s' % (w, p, L, ph, 'E(%d/%d shards)' % (len(a['shards']), a['tot']) if mode == 'E' else 'S')
    print(row(lab, a))
