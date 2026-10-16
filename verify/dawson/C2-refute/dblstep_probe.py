"""Probe: in reachable positions, does a pawn ever stand on its home rank with both squares ahead empty
while the side to move has NO capture (i.e. a double step, if allowed, would be a legal alternative)?
Also: does any reachable position allow a promotion?"""
import sys
sys.setrecursionlimit(100000)
MAXN = int(sys.argv[1]) if len(sys.argv) > 1 else 12
def run(n, wrap):
    def nb(f):
        out = []
        for g in (f-1, f+1):
            if wrap: g %= n
            if 0 <= g < n and g != f and g not in out: out.append(g)
        return out
    NB = [nb(f) for f in range(n)]
    start = tuple(x for f in range(n) for x in (1, 0, 2))
    seen = set(); stack = [(start, 1), (start, 2)]
    quiet_dbl = 0; any_dbl = 0; promo = 0; ex = None
    while stack:
        b, side = stack.pop()
        if (b, side) in seen: continue
        seen.add((b, side))
        d = 1 if side == 1 else -1; opp = 3 - side
        caps, pushes = [], []
        dbl = False
        for f in range(n):
            for r in range(3):
                if b[f*3+r] != side: continue
                r2 = r + d
                if not 0 <= r2 <= 2: continue
                for g in NB[f]:
                    if b[g*3+r2] == opp: caps.append((f*3+r, g*3+r2, r2))
                if b[f*3+r2] == 0: pushes.append((f*3+r, f*3+r2, r2))
                home = 0 if side == 1 else 2
                if r == home and b[f*3+1] == 0 and b[f*3+(2-home)] == 0: dbl = True
        if dbl:
            any_dbl += 1
            if not caps:
                quiet_dbl += 1
                if ex is None: ex = (b, side)
        for (a, c, r2) in (caps if caps else pushes):
            if (side == 1 and r2 == 2) or (side == 2 and r2 == 0): promo += 1
            l = list(b); l[a] = 0; l[c] = side; stack.append((tuple(l), 3 - side))
    return len(seen), any_dbl, quiet_dbl, promo, ex
def show(b, n):
    return " / ".join("".join(".WB"[b[f*3+r]] for f in range(n)) for r in (2, 1, 0))
for wrap in (False, True):
    for n in range(1 if not wrap else 3, MAXN + 1):
        s, a, q, p, ex = run(n, wrap)
        print("%s n=%-2d states=%-7d dbl-geom=%-6d dbl-geom-with-no-capture=%-5d promotions=%d %s"
              % ("cyl " if wrap else "flat", n, s, a, q, p,
                 ("example(rank3/rank2/rank1, %s to move): %s" % ("WB"[ex[1]-1], show(ex[0], n))) if ex else ""))
