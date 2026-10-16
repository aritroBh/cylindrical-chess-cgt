#!/usr/bin/env python3
"""Run any UCI engine on an EPD suite and score it (stdlib only; no engine is
installed by this project -- pass the binary you have).

Examples (from the project root):

    .venv/bin/python engine/run_suite.py --engine /path/to/stockfish \
        --epd engine/suite/cgt_verified.epd --movetime 1000
    .venv/bin/python engine/run_suite.py --engine /path/to/stockfish \
        --epd engine/suite/cgt_verified.epd --nodes 1000 10000 100000 --json out.json
    .venv/bin/python engine/run_suite.py --engine /path/to/lc0 --option Threads=1 --nodes 800 \
        --epd engine/suite/cgt_verified.epd
    # harness self-test with the bundled random-mover (not an engine):
    .venv/bin/python engine/run_suite.py --engine "python3 engine/mock_uci.py" \
        --epd engine/suite/cgt_verified.epd --movetime 10

Scoring: a position is solved if the engine's bestmove is in the solution set.
The solution set is the EPD `c2` opcode (UCI moves; written by build_suite.py),
or, when there is no c2, the SAN `bm` list converted to UCI with a small
king-and-pawn-only SAN parser (enough for this suite).

Per position it also records the last reported depth / nodes / score and the
"solution depth": the first depth from which every reported PV move was a
solution (useful for node-sweep and depth-sweep experiments).

IMPORTANT: do NOT give the engine Syzygy tablebases (SyzygyPath) unless you
want a sanity run: every position in this suite has <= 7 men, so a 7-man
tablebase solves it at the root.
"""
from __future__ import annotations

import argparse
import json
import queue
import shlex
import subprocess
import sys
import threading
import time

FILES = "abcdefgh"


# ------------------------------------------------------------------ EPD
def parse_epd(line: str):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = line.split(None, 4)
    fen4 = " ".join(parts[:4])
    ops = {}
    rest = parts[4] if len(parts) > 4 else ""
    i = 0
    while i < len(rest):
        while i < len(rest) and rest[i] in " ;":
            i += 1
        if i >= len(rest):
            break
        j = i
        while j < len(rest) and rest[j] not in " ;":
            j += 1
        op = rest[i:j]
        i = j
        args, cur, inq = [], "", False
        while i < len(rest):
            ch = rest[i]
            if inq:
                if ch == '"':
                    inq = False
                    args.append(cur)
                    cur = ""
                else:
                    cur += ch
            elif ch == '"':
                inq = True
            elif ch == ";":
                i += 1
                break
            elif ch == " ":
                if cur:
                    args.append(cur)
                    cur = ""
            else:
                cur += ch
            i += 1
        if cur:
            args.append(cur)
        ops[op] = args
    return fen4, ops


def board_from_fen(fen4: str):
    rows = fen4.split()[0].split("/")
    b = {}
    for i, row in enumerate(rows):
        r = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                b[(f, r)] = ch
                f += 1
    return b


def san_to_uci_kp(fen4: str, san: str) -> str:
    """SAN -> UCI for king-and-pawn positions only (no castling, pieces)."""
    b = board_from_fen(fen4)
    stm = fen4.split()[1]
    s = san.rstrip("+#!?")
    promo = ""
    if "=" in s:
        s, p = s.split("=")
        promo = p.lower()
    if s[0] == "K":
        to = (FILES.index(s[-2]), int(s[-1]))
        k = "K" if stm == "w" else "k"
        frm = next(sq for sq, p in b.items() if p == k)
    else:
        to = (FILES.index(s[-2]), int(s[-1]))
        d = 1 if stm == "w" else -1
        pawn = "P" if stm == "w" else "p"
        if "x" in s:
            frm = (FILES.index(s[0]), to[1] - d)
        elif b.get((to[0], to[1] - d)) == pawn:
            frm = (to[0], to[1] - d)
        else:
            frm = (to[0], to[1] - 2 * d)
        if b.get(frm) != pawn:
            raise ValueError(f"cannot parse SAN {san!r} in {fen4}")
    return f"{FILES[frm[0]]}{frm[1]}{FILES[to[0]]}{to[1]}{promo}"


def solutions(fen4, ops):
    if "c2" in ops and ops["c2"]:
        return set(" ".join(ops["c2"]).split())
    if "bm" in ops:
        return {san_to_uci_kp(fen4, m) for m in ops["bm"]}
    raise ValueError("EPD line has neither c2 nor bm")


# ------------------------------------------------------------------ UCI
class Engine:
    def __init__(self, cmd: str, options: dict, timeout: float = 30.0):
        argv = shlex.split(cmd)
        self.p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self.q: queue.Queue = queue.Queue()
        threading.Thread(target=self._reader, daemon=True).start()
        self.timeout = timeout
        self.name = cmd
        self.send("uci")
        for line in self.until("uciok"):
            if line.startswith("id name "):
                self.name = line[8:]
        for k, v in options.items():
            self.send(f"setoption name {k} value {v}")
        self.ready()

    def _reader(self):
        for line in self.p.stdout:
            self.q.put(line.rstrip("\n"))
        self.q.put(None)

    def send(self, s: str):
        self.p.stdin.write(s + "\n")
        self.p.stdin.flush()

    def until(self, prefix: str, timeout: float | None = None):
        deadline = time.time() + (timeout or self.timeout)
        while True:
            left = deadline - time.time()
            if left <= 0:
                raise TimeoutError(f"engine did not send {prefix!r}")
            try:
                line = self.q.get(timeout=left)
            except queue.Empty:
                continue
            if line is None:
                raise RuntimeError("engine exited")
            yield line
            if line.startswith(prefix):
                return

    def ready(self):
        self.send("isready")
        for _ in self.until("readyok"):
            pass

    def go(self, fen4: str, limit: str, budget_s: float):
        self.send("ucinewgame")
        self.ready()
        self.send(f"position fen {fen4} 0 1")
        self.send(f"go {limit}")
        infos, best = [], None
        for line in self.until("bestmove", timeout=budget_s):
            if line.startswith("info") and " pv " in line:
                infos.append(parse_info(line))
            if line.startswith("bestmove"):
                best = line.split()[1]
        return best, infos

    def quit(self):
        try:
            self.send("quit")
            self.p.wait(timeout=5)
        except Exception:
            self.p.kill()


def parse_info(line: str) -> dict:
    t = line.split()
    d = {}
    for key in ("depth", "seldepth", "nodes", "multipv", "time"):
        if key in t:
            try:
                d[key] = int(t[t.index(key) + 1])
            except (ValueError, IndexError):
                pass
    if "score" in t:
        i = t.index("score")
        d["score"] = f"{t[i+1]} {t[i+2]}"
    if "pv" in t:
        d["pv"] = t[t.index("pv") + 1:]
    return d


def solution_depth(infos, sol):
    """First depth from which every PV head (multipv 1) is a solution."""
    heads = [(i.get("depth"), i["pv"][0]) for i in infos if i.get("multipv", 1) == 1 and i.get("pv")]
    first = None
    for depth, mv in heads:
        if mv in sol:
            if first is None:
                first = depth
        else:
            first = None
    return first


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engine", required=True, help="engine command line (quoted if it has arguments)")
    ap.add_argument("--epd", nargs="+", required=True)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--movetime", type=int, nargs="+", help="milliseconds per position (sweep allowed)")
    g.add_argument("--nodes", type=int, nargs="+", help="node limit(s) (sweep allowed)")
    g.add_argument("--depth", type=int, nargs="+", help="depth limit(s) (sweep allowed)")
    ap.add_argument("--option", action="append", default=[], help="UCI option NAME=VALUE (repeatable)")
    ap.add_argument("--timeout", type=float, default=120.0, help="seconds before a search is abandoned")
    ap.add_argument("--json", help="write per-position results here")
    ap.add_argument("--filter", help="only ids containing this substring")
    a = ap.parse_args()

    opts = dict(o.split("=", 1) for o in a.option)
    if any(k.lower() == "syzygypath" for k in opts):
        print("warning: SyzygyPath given; <=7-man positions are solved by the tablebase at the root",
              file=sys.stderr)
    if a.nodes:
        limits = [f"nodes {n}" for n in a.nodes]
    elif a.depth:
        limits = [f"depth {d}" for d in a.depth]
    else:
        limits = [f"movetime {m}" for m in (a.movetime or [1000])]

    items = []
    for path in a.epd:
        for line in open(path, encoding="utf-8"):
            e = parse_epd(line)
            if e is None:
                continue
            fen4, ops = e
            pid = ops.get("id", [f"{path}:{len(items)+1}"])[0]
            if a.filter and a.filter not in pid:
                continue
            items.append((pid, fen4, ops, solutions(fen4, ops)))

    eng = Engine(a.engine, opts, timeout=a.timeout)
    print(f"engine: {eng.name}; {len(items)} positions; limits: {', '.join(limits)}")
    results = []
    for limit in limits:
        solved = 0
        for pid, fen4, ops, sol in items:
            t0 = time.time()
            try:
                best, infos = eng.go(fen4, limit, a.timeout)
                err = None
            except (TimeoutError, RuntimeError) as ex:
                best, infos, err = None, [], str(ex)
                eng.quit()
                eng = Engine(a.engine, opts, timeout=a.timeout)
            ok = best in sol
            solved += ok
            last = infos[-1] if infos else {}
            res = {"id": pid, "limit": limit, "fen": fen4, "best": best, "solved": ok,
                   "solutions": sorted(sol), "depth": last.get("depth"), "nodes": last.get("nodes"),
                   "score": last.get("score"), "solution_depth": solution_depth(infos, sol),
                   "seconds": round(time.time() - t0, 3), "error": err,
                   "tier": next((x for x in " ".join(ops.get("c3", [])).split(";") if "tier" in x), "").strip()}
            results.append(res)
            print(f"{pid:10s} {limit:16s} best={best!s:6s} {'OK ' if ok else 'XX '} "
                  f"sol={','.join(sorted(sol))} depth={res['depth']} score={res['score']}", flush=True)
        print(f"== {limit}: solved {solved}/{len(items)}")
    eng.quit()
    if a.json:
        with open(a.json, "w") as fh:
            json.dump({"engine": eng.name, "limits": limits, "results": results}, fh, indent=1)


if __name__ == "__main__":
    main()
