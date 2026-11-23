#!/usr/bin/env python3
"""K43: independent check (ref3m, a different solver and move generator) of the root and q conditions of the exact under test,
for the placements listed on the HALF and LOOSE lines of a plocal output.
usage: verify_roots.py OUTFILE BOARD(cyl:7x6|pln:7x6) KIND(HALF|LOOSE) MAXN
For every placement (shuttle = white king on {a,b}, black king b0, pawns): both roots; at each root the legal moves with their P values
(ref3m --moves); U1: every non-shuttle White move has value L; freezes: Black moves with value != W (a promotion is a freeze that spoils exactness);
U3/U4 of every freeze at the q positions (q with White to move with the e.p. flag if the freeze is a double step; q with Black to move without flag).
Prints one line per placement: rootstatus for z_a: U1, nfreeze, U3, U4  and the verdict 'exact root'.
"""
import sys, subprocess, re
out, board, kind, maxn = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
BIN = sys.argv[5] if len(sys.argv) > 5 else "bin/ref3m43"
def run(lines):
    if not lines: return []
    r = subprocess.run([BIN, "--board", board, "--moves"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout.splitlines()
    r = [l for l in r if " | " in l]
    assert len(r) == len(lines), (len(r), len(lines))
    res = []
    for l in r:
        t = l.partition(" | ")[2].split()
        res.append((t[0], [x.rsplit(":", 1) for x in t[1:]]))
    return res
def parse_pos(s):
    toks = s.split()
    return toks
def name_to_sq(n): return (ord(n[0]) - 97, int(n[1:]) - 1)
def sqname(s): return chr(97 + s[0]) + str(s[1] + 1)
rows = []
for l in open(out):
    if l.startswith(kind + " "):
        m = re.match(r"%s sh=(\d) (.*?) ([wb]) -\s+shuttle (\w\d)(\w\d)" % kind, l)
        if not m: continue
        rows.append((int(m.group(1)), m.group(2).split(), m.group(4), m.group(5)))
rows = rows[:maxn]
tot = {"U1": 0, "rootexact": 0, "n": 0}
for sh, toks, za, zb in rows:
    # tokens: K.. k.. P.. p.. ; sh = 0: White king shuttles (K is on one of the pair), black king single; sh = 1: mirror
    kk = [t for t in toks if t[0] in "Kk"]; pw = [t for t in toks if t[0] in "Pp"]
    wk = [t for t in kk if t[0] == "K"][0][1:]; bk = [t for t in kk if t[0] == "k"][0][1:]
    z = [za, zb]
    sht = 0 if sh == 0 else 1     # shuttler colour index: 0 White
    frc = 1 - sht
    res = []
    for a in (0, 1):
        k_sh = z[a]; k_fr = bk if sh == 0 else wk
        kw, kb = (k_sh, k_fr) if sh == 0 else (k_fr, k_sh)
        base = " ".join(["K" + kw, "k" + kb] + pw)
        # shuttler root
        (rv1, mv1), = run([base + (" w -" if sh == 0 else " b -")])
        shn = "K" + k_sh + z[1 - a]
        names = [m for m, v in mv1]
        lose = "L" if sh == 0 else "W"
        u1 = rv1 != "X" and names.count(shn) == 1 and all(v == lose for m, v in mv1 if m != shn)
        # freezer root
        (rv2, mv2), = run([base + (" b -" if sh == 0 else " w -")])
        win_fr = "W" if sh == 0 else "L"   # value after a freezer move that loses at once for the freezer: shuttler wins
        fz = [m for m, v in mv2 if v != lose and False] if False else [m for m, v in mv2 if v != ("W" if sh == 0 else "L")]
        promo = any(m == "promo" or "=" in m for m in fz)
        # q positions
        okU3 = okU4 = True
        qs_w, qs_b = [], []
        for m in fz:
            if m == "promo" or "=" in m: continue
            pawns_w = [t[1:] for t in pw if t[0] == "P"]; pawns_b = [t[1:] for t in pw if t[0] == "p"]
            fr_sq = m[1:3]; to_sq = m[3:5]; kw2, kb2 = kw, kb; ep = "-"
            if m[0] == "K":
                if sh == 0:
                    kb2 = to_sq; pawns_w = [x for x in pawns_w if x != to_sq]
                else:
                    kw2 = to_sq; pawns_b = [x for x in pawns_b if x != to_sq]
            else:
                if sh == 0:   # Black pawn moves
                    pawns_b = [x for x in pawns_b if x != fr_sq] + [to_sq]; pawns_w = [x for x in pawns_w if x != to_sq]
                    if int(fr_sq[1:]) - int(to_sq[1:]) == 2: ep = fr_sq[0] + str(int(fr_sq[1:]) - 1)
                else:
                    pawns_w = [x for x in pawns_w if x != fr_sq] + [to_sq]; pawns_b = [x for x in pawns_b if x != to_sq]
                    if int(to_sq[1:]) - int(fr_sq[1:]) == 2: ep = fr_sq[0] + str(int(fr_sq[1:]) + 1)
            ps = " ".join(["K" + kw2, "k" + kb2] + ["P" + x for x in pawns_w] + ["p" + x for x in pawns_b])
            qs_w.append(ps + (" w " if sh == 0 else " b ") + ep)    # shuttler to move: with e.p. flag
            qs_b.append(ps + (" b -" if sh == 0 else " w -"))       # freezer to move, no flag
        R3 = run(qs_w); R4 = run(qs_b)
        for rv, mv in R3:
            if rv == "X" or not mv or any(v != lose for m, v in mv): okU3 = False
        for rv, mv in R4:
            if rv == "X": okU4 = False
            elif not mv or any(v != ("W" if sh == 0 else "L") for m, v in mv): okU4 = False
        res.append((u1, len(fz), promo, okU3, okU4))
    tot["n"] += 1
    r0, r1 = res
    ex = [r[0] and r[1] > 0 and not r[2] and r[3] and r[4] for r in res]
    tot["U1"] += all(r[0] for r in res)
    tot["rootexact"] += sum(ex)
    print(sh, " ".join(toks), "shuttle", za + zb, "| root z0:", res[0], "root z1:", res[1], "| exact roots:", ex)
print("placements checked", tot["n"], "U1 at both roots", tot["U1"], "exact roots (total over both roots)", tot["rootexact"])
