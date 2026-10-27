# Stage C: random + hill-climbing search over width 5..6 blocks.  score(sig): nimber *k -> 10(k+1); otherwise 3*lead_N
# (all-N counts 12).  Reports every nimber >= 4 and every NNNNP pattern.
import sys
from p3lib import *
CAP = int(sys.argv[1]); SEED = int(sys.argv[2]); K = int(sys.argv[3])
random.seed(SEED)
ev = Evaluator(f"results_p3r_{K}.tsv", tbits=22, nodelim=2000000, extra=("results.tsv", "results_blocks.tsv", "results_p3.tsv"))
lg = Log(f"p3_rand_hits_{K}.tsv")
vocab = V35 + random.sample(VDBL, 30)
def score(sig):
    v = nimber(sig)
    if isinstance(v, int): return 10 * (v + 1)
    if v == 'N+': return 12
    return 3 * lead_n(sig)
def rand_block():
    w = random.choice((5, 6, 6))
    for _ in range(1000):
        blk = [random.choice(vocab) for _ in range(w)]
        f, L = random.choice(TYPES)
        if legal_start(blk + wall(L, f)): return blk, f, L
def mutate(blk):
    b = list(blk); r = random.random()
    if r < 0.6: b[random.randrange(len(b))] = random.choice(vocab)
    elif r < 0.8:
        i = random.randrange(len(b)); w, bb = parse_token(b[i])
        if random.random() < 0.5 and w: w = {max(2, min(6, x + random.choice((-1, 1)))) for x in w}
        elif bb: bb = {max(3, min(7, x + random.choice((-1, 1)))) for x in bb}
        b[i] = make_token(w, bb) if (w or bb) else b[i]
    elif r < 0.9 and len(b) > 5: del b[random.randrange(len(b))]
    elif len(b) < 6: b.insert(random.randrange(len(b) + 1), random.choice(vocab))
    else:
        i, j = random.randrange(len(b)), random.randrange(len(b)); b[i], b[j] = b[j], b[i]
    return b
calls0 = ev.n_new; best_ever = 0
step = 0
while ev.n_new - calls0 < CAP:
    cur, f, L = rand_block(); full = cur + wall(L, f)
    cs = score(ev.sig(full)); lg.rec("rand", cur, f, L, ev.sig(full))
    stall = 0
    while stall < 150 and ev.n_new - calls0 < CAP:
        nb = mutate(cur)
        if random.random() < 0.05: f2, L2 = random.choice(TYPES)
        else: f2, L2 = f, L
        full = nb + wall(L2, f2)
        if not legal_start(full): stall += 1; continue
        sig = ev.sig(full); lg.rec("rand", nb, f2, L2, sig)
        s = score(sig); v = nimber(sig)
        if isinstance(v, int) and v > best_ever: best_ever = v; print("best nimber so far", v, S(nb), f2, L2, sig, flush=True)
        if sig[:5] == 'NNNNP': print("STAR4-PATTERN", S(nb), f2, L2, sig, flush=True)
        if s >= cs:
            if s > cs: stall = 0
            else: stall += 1
            cur, f, L, cs = nb, f2, L2, s
        else: stall += 1
    step += 1
    if step % 10 == 0: print("restarts", step, "calls", ev.n_new - calls0, dict(lg.hist), flush=True)
print("done", ev.n_new - calls0, dict(lg.hist), "best", best_ever)
