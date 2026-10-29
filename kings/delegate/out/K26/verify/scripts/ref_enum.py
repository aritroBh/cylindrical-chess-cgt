#!/usr/bin/env python3
"""Referee's own enumerator for exact two-shuttle (dud) groups, written from the task statement.
usage: ref_enum.py gen  BOARD(cyl:7x6|flat:7x6) nW nB OUTDIR      -> writes stage-1 root files (chunks) + count
       ref_enum.py run  BOARD nW nB OUTDIR                          -> runs ref3m on chunks, stage 2, prints counts
Definition used (from the task text / FINDINGS section 1):
 F_Z = files a,b,c.  Each king has an adjacent (king-distance 1) pair of squares inside F_Z (ranks 1..H).
 Pawns of the group: at most nW white, nB black on F_Z squares of ranks 2..H-1.
 K1: no king square occupied by a pawn nor attacked by an enemy pawn of the placement.
 K2: every White king square at king distance >=2 from every Black king square.
 Roots: 4 king states x 2 sides.  A leak = legal non-shuttle move of the mover that does not lose at once
 (White mover: value after move != L; Black mover: value after != W).  Exact dud = 0 leaks at all 8 roots.
"""
import sys, itertools, os, subprocess, json
board, nW, nB, out = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
mode = sys.argv[1]
cyl = board.startswith("cyl")
W, H = map(int, board.split(":")[1].split("x"))
FILES = [0, 1, 2]
def fd(a, b):
    d = abs(a - b)
    return min(d, W - d) if cyl else d
def kdist(s, t):
    return max(fd(s[0], t[0]), abs(s[1] - t[1]))
def name(s): return "abc..."[0] if False else chr(ord('a') + s[0]) + str(s[1] + 1)
kingsq = [(f, r) for f in FILES for r in range(H)]
pairs = [(s, t) for i, s in enumerate(kingsq) for t in kingsq[i + 1:] if kdist(s, t) == 1]
pawnsq = [(f, r) for f in FILES for r in range(1, H - 1)]
def subsets(n):
    for k in range(n + 1):
        yield from itertools.combinations(pawnsq, k)
def attacked_by(pawns, color, sq):
    # pawns of `color` (0 white moving up, 1 black moving down) attack sq?
    d = 1 if color == 0 else -1
    for (f, r) in pawns:
        if r + d == sq[1] and fd(f, sq[0]) == 1:  # file distance 1 (cyl wrap handled by fd)
            return True
    return False
def placements():
    for wp in subsets(nW):
        for bp in subsets(nB):
            if set(wp) & set(bp): continue
            occ = set(wp) | set(bp)
            wpairs = [p for p in pairs if not (set(p) & occ) and not any(attacked_by(bp, 1, s) for s in p)]
            bpairs = [p for p in pairs if not (set(p) & occ) and not any(attacked_by(wp, 0, s) for s in p)]
            for wz in wpairs:
                for bz in bpairs:
                    if all(kdist(s, t) >= 2 for s in wz for t in bz):
                        yield wp, bp, wz, bz
def pstr(wp, bp):
    return " ".join(["P" + name(s) for s in wp] + ["p" + name(s) for s in bp])
if mode == "count":
    n = 0
    for _ in placements(): n += 1
    print(board, nW, nB, "placements", n)
    sys.exit()
if mode == "gen":
    os.makedirs(out, exist_ok=True)
    CH = int(os.environ.get("CHUNK", "60000"))
    ci = 0; buf = []; tot = 0
    def flush():
        global ci, buf
        if not buf: return
        with open(f"{out}/s1_{ci:03d}.in", "w") as f:
            for (wp, bp, wz, bz) in buf:
                f.write(f"K{name(wz[0])} k{name(bz[0])} {pstr(wp, bp)} w -\n")
        with open(f"{out}/s1_{ci:03d}.meta", "w") as f:
            json.dump([[list(map(name, wp)), list(map(name, bp)), list(map(name, wz)), list(map(name, bz))] for (wp, bp, wz, bz) in buf], f)
        ci += 1; buf = []
    for row in placements():
        buf.append(row); tot += 1
        if len(buf) >= CH: flush()
    flush()
    print(board, nW, nB, "placements", tot, "chunks", ci)
def sqname_to_t(n): return (ord(n[0]) - 97, int(n[1:]) - 1)
def leaks_from_output(line, stm, kfrom, kto):
    """line: ref3m --moves output. returns (rootvalue, nleaks, shuttle_found_count) ; leak = non-shuttle move whose value is not 'loses at once'"""
    head, _, rest = line.partition(" | ")
    toks = rest.split()
    rv = toks[0]
    bad = "L" if stm == 0 else "W"   # value after the move that means the mover has lost at once
    n = 0; sh = 0; leaklist = []
    for t in toks[1:]:
        mv, v = t.rsplit(":", 1)
        if mv == "K" + kfrom + kto:
            sh += 1; continue
        if v != bad:
            n += 1; leaklist.append(t)
    return rv, n, sh, leaklist
if mode == "run":
    import glob
    bd = board if cyl else board.replace(":", "")
    chunks = sorted(glob.glob(f"{out}/s1_*.in"))
    sel = os.environ.get("CHUNKS")
    if sel:
        a, b = map(int, sel.split("-")); chunks = chunks[a:b + 1]
    hist = {}
    survivors = []
    TMAX = int(os.environ.get('TMAX', '-1'))
    for cf in chunks:
        meta = json.load(open(cf[:-3] + ".meta"))
        res = subprocess.run(["bin/ref3m", "--board", bd, "--moves"], stdin=open(cf), capture_output=True, text=True).stdout.splitlines()
        res = [l for l in res if " | " in l]
        assert len(res) == len(meta), (len(res), len(meta))
        for line, (wp, bp, wz, bz) in zip(res, meta):
            rv, n, sh, ll = leaks_from_output(line, 0, wz[0], wz[1])
            hist[n] = hist.get(n, 0) + 1
            assert sh == 1 and rv != "X", line
            if (n <= TMAX if TMAX >= 0 else (n == 0 and rv == 'D')): survivors.append((wp, bp, wz, bz))
        print(cf, "done", file=sys.stderr, flush=True)
    print("stage1 hist (leaks at root state0, White to move):", dict(sorted(hist.items())), "survivors (0 leaks and root value D)", len(survivors), flush=True)
    # stage 2: all 8 roots of every survivor
    exact = []; hist2 = {}; tot_list = {}
    S = survivors
    B = 20000
    for i in range(0, len(S), B):
        part = S[i:i + B]
        lines = []; keys = []
        for (wp, bp, wz, bz) in part:
            for wi in (0, 1):
                for bi in (0, 1):
                    for stm in (0, 1):
                        lines.append(f"K{wz[wi]} k{bz[bi]} {' '.join(['P'+x for x in wp]+['p'+x for x in bp])} {'wb'[stm]} -")
                        keys.append((wz, bz, wi, bi, stm))
        res = subprocess.run(["bin/ref3m", "--board", bd, "--moves"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout.splitlines()
        res = [l for l in res if " | " in l]
        assert len(res) == len(lines)
        k = 0
        for (wp, bp, wz, bz) in part:
            tot = 0; ok = True
            for j in range(8):
                line = res[k]; (_, _, wi, bi, stm) = keys[k]; k += 1
                kf, kt = (wz[wi], wz[1 - wi]) if stm == 0 else (bz[bi], bz[1 - bi])
                rv, n, sh, ll = leaks_from_output(line, stm, kf, kt)
                tot += n
                if rv != "D" or sh != 1: ok = False
            hist2[tot] = hist2.get(tot, 0) + 1
            if tot <= 2: tot_list.setdefault(tot, []).append((wp, bp, wz, bz))
            if tot == 0 and ok: exact.append((wp, bp, wz, bz))
    print("stage2 total leaks over 8 roots (survivors only):", dict(sorted(hist2.items())))
    print("totals 0/1/2 (complete when TMAX>=2):", [len(tot_list.get(t, [])) for t in (0, 1, 2)])
    print("EXACT DUDS:", len(exact))
    for e in exact: print("  W", e[2], "B", e[3], "wp", e[0], "bp", e[1])
    json.dump({"hist1": hist, "n_surv": len(survivors), "exact": exact}, open(f"{out}/result_{os.environ.get('TAG','x')}.json", "w"))
