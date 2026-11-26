"""K75: second D-sum predictor, written for K75 without reading dpred.py's solving code (only its output format).

X = the D-game of the pawns of one file alone (Definition 1.1): a White pawn steps one square up to an empty square,
two from rank 2 if both squares are empty; a Black pawn the same downwards from rank 7; a step to the last rank is a
promotion, a terminal win for the mover.  No captures on one file.  over_D (Proposition 4.6): positions w and 0,
White w -> 0, Black w -> w.  Sum rules (Definition 1.3): a side with no move loses; a promotion ends the play; an
infinite play is a draw.  Solved by retrograde analysis with counters (one pass over a queue), not by sweeps.
Prediction (Corollary 4.17 with Lemma 4.15 / Theorem 4.18): root, side s: r(w (+) X, s); q, side s: r(X, s).
Usage:  python3 pred75.py N    prints, for every context of at most N + N pawns (ranks 2-7, file h as a stand-in
for any file), "name  Ab Aw Bb Bw qAb qAw qBb qBw" (White's view, W/L/D).
"""
import itertools, sys
from collections import deque

def succ(state):
    """state = (g, W, B, s): g 1 = w, 0 = zero; W, B frozensets of ranks; s 0 White, 1 Black to move.
    Returns a list of successor states or the string 'WIN' for a promotion by the mover."""
    g, W, B, s = state
    occ = W | B
    out = []
    if s == 0:
        if g == 1: out.append((0, W, B, 1))
        for r in W:
            if r == 7: out.append("WIN"); continue
            if r + 1 not in occ:
                out.append((g, (W - {r}) | {r + 1}, B, 1))
                if r == 2 and 4 not in occ: out.append((g, (W - {r}) | {4}, B, 1))
    else:
        if g == 1: out.append((1, W, B, 0))
        for r in B:
            if r == 2: out.append("WIN"); continue
            if r - 1 not in occ:
                out.append((g, W, (B - {r}) | {r - 1}, 0))
                if r == 7 and 5 not in occ: out.append((g, W, (B - {r}) | {5}, 0))
    return out

def solve(W0, B0):
    # reachable graph
    start = [(g, W0, B0, s) for g in (0, 1) for s in (0, 1)]
    seen, todo, kids = set(start), list(start), {}
    while todo:
        x = todo.pop()
        kids[x] = succ(x)
        for y in kids[x]:
            if y != "WIN" and y not in seen: seen.add(y); todo.append(y)
    par = {x: [] for x in kids}
    for x, ks in kids.items():
        for y in ks:
            if y != "WIN": par[y].append(x)
    res = {}                       # +1 mover wins, -1 mover loses
    cnt = {x: sum(1 for y in kids[x] if y != "WIN") for x in kids}
    q = deque()
    for x, ks in kids.items():
        if "WIN" in ks: res[x] = 1; q.append(x)
        elif not ks: res[x] = -1; q.append(x)
    while q:
        y = q.popleft()
        for x in par[y]:
            if x in res: continue
            if res[y] == -1: res[x] = 1; q.append(x)
            else:
                cnt[x] -= 1
                if cnt[x] == 0: res[x] = -1; q.append(x)
    def r(g, s):
        v = res.get((g, W0, B0, s))
        if v is None: return "D"
        return "W" if (v == 1) == (s == 0) else "L"
    return [r(1, 1), r(1, 0), r(1, 1), r(1, 0), r(0, 1), r(0, 0), r(0, 1), r(0, 0)]

if __name__ == "__main__":
    n = int(sys.argv[1])
    for nw in range(n + 1):
        for ws in itertools.combinations(range(2, 8), nw):
            rest = [x for x in range(2, 8) if x not in ws]
            for nb in range(n + 1):
                for bs in itertools.combinations(rest, nb):
                    name = " ".join([f"Ph{x}" for x in ws] + [f"ph{x}" for x in bs]) or "empty"
                    print(f"{name:22s} {' '.join(solve(frozenset(ws), frozenset(bs)))}")
