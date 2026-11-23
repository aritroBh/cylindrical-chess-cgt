"""Random-move baseline for the 200 ChessSums engine-test positions. Offline.
Run from repo root: .venv/bin/python research/engine_baselines/baseline_b.py"""
import json, statistics as st, collections, chess
D = "engine/runs/chesssums/"
ids = json.load(open(D + "subset_ids.json"))
meta = {m["id"]: m for m in json.load(open(D + "meta.json"))}
assert len(ids) == 200 and len(set(ids)) == 200
res = {"sf": json.load(open(D + "sf_results.json"))["results"],
       "lc1k": json.load(open(D + "lc0_1k_merged.json"))["results"],
       "lc10k": json.load(open(D + "lc0_10k_merged.json"))["results"]}
rows = []
for i in ids:
    m = meta[i]; b = chess.Board(m["fen"] + " 0 1")
    st_ = b.status() & ~(chess.STATUS_TOO_MANY_WHITE_PAWNS | chess.STATUS_TOO_MANY_BLACK_PAWNS | chess.STATUS_TOO_MANY_WHITE_PIECES | chess.STATUS_TOO_MANY_BLACK_PIECES)
    assert st_ == 0, (i, b.status())  # only >8 pawns / >16 men allowed (engines accept these)
    assert (b.turn == chess.WHITE) == (m["stm"] == "w"), i
    legal = {mv.uci() for mv in b.legal_moves}
    pawn = {mv.uci() for mv in b.legal_moves if b.piece_type_at(mv.from_square) == chess.PAWN}
    sol = set(m["solutions_uci"])
    rows.append(dict(id=i, nlegal=len(legal), npawn=len(pawn), nwin=len(sol), win_legal=len(sol & legal),
                     win_pawn=len(sol & pawn), outcome=m["outcome"], k=m["k"]))
for r in rows[:5]: print(r)
nobad = sum(r["nwin"] != r["win_legal"] for r in rows)
def mean(x): return sum(x) / len(x)
def dist(x): return (min(x), st.median(x), max(x))
out = {}
out["n"] = len(rows)
out["illegal_winning_moves_positions"] = nobad
out["no_winning_move_positions"] = sum(r["nwin"] == 0 for r in rows)
out["no_winning_by_outcome"] = dict(collections.Counter(r["outcome"] for r in rows if r["nwin"] == 0))
out["outcome_counts"] = dict(collections.Counter(r["outcome"] for r in rows))
out["rand_legal_all200"] = mean([r["win_legal"] / r["nlegal"] for r in rows])
out["rand_pawn_all200"] = mean([r["win_pawn"] / r["npawn"] for r in rows if r["npawn"]])
out["pawn_positions_with_no_pawn_move"] = sum(r["npawn"] == 0 for r in rows)
w = [r for r in rows if r["nwin"] > 0]
out["rand_legal_with_winning"] = mean([r["win_legal"] / r["nlegal"] for r in w])
out["rand_pawn_with_winning"] = mean([r["win_pawn"] / r["npawn"] for r in w])
out["n_with_winning"] = len(w)
out["nlegal_min_med_max"] = dist([r["nlegal"] for r in rows])
out["nwin_min_med_max_all"] = dist([r["nwin"] for r in rows])
out["nwin_min_med_max_with_winning"] = dist([r["nwin"] for r in w])
out["npawn_min_med_max"] = dist([r["npawn"] for r in rows])
out["winning_moves_nonpawn"] = sum(r["win_legal"] - r["win_pawn"] for r in rows)
# engines
eng = {}
for name, lst in [("SF 1k", [r for r in res["sf"] if r["limit"] == "nodes 1000"]),
                  ("SF 10k", [r for r in res["sf"] if r["limit"] == "nodes 10000"]),
                  ("SF 100k", [r for r in res["sf"] if r["limit"] == "nodes 100000"]),
                  ("SF 1M", [r for r in res["sf"] if r["limit"] == "nodes 1000000"]),
                  ("Lc0 1k", res["lc1k"]), ("Lc0 10k", res["lc10k"])]:
    d = {r["id"]: r for r in lst}
    assert set(d) == set(ids), name
    solved_flag = sum(d[i]["solved"] for i in ids)
    recomputed = sum(d[i]["best"] in set(meta[i]["solutions_uci"]) for i in ids)
    onw = sum(d[i]["solved"] for i in ids if meta[i]["solutions_uci"])
    nonw_scored_solved = sum(d[i]["solved"] for i in ids if not meta[i]["solutions_uci"])
    eng[name] = dict(solved=solved_flag, recomputed=recomputed, pct=100 * solved_flag / 200,
                     solved_among_with_winning=onw, pct_among_with_winning=100 * onw / len(w),
                     solved_among_no_winning=nonw_scored_solved)
out["engines"] = eng
exp_legal = sum(r["win_legal"] / r["nlegal"] for r in rows)
exp_pawn = sum(r["win_pawn"] / r["npawn"] for r in rows if r["npawn"])
out["expected_correct_random_legal"] = exp_legal
out["expected_correct_random_pawn"] = exp_pawn
for n, e in eng.items():
    e["ratio_vs_random_legal"] = e["solved"] / exp_legal
    e["ratio_vs_random_pawn"] = e["solved"] / exp_pawn
lw = [r for r in rows if r["win_legal"] > 0]
out["n_with_legal_winning"] = len(lw)
out["positions_all_winning_illegal"] = sum(1 for r in rows if r["nwin"] > 0 and r["win_legal"] == 0)
out["nwin_legal_min_med_max_all"] = dist([r["win_legal"] for r in rows])
out["rand_legal_with_legal_winning"] = mean([r["win_legal"] / r["nlegal"] for r in lw])
out["rand_pawn_with_legal_winning"] = mean([r["win_pawn"] / r["npawn"] for r in lw])
lwids = {r["id"] for r in lw}
lims = {"SF 1k": ("sf", "nodes 1000"), "SF 10k": ("sf", "nodes 10000"), "SF 100k": ("sf", "nodes 100000"),
        "SF 1M": ("sf", "nodes 1000000"), "Lc0 1k": ("lc1k", None), "Lc0 10k": ("lc10k", None)}
for n, (k, lim) in lims.items():
    sv = sum(r["solved"] for r in res[k] if (lim is None or r["limit"] == lim) and r["id"] in lwids)
    eng[n]["solved_among_legal_winning"] = sv
    eng[n]["pct_among_legal_winning"] = 100 * sv / len(lw)
json.dump(dict(summary=out, rows=rows), open("research/engine_baselines/baseline_b.json", "w"), indent=1)
print(json.dumps(out, indent=1))
