"""Cross-check of T10's KPK statistics. Every legal KPK position on the flat and the cylindrical
8x8 board is solved twice: by kings/kpsolve (all promotions) and by the project's own KPK solver
atlas/cylinder/kpk (queen promotion only, written independently). Statistics use kpsolve.

    python3 delegate/checks/kpk_crosscheck.py
"""
import subprocess
from collections import Counter

N = 8
FILES = "abcdefgh"


def name(s):
    return f"{FILES[s % N]}{s // N + 1}"


def dist(a, b, wrap):
    df = abs(a % N - b % N)
    if wrap:
        df = min(df, N - df)
    return max(df, abs(a // N - b // N))


def pawn_attacks(p, s, wrap):
    f, r = p % N, p // N
    out = []
    for df in (-1, 1):
        g = f + df
        if wrap:
            g %= N
        elif not 0 <= g < N:
            continue
        out.append((r + 1) * N + g)
    return s in out


def positions(wrap):
    for wk in range(64):
        for bk in range(64):
            if bk == wk or dist(wk, bk, wrap) <= 1:
                continue
            for p in range(8, 56):
                if p in (wk, bk):
                    continue
                for stm in "WB":
                    if stm == "W" and pawn_attacks(p, bk, wrap):
                        continue  # Black (not to move) in check
                    yield wk, bk, p, stm


res = {}
for wrap in (0, 1):
    pos = list(positions(wrap))
    q = "".join(f"{name(a)} {name(b)} {name(c)} {s}\n" for a, b, c, s in pos)
    out = subprocess.run(["atlas/cylinder/kpk", str(N), str(wrap)], input=q, capture_output=True, text=True).stdout
    alt = [line.split()[-1] for line in out.splitlines() if line.strip()]
    q = "".join(f"K{name(a)} P{name(c)} k{name(b)} {s.lower()} -\n" for a, b, c, s in pos)
    out = subprocess.run(["kings/kpsolve", "--board", f"{'cyl' if wrap else 'flat'}:8x8", "--ep", "on",
                          "--promote", "QRBN", "--cap", "1"], input=q, capture_output=True, text=True).stdout
    vals = [line.split("|")[1].split()[0] for line in out.splitlines() if "|" in line]
    assert len(vals) == len(alt) == len(pos), (len(vals), len(alt), len(pos))
    diff = [(p, v, a) for p, v, a in zip(pos, vals, alt) if v != a]
    print(f"{'cyl' if wrap else 'flat'}: kpsolve vs atlas/cylinder/kpk differ on {len(diff)} of {len(pos)}",
          [f"K{name(p[0])} P{name(p[2])} k{name(p[1])} {p[3]}: {v}/{a}" for p, v, a in diff[:3]])
    res[wrap] = dict(zip(pos, vals))
    c = Counter((p[3], v) for p, v in res[wrap].items())
    for stm in "WB":
        n = c[(stm, "W")] + c[(stm, "D")]
        print(f"{'cyl' if wrap else 'flat'} {stm} to move: {n} legal, {c[(stm, 'W')]} wins ({100 * c[(stm, 'W')] / n:.2f}%)")
common = set(res[0]) & set(res[1])
d2w = sum(1 for p in common if res[0][p] == "D" and res[1][p] == "W")
w2d = sum(1 for p in common if res[0][p] == "W" and res[1][p] == "D")
print(f"legal on both boards: {len(common)}; flat draw -> cyl win: {d2w}; flat win -> cyl draw: {w2d}")
for wrap in (0, 1):
    zz = sum(1 for (wk, bk, p, s), v in res[wrap].items() if s == "W" and v == "D" and res[wrap].get((wk, bk, p, "B")) == "W")
    print(f"{'cyl' if wrap else 'flat'} mutual zugzwangs (W to move draws, B to move White wins): {zz}")

