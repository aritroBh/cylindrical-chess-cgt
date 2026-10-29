"""Re-score the 500 testable components with the corrected convention CC (certified passers; == exact frozen game).
Writes rescore_rows.jsonl (one row per component) and rescore_result.json.  Usage: python3 -I rescore.py"""
import json, sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms")
import pawngame as pg, tests as T
from cc import CC, cfg, R, OUT, PRED
res = {}
allrows = []
for name, (fn, k, off, H) in cfg.items():
    rows = [json.loads(l) for l in open(R + fn)]
    G = pg.Game(k, H, True, off)
    cc = CC(G, T.S_cert)
    trans = collections.Counter()
    for r in rows:
        pos = G.parse(r["P"])
        pred = (cc.node(pos, "W"), cc.node(pos, "B"))
        real = (r["real"]["wtm"][0], r["real"]["btm"][0])
        testable = r["convention_textbook"]["outcome"] != "race" and r["exact"]
        bt, be = r["verdict_textbook"], r["verdict_ep-aware"]
        after = "n/a" if not r["exact"] else ("match" if pred == real else "MISMATCH")
        row = dict(board=name, P=r["P"], testable=testable, before_textbook=bt, before_epaware=be, cc_pred=pred, real=real,
                   frozen=(r["frozen"]["wtm"][0], r["frozen"]["btm"][0]), after=after,
                   cc_equals_frozen=(pred == (r["frozen"]["wtm"][0], r["frozen"]["btm"][0])))
        allrows.append(row)
        if testable:
            trans[(bt, "->", after)] += 1
    res[name] = {f"{a} {b} {c}": v for (a, b, c), v in sorted(trans.items())}
tot = collections.Counter()
for r in allrows:
    if r["testable"]:
        tot["testable"] += 1
        tot["before textbook MISMATCH"] += r["before_textbook"] == "MISMATCH"
        tot["before ep-aware MISMATCH"] += r["before_epaware"] == "MISMATCH"
        tot["after CC MISMATCH"] += r["after"] == "MISMATCH"
        tot["after CC MISMATCH with real=D"] += (r["after"] == "MISMATCH" and "D" in r["real"])
        tot["after CC MISMATCH, real decisive both ways"] += (r["after"] == "MISMATCH" and "D" not in r["real"])
res["total_testable"] = dict(tot)
# 7x6 mismatches by the 143 / 52 / 91 decomposition
c = collections.Counter()
for r in allrows:
    if r["board"] == "cyl7x6" and r["testable"]:
        c[(r["before_textbook"], r["after"])] += 1
res["cyl7x6_before_after"] = {f"{a} -> {b}": v for (a, b), v in c.items()}
json.dump(res, open(OUT + "rescore_result.json", "w"), indent=1)
with open(OUT + "rescore_rows.jsonl", "w") as fh:
    for r in allrows: fh.write(json.dumps(r) + "\n")
print(json.dumps(res, indent=1))
