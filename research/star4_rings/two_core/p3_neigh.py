# Stage B: neutral-network exploration.  Start from every width<=6 block that has a nimber >= 2 in some wall type
# (from p3_hits.tsv / p3_seeds.tsv), expand by single-token substitution, deletion and insertion (width stays 4..6).
# A neighbour is expanded further when it is itself a nimber >= 2 in the same wall type.  Hard cap on engine calls.
import sys, collections
from p3lib import *
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
NW = int(sys.argv[3]) if len(sys.argv) > 3 else 1      # worker split of the seed list
K = int(sys.argv[4]) if len(sys.argv) > 4 else 0
TAG = os.environ.get("TAG", str(K))
random.seed(SEED)
ev = Evaluator(f"results_p3_{TAG}.tsv", tbits=22, nodelim=2000000, extra=("results.tsv", "results_blocks.tsv", "results_p3.tsv", "results_p3_0.tsv"))
lg = Log(f"p3_neigh_hits_{TAG}.tsv")
# seeds
seeds = set()
for fn in os.environ.get("SEEDFILES", "p3_hits.tsv").split(","):
    for line in open(fn):
        tag, blk, f, L, sig = line.rstrip("\n").split("\t")
        v = nimber(sig)
        if isinstance(v, int) and v >= 2 and len(blk.split()) <= 6: seeds.add((blk, f, int(L)))
seeds = sorted(seeds)
print(len(seeds), "seeds", flush=True)
seeds = [s for i, s in enumerate(seeds) if i % NW == K]
random.shuffle(seeds)
vocab = V35 + random.sample(VDBL, 40)
queue = collections.deque(seeds); visited = set(seeds)
calls0 = ev.n_new; best = 0; nvals = collections.Counter()
def neighbours(blk):
    t = blk
    for i in range(len(t)):
        for tok in vocab:
            if tok != t[i]: yield t[:i] + [tok] + t[i + 1:]
    if len(t) > 4:
        for i in range(len(t)): yield t[:i] + t[i + 1:]
    if len(t) < 6:
        for i in range(len(t) + 1):
            for tok in vocab: yield t[:i] + [tok] + t[i:]
while queue and ev.n_new - calls0 < CAP:
    blk, f, L = queue.popleft()
    t = blk.split()
    nb = list(neighbours(t)); random.shuffle(nb)
    nb = nb[:int(os.environ.get('NBSAMPLE', '260'))]            # subsample the neighbourhood
    for b2 in nb:
        key = (S(b2), f, L)
        if key in visited: continue
        visited.add(key)
        full = b2 + wall(L, f)
        if not legal_start(full): continue
        sig = ev.sig(full)
        lg.rec("neigh", b2, f, L, sig)
        v = nimber(sig)
        nvals[v if isinstance(v, int) else ('N+' if v == 'N+' else 'other')] += 1
        if isinstance(v, int) and v >= 2: queue.append(key)
        if isinstance(v, int) and v > best:
            best = v; print("new best nimber", v, S(b2), f, L, sig, flush=True)
        if sig[:5] == 'NNNNP': print("STAR4-PATTERN", S(b2), f, L, sig, flush=True)
    if ev.n_new % 500 < 260: print("calls", ev.n_new - calls0, "queue", len(queue), "visited", len(visited), dict(nvals), flush=True)
print("done calls", ev.n_new - calls0, "visited", len(visited), dict(nvals), "best", best)
