"""Falsification test of a STRONGER freeze lemma (theory lens, L3.4).

Lemma F (proof in the verifier's report). Let G be a game every follower H of
which satisfies -BIG < H < BIG. If W(Y) = G then WF(Y) = G. More generally
o(W(Y) + H) = o(WF(Y) + H) for every such H, because the extra king options
-BIG + H (for Left) and BIG + H (for Right) have outcome R resp. L and so are
never winning moves; induction on the sum.

So "WF = *2" for the candidate FOLLOWS from "W = *2": the hypothesis of
Theorem 3.3(b) (every reachable node BIG-interior) is not needed.

Check: on the same random sample as test_L3_trebuchet.py part A (same
generator, same default seed) and on every non-terminal node of the
candidate's tree, whenever canonical W(Y) is 'BIG-bounded' (all followers
strictly between -BIG and BIG), WF(Y) must be identical to W(Y).
Project code used read-only.
Run: cd <project root> && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python \
       verify/lemmas/L3.4-candidate-all-models-theory/freeze_strong.py [--n 400] [--seed 20261015]
"""
import argparse, random, sys
sys.setrecursionlimit(1_000_000)
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import NBIG, PBIG, RULES, W, WF, random_position, reachable, terminal

_bb = {}
def big_bounded(g):
    """every follower x of the canonical form satisfies -BIG < x < BIG"""
    seen, st = set(), [g]
    while st:
        x = st.pop()
        if x.id in seen:
            continue
        seen.add(x.id)
        r = _bb.get(x.id)
        if r is None:
            r = (cgt.le(NBIG, x) and not cgt.le(x, NBIG) and cgt.le(x, PBIG) and not cgt.le(PBIG, x))
            _bb[x.id] = r
        if not r:
            return False
        st.extend(x.L + x.R)
    return True

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=400)
ap.add_argument("--seed", type=int, default=20261015)
a = ap.parse_args()

fails = 0
st = dict(samples=0, bounded=0, bounded_equal=0, unbounded=0, unbounded_differ=0)
rng = random.Random(a.seed)
for _ in range(a.n):
    b = Board(rng.choice([3, 4, 5]), rng.choice([5, 6, 7, 8]), rng.random() < 0.3, rng.random() < 0.5)
    y = None
    for _ in range(200):
        p = random_position(rng, b, rng.randint(1, 3), rng.randint(1, 3))
        if terminal(b, p) is None:
            y = p
            break
    if y is None:
        continue
    rule = rng.choice(RULES)
    try:
        w, wf = W(b, y, rule), WF(b, y, rule)
    except pawns.RaceError:
        continue
    st["samples"] += 1
    if big_bounded(w):
        st["bounded"] += 1
        if w is wf:
            st["bounded_equal"] += 1
        else:
            fails += 1
            print("FAIL (lemma F)", b, y, rule, cgt.show(w), cgt.show(wf))
    else:
        st["unbounded"] += 1
        st["unbounded_differ"] += (w is not wf)
print("random sample:", st)

X = Pos.parse("W: a2 c2 / B: b7 d7")
for ep in (True, False):
    b = Board(4, 8, False, ep)
    for rule in RULES:
        nodes = [z for z in reachable(b, X) if terminal(b, z) is None]
        nb = ne = nd = 0
        for z in nodes:
            w, wf = W(b, z, rule), WF(b, z, rule)
            if big_bounded(w):
                nb += 1
                if w is wf:
                    ne += 1
                else:
                    fails += 1
                    print("FAIL (lemma F) candidate node", z, rule, ep)
            else:
                nd += (w is not wf)
        print(f"candidate tree ep={ep!s:5} {rule:8}: non-terminal {len(nodes)}, W BIG-bounded at {nb} "
              f"(WF identical at {ne}); at the other {len(nodes)-nb} nodes WF differs from W at {nd}; "
              f"root W={cgt.show(W(b, X, rule))} WF={cgt.show(WF(b, X, rule))}")
print("FAILURES:", fails)
