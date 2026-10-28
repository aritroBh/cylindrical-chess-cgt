import json, sys
base = "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K21/chess/"
def load(fn):
    d = {}
    for l in open(base + fn):
        if " | " in l:
            p, r = l.rsplit(" | ", 1); d[p.strip()] = r.split()
    return d
def f(v): return v[0] if v[0] == v[1] else v[0] + "/" + v[1]
for pj, rf in (("pred.json", "results_P.txt"), ("pred_rand.json", "results_rand_P.txt")):
    rows = json.load(open(base + pj)); res = load(rf)
    ag = dis = 0; by = {}
    for r in rows:
        b = r["base"] + " " + r["ctx"]
        got = (f(res[b + " w -"]), f(res[b + " b -"])); pred = tuple(r["pred"])
        k = (r["group"], pred)
        by.setdefault(k, [0, 0]); by[k][got == pred] += 1
        ag += got == pred; dis += got != pred
        if got != pred: print("  DIFF", r["group"], r["ctx"], "pred", pred, "P:", got)
    print(pj, rf, "n=%d agree=%d differ=%d" % (len(rows), ag, dis)); 
    for k, v in sorted(by.items()): print("   ", k, "differ/agree", v)
