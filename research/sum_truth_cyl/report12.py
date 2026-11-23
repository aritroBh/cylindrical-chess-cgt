import json, os, collections
from analysis12 import *
PRN = lambda s: len(s.replace('W:', '').replace('B:', '').replace('/', '').split())
tot = collections.Counter(); lines = []; dis = []
def fmt(r):
    return ' / '.join(x.split('|')[1].strip() for x in r['stdout'])
def block(items, prefix, idxs, label):
    for i in idxs:
        it = items[i]; r = load(f'{prefix}{i:02d}')
        if r is None: lines.append(f'| {label}{i} | {it["A"]} + {it["B"]} | not run |||||||'); continue
        o = it['ep-aware']['outcome']; j = judge(r, PRED[o])
        for x in j: tot[(label, x)] += 1
        c2 = load_c2(prefix, i)
        c2n = None
        if c2 and not c2['stdout']:
            c2n = f'cap2 killed at 12 GB after {c2["secs"]:.0f}s, no answer'; c2 = None
        j2 = judge(c2, PRED[o]) if c2 else None
        if c2: 
            for x in j2: tot[(label + '-cap2', x)] += 1
        ex = sum(x.startswith('exact') for x in j)
        st = 'exact' if ex == 2 else ('exact on one side, bounds on other' if ex == 1 else 'bounds')
        agree = 'DISAGREE' if any('MISMATCH' in x or 'CONTRADICT' in x for x in j + (j2 or [])) else ('agree (exact)' if ex == 2 else 'no contradiction')
        if agree == 'DISAGREE': dis.append((label, i))
        comp = lambda t: it['ep-aware_' + t]['value']
        lines.append(f'| {label}{i} | {it["A"]} ({comp("A")}) + {it["B"]} ({comp("B")}) | {PRN(it["A"])+PRN(it["B"])+2} | {it["ep-aware"]["value"]} = {o} {PRED[o]} | {fmt(r)} | {st} | {r["maxrss_bytes"]/1e9:.1f} | {r["secs"]:.0f} | {agree}' + (f' | cap2: {fmt(c2)} ({c2["maxrss_bytes"]/1e9:.1f} GB, {c2["secs"]:.0f}s) {j2}' if c2 else (' ' + c2n if c2n else '')) + ' |')
def load_c2(prefix, i):
    f = f'{D}/jobs12/{prefix}{i:02d}_cap2.json'
    return json.load(open(f)) if os.path.exists(f) else None
i1 = json.load(open(D + '/pairs.json')); i2 = json.load(open(D + '/pairs2.json'))
block(i1, 'pair', [1, 9, 21, 22, 26, 29, 35, 40, 48], 'P')
block(i2, 'p2_', range(10), 'N')
print('| pair | components (model value) | pawns+anchors | model sum (ep-aware) value = outcome (W-to-move, B-to-move) | real cap-1 (W-to-move / B-to-move; first token = upper bound, second = lower) | status | peak GB | secs | verdict | cap 2 |')
print('|---|---|---|---|---|---|---|---|---|---|')
print('\n'.join(lines)); print(); print(sorted(tot.items())); print('disagree', dis)
