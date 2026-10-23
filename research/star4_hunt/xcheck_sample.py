#!/usr/bin/env python3
"""Cross-check the scanner core (h4) against the Codex mask solver on (a) every hit of the w5 p10 scan (nimber >= 2 and near-*3),
(b) random single-component 10-pawn roots on 5 files.  Usage: from the project root:
   PYTHONPATH=. .venv/bin/python research/star4_hunt/xcheck_sample.py"""
import os, sys, random, subprocess, glob, re, time, signal
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.join(ROOT, "research", "star4_hunt")
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex"))
sys.setrecursionlimit(1000000)
import solver as cx
random.seed(4949)
hits = []
for f in glob.glob(HERE + "/out/w5p10/*.tsv"):
    for line in open(f):
        if line.startswith("#"): continue
        p = line.rstrip("\n").split("\t")
        if p[0].startswith("NEAR"): hits.append(p[1])
        elif len(p) >= 5 and p[4] in ("2", "3"): hits.append(p[0])
hits = sorted(set(hits)); random.shuffle(hits)
def rand_root(nw, nb):
    while True:
        W = random.sample([(f, r) for f in range(5) for r in range(2, 7)], nw)
        B = random.sample([(f, r) for f in range(5) for r in range(3, 8)], nb)
        if set(W) & set(B): continue
        if len({f for f, _ in W + B}) < 5: continue
        # no passed pawn
        def passed(side, mine, theirs):
            for f, r in mine:
                fr = [(g, s) for g, s in theirs if abs(g - f) <= 1 and ((s > r) if side == 'W' else (s < r))]
                if not fr: return True
            return False
        if passed('W', W, B) or passed('B', B, W): continue
        nm = lambda s: f"{chr(97+s[0])}{s[1]}"
        return "W: " + " ".join(map(nm, sorted(W))) + " / B: " + " ".join(map(nm, sorted(B)))
rnd = [rand_root(*random.choice([(5, 5), (4, 6), (5, 5)])) for _ in range(120)]
allp = hits + rnd
open(HERE + "/tmp_xc.txt", "w").write("\n".join(allp) + "\n")
out = subprocess.run([HERE + "/h4", "--flat", "--width", "5", "--max-entries", "8388608", "--eval", HERE + "/tmp_xc.txt"], capture_output=True, text=True).stdout.splitlines()[1:]
c_res = {}
for line in out:
    p = line.split("\t")
    c_res[p[0]] = (p[3], p[4], p[5]) if len(p) > 5 else (p[3], "?", "?")
g = cx.PawnGame(5, "count", True, "aware")
full = (1 << (cx.MAX_NIMBER + 1)) - 1
agree = dis = 0
t0 = time.time()
with open(HERE + "/out/xcheck_w5p10.txt", "w") as fh:
    for pos in allp:
        w, b = cx.parse_position(pos.replace(":", ""), 5)
        signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(TimeoutError()))
        signal.alarm(60)
        try:
            left, right = g._outcome_masks(w, b, -1, 0)
        except TimeoutError:
            fh.write(f"TIMEOUT\t{pos}\n"); fh.flush(); continue
        finally:
            signal.alarm(0)
        nim = next((k for k in range(cx.MAX_NIMBER + 1) if not (left >> k) & 1 and not (right >> k) & 1), -1)
        outc = "N" if (left & 1 and right & 1) else "L" if left & 1 else "R" if right & 1 else "P"
        sig = "".join("N" if ((left >> k) & 1 and (right >> k) & 1) else "L" if (left >> k) & 1 else "R" if (right >> k) & 1 else "P" for k in range(8))
        key = pos
        c = None
        for k2 in c_res:
            if k2.replace(" ", "") == key.replace(" ", ""): c = c_res[k2]; break
        ok = c is not None and c[0] == outc and int(c[1]) == nim and c[2][:8] == sig
        agree += ok; dis += (not ok)
        fh.write(f"{'OK ' if ok else 'DIFF'}\t{pos}\tcodex:{outc},{nim},{sig}\th4:{c}\n"); fh.flush()
    fh.write(f"# agree={agree} disagree={dis} hits_included={len(hits)} random={len(rnd)} time={time.time()-t0:.0f}s\n")
print(f"agree={agree} disagree={dis}")
