"""Independent check of claim C2 (verifier C2-reproduce). Imports nothing from
cylcgt or bench: its own move generator, its own textbook and e.p.-aware
passed tests, its own race judgement, its own minimax.

Usage:  python indep_tree.py <components.jsonl (v2)> <v1 positions .txt (one 'w|position' per line)>

For every component:
  T. build the game graph that the textbook test expands (all positions
     reachable by moves of EITHER side, not expanded below a position where a
     side has a passed pawn) and the graph that the e.p.-aware test expands;
     compare node sets and, at every node, the judgement
     (passed W, passed B, race distances when both are passed).
  O. alternating-play outcome (first passer ends the game, races by rule) of
     the root with each side to move and of every child, in all 12 settings
     (2 passed tests x 3 race rules x e.p. on/off).
"""
import json
import sys
from functools import lru_cache

R = 8
FL = "abcdefgh"


def parse(text):
    w, b = text.split("/")
    sq = lambda t: (FL.index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()), None)


def nbrs(w, f):
    return [g for g in (f - 1, f + 1) if 0 <= g < w]


def gen(w, ep_on, pos, side):
    """Children of pos after a move by side. pos = (W, B, ep), ep = (target, pawn_sq, capturer)."""
    W, B, ep = pos
    mine, theirs = (W, B) if side == "W" else (B, W)
    d, start = (1, 2) if side == "W" else (-1, R - 1)
    occ = W | B
    out = set()

    def put(m, t, e=None):
        out.add((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= R:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            if r == start and (f, r + 2 * d) not in occ:
                e = ((f, r1), (f, r + 2 * d), "B" if side == "W" else "W") if ep_on else None
                put(rest | {(f, r + 2 * d)}, theirs, e)
        for g in nbrs(w, f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif ep is not None and ep[2] == side and ep[0] == t:
                put(rest | {t}, theirs - {ep[1]})
    return out


def pawn_passed(w, pos, side, sq, aware):
    W, B, ep = pos
    f, r = sq
    theirs = B if side == "W" else W
    for (g, s) in theirs:
        if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)):
            return False
    if aware and ep is not None and ep[1] == sq and ep[2] != side:
        # can it be taken e.p. right now? an enemy pawn beside it on the same rank
        if any((g, r) in theirs for g in nbrs(w, f)):
            return False
    return True


def passed(w, pos, side, aware):
    mine = pos[0] if side == "W" else pos[1]
    return any(pawn_passed(w, pos, side, s, aware) for s in mine)


def dist(w, pos, side, aware):
    mine = pos[0] if side == "W" else pos[1]
    best = 10 ** 6
    for (f, r) in mine:
        if not pawn_passed(w, pos, side, (f, r), aware):
            continue
        if side == "W":
            if any((f, s) in mine for s in range(r + 1, R + 1)):
                continue
            dd = R - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in mine for s in range(1, r)):
                continue
            dd = r - 1 - (1 if r == R - 1 else 0)
        best = min(best, dd)
    return best


def judge(w, pos, aware):
    pw, pb = passed(w, pos, "W", aware), passed(w, pos, "B", aware)
    d = (dist(w, pos, "W", aware), dist(w, pos, "B", aware)) if (pw and pb) else None
    return pw, pb, d


def graph(w, root, aware):
    seen, stack = {}, [root]
    while stack:
        q = stack.pop()
        if q in seen:
            continue
        j = judge(w, q, aware)
        seen[q] = j
        if j[0] or j[1]:
            continue
        for side in "WB":
            stack.extend(gen(w, True, q, side))
    return seen


def tree_check(w, root):
    gt, ga = graph(w, root, False), graph(w, root, True)
    same_nodes = set(gt) == set(ga)
    diff = [q for q in gt if q in ga and gt[q] != ga[q]]
    return same_nodes and not diff, len(gt), len(ga), len(diff)


def make_solver(w, ep_on, aware, rule):
    @lru_cache(maxsize=None)
    def after(pos, mover):
        """Winner ('W'/'B') of the position reached by mover's move, other side to move."""
        pw, pb = passed(w, pos, "W", aware), passed(w, pos, "B", aware)
        other = "B" if mover == "W" else "W"
        if pw and pb:
            if rule == "mover":
                return mover
            if rule == "opponent":
                return other
            return other if dist(w, pos, other, aware) <= dist(w, pos, mover, aware) else mover
        if pw:
            return "W"
        if pb:
            return "B"
        return tomove(pos, other)

    @lru_cache(maxsize=None)
    def tomove(pos, side):
        p = pos if (pos[2] is None or pos[2][2] == side) else (pos[0], pos[1], None)
        other = "B" if side == "W" else "W"
        for c in gen(w, ep_on, p, side):
            if after(c, side) == side:
                return side
        return other
    return after, tomove


def outcome(wW, wB):
    """wW: winner with White to move; wB: winner with Black to move."""
    return {("W", "W"): "L", ("B", "B"): "R", ("W", "B"): "N", ("B", "W"): "P"}[(wW, wB)]


def main():
    lib = [json.loads(x) for x in open(sys.argv[1])]
    v1 = [ln.rstrip("\n").split("|") for ln in open(sys.argv[2]) if ln.strip()]
    v1 = [(int(a), b) for a, b in v1]
    libset = {(c["width"], c["position"]) for c in lib}
    # T on v1 (which contains the library)
    n_div, div_in_lib, nodiv_not_in_lib, sizes = 0, [], [], []
    for w, ptxt in v1:
        ok, nt, na, nd = tree_check(w, parse(ptxt))
        sizes.append(nt)
        inlib = (w, ptxt) in libset
        if not ok:
            n_div += 1
            if inlib:
                div_in_lib.append(ptxt)
        elif not inlib:
            nodiv_not_in_lib.append(ptxt)
    print(f"T: v1 components {len(v1)}; trees diverge in {n_div}; diverging but in v2: {len(div_in_lib)}; "
          f"identical but not in v2: {len(nodiv_not_in_lib)}; v2 subset of v1: {libset <= set(v1)}; "
          f"graph sizes min/median/max {min(sizes)}/{sorted(sizes)[len(sizes)//2]}/{max(sizes)}")
    for x in div_in_lib[:10] + nodiv_not_in_lib[:10]:
        print("   ", x)
    # O on v2: outcomes in 12 settings, root and every child
    bad, mism = [], []
    for c in lib:
        w, root = c["width"], parse(c["position"])
        res = []
        for aware in (False, True):
            for rule in ("count", "mover", "opponent"):
                for ep_on in (True, False):
                    after, tomove = make_solver(w, ep_on, aware, rule)
                    r = [outcome(tomove(root, "W"), tomove(root, "B"))]
                    for side in "WB":
                        for ch in sorted(gen(w, ep_on, root, side), key=lambda q: (sorted(q[0]), sorted(q[1]))):
                            # outcome of the child as a game with either side to move next
                            r.append(after(ch, side) if (passed(w, ch, "W", aware) or passed(w, ch, "B", aware))
                                     else outcome(tomove(ch, "W"), tomove(ch, "B")))
                    res.append(tuple(r))
        if any(x != res[0] for x in res):
            bad.append(c["comp_id"])
        if res[0][0] != c["outcome"]:
            mism.append((c["comp_id"], res[0][0], c["outcome"]))
    print(f"O: v2 components {len(lib)}; root/child outcomes differ across the 12 settings in {len(bad)}; "
          f"root outcome != library 'outcome' field in {len(mism)}")
    print("   ", bad[:10], mism[:10])


if __name__ == "__main__":
    main()
