#!/usr/bin/env python3
"""Run my instrumented build (sf_instr = patched sf_19, no ABL flag, + stderr logging) on every suite
position with `go depth D`, one process per position. Logs:
  INSTR NMP  -> Step-10 null-move block entered (full condition incl. non_pawn_material(us) true)
  INSTR NPM  -> a non-root main-search move-loop node whose side to move has non-pawn material
  INSTR S15  -> Step-15 block entered
Prints per kind the earliest iteration (rootDepth) per position, and writes instr_d<D>.json.
Usage: instr_runner.py DEPTH [id ...]"""
import json, subprocess, sys
from collections import Counter
from pathlib import Path
H = Path(__file__).resolve().parent
ROOT = H.parents[2]
D = int(sys.argv[1]); only = set(sys.argv[2:])
items = []
for f in ["cgt_verified.epd", "cgt_disagree.epd"]:
    for line in open(ROOT / "engine" / "suite" / f):
        if line.strip():
            pid = line.split('id "')[1].split('"')[0]
            if not only or pid in only:
                items.append((pid, " ".join(line.split()[:4])))
out = {}
for pid, fen4 in items:
    cmds = f"uci\nsetoption name Threads value 1\nsetoption name Hash value 64\nisready\nucinewgame\nisready\nposition fen {fen4} 0 1\ngo depth {D}\n"
    errf = open(H / "instr_stderr.tmp", "w")   # a file, not a pipe: avoids the stderr-pipe deadlock
    p = subprocess.Popen([str(H / "sf" / "bin" / "sf_instr")], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=errf, text=True)
    p.stdin.write(cmds); p.stdin.flush()
    so = []
    for l in p.stdout:
        so.append(l.rstrip("\n"))
        if l.startswith("bestmove"):
            break
    p.stdin.write("quit\n"); p.stdin.flush()
    p.communicate(); errf.close()
    se = (H / "instr_stderr.tmp").read_text()
    ev = [l.split() for l in se.splitlines() if l.startswith("INSTR")]
    rec = {"fen": fen4, "nodes_last": [l for l in so if l.startswith("info depth")][-1].split("nodes")[1].split()[0]}
    for kind in ("NMP", "NPM", "S15"):
        rds = [int(e[e.index("rootDepth") + 1]) for e in ev if e[1] == kind]
        rec[kind + "_min_iter"] = min(rds) if rds else None
        rec[kind + "_count"] = len(rds)
    rec["first_events"] = [" ".join(e) for e in ev[:12]]
    out[pid] = rec
(H / f"instr_d{D}.json").write_text(json.dumps(out, indent=1))
for kind in ("NMP", "NPM", "S15"):
    c = Counter(r[kind + "_min_iter"] for r in out.values())
    print(kind, "earliest iteration per position:", dict(sorted(((str(k), n) for k, n in c.items()))))
