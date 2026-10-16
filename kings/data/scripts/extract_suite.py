"""Offline extraction of the engine-suite king-move statistics (A8 test data).

Reads engine/suite/results.json and the cached Lichess records (engine/suite/tbcache, realchess/cache),
read-only, no network. Writes kings/data/suite_king_moves.json.
"""
import collections
import hashlib
import json
import os
import sys

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
sys.path.insert(0, ROOT)
from realchess import movegen as mg  # noqa: E402

SUITE = os.path.join(ROOT, "engine", "suite")
CACHES = [os.path.join(ROOT, "realchess", "cache"), os.path.join(SUITE, "tbcache")]
OUT = os.path.join(ROOT, "kings", "data", "suite_king_moves.json")
WINS = {"win", "cursed-win"}
LOSSES = {"loss", "blessed-loss"}
RANK = {"loss": 0, "blessed-loss": 0, "draw": 1, "cursed-win": 2, "win": 2}


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
            return rec, os.path.relpath(c, ROOT)
    return None, None


def group(r):
    tame = "W" not in r["value"]["count"]
    rs = r["features"]["race_sensitive"]
    a = r["treb"].startswith("A")
    if rs:
        return "race-sensitive, A-trebuchets" if a else "race-sensitive, B-trebuchets"
    if not tame:
        return "BIG-valued, race-insensitive"
    return "tame, race-insensitive, A-trebuchets" if a else "tame, race-insensitive, B-trebuchets"


def cheb(a, b):
    return max(abs(a % 8 - b % 8), abs(a // 8 - b // 8))


def main():
    rows = json.load(open(os.path.join(SUITE, "results.json")))
    out_rows = []
    for r in rows:
        pos = mg.parse_fen(r["fen"])
        rec, src = cached(r["fen"])
        flags = {}
        if rec and rec.get("data"):
            for m in rec["data"].get("moves", []):
                flags[m["uci"]] = {"stalemate": m.get("stalemate"), "checkmate": m.get("checkmate"),
                                   "dtz": m.get("dtz")}
        enemy = "p" if r["stm"] == "W" else "P"
        enemy_pawns = [s for s, pc in enumerate(pos.board) if pc == enemy and s % 8 < 4]
        own = "P" if r["stm"] == "W" else "p"
        ksq = mg.sq(r["king_moves"][0][:2]) if r["king_moves"] else None
        kms = []
        for u in r["king_moves"]:
            to = mg.sq(u[2:4])
            res = r["king_move_results"][u]
            kms.append({
                "uci": u, "san": r["san"][u], "real_result_for_mover": res,
                "convention": "loss",
                "convention_wrong": res not in LOSSES,
                "dest_file": "abcdefgh"[to % 8],
                "dist_to_nearest_enemy_component_pawn_before": min((cheb(ksq, s) for s in enemy_pawns), default=None),
                "dist_to_nearest_enemy_component_pawn_after": min((cheb(to, s) for s in enemy_pawns), default=None),
                "immediate_stalemate": flags.get(u, {}).get("stalemate"),
            })
        pawn = [u for u in r["tb_moves"] if u not in r["king_moves"]]
        cnt = r["rules"]["count"]
        best_pawn = max((RANK[r["tb_moves"][u]] for u in pawn), default=0)  # no pawn move: the convention scores a loss
        best_king = max((RANK[r["tb_moves"][u]] for u in r["king_moves"]), default=None)
        conv_root = "win" if cnt["pred_win"] else "loss"
        real_root = "win" if r["tb_root"] in WINS else "loss" if r["tb_root"] in LOSSES else r["tb_root"]
        km_wrong = [k for k in kms if k["convention_wrong"]]
        out_rows.append({
            "id": r["id"], "tier": r["tier"], "group": group(r), "treb": r["treb"], "stm": r["stm"],
            "fen": r["fen"], "component": r["component"], "cgt_value": r["value"],
            "value_class": r["features"]["class"], "race_sensitive": r["features"]["race_sensitive"],
            "real_root": r["tb_root"],
            "convention_root_count_rule": conv_root,
            "convention_winning_moves_count_rule": sorted(r["san"][u] for u in cnt["pred_win"]),
            "real_winning_moves": sorted(r["san"][u] for u in r["tb_win"]),
            "real_drawing_moves": sorted(r["san"][u] for u in r["tb_draw"]),
            "pawn_moves": {r["san"][u]: r["tb_moves"][u] for u in sorted(pawn)},
            "king_moves": kms,
            "king_moves_drawing": [k["san"] for k in kms if k["real_result_for_mover"] == "draw"],
            "king_moves_winning": [k["san"] for k in kms if k["real_result_for_mover"] in WINS],
            "king_moves_all_lose": r["king_moves_all_lose"],
            "frozen_king_wrong": bool(km_wrong),
            "king_move_changes_outcome": (best_king is not None and best_king > best_pawn),
            "root_agree_count_rule": cnt["root_agree"],
            "pawn_win_set_agree_count_rule": cnt["pawn_set_agree"],
            "tb_record_source": src,
        })

    def stats(grp):
        km = collections.Counter(k["real_result_for_mover"] for x in grp for k in x["king_moves"])
        return {"positions": len(grp), "king_moves": sum(km.values()), "king_move_results": dict(km),
                "positions_all_king_moves_lose": sum(x["king_moves_all_lose"] for x in grp),
                "positions_frozen_king_wrong": sum(x["frozen_king_wrong"] for x in grp),
                "positions_where_a_king_move_beats_every_pawn_move": sum(x["king_move_changes_outcome"] for x in grp)}

    groups = collections.OrderedDict()
    for g in ("tame, race-insensitive, A-trebuchets", "tame, race-insensitive, B-trebuchets",
              "BIG-valued, race-insensitive", "race-sensitive, A-trebuchets", "race-sensitive, B-trebuchets"):
        groups[g] = stats([x for x in out_rows if x["group"] == g])
    headline = [x for x in out_rows if x["group"] == "tame, race-insensitive, A-trebuchets"]
    hs = groups["tame, race-insensitive, A-trebuchets"]
    assert hs["positions"] == 94 and hs["king_moves"] == 449, hs
    assert hs["king_move_results"].get("draw") == 41 and hs["king_move_results"].get("win") == 7, hs
    stalemates = [(x["id"], k["san"]) for x in out_rows for k in x["king_moves"] if k["immediate_stalemate"]]
    out = {
        "_about": {
            "item": "A8 test data: real-chess results of every king move in the engine suite (engine/suite/results.json), "
                    "against the frozen-king convention's prediction that every king move loses.",
            "source": "engine/suite/results.json (275 probed positions, Lichess 7-man tablebase); king-move results are "
                      "the tablebase result for the MOVER. Flags 'immediate_stalemate' read offline from the cached "
                      "Lichess records (engine/suite/tbcache, realchess/cache).",
            "headline_group": "tame, race-insensitive, A-trebuchets: 94 positions, 449 king moves, 41 draw, 7 win "
                              "(engine/suite/README.md, RESULTS.md section 1).",
            "groups": "as in engine/suite/summarize.py: tame = no +-BIG in the CGT(count) value; race-sensitive = the "
                      "CGT winning set depends on RACE_RULE; A_r trebuchet: W Pg r, B Pg r+1, WK f r+1, BK h r; "
                      "B_r: same pawns, WK h r+1, BK f r.",
            "fields": {
                "convention": "the model's prediction for the king move: always 'loss' (it drops the mover's g-pawn).",
                "frozen_king_wrong": "true iff at least one king move does not lose in real chess.",
                "king_move_changes_outcome": "true iff the best king move is strictly better for the mover than the best "
                                             "pawn move, i.e. the frozen-king assumption alone makes the predicted outcome wrong.",
                "dist_to_nearest_enemy_component_pawn_*": "Chebyshev distance from the king to the nearest enemy pawn on "
                                                          "files a-d, before / after the move (derived from the FEN).",
                "convention_root_count_rule": "'win' iff CGT(count) predicts a winning pawn move; draws are never predicted.",
            },
        },
        "summary": {
            "positions": len(out_rows),
            "by_group": groups,
            "all_positions": stats(out_rows),
            "headline_group_positions_with_nonlosing_king_moves": [x["id"] for x in headline if x["frozen_king_wrong"]],
            "positions_where_a_king_move_beats_every_pawn_move": [x["id"] for x in out_rows if x["king_move_changes_outcome"]],
            "king_moves_giving_immediate_stalemate": stalemates,
        },
        "positions": out_rows,
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(json.dumps(out["summary"], indent=1))


if __name__ == "__main__":
    main()
