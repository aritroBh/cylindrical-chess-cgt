"""THEORY-lens checks of claim C1 (verifier scratch; reads cylcgt and sumtest, writes nothing there).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C1-theory/theory.py fingerprint
  PYTHONPATH=. .venv/bin/python verify/sumtest/C1-theory/theory.py identity
  PYTHONPATH=. .venv/bin/python verify/sumtest/C1-theory/theory.py exact --big 16 [--sample N]

fingerprint : what the 15-probe outcome vectors can and cannot certify.
              A probe X with outcome(G+X) = P proves G = -X exactly; any other
              vector only constrains G.  Counts certified cases, distinct cylcgt
              values per fingerprint, and BIG-dominated (all-L/all-R/all-N) cases.
identity    : exact canonical identity.  Build each position's game tree with the
              worker's move generator / passer test / race rule (sumtest.sumsolver.Rules,
              component semantics, passer -> integer +-BIG) and canonicalise it with
              cylcgt.cgt; compare with cylcgt.pawns.value by object identity
              (cgt hash-conses canonical forms).
exact       : cgt-free exact equality.  Brute-force outcome of G + (-v), v = cylcgt
              value, with an explicit-tree solver (no cgt arithmetic; v is only
              traversed).  G = v iff the sum is P.  BIG is monkeypatched in-process
              (pawns.BIG) so the integer chains stay short; the equality test is exact
              for whatever BIG both sides use.
"""
import argparse
import random
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from multiprocessing import Pool

sys.setrecursionlimit(1_000_000)

BOARDS = {"flat3": (3, False), "flat4": (4, False), "cyl3": (3, True), "cyl4": (4, True), "cyl5": (5, True)}
RULES = ("count", "mover", "opponent")
REF = ["0", "*", "*2", "*3", "up", "down", "up*", "dup*", "1/2", "-1/2", "1", "-1", "{1|0}", "+-1", "tiny1"]


def ref_games():
    from cylcgt import cgt
    one, mone = cgt.integer(1), cgt.integer(-1)
    return {"0": cgt.ZERO, "*": cgt.STAR, "*2": cgt.nimber(2), "*3": cgt.nimber(3),
            "up": cgt.UP, "down": cgt.DOWN, "up*": cgt.add(cgt.UP, cgt.STAR),
            "dup*": cgt.add(cgt.add(cgt.UP, cgt.UP), cgt.STAR),
            "1/2": cgt.number(Fraction(1, 2)), "-1/2": cgt.number(Fraction(-1, 2)),
            "1": one, "-1": mone, "{1|0}": cgt.make([one], [cgt.ZERO]), "+-1": cgt.make([one], [mone]),
            "tiny1": cgt.make([cgt.ZERO], [cgt.make([cgt.ZERO], [mone])])}


def setup(board, rule, ep, big=None):
    from cylcgt import pawns
    from sumtest.enum_positions import positions
    if big is not None:
        pawns.BIG = big
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    files, wrap = BOARDS[board]
    geo, pos = positions(files, wrap)
    return pawns, geo, pos, pawns.Board(files, 8, wrap, ep)


# ---------------------------------------------------------------- fingerprint
def fp_task(args):
    board, rule, ep = args
    from cylcgt import cgt
    pawns, geo, pos, b = setup(board, rule, ep)
    R = ref_games()
    out = []
    for W, B in pos:
        text = geo.show(W, B)
        v = pawns.value(b, pawns.Pos.parse(text))
        fp = "".join(cgt.outcome(cgt.add(v, R[n])) for n in REF)
        out.append((text, fp, cgt.show_full(v) if hasattr(cgt, "show_full") else None, v.id, _key(v)))
    return board, rule, ep, out


def _key(g, memo=None):
    """A structural canonical key (process-independent) for a canonical game."""
    if memo is None:
        memo = {}
    if g.id in memo:
        return memo[g.id]
    if g.num is not None:
        k = ("n", str(g.num))
    else:
        k = ("g", tuple(sorted(_key(x, memo) for x in g.L)), tuple(sorted(_key(x, memo) for x in g.R)))
    memo[g.id] = k
    return k


def fingerprint(a):
    tasks = [(b, r, e) for b in BOARDS for r in RULES for e in (False, True)]
    with Pool(12) as p:
        res = p.map(fp_task, tasks)
    from cylcgt import cgt
    total = cert = 0
    allL = allR = allN = 0
    by_fp = defaultdict(set)
    key_show = {}
    certified_by = Counter()
    distinct_cases = set()
    for board, rule, ep, out in res:
        for text, fp, _, _, key in out:
            total += 1
            distinct_cases.add((board, text, ep, fp))
            if "P" in fp:
                cert += 1
                certified_by[REF[fp.index("P")]] += 1
            if fp == "L" * 15:
                allL += 1
            elif fp == "R" * 15:
                allR += 1
            elif fp == "N" * 15:
                allN += 1
            by_fp[fp].add(key)
    print(f"(position, rule, e.p.) cases: {total}  (x15 probes = {total * 15})")
    print(f"cases whose value is certified EXACTLY by a P-probe (G = -X): {cert} ({100 * cert / total:.1f}%)")
    print("   certified value counts (as -X):", dict(certified_by))
    print(f"BIG-dominated fingerprints: all-L {allL}, all-R {allR}, all-N {allN}  "
          f"(total {allL + allR + allN}, {100 * (allL + allR + allN) / total:.1f}%)")
    nvals = len({k for s in by_fp.values() for k in s})
    print(f"distinct cylcgt canonical values: {nvals}; distinct fingerprints: {len(by_fp)}")
    coll = sorted(((len(s), fp) for fp, s in by_fp.items() if len(s) > 1), reverse=True)
    print(f"fingerprints shared by >1 distinct value: {len(coll)}; "
          f"values lying in such shared fingerprints: {sum(n for n, _ in coll)}")
    for n, fp in coll[:8]:
        print(f"   {fp}: {n} distinct values")
    # concrete small examples of distinct values with one fingerprint (rebuild from keys)
    print("examples (first 2 values of the 4 largest shared non-trivial fingerprints):")
    shown = 0
    for n, fp in coll:
        if fp in ("L" * 15, "R" * 15, "N" * 15):
            continue
        ks = sorted(by_fp[fp], key=lambda k: len(repr(k)))[:2]
        print(f"   {fp}: " + "  vs  ".join(cgt.show(_rebuild(k)) for k in ks))
        shown += 1
        if shown == 4:
            break
    # sensitivity of the 'x3 rules x2 ep' multiplicity
    per_pos = defaultdict(set)
    for board, rule, ep, out in res:
        for text, fp, _, _, key in out:
            per_pos[(board, text)].add((ep, rule, key))
    same_all6 = sum(1 for s in per_pos.values() if len({k for _, _, k in s}) == 1)
    print(f"positions: {len(per_pos)}; positions whose cylcgt value is identical in all 6 rule/e.p. settings: "
          f"{same_all6} ({100 * same_all6 / len(per_pos):.1f}%)")
    print(f"distinct (board, position, e.p., fingerprint) tuples: {len(distinct_cases)}")


def _rebuild(k, memo={}):
    from cylcgt import cgt
    if k in memo:
        return memo[k]
    if k[0] == "n":
        g = cgt.number(Fraction(k[1]))
    else:
        g = cgt.make([_rebuild(x) for x in k[1]], [_rebuild(x) for x in k[2]])
    memo[k] = g
    return g


# ---------------------------------------------------------------- identity
def id_task(args):
    board, rule, ep = args
    from cylcgt import cgt
    from sumtest.sumsolver import Rules
    pawns, geo, pos, b = setup(board, rule, ep)
    rules = Rules(geo, ep=ep, ep_aware=False, race_rule=rule, race_double=True)
    BIG = pawns.BIG
    memo = {}

    def comp(W, B, e):
        k = (W, B, e)
        g = memo.get(k)
        if g is None:
            Lo = [child(c, True) for c in rules.moves(W, B, e, True)]
            Ro = [child(c, False) for c in rules.moves(W, B, e, False)]
            g = cgt.make(Lo, Ro)
            memo[k] = g
        return g

    def child(c, white):
        r = rules.resolve(*c, white)
        if r:
            return cgt.integer(BIG if r == "L" else -BIG)
        return tot(*c)

    def tot(W, B, e):
        g = cgt.ZERO
        for c in rules.split(W, B, e):
            g = cgt.add(g, comp(*c))
        return g

    bad = []
    for W, B in pos:
        text = geo.show(W, B)
        v = pawns.value(b, pawns.Pos.parse(text))
        mine = tot(W, B, -1)
        if mine is not v:
            bad.append((text, cgt.show(v), cgt.show(mine)))
    return board, rule, ep, len(pos), bad


def identity(a):
    tasks = [(b, r, e) for b in BOARDS for r in RULES for e in (False, True)]
    n = nb = 0
    with Pool(12) as p:
        for board, rule, ep, cnt, bad in p.imap_unordered(id_task, tasks):
            n += cnt
            nb += len(bad)
            print(f"{board:6s} {rule:8s} ep={'on ' if ep else 'off'} positions {cnt:6d}  non-identical {len(bad)}",
                  flush=True)
            for x in bad[:3]:
                print("     ", x)
    print(f"TOTAL cases {n}, canonical values not identical: {nb}")


# ---------------------------------------------------------------- exact (cgt-free)
def exact_task(args):
    board, rule, ep, big, sample, seed, perturb = args
    from cylcgt import cgt
    from sumtest.sumsolver import Rules
    pawns, geo, pos, b = setup(board, rule, ep, big=big)
    rules = Rules(geo, ep=ep, ep_aware=False, race_rule=rule, race_double=True)
    if sample and sample < len(pos):
        pos = random.Random(f"{seed}-{board}-{rule}-{ep}").sample(pos, sample)
    BIG = big
    movememo = {}

    def comp_moves(c, white):
        k = (c, white)
        r = movememo.get(k)
        if r is None:
            r = []
            for c2 in rules.moves(*c, white):
                res = rules.resolve(*c2, white)
                if res:
                    r.append((None, BIG if res == "L" else -BIG))
                else:
                    live = tuple(x for x in rules.split(*c2)
                                 if rules.moves(*x, True) or rules.moves(*x, False))
                    r.append((live, 0))
            movememo[k] = r
        return r

    LW, RW = {}, {}

    def succ(state, white):
        comps, bank, h = state
        for i, c in enumerate(comps):
            rest = comps[:i] + comps[i + 1:]
            for live, d in comp_moves(c, white):
                nc = rest if live is None else tuple(sorted(rest + live))
                yield (nc, bank + d, h)
        # H = -v : Left's options are -(v^R), Right's are -(v^L)
        for x in (h.R if white else h.L):
            yield (comps, bank, x)
        if white and bank > 0:
            yield (comps, bank - 1, h)
        if not white and bank < 0:
            yield (comps, bank + 1, h)

    def lw(s):
        r = LW.get(s)
        if r is None:
            r = any(not rw(t) for t in succ(s, True))
            LW[s] = r
        return r

    def rw(s):
        r = RW.get(s)
        if r is None:
            r = any(not lw(t) for t in succ(s, False))
            RW[s] = r
        return r

    eps = {"none": None, "eighth": cgt.number(Fraction(1, 8)), "dup": cgt.add(cgt.UP, cgt.UP),
           "star4": cgt.nimber(4)}[perturb]
    R = ref_games()
    bad = []
    fp_same = 0
    for W, B in pos:
        text = geo.show(W, B)
        v = pawns.value(b, pawns.Pos.parse(text))
        if eps is not None:
            v2 = cgt.add(v, eps)
            if all(cgt.outcome(cgt.add(v, R[n])) == cgt.outcome(cgt.add(v2, R[n])) for n in REF):
                fp_same += 1
            v = v2
        comps = tuple(sorted(x for x in rules.split(W, B, -1)
                             if rules.moves(*x, True) or rules.moves(*x, False)))
        s0 = (comps, 0, v)
        if lw(s0) or rw(s0):
            bad.append(text)
    return board, rule, ep, len(pos), bad, len(LW) + len(RW), fp_same


def exact(a):
    tasks = [(b, r, e, a.big, a.sample, a.seed, a.perturb) for b in BOARDS for r in RULES for e in (False, True)]
    n = nb = nfs = 0
    with Pool(12) as p:
        for board, rule, ep, cnt, bad, states, fs in p.imap_unordered(exact_task, tasks):
            n += cnt
            nb += len(bad)
            nfs += fs
            print(f"{board:6s} {rule:8s} ep={'on ' if ep else 'off'} BIG={a.big} perturb={a.perturb} "
                  f"positions {cnt:6d}  G-v not P: {len(bad)}  (states {states})", flush=True)
            if a.perturb == "none":
                for x in bad[:3]:
                    print("     ", x)
    print(f"TOTAL cases {n}, G - v' != 0 (v' = cylcgt value + {a.perturb}): {nb}")
    if a.perturb != "none":
        print(f"   of which the 15-probe fingerprint of v' equals that of v (perturbation invisible to probes): {nfs}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fingerprint", "identity", "exact"])
    ap.add_argument("--big", type=int, default=16)
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--perturb", default="none", choices=["none", "eighth", "dup", "star4"])
    a = ap.parse_args()
    {"fingerprint": fingerprint, "identity": identity, "exact": exact}[a.cmd](a)
