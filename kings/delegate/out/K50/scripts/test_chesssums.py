"""K50 test (a): the ChessSums positions of the engine test (engine/runs/chesssums/), split as in
research/engine_baselines/embedding_flaw.py (SHARED / ADJACENT / APART by the declared freeze group).
Each position is checked twice: with --group (the declared group wk, bk, wp, bp) and with the default F_Z.
Run from the project root: python3 kings/delegate/out/K50/scripts/test_chesssums.py [n_shared_sample]"""
import json
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.getcwd())
from kings.embed_check import Board, Checker  # noqa: E402

D = "engine/runs/chesssums/"
meta = {m["id"]: m for m in json.load(open(D + "meta.json"))}
ids = json.load(open(D + "subset_ids.json"))


def klass(m):
    fz = m["freeze"]
    g = {ord(fz[x][0]) - 97 for x in ("wk", "bk", "wp", "bp")}
    gsq = {fz[x] for x in ("wk", "bk", "wp", "bp")}
    cf = set()
    for i, row in enumerate(m["fen"].split()[0].split("/")):
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                if ch in "Pp" and f"{'abcdefgh'[f]}{8 - i}" not in gsq:
                    cf.add(f)
                f += 1
    if cf & g:
        return "SHARED"
    if any(abs(a - c) == 1 for a in cf for c in g):
        return "ADJACENT"
    return "APART"


def main():
    nshared = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    sel = {"SHARED": [], "ADJACENT": [], "APART": []}
    for i in ids:
        sel[klass(meta[i])].append(i)
    print({k: len(v) for k, v in sel.items()})
    random.seed(50)
    run = sel["APART"] + sel["ADJACENT"] + random.sample(sel["SHARED"], nshared)
    tally = Counter()
    for i in run:
        m = meta[i]
        fz = m["freeze"]
        grp = f"K{fz['wk']},P{fz['wp']},k{fz['bk']},p{fz['bp']}"
        cls = klass(m)
        for mode in ("group", "default"):
            t0 = time.process_time()
            r = Checker(Board(8, 8, False), 8, 300000, False, 20).run(m["fen"], None, grp if mode == "group" else None)
            dt = time.process_time() - t0
            sep = r["separation"]["verdict"]
            row = {"id": i, "class": cls, "mode": mode, "sep": sep, "verdict": r["verdict"],
                   "V1": r["V1"]["verdict"], "V2": r["V2"]["verdict"], "V3": r["V3"]["verdict"],
                   "E": r["V1"].get("E", {}).get("verdict"), "files_left": r["separation"].get("files_left_for_components"),
                   "witness": r["separation"].get("witness"), "D": r.get("D_result"), "outcome": m["outcome"],
                   "cpu_s": round(dt, 2)}
            print(json.dumps(row), flush=True)
            tally[(cls, mode, "sep=" + sep, r["verdict"], "V1=" + row["V1"], "V2=" + row["V2"], "V3=" + row["V3"])] += 1
    print("TALLY")
    for k, v in sorted(tally.items()):
        print(v, *k)


if __name__ == "__main__":
    main()
