"""Build the CGT-vs-tablebase verified EPD suite.

Stages (each reproducible; network only in `probe`):

    cd /Users/aritro/Downloads/Research/Chessendgames
    PYTHONPATH=. .venv/bin/python engine/suite/gen_candidates.py          # CGT predictions
    PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py select      # -> selection.json
    PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py probe       # Lichess (round 1)
    PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py report      # writes results.json
    PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py select_ext  # round 2, uses results.json
    PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py probe_ext   # Lichess (round 2); total cap 300
    PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py report      # offline: compare + write EPD

A chess position = trebuchet variant (A_r / B_r, see cgtpos.trebuchet) + one
queenside component on files a-d. Model prediction for every legal move:
pawn moves win/lose according to the CGT value of the resulting component,
king moves always lose.
"""
from __future__ import annotations

import collections
import functools
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cgtpos as C  # noqa: E402
import tb  # noqa: E402
from cylcgt import pawns  # noqa: E402
from realchess import movegen as MG  # noqa: E402  (read-only use)

CANDS = os.path.join(HERE, "candidates.json")
SELECTION = os.path.join(HERE, "selection.json")
SELECTION_EXT = os.path.join(HERE, "selection_ext.json")
RESULTS = os.path.join(HERE, "results.json")
TREBS = [(k, r) for k in "AB" for r in range(2, 7)]
BASE = ("A", 4)


def tame(v):
    return "W" not in v


def rec_pos(rec):
    w = frozenset(pawns.sq(s) for s in rec["white"])
    b = frozenset(pawns.sq(s) for s in rec["black"])
    ep = None
    if rec["ep"]:
        t = pawns.sq(rec["ep"])
        ep = (t, (t[0], t[1] - 1), "W") if rec["stm"] == "W" else (t, (t[0], t[1] + 1), "B")
    return pawns.Pos(w, b, ep)


def chess_position(rec, treb):
    pos = rec_pos(rec)
    fen = C.fen(pos, C.trebuchet(*treb), rec["stm"])
    p = MG.parse_fen(fen)
    errs = MG.validity_errors(p)
    assert not errs, (fen, errs)
    legal = MG.legal_uci(fen)
    pawn_moves = {m[0]: m for m in rec["rules"]["count"]["moves"]}
    assert set(pawn_moves) <= legal, (fen, set(pawn_moves) - legal)
    ksq = MG.sqname(p.king(MG.WHITE if rec["stm"] == "W" else MG.BLACK))
    king_moves = legal - set(pawn_moves)
    assert all(u.startswith(ksq) for u in king_moves), (fen, king_moves)
    pred = {}
    for rule in C.RULES:
        wins = {m[0] for m in rec["rules"][rule]["moves"] if m[4]}
        pred[rule] = {u: ("win" if u in wins else "loss") for u in legal}
    return {"fen": fen, "treb": f"{treb[0]}{treb[1]}", "stm": rec["stm"], "component": rec["pos"],
            "value": {r: rec["rules"][r]["value"] for r in C.RULES},
            "pred": pred, "pawn_moves": {u: m[1] for u, m in pawn_moves.items()},
            "king_moves": sorted(king_moves)}


def race_sensitive(rec):
    sets = {r: tuple(sorted(m[0] for m in rec["rules"][r]["moves"] if m[4])) for r in C.RULES}
    return len(set(sets.values())) > 1


def group_key(rec):
    c = rec["rules"]["count"]
    nw = sum(m[4] for m in c["moves"])
    return (c["value"], c["stm_wins"], len(c["moves"]), nw)


def select():
    rnd = random.Random(20261015)
    cands = json.load(open(CANDS))
    white = [r for r in cands if r["stm"] == "W"]
    chosen = []  # (tier, rec, treb)
    used = set()

    def add(tier, rec, treb):
        k = (rec["pos"], rec["stm"], treb)
        if k not in used:
            used.add(k)
            chosen.append((tier, rec, treb))

    # T1: tame values, White wins: up to 2 representatives per (value, #moves, #winning) group
    groups = collections.defaultdict(list)
    for r in white:
        if tame(r["rules"]["count"]["value"]) and not race_sensitive(r):
            groups[group_key(r)].append(r)
    for k in sorted(groups, key=str):
        if not k[1]:
            continue
        for r in rnd.sample(groups[k], min(2, len(groups[k]))):
            add("T1-tame-win", r, BASE)
    # T2: tame values, White loses: 1 per group
    for k in sorted(groups, key=str):
        if k[1]:
            continue
        for r in rnd.sample(groups[k], min(1, len(groups[k]))):
            add("T2-tame-loss", r, BASE)
    # T3: race-sensitive win sets (any value), stratified by the pattern of agreement
    rs = collections.defaultdict(list)
    for r in white:
        if race_sensitive(r):
            sets = {ru: tuple(sorted(m[0] for m in r["rules"][ru]["moves"] if m[4])) for ru in C.RULES}
            pat = (sets["count"] == sets["mover"], sets["count"] == sets["opponent"],
                   sets["mover"] == sets["opponent"], tame(r["rules"]["count"]["value"]),
                   r["rules"]["count"]["stm_wins"], r["rules"]["opponent"]["stm_wins"],
                   r["rules"]["mover"]["stm_wins"])
            rs[pat].append(r)
    for k in sorted(rs, key=str):
        for r in rnd.sample(rs[k], min(8, len(rs[k]))):
            add("T3-race-sensitive", r, BASE)
    # T4: BIG-valued, race-insensitive, White wins but not with every pawn move
    big = [r for r in white if not tame(r["rules"]["count"]["value"]) and not race_sensitive(r)
           and r["rules"]["count"]["stm_wins"]
           and not all(m[4] for m in r["rules"]["count"]["moves"])]
    for r in rnd.sample(big, min(20, len(big))):
        add("T4-big-win", r, BASE)
    # T5: trebuchet robustness: fixed components x all 10 trebuchet variants
    t5 = ["W: a2 / B: a5", "W: a2 a5 / B: a7", "W: a2 / B: a6", "W: c2 / B: b7 d7",
          "W: a2 c2 / B: b7"]
    byname = {(r["pos"], r["stm"]): r for r in white}
    for name in t5:
        if (name, "W") in byname:
            for treb in TREBS:
                add("T5-trebuchet-variants", byname[(name, "W")], treb)
    # T6: colour-reversal sanity checks (Black to move; predicted equal to the reversed White case)
    black = [r for r in cands if r["stm"] == "B" and tame(r["rules"]["count"]["value"])
             and r["rules"]["count"]["stm_wins"] and not race_sensitive(r)]
    for r in rnd.sample(black, min(4, len(black))):
        add("T6-black-to-move", r, ("B", 4))
    out = []
    for tier, rec, treb in chosen:
        cp = chess_position(rec, treb)
        cp["tier"] = tier
        cp["id"] = f"cgt{len(out)+1:03d}"
        out.append(cp)
    json.dump(out, open(SELECTION, "w"), indent=1)
    print(collections.Counter(c["tier"] for c in out), len(out), "positions ->", SELECTION)


def select_ext():
    """Second round, chosen after looking at round one (results.json):
    X1  the B4 trebuchet (White king far from the queenside) for every T1 component
        in which some White king move did NOT lose with the A4 trebuchet;
    X2  more tame White wins (3rd/4th representative per group), random trebuchet variant;
    X3  the B4 trebuchet for a random sample of race-sensitive (T3) components."""
    rnd = random.Random(20261016)
    cands = json.load(open(CANDS))
    byname = {(r["pos"], r["stm"]): r for r in cands}
    sel = json.load(open(SELECTION))
    res = {r["id"]: r for r in json.load(open(RESULTS))}
    used = {(c["component"], c["stm"], c["treb"]) for c in sel}
    chosen = []

    def add(tier, rec, treb):
        k = (rec["pos"], rec["stm"], f"{treb[0]}{treb[1]}")
        if k not in used:
            used.add(k)
            chosen.append((tier, rec, treb))

    for c in sel:
        r = res.get(c["id"])
        if r and c["tier"].startswith("T1") and not r["king_moves_all_lose"]:
            add("X1-B4-of-T1-kingmove", byname[(c["component"], c["stm"])], ("B", 4))
    groups = collections.defaultdict(list)
    for r in cands:
        if r["stm"] == "W" and tame(r["rules"]["count"]["value"]) and not race_sensitive(r) \
                and r["rules"]["count"]["stm_wins"]:
            groups[group_key(r)].append(r)
    picked = {c["component"] for c in sel}
    for k in sorted(groups, key=str):
        rest = [r for r in groups[k] if r["pos"] not in picked]
        for r in rnd.sample(rest, min(2, len(rest))):
            add("X2-tame-win-more", r, rnd.choice(TREBS))
    t3 = [c for c in sel if c["tier"].startswith("T3")]
    for c in rnd.sample(t3, 15):
        add("X3-B4-of-T3-race", byname[(c["component"], c["stm"])], ("B", 4))
    out = []
    for tier, rec, treb in chosen:
        cp = chess_position(rec, treb)
        cp["tier"] = tier
        cp["id"] = f"cgt{len(sel)+len(out)+1:03d}"
        out.append(cp)
    json.dump(out, open(SELECTION_EXT, "w"), indent=1)
    print(collections.Counter(c["tier"] for c in out), len(out), "positions ->", SELECTION_EXT)


def all_selected():
    sel = json.load(open(SELECTION))
    if os.path.exists(SELECTION_EXT):
        sel += json.load(open(SELECTION_EXT))
    return sel


def probe(limit=None, path=SELECTION):
    sel = json.load(open(path))
    n = 0
    for c in sel:
        if limit is not None and n >= limit:
            break
        before = tb.requests_used()
        rec = tb.lookup(c["fen"])
        n += tb.requests_used() - before
        s = tb.summarize(rec)
        print(c["id"], c["tier"], c["fen"], "->", s["root"], f"[requests used {tb.requests_used()}]",
              flush=True)


# ---------------------------------------------------------------- comparison
WINS = {"win", "cursed-win"}       # ignore the 50-move rule, as CGT does
LOSSES = {"loss", "blessed-loss"}

ASCII = {"↑": "^", "↓": "v", "⇑": "^^", "⇓": "vv", "±": "+-", "∗": "*"}


def ascii_value(v: str) -> str:
    for a, b in ASCII.items():
        v = v.replace(a, b)
    return v


def compare(c, s):
    """Compare one selected position with its tablebase summary."""
    tbm = s["moves"]
    legal = set(c["pred"]["count"])
    assert set(tbm) == legal, (c["id"], set(tbm) ^ legal)
    tb_win = {u for u, v in tbm.items() if v[1] in WINS}
    tb_draw = {u for u, v in tbm.items() if v[1] == "draw"}
    tb_unres = {u for u, v in tbm.items() if v[1] not in WINS | LOSSES | {"draw"}}
    root = s["root"]
    root_res = "win" if root in WINS else "loss" if root in LOSSES else root
    out = {"id": c["id"], "tier": c["tier"], "fen": c["fen"], "treb": c["treb"], "stm": c["stm"],
           "component": c["component"], "value": c["value"], "tb_root": root,
           "tb_win": sorted(tb_win), "tb_draw": sorted(tb_draw), "tb_unresolved": sorted(tb_unres),
           "san": {u: v[0] for u, v in tbm.items()}, "tb_moves": {u: v[1] for u, v in tbm.items()},
           "king_moves": c["king_moves"], "rules": {}}
    pawn = set(c["pawn_moves"])
    for rule in C.RULES:
        pw = {u for u, v in c["pred"][rule].items() if v == "win"}
        pred_root = "win" if pw else "loss"
        out["rules"][rule] = {
            "pred_win": sorted(pw),
            "root_agree": pred_root == root_res,
            "win_set_agree": pw == tb_win,
            "pawn_set_agree": pw == (tb_win & pawn),
            # every move's exact result (win / loss), draws count as disagreement
            "all_moves_agree": all((tbm[u][1] in WINS) == (c["pred"][rule][u] == "win")
                                   and tbm[u][1] in WINS | LOSSES for u in legal),
        }
    out["king_moves_all_lose"] = all(tbm[u][1] in LOSSES for u in c["king_moves"])
    out["king_move_results"] = {u: tbm[u][1] for u in c["king_moves"]}
    return out


def value_class(v: str) -> str:
    if "W" in v:
        return "hot-BIG" if "|" in v or "±" in v else "decided"
    if v.lstrip("-").replace("/", "").isdigit():
        return "number"
    if v.startswith("*"):
        return "nimber"
    if any(a in v for a in "↑↓⇑⇓"):
        return "infinitesimal"
    if "±" in v and "|" not in v:
        return "switch"
    return "other-tame"


@functools.lru_cache(maxsize=None)
def _maxlen(pos, side):
    """Longest alternating pawn-move sequence from pos with `side` to move, stopping
    when a passed pawn appears (the model's terminal) or the mover has no pawn move."""
    if pawns.passed(C.B4, pos, "W") or pawns.passed(C.B4, pos, "B"):
        return 0
    other = "B" if side == "W" else "W"
    kids = [ch for *_, ch in C.labeled_moves(C.B4, pos, side)]
    return 1 + max((_maxlen(ch, other) for ch in kids), default=-1)


def features(r, cands):
    rec = cands[(r["component"], r["stm"])]
    pos = rec_pos(rec)
    kinds = {m[0]: m[2] for m in rec["rules"]["count"]["moves"]}
    winp = [u for u in r["tb_win"] if u in kinds]
    slow = bool(winp) and all(kinds[u] == "push" for u in winp) and any(k in ("double", "capture") for k in kinds.values())
    return {"class": value_class(r["value"]["count"]), "nsol": len(r["tb_win"]),
            "race_sensitive": race_sensitive(rec),
            "maxlen": _maxlen(pos, r["stm"]), "slow": slow}


def epd_line(r, label):
    fen4 = " ".join(r["fen"].split()[:4])
    ok = r["tb_win"] if r["tb_win"] else r["tb_draw"]
    bm = " ".join(sorted(r["san"][u] for u in ok))
    cnt = r["rules"]["count"]
    vals = "; ".join(f"{k}={ascii_value(v)}" for k, v in r["value"].items())
    pred = " ".join(sorted(r["san"][u] for u in cnt["pred_win"])) or "none"
    tbsum = " ".join(f"{r['san'][u]}:{r['tb_moves'][u]}" for u in sorted(r["san"], key=lambda x: r["san"][x]))
    ops = [f"bm {bm};", f'id "{r["id"]}";',
           f'c0 "CGT component {r["component"]} on files a-d, value {vals}";',
           f'c1 "CGT(count) predicted winning moves: {pred}; tablebase root: {r["tb_root"]}";',
           f'c2 "{" ".join(sorted(ok))}";',
           f'c3 "{label}; tier {r["tier"]}; trebuchet {r["treb"]}";',
           f'c4 "TB per move (result for mover): {tbsum}";']
    if "features" in r:
        f = r["features"]
        ops.append(f'c5 "class {f["class"]}; solutions {f["nsol"]}; max pawn-play length {f["maxlen"]}; '
                   f'only-slow-winning-move {str(f["slow"]).lower()}";')
    return fen4 + " " + " ".join(ops)


def report():
    sel = all_selected()
    rows = []
    missing = 0
    for c in sel:
        rec = tb.lookup(c["fen"], allow_network=False)
        if rec is None or rec.get("status") != 200:
            missing += 1
            continue
        rows.append(compare(c, tb.summarize(rec)))
    cands = {(r["pos"], r["stm"]): r for r in json.load(open(CANDS))}
    for r in rows:
        r["features"] = features(r, cands)
    json.dump(rows, open(RESULTS, "w"), indent=1)
    agree, disagree = [], []
    for r in rows:
        cnt = r["rules"]["count"]
        if r["tb_root"] in WINS and cnt["win_set_agree"]:
            agree.append(epd_line(r, "VERIFIED: CGT(count) winning set == tablebase winning set"))
        elif r["tb_win"] or r["tb_draw"]:
            if not (cnt["win_set_agree"] and r["tb_root"] in LOSSES):
                disagree.append(epd_line(r, "DISAGREE: tablebase differs from CGT(count); bm = tablebase"))
    with open(os.path.join(HERE, "cgt_verified.epd"), "w") as fh:
        fh.write("\n".join(agree) + "\n")
    with open(os.path.join(HERE, "cgt_disagree.epd"), "w") as fh:
        fh.write("\n".join(disagree) + "\n")
    # summary tables
    print(f"compared {len(rows)} positions ({missing} not yet probed); "
          f"verified EPD {len(agree)}, disagreement EPD {len(disagree)}; requests used {tb.requests_used()}")
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        t = r["tier"]
        by[t]["n"] += 1
        by[t]["tb_win"] += r["tb_root"] in WINS
        by[t]["tb_draw"] += r["tb_root"] == "draw"
        by[t]["king_all_lose"] += r["king_moves_all_lose"]
        for rule in C.RULES:
            x = r["rules"][rule]
            by[t][f"{rule}:root"] += x["root_agree"]
            by[t][f"{rule}:winset"] += x["win_set_agree"]
            by[t][f"{rule}:pawnset"] += x["pawn_set_agree"]
            by[t][f"{rule}:allmoves"] += x["all_moves_agree"]
    cols = ["n", "tb_win", "tb_draw", "king_all_lose"] + [f"{ru}:{k}" for ru in C.RULES
                                                          for k in ("root", "winset", "pawnset", "allmoves")]
    print("tier".ljust(24) + " ".join(c.split(":")[-1][:7].rjust(7) if ":" not in c else
                                     (c.split(":")[0][:3] + ":" + c.split(":")[1][:4]).rjust(9) for c in cols))
    tot = collections.Counter()
    for t in sorted(by):
        tot.update(by[t])
        print(t.ljust(24) + " ".join(str(by[t][c]).rjust(7 if ":" not in c else 9) for c in cols))
    print("TOTAL".ljust(24) + " ".join(str(tot[c]).rjust(7 if ":" not in c else 9) for c in cols))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "select"
    if cmd == "select":
        select()
    elif cmd == "select_ext":
        select_ext()
    elif cmd == "probe":
        probe(None)
    elif cmd == "probe_ext":
        probe(None, SELECTION_EXT)
    elif cmd == "report":
        report()
    else:
        raise SystemExit(f"unknown command {cmd}")
