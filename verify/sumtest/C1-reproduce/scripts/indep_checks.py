"""Verifier checks for claim C1 (sumtest). Reads worker data; writes nothing outside C1-reproduce.

1. Re-enumerate the family with MY OWN loop and cylcgt.pawns.passed() as the filter
   (not the worker's Rules.has_initial_passer); compare counts and key sets.
2. Third implementation for the X=0 column: crosscheck.minimax.outcome_class (Codex,
   alternating play, count rule, textbook passer test) vs worker and cylcgt column 0.
3. Sensitivity: how discriminating is the comparison (distinct vectors, cross-rule and
   e.p. on/off differences, constant vectors).
Run: cd C1-reproduce && PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames \
     /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python scripts/indep_checks.py
"""
import gzip, itertools, json, os, sys
from collections import Counter
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
D = os.path.join(ROOT, "sumtest", "data")
from cylcgt import pawns
from crosscheck import minimax as mm

BOARDS = {"flat3": (3, False), "flat4": (4, False), "cyl3": (3, True), "cyl4": (4, True), "cyl5": (5, True)}
L = "abcdefghij"
def load(n): return json.load(gzip.open(os.path.join(D, n), "rt"))

def my_family(files, wrap):
    b = pawns.Board(files, 8, wrap, False)
    sqs = [(f, r) for f in range(files) for r in range(2, 8)]
    out = set()
    for nw, nb in [(1, 1), (2, 1), (1, 2), (2, 2)]:
        for ws in itertools.combinations(sqs, nw):
            rest = [s for s in sqs if s not in ws]
            for bs in itertools.combinations(rest, nb):
                p = pawns.Pos(frozenset(ws), frozenset(bs))
                if pawns.passed(b, p, "W") or pawns.passed(b, p, "B"):
                    continue
                out.add(p)
    return out

def key_to_pos(k):
    w, bl = k.split("/")
    f = lambda part: frozenset((L.index(t[0]), int(t[1:])) for t in part.split(":")[1].split())
    return pawns.Pos(f(w), f(bl))

total = 0
print("== 1. family re-enumeration with cylcgt.passed filter ==")
for bd, (files, wrap) in BOARDS.items():
    fam = my_family(files, wrap)
    keys = set(key_to_pos(k) for k in load(f"mine__{bd}__count__off__whole.json.gz")["outcomes"])
    ck = set(key_to_pos(k) for k in load(f"cylcgt__{bd}__count__noep.json.gz")["outcomes"])
    total += len(fam)
    print(bd, "mine-family", len(fam), "worker-keys", len(keys), "cylcgt-keys", len(ck), "sets equal:", fam == keys == ck)
print("total", total)

print("\n== 2. crosscheck.minimax (Codex) outcome_class vs X=0 column, count rule ==")
for bd, (files, wrap) in BOARDS.items():
    for ep in (False, True):
        mb = mm.Board(files, 8, wrap, ep)
        mine = load(f"mine__{bd}__count__{'plain' if ep else 'off'}__whole.json.gz")["outcomes"]
        cy = load(f"cylcgt__{bd}__count__{'ep' if ep else 'noep'}.json.gz")["outcomes"]
        dm = dc = 0
        cls = Counter()
        for k in mine:
            o = mm.outcome_class(mb, mm.parse_position(k))
            cls[o] += 1
            dm += o != mine[k][0]; dc += o != cy[k][0]
        print(bd, "ep" if ep else "noep", "n", len(mine), "crosscheck!=worker", dm, "crosscheck!=cylcgt", dc, dict(cls))

print("\n== 3. sensitivity of the C1 comparison ==")
for bd in BOARDS:
    for ep in (False, True):
        e = "ep" if ep else "noep"
        cyr = {r: load(f"cylcgt__{bd}__{r}__{e}.json.gz")["outcomes"] for r in ("count", "mover", "opponent")}
        vecs = Counter(cyr["count"].values())
        const = sum(1 for v in cyr["count"].values() if len(set(v)) == 1)
        cross = {f"{a}/{b}": sum(1 for k in cyr[a] if cyr[a][k] != cyr[b][k]) for a, b in
                 [("count", "mover"), ("count", "opponent"), ("mover", "opponent")]}
        print(bd, e, "distinct vectors(count)", len(vecs), "constant vectors", const, "of", len(cyr["count"]),
              "cross-rule differing positions", cross)
    for r in ("count", "mover", "opponent"):
        a = load(f"cylcgt__{bd}__{r}__ep.json.gz")["outcomes"]; b = load(f"cylcgt__{bd}__{r}__noep.json.gz")["outcomes"]
        print("   ", bd, r, "e.p. on vs off differing positions (cylcgt):", sum(1 for k in a if a[k] != b[k]))
