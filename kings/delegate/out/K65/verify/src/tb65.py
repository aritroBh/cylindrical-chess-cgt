"""K65 referee: Lichess (Syzygy) tablebase for the exact over groups of K65 with at most seven men (F1-F4 excluded:
K63's referee settled them).  For each group: both roots and both q's, each side to move (8 positions), through
realchess.probe.Prober only (cap 150, own ledger and cache).  Roots and q's are read from the referee's own ax65 logs
(logs/g/<group>.out).  The API move list must equal realchess.movegen's legal moves.
Question: is the group an exact over group in chess, i.e. Definition 4.8 read with chess values: at both roots every
non-shuttle Black move loses (no Black move but the shuttle avoids loss; the shuttle may lose too, as it does in P), the
freeze is White's only non-losing move, and both q's are mutual zugzwangs (the side to move loses, either side)?
Run from the repository root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python kings/delegate/out/K65/verify/src/tb65.py
"""
import json, os, re, sys, time
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../../.."))  # repository root
sys.path.insert(0, os.getcwd())
from realchess.probe import Prober, categories
from realchess import movegen as mg

V = "kings/delegate/out/K65/verify"
PR = Prober(cap=150, ledger=f"{V}/tb_ledger.jsonl", cache_dir=f"{V}/tbcache", tag="K65ref")
F1F4 = {"C125_03": "F2", "C145_12": "F1", "C125_06": "F3", "C125_07": "F4"}

def fen_of(pieces, stm, ep="-"):
    b = [["."] * 8 for _ in range(8)]
    for p in pieces.split():
        f, r = "abcdefgh".index(p[1]), int(p[2]) - 1
        assert b[r][f] == "."; b[r][f] = p[0]
    rows = []
    for r in range(7, -1, -1):
        s, n = "", 0
        for c in b[r]:
            if c == ".": n += 1
            else:
                if n: s += str(n); n = 0
                s += c
        rows.append(s + (str(n) if n else ""))
    return "/".join(rows) + f" {stm} - {ep} 0 1"

def lose_after(cat):   # category after a move is the opponent's: the MOVER loses iff the opponent wins
    return cat in ("win", "maybe-win")
GROUPS = [l.strip().split("|") for l in open(f"{V}/src/groups38.txt")]
out, res = [], []
for nm, pcs, z0, z1 in GROUPS:
    if len(pcs.split()) > 7 or nm in F1F4: continue
    log = open(f"{V}/logs/g/{nm}.out").read()
    toks = pcs.split()
    root = {z: " ".join(t if t[0] != "k" else "k" + z for t in toks) for z in (z0, z1)}
    frz = dict()
    for m in re.finditer(r"freeze P(\w\d)(\w\d) at (\w\d) -> q = (.*?) [bw] ", log):
        a, b, z, q = m.groups(); frz[z] = (a + b, q, (a[0] + "3") if (a[1] == "2" and b[1] == "4") else "-")
    assert set(frz) == {z0, z1}, (nm, frz)
    verdict, lines = True, []
    for lab, z in (("root " + z0, z0), ("root " + z1, z1)):
        for stm in "wb":
            fen = fen_of(root[z], stm); pos = mg.parse_fen(fen); assert not mg.validity_errors(pos), fen
            rec = PR.probe(fen); cat, mv = categories(rec)
            assert sorted(mv) == sorted(m.uci() for m in mg.legal_moves(pos)), fen
            nonlose = sorted(u for u, c in mv.items() if not lose_after(c))
            want = [(z0 + z1) if z == z0 else (z1 + z0)] if stm == "b" else [frz[z][0]]
            # (O1): every non-shuttle Black move loses (the shuttle itself may lose: it does in P);
            # (O2): the freeze is White's only non-losing move (in P every other White move loses at once)
            ok = set(nonlose) <= set(want) if stm == "b" else nonlose == want
            verdict &= ok
            lines.append(f"  {lab:8s} {'White' if stm == 'w' else 'Black'} to move: {cat:12s} non-losing moves {nonlose}  (Def 4.8 allows {want}) {'ok' if ok else 'NO'}")
            res.append({"group": nm, "pos": lab, "stm": stm, "fen": fen, "category": cat, "moves": mv, "fetched": rec["fetched"]})
    for z in (z0, z1):
        fr, q, ep = frz[z]; qp = " ".join(q.split())
        for stm in "wb":
            fen = fen_of(qp, stm, ep if stm == "b" else "-"); pos = mg.parse_fen(fen); assert not mg.validity_errors(pos), fen
            rec = PR.probe(fen); cat, mv = categories(rec)
            assert sorted(mv) == sorted(m.uci() for m in mg.legal_moves(pos)), fen
            ok = cat in ("loss", "maybe-loss")
            verdict &= ok
            lines.append(f"  q after {fr} at {z} {'White' if stm == 'w' else 'Black'} to move: {cat:12s} {'ok' if ok else 'NO (not a loss for the side to move)'}   {fen}")
            res.append({"group": nm, "pos": "q " + z, "stm": stm, "fen": fen, "category": cat, "moves": mv, "fetched": rec["fetched"]})
    out.append(f"{nm} {pcs} /{z1}: exact over group in chess: {'YES' if verdict else 'no'}")
    out += lines
print("\n".join(out))
json.dump(res, open(f"{V}/logs/tb/tb_results.json", "w"), indent=1)
print(f"requests in ledger: {PR.ledger_count()}  cache hits this run: {PR.hits}")
