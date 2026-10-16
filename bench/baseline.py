"""Baseline: whole-board alpha-beta that ignores the decomposition into components.

The search plays the real pawn game on the whole board:
  * a side with no legal move loses;
  * after a move, if exactly one side has a passed pawn, that side wins;
    if both do (a promotion race), the "count" rule of cylcgt decides;
  * double steps and en passant follow the chess rules (an e.p. right lasts
    for the opponent's very next move only, whatever component it is in).
The solver (class Solver here, and the C port bench/ab.c with identical move
order and node counts) does not import cylcgt and has its own move generator;
only the experiment harness below uses cylcgt, for the CGT timings.

Values are win/loss (+1/-1) for the side to move, so alpha-beta with the
window (-1, +1) stops at the first winning move ("plain" = no transposition
table, no move ordering). `tt=True` adds a transposition table.

All times are CPU seconds (process time), not wall-clock time.

Scaling experiment (writes bench/results/baseline_scaling_c.{json,md}; needs
`cc -O2 -o bench/ab bench/ab.c`):
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.baseline \
        --engine c --chains 8 --kmax 8 --per-k 12 --node-cap 30000000 --time-cap 60 --seed 1
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from pathlib import Path

RANKS = 8
ROOT = Path(__file__).resolve().parent


class NodeCap(Exception):
    pass


class Solver:
    def __init__(self, files: int, wrap: bool, tt: bool = False, node_cap: int | None = None,
                 time_cap: float | None = None):
        self.W, self.wrap, self.use_tt = files, wrap, tt
        self.node_cap, self.time_cap = node_cap, time_cap
        self.nodes = 0
        self.tt: dict = {}
        self.t_end = None

    # --- rules -----------------------------------------------------------
    def nb(self, f, df):
        g = f + df
        if self.wrap:
            return g % self.W
        return g if 0 <= g < self.W else None

    def passed(self, mine, theirs, white_side):
        for f, r in mine:
            fs = (f, self.nb(f, -1), self.nb(f, 1))
            if white_side:
                if not any(g in fs and s > r for g, s in theirs):
                    return True
            else:
                if not any(g in fs and s < r for g, s in theirs):
                    return True
        return False

    def dist(self, mine, theirs, white_side):
        """Moves to promote for the side's best passed front pawn (count rule)."""
        occ = mine | theirs
        best = 10 ** 6
        for f, r in mine:
            fs = (f, self.nb(f, -1), self.nb(f, 1))
            if white_side:
                if any(g in fs and s > r for g, s in theirs) or any((f, s) in occ for s in range(r + 1, RANKS + 1)):
                    continue
                d = RANKS - r - (1 if r == 2 else 0)
            else:
                if any(g in fs and s < r for g, s in theirs) or any((f, s) in occ for s in range(1, r)):
                    continue
                d = r - 1 - (1 if r == RANKS - 1 else 0)
            best = min(best, d)
        return best

    def children(self, white, black, ep, side_white):
        """Yield (new_white, new_black, new_ep). ep = (target_sq, captured_sq) usable by side to move."""
        mine, theirs = (white, black) if side_white else (black, white)
        occ = white | black
        d = 1 if side_white else -1
        start = 2 if side_white else RANKS - 1
        out = []
        for (f, r) in sorted(mine):  # (file, rank) order, as in ab.c
            r1 = r + d
            if not 1 <= r1 <= RANKS:
                continue
            rest = mine - {(f, r)}
            if (f, r1) not in occ:
                out.append((rest | {(f, r1)}, theirs, None))
                r2 = r + 2 * d
                if r == start and (f, r2) not in occ:
                    out.append((rest | {(f, r2)}, theirs, ((f, r1), (f, r2))))
            for df in (-1, 1):
                g = self.nb(f, df)
                if g is None:
                    continue
                t = (g, r1)
                if t in theirs:
                    out.append((rest | {t}, theirs - {t}, None))
                elif ep is not None and ep[0] == t:
                    out.append((rest | {t}, theirs - {ep[1]}, None))
        res = []
        for m2, t2, e in out:
            res.append((m2, t2, e) if side_white else (t2, m2, e))
        return res

    # --- search ----------------------------------------------------------
    def negamax(self, white, black, ep, side_white, alpha=-1, beta=1):
        self.nodes += 1
        if self.node_cap is not None and self.nodes > self.node_cap:
            raise NodeCap
        if self.t_end is not None and (self.nodes & 1023) == 0 and time.process_time() > self.t_end:
            raise NodeCap
        key = None
        if self.use_tt:
            key = (white, black, ep, side_white)
            v = self.tt.get(key)
            if v is not None:
                return v
        best = -1
        for nw, nbk, e in self.children(white, black, ep, side_white):
            wp = self.passed(nw, nbk, True)
            bp = self.passed(nbk, nw, False)
            if wp != bp:
                v = 1 if (wp == side_white) else -1
            elif wp:  # race: the mover's opponent moves first; fewer moves wins, opponent wins ties
                dm = self.dist(nw, nbk, True) if side_white else self.dist(nbk, nw, False)
                do = self.dist(nbk, nw, False) if side_white else self.dist(nw, nbk, True)
                v = -1 if do <= dm else 1
            else:
                v = -self.negamax(nw, nbk, e, not side_white, -beta, -alpha)
            if v > best:
                best = v
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
        if self.use_tt:
            self.tt[key] = best
        return best

    def solve(self, white, black, side_white):
        """+1 if the side to move wins. Raises NodeCap past the budget."""
        self.nodes = 0
        self.tt = {}
        self.t_end = None if self.time_cap is None else time.process_time() + self.time_cap
        return self.negamax(frozenset(white), frozenset(black), None, side_white)


def outcome_class(files, wrap, white, black, tt=True, node_cap=None):
    """L/R/N/P from two searches (White first, Black first)."""
    s = Solver(files, wrap, tt=tt, node_cap=node_cap)
    w_first = s.solve(white, black, True) == 1   # White wins moving first
    b_first = s.solve(white, black, False) == 1  # Black wins moving first
    if w_first and not b_first:
        return "L"
    if b_first and not w_first:
        return "R"
    return "N" if w_first else "P"


AB_BIN = ROOT / "ab"


def c_solve(jobs, binary=AB_BIN):
    """Run ab.c on jobs [(files, wrap, white, black, side_white, tt, node_cap, time_cap)].
    Returns [(result, nodes, seconds)] with result 1 / -1 / 0 (= cap reached)."""
    if not Path(binary).exists():
        raise FileNotFoundError(f"{binary} missing: build it with  cc -O2 -o bench/ab bench/ab.c")
    lines = []
    for files, wrap, white, black, side_white, tt, cap, tcap in jobs:
        w = " ".join(f"{f} {r}" for f, r in sorted(white))
        b = " ".join(f"{f} {r}" for f, r in sorted(black))
        lines.append(f"{files} {int(wrap)} {int(side_white)} {int(tt)} {cap or 0} {tcap or 0} "
                     f"{len(white)} {w} {len(black)} {b}")
    r = subprocess.run([str(binary)], input="\n".join(lines) + "\n", capture_output=True, text=True, check=True)
    out = []
    for line in r.stdout.strip().splitlines():
        v, n, t = line.split()
        out.append((int(v), int(n), float(t)))
    assert len(out) == len(jobs)
    return out


# ---------------------------------------------------------------------------
# scaling experiment
# ---------------------------------------------------------------------------

def _sq(t):
    return ("abcdefghijklmnopqrstuvwxyz".index(t[0]), int(t[1:]))


def build_chains(comps, n_chains, kmax, seed, max_files=26):
    """Nested instances: chain j uses components c1..ck (k = 1..kmax) of one
    random sequence of non-zero-valued training components, side by side on a
    flat board with one empty file between components (instance k+1 =
    instance k plus one component). Sequences whose full board would exceed
    `max_files` are redrawn."""
    pool = [c for c in comps if c["heldout"] is None and c["value"] != "0"]
    rng = random.Random(seed)
    chains = []
    while len(chains) < n_chains:
        seq = [rng.choice(pool) for _ in range(kmax)]
        if sum(c["width"] for c in seq) + kmax - 1 > max_files:
            continue
        chain = []
        for k in range(1, kmax + 1):
            white, black, f, games = [], [], 0, []
            for c in seq[:k]:
                p = c["_pos"]
                white += [(x + f, r) for x, r in p.white]
                black += [(x + f, r) for x, r in p.black]
                games.append(c["_game"])
                f += c["width"] + 1
            chain.append({"set": "chain", "chain": len(chains), "k": k, "files": f - 1, "wrap": False,
                          "white": sorted(white), "black": sorted(black),
                          "values": [c["value"] for c in seq[:k]], "_games": games})
        chains.append(chain)
    return chains


def dataset_sample(comps, per_k, seed):
    """`per_k` benchmark rows for each k: k = 1..3 from val.jsonl, 4..6 from test.jsonl."""
    by_id = {c["comp_id"]: c for c in comps}
    rng = random.Random(seed)
    out = []
    for split, ks in (("val", (1, 2, 3)), ("test", (4, 5, 6))):
        rows = [json.loads(x) for x in (ROOT / "data" / f"{split}.jsonl").read_text().splitlines()]
        for k in ks:
            rk = [r for r in rows if r["k"] == k]
            for r in rng.sample(rk, min(per_k, len(rk))):
                out.append({"set": "dataset", "id": r["id"], "k": k, "files": r["board"]["files"],
                            "wrap": r["board"]["cylinder"], "white": sorted(map(_sq, r["white"])),
                            "black": sorted(map(_sq, r["black"])), "values": [c["value"] for c in r["components"]],
                            "outcome_gold": r["outcome"],
                            "_games": [by_id[c["comp_id"]]["_game"] for c in r["components"]]})
    return out


FRESH = r"""
import sys, json, time
from cylcgt import cgt, pawns
d = json.loads(sys.argv[1])
pos = pawns.Pos(frozenset(map(tuple, d["white"])), frozenset(map(tuple, d["black"])))
t = time.process_time()
g = pawns.value(pawns.Board(d["files"], 8, d["wrap"], True), pos)
o = cgt.outcome(g)
print(json.dumps({"outcome": o, "seconds": time.process_time() - t}))
"""


def cgt_fresh(inst):
    """Time cylcgt from scratch (new interpreter, empty caches; import time excluded)."""
    arg = json.dumps({"files": inst["files"], "wrap": inst["wrap"], "white": inst["white"], "black": inst["black"]})
    env = {"PYTHONPATH": str(ROOT.parent), "PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}
    r = subprocess.run([sys.executable, "-c", FRESH, arg], capture_output=True, text=True, env=env,
                       cwd=str(ROOT.parent), timeout=600)
    return json.loads(r.stdout.strip().splitlines()[-1])


def _search(inst, variant, side, engine, node_cap, time_cap):
    if engine == "c":
        v, n, t = c_solve([(inst["files"], inst["wrap"], inst["white"], inst["black"], side,
                            variant == "tt", node_cap, time_cap)])[0]
        return {"solved": v != 0, "win": v == 1, "nodes": n, "seconds": t} if v else \
            {"solved": False, "nodes": n, "seconds": t}
    s = Solver(inst["files"], inst["wrap"], tt=(variant == "tt"), node_cap=node_cap, time_cap=time_cap)
    t = time.process_time()
    try:
        v = s.solve(inst["white"], inst["black"], side)
        return {"solved": True, "win": v == 1, "nodes": s.nodes, "seconds": time.process_time() - t}
    except NodeCap:
        return {"solved": False, "nodes": s.nodes, "seconds": time.process_time() - t}


def measure(inst, engine, node_cap, time_cap):
    """Every search is run (no skipping): a larger instance is not assumed to be harder."""
    from cylcgt import cgt
    t0 = time.process_time()
    G = cgt.total(inst["_games"])
    o = cgt.outcome(G)
    t_sum = time.process_time() - t0
    fresh = cgt_fresh(inst)
    assert fresh["outcome"] == o
    if "outcome_gold" in inst:
        assert inst["outcome_gold"] == o
    row = {k: v for k, v in inst.items() if not k.startswith("_") and k not in ("white", "black")}
    row.update({"pawns": len(inst["white"]) + len(inst["black"]), "outcome": o,
                "cgt_sum_seconds": t_sum, "cgt_fresh_seconds": fresh["seconds"]})
    for variant in ("plain", "tt"):
        for side in (True, False):
            tag = f"{variant}_{'W' if side else 'B'}"
            row[tag] = _search(inst, variant, side, engine, node_cap, time_cap)
        rw, rb = row[f"{variant}_W"], row[f"{variant}_B"]
        if rw.get("solved") and rb.get("solved"):
            oc = ("L" if rw["win"] and not rb["win"] else "R" if not rw["win"] and rb["win"]
                  else "N" if rw["win"] else "P")
            row[f"{variant}_outcome"] = oc
            row[f"{variant}_agrees"] = oc == o
    return row


def run_scaling(a):
    from .components import build
    comps, _ = build(verbose=False)
    rows = []
    for chain in build_chains(comps, a.chains, a.kmax, a.seed):
        for inst in chain:
            rows.append(measure(inst, a.engine, a.node_cap, a.time_cap))
            print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    for inst in dataset_sample(comps, a.per_k, a.seed):
        rows.append(measure(inst, a.engine, a.node_cap, a.time_cap))
        print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    a.out.mkdir(parents=True, exist_ok=True)
    meta = {"engine": a.engine, "node_cap": a.node_cap, "time_cap": a.time_cap, "seed": a.seed,
            "chains": a.chains, "kmax": a.kmax, "per_k": a.per_k}
    stem = f"baseline_scaling_{a.engine}"
    (a.out / f"{stem}.json").write_text(json.dumps({"meta": meta, "rows": rows}, indent=1, ensure_ascii=False) + "\n")
    md = scaling_tables(rows, meta)
    (a.out / f"{stem}.md").write_text(md)
    print(md)


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    return None if n == 0 else xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def _fmt_med(searches, key):
    """Median over ALL searches, counting unsolved/skipped ones as +infinity."""
    vals = [x[key] if x.get("solved") else float("inf") for x in searches]
    m = _median(vals)
    if m == float("inf"):
        return "> cap"
    return f"{m:,.0f}" if key == "nodes" else f"{m:.2g}"


def scaling_tables(rows, meta):
    cap = []
    if meta["node_cap"]:
        cap.append(f"{meta['node_cap']:,} nodes")
    if meta["time_cap"]:
        cap.append(f"{meta['time_cap']:g} s")
    out = [f"Engine: {meta['engine']} (bench/{'ab.c' if meta['engine'] == 'c' else 'baseline.py'}); "
           f"cap per search: {' / '.join(cap)} (CPU). Each instance is searched twice (White first, Black first); "
           "medians are over all searches, with unsolved searches counted as infinite. Times are CPU seconds.", ""]
    for kind, title in (("chain", "Nested chains (instance k+1 = instance k plus one more component)"),
                        ("dataset", "Benchmark rows (k <= 3 from val, k >= 4 from test)")):
        rs_all = [r for r in rows if r["set"] == kind]
        if not rs_all:
            continue
        out += [f"### {title}", "",
                "| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | "
                "α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | "
                "CGT from scratch, median s |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for k in sorted({r["k"] for r in rs_all}):
            rs = [r for r in rs_all if r["k"] == k]
            cells = [str(k), str(len(rs)), f"{_median([r['pawns'] for r in rs]):g}"]
            for v in ("plain", "tt"):
                ss = [r[f"{v}_{s}"] for r in rs for s in "WB"]
                cells.append(f"{sum(1 for x in ss if x.get('solved'))}/{len(ss)}")
                cells.append(_fmt_med(ss, "nodes"))
                cells.append(_fmt_med(ss, "seconds"))
            cells.append(f"{_median([r['cgt_sum_seconds'] for r in rs]):.1g}")
            cells.append(f"{_median([r['cgt_fresh_seconds'] for r in rs]):.2g}")
            out.append("| " + " | ".join(cells) + " |")
        out.append("")
        if kind == "chain":
            out += ["Growth per added component (chains): median over chains and sides of nodes(k) / nodes(k-1), "
                    "where both searches finished.", "", "| k | plain α-β | α-β+TT |", "|---|---|---|"]
            by = {(r["chain"], r["k"]): r for r in rs_all}
            for k in sorted({r["k"] for r in rs_all})[1:]:
                cells = [str(k)]
                for v in ("plain", "tt"):
                    ratios = []
                    for (c, kk), r in by.items():
                        if kk != k or (c, k - 1) not in by:
                            continue
                        for sd in "WB":
                            a, b = by[(c, k - 1)][f"{v}_{sd}"], r[f"{v}_{sd}"]
                            if a.get("solved") and b.get("solved"):
                                ratios.append(b["nodes"] / a["nodes"])
                    cells.append(f"{_median(ratios):.1f} (n={len(ratios)})" if ratios else "—")
                out.append("| " + " | ".join(cells) + " |")
            out.append("")
    agree = [r[f"{v}_agrees"] for r in rows for v in ("plain", "tt") if f"{v}_agrees" in r]
    out += [f"Outcome agreement between the searches and CGT wherever both searches of an instance finished: "
            f"{sum(agree)}/{len(agree)}."]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", choices=["c", "python"], default="c")
    ap.add_argument("--chains", type=int, default=12)
    ap.add_argument("--kmax", type=int, default=8)
    ap.add_argument("--per-k", type=int, default=20)
    ap.add_argument("--node-cap", type=int, default=0, help="0 = none")
    ap.add_argument("--time-cap", type=float, default=20.0)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", type=Path, default=ROOT / "results")
    ap.add_argument("--table-only", action="store_true", help="re-render the .md from the saved .json")
    a = ap.parse_args()
    if a.table_only:
        stem = a.out / f"baseline_scaling_{a.engine}"
        d = json.loads(stem.with_suffix(".json").read_text())
        md = scaling_tables(d["rows"], d["meta"])
        stem.with_suffix(".md").write_text(md)
        print(md)
    else:
        run_scaling(a)
