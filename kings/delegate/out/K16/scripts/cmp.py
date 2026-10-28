#!/usr/bin/env python3
"""cmp.py POS META RES [VIOL_OUT]: every certified instance (beta,p) must be a beta win in P.
Meta tokens: BETA:psq:MASK.H  with MASK (hex) = failure kinds of the strategy 'beta pushes p' against all omega lines
(1 omega stalemated, 2 omega promotes, 4 p captured, 8 beta cannot push, 16 omega stalemated at y) and H = static escape
hypothesis H3K.  Variants: orig (the conjecture as stated), S0 (omega not stalemated at y), S1 (no omega stalemate in any
line), S2 (H3K).  'gap' = instances where the strategy fails other than by stalemate (should be 0)."""
import sys, json
pos, meta, res = sys.argv[1:4]
vout = sys.argv[4] if len(sys.argv) > 4 else None
S = {"orig": [0, 0], "S0": [0, 0], "S1": [0, 0], "S2": [0, 0], "S1S2": [0, 0], "S3": [0, 0]}  # [instances, violating instances]
n = pv = gap = s2bad = 0
bad = []
other = {}
stale_only = 0
with open(pos) as fp, open(meta) as fm, open(res) as fr:
    for lp, lm, lr in zip(fp, fm, fr):
        lp = lp.strip(); a = lm.rstrip("\n").split(" | ")
        r = lr.rstrip("\n").split(" | ")
        assert a[0] == lp and r[0] == lp, (lp, a[0], r[0])
        A, B = r[1].split()
        n += 1
        posbad = False
        badinst = []
        for tok in a[1].split():
            b, p, fl = tok.split(":")
            parts = fl.split(".")
            mask = int(parts[0], 16); h = int(parts[1]); h3 = int(parts[2]) if len(parts) > 2 else None
            want = 'W' if b == 'W' else 'L'
            ok = (A == want and B == want)
            if mask & 14: gap += 1
            if h and (mask & 1): s2bad += 1
            variants = ["orig"]
            if not mask & 16: variants.append("S0")
            if not mask & 1: variants.append("S1")
            if h: variants.append("S2")
            if h and not mask & 1: variants.append("S1S2")
            if h3: variants.append("S3")
            for v in variants:
                S[v][0] += 1
                if not ok: S[v][1] += 1
            if not ok:
                posbad = True
                badinst.append(f"{b}:{p}:{fl}")
        if posbad:
            pv += 1
            bad.append(f"{lp} | {A} {B} | {' '.join(badinst)}")
            other[A + B] = other.get(A + B, 0) + 1
print(json.dumps({"positions": n, "violating_positions": pv, "viol_results": other, "variants[instances,violations]": S, "gap": gap, "S2_but_stalemate": s2bad}))
if vout and bad:
    open(vout, "w").write("\n".join(bad) + "\n")
