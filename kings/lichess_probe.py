"""Check kpsolve's 8x8 king-group results on the ordinary board against the Lichess
tablebase (ground truth not written by any Claude model).

Uses realchess.probe.Prober (read-only import) with this folder's own cache and
ledger and a hard cap of 20 requests. The shared realchess cache is consulted
first, so positions already fetched cost nothing.

Run from the project root:  python3 kings/lichess_probe.py
Writes kings/results/king_groups_lichess.txt.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from realchess.probe import Prober  # noqa: E402

CATS = {"win": "W", "cursed-win": "W", "maybe-win": "W", "loss": "L", "blessed-loss": "L",
        "maybe-loss": "L", "draw": "D"}
# (label, FEN without side, kpsolve line)
GROUPS = [
    ("7.2 king group", "3k4/3Pp3/4K3/8/8/8/8/8", "Ke6 Pd7 kd8 pe7"),
    ("7.3 as drawn", "6K1/5Pp1/5k2/8/8/8/8/8", "Kg8 Pf7 kf6 pg7"),
    ("7.3, kings as the audit conjectures", "5k2/5Pp1/6K1/8/8/8/8/8", "Kg6 Pf7 kf8 pg7"),
    ("*2 candidate's trebuchet", "8/8/8/5Kp1/6Pk/8/8/8", "Kf5 Pg4 kh4 pg5"),
]


def main():
    os.makedirs(os.path.join(ROOT, "kings", "results", "lichess_cache"), exist_ok=True)
    shared = Prober(cap=0, cache_dir=os.path.join(ROOT, "realchess", "cache"), offline=True)
    mine = Prober(cap=20, cache_dir=os.path.join(ROOT, "kings", "results", "lichess_cache"),
                  ledger=os.path.join(ROOT, "kings", "results", "lichess_ledger.jsonl"), tag="A8-kings")
    kp = {}
    for line in open(os.path.join(ROOT, "kings", "results", "king_groups_8x8.txt")):
        if line.startswith("== "):
            board = line[3:].strip()
        elif "|" in line and board == "flat:8x8":
            pos, res = [p.strip() for p in line.split("|")[:2]]
            kp[pos] = res.split()[0]
    out = ["# kpsolve versus Lichess on the king groups (ordinary 8x8 board)", "",
           "| Group | Side | Lichess | kpsolve | Agree |", "|---|---|---|---|---|"]
    bad = 0
    for label, board, line in GROUPS:
        for stm in "wb":
            fen = f"{board} {stm} - - 0 1"
            try:
                rec = shared.probe(fen)
            except Exception:
                rec = mine.probe(fen)
            cat = CATS.get((rec.get("data") or {}).get("category"), "?")
            if stm == "b":
                cat = {"W": "L", "L": "W", "D": "D"}.get(cat, "?")
            ours = kp.get(f"{line} {stm} -", "?")
            ok = cat == ours
            bad += not ok
            out.append(f"| {label} | {'White' if stm == 'w' else 'Black'} to move | {cat} | {ours} | "
                       f"{'yes' if ok else 'NO'} |")
    out.append("")
    out.append("Values are from White's point of view: W White wins, D draw, L Black wins.")
    path = os.path.join(ROOT, "kings", "results", "king_groups_lichess.txt")
    with open(path, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("\n".join(out))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
