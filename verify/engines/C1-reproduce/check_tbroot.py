"""Independent check of tb_root in engine/suite/results.json against the raw on-disk Lichess cache.
Reads cache files directly (no network, no writes). Also checks root/move-category consistency."""
import hashlib, json, os, sys
from realchess import movegen
ROOT = os.getcwd()
DIRS = [os.path.join(ROOT, "realchess", "cache"), os.path.join(ROOT, "engine", "suite", "tbcache")]
rows = json.load(open("engine/suite/results.json"))
bad, incons, missing = [], [], 0
for r in rows:
    key = movegen.normal_fen(r["fen"])
    h = hashlib.sha256(key.encode()).hexdigest()
    rec = None
    for d in DIRS:
        p = os.path.join(d, h[:2], h + ".json")
        if os.path.exists(p):
            rec = json.load(open(p)); break
    if rec is None or rec.get("fen") != key:
        missing += 1; continue
    data = rec["data"]
    root = data["category"]
    if root != r["tb_root"]:
        bad.append((r["id"], root, r["tb_root"]))
    if key.split()[1] != ("w" if r["stm"] == "W" else "b"):
        bad.append((r["id"], "stm mismatch", key))
    cats = [m["category"] for m in data["moves"]]
    # root win <=> some move leaves opponent (side to move after) in loss
    if root in ("win", "cursed-win"):
        if not any(c in ("loss", "blessed-loss") for c in cats): incons.append((r["id"], root, cats))
    elif root in ("loss", "blessed-loss"):
        if not all(c in ("win", "cursed-win") for c in cats): incons.append((r["id"], root, cats))
    elif root == "draw":
        if any(c in ("loss", "blessed-loss") for c in cats) or not any(c == "draw" for c in cats):
            incons.append((r["id"], root, cats))
print("rows", len(rows), "missing", missing, "tb_root mismatches", len(bad), bad[:5], "inconsistent", len(incons), incons[:5])
