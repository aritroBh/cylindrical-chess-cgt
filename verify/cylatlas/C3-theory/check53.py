"""Re-evaluate the 53 W-free cylinder-only witnesses of claim C3.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/check53.py

(a) cylcgt main checkout (textbook passed test), count rule, e.p. on  -> must equal the atlas value
(b) same with BIG = 512 instead of 256                               -> W-free value unchanged?
(c) sumtest's independent move generator + passer test (textbook), canonical form via cylcgt.cgt,
    and the brute-force outcome vector vs 15 reference games          -> independent value check
(d) sumtest, e.p.-aware passer test (the convention adopted 2026-10-16)
(e) cylcgt textbook under the 6 (race rule x e.p.) settings
"""
import json, sys
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from sumtest import aware_value

def key(g, memo={}):
    if g.id in memo: return memo[g.id]
    if g.num is not None:
        x = g.num; r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    elif g.nim is not None:
        r = f"*{g.nim}"
    else:
        r = "{" + ",".join(sorted(key(x) for x in g.L)) + "|" + ",".join(sorted(key(x) for x in g.R)) + "}"
    memo[g.id] = r; return r

def hasbig(g, thr):
    seen, st = set(), [g]
    while st:
        x = st.pop()
        if x.id in seen: continue
        seen.add(x.id)
        if x.num is not None and abs(x.num) >= thr: return True
        st.extend(x.L + x.R)
    return False

def setrule(rule):
    if pawns.RACE_RULE != rule:
        pawns.RACE_RULE = rule; pawns._value.cache_clear()

rows = json.load(open("verify/cylatlas/C3-theory/t3_rows.json"))
out = []
for r in rows:
    n, pos = r["n"], Pos.parse(r["pos"])
    setrule("count"); pawns.BIG = 256; pawns._value.cache_clear()
    g = pawns.value(Board(n, 8, True, True), pos)
    rec = {"pos": r["pos"], "n": n, "atlas": r["value"], "a_show": cgt.show(g), "a_key": key(g), "a_bigfree": not hasbig(g, 128)}
    pawns.BIG = 512; pawns._value.cache_clear()
    g2 = pawns.value(Board(n, 8, True, True), pos)
    rec["b_same_as_a"] = key(g2) == key(g); rec["b_bigfree"] = not hasbig(g2, 128)
    pawns.BIG = 256; pawns._value.cache_clear()
    v, brute, pred = aware_value.value(r["pos"], n, True, ep=True, aware=False, race_rule="count")
    rec["c_same_as_a"] = key(v) == key(g); rec["c_brute_eq_pred"] = brute == pred
    v2, brute2, pred2 = aware_value.value(r["pos"], n, True, ep=True, aware=True, race_rule="count")
    rec["d_epaware_show"] = cgt.show(v2); rec["d_epaware_key"] = key(v2); rec["d_same_as_a"] = key(v2) == key(g)
    rec["d_brute_eq_pred"] = brute2 == pred2; rec["d_bigfree"] = not hasbig(v2, 128)
    six = {}
    for rule in ("count", "mover", "opponent"):
        setrule(rule)
        for ep in (True, False):
            gg = pawns.value(Board(n, 8, True, ep), pos)
            six[f"{rule}/ep{int(ep)}"] = cgt.show(gg) if len(cgt.show(gg)) < 70 else ("same" if key(gg) == key(g) else "other(long)")
    setrule("count")
    rec["e_six"] = six
    rec["e_all_same"] = all(s == rec["a_show"] for s in six.values())
    out.append(rec)
    print(json.dumps(rec, ensure_ascii=False), flush=True)
json.dump(out, open("verify/cylatlas/C3-theory/check53_out.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print("SUMMARY")
for k in ("a_bigfree", "b_same_as_a", "b_bigfree", "c_same_as_a", "c_brute_eq_pred", "d_same_as_a", "d_brute_eq_pred", "d_bigfree", "e_all_same"):
    print(k, Counter(x[k] for x in out))
