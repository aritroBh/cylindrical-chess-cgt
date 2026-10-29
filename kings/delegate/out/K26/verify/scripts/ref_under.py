#!/usr/bin/env python3
"""Referee's own search for exact UNDER groups (U1)-(U4) of the proposed Definition 4.8 (no use of Lemma 4.9).
usage: ref_under.py BOARD nW nB NFILES [i/n]
White king shuttles on an adjacent pair z in F_Z; Black king on ONE square b0 (K1; K2 vs both z squares); <=nW White, <=nB Black pawns on F_Z ranks 2..H-1.
(U1) at both White-to-move roots: shuttle legal and every other White move loses at once (value L after it).
(U2) at both Black-to-move roots: some Black move does not lose at once (value after != W) = freeze.
     A freeze that is a promotion is recorded separately (decisive event, q undefined) and makes the placement NOT exact.
(U3) after every freeze: q (with e.p. flag if a double step), White to move: >=1 legal move, all White moves have value L.
(U4) same q, Black to move (no flag): q legal, >=1 legal move, every Black move has value W.
"""
import sys, itertools, subprocess, os, json
board, nW, nB, NF = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
shard = sys.argv[5] if len(sys.argv) > 5 else "0/1"
si, sn = map(int, shard.split("/"))
cyl = board.startswith("cyl"); W, H = map(int, board.split(":")[1].split("x"))
FILES = list(range(NF))
def fd(a, b):
    d = abs(a - b); return min(d, W - d) if cyl else d
def kdist(s, t): return max(fd(s[0], t[0]), abs(s[1] - t[1]))
def name(s): return chr(97 + s[0]) + str(s[1] + 1)
def unname(n): return (ord(n[0]) - 97, int(n[1:]) - 1)
kingsq = [(f, r) for f in FILES for r in range(H)]
pairs = [(s, t) for i, s in enumerate(kingsq) for t in kingsq[i + 1:] if kdist(s, t) == 1]
pawnsq = [(f, r) for f in FILES for r in range(1, H - 1)]
def subsets(n):
    for k in range(n + 1): yield from itertools.combinations(pawnsq, k)
def attacked_by(pawns, color, sq):
    d = 1 if color == 0 else -1
    return any(r + d == sq[1] and fd(f, sq[0]) == 1 for (f, r) in pawns)
def placements(cfgshard=None):
    _c = -1
    for wp in subsets(nW):
        for bp in subsets(nB):
            if set(wp) & set(bp): continue
            _c += 1
            if cfgshard is not None and _c % cfgshard[1] != cfgshard[0]: continue
            occ = set(wp) | set(bp)
            wpairs = [p for p in pairs if not (set(p) & occ) and not any(attacked_by(bp, 1, s) for s in p)]
            bsqs = [s for s in kingsq if s not in occ and not attacked_by(wp, 0, s)]
            for wz in wpairs:
                for b0 in bsqs:
                    if all(kdist(s, b0) >= 2 for s in wz): yield wp, bp, wz, b0
def pstr(wp, bp, extra=()):
    return " ".join(["P" + name(s) for s in wp] + ["p" + name(s) for s in bp])
bd = board if cyl else board.replace(":", "")
def solve(lines):
    if not lines: return []
    o = subprocess.run(["bin/ref3m", "--board", bd, "--moves"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout.splitlines()
    o = [l for l in o if " | " in l]
    assert len(o) == len(lines)
    out = []
    for l in o:
        t = l.partition(" | ")[2].split()
        out.append((t[0], [x.rsplit(":", 1) for x in t[1:]]))
    return out
rows = list(placements((si, sn))); total = -1
print("placements total", total, "this shard", len(rows), file=sys.stderr, flush=True)
stat = {"placements": len(rows), "U1": 0, "U1_U2_both": 0, "U1_U2_U3": 0, "fail_U4": 0, "freeze_is_promo": 0, "q_illegal_for_U4": 0, "loose1": 0, "exact": []}
CH = 40000
for a in range(0, len(rows), CH):
    part = rows[a:a + CH]
    # stage 1: White-to-move roots
    L1 = []; 
    for (wp, bp, wz, b0) in part:
        for zi in (0, 1): L1.append(f"K{name(wz[zi])} k{name(b0)} {pstr(wp,bp)} w -")
    R1 = solve(L1)
    surv = []
    for k, (wp, bp, wz, b0) in enumerate(part):
        ok = True
        for zi in (0, 1):
            rv, mv = R1[2 * k + zi]
            shut = "K" + name(wz[zi]) + name(wz[1 - zi])
            names = [m for m, v in mv]
            if rv == "X" or names.count(shut) != 1: ok = False; break
            if any(v != "L" for m, v in mv if m != shut): ok = False; break
        if ok: surv.append((wp, bp, wz, b0))
    stat["U1"] += len(surv)
    # stage 2: Black-to-move roots
    L2 = []
    for (wp, bp, wz, b0) in surv:
        for zi in (0, 1): L2.append(f"K{name(wz[zi])} k{name(b0)} {pstr(wp,bp)} b -")
    R2 = solve(L2)
    surv2 = []; freezes = []
    for k, (wp, bp, wz, b0) in enumerate(surv):
        fr = []; ok = True
        for zi in (0, 1):
            rv, mv = R2[2 * k + zi]
            f = [m for m, v in mv if v != "W"]
            if rv == "X" or not f: ok = False; break
            fr.append((zi, f))
        if ok: surv2.append((wp, bp, wz, b0, fr))
    stat["U1_U2_both"] += len(surv2)
    # build q positions for all freezes
    Q = []   # (idx, line_white_to_move, line_black_to_move)
    qinfo = []
    for k, (wp, bp, wz, b0, fr) in enumerate(surv2):
        promo = False
        for zi, fl in fr:
            for m in fl:
                if m == "promo" or "=" in m: promo = True; continue
                if m[0] == "K":
                    fr_sq, to_sq = unname(m[1:3]), unname(m[3:5])
                    nb = to_sq; nbp = list(bp); nwp = list(wp)
                    if to_sq in nwp: nwp.remove(to_sq)
                    ep = "-"
                elif m[0] == "P":
                    fr_sq, to_sq = unname(m[1:3]), unname(m[3:5])
                    nb = b0; nbp = [s for s in bp if s != fr_sq] + [to_sq]; nwp = [s for s in wp if s != to_sq]
                    ep = name((fr_sq[0], fr_sq[1] - 1)) if fr_sq[1] - to_sq[1] == 2 else "-"
                    assert to_sq[1] != 0
                else:
                    raise Exception("unknown move " + m)
                ps = pstr(sorted(nwp), sorted(nbp))
                Q.append((k, f"K{name(wz[zi])} k{name(nb)} {ps} w {ep}", f"K{name(wz[zi])} k{name(nb)} {ps} b -"))
        qinfo.append(promo)
    # evaluate all q
    RW = solve([q[1] for q in Q]); RB = solve([q[2] for q in Q])
    bad = {}
    for (k, lw, lb), (rvw, mvw), (rvb, mvb) in zip(Q, RW, RB):
        r = bad.setdefault(k, {"U3": True, "U4": True, "qill": False})
        if rvw == "X" or not mvw or any(v != "L" for m, v in mvw): r["U3"] = False
        if rvb == "X": r["U4"] = False; r["qill"] = True
        elif not mvb or any(v != "W" for m, v in mvb): r["U4"] = False
    for k, (wp, bp, wz, b0, fr) in enumerate(surv2):
        r = bad.get(k, {"U3": True, "U4": True, "qill": False})
        if not r["U3"]: continue
        stat["U1_U2_U3"] += 1          # K26-style: promotion freezes count as value L
        if not qinfo[k] and all(len(fl) == 1 for zi, fl in fr): stat["loose1"] += 1
        if not r["U4"]:
            stat["fail_U4"] += 1; stat["q_illegal_for_U4"] += r["qill"] and 1 or 0; continue
        if qinfo[k]: stat["freeze_is_promo"] += 1; continue
        stat["exact"].append([list(map(name, wp)), list(map(name, bp)), list(map(name, wz)), name(b0)])
    print("progress", a + len(part), "/", len(rows), file=sys.stderr, flush=True)
print(board, nW, nB, "files", NF, "shard", shard, json.dumps(stat))
json.dump(stat, open(f"logs/under_{board.replace(':','')}_{nW}{nB}_f{NF}_{si}of{sn}.json", "w"))
