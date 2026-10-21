"""Regenerate the worker's T1 sample (lemmas/test_L2_big.run, seed 1, n 1500)
with the same RNG call sequence, then for every sample compare
   mine (indep.py): HSS, (E), nontrivial flag, oS (BIG=256 and BIG=max M+1), oW
   worker:          common.hereditarily_safe, cgt.outcome(pawns.value), alt_outcome
Secondary check only: the worker code is imported for the comparison side.
usage: cd <root>; PYTHONPATH=. .venv/bin/python <this> [N] [SEED]
"""
import sys, random, time
from collections import Counter
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/verify/lemmas/L2.1-HSS-theorem-refute')
import indep as I
from cylcgt import cgt, pawns
from cylcgt.pawns import Board
from lemmas.common import RULES, S, W, alt_outcome, hereditarily_safe, random_position, terminal

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1


def to_mine(b, x):
    e = None
    if x.ep:
        e = (tuple(x.ep[0]), tuple(x.ep[1]), x.ep[2])
    return I.Board(b.files, b.ranks, b.wrap, b.ep), I.mkpos(x.white, x.black, e)


memo = {}


def props(bd, y):
    key = (bd, y)
    if key in memo:
        return memo[key]
    tau = I.tau_of(bd)
    comps = I.components(bd, y)
    h, e_ok, nt = True, True, False
    if len(comps) >= 2:
        ts = [tau(c) for c in comps]
        if any(1 in a and -1 in b for i, a in enumerate(ts) for j, b in enumerate(ts) if i != j):
            h = False
        if I.ep_usable(bd, y):
            e_ok = False
        live = sum(1 for c in comps if I.gen_moves(bd, c, "W") or I.gen_moves(bd, c, "B"))
        if live >= 2 and any(ts):
            nt = True
    for side in ("W", "B"):
        for c in I.gen_moves(bd, y, side):
            wp, bp = I.status(bd, c)
            if not (wp or bp):
                ch, ce, cn = props(bd, c)
                h &= ch; e_ok &= ce; nt |= cn
    memo[key] = (h, e_ok, nt)
    return memo[key]


rng = random.Random(SEED)
st = Counter()
bad = []
done = 0
t0 = time.time()
while done < N:
    files = rng.choice([4, 5, 6, 7, 8])
    ranks = rng.choice([6, 7, 8])
    b = Board(files, ranks, rng.random() < 0.6, rng.random() < 0.5)
    x = None
    nw, nb = rng.randint(1, 4), rng.randint(1, 4)
    for _ in range(300):
        p = random_position(rng, b, nw, nb)
        if terminal(b, p) is None:
            x = p
            break
    if x is None:
        continue
    rule = rng.choice(RULES)
    try:
        s, w = S(b, x, rule), W(b, x, rule)
        a = alt_outcome(b, x, rule)
    except pawns.RaceError:
        continue
    done += 1
    if done % 50 == 0: print(f"  {done} done {time.time()-t0:.0f}s", flush=True)
    bd, y = to_mine(b, x)
    h, e_ok, nt = props(bd, y)
    hw = hereditarily_safe(b, x)
    mw, mbb = I.move_bound(bd, y)
    myW = I.oW(bd, y, rule)
    myS = I.oS(bd, y, rule, BIG=256)
    myS_t = I.oS(bd, y, rule, BIG=max(mw, mbb) + 1)
    wS, wW = cgt.outcome(s), cgt.outcome(w)
    if hw != h: bad.append(("HSS differs", str(b), str(x), rule, hw, h))
    if wS != myS: bad.append(("o(S) differs", str(b), str(x), rule, wS, myS))
    if wW != myW or a != myW: bad.append(("o(W) differs", str(b), str(x), rule, wW, a, myW))
    st[("HSS" if h else "notHSS", "E" if e_ok else "notE", "nontriv" if nt else "triv",
        "agree" if myS == myW else "DISAGREE")] += 1
    if h and myS_t != myW:
        bad.append(("tight-BIG disagreement on HSS", str(b), str(x), rule, myS_t, myW))
print(f"regenerated sample n={N} seed={SEED} in {time.time()-t0:.0f}s")
for k in sorted(st, key=str):
    print("   ", k, st[k])
print("implementation mismatches / tight-BIG HSS failures:", len(bad))
for z in bad[:20]:
    print("   ", z)
