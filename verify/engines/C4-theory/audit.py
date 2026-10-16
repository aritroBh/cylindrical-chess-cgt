"""Theory-lens audit of claim C4 (engine/suite). Read-only on worker files.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C4-theory/audit.py
"""
import collections, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "engine", "suite"))
import build_suite as BS  # noqa

rows = json.load(open(BS.RESULTS))
WINS, LOSSES = BS.WINS, BS.LOSSES
print("rows compared:", len(rows))
ver = [r for r in rows if r["tb_root"] in WINS and r["rules"]["count"]["win_set_agree"]]
print("verified:", len(ver), "stm:", collections.Counter(r["stm"] for r in ver))
# all disagreements under count (winning set differs OR root differs)
dis_all = [r for r in rows if not r["rules"]["count"]["win_set_agree"]]
print("rows whose count win-set != TB win-set:", len(dis_all))
in_file = [r for r in rows if not (r["tb_root"] in WINS and r["rules"]["count"]["win_set_agree"])
           and (r["tb_win"] or r["tb_draw"]) and not (r["rules"]["count"]["win_set_agree"] and r["tb_root"] in LOSSES)]
print("rows written to cgt_disagree.epd:", len(in_file))
omitted = [r for r in dis_all if r not in in_file]
print("count-disagreements NOT in cgt_disagree.epd:", len(omitted))
for r in omitted:
    print("   ", r["id"], r["tier"], r["fen"], "tb_root", r["tb_root"], "pred_win", r["rules"]["count"]["pred_win"])
# rows in disagree file that actually agree on win set (root draw but CGT says loss with empty win set)
agree_but_in = [r for r in in_file if r["rules"]["count"]["win_set_agree"]]
print("rows in disagree file whose win set agrees (TB draw root, CGT predicted loss):", len(agree_but_in))
print("disagree file by TB root:", collections.Counter(r["tb_root"] for r in in_file))
# rows excluded from both files
both_out = [r for r in rows if r not in ver and r not in in_file]
print("rows in neither file:", len(both_out), collections.Counter((r["tb_root"], r["rules"]["count"]["win_set_agree"]) for r in both_out))

print("\n--- verified set: how exact is the model beyond the winning set? ---")
print("every move's result exact (W/L, no draws):", sum(r["rules"]["count"]["all_moves_agree"] for r in ver))
print("all king moves lose:", sum(r["king_moves_all_lose"] for r in ver))
km = collections.Counter(v for r in ver for v in r["king_move_results"].values())
print("king-move TB results in verified positions:", dict(km))
pawn_draws = 0; pawn_draw_pos = 0
for r in ver:
    pd = [u for u in r["tb_draw"] if u not in r["king_moves"]]
    pawn_draws += len(pd); pawn_draw_pos += bool(pd)
print("predicted-losing pawn moves that TB rates a draw:", pawn_draws, "in", pawn_draw_pos, "positions")

print("\n--- value labels depend on race rule? ---")
vdep = [r for r in ver if len(set(r["value"].values())) > 1]
print("verified positions whose CGT value differs between race rules:", len(vdep))
cc = collections.Counter()
for r in vdep:
    cls = {ru: BS.value_class(v) for ru, v in r["value"].items()}
    cc[(cls["count"], cls["mover"], cls["opponent"])] += 1
    if len(set(cls.values())) > 1:
        pass
for k, n in cc.most_common():
    print("   class (count, mover, opponent):", k, n)
cls_change = [r for r in vdep if len({BS.value_class(v) for v in r["value"].values()}) > 1]
print("verified positions whose value CLASS differs between race rules:", len(cls_change))
print("race_sensitive (win set) in verified:", sum(r["features"]["race_sensitive"] for r in ver))
byclass = collections.defaultdict(list)
for r in ver:
    byclass[r["features"]["class"]].append(r)
for k, g in byclass.items():
    print(f"   {k}: {len(g)}; value rule-dependent {sum(len(set(r['value'].values()))>1 for r in g)}; "
          f"class rule-dependent {sum(len({BS.value_class(v) for v in r['value'].values()})>1 for r in g)}; "
          f"distinct values {len({r['value']['count'] for r in g})}; distinct components {len({(r['component'], r['stm']) for r in g})}")
print("\n--- distinct values per class (count) ---")
for k, g in byclass.items():
    print(k, sorted(collections.Counter(r["value"]["count"] for r in g).items()))
print("\n--- distinct components in verified ---")
print("distinct (component, stm):", len({(r['component'], r['stm']) for r in ver}))
print("by trebuchet:", collections.Counter(r["treb"] for r in ver))
print("by tier:", collections.Counter(r["tier"] for r in ver))
print("men count:", collections.Counter(4 + len(r['component'].replace('W:','').replace('B:','').replace('/',' ').split()) for r in ver))
print("\n--- decided row ---")
for r in ver:
    if r["features"]["class"] == "decided":
        print(json.dumps({k: r[k] for k in ("id", "fen", "component", "value", "tb_win", "tb_moves")}))
