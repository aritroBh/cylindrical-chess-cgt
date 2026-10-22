"""C7 10-pawn *2 rings produced by 2-insertion from C5 (all default-setting *2, ringeval): where the C7 scan must find them."""
import sys, json
sys.path.insert(0, "research/ring_family")
from ringlib import *
from closure import classes_of
from ins_search import insertions
import scan_crosscheck as sc
gen = {}
for base in classes_of(5):
    cands = insertions(base, 2)
    res = evaluate([c[2] for c in cands])
    for (slot, block, ring), r in zip(cands, res):
        if r[0] == "N" and r[1] == 2: gen.setdefault(canon(ring), (base, slot, block))
out = []
for c, (b, s, bl) in gen.items():
    for (nw, nb, i, N, done, hit) in sc.info(c):
        # scanner-canonical text
        wm, bm = sc.to_masks(c if nw <= nb and sum(len(a) for a, _ in c) == nw else colour_reverse(c))
        W = len(c)
        cw, cb = sc.scanner_canon(wm, bm, W)
        ws = [f"{chr(97+(s_&7))}{(s_>>3)+1}" for s_ in range(64) if cw >> s_ & 1]
        bs = [f"{chr(97+(s_&7))}{(s_>>3)+1}" for s_ in range(64) if cb >> s_ & 1]
        key = "W: " + " ".join(sorted(ws, key=lambda t: (t[0], int(t[1:])))) + " / B: " + " ".join(sorted(bs, key=lambda t: (t[0], int(t[1:]))))
        out.append((f"p10_{nw}_{nb}", f"c{i}of{N}", "finished" if done else "not yet", "FOUND" if hit else ("MISSING!" if done else "-"), key, cstr(c)))
for o in sorted(out): print("\t".join(o))
