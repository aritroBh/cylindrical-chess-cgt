# Stage C (replaces the plain random walk, which collapsed onto the all-N plateau): multi-token bursts around every
# known width<=6 block with a nimber >= 2.  Each iteration: pick a seed (block, wall type), apply 2-3 random edits
# (substitute / shift a rank / insert / delete / swap), evaluate at the seed's wall type; a nimber >= 2 becomes a new seed.
import sys, glob
from p3lib import *
CAP = int(sys.argv[1]); SEED = int(sys.argv[2]); TAG = sys.argv[3]
random.seed(SEED)
ev = Evaluator(f"results_p3b_{TAG}.tsv", tbits=22, nodelim=2000000,
               extra=("results.tsv", "results_blocks.tsv", "results_p3.tsv", "results_p3_0.tsv", "results_p3_r2.tsv"))
lg = Log(f"p3_burst_hits_{TAG}.tsv")
vocab = V35 * 3 + VDBL
seeds = {}
for fn in ["p3_hits.tsv"] + sorted(glob.glob("p3_neigh_hits_*.tsv")) + sorted(glob.glob("p3_burst_hits_*.tsv")):
    for line in open(fn):
        tag, blk, f, L, sig = line.rstrip("\n").split("\t")
        v = nimber(sig)
        if isinstance(v, int) and v >= 2 and len(blk.split()) <= 6: seeds[(blk, f, int(L))] = v
seed_list = list(seeds)
print(len(seed_list), "seeds", flush=True)
def edit(b):
    b = list(b); r = random.random()
    if r < 0.45: b[random.randrange(len(b))] = random.choice(vocab)
    elif r < 0.65:
        i = random.randrange(len(b)); w, bb = parse_token(b[i])
        if w and (not bb or random.random() < 0.5): w = {max(2, min(6, x + random.choice((-1, 1)))) for x in w}
        elif bb: bb = {max(3, min(7, x + random.choice((-1, 1)))) for x in bb}
        b[i] = make_token(w, bb)
    elif r < 0.78 and len(b) > 4: del b[random.randrange(len(b))]
    elif r < 0.9 and len(b) < 6: b.insert(random.randrange(len(b) + 1), random.choice(vocab))
    else:
        i, j = random.randrange(len(b)), random.randrange(len(b)); b[i], b[j] = b[j], b[i]
    return b
calls0 = ev.n_new; best = max(seeds.values()); nv = Counter(); tried = set(seeds)
it = 0
while ev.n_new - calls0 < CAP:
    it += 1
    blk, f, L = random.choice(seed_list)
    b = blk.split()
    for _ in range(random.choice((2, 2, 3, 3, 4))): b = edit(b)
    if not (4 <= len(b) <= 6): continue
    key = (S(b), f, L)
    if key in tried: continue
    tried.add(key)
    full = b + wall(L, f)
    if not legal_start(full): continue
    sig = ev.sig(full); lg.rec("burst", b, f, L, sig)
    v = nimber(sig); nv[v if isinstance(v, int) else ('N+' if v == 'N+' else 'other')] += 1
    if isinstance(v, int) and v >= 2:
        seed_list.append(key); seeds[key] = v
        if v > best: best = v; print("new best", v, S(b), f, L, sig, flush=True)
    if sig[:5] == 'NNNNP': print("STAR4-PATTERN", S(b), f, L, sig, flush=True)
    if it % 2000 == 0: print("it", it, "calls", ev.n_new - calls0, "seeds", len(seed_list), dict(nv), flush=True)
print("done", it, ev.n_new - calls0, len(seed_list), dict(nv), "best", best)
