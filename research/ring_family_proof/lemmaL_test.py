"""Stress test of the insertion lemma (Lemma L of the proof) on RANDOM zone states.

Lemma L.  Let p be a non-terminal e.p.-free position on C_n whose files c-rho+1 .. c+rho (cut between c and c+1) hold the
periodic wall pattern ("pristine").  Let p^ be p with two further wall files inserted at the cut (copies of the files
c+1, c, in this order, so that the pattern continues).  Then for each side X
   * the set of children of KEPT moves of p^ is exactly ins(children of kept moves of p), and
   * X has a terminal-win move in p^ iff X has one in p.
(kept = not a terminal loss, not poisoned, not a terminal win; see graph.py).  Here rho = RHO below.

This script draws random contents for the "zone" files (outside the pristine arc), keeps the positions that are
non-terminal and e.p.-free, and compares the engine's move classification on p and p^.  It is a stress test of the
hand proof, not part of it.
Usage: python lemmaL_test.py <odd|even|F> <samples> [seed] [rho]
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam
from fam import parse_classify


def pristine_cuts(famname, p, S, n, rho):
    """cuts c (between files c and c+1, no wrap) such that files c-rho+1 .. c+rho are wall files that still hold the pattern"""
    wall = fam.wall_files(famname, n)
    good = [(j in wall and p[j] == S[j]) for j in range(n)]
    return [c for c in range(rho - 1, n - rho) if all(good[c + d] for d in range(-rho + 1, rho + 1))]

def rand_file(rng):
    w = sorted(rng.sample(range(2, 8), rng.choice([0, 0, 1, 1, 1, 2])))
    b = sorted(rng.sample(range(2, 8), rng.choice([0, 0, 1, 1, 1, 2])))
    b = [r for r in b if r not in w]
    return fam.join_file((tuple(w), tuple(b)))

def classify_many(texts):
    out = fam.run_rg("classify", "\n".join(texts) + "\n")
    return parse_classify(out)

def summarize(blk):
    """per side: (set of kept child strings, has terminal win)"""
    kept = {"W": set(), "B": set()}; tw = {"W": False, "B": False}
    for side, code, mv, child in blk["mv"]:
        if code == "K": kept[side].add(child)
        if code == "T": tw[side] = True
    return kept, tw

def ins_str(child, c):
    t = child.split()
    files = [x for x in t if not x.startswith("ep")]
    eps = [x for x in t if x.startswith("ep")]
    out = files[:c + 1] + ([files[c], files[c + 1]] if os.environ.get('MUTATE') else [files[c + 1], files[c]]) + files[c + 1:]
    res = []
    for e in eps:
        f = int(e.split("=")[1])
        res.append(e.split("=")[0] + "=" + str(f if f <= c else f + 2))
    return " ".join(out + res)


def walkers(famname, count, rng, rho, steps, allow_ep=False):
    """random walks from the start position using only moves of pawns near the zone (all non-terminal moves, kept or not)"""
    zone_of = {"odd": lambda n: [n - 1, 0, 1, 2, 3, 4], "even": lambda n: [n - 1, 0, 1, 2, 3], "F": lambda n: [n - 1, 0, 1, 2, 3, 4]}[famname]
    nlist = {"odd": list(range(2 * rho + 7, 2 * rho + 20, 2)), "even": list(range(2 * rho + 6, 2 * rho + 20, 2)), "F": list(range(2 * rho + 8, 2 * rho + 21))}[famname]
    state = []
    for _ in range(count):
        n = rng.choice(nlist); S = fam.FAMILIES[famname](n)
        state.append((n, S, list(S)))
    snaps = []
    for step in range(steps):
        blocks = classify_many([" ".join(p) for n, S, p in state])
        for i, ((n, S, p), blk) in enumerate(zip(state, blocks)):
            zone = zone_of(n)
            cand = [(code, mv, child) for side, code, mv, child in blk["mv"]
                    if code in "KP" and min(abs(int(mv.split(".")[0]) - z) for z in zone) <= 2 + step // 3]
            if not cand: continue
            code, mv, child = rng.choice(cand)
            newp = child.split()
            if any(x.startswith("ep") for x in newp) and not allow_ep:
                continue
            state[i] = (n, S, newp)
            snaps.append((n, S, newp))
    return snaps

def main():
    famname = sys.argv[1]; samples = int(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rho = int(sys.argv[4]) if len(sys.argv) > 4 else 7
    rng = random.Random(seed)
    zone_of = {"odd": lambda n: [n - 1, 0, 1, 2, 3, 4], "even": lambda n: [n - 1, 0, 1, 2, 3], "F": lambda n: [n - 1, 0, 1, 2, 3, 4]}[famname]
    nlist = {"odd": list(range(2 * rho + 7, 2 * rho + 20, 2)), "even": list(range(2 * rho + 6, 2 * rho + 20, 2)), "F": list(range(2 * rho + 8, 2 * rho + 21))}[famname]
    cases = []
    while len(cases) < samples:
        n = rng.choice(nlist)
        S = fam.FAMILIES[famname](n)
        zone = set(zone_of(n))
        # pristine arc: all files not in zone and at least rho from the zone on both sides
        free = [j for j in range(n) if j not in zone]
        p = list(S)
        mode = rng.random()
        for j in zone:
            r = rng.random()
            p[j] = S[j] if r < 0.25 else rand_file(rng)
        # optionally also randomise the files adjacent to the zone (a wider active zone)
        for j in range(n):
            if j not in zone and min((abs(j - z) for z in zone), default=99) <= 2 and rng.random() < 0.3:
                p[j] = rand_file(rng)
        # pick a cut such that files c-rho+1..c+rho are pristine
        ok = pristine_cuts(famname, p, S, n, rho)
        if not ok: continue
        c = rng.choice(ok)
        cases.append((n, c, p, S))
    for n, S, p in walkers(famname, max(40, samples // 20), rng, rho, 14):
        ok = pristine_cuts(famname, p, S, n, rho)
        if ok: cases.append((n, rng.choice(ok), p, S))
    texts = []
    for n, c, p, S in cases:
        texts.append(" ".join(p))
        texts.append(" ".join(p[:c + 1] + ([p[c], p[c + 1]] if os.environ.get('MUTATE') else [p[c + 1], p[c]]) + p[c + 1:]))
    blocks = classify_many(texts)
    assert len(blocks) == len(texts)
    used = 0; bad = 0; nontriv = 0; withT = 0; withK = 0
    for i, (n, c, p, S) in enumerate(cases):
        b1, b2 = blocks[2 * i], blocks[2 * i + 1]
        if b1["passed"] != "PASSED 0 0" or b2["passed"] != "PASSED 0 0": continue
        used += 1
        k1, t1 = summarize(b1); k2, t2 = summarize(b2)
        good = True
        for X in "WB":
            if {ins_str(x, c) for x in k1[X]} != k2[X] or t1[X] != t2[X]: good = False
        nontriv += any(k1[X] for X in "WB")
        withT += any(t1.values()); withK += sum(len(k1[X]) for X in "WB")
        if not good:
            bad += 1
            if bad <= 3: print("COUNTEREXAMPLE n=%d c=%d" % (n, c), " ".join(p), "\n   kept p:", k1, t1, "\n   kept p^:", k2, t2)
    print(f"Lemma L stress test [{famname}, rho={rho}]: {len(cases)} drawn, {used} non-terminal; positions with a kept move: {nontriv}; with a terminal-win move: {withT}; total kept moves compared {withK}; counterexamples: {bad}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
