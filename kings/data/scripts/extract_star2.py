"""Offline extraction of the *2 candidate's real-chess comparison data (A8 test data).

Reads realchess/results/*.json and realchess/cache (read-only; no network, no probes).
Writes kings/data/star2_tree.json.

    cd /Users/aritro/Downloads/Research/Chessendgames
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/data/scripts/extract_star2.py
"""
import collections
import datetime
import hashlib
import json
import os
import sys

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
sys.path.insert(0, ROOT)
from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Pos  # noqa: E402
from realchess import component as C  # noqa: E402
from realchess import movegen as mg  # noqa: E402

RES = os.path.join(ROOT, "realchess", "results")
CACHE = os.path.join(ROOT, "realchess", "cache")
CACHES = [CACHE, os.path.join(ROOT, "engine", "suite", "tbcache")]
ORACLEALL = "comp_Wa2c2_Bb7d7_oracleall_pure_textbook_offline.json"
OUT = os.path.join(ROOT, "kings", "data", "star2_tree.json")

MOVER_RESULT = {"loss": "win", "blessed-loss": "cursed-win", "draw": "draw", "cursed-win": "blessed-loss",
                "win": "loss", "maybe-loss": "maybe-win", "maybe-win": "maybe-loss", "unknown": "unknown"}
VAL = {1: "win", 0: "draw", -1: "loss", None: None}
NUM = {"win": 1, "draw": 0, "loss": -1, "unresolved": None, None: None}
FLIP = {"win": "loss", "loss": "win", "draw": "draw", None: None}
RANK = {"loss": 0, "blessed-loss": 0, "draw": 1, "cursed-win": 2, "win": 2}
INPUTS = ["comp_Wa2c2_Bb7d7_oracleall_pure_textbook_offline.json", "comp_Wa2c2_Bb7d7_oracle_pure.json", "oracle_pure_run1_pin.json", "oracle_pure_run2_exclude.json",
          "comp_Wa2c2_Bb7d7_nodes_pure.json", "comp_Wa2c2_Bb7d7_roots_pure.json",
          "comp_Wa2c2_Bb7d7_nodes_pure_offline.json", "comp_Wa2c2_Bb7d7_nodes_pure_offline_ext6.json",
          "comp_Wa2c2_Bb7d7_kings_pure_offline.json", "comp_Wa2c2_Bb7d7_kings_pure_root.json",
          "comp_Wa2c2_Bb7d7_consistency.json",
          "comp_Wa2c2_Bb7d7_summary.json", "cert_root_w.json", "cert_root_b.json", "cert_T1_wfirst.json",
          "cert_T1_bfirst.json", "cert_T2_wfirst.json", "cert_T2_bfirst.json"]


def load(name):
    return json.load(open(os.path.join(RES, name)))


def file_info(name):
    p = os.path.join(RES, name)
    st = os.stat(p)
    return {"modified": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]}


def cached(fen):
    key = mg.normal_fen(fen)
    h = hashlib.sha256(key.encode()).hexdigest()
    for c in CACHES:
        p = os.path.join(c, h[:2], h + ".json")
        try:
            rec = json.load(open(p))
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        if rec.get("fen") == key:
            return rec
    return None


def move_kind(pos, uci):
    s = mg.sq(uci[:2])
    pc = pos.board[s]
    if pc in "Kk":
        return "king-capture" if pos.board[mg.sq(uci[2:4])] != mg.EMPTY else "king"
    if pc in "Pp":
        return "pawn(a-d)" if s % 8 < 4 else "pawn(g-file trebuchet)"
    return "other"


def record_evidence(fen, full=True):
    """Per-move categories of the position's own cached Lichess record, if any (mover's view)."""
    rec = cached(fen)
    if not rec or not rec.get("data"):
        return None
    d = rec["data"]
    pos = mg.parse_fen(fen)
    moves = []
    for m in d.get("moves", []):
        moves.append({"uci": m["uci"], "san": m.get("san"), "kind": move_kind(pos, m["uci"]),
                      "result_for_mover": MOVER_RESULT.get(m.get("category"), m.get("category")),
                      "dtz": m.get("dtz"), "immediate_stalemate": m.get("stalemate")})
    by = collections.defaultdict(list)
    for m in moves:
        by[m["result_for_mover"]].append(m["san"])
    out = {"source": "cached Lichess record of this exact position (realchess/cache or engine/suite/tbcache)",
           "root_category_for_side_to_move": d.get("category"),
           "winning_moves": sorted(by.get("win", []) + by.get("cursed-win", [])),
           "drawing_moves": sorted(by.get("draw", [])),
           "losing_moves": sorted(by.get("loss", []) + by.get("blessed-loss", [])),
           "unknown_moves": sorted(by.get("unknown", [])),
           "king_moves_by_result": dict(collections.Counter(m["result_for_mover"] for m in moves
                                                            if m["kind"].startswith("king")))}
    if full:
        out["moves"] = moves
    out["_moves"] = moves
    return out


def strip(e):
    if e:
        e = dict(e)
        e.pop("_moves", None)
    return e


def best_moves(e):
    """The mover's best recorded result and the moves (with kind) achieving it."""
    if not e:
        return None
    known = [m for m in e["_moves"] if m["result_for_mover"] in RANK]
    if not known:
        return None
    b = max(RANK[m["result_for_mover"]] for m in known)
    pawn_best = max((RANK[m["result_for_mover"]] for m in known if not m["kind"].startswith("king")), default=None)
    king_best = max((RANK[m["result_for_mover"]] for m in known if m["kind"].startswith("king")), default=None)
    return {"best_result_for_mover": ["loss", "draw", "win"][b],
            "best_moves": [f'{m["san"]} ({m["kind"]})' for m in known if RANK[m["result_for_mover"]] == b],
            "king_moves_by_result": e["king_moves_by_result"],
            "unknown_moves": e["unknown_moves"],
            "a_king_move_beats_every_known_pawn_move": (king_best is not None and
                                                        (pawn_best is None or king_best > pawn_best))}


def class_of_(rw, rb):
    if rw is None or rb is None:
        return None
    return {(1, 1): "L", (-1, -1): "R", (1, -1): "N", (-1, 1): "P"}.get((rw, rb), "D")


def auto_category(t, side_key, e, race):
    """Rule-based diagnosis (inference) of a terminal whose real result for `side_key` contradicts the convention.
    Rules, in order: (1) e.p. right owned by the side to move and an e.p. capture among its best recorded moves
    (or no record) -> en passant; (2) a king move strictly beats every recorded pawn move -> king leaves the
    trebuchet; (3) best recorded moves are pawn captures -> counter-passer (capture); pawn pushes -> race (if a
    race terminal) or counter-passer (push); (4) no record: race terminal -> race; side to move has a component
    capture -> counter-passer (probable); else unclear."""
    s = "W" if side_key == "white_first" else "B"
    bm = best_moves(e)
    ep_own = t.ep is not None and t.ep[2] == s
    ep_sq = pawns.name(t.ep[0]) if t.ep else None
    if e:
        known = [m for m in e["_moves"] if m["result_for_mover"] in RANK]
        b = max((RANK[m["result_for_mover"]] for m in known), default=None)
        best = [m for m in known if RANK[m["result_for_mover"]] == b]
    else:
        best = []
    is_ep = lambda m: m["kind"] == "pawn(a-d)" and m["uci"][2:4] == ep_sq and m["uci"][0] != m["uci"][2]
    if ep_own and (not e or any(is_ep(m) for m in best)):
        return {"side": side_key, "category": "en passant" if e else "en passant (probable)",
                "note": ("best recorded move(s) include the e.p. capture " +
                         ", ".join(m["san"] for m in best if is_ep(m))) if e else
                        "the side to move owns an e.p. right; no record of the position"}
    if bm and bm["a_king_move_beats_every_known_pawn_move"]:
        return {"side": side_key, "category": "king leaves the trebuchet",
                "note": "only king moves reach the best recorded result: " + ", ".join(bm["best_moves"])}
    if best:
        pawn_best = [m for m in best if m["kind"] == "pawn(a-d)"]
        kb = [m["san"] for m in best if m["kind"].startswith("king")]
        tail = (f"; king moves {', '.join(kb)} do equally well" if kb else "")
        if any("x" in (m["san"] or "") for m in pawn_best):
            return {"side": side_key, "category": "counter-passer (capture)",
                    "note": "best recorded moves include the pawn capture(s) " +
                            ", ".join(m["san"] for m in pawn_best if "x" in (m["san"] or "")) + tail}
        return {"side": side_key, "category": "race" if race else "counter-passer (push)",
                "note": "best recorded moves are pawn pushes " + ", ".join(m["san"] for m in pawn_best) + tail}
    if race:
        return {"side": side_key, "category": "race", "note": "race terminal; no record of the position"}
    p = Pos(t.white, t.black, t.ep if ep_own else None)
    caps = [q for q in pawns.moves(C.BOARD4, p, s) if len(q.white) + len(q.black) < len(t.white) + len(t.black)]
    if caps:
        return {"side": side_key, "category": "counter-passer (probable)",
                "note": "no record; the side to move has a pawn capture in the component"}
    return {"side": side_key, "category": "unclear (king move or pawn push)",
            "note": "no record of the position and no pawn capture available, so the real result comes from a king "
                    "move or a pawn push"}


def describe_move(p, q, mover):
    mine_p, mine_q = (p.white, q.white) if mover == "W" else (p.black, q.black)
    th_p, th_q = (p.black, q.black) if mover == "W" else (p.white, q.white)
    fr, to, cap = list(mine_p - mine_q), list(mine_q - mine_p), list(th_p - th_q)
    if len(fr) != 1 or len(to) != 1:
        return None
    f, t = pawns.name(fr[0]), pawns.name(to[0])
    if cap:
        return f"{f[0]}x{t}" + (" e.p." if pawns.name(cap[0]) != t else "")
    return t if abs(fr[0][1] - to[0][1]) == 1 else f"{t} (double step)"


def model_side_results(cls):
    return {"L": (1, 1), "R": (-1, -1), "N": (1, -1), "P": (-1, 1)}.get(cls, (None, None))


def comp_from_fen(fen):
    pos = mg.parse_fen(fen)
    c = C.component_of(pos)
    if pos.ep is not None and pos.ep % 8 < 4:
        f, r = pos.ep % 8, pos.ep // 8 + 1
        stm = "W" if pos.stm == mg.WHITE else "B"
        cap = (f, r - 1) if stm == "W" else (f, r + 1)
        c = Pos(c.white, c.black, ((f, r), cap, stm))
    return c


def stm_of(fen):
    return "W" if fen.split()[1] == "w" else "B"


def white_view(res_for_stm, stm):
    return res_for_stm if stm == "W" else FLIP[res_for_stm]


# ----------------------------------------------------------------------------- diagnoses (inference)
RACE = ("race",
        "Race terminal (both sides have a passer). RACE_RULE 'count' and 'mover' give Black the win (Black's c-pawn is "
        "nearer promotion), 'opponent' gives White; real chess is N (the side to move wins), so no rule is exact. "
        "The data record only White's first move (a4 in the a3 sibling, where Ke4/Ke5 merely draw), not the line.")
EP = ("en passant",
      "The convention counts a pawn that has just double-stepped past an enemy pawn as passed; the recorded only "
      "winning reply is the e.p. capture. Not a king effect. Under the adopted e.p.-aware passed test this position "
      "is no longer a terminal.")
DIAG = {
    "W: a2 / B: c5 d7": RACE, "W: a3 / B: c5 d6": RACE, "W: a3 / B: c5 d7": RACE,
    "W: a5 / B: b7 c5": ("king leaves the trebuchet",
                         "Data: with White to move the only non-losing moves are Ke4 and Ke5 (draw); a6 and the other "
                         "king moves lose. Inference: the White king gives up g4 and catches Black's c-pawn."),
    "W: c4 / B: a6 d6": ("king leaves the trebuchet (probable, not shown)",
                         "Data: the White-to-move draw comes from a parent record, so its drawing move is not "
                         "recorded. Inference: as in W: a5 / B: b7 c5, the White king on f5 is inside the square of "
                         "the a6 passer and probably catches it."),
    "W: a4 c2 / B: b4 d5 (ep a3)": EP, "W: a4 c2 / B: b4 d6 (ep a3)": EP,
    "W: a4 c3 / B: b4 d5 (ep a3)": EP, "W: a4 c2 / B: b4 d7 (ep a3)": EP,
    "W: a2 c5 / B: b7 d5 (ep d6)": EP, "W: a3 c5 / B: b7 d5 (ep d6)": EP, "W: a4 c5 / B: b7 d5 (ep d6)": EP,
    "W: a4 c4 / B: b6 d4 (ep c3)": ("unclear",
                                    "Data: Black to move wins only by dxc3 e.p. (the convention is right there); White "
                                    "to move wins (8-man search, no move recorded). This side arises after White's c2-c4 "
                                    "only if Black passes. Inference (unverified): White's king reaches e4 next to the "
                                    "d4 passer, or c4-c5 makes a faster passer."),
    "W: a4 c5 / B: b6 d5 (ep d6)": ("counter-passer after the terminal (plus e.p.)",
                                    "Data (record and cert_T2_*): White to move wins by cxb6 or cxd6 e.p.; Black to "
                                    "move loses with every move, including d4 (met by cxb6) and both king moves. "
                                    "Inference: the d5 'passer' is not an immediate win because White's capture makes "
                                    "a faster passer; not a king effect. Under the e.p.-aware test it is not a terminal."),
}


def main():
    comp = Pos.parse("W: a2 c2 / B: b7 d7")
    internal, terms, edges = C.enumerate_tree(C.BOARD4, comp)
    byname = {str(t): t for t in terms}
    parents = collections.defaultdict(list)
    for (p, side), kids in edges.items():
        for q in kids:
            if q in terms:
                parents[q].append((p, side))

    o3 = load("comp_Wa2c2_Bb7d7_oracle_pure.json")
    o2 = load("oracle_pure_run2_exclude.json")
    o1 = load("oracle_pure_run1_pin.json")
    assert len(terms) == o3["terminals_total"] == 670, len(terms)
    snap = {tag: {r["terminal"]: r for r in o["terminals"]}
            for tag, o in (("run1_pin", o1), ("run2_exclude", o2), ("run3_pin", o3))}
    snapshot_conflicts = []
    for name, r3 in snap["run3_pin"].items():
        assert name in byname, name
        for tag in ("run1_pin", "run2_exclude"):
            r = snap[tag].get(name)
            for k in ("real_W_first", "real_B_first"):
                if r and r[k] is not None and r3[k] is not None and r[k] != r3[k]:
                    snapshot_conflicts.append((name, tag, k, r[k], r3[k]))

    # ------------------------------------------------------------------ terminals (run 3 + oracle-all offline)
    oa = load(ORACLEALL)
    oa_by = {r["terminal"]: r for r in oa["terminals"]}
    assert set(oa_by) == set(byname)
    source_conflicts = []
    for name, ra in oa_by.items():
        r3 = snap["run3_pin"][name]
        for k in ("real_W_first", "real_B_first"):
            if r3[k] is not None and ra[k] is not None and r3[k] != ra[k]:
                source_conflicts.append((name, k, r3[k], ra[k]))
    rows, partial, unresolved = [], [], []
    for name in sorted(byname, key=lambda n: (snap["run3_pin"][n]["men"], n)):
        r3, ra = snap["run3_pin"][name], oa_by[name]
        t = byname[name]
        rw = r3["real_W_first"] if r3["real_W_first"] is not None else ra["real_W_first"]
        rb = r3["real_B_first"] if r3["real_B_first"] is not None else ra["real_B_first"]
        if rw is None and rb is None:
            if r3["how_W"] or r3["how_B"] or ra["how_W"] or ra["how_B"]:
                unresolved.append(name)
            continue
        cls = class_of_(rw, rb)
        fens = {s_: mg.normal_fen(C.embed(t, s_)) for s_ in "WB"}
        mW, mB = model_side_results(r3["model_count"])
        reached = [{"from_component": str(p), "mover": side, "move": describe_move(p, t, side)}
                   for p, side in sorted(parents[t], key=lambda x: (str(x[0]), x[1]))]
        first = {}
        for k, key in (("real_W_first", "white_first"), ("real_B_first", "black_first")):
            first[key] = next((tag for tag, src in (("run1_pin", snap["run1_pin"]), ("run2_exclude", snap["run2_exclude"]),
                                                    ("run3_pin", snap["run3_pin"]), ("oracleall_offline", oa_by))
                               if src.get(name, {}).get(k) is not None), None)
        nxt = sorted({"black_first" if m == "W" else "white_first" for m in r3["entered_by"]})
        row = {
            "terminal": name, "men": r3["men"], "race": r3["race"],
            "fen_white_to_move": fens["W"], "fen_black_to_move": fens["B"],
            "reached": {"entered_by": r3["entered_by"], "side_to_move_after_entry": nxt,
                        "parents_derived_offline": reached},
            "convention": {"class_count_rule": r3["model_count"], "class_by_race_rule": r3["model_by_rule"],
                           "white_result_white_first": VAL[mW], "white_result_black_first": VAL[mB]},
            "real_chess": {"white_result_white_first": VAL[rw], "white_result_black_first": VAL[rb], "class": cls,
                           "how": {"run3": {"white_first": r3["how_W"], "black_first": r3["how_B"]},
                                   "oracleall_offline": {"white_first": ra["how_W"], "black_first": ra["how_B"]}},
                           "first_resolved_in": first},
            "in_run3_snapshot": bool(r3["real_W_first"] is not None or r3["real_B_first"] is not None),
        }
        wrong = [k for k, m_, x in (("white_first", mW, rw), ("black_first", mB, rb)) if x is not None and m_ != x]
        row["frozen_king_wrong"] = bool(wrong)
        row["wrong_side"] = wrong
        if cls:
            row["agrees_by_race_rule"] = {k: v == [cls] for k, v in r3["model_by_rule"].items()}
        ev = {}
        for s_, key in (("W", "white_first"), ("B", "black_first")):
            e = record_evidence(fens[s_], full=bool(wrong))
            if e:
                ev[key] = e
        row["_ev"] = ev
        row["tablebase_evidence"] = {k: strip(e) for k, e in ev.items()} or None
        if wrong:
            auto = [auto_category(t, k, ev.get(k), r3["race"]) for k in wrong]
            if name in DIAG:
                cat, why = DIAG[name]
                row["diagnosis_inferred"] = {"category": cat, "note": why, "source": "hand-checked",
                                             "rule_based": auto}
            else:
                cat = " / ".join(sorted({a["category"] for a in auto}))
                row["diagnosis_inferred"] = {"category": cat, "note": "; ".join(a["note"] for a in auto),
                                             "source": "rule-based (see _about.conventions.rule_based_diagnosis)",
                                             "rule_based": auto}
        (rows if cls else partial).append(row)
    term_real = {}
    for r in rows + partial:
        term_real[r["terminal"]] = (NUM[r["real_chess"]["white_result_white_first"]],
                                    NUM[r["real_chess"]["white_result_black_first"]])

    # ------------------------------------------------------------------ node positions (one per FEN)
    node_sources = [("nodes_pure", load("comp_Wa2c2_Bb7d7_nodes_pure.json")["nodes"]),
                    ("roots_pure.model_nodes", load("comp_Wa2c2_Bb7d7_roots_pure.json")["model_nodes"]),
                    ("nodes_pure_offline (ext 4)", load("comp_Wa2c2_Bb7d7_nodes_pure_offline.json")["nodes"]),
                    ("nodes_pure_offline_ext6", load("comp_Wa2c2_Bb7d7_nodes_pure_offline_ext6.json")["nodes"])]
    posn = {}
    for src, lst in node_sources:
        for x in lst:
            for s in "WB":
                fen = x.get(s + "_fen")
                if not fen:
                    continue
                e = posn.setdefault(fen, {"fen": fen, "side_to_move": s, "recorded_component": x["component"],
                                          "recorded_model_outcome": x["model_outcome"], "real_for_stm": None,
                                          "sources": [], "resolved_by": []})
                assert e["recorded_model_outcome"] == x["model_outcome"]
                e["sources"].append(src)
                iv = x.get(s)
                if iv and iv[0] == iv[1]:
                    v = VAL[iv[0]]
                    assert e["real_for_stm"] in (None, v), (fen, e["real_for_stm"], v)
                    e["real_for_stm"] = v
                    e["resolved_by"].append(src)
    node_real_by_fen = {f: e["real_for_stm"] for f, e in posn.items()}

    def child_info(q, s, desc):
        opp = "B" if s == "W" else "W"
        name = str(q)
        if C.is_terminal(C.BOARD4, q):
            mv = C.model_terminal_value(C.BOARD4, q, s, "count")
            conv = "win" if (mv > 0) == (s == "W") else "loss"
            rr = term_real.get(name)
            v = (rr[0] if opp == "W" else rr[1]) if rr else None
            real = None if v is None else VAL[v if s == "W" else -v]
            return {"move": desc, "child": name, "child_kind": "terminal", "convention_for_mover": conv,
                    "real_for_mover": real}
        o = cgt.outcome(pawns.value(C.BOARD4, q))
        conv = "win" if (o in ("L", "P") if s == "W" else o in ("R", "P")) else "loss"
        cf = mg.normal_fen(C.embed(q, opp))
        r_opp = node_real_by_fen.get(cf)
        return {"move": desc, "child": name, "child_fen": cf, "child_kind": "node", "convention_for_mover": conv,
                "real_for_mover": FLIP[r_opp]}

    # king-move audit (realchess 'kings' stage, offline)
    ka = load("comp_Wa2c2_Bb7d7_kings_pure_offline.json")
    audit_by_fen = collections.defaultdict(lambda: {"loses": [], "draws": [], "wins": [], "unresolved": 0})
    for r in ka["rows"]:
        a = audit_by_fen[r["fen"]]
        if r["verdict"] == "unresolved":
            a["unresolved"] += 1
        else:
            a[r["verdict"]].append({"king_move": r["king_move"], "refutation": r["refutation"], "how": r["how"]})

    nodes = []
    for fen, e in sorted(posn.items(), key=lambda kv: (kv[1]["recorded_component"], kv[1]["side_to_move"])):
        s = e["side_to_move"]
        p = comp_from_fen(fen)
        kids = [child_info(q, s, describe_move(p, q, s)) for q in C.options(C.BOARD4, p, s)]
        conv = "win" if any(k["convention_for_mover"] == "win" for k in kids) else "loss"
        cls = e["recorded_model_outcome"]["count"]
        rec_conv = "win" if cls in (("L", "N") if s == "W" else ("R", "N")) else "loss"
        if p.ep is None:
            assert rec_conv == conv, (fen, rec_conv, conv)
        real = e["real_for_stm"]
        aud = audit_by_fen.get(fen)
        ev = record_evidence(fen, full=False)
        x = {
            "fen": fen, "component": str(p), "side_to_move": s,
            "sources": e["sources"], "resolved_by": e["resolved_by"],
            "is_root": str(p) == "W: a2 c2 / B: b7 d7",
            "convention": {"result_for_side_to_move": conv, "white_result": white_view(conv, s),
                           "recorded_class_by_race_rule": e["recorded_model_outcome"],
                           "recorded_component": e["recorded_component"]},
            "pawn_moves_available_derived_offline": len(kids),
            "real_chess": {"result_for_side_to_move": real, "white_result": white_view(real, s)},
            "frozen_king_wrong": None if real is None else real != conv,
            "king_move_audit": aud and {"draws": [a["king_move"] for a in aud["draws"]],
                                        "wins": [a["king_move"] for a in aud["wins"]],
                                        "loses": [f'{a["king_move"]} (refuted by {a["refutation"]})'
                                                  for a in aud["loses"]],
                                        "unresolved": aud["unresolved"]},
            "tablebase_evidence": strip(ev),
        }
        if p.ep is not None and rec_conv != conv:
            x["ep_note"] = ("the FEN carries an e.p. right on files a-d, but the recorded model class was computed for "
                            "the component WITHOUT it (realchess keys nodes by the ep-less component); 'convention' is "
                            "re-derived WITH the e.p. right. Recorded comparison: " +
                            f"convention {rec_conv} for the side to move.")
            x["frozen_king_wrong_as_recorded"] = None if real is None else real != rec_conv
        if x["frozen_king_wrong"]:
            known = [k for k in kids if k["real_for_mover"] is not None]
            best = max((RANK[k["real_for_mover"]] for k in known), default=None)
            king_res = []
            if aud:
                king_res = ["draw"] * len(aud["draws"]) + ["win"] * len(aud["wins"])
            king_best = max((RANK[r_] for r_ in king_res), default=None)
            reason = None
            if known and len(known) == len(kids) and RANK[real] > best:
                reason = ("every pawn move's real result is known and all are worse for the mover than the "
                          "position's real result, so the best real move is a king move")
            if king_best is not None and king_best == RANK[real] and (best is None or king_best > best) \
                    and len(known) == len(kids):
                reason = (reason or "") + ("; " if reason else "") + "the king-move audit records a king move " \
                    "achieving the real result"
            x["breakdown_derived_offline"] = {
                "convention_for_mover": conv, "real_for_mover": real,
                "pawn_moves": kids, "pawn_moves_with_known_real_result": len(known),
                "pawn_moves_misjudged_by_convention": [k["move"] for k in known
                                                       if k["real_for_mover"] != k["convention_for_mover"]],
                "king_move_is_best": reason,
                "audit_king_moves_matching_real_result": ([a["king_move"] for a in aud["draws"] if real == "draw"] +
                                                          [a["king_move"] for a in aud["wins"] if real == "win"])
                if aud else [],
            }
            x["_ev"] = ev
        nodes.append(x)
    nodes_by_fen = {x["fen"]: x for x in nodes}

    # ------------------------------------------------------------------ failure list
    tfail = {}
    failures = []
    for r in rows + partial:
        if not r["wrong_side"]:
            continue
        cat, why = r["diagnosis_inferred"]["category"], r["diagnosis_inferred"]["note"]
        tfail[r["terminal"]] = cat
        failures.append({
            "kind": "terminal" + (" (one side resolved)" if r["real_chess"]["class"] is None else ""),
            "position": r["terminal"],
            "fen_white_to_move": r["fen_white_to_move"], "fen_black_to_move": r["fen_black_to_move"],
            "entered_by": r["reached"]["entered_by"], "side_to_move_after_entry": r["reached"]["side_to_move_after_entry"],
            "convention_class": r["convention"]["class_count_rule"], "real_class": r["real_chess"]["class"],
            "convention_white_results": [r["convention"]["white_result_white_first"],
                                         r["convention"]["white_result_black_first"]],
            "real_white_results": [r["real_chess"]["white_result_white_first"],
                                   r["real_chess"]["white_result_black_first"]],
            "wrong_side": r["wrong_side"],
            "wrong_on_side_to_move_after_entry": any(s in r["reached"]["side_to_move_after_entry"]
                                                     for s in r["wrong_side"]),
            "diagnosis_category_inferred": cat, "diagnosis_note": why,
            "diagnosis_source": r["diagnosis_inferred"]["source"],
            "in_run3_snapshot": r["in_run3_snapshot"],
            "tablebase_best_moves": {k: best_moves(e) for k, e in r["_ev"].items()} or None,
        })

    def explain(fen, depth=0, seen=()):
        x = nodes_by_fen[fen]
        b = x["breakdown_derived_offline"]
        name = f'{x["component"]} [{x["side_to_move"]} to move]'
        if b["king_move_is_best"]:
            return [f"{name}: {b['king_move_is_best']}"], {"king move"}
        out, causes = [], set()
        kids = b["pawn_moves"]
        if b["convention_for_mover"] == "win":
            wins = [k for k in kids if k["convention_for_mover"] == "win"]
            unknown = [k for k in wins if k["real_for_mover"] is None]
            use = [k for k in wins if k["real_for_mover"] is not None and k["real_for_mover"] != "win"]
            if unknown:
                out.append(f"{name}: {len(unknown)} of {len(wins)} convention-winning pawn moves have no real result "
                           f"({', '.join(k['move'] for k in unknown)})")
                causes.add("children not resolved")
        else:
            use = [k for k in kids if k["real_for_mover"] is not None
                   and RANK[k["real_for_mover"]] >= RANK[b["real_for_mover"]]]
            if b["audit_king_moves_matching_real_result"]:
                out.append(f"{name}: the king-move audit records {', '.join(b['audit_king_moves_matching_real_result'])} "
                           f"reaching the real result ({b['real_for_mover']})")
                causes.add("king move (audit)")
            if not use and not b["audit_king_moves_matching_real_result"]:
                unknown = [k for k in kids if k["real_for_mover"] is None]
                out.append(f"{name}: no pawn move with a known result reaches the real result; "
                           f"{len(unknown)} pawn moves unresolved")
                return out, {"children not resolved"}
        for k in use:
            out.append(f"{name} --{k['move']}--> {k['child']}: convention {k['convention_for_mover']}, "
                       f"real {k['real_for_mover']}")
            if k["child_kind"] == "terminal":
                causes.add(tfail.get(k["child"], "terminal not resolved"))
            else:
                cx = nodes_by_fen.get(k["child_fen"])
                if not cx or "breakdown_derived_offline" not in cx or k["child_fen"] in seen or depth > 8:
                    causes.add("children not resolved")
                    continue
                o2, c2 = explain(k["child_fen"], depth + 1, seen + (fen,))
                out += o2
                causes |= c2
        return out, causes

    for x in nodes:
        if not x["frozen_king_wrong"]:
            continue
        chain, causes = explain(x["fen"])
        x["breakdown_derived_offline"]["trace"] = chain
        x["breakdown_derived_offline"]["traces_to"] = sorted(causes)
        failures.append({
            "kind": "node",
            "position": x["component"], "fen": x["fen"], "side_to_move": x["side_to_move"],
            "convention_for_side_to_move": x["convention"]["result_for_side_to_move"],
            "real_for_side_to_move": x["real_chess"]["result_for_side_to_move"],
            "king_move_audit": x["king_move_audit"],
            "traces_to_derived": sorted(causes),
            "trace_derived": chain,
            "tablebase_best_moves": best_moves(x.pop("_ev", None)),
        })
    for x in nodes:
        x.pop("_ev", None)
    for r in rows + partial:
        r.pop("_ev", None)

    # ------------------------------------------------------------------ consistency check
    cons = load("comp_Wa2c2_Bb7d7_consistency.json")
    cons_rows = []
    for d in cons["draw=Black win"]["disagreements"]:
        x = nodes_by_fen.get(d["fen"])
        cons_rows.append({"fen": d["fen"], "component": x["component"] if x else None,
                          "side_to_move": stm_of(d["fen"]),
                          "real_result_for_side_to_move": VAL[d["real_for_stm"]],
                          "oracle_cgt_predicts_side_to_move_wins": d["cgt_predicts_stm_wins"],
                          "pure_convention_for_side_to_move": x["convention"]["result_for_side_to_move"] if x else None})
    same = cons["draw=Black win"]["disagreements"] == cons["draw=White win"]["disagreements"]

    # ------------------------------------------------------------------ roots, certificates
    ro = load("comp_Wa2c2_Bb7d7_roots_pure.json")
    roots = {s: {"fen": r["fen"], "real_result_for_side_to_move": r["result"],
                 "convention_side_to_move_wins": r["model_stm_wins"],
                 "convention_component_class": r["model_outcome_of_component"], "king_moves": r["king_moves"]}
             for s, r in ro["roots"].items()}
    kr = load("comp_Wa2c2_Bb7d7_kings_pure_root.json")
    for s_, r in roots.items():
        r["king_move_audit"] = [{"king_move": x["king_move"], "verdict": x["verdict"], "refutation": x["refutation"],
                                 "how": x["how"]} for x in kr["rows"] if x["fen"] == mg.normal_fen(r["fen"])]
    roots["_king_move_audit_source"] = {"file": "comp_Wa2c2_Bb7d7_kings_pure_root.json", "tally": kr["tally"],
                                        "status": kr["status"]}
    certs = {}
    for f in ("cert_root_w", "cert_root_b", "cert_T1_wfirst", "cert_T1_bfirst", "cert_T2_wfirst", "cert_T2_bfirst"):
        c = load(f + ".json")
        certs[f] = dict(c["summary"])
        cc = c["certificate"]
        if "by" in cc:
            certs[f]["proving_move"] = cc["by"]["move"]
        elif "all_moves" in cc:
            certs[f]["refuted_moves"] = [m["move"] for m in cc["all_moves"]]
        certs[f]["component"] = str(comp_from_fen(c["summary"]["fen"]))
        nf = mg.normal_fen(c["summary"]["fen"])
        hit = [r["terminal"] for r in rows + partial if nf in (r["fen_white_to_move"], r["fen_black_to_move"])]
        certs[f]["terminal_in_tree"] = hit[0] if hit else None

    # ------------------------------------------------------------------ king audit summary
    non_losing = []
    for r in ka["non_losing"]:
        x = nodes_by_fen.get(r["fen"])
        s_ = stm_of(r["fen"])
        p_ = comp_from_fen(r["fen"])
        kids_ = [child_info(q, s_, describe_move(p_, q, s_)) for q in C.options(C.BOARD4, p_, s_)]
        conv = "win" if any(k["convention_for_mover"] == "win" for k in kids_) else "loss"
        real = x["real_chess"]["result_for_side_to_move"] if x else None
        res = {"draws": "draw", "wins": "win"}[r["verdict"]]
        e_ = {"fen": r["fen"], "component": r["component"], "side_to_move": s_, "king_move": r["king_move"],
              "result_for_mover": res, "convention_for_side_to_move_derived": conv,
              "node_real_for_side_to_move": real, "node_in_node_tables": x is not None,
              "beats_convention_verdict": conv == "loss",
              "node_frozen_king_wrong": x["frozen_king_wrong"] if x else None}
        non_losing.append(e_)
        if conv == "loss" and (x is None or x["frozen_king_wrong"] is None):
            failures.append({
                "kind": "node (king-move audit only)", "position": r["component"], "fen": r["fen"],
                "side_to_move": s_, "convention_for_side_to_move": conv,
                "real_for_side_to_move": f"at least {res} (the node itself is not resolved)",
                "king_move_audit": {"non_losing": [r["king_move"]]},
                "traces_to_derived": ["king move (audit)"],
                "trace_derived": [f"{r['component']} [{s_} to move]: the convention scores the side to move as lost; "
                                  f"the king-move audit records {r['king_move']} as a {res}"],
                "tablebase_best_moves": best_moves(record_evidence(r["fen"], full=False)),
            })
    king_audit = {"source": "realchess/results/comp_Wa2c2_Bb7d7_kings_pure_offline.json (realchess 'kings' stage: "
                            "every king move of every embedded internal node, both sides to move; 'loses' = refuted "
                            "at once by a capture into tablebase data, else a bounded search with ext 2)",
                  "status": ka["status"], "ext": ka["ext"], "node_positions": ka["nodes"],
                  "king_moves": ka["king_moves"], "tally": ka["tally"],
                  "non_losing": non_losing,
                  "node_positions_with_unresolved_king_moves": len(ka["unresolved_nodes"])}

    # ------------------------------------------------------------------ king moves in terminal records
    kagg = {"convention_says_side_to_move_loses": collections.Counter(),
            "convention_says_side_to_move_wins": collections.Counter()}
    kpos = []
    for r in rows + partial:
        for key, e in (r["tablebase_evidence"] or {}).items():
            v = r["convention"]["white_result_white_first" if key == "white_first" else "white_result_black_first"]
            stm_wins = (v == "win") == (key == "white_first")
            g = "convention_says_side_to_move_wins" if stm_wins else "convention_says_side_to_move_loses"
            kagg[g].update(e["king_moves_by_result"])
            if not stm_wins and any(k in e["king_moves_by_result"] for k in ("draw", "win", "cursed-win")):
                kpos.append(f'{r["terminal"]} ({key}): king moves {e["king_moves_by_result"]}')

    resolved_counts = collections.Counter(r["real_chess"]["class"] for r in rows)
    nfail = [x for x in nodes if x["frozen_king_wrong"]]
    out = {
        "_about": {
            "item": "A8 test data: the *2 candidate (W a2 c2 / B b7 d7 on files a-d of a flat 8x8 board, trebuchet "
                    "W g4 / B g5, WK f5, BK h4) compared with real chess.",
            "extracted": datetime.datetime.now().isoformat(timespec="seconds"),
            "input_files": {n: file_info(n) for n in INPUTS},
            "sources": {
                "terminals": "merged from comp_Wa2c2_Bb7d7_oracle_pure.json (run 3, goal pin, 00:29; 84 resolved) and "
                             "comp_Wa2c2_Bb7d7_oracleall_pure_textbook_offline.json (oracle-all, offline, textbook "
                             "passed test, 01:32; written by another workstream during this extraction); the two never "
                             "conflict. Earlier snapshots: oracle_pure_run1_pin.json (62 resolved) and "
                             "oracle_pure_run2_exclude.json (65 resolved; the snapshot RESULTS.md section 1 quotes).",
                "node_positions": "one entry per node FEN, merged from nodes_pure.json (= nodes_pure_run1.json), "
                                  "roots_pure.json 'model_nodes', nodes_pure_offline.json and "
                                  "nodes_pure_offline_ext6.json; resolved results never conflict.",
                "king_move_audit": "comp_Wa2c2_Bb7d7_kings_pure_offline.json",
                "consistency": "comp_Wa2c2_Bb7d7_consistency.json (computed from the run-2-era oracle file).",
                "tablebase_evidence": "per-move categories read offline from realchess/cache for the exact FEN when it "
                                      "was itself probed (7-man positions, and 8-man positions for which Lichess "
                                      "returned categories); converted to the mover's result.",
            },
            "conventions": {
                "terminal": "a component position, entered by a move, in which some side has a passed pawn (textbook "
                            "passed test: e.p. NOT respected, as in the runs). The convention scores it an immediate "
                            "win for the passer's side; races (both passed) by RACE_RULE (default 'count').",
                "results": "terminals: White's view, white_result_white_first / white_result_black_first. Node "
                           "positions: result for the side to move, plus 'white_result'.",
                "class": "L = White wins whoever moves first; R = Black wins whoever moves first; N = side to move "
                         "wins; P = side to move loses; D = a draw for at least one side.",
                "frozen_king_wrong": "true iff the real result differs from the convention (RACE_RULE 'count'). It flags "
                                     "EVERY convention failure (frozen kings, e.p., races, counter-passers); see "
                                     "'diagnosis_inferred' / 'traces_to_derived' and DATA.md for attribution.",
                "rule_based_diagnosis": auto_category.__doc__,
                "derived_offline": "fields ending in _derived_offline are re-derived offline from realchess.component / "
                                   "cylcgt (4-file flat board, e.p. on, textbook passed test), not read from result files.",
            },
            "snapshot_result_conflicts": snapshot_conflicts,
        },
        "summary": {
            "terminals_in_tree": o3["terminals_total"],
            "run3_snapshot": {"terminals_attempted_per_file": o3["terminals_attempted"],
                              "resolved_both_sides": o3["terminals_resolved_both_sides"],
                              "partial": len(o3["terminals_partial"]), "class_counts": o3["class_counts"],
                              "terminals_agreeing_with_count": sum(1 for r in o3["terminals"] if r["real_class"]
                                                                   and r["real_class"] == r["model_count"]),
                              "terminal_failures": sum(1 for f in failures if f["kind"].startswith("terminal")
                                                       and f["in_run3_snapshot"] and f["diagnosis_source"] == "hand-checked")},
            "oracleall_offline": {k: oa[k] for k in ("passed_test", "mode", "ext", "uses_lichess_8man_categories",
                                                      "offline", "status", "terminals_by_men", "sides_resolved",
                                                      "terminals_resolved_both_sides", "terminals_partial",
                                                      "terminals_unresolved", "class_counts",
                                                      "LR_terminals_disagreeing_with_model", "model_values")},
            "oracleall_offline_bounds_as_recorded": oa.get("bounds"),
            "source_conflicts_run3_vs_oracleall": source_conflicts,
            "terminals_resolved_both_sides": len(rows),
            "terminals_partially_resolved": len(partial),
            "terminals_unresolved": len(unresolved),
            "real_class_counts": dict(resolved_counts),
            "convention_vs_real_count_rule": {f"{a}->{b}": v for (a, b), v in sorted(collections.Counter(
                (r["convention"]["class_count_rule"], r["real_chess"]["class"]) for r in rows).items())},
            "terminals_agreeing_by_rule": {k: sum(r["agrees_by_race_rule"][k] for r in rows)
                                           for k in ("count", "mover", "opponent")},
            "terminal_failures": sum(1 for f in failures if f["kind"].startswith("terminal")),
            "terminal_failures_by_category_inferred": dict(collections.Counter(
                f["diagnosis_category_inferred"] for f in failures if f["kind"].startswith("terminal"))),
            "run2_snapshot_as_quoted_in_RESULTS_md": {
                "resolved": o2["terminals_resolved_both_sides"], "class_counts": o2["class_counts"],
                "agreeing_with_count": sum(1 for r in o2["terminals"] if r["real_class"]
                                           and r["real_class"] == r["model_count"])},
            "oracle_value_status_run3": {"status": o3["status"], "draw=White win": o3["draw=White win"],
                                         "draw=Black win": o3["draw=Black win"]},
            "king_moves_in_terminal_records": {g: dict(c) for g, c in kagg.items()},
            "terminal_records_with_nonlosing_king_moves_where_convention_says_loss": kpos,
            "node_positions": len(nodes),
            "node_positions_resolved": sum(1 for x in nodes if x["frozen_king_wrong"] is not None),
            "node_positions_frozen_king_wrong": len(nfail),
            "node_positions_frozen_king_wrong_as_recorded": sum(
                1 for x in nodes if x.get("frozen_king_wrong_as_recorded", x["frozen_king_wrong"])),
            "node_positions_where_ep_rederivation_changes_flag": [x["fen"] for x in nodes if "ep_note" in x
                                                                  and x["frozen_king_wrong"] != x["frozen_king_wrong_as_recorded"]],
            "node_failures_traces_to": dict(collections.Counter(
                " + ".join(f["traces_to_derived"]) for f in failures if f["kind"].startswith("node"))),
            "node_failures_with_tablebase_record": sum(1 for f in failures if f["kind"] == "node"
                                                       and f["tablebase_best_moves"]),
            "node_failures_where_record_shows_a_king_move_is_best": [
                f["fen"] for f in failures if f["kind"] == "node" and f["tablebase_best_moves"]
                and f["tablebase_best_moves"]["a_king_move_beats_every_known_pawn_move"]],
            "node_failures_where_a_king_move_is_best_derived": [
                f'{x["component"]} [{x["side_to_move"]} to move]' for x in nfail
                if x["breakdown_derived_offline"]["king_move_is_best"]],
            "recorded_node_tables": {
                "nodes_pure": {k: load("comp_Wa2c2_Bb7d7_nodes_pure.json")[k] for k in ("class_counts", "agreement_with_rule")},
                "nodes_pure_offline_ext6": {k: load("comp_Wa2c2_Bb7d7_nodes_pure_offline_ext6.json")[k]
                                            for k in ("class_counts", "agreement_with_rule")},
            },
            "king_move_audit_tally": ka["tally"],
            "king_move_audit_nonlosing_where_convention_says_loss": [
                f'{e["component"]} [{e["side_to_move"]} to move] {e["king_move"]}: {e["result_for_mover"]}'
                for e in non_losing if e["beats_convention_verdict"]],
            "consistency_disagreements": len(cons_rows),
            "consistency_tally": cons["draw=Black win"]["tally"],
            "consistency_same_under_both_draw_treatments": same,
        },
        "roots": roots,
        "certificates": certs,
        "failures": failures,
        "terminals": rows,
        "terminals_partial": partial,
        "terminals_unresolved": unresolved,
        "king_move_audit": king_audit,
        "node_positions": nodes,
        "consistency_disagreements": cons_rows,
    }
    json.dump(out, open(OUT, "w"), indent=1)
    s = out["summary"]
    print("terminals", len(rows), dict(resolved_counts), "terminal failures", s["terminal_failures"])
    print("node positions", len(nodes), "resolved", s["node_positions_resolved"], "wrong", len(nfail),
          "as recorded", s["node_positions_frozen_king_wrong_as_recorded"])
    print("node traces", s["node_failures_traces_to"])
    print("king best (record)", s["node_failures_where_record_shows_a_king_move_is_best"])
    print("king best (derived)", s["node_failures_where_a_king_move_is_best_derived"])


if __name__ == "__main__":
    main()
