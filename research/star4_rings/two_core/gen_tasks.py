# Build the task list for the two-core experiment.
import json, random
from collections import defaultdict
from lib import *
random.seed(20261027)
opp = lambda f: 'B' if f == 'W' else 'W'
big = json.load(open("lib_big_ok.json"))
for x in big: x['kind'] = 'big'
# small typed cores from the block enumerations (stable over L=4,6 (even) / 5,7 (odd))
small = []
for w in (1, 2, 3):
    d = defaultdict(dict)
    for line in list(open(f"blocks_w{w}.tsv"))[1:]:
        blk, f, L, sig = line.rstrip("\n").split("\t"); d[(blk, f)][int(L)] = sig
    for (blk, f), m in sorted(d.items()):
        for par, Ls in (("even", (4, 6)), ("odd", (5, 7))):
            s = [m[L] for L in Ls]
            if "ILLEGAL" in s: continue
            v = [nimber(x) for x in s]
            if isinstance(v[0], int) and v[0] == v[1] and v[0] <= 1:
                small.append(dict(block=blk, f=f, par=par, v=v[0], w=w, kind='small'))
print("small typed:", len(small), "by v/w:", sorted(__import__('collections').Counter((x['v'], x['w']) for x in small).items()))
s1 = [x for x in small if x['v'] == 1]; s0 = [x for x in small if x['v'] == 0]
s1_low = [x for x in s1 if x['w'] <= 2]; s1_w3 = [x for x in s1 if x['w'] == 3]
ev = Evaluator("results_blocks.tsv", tbits=22, nodelim=3000000)
def stable_long(x):
    A = R(x['block']); Ls = (8, 10) if x['par'] == 'even' else (9, 11)
    for L in Ls:
        full = A + wall(L, x['f'])
        if not legal_start(full) or nimber(ev.sig(full)) != x['v']: return False
    return True
cand1 = [x for x in s1_low + random.sample(s1_w3, 90) if stable_long(x)]
cand0 = [x for x in random.sample(s0, 60) if stable_long(x)]
print("small pools after long-wall check:", len(cand1), len(cand0))
small_pool1 = cand1; small_pool0 = cand0[:30]
json.dump(dict(big=big, small1=small_pool1, small0=small_pool0), open("lib_all.json", "w"))

def lastof(x):
    return x['f'] if x['par'] == 'odd' else opp(x['f'])
def lens(parity):
    return (3, 5) if parity else (2, 4, 6)
def matched_combos(A, B):
    f1, f2 = A['f'], B['f']
    odd1 = (f1 == lastof(B)); odd2 = (f2 == lastof(A))
    out = []
    nA, nB = len(A['block'].split()), len(B['block'].split())
    for L1 in lens(odd1):
        for L2 in lens(odd2):
            if nA + nB + L1 + L2 <= 24: out.append((f1, L1, f2, L2))
    return out

tasks = []
def add(kind, A, B, combos):
    for (f1, L1, f2, L2) in combos:
        tasks.append(dict(kind=kind, A=A, B=B, f1=f1, L1=L1, f2=f2, L2=L2))
# BS: big x small
for A in big:
    Bs = random.sample(small_pool1, 6) + random.sample(small_pool0, 2)
    for B in Bs:
        c = matched_combos(A, B); random.shuffle(c)
        add('BS', A, B, c[:5])
# BB: big x big (incl. same)
for _ in range(150):
    A, B = random.choice(big), random.choice(big)
    c = matched_combos(A, B); random.shuffle(c)
    add('BB', A, B, c[:4])
# SS: small x small
allsmall = small_pool1 + small_pool0
for _ in range(250):
    A, B = random.choice(allsmall), random.choice(allsmall)
    c = matched_combos(A, B); random.shuffle(c)
    add('SS', A, B, c[:5])
# UN: unmatched, full 100-grid for a few pairs
def find(blockprefix, f, par):
    for x in big + small:
        if x['block'].startswith(blockprefix) and x['f'] == f and x['par'] == par: return x
X2 = find("W5 B7 W4 W4B7 B6 W3B6", 'W', 'even')
Q1 = [x for x in small if x['block'] == 'W4B6' and x['f'] == 'W' and x['par'] == 'even'][0]
Q1b = [x for x in small if x['block'] == 'B7 W4' and x['f'] == 'B' and x['par'] == 'even'][0]
X3s = [x for x in big if x['v'] == 3 and x['src'][0].startswith("C7")]
QCs = [x for x in big if x['block'] == "W3B6 W3 W2B5 B5 W2 B4 W4 B7"]
print("X2", X2, "X3", X3s, "QC", QCs)
pairs = [(X2, Q1), (X2, Q1b), (X2, X2)] + [(X3s[0], Q1)] + [(QCs[0], Q1), (QCs[0], Q1b)]
for A, B in pairs:
    grid = [(f1, L1, f2, L2) for f1 in "WB" for L1 in range(2, 7) for f2 in "WB" for L2 in range(2, 7)
            if len(A['block'].split()) + len(B['block'].split()) + L1 + L2 <= 24]
    add('UN', A, B, grid)
# dedupe identical (A,B,walls)
seen = set(); uniq = []
for t in tasks:
    k = (t['A']['block'], t['A']['f'], t['B']['block'], t['B']['f'], t['f1'], t['L1'], t['f2'], t['L2'])
    if k in seen: continue
    seen.add(k); uniq.append(t)
from collections import Counter
print(len(tasks), len(uniq), Counter(t['kind'] for t in uniq))
random.shuffle(uniq)
# sort so that cheap ones go first? keep shuffled but BB last
uniq.sort(key=lambda t: {'SS': 0, 'BS': 1, 'UN': 2, 'BB': 3}[t['kind']])
with open("tasks.jsonl", "w") as o:
    for t in uniq: o.write(json.dumps(t) + "\n")
