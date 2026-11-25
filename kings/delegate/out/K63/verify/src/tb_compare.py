"""K63 referee: compare the investigator's cap-1 chess bounds (logs/F*_chess_table.txt) with the
tablebase categories (verify/logs/tb_results.json, from tb_probe.py) and print the tables for VERIFY.md.
Values in White's view.  Without the 50-move rule: win, cursed-win, maybe-win count as wins for the
side named; loss, blessed-loss, maybe-loss as losses.  With it: only win / loss are decisive.
Run from the repository root (no network):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K63/verify/src/tb_compare.py
"""
import json, re

V = "kings/delegate/out/K63/verify"
INV = "kings/delegate/out/K63/logs"
ORD = {"L": 0, "D": 1, "W": 2}

def wview(cat, stm, rule50):
    """category for side `stm` to move -> W/D/L in White's view."""
    win = {"win", "cursed-win", "maybe-win"} if not rule50 else {"win"}
    loss = {"loss", "blessed-loss", "maybe-loss"} if not rule50 else {"loss"}
    if cat in win: return "W" if stm == "w" else "L"
    if cat in loss: return "L" if stm == "w" else "W"
    if cat in ("draw", "cursed-win", "blessed-loss", "maybe-win", "maybe-loss"): return "D"
    raise ValueError(cat)

res = json.load(open(f"{V}/logs/tb_results.json"))
tb = {(r["pieces"], r["stm"]): r for r in res}

def norm(pcs):
    return " ".join(sorted(pcs.split()))

tbn = {(norm(k[0]), k[1]): v for k, v in tb.items()}
special = []
for r in res:
    for cat in [r["category"]] + [m[1] for m in r["moves"].values()]:
        if cat not in ("win", "loss", "draw"): special.append((r["group"], r["label"], r["stm"], cat))

print("# 1. Investigator's cap-1 bounds against the tablebase")
nexact = nbound = bad = 0
for g in ("F1", "F2", "F3", "F4"):
    cur = None
    for line in open(f"{INV}/{g}_chess_table.txt"):
        if line.startswith("#"): continue
        m = re.match(r"^(\S.*?) ([wb]) (\S+)\s+value (\S+)", line)
        if m:
            pcs, stm = m.group(1), m.group(2)
            cur = tbn[(norm(pcs), stm)]
            items = [("position", m.group(4), wview(cur["category"], stm, False))]
        else:
            m2 = re.match(r"^\s+(\S+)\s+(\S+)\s", line)
            if not m2: continue
            mv = m2.group(1)[-4:].lower()
            san, cat, _ = cur["moves"][mv]
            stm_after = "b" if cur["stm"] == "w" else "w"
            items = [(mv, m2.group(2), wview(cat, stm_after, False))]
        for what, bnd, tv in items:
            if len(bnd) == 1:
                nexact += 1; ok = bnd == tv
            else:
                a, b = bnd.strip("()").split(","); nbound += 1
                ok = ORD[a] >= ORD[tv] >= ORD[b]
            if not ok:
                bad += 1
                print(f"  DISAGREE {g} {cur['pieces']} {cur['stm']} {what}: cap1 {bnd} tablebase {tv}")
print(f"  exact cap-1 values compared: {nexact}; bound pairs compared: {nbound}; disagreements: {bad}")
print(f"  categories other than win/draw/loss anywhere (position or move): {special if special else 'none'}")

print("\n# 2. Tablebase tables (White's view; 50-move rule ignored = with it, since no special category occurs)")
for r in res:
    stm = r["stm"]; after = "b" if stm == "w" else "w"
    mv = ", ".join(f"{san} {wview(cat, after, False)}" for _, (san, cat, _) in r["moves"].items())
    print(f"  {r['group']:8s} {r['label']:5s} {r['pieces']:28s} {'White' if stm == 'w' else 'Black'} to move: "
          f"{r['category']:5s} = {wview(r['category'], stm, False)} | {mv}")
