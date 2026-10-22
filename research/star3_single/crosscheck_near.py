#!/usr/bin/env python3
"""crosscheck_near.py COUNT SEED : COUNT random positions within 1-3 pawn edits of position A on 5 files (7-9 pawns, one component,
no passed pawn); compare the outcome string of G+*k (k=0..7) from s3 with the Codex solver's outcome-mask recursion."""
import os, random, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex")); sys.setrecursionlimit(1000000)
import solver as cx
count, seed = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed); width = 5
game = cx.PawnGame(width, "count", True, "aware")
A_W = {(0,4),(1,3),(3,2),(3,3)}; A_B = {(0,7),(1,7),(2,5)}
wsq = [(f, r) for f in range(width) for r in range(2, 7)]; bsq = [(f, r) for f in range(width) for r in range(3, 8)]
def sq(f, r): return f"{chr(97+f)}{r}"
out_roots = {}
while len(out_roots) < count:
    ws, bs = set(A_W), set(A_B)
    for _ in range(rnd.randint(1, 3)):
        side = rnd.choice("WB"); S = ws if side == "W" else bs; pool = wsq if side == "W" else bsq
        kind = rnd.choice(["move", "move", "add", "remove"])
        if kind in ("move", "remove") and len(S) > 1: S.discard(rnd.choice(sorted(S)))
        if kind in ("move", "add"): S.add(rnd.choice(pool))
    if ws & bs or not (7 <= len(ws) + len(bs) <= 9): continue
    if len({f for f, _ in ws | bs}) != width: continue
    text = "W: " + " ".join(sorted(sq(*x) for x in ws)) + " / B: " + " ".join(sorted(sq(*x) for x in bs))
    w, b = cx.parse_position(text.replace(":", ""), width)
    if game.passers(w, b) != ([], []): continue
    out_roots[text] = (w, b)
path = os.path.join(HERE, "tmp", f"_xcn_{seed}.txt"); open(path, "w").write("\n".join(out_roots) + "\n")
res = subprocess.run([os.path.join(HERE, "s3"), "--flat", "--width", str(width), "--eval", path], capture_output=True, text=True).stdout
c = {}
for l in res.splitlines():
    if l.startswith("#"): continue
    p = l.split("\t"); c[p[0]] = p[5]
bad = 0; kinds = set(); t0 = time.time()
for text, (w, b) in out_roots.items():
    left, right = game._outcome_masks(w, b, -1, 0)
    s = "".join("N" if (left >> k) & 1 and (right >> k) & 1 else "L" if (left >> k) & 1 else "R" if (right >> k) & 1 else "P" for k in range(8))
    ok = (c.get(text) == s); bad += not ok; kinds.add(s)
    print(("OK  " if ok else "DIFF"), text, s, c.get(text), flush=True)
print(f"checked {len(out_roots)} positions near A, {bad} differences, {len(kinds)} distinct outcome strings, {time.time()-t0:.0f}s")
