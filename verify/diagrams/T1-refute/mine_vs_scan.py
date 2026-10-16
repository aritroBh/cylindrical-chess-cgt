"""Compare the worker's hand FENs (MINE in verify/diagrams/rerun.py, read with ast, not imported)
with the pixel scan in pixscan.py (all pieces, incl. kings).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/T1-refute/mine_vs_scan.py"""
import ast, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import pixscan
src = (ROOT / "verify/diagrams/rerun.py").read_text()
MINE = None
for n in ast.parse(src).body:
    if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "MINE" for t in n.targets):
        MINE = ast.literal_eval(n.value)
def fen_pieces(fen):
    out = {}
    for i, row in enumerate(fen.split("/")):
        f = 0
        for ch in row:
            if ch.isdigit(): f += int(ch)
            else:
                out["abcdefgh"[f] + str(8 - i)] = ("W" if ch.isupper() else "B") + ch.upper(); f += 1
    return out
allok = True
for key, fn in pixscan.DIAGRAMS:
    _, pcs, _ = pixscan.scan(pixscan.PICS / fn)
    scan = {s: v[0] + v[1] for s, v in pcs.items()}
    mine = fen_pieces(MINE[key])
    ok = scan == mine
    allok &= ok
    print(f"{key} {fn}: {'MATCH' if ok else 'DIFF'} ({len(scan)} pieces)" + ("" if ok else f" scan={scan} mine={mine}"))
print("ALL MATCH" if allok else "SOME DIFF")
