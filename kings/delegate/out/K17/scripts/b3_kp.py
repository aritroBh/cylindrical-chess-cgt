"""kp --frozen on the 48 roots of B3_f86_5 with D_fix != D_whole (all have HSS false): which D does P follow?"""
import json, sys
from k17lib import *
spec = "flat:8x6"; b = board_of(spec)
d = json.load(open("../logs/B3_f86_5.json"))["diffs"]
Z = dict(wk="a1", bk="a5", FZ={0})
def parse_ctx(txt):
    pos, ep = (txt.split(" (ep ") + [None])[:2]
    p = Pos.parse(pos)
    return p, ep[:-1] if ep else None
qs = []; meta = []
for x in d:
    p, ep = parse_ctx(x["ctx"])
    s = x["stm"]
    toks = ["Ka1", "ka5"] + ["P" + name(q) for q in sorted(p.white)] + ["p" + name(q) for q in sorted(p.black)]
    q = " ".join(toks) + (" w " if s == "W" else " b ") + ep
    qs.append(q); meta.append(x)
res, err = run_kp(KP, spec, qs, flags=("--frozen",), heavy=False)
print(err.strip())
agree_whole = sum(1 for q, x in zip(qs, meta) if res[q][0] == x["D_whole"])
agree_fix = sum(1 for q, x in zip(qs, meta) if res[q][0] == x["D_fix"])
print("n", len(qs), "P_frozen == D_whole:", agree_whole, " P_frozen == D_fix:", agree_fix)
json.dump([dict(q=q, P=res[q][0], D_whole=x["D_whole"], D_fix=x["D_fix"]) for q, x in zip(qs, meta)], open("../logs/B3_kp.json", "w"))
