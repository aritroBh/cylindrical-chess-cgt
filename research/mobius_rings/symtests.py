#!/usr/bin/env python3
"""Task 5 and symmetry sanity tests for mob1/mob2 (run in research/mobius_rings).
 A. off-seam: 500 random non-passed positions on 8 files whose pawns avoid both seam files and file 1 and 6
    (files 2..5 only): Moebius value == flat value == cylinder value (C1 and C2).
 B. 500 random non-passed positions that touch only ONE end file (file 0 occupied, file n-1 empty): Moebius == flat.
 C. strip symmetries on random positions with arbitrary direction flags (n = 3,4,5; 1500 each):
    rho (one file shift with the seam flip), mirror, colour swap (colours exchanged, ranks and flags kept: L<->R).
Positions: tokens per file, W/B default direction, w/b reversed (white down / black up)."""
import random, subprocess, sys
random.seed(20261122)
SW = {'N': 'N', 'L': 'R', 'R': 'L', 'P': 'P'}
def run(binary, kind, lines):
    p = subprocess.run(["./" + binary, "solve", "--kind", str(kind)], input="\n".join(lines) + "\n", capture_output=True, text=True)
    return p.stdout.split()
def fmt(pawns, n):
    """pawns: set of (f, r, colour, di); colour 0 W / 1 B; di 0 up(+1) / 1 down(-1)"""
    toks = []
    for f in range(n):
        s = ''
        for c, di, ch in ((0, 0, 'W'), (0, 1, 'w'), (1, 1, 'B'), (1, 0, 'b')):
            rs = ''.join(str(r) for r in range(1, 9) if (f, r, c, di) in pawns)
            if rs: s += ch + rs
        toks.append(s or '-')
    return ' '.join(toks)
def passed_flat_or_strip(pawns, n, twist):
    """independent passed test in cover coordinates (twist: strip)."""
    cov = set()
    for (f, r, c, di) in pawns:
        cov.add((f, r, c, di))
        if twist: cov.add((f + n, 9 - r, c, 1 - di))
    L = 2 * n if twist else n
    for (f, r, c, di) in pawns:
        d = 1 if di == 0 else -1
        blocked = False
        for (g, s, c2, d2) in cov:
            if c2 == c: continue
            if any((g - (f + k)) % L == 0 for k in (-1, 0, 1)) and (s - r) * d > 0: blocked = True; break
        if not blocked: return True
    return False
def rand_pos(n, files, npawn, flags, defaults=True):
    sq = [(f, r) for f in files for r in range(2, 8)]
    chosen = random.sample(sq, npawn); P = set()
    for (f, r) in chosen:
        c = random.randint(0, 1)
        di = c if not flags else random.randint(0, 1)   # default: white up (0), black down (1)
        P.add((f, r, c, di))
    return P
def rho(P, n):
    return {((0, 9 - r, c, 1 - di) if f == n - 1 else (f + 1, r, c, di)) for (f, r, c, di) in P}
def mirror(P, n): return {(n - 1 - f, r, c, di) for (f, r, c, di) in P}
def swap(P, n): return {(f, r, 1 - c, di) for (f, r, c, di) in P}
res = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name, detail); res.append(ok)
# A and B
for tag, n, files, need in (("A_off_seam_files_2to5_of_8", 8, [2, 3, 4, 5], 500), ("B_one_end_file_only_n7", 7, [0, 1, 2, 3, 4, 5], 500)):
    L = []
    while len(L) < need:
        P = rand_pos(n, files, random.randint(4, 8), False)
        if len({(f, r) for f, r, _, _ in P}) < len(P): continue
        if passed_flat_or_strip(P, n, True): continue
        if tag.startswith("B") and (0 not in {f for f, _, _, _ in P}): continue
        L.append(fmt(P, n))
    out = {(b, k): run(b, k, L) for b in ("mob1", "mob2") for k in (0, 1, 2)}
    same = all(out[(b, 2)] == out[(b, 0)] for b in ("mob1", "mob2")) and out[("mob1", 2)] == out[("mob2", 2)] and out[("mob1", 0)] == out[("mob2", 0)]
    cyl = out[("mob1", 1)] == out[("mob1", 2)]
    nontriv = sum(1 for s in out[("mob1", 2)] if s not in ("LLLL", "RRRR"))
    check(tag, same and (cyl if tag.startswith("A") else True), "positions %d, Moebius==flat%s, C1==C2, signatures not LLLL/RRRR: %d" % (len(L), "==cylinder" if tag.startswith("A") else "", nontriv))
# C
for n in (3, 4, 5):
    L = []
    while len(L) < 1500:
        P = rand_pos(n, range(n), random.randint(3, 8), True)
        if len({(f, r) for f, r, _, _ in P}) < len(P): continue
        if passed_flat_or_strip(P, n, True): continue
        L.append(P)
    base = {b: run(b, 2, [fmt(P, n) for P in L]) for b in ("mob1", "mob2")}
    check("C1==C2 flagged n=%d" % n, base["mob1"] == base["mob2"], "%d positions" % len(L))
    for name, fn in (("rho", rho), ("rho^n (strip flip)", None), ("mirror", mirror), ("colour swap (L<->R)", swap)):
        for b in ("mob1", "mob2"):
            if fn is None:
                imgs = []
                for P in L:
                    Q = P
                    for _ in range(n): Q = rho(Q, n)
                    imgs.append(Q)
            else: imgs = [fn(P, n) for P in L]
            img_lines = [fmt(Q, n) for Q in imgs]
            r = run(b, 2, img_lines)
            exp = ["".join(SW[ch] for ch in s) for s in base[b]] if name.startswith("colour") else base[b]
            bad = [i for i in range(len(L)) if r[i] != exp[i] and "RACE" not in (r[i], exp[i])]
            check("%s invariance n=%d %s" % (name, n, b), not bad, "positions %d, mismatches %d" % (len(L), len(bad)))
print("ALL PASS" if all(res) else "SOME FAIL"); sys.exit(0 if all(res) else 1)
