#!/usr/bin/env python
"""Workstream A2-search, analysis of values.jsonl.

  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py all

Sub-commands (each writes a JSON file next to this script):
  robust   nimbers.json  - every *k (k>=2) plus the known candidate, under
                           RACE_RULE count/mover/opponent x ep on/off, race-node
                           counts, all-races-to-White / all-races-to-Black
                           extremes, independent minimax check, ranking.
  targets  targets.json  - Elkies' 8x8 open targets (nimbers, dyadics with
                           denominator >= 8, up-second and higher ups, tinies).
  checks   checks.json   - colour-reversal consistency of the database, and an
                           outcome cross-check against crosscheck/minimax.py.
  sens     sensitivity.json - for the known candidate: which single race nodes
                           change the value when their outcome is flipped.

Two implementations are involved:
  * cylcgt/pawns.py + cylcgt/cgt.py (canonical forms);
  * crosscheck/minimax.py (Codex, independent rules code) wrapped here in a
    plain win/loss search of  G + *k  (G = *k  iff  G + *k  is a second-player
    win).  Only the heap wrapper below is new code.
"""
from __future__ import annotations

import json
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import BIG, Board, Pos, passed  # noqa: E402
from crosscheck import minimax as mm  # noqa: E402

sys.setrecursionlimit(1_000_000)
RANKS = 8
CANDIDATE = ("W: a2 c2 / B: b7 d7", 4)
SETTINGS = [(rule, ep) for rule in ("count", "mover", "opponent") for ep in (True, False)]
EXTREMES = ("allW", "allB")


def load_db(path=os.path.join(HERE, "values.jsonl")):
    with open(path) as fh:
        return [json.loads(line) for line in fh]


# --------------------------------------------------------------------------
# implementation 1: cylcgt, with race rule control
# --------------------------------------------------------------------------

_ORIG_CHILD = pawns._child


def _fixed_child(winner_fn):
    """A replacement for pawns._child (monkeypatched at runtime only; the file
    cylcgt/pawns.py is not modified) that resolves races by winner_fn."""
    def child(board, pos, mover):
        if passed(board, pos, "W") and passed(board, pos, "B"):
            pawns.race_hits.append(f"{pos} after {mover}")
            w = winner_fn(board, pos, mover)
            return cgt.integer(BIG if w == "W" else -BIG)
        return pawns.value(board, pos)
    return child


def count_winner(board, pos, mover):
    other = "B" if mover == "W" else "W"
    return other if pawns.promote_distance(board, pos, other) <= pawns.promote_distance(board, pos, mover) else mover


def cgt_value(width, s, rule, ep, override=None):
    """Value under a race rule. rule in count/mover/opponent (stock code) or
    allW/allB (patched). override: dict race-key -> winner on top of count."""
    board = Board(width, RANKS, False, ep)
    try:
        if rule in ("count", "mover", "opponent") and override is None:
            pawns._child = _ORIG_CHILD
            pawns.RACE_RULE = rule
        elif rule == "allW":
            pawns._child = _fixed_child(lambda b, p, m: "W")
        elif rule == "allB":
            pawns._child = _fixed_child(lambda b, p, m: "B")
        elif override is not None:
            def fn(b, p, m):
                return override.get(f"{p} after {m}") or count_winner(b, p, m)
            pawns._child = _fixed_child(fn)
        else:
            raise ValueError(rule)
        pawns._value.cache_clear()
        pawns.race_hits.clear()
        g = pawns.value(board, Pos.parse(s))
        hits = list(pawns.race_hits)
    finally:
        pawns._child = _ORIG_CHILD
        pawns.RACE_RULE = "count"
        pawns._value.cache_clear()
    return g, hits


def n_pawns_in(s):
    body = s.rsplit(" after ", 1)[0]
    body = re.sub(r"\s*\(ep [a-z]\d+\)", "", body)
    w, b = body.split("/")
    return len(w.split(":")[1].split()) + len(b.split(":")[1].split())


def race_stats(s, hits):
    root_n = n_pawns_in(s + " after W")
    distinct = sorted(set(hits))
    pre_edges = [h for h in hits if n_pawns_in(h) == root_n]
    pre_distinct = sorted(set(pre_edges))
    return {"race_edges": len(hits), "race_positions_distinct": len(distinct),
            "precapture_race_edges": len(pre_edges),
            "precapture_race_positions_distinct": len(pre_distinct),
            "by_pawns_left": dict(sorted(Counter(n_pawns_in(h) for h in distinct).items()))}


# --------------------------------------------------------------------------
# pawn-structure legality of the 8x8 embedding (necessary conditions only)
# --------------------------------------------------------------------------

TREBUCHET_W = [(6, 4)]  # Pg4
TREBUCHET_B = [(6, 5)]  # Pg5


def _min_cost_assignment(pawns_, reach):
    """Min total file shift to give each pawn a distinct original file
    (0..7) it can come from; None if impossible. reach(f_orig, (f, r)) -> bool."""
    n = len(pawns_)
    INF = 10 ** 9
    dp = [INF] * (1 << n)  # dp[mask]: pawns in mask assigned to files seen so far
    dp[0] = 0
    for fo in range(8):
        new = dp[:]
        for mask in range(1 << n):
            if dp[mask] == INF:
                continue
            for i, p in enumerate(pawns_):
                if not (mask >> i) & 1 and reach(fo, p):
                    m2 = mask | (1 << i)
                    c = dp[mask] + abs(fo - p[0])
                    if c < new[m2]:
                        new[m2] = c
        dp = new
    best = dp[(1 << n) - 1]
    return None if best == INF else best


def pawn_legality(s):
    """Necessary conditions for the 8x8 embedding (component on files a-d,
    trebuchet W Pg4 / B Pg5, WK f5, BK h4) to be reachable in chess:
      * every pawn has a distinct original file it can come from: a white pawn
        on (f, r) needs |f - f0| <= r - 2 captures (black: <= 7 - r), and the
        files are assigned injectively (so e.g. W a2 a3 b2 is impossible);
      * the minimal number of captures each side needs is at most the number
        of enemy men missing from the board (15 - enemy pawns).
    Sufficiency is not claimed (no full retrograde analysis)."""
    p = Pos.parse(s)
    W = sorted(p.white) + TREBUCHET_W
    B = sorted(p.black) + TREBUCHET_B
    cw = _min_cost_assignment(W, lambda fo, q: abs(fo - q[0]) <= q[1] - 2)
    cb = _min_cost_assignment(B, lambda fo, q: abs(fo - q[0]) <= 7 - q[1])
    ok = cw is not None and cb is not None and cw <= 15 - len(B) and cb <= 15 - len(W)
    return {"legal_necessary_conditions": ok, "min_captures_white": cw, "min_captures_black": cb}


# --------------------------------------------------------------------------
# implementation 2: crosscheck/minimax.py rules + a nim heap, plain win/loss
# --------------------------------------------------------------------------

def indep_winners(width, s, heap, rule, ep, strict_ep=False):
    """Winner of G + *heap with White to move and with Black to move.
    strict_ep: a heap move also cancels a pending e.p. right (real chess);
    otherwise the right persists across heap moves (the cylcgt model)."""
    board = mm.Board(width, RANKS, False, ep)
    root = mm.parse_position(s)
    memo = {}

    def decide(child, mover):
        wp, bp = mm.passed_flags(board, child)
        if wp != bp:
            return "W" if wp else "B"
        if wp and bp:
            if rule == "count":
                return mm._winner_after_move(board, child, mover)
            if rule == "mover":
                return mover
            if rule == "opponent":
                return "B" if mover == "W" else "W"
            if rule == "allW":
                return "W"
            if rule == "allB":
                return "B"
            raise ValueError(rule)
        return None

    def win(pos, h, side):
        key = (pos, h, side)
        r = memo.get(key)
        if r is not None:
            return r
        other = "B" if side == "W" else "W"
        res = other
        for child in mm.legal_moves(board, pos, side):
            w = decide(child, side)
            if w is None:
                w = win(child, h, other)
            if w == side:
                res = side
                break
        if res != side and h:
            hp = mm.Position(pos.white, pos.black, None) if (strict_ep and pos.ep) else pos
            for j in range(h):
                if win(hp, j, other) == side:
                    res = side
                    break
        memo[key] = res
        return res

    if any(passed_flags for passed_flags in mm.passed_flags(board, root)):
        raise ValueError("root has a passed pawn")
    return win(root, heap, "W"), win(root, heap, "B")


def indep_equals_nimber(width, s, k, rule, ep, strict_ep=False):
    """True iff G + *k is a second-player win, i.e. G = *k (exact)."""
    ww, wb = indep_winners(width, s, k, rule, ep, strict_ep)
    return ww == "B" and wb == "W"


def indep_nim_profile(width, s, rule, ep, strict_ep=False, kmax=4):
    """List of j in 0..kmax with G + *j a second-player win (at most one)."""
    return [j for j in range(kmax + 1) if indep_equals_nimber(width, s, j, rule, ep, strict_ep)]


def indep_equals_game(width, s, H, rule, ep, strict_ep=False):
    """Independent test of G = H: is G + (-H) a second-player win?  The pawn
    part is played with crosscheck/minimax.py; the gadget -H is played on the
    explicit option lists of a small cgt.Game (no canonical simplification is
    used in the search itself)."""
    board = mm.Board(width, RANKS, False, ep)
    root = mm.parse_position(s)
    gadget = cgt.neg(H)
    memo = {}

    def decide(child, mover):
        wp, bp = mm.passed_flags(board, child)
        if wp != bp:
            return "W" if wp else "B"
        if wp and bp:
            if rule == "count":
                return mm._winner_after_move(board, child, mover)
            return {"mover": mover, "opponent": "B" if mover == "W" else "W", "allW": "W", "allB": "B"}[rule]
        return None

    def win(pos, g, side):
        key = (pos, g.id, side)
        r = memo.get(key)
        if r is not None:
            return r
        other = "B" if side == "W" else "W"
        res = other
        for child in mm.legal_moves(board, pos, side):
            w = decide(child, side)
            if w is None:
                w = win(child, g, other)
            if w == side:
                res = side
                break
        if res != side:
            hp = mm.Position(pos.white, pos.black, None) if (strict_ep and pos.ep) else pos
            for gg in (g.L if side == "W" else g.R):
                if win(hp, gg, other) == side:
                    res = side
                    break
        memo[key] = res
        return res

    return win(root, gadget, "W") == "B" and win(root, gadget, "B") == "W"


def value_robustness(s, width, target, label):
    """Like robustness() but for a non-nimber target value (e.g. up-second)."""
    root_n = n_pawns_in(s + " after W")
    out = {"position": s, "width": width, "target": label, "pawns": root_n,
           "men_with_trebuchet": root_n + 4, "settings": {}}
    vals = {}
    for rule, ep in SETTINGS + [(r, e) for r in EXTREMES for e in (True, False)]:
        g, hits = cgt_value(width, s, rule, ep)
        vals[(rule, ep)] = g
        rec = {"value": cgt.show(g), "outcome": cgt.outcome(g), "equals_target": g is target}
        rec.update(race_stats(s, hits))
        rec["indep_equals_target"] = indep_equals_game(width, s, target, rule, ep)
        if ep:
            rec["indep_equals_target_strict_ep"] = indep_equals_game(width, s, target, rule, ep, strict_ep=True)
        rec["indep_agrees"] = rec["indep_equals_target"] == rec["equals_target"]
        out["settings"][f"{rule}/ep={'on' if ep else 'off'}"] = rec
    six = [vals[k] for k in SETTINGS]
    out["value_by_setting"] = "; ".join(f"{r}/{'ep' if e else 'noep'}={cgt.show(v)}" for (r, e), v in zip(SETTINGS, six))
    out["robust_6"] = all(v is target for v in six)
    out["race_assignment_independent"] = out["robust_6"] and all(vals[(r, e)] is target for r in EXTREMES
                                                                 for e in (True, False))
    base = out["settings"]["count/ep=on"]
    out["race_nodes"] = base["race_edges"]
    out["precapture_race_nodes"] = base["precapture_race_edges"]
    out["race_positions_distinct"] = base["race_positions_distinct"]
    out["precapture_race_positions_distinct"] = base["precapture_race_positions_distinct"]
    out["indep_all_agree"] = all(v["indep_agrees"] for v in out["settings"].values())
    return out


def cmd_values(db):
    """Robustness of the up-second and tiny/miny hits (values_robust.json)."""
    ups, up2, up3 = upsecond_checks()
    t1 = tiny(cgt.integer(1))
    # negatives (down-second, miny) are the colour reversals of these positions
    # (the database is closed under colour reversal; see checks.json), so they
    # have the same robustness profile and are not recomputed.
    targets = [(up2, "up-second {0|v*}"), (t1, "tiny(1)")]
    res = []
    for T, label in targets:
        name = cgt.show(T)
        for r in db:
            if r["value"] != name:
                continue
            t = time.time()
            o = value_robustness(r["position"], r["width"], T, label)
            o["wall_s"] = round(time.time() - t, 1)
            res.append(o)
            print(f"{label:20s} w{r['width']} {r['position']}: robust={o['robust_6']} "
                  f"assignment_indep={o['race_assignment_independent']} races={o['race_nodes']} "
                  f"pre={o['precapture_race_nodes']} indep_ok={o['indep_all_agree']}  [{o['value_by_setting']}]",
                  flush=True)
    res.sort(key=lambda o: (o["target"], not o["robust_6"], o["men_with_trebuchet"], o["precapture_race_nodes"],
                            o["race_nodes"]))
    with open(os.path.join(HERE, "values_robust.json"), "w") as fh:
        json.dump({"definition_checks": ups, "results": res}, fh, indent=1, ensure_ascii=False)


# --------------------------------------------------------------------------
# robust: nimbers.json
# --------------------------------------------------------------------------

def robustness(s, width):
    out = {"position": s, "width": width, "pawns": n_pawns_in(s + " after W"),
           "men_with_trebuchet": n_pawns_in(s + " after W") + 4, "settings": {}}
    vals = {}
    for rule, ep in SETTINGS + [(r, e) for r in EXTREMES for e in (True, False)]:
        t = time.process_time()
        g, hits = cgt_value(width, s, rule, ep)
        vals[(rule, ep)] = g
        rec = {"value": cgt.show(g), "nim": g.nim, "outcome": cgt.outcome(g),
               "cpu_s": round(time.process_time() - t, 3)}
        rec.update(race_stats(s, hits))
        # independent check: which j <= 4 has G + *j a P-position?
        rec["indep_nim_profile"] = indep_nim_profile(width, s, rule, ep)
        if ep:
            rec["indep_nim_profile_strict_ep"] = indep_nim_profile(width, s, rule, ep, strict_ep=True)
        rec["indep_agrees"] = (rec["indep_nim_profile"] == ([g.nim] if g.nim is not None else []))
        out["settings"][f"{rule}/ep={'on' if ep else 'off'}"] = rec
    # sandwich sanity: allB <= any rule <= allW (monotonicity of options)
    sandwich = all(cgt.le(vals[("allB", ep)], vals[(r, ep)]) and cgt.le(vals[(r, ep)], vals[("allW", ep)])
                   for r, ep in SETTINGS)
    six = [out["settings"][f"{r}/ep={'on' if e else 'off'}"]["value"] for r, e in SETTINGS]
    ext = [out["settings"][f"{r}/ep={'on' if e else 'off'}"]["value"] for r in EXTREMES for e in (True, False)]
    out["value_by_setting"] = "; ".join(f"{r}/{'ep' if e else 'noep'}={v}" for (r, e), v in zip(SETTINGS, six))
    out["robust_6"] = len(set(six)) == 1
    out["race_assignment_independent"] = len(set(six + ext)) == 1
    out["sandwich_allB_le_rule_le_allW"] = sandwich
    base = out["settings"]["count/ep=on"]
    out["race_nodes"] = base["race_edges"]
    out["precapture_race_nodes"] = base["precapture_race_edges"]
    out["race_positions_distinct"] = base["race_positions_distinct"]
    out["precapture_race_positions_distinct"] = base["precapture_race_positions_distinct"]
    out["indep_all_agree"] = all(v["indep_agrees"] for v in out["settings"].values())
    return out


def cmd_robust(db):
    nims = [r for r in db if r["nim"] is not None and r["nim"] >= 2]
    todo = [(r["position"], r["width"]) for r in nims]
    if CANDIDATE not in todo:
        todo.append(CANDIDATE)
    # nimbers that the independent census (indep_scan.py) found under OTHER
    # race / e.p. settings; they are not nimbers in the database setting
    census_hits = defaultdict(list)
    for f in sorted(os.listdir(os.path.join(HERE, "census"))) if os.path.isdir(os.path.join(HERE, "census")) else []:
        if not f.endswith(".json"):
            continue
        with open(os.path.join(HERE, "census", f)) as fh:
            d = json.load(fh)
        for s, w, prof in d["indep_nimbers_ge2"]:
            census_hits[(s, w)].append(f"{d['rule']}/ep={d['ep']}{'/strict' if d['strict_ep'] else ''}: *{prof[0]}")
            if (s, w) not in todo:
                todo.append((s, w))
    results = []
    for s, w in todo:
        t = time.time()
        res = robustness(s, w)
        rec = next((r for r in db if r["position"] == s and r["width"] == w), None)
        res["db_record"] = rec
        res["source"] = "database nimber" if (rec and rec["nim"] and rec["nim"] >= 2) else \
            ("known candidate" if (s, w) == CANDIDATE else "independent census under another setting")
        res["census_nimber_settings"] = census_hits.get((s, w), [])
        res["wall_s"] = round(time.time() - t, 1)
        results.append(res)
        print(f"{w} {s}: {res['value_by_setting']}  robust={res['robust_6']} "
              f"races={res['race_nodes']} pre={res['precapture_race_nodes']} "
              f"indep_ok={res['indep_all_agree']} ({res['wall_s']}s)", flush=True)
    results.sort(key=lambda r: (not r["robust_6"], r["men_with_trebuchet"], r["precapture_race_nodes"],
                                r["race_nodes"], r["position"]))
    summary = {
        "settings_note": "DB value uses RACE_RULE=count, ep on. allW/allB = every race won by White/Black "
                         "(runtime monkeypatch of pawns._child; pawns.py unchanged).",
        "n_nimbers_ge2_in_db": len(nims),
        "nimber_counts_by_k": dict(Counter(r["nim"] for r in nims)),
        "nimbers_by_width_and_components": dict(Counter(f"w{r['width']}/c{r['n_components']}" for r in nims)),
        "ranked": results,
    }
    with open(os.path.join(HERE, "nimbers.json"), "w") as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
    print(f"wrote nimbers.json with {len(results)} entries")


# --------------------------------------------------------------------------
# targets: Elkies' open 8x8 values
# --------------------------------------------------------------------------

def up_power(n):
    """CGSuite/Siegel construction for G = {0|H} = up (H = *):
    G^n = {0 | H - G^->(n-1)},  G^->m = {G^->(m-1) | H},  G^->0 = 0."""
    H = cgt.STAR

    def pow_to(m):
        g = cgt.ZERO
        for _ in range(m):
            g = cgt.make([g], [H])
        return g
    return cgt.make([cgt.ZERO], [cgt.add(H, cgt.neg(pow_to(n - 1)))])


def tiny(G):
    """tiny-G = {0 || 0 | -G}"""
    return cgt.make([cgt.ZERO], [cgt.make([cgt.ZERO], [cgt.neg(G)])])


def mult(n, g):
    out = cgt.ZERO
    h = g if n >= 0 else cgt.neg(g)
    for _ in range(abs(n)):
        out = cgt.add(out, h)
    return out


def upsecond_checks():
    up1, up2, up3 = up_power(1), up_power(2), up_power(3)
    res = {
        "definition_used": "up^2 = {0 | down*} (CGSuite source by A. Siegel: G^n = {0 | H - G^->(n-1)} with "
                           "G = up = {0|*}, H = *, G^->1 = up)",
        "up_power_1_is_up": up1 is cgt.UP,
        "up2_canonical": cgt.show(up2),
        "up2_equals_{0|down*}": up2 is cgt.make([cgt.ZERO], [cgt.add(cgt.DOWN, cgt.STAR)]),
        "up3_canonical": cgt.show(up3),
        "up2_positive": cgt.le(cgt.ZERO, up2) and not cgt.le(up2, cgt.ZERO),
        "up_plus_up2_equals_{up|*}": cgt.add(cgt.UP, up2) is cgt.make([cgt.UP], [cgt.STAR]),
    }
    ok, bad = True, None
    g = cgt.ZERO
    for n in range(1, 65):
        g = cgt.add(g, up2)
        if not (cgt.le(g, cgt.UP) and not cgt.le(cgt.UP, g)):
            ok, bad = False, n
            break
    res["n_up2_lt_up_for_n_1_to_64"] = ok
    res["first_failure"] = bad
    g = cgt.ZERO
    ok3 = True
    for n in range(1, 33):
        g = cgt.add(g, up3)
        if not (cgt.le(cgt.ZERO, up3) and cgt.le(g, up2) and not cgt.le(up2, g)):
            ok3 = False
            break
    res["up3_positive_and_n_up3_lt_up2_for_n_1_to_32"] = ok3
    return res, up2, up3


def denom(x):
    try:
        return Fraction(x).denominator
    except (ValueError, TypeError):
        return None


def cmd_targets(db):
    t0 = time.time()
    ups, up2, up3 = upsecond_checks()
    print(json.dumps(ups, indent=1, ensure_ascii=False))
    # uptimal lookup table: a*up + b*up^2 + c*up^3 + *m
    table = {}
    for a in range(-8, 9):
        A = mult(a, cgt.UP)
        for b in range(-4, 5):
            B = cgt.add(A, mult(b, up2))
            for c in range(-2, 3):
                C = cgt.add(B, mult(c, up3))
                for m in range(8):
                    g = cgt.add(C, cgt.nimber(m))
                    table.setdefault(g.id, (a, b, c, m))
    # tiny targets
    tiny_targets = {}
    for num in [Fraction(k, 2 ** j) for j in range(1, 5) for k in range(1, 8 * 2 ** j) if k % 2]:
        tiny_targets[tiny(cgt.number(num)).id] = f"tiny({num})"
        tiny_targets[cgt.neg(tiny(cgt.number(num))).id] = f"miny({num})"
    for n in range(0, 6):
        for a in (1, 2, -1):
            G = cgt.add(cgt.integer(n), mult(a, cgt.UP))
            tiny_targets.setdefault(tiny(G).id, f"tiny({n}+{a}up)")
            tiny_targets.setdefault(cgt.neg(tiny(G)).id, f"miny({n}+{a}up)")
    # representatives of every distinct BIG-free value string
    # Only temperature-0 non-numbers can be (number + infinitesimal): a game
    # x + e with e infinitesimal has Left stop = Right stop = x, hence
    # temperature 0 in cgt.thermograph. Hot games are skipped (counted below).
    reps = {}
    n_hot = Counter()
    for r in db:
        if r["big"] or r["num"] is not None:
            continue
        if r["temperature"] != "0":
            n_hot[r["value"]] += 1
            continue
        reps.setdefault(r["value"], []).append(r)
    found = defaultdict(list)
    collisions = []
    uptimal_summary = Counter()
    # one warm-cache pass (stock count rule, ep on): two smallest representatives per value string
    pawns._child = _ORIG_CHILD
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    for v, rs in reps.items():
        rs.sort(key=lambda r: (r["nw"] + r["nb"], r["width"], r["position"]))
        ids = set()
        G = None
        for r in rs[:2]:
            g = pawns.value(Board(r["width"], RANKS, False, True), Pos.parse(r["position"]))
            ids.add(g.id)
            G = g
        if len(ids) > 1:
            collisions.append(v)
        x = cgt.mean(G) if G.num is None else G.num
        if G.num is not None:
            continue
        H = cgt.add(G, cgt.neg(cgt.number(x)))
        exp = table.get(H.id)
        if exp is not None:
            a, b, c, m = exp
            uptimal_summary[f"x+{a}up+{b}up2+{c}up3+*{m}" if (b or c) else "number+ups+star"] += len(rs)
            if b or c:
                found["higher_ups"].append({"value": v, "x": str(x), "expansion": exp, "count": len(rs),
                                            "examples": [r["position"] + f" (w{r['width']})" for r in rs[:5]]})
            if denom(x) and denom(x) >= 8:
                found["dyadic_part_den_ge8"].append({"value": v, "count": len(rs),
                                                     "examples": [r["position"] for r in rs[:5]]})
        name = tiny_targets.get(H.id)
        if name is not None:
            found["tinies"].append({"value": v, "x": str(x), "tiny": name, "count": len(rs),
                                    "examples": [r["position"] + f" (w{r['width']})" for r in rs[:5]]})
    # numbers with denominator >= 8, means with denominator >= 8
    nums = Counter(r["num"] for r in db if r["num"] is not None)
    nums_den = {k: v for k, v in nums.items() if denom(k) >= 4}
    big8 = [r for r in db if r["num"] is not None and denom(r["num"]) >= 8]
    mean8 = Counter(r["mean"] for r in db if (not r["big"]) and r["num"] is None
                    and r["mean"] not in ("error",) and denom(r["mean"]) and denom(r["mean"]) >= 8)
    tinies_by_string = Counter(r["value"] for r in db if ("tiny(" in r["value"] or "miny(" in r["value"]))
    nimbers = Counter(r["nim"] for r in db if r["nim"] is not None)
    out = {
        "upsecond_definition_checks": ups,
        "nimber_counts": {f"*{k}" if k != 1 else "*": v for k, v in sorted(nimbers.items())},
        "nimber_ge2_positions": [r["position"] + f" (w{r['width']})" for r in db if r["nim"] and r["nim"] >= 2],
        "numbers_with_denominator_ge4": nums_den,
        "exact_value_1/8": [r["position"] for r in db if r["num"] in ("1/8", "-1/8")],
        "numbers_with_denominator_ge8": [r["position"] + f" = {r['num']}" for r in big8],
        "hot_or_other_values_with_mean_denominator_ge8": dict(mean8.most_common()),
        "tiny_miny_strings_in_db": dict(tinies_by_string),
        "found": dict(found),
        "uptimal_like_values_count": dict(uptimal_summary),
        "distinct_temperature0_nonnumber_values_examined": len(reps),
        "distinct_hot_bigfree_values_skipped": len(n_hot),
        "show_string_collisions": collisions,
        "wall_s": round(time.time() - t0, 1),
    }
    with open(os.path.join(HERE, "targets.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "upsecond_definition_checks"},
                     indent=1, ensure_ascii=False)[:6000])


# --------------------------------------------------------------------------
# checks: internal consistency
# --------------------------------------------------------------------------

def canon_key(W, white, black):
    k = (tuple(sorted(white)), tuple(sorted(black)))
    m = (tuple(sorted((W - 1 - f, r) for f, r in white)), tuple(sorted((W - 1 - f, r) for f, r in black)))
    return min(k, m)


def neg_outcome(o):
    return {"L": "R", "R": "L", "N": "N", "P": "P"}[o]


def neg_str(x):
    if x in ("number", "error", None):
        return x
    return str(-Fraction(x))


def cmd_checks(db, sample=400, seed=20261016):
    t0 = time.time()
    index = {}
    for r in db:
        p = Pos.parse(r["position"])
        index[(r["width"], canon_key(r["width"], p.white, p.black))] = r
    missing, mismatch = 0, []
    for r in db:
        p = Pos.parse(r["position"])
        W = r["width"]
        rw = {(f, RANKS + 1 - rr) for f, rr in p.black}
        rb = {(f, RANKS + 1 - rr) for f, rr in p.white}
        q = index.get((W, canon_key(W, rw, rb)))
        if q is None:
            missing += 1
            continue
        same = (q["outcome"] == neg_outcome(r["outcome"]) and q["temperature"] == r["temperature"]
                and q["mean"] == neg_str(r["mean"]) and q["nim"] == r["nim"] and q["big"] == r["big"]
                and q["num"] == (None if r["num"] is None else neg_str(r["num"])))
        if not same:
            mismatch.append((r["position"], W, r["value"], q["value"]))
    rng = random.Random(seed)
    exact_ok, exact_bad = 0, []
    for r in rng.sample(db, min(sample, len(db))):
        p = Pos.parse(r["position"])
        rw = frozenset((f, RANKS + 1 - rr) for f, rr in p.black)
        rb = frozenset((f, RANKS + 1 - rr) for f, rr in p.white)
        g, _ = cgt_value(r["width"], r["position"], "count", True)
        h, _ = cgt_value(r["width"], str(Pos(rw, rb)), "count", True)
        if cgt.neg(g) is h:
            exact_ok += 1
        else:
            exact_bad.append(r["position"])
    # outcome cross-check against crosscheck/minimax.py (single components only:
    # in sums the CGT model lets +BIG and -BIG cancel, whole-board play does not)
    singles = [r for r in db if r["n_components"] == 1]
    agree, disagree = 0, []
    for r in rng.sample(singles, min(4 * sample, len(singles))):
        b = mm.Board(r["width"], RANKS, False, True)
        oc = mm.outcome_class(b, mm.parse_position(r["position"]))
        if oc == r["outcome"]:
            agree += 1
        else:
            disagree.append((r["position"], r["width"], r["outcome"], oc))
    # same for sums, reported separately (sum_safe ones are expected to agree)
    sums = [r for r in db if r["n_components"] > 1]
    s_agree, s_dis, s_dis_unsafe = 0, 0, 0
    for r in rng.sample(sums, min(sample, len(sums))):
        b = mm.Board(r["width"], RANKS, False, True)
        oc = mm.outcome_class(b, mm.parse_position(r["position"]))
        if oc == r["outcome"]:
            s_agree += 1
        else:
            s_dis += 1
            s_dis_unsafe += (not r.get("sum_safe", True))
    out = {
        "colour_reversal_invariants": {"records": len(db), "partner_missing": missing,
                                       "mismatches": len(mismatch), "first_mismatches": mismatch[:10]},
        "colour_reversal_exact_sample": {"n": exact_ok + len(exact_bad), "ok": exact_ok, "bad": exact_bad[:10]},
        "minimax_outcome_single_components": {"n": agree + len(disagree), "agree": agree,
                                              "disagree": disagree[:10]},
        "minimax_outcome_sums": {"n": s_agree + s_dis, "agree": s_agree, "disagree": s_dis,
                                 "disagree_and_not_sum_safe": s_dis_unsafe},
        "seed": seed,
        "wall_s": round(time.time() - t0, 1),
    }
    with open(os.path.join(HERE, "checks.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


# --------------------------------------------------------------------------
# sens: single-race-node sensitivity of the known candidate
# --------------------------------------------------------------------------

def cmd_sens(db, s=CANDIDATE[0], width=CANDIDATE[1]):
    t0 = time.time()
    out = {"position": s, "width": width}
    for ep in (True, False):
        base, hits = cgt_value(width, s, "count", ep)
        keys = sorted(set(hits))
        board = Board(width, RANKS, False, ep)
        flips = []
        for k in keys:
            ps, mover = k.rsplit(" after ", 1)
            # rebuild the Pos (with ep if present) to get the count-rule winner
            m = re.search(r"\(ep ([a-z]\d+)\)", ps)
            p0 = Pos.parse(re.sub(r"\s*\(ep [a-z]\d+\)", "", ps))
            if m:
                # the ep target only matters for move generation, not for promote_distance
                pass
            w0 = count_winner(board, p0, mover)
            g, _ = cgt_value(width, s, "count", ep, override={k: "B" if w0 == "W" else "W"})
            if g is not base:
                flips.append({"race_position": k, "count_rule_winner": w0, "value_if_flipped": cgt.show(g),
                              "pawns_left": n_pawns_in(k),
                              "precapture": n_pawns_in(k) == n_pawns_in(s + " after W")})
        out[f"ep={'on' if ep else 'off'}"] = {"base_value": cgt.show(base), "distinct_race_positions": len(keys),
                                             "single_flips_that_change_value": len(flips), "flips": flips}
        print(f"ep={ep}: {len(flips)} of {len(keys)} single flips change the value", flush=True)
    out["wall_s"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, "sensitivity.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)


# --------------------------------------------------------------------------
# cert: an inclusion-minimal set of race positions that certifies the value
# --------------------------------------------------------------------------

def _bounds(width, s, ep, keep):
    """Values when races in `keep` follow the count rule and every other race
    is won by White (upper bound) / by Black (lower bound). By monotonicity of
    games in their options, every assignment of the other races (to W or B
    wins) gives a value between the two."""
    board = Board(width, RANKS, False, ep)
    out = []
    for other in ("W", "B"):
        def fn(b, p, m, other=other):
            return count_winner(b, p, m) if f"{p} after {m}" in keep else other
        try:
            pawns._child = _fixed_child(fn)
            pawns._value.cache_clear()
            pawns.race_hits.clear()
            out.append(pawns.value(board, Pos.parse(s)))
        finally:
            pawns._child = _ORIG_CHILD
            pawns._value.cache_clear()
    return out


def _pawns_style_key(pos, mover):
    """Race key in the cylcgt format, built from a crosscheck Position."""
    w = " ".join(sorted(f"{mm.FILES[f]}{r}" for f, r in pos.white))
    b = " ".join(sorted(f"{mm.FILES[f]}{r}" for f, r in pos.black))
    ep = f" (ep {mm.FILES[pos.ep[0][0]]}{pos.ep[0][1]})" if pos.ep else ""
    return f"W: {w} / B: {b}{ep} after {mover}"


def indep_cert_check(width, s, ep, keep, k):
    """Independent (crosscheck/minimax.py) check that G + *k is a P-position
    when races in `keep` follow the count rule and all others go to one side."""
    board = mm.Board(width, RANKS, False, ep)
    root = mm.parse_position(s)
    out = {}
    for fill in ("W", "B"):
        memo = {}
        seen_keys = set()

        def decide(child, mover):
            wp, bp = mm.passed_flags(board, child)
            if wp != bp:
                return "W" if wp else "B"
            if wp and bp:
                key = _pawns_style_key(child, mover)
                seen_keys.add(key)
                return mm._winner_after_move(board, child, mover) if key in keep else fill
            return None

        def win(pos, h, side):
            r = memo.get((pos, h, side))
            if r is not None:
                return r
            other = "B" if side == "W" else "W"
            res = other
            for child in mm.legal_moves(board, pos, side):
                w = decide(child, side)
                if w is None:
                    w = win(child, h, other)
                if w == side:
                    res = side
                    break
            if res != side:
                for j in range(h):
                    if win(pos, j, other) == side:
                        res = side
                        break
            memo[(pos, h, side)] = res
            return res
        # explore fully so that every race key is visited (for the key-match check)
        for h in range(k + 1):
            for side in ("W", "B"):
                win(root, h, side)
        out[f"others_to_{fill}"] = (win(root, k, "W") == "B" and win(root, k, "B") == "W")
        out[f"keep_keys_seen_{fill}"] = len(keep & seen_keys)
    return out


def cmd_cert(db, s=CANDIDATE[0], width=CANDIDATE[1]):
    t0 = time.time()
    root_n = n_pawns_in(s + " after W")
    res = {"position": s, "width": width,
           "method": "greedy removal; races tried in order precapture first, then by position string; a race is "
                     "dropped from the kept set if the value stays the same with all non-kept races given to "
                     "White and, separately, to Black"}
    for ep in (True, False):
        base, hits = cgt_value(width, s, "count", ep)
        races = sorted(set(hits), key=lambda k: (-n_pawns_in(k), k))
        keep = set(races)
        hi, lo = _bounds(width, s, ep, keep)
        assert hi is base and lo is base, "full set must reproduce the count-rule value"
        for k in races:
            trial = keep - {k}
            hi, lo = _bounds(width, s, ep, trial)
            if hi is base and lo is base:
                keep = trial
        # minimality check: removing any single kept race breaks the certificate
        minimal = all(not all(g is base for g in _bounds(width, s, ep, keep - {k})) for k in keep)
        board = Board(width, RANKS, False, ep)
        kept = []
        for k in sorted(keep):
            ps, mover = k.rsplit(" after ", 1)
            p0 = Pos.parse(re.sub(r"\s*\(ep [a-z]\d+\)", "", ps))
            kept.append({"race_position": k, "count_rule_winner": count_winner(board, p0, mover),
                         "pawns_left": n_pawns_in(k), "precapture": n_pawns_in(k) == root_n,
                         "men_in_embedding": n_pawns_in(k) + 4})
        res[f"ep={'on' if ep else 'off'}"] = {
            "value": cgt.show(base), "distinct_race_positions": len(races), "certificate_size": len(keep),
            "inclusion_minimal": minimal, "certificate": kept,
            "all_postcapture": all(not x["precapture"] for x in kept)}
        print(f"ep={ep}: value {cgt.show(base)} certified by {len(keep)} of {len(races)} race positions "
              f"(minimal={minimal}); precapture in certificate: {sum(x['precapture'] for x in kept)}", flush=True)
    res["wall_s"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, "certificate.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)


def cmd_fractions(db):
    """Robustness of every positive number with denominator >= 8 (BIG-free)
    and of the tiny(4) hit (fractions_robust.json). Negative ones are colour
    reversals of these and are not recomputed."""
    hits = [r for r in db if r["num"] is not None and not r["big"] and denom(r["num"]) >= 8
            and Fraction(r["num"]) > 0]
    hits += [r for r in db if r["value"] == "tiny(4)"]
    res = []
    for r in hits:
        T = cgt.number(Fraction(r["num"])) if r["num"] is not None else tiny(cgt.integer(4))
        label = r["num"] if r["num"] is not None else "tiny(4)"
        t = time.time()
        o = value_robustness(r["position"], r["width"], T, label)
        o["wall_s"] = round(time.time() - t, 1)
        res.append(o)
        print(f"{label:8s} w{r['width']} {r['position']}: robust={o['robust_6']} "
              f"assignment_indep={o['race_assignment_independent']} races={o['race_nodes']} "
              f"pre={o['precapture_race_nodes']} indep_ok={o['indep_all_agree']}  [{o['value_by_setting']}]",
              flush=True)
    res.sort(key=lambda o: (not o["robust_6"], o["men_with_trebuchet"], o["precapture_race_nodes"],
                            o["race_nodes"], o["target"]))
    with open(os.path.join(HERE, "fractions_robust.json"), "w") as fh:
        json.dump({"results": res}, fh, indent=1, ensure_ascii=False)


def cmd_ups(db):
    """Robustness of positive values with an up-second component other than
    exact up-second (e.g. up-second-star, up + up-second); ups_robust.json."""
    with open(os.path.join(HERE, "targets.json")) as fh:
        tg = json.load(fh)
    ups, up2, up3 = upsecond_checks()
    res = []
    for h in tg["found"]["higher_ups"]:
        a, b, c, m = h["expansion"]
        x = Fraction(h["x"])
        if b <= 0 or (a, b, c, m) == (0, 1, 0, 0):
            continue  # negatives are colour reversals; exact up-second is in values_robust.json
        T = cgt.add(cgt.add(cgt.add(cgt.number(x), mult(a, cgt.UP)), mult(b, up2)),
                    cgt.add(mult(c, up3), cgt.nimber(m)))
        assert cgt.show(T) == h["value"], (cgt.show(T), h["value"])
        label = f"{h['x']} + {a}.up + {b}.up2 + {c}.up3 + *{m}"
        for r in db:
            if r["value"] != h["value"]:
                continue
            t = time.time()
            o = value_robustness(r["position"], r["width"], T, label)
            o["wall_s"] = round(time.time() - t, 1)
            res.append(o)
            print(f"{label:28s} w{r['width']} {r['position']}: robust={o['robust_6']} races={o['race_nodes']} "
                  f"pre={o['precapture_race_nodes']} indep_ok={o['indep_all_agree']}  [{o['value_by_setting'][:200]}]",
                  flush=True)
    res.sort(key=lambda o: (not o["robust_6"], o["men_with_trebuchet"], o["precapture_race_nodes"], o["race_nodes"]))
    with open(os.path.join(HERE, "ups_robust.json"), "w") as fh:
        json.dump({"results": res}, fh, indent=1, ensure_ascii=False)


def _annotate(o):
    st = o["settings"]
    six = [st[f"{r}/ep={'on' if e else 'off'}"]["value"] for r, e in SETTINGS]
    epon = [st[f"{r}/ep=on"]["value"] for r in ("count", "mover", "opponent")]
    ext_on = [st[f"{r}/ep=on"]["value"] for r in EXTREMES]
    ext_all = [st[f"{r}/ep={e}"]["value"] for r in EXTREMES for e in ("on", "off")]
    o["robust_6"] = len(set(six)) == 1
    o["robust_ep_on_3rules"] = len(set(epon)) == 1
    o["assignment_independent_ep_on"] = len(set(epon + ext_on)) == 1
    o["race_assignment_independent"] = len(set(six + ext_all)) == 1
    o.update(pawn_legality(o["position"]))
    return o


def cmd_summary():
    """Annotate nimbers.json and *_robust.json with legality and the extra
    robustness flags, and print one ranked table (summary.json)."""
    rows = []
    for f in ("nimbers.json", "values_robust.json", "fractions_robust.json", "ups_robust.json"):
        path = os.path.join(HERE, f)
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            d = json.load(fh)
        key = "ranked" if f == "nimbers.json" else "results"
        for o in d[key]:
            _annotate(o)
            tgt = o.get("target") or ("*k" if f == "nimbers.json" else "?")
            rows.append({"file": f, "target": tgt, "position": o["position"], "width": o["width"],
                         "men_with_trebuchet": o["men_with_trebuchet"],
                         "db_value": o["settings"]["count/ep=on"]["value"],
                         "robust_6": o["robust_6"], "robust_ep_on_3rules": o["robust_ep_on_3rules"],
                         "assignment_independent_ep_on": o["assignment_independent_ep_on"],
                         "race_assignment_independent": o["race_assignment_independent"],
                         "legal8x8": o["legal_necessary_conditions"],
                         "race_nodes": o["race_nodes"], "precapture_race_nodes": o["precapture_race_nodes"],
                         "indep_all_agree": o["indep_all_agree"], "value_by_setting": o["value_by_setting"]})
        with open(path, "w") as fh:
            json.dump(d, fh, indent=1, ensure_ascii=False)
    rows.sort(key=lambda r: (not r["robust_6"], not r["robust_ep_on_3rules"], not r["legal8x8"],
                             r["men_with_trebuchet"], r["precapture_race_nodes"], r["race_nodes"]))
    with open(os.path.join(HERE, "summary.json"), "w") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=False)
    for r in rows:
        print(f"{r['target'][:18]:18s} w{r['width']} {r['position']:28s} men={r['men_with_trebuchet']} "
              f"r6={int(r['robust_6'])} rEP={int(r['robust_ep_on_3rules'])} "
              f"aiEP={int(r['assignment_independent_ep_on'])} ai={int(r['race_assignment_independent'])} "
              f"legal={int(r['legal8x8'])} races={r['race_nodes']} pre={r['precapture_race_nodes']} "
              f"indep={int(r['indep_all_agree'])}")


def embedding_fen(s, side="w"):
    """FEN of the proposed 8x8 embedding: component on files a-d, file e
    empty, trebuchet W Pg4 / B Pg5 with WK f5 and BK h4."""
    p = Pos.parse(s)
    board = {}
    for f, r in p.white:
        board[(f, r)] = "P"
    for f, r in p.black:
        board[(f, r)] = "p"
    board.update({(6, 4): "P", (6, 5): "p", (5, 5): "K", (7, 4): "k"})
    rows = []
    for r in range(8, 0, -1):
        row, gap = "", 0
        for f in range(8):
            c = board.get((f, r))
            if c is None:
                gap += 1
            else:
                row += (str(gap) if gap else "") + c
                gap = 0
        rows.append(row + (str(gap) if gap else ""))
    return "/".join(rows) + f" {side} - - 0 1"


def cmd_legality():
    """Add field legal8x8 (pawn_legality necessary conditions for the 8x8
    embedding with the g-file trebuchet) to every record of values.jsonl."""
    path = os.path.join(HERE, "values.jsonl")
    tmp = path + ".tmp"
    n = bad = 0
    with open(path) as fi, open(tmp, "w") as fo:
        for line in fi:
            r = json.loads(line)
            r["legal8x8"] = pawn_legality(r["position"])["legal_necessary_conditions"]
            n += 1
            bad += not r["legal8x8"]
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)
    print(f"{n} records, {bad} fail the 8x8 pawn-structure conditions")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "legality":
        cmd_legality()
        sys.exit(0)
    if cmd == "summary":
        cmd_summary()
        sys.exit(0)
    if cmd == "fractions":
        cmd_fractions(load_db())
        sys.exit(0)
    if cmd == "ups":
        cmd_ups(load_db())
        sys.exit(0)
    db = load_db()
    if cmd in ("robust", "all"):
        cmd_robust(db)
    if cmd in ("targets", "all"):
        cmd_targets(db)
    if cmd in ("values", "all"):
        cmd_values(db)
    if cmd in ("checks", "all"):
        cmd_checks(db)
    if cmd in ("sens", "all"):
        cmd_sens(db)
    if cmd in ("cert", "all"):
        cmd_cert(db)
    if cmd in ("certcheck", "cert", "all"):
        # independent re-check of certificate.json with crosscheck/minimax.py
        path = os.path.join(HERE, "certificate.json")
        with open(path) as fh:
            cert = json.load(fh)
        for key in ("ep=on", "ep=off"):
            c = cert[key]
            keep = {x["race_position"] for x in c["certificate"]}
            k = 2 if c["value"] == "*2" else None
            c["indep_check"] = indep_cert_check(cert["width"], cert["position"], key == "ep=on", keep, k)
            print(key, c["indep_check"], flush=True)
        with open(path, "w") as fh:
            json.dump(cert, fh, indent=1, ensure_ascii=False)
