#!/usr/bin/env python3
"""crosscheck_sample.py WIDTH NW NB COUNT SEED : draw COUNT random no-passer roots (all WIDTH files occupied) and compare the
outcome string of G+*k (k=0..7) from the C program s3 with the Codex solver's outcome-mask recursion (independent code)."""
import os, random, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex")); sys.setrecursionlimit(1000000)
import solver as cx
width, nw, nb, count, seed = map(int, sys.argv[1:6])
rnd = random.Random(seed)
game = cx.PawnGame(width, "count", True, "aware")
def sq(f, r): return f"{chr(97+f)}{r}"
roots = []
while len(roots) < count:
    ws = rnd.sample([(f, r) for f in range(width) for r in range(2, 7)], nw)
    bs = rnd.sample([(f, r) for f in range(width) for r in range(3, 8)], nb)
    if set(ws) & set(bs) or len({f for f, _ in ws + bs}) != width: continue
    text = "W: " + " ".join(sorted(sq(*x) for x in ws)) + " / B: " + " ".join(sorted(sq(*x) for x in bs))
    w, b = cx.parse_position(text.replace(":", ""), width)
    if game.passers(w, b) != ([], []): continue
    roots.append((text, w, b))
path = os.path.join(HERE, "tmp", f"_xc_{width}_{nw}{nb}_{seed}.txt")
open(path, "w").write("\n".join(t for t, _, _ in roots) + "\n")
out = subprocess.run([os.path.join(HERE, "s3"), "--flat", "--width", str(width), "--eval", path], capture_output=True, text=True).stdout
c = {}
for l in out.splitlines():
    if l.startswith("#"): continue
    p = l.split("\t"); c[p[0]] = p[5]
bad = 0; t0 = time.time()
for text, w, b in roots:
    left, right = game._outcome_masks(w, b, -1, 0)
    s = "".join("N" if (left >> k) & 1 and (right >> k) & 1 else "L" if (left >> k) & 1 else "R" if (right >> k) & 1 else "P" for k in range(8))
    ok = (c.get(text) == s); bad += not ok
    print(("OK  " if ok else "DIFF"), text, s, c.get(text), flush=True)
print(f"checked {len(roots)} random roots, {bad} differences, {time.time()-t0:.0f}s")
