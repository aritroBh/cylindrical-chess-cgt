"""C4 refute check: re-solve ChessSums rows on the WHOLE BOARD with an independent solver.

Independent of cylcgt, bench/ and crosscheck/: imports only the stdlib. Reads the dataset
JSONL files as data.

  mode moves : for every root move of each side, does the mover win (real-chess whole-board
               play, e.p.-aware passed test, real e.p. right that expires after one ply)?
               Compared with row["winning_moves"], row["legal_moves"] and row["outcome"].
  mode value : is (whole-board pawn game) + (-gold) a second-player win?  That holds iff the
               whole-board game equals the stored value (gold parsed by our own parser below).

Usage (from the project root):
  python3 verify/bench/C4-refute/driver.py moves val [--rule count] [--aware 1] [--ep 1] [--jobs 6]
  python3 verify/bench/C4-refute/driver.py value val ...
Splits: val, test, test_heldout, train3000 (= the E2 train sample: random.Random(5).sample(train, 3000)).
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "bench", "data")
FILES = "abcdefghijklmnopqrstuvwxyz"
RULES = {"count": 0, "mover": 1, "opponent": 2}


# --------------------------------------------------------------------------- games (explicit DAG)
class G:
    def __init__(self):
        self.nodes = []      # id -> (L tuple, R tuple)
        self.index = {}
        self._add, self._neg, self._num, self._star = {}, {}, {}, {}
        self.zero = self.mk((), ())

    def mk(self, L, R):
        key = (tuple(sorted(set(L))), tuple(sorted(set(R))))
        i = self.index.get(key)
        if i is None:
            i = len(self.nodes)
            self.nodes.append(key)
            self.index[key] = i
        return i

    def num(self, x: Fraction):
        x = Fraction(x)
        if x in self._num:
            return self._num[x]
        if x == 0:
            g = self.zero
        elif x.denominator == 1:
            g = self.mk((self.num(x - 1),), ()) if x > 0 else self.mk((), (self.num(x + 1),))
        else:
            d = x.denominator
            assert d & (d - 1) == 0, x
            e = Fraction(1, d)
            g = self.mk((self.num(x - e),), (self.num(x + e),))
        self._num[x] = g
        return g

    def star(self, m):
        if m not in self._star:
            opts = tuple(self.star(i) for i in range(m))
            self._star[m] = self.mk(opts, opts)
        return self._star[m]

    def add(self, a, b):
        if a == self.zero:
            return b
        if b == self.zero:
            return a
        key = (a, b) if a <= b else (b, a)
        if key in self._add:
            return self._add[key]
        (aL, aR), (bL, bR) = self.nodes[a], self.nodes[b]
        L = [self.add(x, b) for x in aL] + [self.add(a, y) for y in bL]
        R = [self.add(x, b) for x in aR] + [self.add(a, y) for y in bR]
        g = self.mk(L, R)
        self._add[key] = g
        return g

    def neg(self, a):
        if a in self._neg:
            return self._neg[a]
        L, R = self.nodes[a]
        g = self.mk([self.neg(y) for y in R], [self.neg(x) for x in L])
        self._neg[a] = g
        return g

    def export(self, root):
        """BFS-renumber the sub-DAG under root (root -> 0); returns list of (L, R)."""
        order, ix = [root], {root: 0}
        i = 0
        while i < len(order):
            L, R = self.nodes[order[i]]
            for c in L + R:
                if c not in ix:
                    ix[c] = len(order)
                    order.append(c)
            i += 1
        return [(tuple(ix[c] for c in self.nodes[n][0]), tuple(ix[c] for c in self.nodes[n][1])) for n in order]


TOK = re.compile(r"\s*(\+-|\d+(?:/\d+)?|\*\d*|\^|v|[{}|,\-])")


def tokens(s):
    out, pos = [], 0
    s = s.strip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m:
            raise ValueError(f"bad char at {pos} in {s!r}")
        out.append(m.group(1))
        pos = m.end()
        while pos < len(s) and s[pos] == " ":
            pos += 1
    return out


def parse_value(gm: G, s: str):
    t = tokens(s)
    i = 0

    def peek():
        return t[i] if i < len(t) else None

    def game():
        nonlocal i
        if peek() == "{":
            i += 1
            L = []
            while peek() != "|":
                L.append(game())
                if peek() == ",":
                    i += 1
            i += 1
            R = []
            while peek() != "}":
                R.append(game())
                if peek() == ",":
                    i += 1
            i += 1
            return gm.mk(L, R)
        # term: [-]num? (^|v)* (*n)? (+- num)?
        x = Fraction(0)
        sign = 1
        if peek() == "-":
            i += 1
            sign = -1
        if peek() is not None and peek()[0].isdigit():
            x = sign * Fraction(peek())
            i += 1
        else:
            assert sign == 1, s
        u, m = 0, 0
        while peek() in ("^", "v"):
            u += 1 if peek() == "^" else -1
            i += 1
        if peek() is not None and peek().startswith("*"):
            m = int(peek()[1:] or 1)
            i += 1
        if peek() == "+-":
            i += 1
            y = Fraction(peek())
            i += 1
            assert u == 0 and m == 0 and y > 0, s
            return gm.mk((gm.num(x + y),), (gm.num(x - y),))   # x + (+-y) = {x+y | x-y}
        g = gm.num(x)
        step = gm.mk((gm.zero,), (gm.star(1),)) if u > 0 else gm.mk((gm.star(1),), (gm.zero,))
        for _ in range(abs(u)):
            g = gm.add(g, step)
        if m:
            g = gm.add(g, gm.star(m))
        return g

    g = game()
    assert i == len(t), (s, i, t)
    return g


# --------------------------------------------------------------------------- rows and jobs
def sq(name):
    return FILES.index(name[0]), int(name[1:])


def load(split):
    if split == "train3000":
        rows = [json.loads(x) for x in open(os.path.join(DATA, "train.jsonl"))]
        return random.Random(5).sample(rows, 3000)
    return [json.loads(x) for x in open(os.path.join(DATA, f"{split}.jsonl"))]


def job_line(jid, row, rule, aware, ep, cap, stop, H):
    w = [sq(s) for s in row["white"]]
    b = [sq(s) for s in row["black"]]
    parts = [jid, row["board"]["files"], int(row["board"]["cylinder"]), RULES[rule], aware, ep, cap, stop, len(w)]
    for f, r in w:
        parts += [f, r]
    parts.append(len(b))
    for f, r in b:
        parts += [f, r]
    parts.append(len(H))
    for L, R in H:
        parts += [len(L), *L, len(R), *R]
    return " ".join(map(str, parts))


def run_jobs(lines, nproc, tag):
    exe = os.path.join(HERE, "wb")
    chunks = [lines[i::nproc] for i in range(nproc)]
    procs = []
    for k, ch in enumerate(chunks):
        inp = os.path.join(HERE, "tmp", f"{tag}_{k}.in")
        out = os.path.join(HERE, "tmp", f"{tag}_{k}.out")
        os.makedirs(os.path.dirname(inp), exist_ok=True)
        open(inp, "w").write("\n".join(ch) + "\n")
        procs.append((subprocess.Popen([exe], stdin=open(inp), stdout=open(out, "w")), out))
    res = {}
    for p, out in procs:
        p.wait()
        cur = None
        for line in open(out):
            x = line.split()
            if x[0] == "J":
                cur = int(x[1])
                res[cur] = {"M": [], "H": [], "X": False}
            elif x[0] == "M":
                res[cur]["M"].append((x[1], int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6])))
            elif x[0] == "H":
                res[cur]["H"].append((x[1], int(x[2]), int(x[3])))
            elif x[0] == "E":
                res[cur]["E"] = tuple(int(v) for v in x[1:])
            elif x[0] == "X":
                res[cur]["X"] = True
    return res


def mname(f, r, g, s):
    return f"{FILES[f]}{r}-{FILES[g]}{s}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["moves", "value"])
    ap.add_argument("split")
    ap.add_argument("--rule", default="count")
    ap.add_argument("--aware", type=int, default=1)
    ap.add_argument("--ep", type=int, default=1)
    ap.add_argument("--cap", type=int, default=20_000_000)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--k", type=int, default=0, help="only rows with this k")
    ap.add_argument("--sample", type=int, default=0, help="random sample of this many rows (seed 7)")
    a = ap.parse_args()
    rows = load(a.split)
    if a.k:
        rows = [r for r in rows if r["k"] == a.k]
    if a.sample:
        rows = random.Random(7).sample(rows, min(a.sample, len(rows)))
    if a.limit:
        rows = rows[:a.limit]
    t0 = time.time()
    lines = []
    hsize = []
    for i, r in enumerate(rows):
        H = []
        if a.mode == "value":
            gm = G()
            H = gm.export(gm.neg(parse_value(gm, r["value_ascii"])))
            hsize.append(len(H))
        lines.append(job_line(i, r, a.rule, a.aware, a.ep, a.cap, int(a.mode == "value"), H))
    tag = f"{a.mode}_{a.split}_{a.rule}_a{a.aware}_e{a.ep}_k{a.k}_s{a.sample}_l{a.limit}"
    res = run_jobs(lines, a.jobs, tag)
    agree = bad = unknown = 0
    tot_nodes = tot_epa = tot_epd = 0
    bad_list = []
    for i, r in enumerate(rows):
        o = res[i]
        nodes, epa, epd, ab = o["E"]
        tot_nodes += nodes
        tot_epa += epa
        tot_epd += epd
        if o["X"]:
            bad += 1
            bad_list.append((r["id"], "root has passer"))
            continue
        if a.mode == "moves":
            if ab or any(m[5] < 0 for m in o["M"]):
                unknown += 1
                continue
            legal = {s: sorted(mname(*m[1:5]) for m in o["M"] if m[0] == s) for s in "WB"}
            wins = {s: sorted(mname(*m[1:5]) for m in o["M"] if m[0] == s and m[5] == 1) for s in "WB"}
            wf, bf = bool(wins["W"]), bool(wins["B"])
            oc = "L" if wf and not bf else "R" if bf and not wf else "N" if wf else "P"
            ok = (legal == {s: sorted(r["legal_moves"][s]) for s in "WB"}
                  and wins == {s: sorted(r["winning_moves"][s]) for s in "WB"} and oc == r["outcome"])
            if ok:
                agree += 1
            else:
                bad += 1
                bad_list.append((r["id"], r["position"], r["board"], oc, r["outcome"], wins, r["winning_moves"]))
        else:
            allr = [m[5] for m in o["M"]] + [h[2] for h in o["H"]]
            if any(x == 1 for x in allr):
                bad += 1
                wf = any(x[-1] == 1 for x in o["M"] + o["H"] if x[0] == "W")
                bf = any(x[-1] == 1 for x in o["M"] + o["H"] if x[0] == "B")
                bad_list.append((r["id"], r["position"], r["board"], r["value_ascii"], "W-first wins" if wf else "", "B-first wins" if bf else ""))
            elif ab or any(x < 0 for x in allr):
                unknown += 1
            else:
                agree += 1
    out = {"mode": a.mode, "split": a.split, "rule": a.rule, "aware": a.aware, "ep": a.ep, "cap": a.cap,
           "k": a.k, "sample": a.sample, "limit": a.limit,
           "rows": len(rows), "agree": agree, "disagree": bad, "unknown(cap)": unknown,
           "nodes": tot_nodes, "ep_capture_available_events": tot_epa, "ep_test_differs_events": tot_epd,
           "max_H_nodes": max(hsize) if hsize else 0, "seconds": round(time.time() - t0, 1),
           "disagreements": bad_list[:40]}
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "results", tag + ".json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "disagreements"}))
    for x in bad_list[:10]:
        print("  BAD", x)


if __name__ == "__main__":
    main()
