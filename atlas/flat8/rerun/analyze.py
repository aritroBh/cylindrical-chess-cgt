#!/usr/bin/env python3
"""Analyses for workstream A2-search (rerun 2026-10-16).

  census   compare the C census (census.tsv, independent rules code) with a cylcgt
           database (outcome + nimber columns) and list every *k, k >= 2, under
           any of the 9 settings
  robust   cylcgt values of the nimber candidates under count/mover/opponent x
           e.p. on/off (project cylcgt, textbook passed test) plus, in a
           subprocess, the e.p.-aware variant; race-node counts
  targets  Elkies' 8x8 open targets in the database (nimbers, dyadics with
           denominator >= 8, up-second family, fractional tinies)
  upsecond definition checks for up-second with cgt.le

Run from the project root with PYTHONPATH=. (see REPRODUCE lines in the output).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from enumerate import norm_show  # noqa: E402  (order-normalised cgt.show)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CANDIDATE = "W: a2 c2 / B: b7 d7"
SETTINGS6 = [(r, ep) for r in ("count", "mover", "opponent") for ep in (True, False)]


# ------------------------------------------------------------------ helpers
def parse(s):
    w, b = s.split("/")
    W = [(ord(t[0]) - 97, int(t[1:])) for t in w.split(":")[1].split()]
    B = [(ord(t[0]) - 97, int(t[1:])) for t in b.split(":")[1].split()]
    return W, B


def fmt(W, B):
    n = lambda s: f"{chr(97 + s[0])}{s[1]}"
    return "W: " + " ".join(sorted(map(n, W))) + " / B: " + " ".join(sorted(map(n, B)))


def mirror(s, width):
    W, B = parse(s)
    return fmt([(width - 1 - f, r) for f, r in W], [(width - 1 - f, r) for f, r in B])


def norm(s, width):
    return min(s, mirror(s, width))


def colour_reverse(s, width):
    """Swap colours and flip ranks (r -> 9 - r): value becomes -G."""
    W, B = parse(s)
    return fmt([(f, 9 - r) for f, r in B], [(f, 9 - r) for f, r in W])


def load_db(path):
    db = {}
    with open(path) as fh:
        for line in fh:
            r = json.loads(line)
            db[norm(r["position"], r["width"])] = r
    return db


def load_census(path):
    rows = {}
    with open(path) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        names = header[3:]
        for line in fh:
            p = line.rstrip("\n").split("\t")
            width = int(p[1])
            vals = {}
            for nm, cell in zip(names, p[3:]):
                o, k = cell.split(",")
                vals[nm] = (o, int(k))
            rows[norm(p[0], width)] = {"position": p[0], "width": width, "npawns": int(p[2]), "s": vals}
    return names, rows


# ------------------------------------------------------------------ census
def cmd_census(args):
    names, cen = load_census(args.census)
    out = {"census_file": args.census, "n_roots": len(cen), "settings": names}
    # nimber counts per setting
    out["nimber_counts"] = {nm: dict(sorted(Counter(r["s"][nm][1] for r in cen.values() if r["s"][nm][1] >= 0).items()))
                            for nm in names}
    out["outcome_counts"] = {nm: dict(sorted(Counter(r["s"][nm][0] for r in cen.values()).items())) for nm in names}
    hi = []
    for key, r in sorted(cen.items()):
        ks = {nm: r["s"][nm][1] for nm in names}
        if any(k >= 2 for k in ks.values()):
            hi.append({"position": r["position"], "width": r["width"], "npawns": r["npawns"], "nim_by_setting": ks})
    out["nimbers_k_ge_2_any_setting"] = hi
    # comparisons with cylcgt databases
    comps = {}
    for label, path, col in [("rerun_textbook_count_epon", args.db, "count/epon"),
                             ("prior_textbook_count_epon", args.prior, "count/epon"),
                             ("parent_aware_count_epon", args.aware, "count/epon/aware")]:
        if not path or not os.path.exists(path):
            comps[label] = "missing"
            continue
        db = load_db(path)
        only_db = [k for k in db if k not in cen]
        only_cen = [k for k in cen if k not in db]
        common = [k for k in db if k in cen]
        o_bad = [k for k in common if db[k]["outcome"] != cen[k]["s"][col][0]]

        def dbnim(r):
            return -1 if r["nim"] is None or r["nim"] >= 16 else r["nim"]
        n_bad = [k for k in common if dbnim(db[k]) != cen[k]["s"][col][1]]
        comps[label] = {"path": path, "db_records": len(db), "common": len(common),
                        "only_in_db": len(only_db), "only_in_census": len(only_cen),
                        "only_in_census_examples": only_cen[:5], "only_in_db_examples": only_db[:5],
                        "outcome_mismatch": len(o_bad), "outcome_mismatch_examples": o_bad[:10],
                        "nim_mismatch": len(n_bad), "nim_mismatch_examples": n_bad[:10]}
    out["comparisons"] = comps
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "nimbers_k_ge_2_any_setting"}, indent=1, ensure_ascii=False))
    print("nimbers k>=2 under some setting:")
    for h in hi:
        print("  ", h["position"], h["width"], h["nim_by_setting"])


# ------------------------------------------------------------------ robust
def _race_stats(pawns, cgt, board, pos):
    """value, race edges, distinct race positions, and the same restricted to
    race positions reached before any capture (all root pawns still present)."""
    pawns._value.cache_clear()
    pawns.race_hits.clear()
    g = pawns.value(board, pos)
    n0 = len(pos.white) + len(pos.black)
    hits = list(pawns.race_hits)
    def npawns(h):
        body = h.rsplit(" after ", 1)[0].split(" (ep")[0]
        W, B = parse(body)
        return len(W) + len(B)
    pre = [h for h in hits if npawns(h) == n0]
    distinct = {h.rsplit(" after ", 1)[0] for h in hits}
    distinct_pre = {h.rsplit(" after ", 1)[0] for h in pre}
    return g, {"race_edges": len(hits), "race_positions": len(distinct),
               "race_position_mover_pairs": len(set(hits)),
               "precapture_race_edges": len(pre), "precapture_race_positions": len(distinct_pre),
               "precapture_race_position_mover_pairs": len(set(pre))}


def robust_values(positions, width_of, settings=SETTINGS6):
    from cylcgt import cgt, pawns
    res = {}
    for p in positions:
        W = width_of[p]
        pos = pawns.Pos.parse(p)
        row = {}
        for rule, ep in settings:
            pawns.RACE_RULE = rule
            board = pawns.Board(W, 8, False, ep)
            g, st = _race_stats(pawns, cgt, board, pos)
            row[f"{rule}/{'epon' if ep else 'epoff'}"] = {"value": cgt.show(g), "nim": g.nim, **st}
        pawns.RACE_RULE = "count"
        pawns._value.cache_clear()
        res[p] = row
    return res


def cmd_robust_worker(args):
    """Runs inside a subprocess; prints JSON of robust_values for args.positions."""
    items = json.loads(args.items)
    settings = [(r, e == "on") for r, e in (s.split("/") for s in args.settings.split(","))]
    res = robust_values([p for p, _ in items], {p: w for p, w in items}, settings)
    if args.aware_check:
        from cylcgt import pawns
        res["_module"] = {"file": pawns.__file__, "PASSED_RESPECTS_EP": getattr(pawns, "PASSED_RESPECTS_EP", None)}
    print(json.dumps(res, ensure_ascii=False))


def cmd_robust(args):
    items = {}
    if not args.only_extra:
        with open(args.census_json) as fh:
            cen = json.load(fh)
        items[CANDIDATE] = 4
        for h in cen["nimbers_k_ge_2_any_setting"]:
            items[h["position"]] = h["width"]
    for extra in (args.extra or []):
        p, w = extra.rsplit("@", 1)
        items[p] = int(w)
    if args.targets_json:
        with open(args.targets_json) as fh:
            tj = json.load(fh)
        cand = {}
        for v, d in tj["dyadic_numbers_den_ge_8"].items():
            for p in d["positions"]:
                cand[p] = None
        for v, conf in tj["upsecond_and_tiny_targets"].items():
            for c in conf:
                cand[c["position"]] = c["width"]
        with open(args.db) as fh:
            for line in fh:
                r = json.loads(line)
                if r["position"] in cand and cand[r["position"]] is None:
                    cand[r["position"]] = r["width"]
        # colour reversal gives -G under every setting; keep one of each pair
        kept = set()
        for p, w in sorted(cand.items()):
            k, kr = norm(p, w), norm(colour_reverse(p, w), w)
            if kr in kept:
                continue
            kept.add(k)
            items[p] = w
    items = sorted(items.items())
    t0 = time.time()
    env = dict(os.environ, PYTHONPATH=ROOT)
    proj = subprocess.run([sys.executable, __file__, "robust-worker", "--items", json.dumps(items),
                           "--settings", "count/on,count/off,mover/on,mover/off,opponent/on,opponent/off"],
                          capture_output=True, text=True, env=env, cwd=ROOT, check=True)
    textbook = json.loads(proj.stdout)
    aware = None
    if args.aware_root:
        env2 = dict(os.environ, PYTHONPATH=args.aware_root)
        aw = subprocess.run([sys.executable, __file__, "robust-worker", "--items", json.dumps(items),
                             "--settings", "count/on,mover/on,opponent/on", "--aware-check"],
                            capture_output=True, text=True, env=env2, cwd=args.aware_root, check=True)
        aware = json.loads(aw.stdout)
    # census cross-check for each setting
    _, crows = load_census(args.census)
    out = []
    for p, w in items:
        tb = textbook[p]
        cr = crows[norm(p, w)]["s"]
        nims = {s: v["nim"] for s, v in tb.items()}
        ks = set(nims.values())
        robust = len(ks) == 1 and None not in ks and next(iter(ks)) >= 2
        npawns = sum(len(x) for x in parse(p))
        agree = {s: (cr[s][1] == (-1 if v["nim"] is None else v["nim"])) for s, v in tb.items()}
        row = {"position": p, "width": w, "npawns": npawns, "men_with_trebuchet": npawns + 4,
               "textbook": tb, "robust_textbook_6": robust, "census_agrees_textbook": agree}
        if aware:
            row["aware"] = {s: v for s, v in aware[p].items()}
            row["census_agrees_aware"] = {s: (cr[s + "/aware"][1] == (-1 if v["nim"] is None else v["nim"]))
                                          for s, v in aware[p].items()}
        out.append(row)
    res = {"rows": out, "aware_module": aware.get("_module") if aware else None, "wall_s": round(time.time() - t0, 1)}
    with open(args.out, "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    for r in out:
        print(r["position"], "w", r["width"], "men", r["men_with_trebuchet"], "robust6", r["robust_textbook_6"])
        for s, v in r["textbook"].items():
            print(f"   textbook {s:13s} {v['value']:>22s}  race {v['race_edges']}/{v['race_positions']}"
                  f"  precap {v['precapture_race_edges']}/{v['precapture_race_positions']}  census-agree {r['census_agrees_textbook'][s]}")
        if aware:
            for s, v in r["aware"].items():
                print(f"   aware    {s:13s} {v['value']:>22s}  race {v['race_edges']}/{v['race_positions']}"
                      f"  precap {v['precapture_race_edges']}/{v['precapture_race_positions']}  census-agree {r['census_agrees_aware'][s]}")
    print("aware module:", res["aware_module"])


# ------------------------------------------------------------------ targets
def target_games():
    from cylcgt import cgt
    Z, S, U, D = cgt.ZERO, cgt.STAR, cgt.UP, cgt.DOWN
    up2 = cgt.make([Z], [cgt.add(D, S)])                  # {0 | v*}
    up3 = cgt.make([Z], [cgt.add(cgt.add(D, cgt.neg(up2)), S)])  # {0 | * - up - up2}
    T = {}
    def put(g, name):
        T.setdefault(g.id, (g, name))
    # up-second family: a.up + b.up2 + c.up3 (+ *), b or c nonzero
    for a in range(-3, 4):
        for b in range(-3, 4):
            for c in range(-1, 2):
                if b == 0 and c == 0:
                    continue
                g = cgt.ZERO
                for _ in range(abs(a)):
                    g = cgt.add(g, U if a > 0 else D)
                for _ in range(abs(b)):
                    g = cgt.add(g, up2 if b > 0 else cgt.neg(up2))
                for _ in range(abs(c)):
                    g = cgt.add(g, up3 if c > 0 else cgt.neg(up3))
                for st in (0, 1):
                    h = cgt.add(g, S) if st else g
                    nm = []
                    if a: nm.append(f"{a}.up")
                    if b: nm.append(f"{b}.up2")
                    if c: nm.append(f"{c}.up3")
                    put(h, "+".join(nm) + ("+*" if st else ""))
    # tiny(x) / miny(x) for non-integer x, and for x = 1+up, 1*, up
    def tiny(G):
        return cgt.make([Z], [cgt.make([Z], [cgt.neg(G)])])
    xs = [Fraction(k, 2 ** j) for j in range(1, 5) for k in range(1, 8 * 2 ** j) if k % 2]
    for x in xs:
        g = tiny(cgt.number(x))
        put(g, f"tiny({x})")
        put(cgt.neg(g), f"miny({x})")
    # (tiny(up) is omitted: {0 || 0 | down} is canonically equal to up itself)
    for G, nm in [(cgt.add(cgt.integer(1), U), "1+up"), (cgt.add(cgt.integer(1), S), "1*"),
                  (cgt.add(cgt.integer(1), D), "1+down"), (cgt.add(cgt.integer(2), U), "2+up"),
                  (cgt.add(cgt.integer(2), S), "2*")]:
        g = tiny(G)
        put(g, f"tiny({nm})")
        put(cgt.neg(g), f"miny({nm})")
    return T, up2, up3


def cmd_targets(args):
    from cylcgt import cgt, pawns
    T, up2, up3 = target_games()
    by_show = {}
    for gid, (g, nm) in T.items():
        by_show.setdefault(norm_show(cgt.show(g)), []).append((g, nm))
    hits = defaultdict(list)
    dyadic = defaultdict(list)
    nims = defaultdict(list)
    tinies_int = Counter()
    n = 0
    with open(args.db) as fh:
        for line in fh:
            r = json.loads(line)
            n += 1
            v = r["value"]
            if r["nim"] is not None and r["nim"] >= 2:
                nims[f"*{r['nim']}"].append(r["position"])
            if r["num"] is not None:
                x = Fraction(r["num"])
                if x.denominator >= 8 and abs(x) < 128:  # |x| >= 128 involves BIG
                    dyadic[str(x)].append(r["position"])
            v = norm_show(v)
            if v in by_show:
                hits[v].append((r["position"], r["width"]))
            m = re.fullmatch(r"(tiny|miny)\((-?\d+)\)", v)
            if m:
                tinies_int[v] += 1
    # each hit: the database's (order-normalised) show string equals show(T) for a
    # BIG-free target T. Optional: recompute in cylcgt and test identity (slow);
    # the default independent confirmation is `gtest`, which runs the C solver on
    # G + (-T) under all 9 settings.
    confirmed = {}
    for v, plist in hits.items():
        conf = []
        for p, w in plist:
            names = [nm for (t, nm) in by_show[v]]
            if args.recompute:
                pawns._value.cache_clear()
                g = pawns.value(pawns.Board(w, 8, False, True), pawns.Pos.parse(p))
                names = [nm for (t, nm) in by_show[v] if t is g]
            conf.append({"position": p, "width": w, "equal_to": names, "recomputed": bool(args.recompute)})
        confirmed[v] = conf
    out = {"db": args.db, "records": n,
           "nimbers_k_ge_2": {k: v for k, v in nims.items()},
           "dyadic_numbers_den_ge_8": {k: {"count": len(v), "positions": v} for k, v in
                                       sorted(dyadic.items(), key=lambda kv: (Fraction(kv[0]).denominator, Fraction(kv[0])))},
           "upsecond_and_tiny_targets": confirmed,
           "integer_tiny_miny_counts": dict(tinies_int),
           "targets_searched": sorted({nm for _, nm in T.values()})}
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print("records", n)
    print("nimbers k>=2:", {k: len(v) for k, v in nims.items()}, {k: v[:4] for k, v in nims.items()})
    print("dyadics den>=8:", {k: v["count"] for k, v in out["dyadic_numbers_den_ge_8"].items()})
    for v, conf in confirmed.items():
        print(f"target {v}: {len(conf)} positions; names {sorted({n for c in conf for n in c['equal_to']})}")
        for c in conf[:6]:
            print("    ", c["position"], "w", c["width"], c["equal_to"])
    print("integer tiny/miny:", dict(tinies_int))


# ------------------------------------------------------------------ gtest
def dag_of(g):
    """Explicit DAG of a canonical game: list of (left indices, right indices)."""
    idx, order = {}, []
    def visit(x):
        if x.id in idx:
            return idx[x.id]
        idx[x.id] = len(order)
        order.append(x)
        for y in x.L + x.R:
            visit(y)
        return idx[x.id]
    visit(g)
    return [([idx[y.id] for y in x.L], [idx[y.id] for y in x.R]) for x in order]


def cmd_gtest(args):
    """Second-implementation check of exact values: for each (position, claimed
    value T) run the C solver on G + (-T) under all 9 settings and compare with
    cylcgt's value under each setting (from the robust JSON files)."""
    from cylcgt import cgt
    T, up2, up3 = target_games()
    name_to_game = {nm: g for g, nm in T.values()}
    for k in range(2, 8):
        name_to_game[f"*{k}"] = cgt.nimber(k)
    for x in ("1/8", "-1/8", "1/16", "-1/16", "1/32", "-1/32", "3/8", "-3/8", "5/8", "-5/8"):
        name_to_game[x] = cgt.number(Fraction(x))
    rows = []
    for path in args.robust:
        with open(path) as fh:
            rows += json.load(fh)["rows"]
    if args.targets_json:
        # database hits: cylcgt value known only for count / e.p. on (textbook)
        with open(args.targets_json) as fh:
            tj = json.load(fh)
        width = {}
        want = {p for d in tj["dyadic_numbers_den_ge_8"].values() for p in d["positions"]}
        with open(args.db) as fh:
            for line in fh:
                r = json.loads(line)
                if r["position"] in want:
                    width[r["position"]] = r["width"]
        for v, d in tj["dyadic_numbers_den_ge_8"].items():
            for p in d["positions"]:
                rows.append({"position": p, "width": width[p], "textbook": {"count/epon": {"value": v}}})
        for v, conf in tj["upsecond_and_tiny_targets"].items():
            for c in conf:
                rows.append({"position": c["position"], "width": c["width"], "textbook": {"count/epon": {"value": v}}})
    tests = []
    for r in rows:
        claimed = set()
        for part in ("textbook", "aware"):
            for s, v in r.get(part, {}).items():
                claimed.add(v["value"])
        for v in sorted(claimed):
            g = None
            for nm, t in name_to_game.items():
                if norm_show(cgt.show(t)) == norm_show(v):
                    g, gname = t, nm
                    break
            if g is None:
                continue
            tests.append((r, gname, g))
    path = os.path.join(HERE, "gtest_input.tsv")
    with open(path, "w") as fh:
        for r, gname, g in tests:
            dag = dag_of(cgt.neg(g))
            fh.write(f"{r['position']}\t{r['width']}\t" + ";".join(",".join(map(str, L)) + "|" + ",".join(map(str, R))
                                                           for L, R in dag) + "\n")
    out = subprocess.run([os.path.join(HERE, "nimscan"), "--test", path], capture_output=True, text=True, check=True)
    lines = out.stdout.strip().split("\n")
    header = lines[0].split("\t")[2:]
    res = []
    n_agree = n_total = 0
    for (r, gname, g), line in zip(tests, lines[1:]):
        p = line.split("\t")
        assert p[0] == r["position"], (p[0], r["position"])
        c_equal = dict(zip(header, (x == "EQUAL" for x in p[2:])))
        cy_equal = {}
        for s, v in r["textbook"].items():
            cy_equal[s] = norm_show(v["value"]) == norm_show(cgt.show(g))
        for s, v in r.get("aware", {}).items():
            cy_equal[s + "/aware"] = norm_show(v["value"]) == norm_show(cgt.show(g))
        agree = {s: c_equal[s] == cy_equal[s] for s in cy_equal}
        n_total += len(agree)
        n_agree += sum(agree.values())
        res.append({"position": r["position"], "width": r["width"], "target": gname,
                    "C_equal": c_equal, "cylcgt_equal": cy_equal, "all_agree": all(agree.values())})
    with open(args.out, "w") as fh:
        json.dump({"tests": res, "agree": n_agree, "total": n_total}, fh, indent=1, ensure_ascii=False)
    for x in res:
        eq = [s for s, b in x["C_equal"].items() if b]
        print(f"{x['position']:32s} w{x['width']} = {x['target']:14s} C-equal in {len(eq)}/{len(x["C_equal"])}: {eq}  agree-with-cylcgt {x['all_agree']}")
    print(f"setting-level agreement C vs cylcgt: {n_agree}/{n_total}")


# ------------------------------------------------------------------ reachability
def _min_captures(pawns_, white):
    """Minimum total pawn captures to bring these pawns from distinct start files
    (each capture moves one file and one rank), or None if impossible.
    Necessary conditions only: no check of pawns passing each other."""
    from itertools import permutations
    best = None
    for starts in permutations(range(8), len(pawns_)):
        tot = 0
        for (f, r), f0 in zip(pawns_, starts):
            need = abs(f - f0)
            adv = (r - 2) if white else (7 - r)
            if need > adv:
                break
            tot += need
        else:
            best = tot if best is None else min(best, tot)
    return best


def reach_check(position, width):
    """Necessary conditions for the 8x8 embedding (trebuchet W g4 / B g5, kings f5/h4,
    file e empty): try every placement of the component on files a-d and both mirror
    images. Returns the list of placements that pass."""
    W0, B0 = parse(position)
    ok = []
    for mir in (False, True):
        for off in range(0, 4 - width + 1):
            Wp = [((width - 1 - f if mir else f) + off, r) for f, r in W0] + [(6, 4)]
            Bp = [((width - 1 - f if mir else f) + off, r) for f, r in B0] + [(6, 5)]
            cw, cb = _min_captures(Wp, True), _min_captures(Bp, False)
            if cw is None or cb is None:
                continue
            missing_black = 16 - (len(Bp) + 1)
            missing_white = 16 - (len(Wp) + 1)
            if cw <= missing_black and cb <= missing_white:
                ok.append({"mirror": mir, "offset": off, "white": fmt([q for q in Wp if q != (6, 4)], []).split(" / ")[0],
                           "black": fmt([], [q for q in Bp if q != (6, 5)]).split(" / ")[1],
                           "white_pawn_captures": cw, "black_pawn_captures": cb})
    return ok


def cmd_reach(args):
    with open(args.gtest) as fh:
        gt = json.load(fh)
    seen = {}
    for t in gt["tests"]:
        seen[(t["position"], t["width"])] = t["target"]
    out = []
    for (p, w), tgt in sorted(seen.items(), key=lambda kv: kv[1]):
        ok = reach_check(p, w)
        rep = [x for x in ok if not x["mirror"] and x["offset"] == 0]
        placed = ok[0] if ok else None
        out.append({"position": p, "width": w, "target": tgt, "representative_at_files_a_passes": bool(rep),
                    "passing_placements": ok,
                    "fen_white_to_move": fen(placed["white"] + " / " + placed["black"]) if placed else None})
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    for x in out:
        pl = x["passing_placements"]
        print(f"{x['target']:16s} {x['position']:32s} rep-ok {x['representative_at_files_a_passes']!s:5s} "
              f"placements-ok {len(pl)}  e.g. {pl[0]['white'] + ' / ' + pl[0]['black'] if pl else '-'}  {x['fen_white_to_move'] or ''}")


# ------------------------------------------------------------------ nimbers.json
def fen(position, to_move="w"):
    """8x8 embedding: component on files a.. (file e empty), trebuchet W g4 / B g5,
    WK f5, BK h4."""
    W, B = parse(position)
    board = {}
    for f, r in W:
        board[(f, r)] = "P"
    for f, r in B:
        board[(f, r)] = "p"
    board[(5, 5)] = "K"; board[(6, 4)] = "P"; board[(6, 5)] = "p"; board[(7, 4)] = "k"
    rows = []
    for r in range(8, 0, -1):
        s, e = "", 0
        for f in range(8):
            c = board.get((f, r))
            if c is None:
                e += 1
            else:
                s += (str(e) if e else "") + c
                e = 0
        rows.append(s + (str(e) if e else ""))
    return "/".join(rows) + f" {to_move} - - 0 1"


def cmd_nimbers(args):
    with open(args.census_json) as fh:
        cen = json.load(fh)
    with open(args.robust) as fh:
        rob = json.load(fh)
    with open(args.gtest) as fh:
        gt = json.load(fh)
    rows = []
    for r in rob["rows"]:
        tb, aw = r["textbook"], r.get("aware", {})
        k_by = {s: v["nim"] for s, v in tb.items()}
        ks = [k for k in k_by.values() if k is not None and k >= 2]
        n_textbook = len(ks)
        n_aware = sum(1 for v in aw.values() if v["nim"] is not None and v["nim"] >= 2)
        c = tb["count/epon"]
        rows.append({
            "position": r["position"], "width": r["width"], "npawns": r["npawns"],
            "men_with_trebuchet": r["men_with_trebuchet"],
            "fen_white_to_move": fen(r["position"], "w"), "fen_black_to_move": fen(r["position"], "b"),
            "value_by_setting_textbook": {s: v["value"] for s, v in tb.items()},
            "value_by_setting_ep_aware": {s: v["value"] for s, v in aw.items()},
            "settings_with_nimber_k_ge_2": {"textbook_of_6": n_textbook, "ep_aware_of_3": n_aware},
            "robust_all_6_textbook": r["robust_textbook_6"],
            "race_nodes_count_epon": {k: c[k] for k in c if k.startswith("race") or k.startswith("precapture")},
            "race_nodes_by_setting": {s: {k: v[k] for k in v if k.startswith("race") or k.startswith("precapture")}
                                      for s, v in list(tb.items()) + [(s + "/aware", v) for s, v in aw.items()]},
            "C_census_agrees": {**r["census_agrees_textbook"], **{s + "/aware": b for s, b in r.get("census_agrees_aware", {}).items()}},
        })
    rows.sort(key=lambda x: (not x["robust_all_6_textbook"], x["men_with_trebuchet"],
                             x["race_nodes_count_epon"]["precapture_race_edges"],
                             -(x["settings_with_nimber_k_ge_2"]["textbook_of_6"] + x["settings_with_nimber_k_ge_2"]["ep_aware_of_3"]),
                             x["position"]))
    out = {
        "scope": "flat 8-rank boards, widths 1-4, pawns on ranks 2-7, w,b >= 1, w+b <= 6 (all widths), "
                 "no passed pawn at the root; 231,071 canonical positions (459,443 board positions)",
        "nimber_census_by_setting_C": cen["nimber_counts"],
        "census_vs_cylcgt": cen["comparisons"],
        "nimbers_k_ge_2_any_setting": rows,
        "ranking": "robust under all 6 textbook settings first (none is), then fewest men, then fewest "
                   "pre-capture race edges (count rule, e.p. on), then most settings giving *k",
        "gtest_agreement": f"{gt['agree']}/{gt['total']}",
        "notes": [
            "textbook = cylcgt/pawns.py on disk (a pawn that can still be taken e.p. counts as passed)",
            "ep_aware = the PASSED_RESPECTS_EP variant in the parent session's worktree "
            "(scratchpad/ep-wt/cylcgt/pawns.py), run read-only",
            "race_edges = len(pawns.race_hits) from a cold cache; race_position_mover_pairs counts distinct "
            "(position, mover) pairs (the prior report's 'distinct positions'); precapture = all root pawns still on the board",
            "no *k with k >= 3 occurs under any of the 9 settings (the C census tests k <= 15)",
        ],
    }
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    for x in rows:
        print(x["position"], x["men_with_trebuchet"], x["settings_with_nimber_k_ge_2"], x["race_nodes_count_epon"], x["fen_white_to_move"])


# ------------------------------------------------------------------ upsecond
def cmd_upsecond(args):
    from cylcgt import cgt
    Z, S, U, D = cgt.ZERO, cgt.STAR, cgt.UP, cgt.DOWN
    up2 = cgt.make([Z], [cgt.add(D, S)])
    lt = lambda a, b: cgt.le(a, b) and not cgt.le(b, a)
    checks = {}
    checks["up2_canonical_show"] = cgt.show(up2)
    checks["up2 > 0"] = lt(Z, up2)
    checks["up2 < up"] = lt(up2, U)
    checks["up2 != double-up (up+up)"] = up2 is not cgt.add(U, U)
    # Siegel/CGSuite: G^{->n} = {G^{->(n-1)} | H}; G^n = {0 | H - G^{->(n-1)}} for G = {0|H}, H = *
    upto2 = cgt.make([U], [S])
    checks["up + up2 == {up | *} (= up^{->2})"] = cgt.add(U, up2) is upto2
    up3 = cgt.make([Z], [cgt.add(S, cgt.neg(upto2))])
    checks["up3 == {0 | * - up^{->2}} is positive"] = lt(Z, up3)
    checks["up3 < up2"] = lt(up3, up2)
    nmax = args.nmax
    g = Z
    ok = True
    first_fail = None
    for n in range(1, nmax + 1):
        g = cgt.add(g, up2)
        if not lt(g, U):
            ok, first_fail = False, n
            break
    checks[f"n.up2 < up for n = 1..{nmax}"] = ok
    checks["first n with n.up2 >= up"] = first_fail
    # up2 is infinitesimal: below every positive number tested
    checks["up2 < 2^-k for k = 0..20"] = all(lt(up2, cgt.number(Fraction(1, 2 ** k))) for k in range(21))
    checks["up2 + * == {0, * | down}"] = cgt.add(up2, S) is cgt.make([Z, S], [D])
    checks["up2 is fuzzy with *"] = cgt.add(up2, S).fuzzy(Z) if hasattr(cgt.Game, "fuzzy") else None
    for k, v in checks.items():
        print(f"{k}: {v}")
    if args.out:
        with open(args.out, "w") as fh:
            json.dump(checks, fh, indent=1, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("census")
    c.add_argument("--census", default=os.path.join(HERE, "census.tsv"))
    c.add_argument("--db", default=os.path.join(HERE, "values.jsonl"))
    c.add_argument("--prior", default=os.path.join(HERE, "..", "values.jsonl"))
    c.add_argument("--aware", default=os.path.join(HERE, "..", "values_aware.jsonl"))
    c.add_argument("--out", default=os.path.join(HERE, "census_summary.json"))
    r = sub.add_parser("robust")
    r.add_argument("--census-json", default=os.path.join(HERE, "census_summary.json"))
    r.add_argument("--census", default=os.path.join(HERE, "census.tsv"))
    r.add_argument("--aware-root")
    r.add_argument("--extra", nargs="*")
    r.add_argument("--only-extra", action="store_true")
    r.add_argument("--targets-json")
    r.add_argument("--db", default=os.path.join(HERE, "values.jsonl"))
    r.add_argument("--out", default=os.path.join(HERE, "robust.json"))
    rw = sub.add_parser("robust-worker")
    rw.add_argument("--items", required=True)
    rw.add_argument("--settings", required=True)
    rw.add_argument("--aware-check", action="store_true")
    t = sub.add_parser("targets")
    t.add_argument("--db", default=os.path.join(HERE, "values.jsonl"))
    t.add_argument("--out", default=os.path.join(HERE, "targets.json"))
    t.add_argument("--recompute", action="store_true")
    gt = sub.add_parser("gtest")
    gt.add_argument("--robust", nargs="*", default=[os.path.join(HERE, "robust.json")])
    gt.add_argument("--targets-json")
    gt.add_argument("--db", default=os.path.join(HERE, "values.jsonl"))
    gt.add_argument("--out", default=os.path.join(HERE, "gtest.json"))
    rc = sub.add_parser("reach")
    rc.add_argument("--gtest", default=os.path.join(HERE, "gtest.json"))
    rc.add_argument("--out", default=os.path.join(HERE, "reach.json"))
    nb = sub.add_parser("nimbers")
    nb.add_argument("--census-json", default=os.path.join(HERE, "census_summary.json"))
    nb.add_argument("--robust", default=os.path.join(HERE, "robust.json"))
    nb.add_argument("--gtest", default=os.path.join(HERE, "gtest.json"))
    nb.add_argument("--out", default=os.path.join(HERE, "nimbers.json"))
    u = sub.add_parser("upsecond")
    u.add_argument("--nmax", type=int, default=64)
    u.add_argument("--out", default=os.path.join(HERE, "upsecond_checks.json"))
    args = ap.parse_args()
    {"census": cmd_census, "robust": cmd_robust, "robust-worker": cmd_robust_worker,
     "targets": cmd_targets, "upsecond": cmd_upsecond, "gtest": cmd_gtest,
     "nimbers": cmd_nimbers, "reach": cmd_reach}[args.cmd](args)


if __name__ == "__main__":
    main()
