"""Put exact kpsolve results for the decisive terminals into the sandwich and see what is left.

Starts from the min_support end state (every non-needed terminal at its resolved-only value,
the needed ones at the model assignment), then replaces each needed terminal side by the kpsolve
result where kpsolve is exact (A == B) and frees it otherwise. The kpsolve rows are an overlay;
realdb.jsonl is not touched (the runs used --promote Q, so they are not full-chess certificates).

    PYTHONPATH=. .venv/bin/python realchess/targets18/apply_kpsolve.py \
        realchess/targets18/min_support_after2.json realchess/targets18/kp_eighth_*.out
"""
import json
import sys

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess.certify import termdb
from realchess.certify.oracle10 import raw_from_db, side_fens
from realchess.oracle_value import TREATMENTS, Terminals, sandwich



def tokens(fen):
    """kpsolve input tokens of a FEN (same as to_kpsolve.tokens)."""
    board, stm, _castle, ep = fen.split()[:4]
    out = []
    for i, row in enumerate(board.split("/")):
        rank, f = 8 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
                continue
            out.append(f"{ch}{'abcdefgh'[f]}{rank}")
            f += 1
    return " ".join(out) + f" {stm} {ep}"


WDL = {"W": 1, "D": 0, "L": -1}

d = json.load(open(sys.argv[1]))
kp = {}
for path in sys.argv[2:]:
    for line in open(path):
        if line.startswith("#") or "|" not in line:
            continue
        pos, res = line.split("|")[:2]
        a_b = res.split()
        kp[pos.strip()] = (WDL.get(a_b[0]), WDL.get(a_b[1]))

T = Terminals(Pos.parse(d["component"]))
byname = {str(t): t for t in T.terms}
kind, dr = TREATMENTS[d["treatment"]]
db = termdb.load()
raw_none, _ = raw_from_db(T, db, "none", None)
raw_model, _ = raw_from_db(T, db, "model", d["race_rule_for_fill"])
needed = [byname[x["terminal"]] for x in d["needed_terminals"]]


def show(raw, label):
    lo, hi = sandwich(T, raw, kind, dr)
    pinned = lo is hi
    print(f"{label}: {cgt.show(lo)} .. {cgt.show(hi)}{'  (pinned)' if pinned else ''}")
    return lo, hi


base = dict(raw_none)
for t in needed:
    base[t] = raw_model[t]
show(base, "needed terminals at model assignment")
show(raw_none, "needed terminals free")

applied = dict(base)
report = []
for t in needed:
    f = side_fens(T, t)
    sides = []
    for s in "WB":
        r = kp.get(tokens(f[s]))
        exact = r is not None and r[0] == r[1]
        sides.append(r[0] if exact else None)
        report.append({"terminal": str(t), "side_to_move": s, "kpsolve": r, "exact": exact,
                       "model": raw_model[t]["WB".index(s)]})
    applied[t] = tuple(sides)
for r in report:
    print(" ", r)
lo, hi = show(applied, "exact kpsolve sides fixed, the rest free")

# each still-open side alone: the other open sides at the model assignment, this one at W/D/L
for t in needed:
    for i, v in enumerate(applied[t]):
        if v is not None:
            continue
        for val in (1, 0, -1):
            trial = dict(applied)
            for u in needed:
                trial[u] = tuple(raw_model[u][j] if trial[u][j] is None else trial[u][j] for j in range(2))
            trial[t] = tuple(val if j == i else trial[t][j] for j in range(2))
            show(trial, f"  only open side {t}, {'WB'[i]} to move = {val:+d}")
