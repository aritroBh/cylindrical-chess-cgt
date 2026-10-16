"""Black-to-move twins of the verified 'nimber' positions (value * under count).

A nimber * is an N-position: the side to move wins, whoever it is. The suite only
checked White to move. The Black-to-move twin (same men, same trebuchet) discriminates
* (Black to move wins) from a positive value such as 1 (Black to move loses), which is
what the 'mover' race rule gives for 4 of these components.

Reads every existing tablebase cache in the project offline first; only then fetches
through realchess/probe.py into THIS directory (cap 40 HTTP attempts, 5 s spacing).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C4-theory/twin_probe.py [--offline]
"""
import collections, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "engine", "suite"))
import build_suite as BS  # noqa
import cgtpos as C  # noqa
from cylcgt import cgt, pawns  # noqa
from realchess import probe as P, movegen as MG  # noqa

P.MIN_INTERVAL = 5.0
offline = "--offline" in sys.argv
caches = [d for d in glob.glob(os.path.join(ROOT, "**", "*cache*"), recursive=True)
          if os.path.isdir(d) and "pycache" not in d and ".pytest" not in d and ".venv" not in d
          and os.path.abspath(d) != os.path.join(HERE, "tbcache")]
readers = [P.Prober(0, ledger=os.path.join(HERE, "ro_ledger.jsonl"), cache_dir=d, offline=True) for d in caches]
own = P.Prober(40, ledger=os.path.join(HERE, "tb_ledger.jsonl"), cache_dir=os.path.join(HERE, "tbcache"),
               tag="C4-theory", offline=offline, verbose=True)

def lookup(fen):
    for r in readers + [own]:
        rec = r.cached(fen)
        if rec is not None:
            return rec, "cache:" + os.path.relpath(r.cache_dir, ROOT)
    if offline:
        return None, "not cached"
    return own.probe(fen), "fetched"

rows = json.load(open(BS.RESULTS))
cands = {(r["pos"], r["stm"]): r for r in json.load(open(BS.CANDS))}
ver = [r for r in rows if r["tb_root"] in BS.WINS and r["rules"]["count"]["win_set_agree"]]
targets = [r for r in ver if r["features"]["class"] == "nimber"]
out = []
for r in targets:
    parts = r["fen"].split()
    tstm = "W" if r["stm"] == "B" else "B"
    twin = " ".join([parts[0], tstm.lower(), "-", "-", "0", "1"])
    p = MG.parse_fen(twin)
    errs = MG.validity_errors(p)
    pos = BS.rec_pos(cands[(r["component"], "W")])
    pred = {}
    for rule in C.RULES:
        C.set_rule(rule)
        v = pawns.value(C.B4, pos)
        tw = (not cgt.le(cgt.ZERO, v)) if tstm == "B" else (not cgt.le(v, cgt.ZERO))
        pred[rule] = {"value": cgt.show(v), "twin_mover_wins": tw}
    if errs:
        out.append({"id": r["id"], "twin": twin, "errors": errs}); continue
    rec, src = lookup(twin)
    cat = None; mv = {}
    if rec and rec.get("status") == 200:
        cat = rec["data"]["category"]
        mv = {m["san"]: m["category"] for m in rec["data"]["moves"]}
    out.append({"id": r["id"], "component": r["component"], "treb": r["treb"], "twin": twin, "twin_stm": tstm,
                "pred": pred, "tb_root_twin": cat, "tb_moves_after": mv, "source": src})
    print(r["id"], r["component"], r["treb"], twin, "| model:",
          {k: (v["value"], tstm + (" wins" if v["twin_mover_wins"] else " loses")) for k, v in pred.items()},
          "| TB twin (mover):", cat, src, flush=True)
json.dump(out, open(os.path.join(HERE, "twin_results.json"), "w"), indent=1)
agree = collections.Counter()
for o in out:
    if o.get("tb_root_twin") is None:
        continue
    tbw = o["tb_root_twin"] in ("win", "cursed-win")
    for rule in C.RULES:
        agree[rule] += (tbw == o["pred"][rule]["twin_mover_wins"])
print("twins resolved:", sum(o.get("tb_root_twin") is not None for o in out), "of", len(out))
print("model agrees with TB on twin (other side to move) outcome:", dict(agree))
print("TB root categories:", collections.Counter(o.get("tb_root_twin") for o in out))
print("HTTP attempts in own ledger:", own.ledger_count())
