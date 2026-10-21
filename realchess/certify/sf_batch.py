"""Run sf_eval.evaluate on every FEN of a file (one per line). Engine evidence only.
    PYTHONPATH=. .venv/bin/python -m realchess.certify.sf_batch <fens.txt> <out.json> [movetime_ms] [multipv]"""
import json
import sys

from .sf_eval import evaluate

fens = [l.strip() for l in open(sys.argv[1]) if l.strip()]
mt = int(sys.argv[3]) if len(sys.argv) > 3 else 60000
mpv = int(sys.argv[4]) if len(sys.argv) > 4 else 1
res = evaluate(fens, movetime=mt, multipv=mpv)
res["settings"] = {"movetime_ms": mt, "multipv": mpv, "threads": 1, "hash_mb": 64, "tablebases": "none"}
json.dump(res, open(sys.argv[2], "w"), indent=1)
for r in res["results"]:
    print(r["fen"], r["bestmove"], [(l["score"], l["depth"], l["pv"][:40]) for l in r["lines"]])
