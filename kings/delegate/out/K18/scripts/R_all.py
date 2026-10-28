#!/usr/bin/env python3
"""R (squares the sortie king can reach in lines of the plain local game under optimal play of sbar), T and (L3_F) for the sorties
used in the context experiments (P variant, no queen clause).  usage: R_all.py BOARD SORTIES.json OUT.json"""
import sys, json
sys.path.insert(0, "scripts")
import kit, analysis_R
board, fn, out = sys.argv[1:4]
kit.setboard(board, "0:3")
sel = json.load(open(fn)); res = []
for s in sel:
    r = analysis_R.analyse(s["Q"], qclause=False)
    if r is None: res.append(None); continue
    n, R, l3f = r
    res.append({"T": n, "R": sorted(kit.sqn(x) for x in R), "l3f": l3f})
    print(s["Y"], s["m"], "T", n, "|R|", len(R), "L3F", l3f, flush=True)
json.dump(res, open(out, "w"))
