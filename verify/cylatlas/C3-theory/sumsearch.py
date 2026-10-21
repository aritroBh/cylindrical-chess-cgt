"""Is each of the 53 'cylinder-only' values a sum A+B of two W-free values of single FLAT components?
If so, it occurs on a flat 8-file strip once more than 5 pawns are allowed (A on one segment, an empty
file, B on another), so its 'cylinder-only' status is an artefact of the w+b<=5 cap.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/sumsearch.py
"""
import json
from fractions import Fraction
from cylcgt import cgt

def parse(s):
    pos = 0
    def p():
        nonlocal pos
        if s[pos] == "{":
            pos += 1
            L, R = [], []
            cur = L
            while True:
                c = s[pos]
                if c == "|":
                    cur = R; pos += 1; continue
                if c == "}":
                    pos += 1; break
                if c == ",":
                    pos += 1; continue
                cur.append(p())
            return cgt.make(L, R)
        if s[pos] == "*":
            j = pos + 1
            while j < len(s) and s[j].isdigit(): j += 1
            k = int(s[pos+1:j]); pos = j
            return cgt.nimber(k)
        j = pos
        while j < len(s) and (s[j].isdigit() or s[j] in "-/"): j += 1
        t = s[pos:j]; pos = j
        return cgt.number(Fraction(t))
    g = p()
    assert pos == len(s), (s, pos)
    return g

def key(g, memo={}):
    if g.id in memo: return memo[g.id]
    if g.num is not None:
        x = g.num; r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    elif g.nim is not None:
        r = f"*{g.nim}"
    else:
        r = "{" + ",".join(sorted(key(x) for x in g.L)) + "|" + ",".join(sorted(key(x) for x in g.R)) + "}"
    memo[g.id] = r; return r

idx = {}
for line in open("atlas/cylinder/value_index.jsonl"):
    d = json.loads(line); idx[d["key"]] = d
flat = json.load(open("verify/cylatlas/C3-theory/flat_singles.json"))
F = {}
for vid, d in flat.items():
    g = parse(d["key"])
    assert key(g) == d["key"], d["key"]
    F[d["key"]] = (g, d)
# the 53 cylinder-only W-free values, straight from values.jsonl (cyl W-free vids minus flat W-free vids)
byvid = {d["vid"]: d for d in idx.values()}
cylv, flatv, wit = set(), set(), {}
for line in open("atlas/cylinder/values.jsonl"):
    q = json.loads(line)
    if byvid[q["vid"]]["big"]: continue
    (cylv if q["board"] == "cyl" else flatv).add(q["vid"])
    if q["board"] == "cyl":
        s_ = (q["n"], q["w"] + q["b"], q["pos"])
        if q["vid"] not in wit or s_ < wit[q["vid"]]: wit[q["vid"]] = s_
only = sorted(cylv - flatv, key=lambda v: wit[v])
print("cylinder-only W-free values recomputed from values.jsonl:", len(only))
rows = [{"value": byvid[v].get("detail") or byvid[v]["show"], "n": wit[v][0], "pos": wit[v][2], "key": byvid[v]["key"]} for v in only]
res = []
for r in rows:
    k = r["key"]
    X = parse(k)
    hits = []
    for ka, (A, da) in F.items():
        D = cgt.add(X, cgt.neg(A))
        kd = key(D)
        if kd in F:
            db = F[kd][1]
            if da["span"] + db["span"] + 1 <= 8:
                hits.append((da["pawns"] + db["pawns"], da["span"] + db["span"] + 1, da["pos"], da["show"], db["pos"], db["show"]))
    hits.sort()
    res.append({"value": r["value"], "n": r["n"], "cyl_witness": r["pos"], "n_decomp": len(hits), "best": hits[0] if hits else None})
    print(r["n"], r["value"], "->", ("A+B: %d pawns, %d files: [%s]=%s + [%s]=%s" % hits[0]) if hits else "no 2-component flat decomposition", flush=True)
json.dump(res, open("verify/cylatlas/C3-theory/sumsearch_out.json", "w"), indent=1, ensure_ascii=False)
print("decomposable:", sum(1 for x in res if x["best"]), "of", len(res))
