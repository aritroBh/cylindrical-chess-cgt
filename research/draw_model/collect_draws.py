"""Collect draw positions from realchess and engine suite; write draws.json."""
import json, os
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
out = {"real_nodes": [], "draw_terminals": [], "proven_king_moves": [], "suite_draw_roots": []}

# 13 real-draw nodes
d = json.load(open(os.path.join(ROOT, "realchess/results/comp_Wa2c2_Bb7d7_nodes_pure_offline.json")))
for n in d["nodes"]:
    if "draw" in str(n.get("real_class", "")).lower():
        out["real_nodes"].append({
            "component": n["component"],
            "fen": n["W_fen"],
            "real_class": n["real_class"],
        })

# 3 draw terminals from REPORT
out["draw_terminals"] = [
    "W: a4 / B: b7 c6",
    "W: a5 / B: b7 c5",
    "W: c4 / B: a6 d6",
]

# 6 proven drawing king moves
kp = json.load(open(os.path.join(ROOT, "realchess/results/comp_Wa2c2_Bb7d7_kings_pure_offline.json")))
for r in kp["non_losing"]:
    if r["verdict"] == "draws":
        out["proven_king_moves"].append({
            "fen": r["fen"], "component": r["component"], "king_move": r["king_move"],
        })

# suite draw roots
su = json.load(open(os.path.join(ROOT, "engine/suite/results.json")))
for x in su:
    if x.get("tb_root") == "draw":
        out["suite_draw_roots"].append({"id": x["id"], "fen": x["fen"], "component": x.get("component")})

with open("draws.json", "w") as f:
    json.dump(out, f, indent=2)
print("real_nodes", len(out["real_nodes"]))
print("proven_king_moves", len(out["proven_king_moves"]))
print("suite_draw_roots", len(out["suite_draw_roots"]))