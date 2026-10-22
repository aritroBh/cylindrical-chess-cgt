"""run the project's cylcgt over my own enumeration (dump file), compare with my value class"""
import sys, time
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, value
assert pawns.RACE_RULE == "count" and pawns.PASSED_RESPECTS_EP is True
n = int(sys.argv[1]); maxnp = int(sys.argv[2]); fn = sys.argv[3]
NAMES = {"0": "0", "1": "*", "2": "*2", "3": "*3"}
t0 = time.time(); cnt = {}; bad = 0; tot = 0
for line in open(fn):
    np_, k, s = line.rstrip("\n").split("\t"); np_ = int(np_)
    if np_ > maxnp: continue
    g = value(Board(n, 8, True, True), Pos.parse(s)); sh = cgt.show(g)
    mine = NAMES.get(k)           # None for 'x' (not 0,*,*2 among my heaps)
    ok = (sh == mine) if mine else (sh not in NAMES.values() or sh == "*3")
    tot += 1
    c = cnt.setdefault(np_, {}); c[sh if sh in ("0", "*", "*2", "*3") else "other"] = c.get(sh if sh in ("0", "*", "*2", "*3") else "other", 0) + 1
    if not ok:
        bad += 1; print("DISAGREE", np_, s, "mine", k, "cylcgt", sh, flush=True)
    if tot % 500 == 0: print("progress", tot, "%.0fs" % (time.time() - t0), flush=True)
print("TOTAL", tot, "disagree", bad, "%.0fs" % (time.time() - t0))
for np_ in sorted(cnt): print(np_, cnt[np_])
