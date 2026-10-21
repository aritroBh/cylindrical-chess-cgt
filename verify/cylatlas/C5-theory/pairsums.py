"""C5-theory: which nimbers *k (k>=2) arise as (i) single atoms and (ii) sums of TWO non-W flat atoms
(each <=5 pawns, widths w1+w2<=7 so they fit on an 8-file flat board with an empty file between),
under the textbook test (worker keys) and the e.p.-aware test (epa_*.jsonl keys), count rule, e.p. on.
Sum values are disjunctive sums in the model (valid when no e.p. right is live in a 2-component node,
condition (E) of notes/lemmas.md; not re-checked here for every pair).
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C5-theory/pairsums.py
"""
import glob
import json
import os
import collections
from fractions import Fraction

from cylcgt import cgt

HERE = os.path.dirname(os.path.abspath(__file__))
BIG = 256


def parse(s):
    i = 0

    def game():
        nonlocal i
        if s[i] == "{":
            i += 1
            L = lst("|")
            i += 1  # '|'
            R = lst("}")
            i += 1  # '}'
            return cgt.make(L, R)
        if s[i] == "*":
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            k = int(s[i + 1:j]); i = j
            return cgt.nimber(k)
        j = i
        while j < len(s) and (s[j].isdigit() or s[j] in "-/"):
            j += 1
        x = Fraction(s[i:j]); i = j
        return cgt.number(x)

    def lst(end):
        nonlocal i
        out = []
        if s[i] == end:
            return out
        out.append(game())
        while s[i] == ",":
            i += 1
            out.append(game())
        return out

    g = game()
    assert i == len(s), (s, i)
    return g


def has_big(g, memo={}):
    r = memo.get(g.id)
    if r is None:
        r = abs(g.num) >= BIG // 2 if g.num is not None else any(has_big(x) for x in g.L + g.R)
        memo[g.id] = r
    return r


def npawns(pos):
    return len(pos.replace("W:", "").replace("B:", "").replace("/", " ").split())


rows = []
for f in sorted(glob.glob(os.path.join(HERE, "epa_*.jsonl"))):
    rows += [json.loads(l) for l in open(f)]
print("atoms loaded:", len(rows))
# sanity: parser round trip on a few keys
for conv, field in (("textbook", "key_textbook_worker"), ("e.p.-aware", "key_epa")):
    games = {}
    for r in rows:
        k = r[field]
        if k not in games:
            games[k] = parse(k)
    single = collections.Counter()
    for r in rows:
        g = games[r[field]]
        if g.nim is not None and g.nim >= 2:
            single[(r["board"], r["n"], r["pos"], f"*{g.nim}")] += 1
    print(f"\n[{conv}] atoms whose value is *k, k>=2: {len(single)}")
    for k in sorted(single):
        print("   ", k)
    flat = [(r["n"], npawns(r["pos"]), r["pos"], games[r[field]]) for r in rows if r["board"] == "flat" and not has_big(games[r[field]])]
    # distinct (width, pawns, value) classes, keep one witness
    cls = {}
    for w, p, pos, g in flat:  # one witness per value: narrowest, then fewest pawns
        if g.id not in cls or (w, p) < cls[g.id][:2]:
            cls[g.id] = (w, p, pos, g)
    cl = list(cls.values())
    print(f"[{conv}] non-W flat atoms: {len(flat)}; distinct values: {len(cl)} (one narrowest witness each)")
    hits = collections.defaultdict(list)
    for i in range(len(cl)):
        for j in range(i, len(cl)):
            w1, p1, s1, g1 = cl[i]
            w2, p2, s2, g2 = cl[j]
            if w1 + w2 > 7:
                continue
            g = cgt.add(g1, g2)
            if g.nim is not None and g.nim >= 2:
                hits[(g.nim, p1 + p2)].append((s1, s2))
    for (k, p), lst in sorted(hits.items()):
        lst.sort(key=lambda t: (npawns(t[0]) + npawns(t[1]), t))
        print(f"   witness pairs summing to *{k} with {p} pawns: {len(lst)} value-pairs, e.g. {lst[:3]}")
    if not hits:
        print("   no pair of non-W flat atoms sums to *k (k>=2)")
