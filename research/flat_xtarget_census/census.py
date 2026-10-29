"""Offline multi-target flat 8x8 census (avenue 6).

Pool every exact real-chess result for an embedded position (4-file component
next to the g-file trebuchet WK f5 Pg4 / BK h4 Pg5) that already exists on disk,
score each one with the cylcgt model under 2 passer tests x 3 race rules, and
write pool.json / census.json.  No network (sockets are disabled), no git, no
file outside this folder is written.

    cd <project root>; PYTHONPATH=. nice -n 15 .venv/bin/python research/flat_xtarget_census/census.py
"""
from __future__ import annotations

import glob
import json
import math
import os
import socket
import sys
import time
from collections import Counter, defaultdict

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
OUT = os.path.join(ROOT, "research", "flat_xtarget_census")
sys.path.insert(0, ROOT)


from cylcgt import cgt, pawns                       # noqa: E402
from cylcgt.pawns import Pos                         # noqa: E402
from realchess import component as C                 # noqa: E402
from realchess import movegen as mg                  # noqa: E402
from realchess.kb import KB                          # noqa: E402
from realchess.solve_candidate import Model          # noqa: E402

def _no_net(*a, **k):
    raise RuntimeError("network disabled: offline census fails closed")


socket.socket = _no_net  # type: ignore
socket.create_connection = _no_net  # type: ignore

RULES = ("count", "mover", "opponent")
CONVS = (("textbook", False), ("e.p.-aware", True))
TARGETS = {
    "A2 (refuted *2)": "W: a2 c2 / B: b7 d7",
    "1/8": "W: a2 b2 b3 / B: a5 a6 b6",
    "up-second-star": "W: a2 b2 b6 / B: a6 b7 c5",
    "tiny(1)": "W: a2 b2 b6 / B: a6 b7 c6",
    "pos A (*2 cand.)": "W: a4 b3 d2 d3 / B: a7 b7 c5",
    "pos B (*2 cand.)": "W: b4 c2 d2 / B: a6 a7 c6 d5",
    "cand 3": "W: a3 b2 b4 / B: a7 b6 c6",
    "cand 4": "W: a3 b2 c2 / B: a4 b6 c5",
    "cand 2 (refuted)": "W: a3 b3 c2 / B: b5 b7 c6",
    "cand 5": "W: a5 b3 c4 / B: a6 b7 c7",
    "cand 6": "W: a3 b2 d3 / B: a6 c7 d6",
}
CAT = {"win": 1, "draw": 0, "loss": -1}
WDL = {"W": 1, "D": 0, "L": -1}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ------------------------------------------------------------------ pool
pool: dict[str, dict] = {}
conflicts = []


def add(fen, res_stm, src, l8=False):
    nf = mg.normal_fen(fen)
    e = pool.get(nf)
    if e is None:
        pool[nf] = {"res": res_stm, "src": [src], "l8": l8}
        return
    if e["res"] != res_stm:
        conflicts.append({"fen": nf, "have": e["res"], "have_src": e["src"], "new": res_stm, "new_src": src})
        return
    if src not in e["src"]:
        e["src"].append(src)
    e["l8"] = e["l8"] and l8     # l8 only if every source relies on Lichess 8-man categories


def tokens_to_fen(line):
    toks = line.split()
    stm, ep = toks[-2], toks[-1]
    b = [["."] * 8 for _ in range(8)]
    for t in toks[:-2]:
        pc, f, r = t[0], "abcdefgh".index(t[1]), int(t[2])
        b[r - 1][f] = pc
    rows = []
    for r in range(7, -1, -1):
        s, n = "", 0
        for ch in b[r]:
            if ch == ".":
                n += 1
            else:
                s += (str(n) if n else "") + ch
                n = 0
        rows.append(s + (str(n) if n else ""))
    return "/".join(rows) + f" {stm} - {ep} 0 1"


def load_pool():
    srcs = Counter()
    # 1. Lichess-derived knowledge base (cache only)
    kb = KB()
    for fen, (cat, prov) in kb.cat.items():
        if cat not in CAT:
            continue
        pos = mg.parse_fen(fen)
        if not C.only_component_and_trebuchet(pos):
            continue
        men = pos.men()
        add(fen, CAT[cat], "kb" + ("-l8" if men >= 8 else ""), l8=men >= 8)
        srcs["kb"] += 1
    # 2. realdb (tablebase / search results)
    for l in open(os.path.join(ROOT, "realchess/certify/results/realdb.jsonl")):
        r = json.loads(l)
        pos = mg.parse_fen(r["fen"])
        if C.only_component_and_trebuchet(pos):
            add(r["fen"], r["result_stm"], "realdb", l8="Lichess 8-man" in r["how"] and "no Lichess" not in r["how"])
            srcs["realdb"] += 1
    # 3. A2 node file (search over tablebase)
    d = json.load(open(os.path.join(ROOT, "realchess/results/comp_Wa2c2_Bb7d7_nodes_pure_offline.json")))
    for r in d["nodes"]:
        for s in "WB":
            if r.get(s + "_fen") and r.get(s) and r[s][0] == r[s][1]:
                add(r[s + "_fen"], r[s][0], "A2nodes")
                srcs["A2nodes"] += 1
    # 4. kpsolve outputs (exact only when the two bounds meet); White's view
    files = (glob.glob(os.path.join(ROOT, "realchess/targets18/*.out")) +
             glob.glob(os.path.join(ROOT, "realchess/targets18/r7/*.out")) +
             glob.glob(os.path.join(ROOT, "research/star2_oracle/kp_*.out")))
    kp_seen = Counter()
    for f in sorted(files):
        for l in open(f):
            if l.startswith("#") or "|" not in l:
                continue
            lhs, rhs = l.rsplit("|", 1)
            a = rhs.split()
            if len(a) != 2 or a[0] != a[1] or a[0] not in WDL:
                kp_seen["inexact"] += 1
                continue
            fen = tokens_to_fen(lhs)
            pos = mg.parse_fen(fen)
            if not C.only_component_and_trebuchet(pos):
                kp_seen["off-model"] += 1
                continue
            w = WDL[a[0]]
            add(fen, w if pos.stm == "w" else -w, "kpsolve:" + os.path.relpath(f, ROOT))
            kp_seen["exact"] += 1
    srcs["kpsolve"] = dict(kp_seen)
    # 5. star2 searcher results (mover's view)
    d = json.load(open(os.path.join(ROOT, "research/star2_oracle/tb_A_8men.json")))
    for s in d["sides"]:
        if s["exact"]:
            add(s["fen"], s["interval"][0], "star2_tb_A")
            srcs["star2_tb_A"] += 1
    return srcs, kb


# ------------------------------------------------------------------ model
def comp_pos(pos):
    c = C.component_of(pos)
    if pos.ep is not None and pos.ep % 8 < 4:
        f, r = pos.ep % 8, pos.ep // 8 + 1
        stm = "W" if pos.stm == mg.WHITE else "B"
        cap = (f, r - 1) if stm == "W" else (f, r + 1)
        c = Pos(c.white, c.black, ((f, r), cap, stm))
    return c


def set_conv(flag):
    pawns.PASSED_RESPECTS_EP = flag
    pawns._value.cache_clear()
    return Model()


def wilson(k, n, z=1.959964):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def main():
    t0 = time.time()
    log("loading pool (cache only)")
    srcs, kb = load_pool()
    log("pool", len(pool), "conflicts", len(conflicts), dict(srcs))
    json.dump({"sources_loaded": srcs, "conflicts": conflicts, "kb_stats": kb.stats(),
               "pool_size": len(pool)}, open(os.path.join(OUT, "pool_meta.json"), "w"), indent=1, default=str)

    fens = sorted(pool)
    poss = {f: mg.parse_fen(f) for f in fens}
    comps = {f: comp_pos(poss[f]) for f in fens}

    # trees per target per convention
    trees = {}
    for conv, flag in CONVS:
        set_conv(flag)
        for tn, ts in TARGETS.items():
            root = Pos.parse(ts)
            internal, terms, _ = C.enumerate_tree(C.BOARD4, root)
            trees[(conv, tn)] = (internal, terms)
            log("tree", conv, tn, len(internal), len(terms))

    rows = {}   # fen -> dict
    for conv, flag in CONVS:
        model = set_conv(flag)
        for fen in fens:
            pos, p = poss[fen], comps[fen]
            r = rows.setdefault(fen, {"fen": fen, "res": pool[fen]["res"], "src": pool[fen]["src"], "l8": pool[fen]["l8"],
                                      "men": pos.men(), "stm": "W" if pos.stm == mg.WHITE else "B",
                                      "npawn": len(p.white) + len(p.black),
                                      "afile": sum(1 for q in p.white | p.black if q[0] == 0),
                                      "pred": {}, "term": {}, "race": {}, "tree": {}})
            term = C.is_terminal(C.BOARD4, p)
            r["term"][conv] = term
            r["race"][conv] = bool(term and pawns.passed(C.BOARD4, p, "W") and pawns.passed(C.BOARD4, p, "B"))
            r["ep"] = p.ep is not None
            r["tree"][conv] = [tn for tn in TARGETS if p in trees[(conv, tn)][0] or p in trees[(conv, tn)][1]]
            for rule in RULES:
                if not term and r["npawn"] > 6:
                    r["pred"][f"{conv}|{rule}"] = None
                    continue
                r["pred"][f"{conv}|{rule}"] = model.stm_wins(pos, rule)
        log("scored", conv, "t=%.0fs" % (time.time() - t0))
    json.dump(list(rows.values()), open(os.path.join(OUT, "pool_scored.json"), "w"))
    log("done", "t=%.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
