"""K21: compare chess/pred.json with a kpsolve-format results file.  usage: chess_compare.py results_P.txt [results_C.txt]"""
import json, sys, os
here = os.path.dirname(os.path.abspath(__file__)); ch = os.path.join(here, "..", "chess")
rows = json.load(open(os.path.join(ch, "pred.json")))
for fn in sys.argv[1:]:
    res = {}
    for l in open(os.path.join(ch, fn)):
        if " | " in l:
            pos, r = l.rsplit(" | ", 1); res[pos.strip()] = r.split()
    ok = bad = 0
    print("==", fn)
    for r in rows:
        base = r["base"] + " " + r["ctx"]
        if base + " w -" not in res or base + " b -" not in res: continue
        def f(v): return v[0] if v[0] == v[1] else v[0] + "/" + v[1]
        got = (f(res[base + " w -"]), f(res[base + " b -"])); pred = tuple(r["pred"])
        ok += got == pred; bad += got != pred
        print(r["group"], base, "pred", pred, "got", got, "ok" if got == pred else "DIFF")
    print("agree", ok, "differ", bad)
