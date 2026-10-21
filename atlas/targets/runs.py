#!/usr/bin/env python3
"""Build pcgt inputs (positions x boards x settings) and run pcgt.

Settings: race in {count, mover, opponent, white, black} x
          e.p. variant in {on+textbook (1,0), on+aware (1,1), off (0,0)}.
("white"/"black": every race is won by that side; a value that is the same under
both holds for every assignment of race results, by monotonicity.)

Scopes:
  db      the 231,071 records of atlas/flat8/rerun/values.jsonl (flat widths 1-4,
          <= 6 pawns), on the flat board AND on the cylinder of the same width
  w5      flat width 5, every file occupied, 5-6 pawns (80,163 positions; pcgt --enum)
  n7      flat widths 2-4, 7 pawns (files a and last occupied; pcgt --enum)
  w5n7    flat width 5, every file occupied, 7 pawns

Usage (from the project root):
  .venv/bin/python atlas/targets/runs.py SCOPE [--settings all|core] [--boards flat,cyl]
Writes atlas/targets/work/run_SCOPE.tsv (+ .log with pcgt's stderr and timing).
"""
from __future__ import annotations

import argparse
import json
import os
import resource
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.join(HERE, "work")
PCGT = os.path.join(HERE, "pcgt")

RACES = ["count", "mover", "opponent", "white", "black"]
EPV = [(1, 0), (1, 1), (0, 0)]
ALL_SETTINGS = [(r, ep, aw) for r in RACES for (ep, aw) in EPV]
CORE_SETTINGS = [(r, ep, aw) for r in ("count", "mover", "opponent") for (ep, aw) in EPV]


def db_positions():
    out = []
    with open(os.path.join(ROOT, "atlas", "flat8", "rerun", "values.jsonl")) as fh:
        for line in fh:
            r = json.loads(line)
            out.append((r["position"], r["width"]))
    return out


def enum_positions(w, nmin, nmax, conn):
    res = subprocess.run([PCGT, "--enum", str(w), "0", str(nmin), str(nmax), str(conn)],
                         capture_output=True, text=True, check=True)
    out = []
    for line in res.stdout.splitlines():
        p = line.split("\t")
        out.append((p[0], int(p[1])))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scope", choices=["db", "w5", "n7", "w5n7"])
    ap.add_argument("--settings", default="all", choices=["all", "core"])
    ap.add_argument("--boards", default=None)
    ap.add_argument("--split", type=int, default=0,
                    help="run one pcgt process per (board, setting), N at a time, then merge by structural hash")
    a = ap.parse_args()
    if a.scope == "db":
        pos = db_positions()
        boards = a.boards or "flat,cyl"
    elif a.scope == "w5":
        pos = enum_positions(5, 5, 6, 1)
        boards = a.boards or "flat,cyl"
    elif a.scope == "n7":
        pos = []
        for w in (2, 3, 4):
            pos += enum_positions(w, 7, 7, 0)
        boards = a.boards or "flat"
    else:
        pos = enum_positions(5, 7, 7, 1)
        boards = a.boards or "flat"
    settings = ALL_SETTINGS if a.settings == "all" else CORE_SETTINGS
    wraps = [0 if b == "flat" else 1 for b in boards.split(",")]
    pos.sort(key=lambda t: t[1])
    if a.split:
        return run_split(a, pos, wraps, settings)
    inp = os.path.join(WORK, f"in_{a.scope}.tsv")
    with open(inp, "w") as fh:
        for wrap in wraps:
            for (race, ep, aw) in settings:
                for p, w in pos:
                    fh.write(f"{p}\t{w}\t{wrap}\t{race}\t{ep}\t{aw}\n")
    out = os.path.join(WORK, f"run_{a.scope}.tsv")
    log = os.path.join(WORK, f"run_{a.scope}.log")
    t0 = time.time()
    with open(inp) as fi, open(out, "w") as fo, open(log, "w") as fl:
        rc = subprocess.run([PCGT], stdin=fi, stdout=fo, stderr=fl).returncode
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    with open(log, "a") as fl:
        fl.write(json.dumps({"scope": a.scope, "positions": len(pos), "boards": boards,
                             "settings": len(settings), "returncode": rc,
                             "wall_s": round(time.time() - t0, 1), "cpu_user_s": round(ru.ru_utime, 1),
                             "cpu_sys_s": round(ru.ru_stime, 1), "max_rss_bytes": ru.ru_maxrss}) + "\n")
    print(open(log).read())


def run_split(a, pos, wraps, settings):
    """One pcgt process per (board, setting), a.split at a time; merge into
    work/run_SCOPE.tsv with value ids renumbered by structural hash."""
    jobs = []
    for wrap in wraps:
        for (race, ep, aw) in settings:
            tag = f"{a.scope}_{wrap}_{race}_{ep}{aw}"
            inp = os.path.join(WORK, f"in_{tag}.tsv")
            with open(inp, "w") as fh:
                for p, w in pos:
                    fh.write(f"{p}\t{w}\t{wrap}\t{race}\t{ep}\t{aw}\n")
            jobs.append((tag, inp))
    t0 = time.time()
    running, done, logs = [], [], []
    queue = list(jobs)
    while queue or running:
        while queue and len(running) < a.split:
            tag, inp = queue.pop(0)
            fi = open(inp)
            fo = open(os.path.join(WORK, f"part_{tag}.tsv"), "w")
            fe = open(os.path.join(WORK, f"part_{tag}.log"), "w")
            pr = subprocess.Popen(["/usr/bin/time", "-l", PCGT], stdin=fi, stdout=fo, stderr=fe)
            running.append((tag, pr, fi, fo, fe, time.time()))
        time.sleep(2)
        for item in list(running):
            tag, pr, fi, fo, fe, ts = item
            if pr.poll() is not None:
                fi.close(); fo.close(); fe.close()
                running.remove(item)
                done.append(tag)
                logs.append({"tag": tag, "rc": pr.returncode, "wall_s": round(time.time() - ts, 1)})
                print(f"done {tag} rc={pr.returncode} {time.time() - ts:.0f}s", flush=True)
    # merge
    out = os.path.join(WORK, f"run_{a.scope}.tsv")
    hid, vinfo = {}, {}
    checks = {"within_part_hash_collisions": 0, "cross_part_key_conflicts": 0, "cross_part_key_agreements": 0}
    with open(out, "w") as fo:
        for tag, _ in jobs:
            path = os.path.join(WORK, f"part_{tag}.tsv")
            local = {}
            seen_here = {}
            with open(path) as fh:
                for line in fh:
                    if line.startswith("#V"):
                        q = line.rstrip("\n").split("\t")
                        h = q[3]
                        # within one process distinct gids are distinct values: hashes must differ
                        if h in seen_here and seen_here[h] != int(q[1]):
                            checks["within_part_hash_collisions"] += 1
                        seen_here[h] = int(q[1])
                        if h not in hid:
                            hid[h] = len(hid)
                            vinfo[h] = q
                        else:
                            if vinfo[h][5] != "-" and q[5] != "-":
                                if vinfo[h][5] == q[5]:
                                    checks["cross_part_key_agreements"] += 1
                                else:
                                    checks["cross_part_key_conflicts"] += 1
                            if vinfo[h][4] == "-" and q[4] != "-":
                                vinfo[h] = q
                        local[int(q[1])] = hid[h]
            with open(path) as fh:
                for line in fh:
                    if line.startswith("#V"):
                        continue
                    q = line.rstrip("\n").split("\t")
                    if q[6] != "-1":
                        q[6] = str(local[int(q[6])])
                    fo.write("\t".join(q) + "\n")
        for h, q in vinfo.items():
            fo.write("\t".join(["#V", str(hid[h])] + q[2:]) + "\n")
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    log = os.path.join(WORK, f"run_{a.scope}.log")
    maxrss = []
    for tag, _ in jobs:
        txt = open(os.path.join(WORK, f"part_{tag}.log")).read()
        for line in txt.splitlines():
            if "maximum resident set size" in line:
                maxrss.append(int(line.split()[0]))
    with open(log, "w") as fl:
        fl.write(json.dumps({"scope": a.scope, "positions": len(pos), "boards": a.boards, "jobs": len(jobs),
                             "parallel": a.split, "wall_s": round(time.time() - t0, 1),
                             "cpu_user_s": round(ru.ru_utime, 1), "cpu_sys_s": round(ru.ru_stime, 1),
                             "max_rss_bytes_per_job_max": max(maxrss) if maxrss else None,
                             "distinct_values": len(hid), "merge_checks": checks, "jobs_log": logs}) + "\n")
    if checks["within_part_hash_collisions"] or checks["cross_part_key_conflicts"]:
        raise SystemExit(f"hash collision detected in merge: {checks}")
    print(open(log).read())


if __name__ == "__main__":
    main()
