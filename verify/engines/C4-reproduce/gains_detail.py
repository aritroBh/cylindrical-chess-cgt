"""Detail of the positions where RFP-off flips the +-150 cp root verdict at d3/d4 (reads engine/ablation/results).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C4-reproduce/gains_detail.py"""
import json, re
from pathlib import Path
E = Path(__file__).resolve().parents[3] / "engine"
meta = {}
for p in [E/"suite"/"cgt_verified.epd", E/"suite"/"cgt_disagree.epd"]:
    for line in open(p):
        if line.strip():
            i = re.search(r'id "([^"]+)"', line).group(1)
            meta[i] = (re.search(r"tablebase root: ([a-z-]+)", line).group(1), re.search(r'c5 "class ([^;]+);', line).group(1),
                       re.search(r"value count=([^;]+);", line).group(1))
R = {v: {r["id"]: r for r in json.loads((E/"ablation"/"results"/f"{v}.json").read_text())["results"]} for v in ("base","RFP")}
def cp(s):
    k, x = s.split(); x = int(x); return (100000 if x > 0 else -100000) if k == "mate" else x
def vd(s, thr=150):
    c = cp(s); return "win" if c >= thr else "loss" if c <= -thr else "draw"
for d in ("3", "4"):
    print(f"depth {d}: id tb class value | base score -> RFP score")
    for i, (tb, cl, val) in meta.items():
        b, r = R["base"][i]["iters"][d]["score"], R["RFP"][i]["iters"][d]["score"]
        if (vd(b) == tb) != (vd(r) == tb):
            print(f"  {i} {tb:4s} {cl:13s} {val:>10s} | {b:>9s} -> {r:>9s}  {'GAIN' if vd(r)==tb else 'LOSS'}")
# sign test restricted to wins
for d in ("2","3","4","6"):
    wb = sum(cp(R['base'][i]['iters'][d]['score']) > 0 for i,m in meta.items() if m[0]=='win')
    wr = sum(cp(R['RFP'][i]['iters'][d]['score']) > 0 for i,m in meta.items() if m[0]=='win')
    db = sum(abs(cp(R['base'][i]['iters'][d]['score'])) < 150 for i,m in meta.items() if m[0]=='draw')
    dr = sum(abs(cp(R['RFP'][i]['iters'][d]['score'])) < 150 for i,m in meta.items() if m[0]=='draw')
    import statistics
    mb = statistics.median(cp(R['base'][i]['iters'][d]['score']) for i in meta)
    mr = statistics.median(cp(R['RFP'][i]['iters'][d]['score']) for i in meta)
    print(f"d{d}: wins with score>0 base {wb} RFP {wr} (of 216); draws |s|<150 base {db} RFP {dr} (of 17); median root cp base {mb} RFP {mr}")
