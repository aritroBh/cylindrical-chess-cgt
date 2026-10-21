"""Targeted falsification of Theorem 2.1: sums built ON PURPOSE so that a frozen
+-BIG must outlast play in other live components (the situation Step 1 of the
proof handles). Uses only indep.py.

1. Library: all non-terminal one-component positions on flat strips of width
   1-3 (ranks m), 1-3 pawns per side, <= 5 pawns, classified by threat set tau.
2. Combos (laid side by side with one empty file between parts, flat board):
     {+,-} + {} (+ {})        both-sign part with threat-free live parts
     {+} + {+} (+ {}) ,  {-} + {-} (+ {})
     {+} + {} + {}
   Root is pairwise safe by construction; full HSS and (E) are then checked.
3. For each HSS combo: oW vs oS at BIG = max(M_W,M_B)+1 and BIG = 256, 3 rules.
usage: python -I targeted.py SEED N_COMBOS MAXSEC RANKS EP(0/1)
"""
import sys, time, random, itertools, signal
from collections import Counter
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import indep as I

seed, ncomb, maxsec, m, ep = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
rng = random.Random(seed)
RULES = ("count", "mover", "opponent")

lib = {}  # tau -> list of (width, pos)
for w in (1, 2, 3):
    bd = I.Board(w, m, False, bool(ep))
    tau = I.tau_of(bd)
    sqs = [(f, r) for f in range(w) for r in range(2, m)]
    for nw in (1, 2, 3):
        for nb in (1, 2, 3):
            if nw + nb > 5:
                continue
            for ws in itertools.combinations(sqs, nw):
                rest = [s for s in sqs if s not in ws]
                for bs in itertools.combinations(rest, nb):
                    x = I.mkpos(ws, bs)
                    if len({f for f, _ in ws} | {f for f, _ in bs}) != w:
                        continue  # must occupy every file (one component)
                    wp, bp = I.status(bd, x)
                    if wp or bp:
                        continue
                    if not (I.gen_moves(bd, x, "W") or I.gen_moves(bd, x, "B")):
                        continue
                    lib.setdefault(tau(x), []).append((w, x))
print({tuple(sorted(k)): len(v) for k, v in lib.items()}, flush=True)
P, M, PM, Z = frozenset([1]), frozenset([-1]), frozenset([1, -1]), frozenset()
PATTERNS = [(PM, Z), (PM, Z, Z), (P, P), (P, P, Z), (M, M), (M, M, Z), (P, Z, Z), (PM, Z), (PM, Z)]


class TO(Exception):
    pass


def _al(*a):
    raise TO()


signal.signal(signal.SIGALRM, _al)
stats = Counter()
cex = []
t0 = time.time()
memo = {}


def props(bd, y):
    key = (bd, y)
    r = memo.get(key)
    if r is not None:
        return r
    tau = I.tau_of(bd)
    comps = I.components(bd, y)
    h, e_ok = True, True
    if len(comps) >= 2:
        ts = [tau(c) for c in comps]
        if any(1 in a and -1 in b for i, a in enumerate(ts) for j, b in enumerate(ts) if i != j):
            h = False
        if I.ep_usable(bd, y):
            e_ok = False
    for side in ("W", "B"):
        for c in I.gen_moves(bd, y, side):
            wp, bp = I.status(bd, c)
            if not (wp or bp):
                ch, ce = props(bd, c)
                h &= ch; e_ok &= ce
    memo[key] = (h, e_ok)
    return memo[key]


done = 0
while done < ncomb and time.time() - t0 < maxsec:
    pat = rng.choice(PATTERNS)
    if any(not lib.get(t) for t in pat):
        continue
    parts = [rng.choice(lib[t]) for t in pat]
    rng.shuffle(parts)
    width = sum(w for w, _ in parts) + len(parts) - 1
    if width > 9:
        continue
    bd = I.Board(width, m, False, bool(ep))
    W_, B_ = [], []
    off = 0
    for w, x in parts:
        W_ += [(f + off, r) for f, r in x[0]]
        B_ += [(f + off, r) for f, r in x[1]]
        off += w + 1
    x = I.mkpos(W_, B_)
    signal.alarm(30)
    try:
        h, e_ok = props(bd, x)
        if not h:
            signal.alarm(0)
            stats["combo_not_HSS"] += 1
            continue
        mw, mbb = I.move_bound(bd, x)
        bt = max(mw, mbb) + 1
        out = []
        for rule in RULES:
            ow = I.oW(bd, x, rule)
            out.append((rule, ow, I.oS(bd, x, rule, BIG=bt), I.oS(bd, x, rule, BIG=256)))
        signal.alarm(0)
    except TO:
        stats["timeout"] += 1
        memo.clear(); I.clear_caches(); I._tau_cache.clear()
        continue
    done += 1
    stats[("pattern", tuple(tuple(sorted(t)) for t in pat))] += 1
    for rule, ow, o1, o2 in out:
        ok = (o1 == ow == o2)
        stats[("E" if e_ok else "notE", "agree" if ok else "DISAGREE")] += 1
        stats[("oW", ow)] += 1
        if not ok:
            cex.append(("E" if e_ok else "notE", str(bd), I.show(x), rule, ow, o1, o2))
    if len(memo) > 3_000_000:
        memo.clear(); I.clear_caches(); I._tau_cache.clear()
print(f"seed={seed} ranks={m} ep={ep} combos={done} time={time.time()-t0:.0f}s")
for k in sorted(stats, key=str):
    print("   ", k, stats[k])
print("COUNTEREXAMPLES (E):", len([c for c in cex if c[0] == "E"]))
for c in cex[:30]:
    print("   ", c)
