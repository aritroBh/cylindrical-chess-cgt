"""Join part1 (freeze failures) with part3 (extended-model *2 test).
Run after freeze_indep.py 1 and part3_captures.py:
  cd /Users/aritro/Downloads/Research/Chessendgames/verify/cylatlas/C7-refute && \
  ../../../.venv/bin/python -I join_summary.py"""
import json
p1 = [json.loads(l) for l in open("part1_freeze.jsonl")]
p3 = [json.loads(l) for l in open("part3_captures.jsonl")]
key = lambda x: (x["board"], x["o"], x["mirror"], x["s"], x["r"])
d3 = {key(x): x for x in p3}
for b in ("cyl8", "flat8"):
    tab = {}
    for x in p1:
        if x["board"] != b:
            continue
        hascheck = "check" in x["std"]["kinds"]
        k = ("passes-freeze" if x["std"]["ok"] else ("check reachable" if hascheck else "capture-only"),
             d3[key(x)]["capturer_realep"]["star2"] and d3[key(x)]["opponent_realep"]["star2"])
        tab[k] = tab.get(k, 0) + 1
    print(b, {f"{a} / *2 survives={s}": n for (a, s), n in sorted(tab.items())})
