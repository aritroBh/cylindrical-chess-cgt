"""K75: king route lengths from the group to the context file (a geometric candidate for the rule of question 3).

For a group and a context file f (the context: one White pawn on f2 and one Black pawn on f3, the commonest failing
context; and the mirror target, a Black pawn on f7 or f3):
  rB = least number of Black king moves from a shuttle square (min over the two) to capture a White pawn on f2
       (blocked by a Black pawn on f3), the king never entering a square occupied by a pawn or attacked by a White
       group pawn, nor a square next to the White king's root square;
  rW = least number of White king moves from its root square to capture a Black pawn on f3 (with a White pawn on f2),
       avoiding squares occupied by pawns, attacked by a Black group pawn or next to either shuttle square.
A static count (pieces do not move meanwhile); it is a geometric quantity, not a game value.
Usage (repository root): PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K75/src/routes.py -> logs/routes.txt
"""
from collections import deque
V = "kings/delegate/out/K75"
sq = lambda s: (ord(s[0]) - 97, int(s[1]) - 1)
adj = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1

def bfs(starts, target, bad):
    d = {s: 0 for s in starts}; q = deque(starts)
    while q:
        x = q.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                y = (x[0] + dx, x[1] + dy)
                if y == x or not (0 <= y[0] < 8 and 0 <= y[1] < 8) or y in d: continue
                if y == target: return d[x] + 1
                if bad(y): continue
                d[y] = d[x] + 1; q.append(y)
    return 99

out = ["# group file rB rW fB fW  (see the docstring; fB, fW: least king moves to any square of the context file, group pawns as the only obstacles, never next to the other king's squares)"]
for l in open(f"{V}/in/groups48.txt"):
    if l.startswith("#"): continue
    r = l.rstrip("\n").split("|")
    nm, WK, kA, kB = r[0], sq(r[3]), sq(r[4]), sq(r[5])
    wp = [sq(s) for s in r[6].split(",")]; bp = [sq(s) for s in r[7].split(",")]
    for f in r[13]:
        F = ord(f) - 97
        cw, cb = (F, 1), (F, 2)
        occ = set(wp) | set(bp) | {cw, cb}
        watt = {(p[0] + d, p[1] + 1) for p in wp + [cw] for d in (-1, 1)}
        batt = {(p[0] + d, p[1] - 1) for p in bp + [cb] for d in (-1, 1)}
        rB = bfs([kA, kB], cw, lambda y: y in occ or y in watt or adj(y, WK))
        rW = bfs([WK], cb, lambda y: y in occ or y in batt or adj(y, kA) or adj(y, kB))
        # second measure: moves to reach the context file itself (any rank), group pawns only as obstacles
        occ0 = set(wp) | set(bp)
        watt0 = {(p[0] + d, p[1] + 1) for p in wp for d in (-1, 1)}
        batt0 = {(p[0] + d, p[1] - 1) for p in bp for d in (-1, 1)}
        def tofile(starts, bad):
            best = 99
            for rk in range(8):
                t = (F, rk)
                if t in occ0 or bad(t): continue
                best = min(best, 0 if t in starts else bfs(starts, t, bad))
            return best
        fB = tofile([kA, kB], lambda y: y in occ0 or y in watt0 or adj(y, WK))
        fW = tofile([WK], lambda y: y in occ0 or y in batt0 or adj(y, kA) or adj(y, kB))
        out.append(f"{nm} {f} {rB} {rW} {fB} {fW}")
open(f"{V}/logs/routes.txt", "w").write("\n".join(out) + "\n")
