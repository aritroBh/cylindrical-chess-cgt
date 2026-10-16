"""Independent check of claim C3 (ring rule for Dawson's chess on a 3 x n cylinder).

Written from scratch by the C3 verifier; it does not import anything from dawson/ or cylcgt/.

Board: 3 ranks (0 = White's home rank, 2 = Black's home rank), n files.
Cell index = rank * n + file. Position = (Wmask, Bmask, side), side 0 = White to move.
Rules: pawn moves one square forward to an empty square, or captures one square diagonally
forward; on the cylinder files 0 and n-1 are adjacent; captures are compulsory; the side to
move with no legal move loses (normal) or wins (misere).

Parts:
  A. For every first move from the full ring (both colours), follow EVERY forced capture line
     until the side to move has no capture; record the resulting positions, the side to move,
     and the set of untouched files.
  B. Plain memoised minimax (normal and misere) from the start, cylinder n and flat strip m,
     straight from the pawn rules. Compare cylinder n with flat n-3 (the ring rule) and with
     an independently computed Grundy sequence of 0.137.

Run:  PYTHONPATH=. .venv/bin/python verify/dawson/C3-reproduce/indep_ring.py NMAX
"""
import sys
import time

sys.setrecursionlimit(1_000_000)


def make(n, wrap):
    def cell(r, f):
        return r * n + f

    def nb(f):
        out = []
        for d in (-1, 1):
            g = f + d
            if wrap:
                g %= n
            if 0 <= g < n and g != f and g not in out:
                out.append(g)
        return out

    NB = [nb(f) for f in range(n)]

    def moves(Wm, Bm, side):
        caps, pushes = [], []
        occ = Wm | Bm
        if side == 0:
            me, them, d = Wm, Bm, 1
        else:
            me, them, d = Bm, Wm, -1
        for r in range(3):
            r1 = r + d
            if not 0 <= r1 <= 2:
                continue
            for f in range(n):
                src = 1 << cell(r, f)
                if not me & src:
                    continue
                for g in NB[f]:
                    dst = 1 << cell(r1, g)
                    if them & dst:
                        caps.append((src, dst))
                dst = 1 << cell(r1, f)
                if not occ & dst:
                    pushes.append((src, dst))
        lst = caps if caps else pushes
        out = []
        for src, dst in lst:
            if side == 0:
                out.append(((Wm & ~src) | dst, Bm & ~dst))
            else:
                out.append((Wm & ~dst, (Bm & ~src) | dst))
        return out, bool(caps)

    start_W = sum(1 << cell(0, f) for f in range(n))
    start_B = sum(1 << cell(2, f) for f in range(n))

    def untouched(Wm, Bm):
        u = []
        for f in range(n):
            if (Wm >> cell(0, f)) & 1 and (Bm >> cell(2, f)) & 1 and not ((Wm | Bm) >> cell(1, f)) & 1:
                u.append(f)
        return u

    def file_state(Wm, Bm, f):
        s = ""
        for r in range(3):
            b = 1 << cell(r, f)
            s += "W" if Wm & b else ("B" if Bm & b else ".")
        return s

    return moves, start_W, start_B, untouched, file_state


def part_A(n):
    """Ring rule: every first move + forced captures -> one strip of n-3 untouched files."""
    moves, W0, B0, untouched, fs = make(n, True)
    problems = []
    for side in (0, 1):
        first, iscap = moves(W0, B0, side)
        assert not iscap and len(first) == n, (n, side, len(first))
        for (Wm, Bm) in first:
            # identify pushed file
            pushed = [f for f in range(n) if fs(Wm, Bm, f) != "W.B"]
            assert len(pushed) == 1
            f = pushed[0]
            ends = set()
            plies = set()
            stack = [(Wm, Bm, 1 - side, 1)]
            while stack:
                w, b, s, k = stack.pop()
                nxt, c = moves(w, b, s)
                if c:
                    for (w2, b2) in nxt:
                        stack.append((w2, b2, 1 - s, k + 1))
                else:
                    ends.add((w, b, s))
                    plies.add(k)
            for (w, b, s) in ends:
                u = untouched(w, b)
                exp_u = [(f + 2 + i) % n for i in range(n - 3)]
                ok = (s == 1 - side and sorted(u) == sorted(exp_u)
                      and fs(w, b, (f - 1) % n) == "..." and fs(w, b, (f + 1) % n) == "..."
                      and fs(w, b, f) == (".WB" if side == 0 else "WB."))
                if not ok:
                    problems.append((n, side, f, [fs(w, b, x) for x in range(n)], s))
            # untouched files must be consecutive around the ring, i.e. one strip
    return problems, plies


def solve_start(n, wrap):
    moves, W0, B0, _, _ = make(n, wrap)
    memo_n, memo_m = {}, {}

    def normal(w, b, s):
        key = (w, b, s)
        v = memo_n.get(key)
        if v is None:
            nxt, _ = moves(w, b, s)
            v = any(not normal(w2, b2, 1 - s) for (w2, b2) in nxt)
            memo_n[key] = v
        return v

    def misere(w, b, s):
        key = (w, b, s)
        v = memo_m.get(key)
        if v is None:
            nxt, _ = moves(w, b, s)
            if not nxt:
                v = True
            else:
                v = any(not misere(w2, b2, 1 - s) for (w2, b2) in nxt)
            memo_m[key] = v
        return v

    if n == 0:
        return (False, False, True, True, 0)
    res = (normal(W0, B0, 0), normal(W0, B0, 1), misere(W0, B0, 0), misere(W0, B0, 1))
    return res + (max(len(memo_n), len(memo_m)),)


def grundy0137(N):
    # 0.137: remove 1 leaving nothing; remove 2 leaving 0 or 1 heap; remove 3 leaving 0, 1 or 2 heaps
    g = []
    for n in range(N + 1):
        opts = set()
        if n == 1:
            opts.add(0)
        if n == 2:
            opts.add(0)
        if n >= 3:
            opts.add(g[n - 2])
        if n == 3:
            opts.add(0)
        for a in range(0, n - 2):
            bb = n - 3 - a
            if bb >= 0:
                opts.add(g[a] ^ g[bb])
        m = 0
        while m in opts:
            m += 1
        g.append(m)
    return g


def main(NMAX):
    g = grundy0137(3000)
    print("g(0..33) =", " ".join(map(str, g[:34])), flush=True)
    for n in range(3, NMAX + 1):
        probs, plies = part_A(n)
        print(f"A ring n={n}: forced-line ply counts {sorted(plies)}; problems {len(probs)}"
              + (f" e.g. {probs[0]}" if probs else ""), flush=True)
    flat = {}
    for m in range(0, NMAX - 2):
        t = time.time()
        flat[m] = solve_start(m, False)
        print(f"B flat m={m}: normal W/B first {flat[m][0]}/{flat[m][1]}, misere {flat[m][2]}/{flat[m][3]},"
              f" g(m)={g[m]}, normal-consistent={flat[m][0] == (g[m] != 0) == flat[m][1]}"
              f" (states {flat[m][4]}, {time.time()-t:.1f}s)", flush=True)
    for n in range(3, NMAX + 1):
        t = time.time()
        c = solve_start(n, True)
        m = n - 3
        ring_rule_normal = c[0] == (not flat[m][0]) and c[1] == (not flat[m][1])
        ring_rule_misere = c[2] == (not flat[m][2]) and c[3] == (not flat[m][3])
        pred = (g[n - 3] == 0)
        print(f"B cyl n={n}: normal W/B first {c[0]}/{c[1]}, misere {c[2]}/{c[3]};"
              f" pred normal (g(n-3)==0) {pred} -> {c[0] == pred == c[1]};"
              f" ring rule vs flat {m}: normal {ring_rule_normal}, misere {ring_rule_misere}"
              f" (states {c[4]}, {time.time()-t:.1f}s)", flush=True)
    # periodicity of the ring outcome, from the independently computed g
    R = {n: g[n - 3] == 0 for n in range(3, 3001)}
    exc = [n for n in range(3, 3001 - 34) if R[n] != R[n + 34]]
    print("ring outcome exceptions R(n) != R(n+34), n <= 2966:", exc)
    for p in range(1, 35):
        if all(R[n] == R[n + p] for n in range(38, 3001 - p)):
            print("least p with R(n+p)=R(n) for all 38<=n<=3000-p:", p)
            break
    gex = [n for n in range(0, 3001 - 34) if g[n] != g[n + 34]]
    print("g exceptions g(n) != g(n+34), n <= 2966:", gex)
    print("first-player ring wins n <= 100:", [n for n in range(3, 101) if R[n]])


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 12)
