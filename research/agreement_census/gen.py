"""Generate the census position set for one board: every pawn placement P (1..3 pawns per side, as fits on the
P files) beside the board's frozen trebuchet Z, both sides to move, plus cylcgt's model value of P alone
(default ep-aware passed test; cylcgt is imported read-only).
Usage: python3 -I gen.py <cyl|flat>:WxH <layout: orig|compact> OUTDIR"""
import itertools, json, os, sys
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
sys.path.insert(0, ROOT)
from cylcgt import cgt, pawns
assert pawns.PASSED_RESPECTS_EP is True   # default model: e.p.-aware, count rule
FILES = "abcdefgh"
nm = lambda f, r: f"{FILES[f]}{r}"
spec, layout_kind, outdir = sys.argv[1:4]
mode = sys.argv[4] if len(sys.argv) > 4 else "le2"   # le2: <=2/<=2 ; ext3: 3 pawns on a side
kind, size = spec.split(":"); W, H = map(int, size.split("x")); ep = True
r = H // 2
if kind == "cyl":
    z = [f"P{nm(0,r)}", f"p{nm(0,r+1)}", f"K{nm(W-1,r+1)}", f"k{nm(1,r)}"]
    pfiles = list(range(3, W-2)) if layout_kind == "orig" else list(range(2, W-1))
else:
    z = [f"P{nm(W-2,r)}", f"p{nm(W-2,r+1)}", f"K{nm(W-3,r+1)}", f"k{nm(W-1,r)}"]
    pfiles = list(range(0, W-4))
sqs = [(f, rk) for f in pfiles for rk in range(2, H)]
COUNTS = [(1,1),(2,1),(1,2),(2,2)] if mode == "le2" else [(a,b) for a in (1,2,3) for b in (1,2,3) if max(a,b) == 3]
os.makedirs(outdir, exist_ok=True)
off = pfiles[0]
board = pawns.Board(len(pfiles), H, False, ep)
rows, lines = [], []
for nw, nb in COUNTS:
    if nw + nb > len(sqs): continue
    for ws in itertools.combinations(sqs, nw):
        rest = [s for s in sqs if s not in ws]
        for bs in itertools.combinations(rest, nb):
            pos = pawns.Pos(frozenset((f-off, rk) for f, rk in ws), frozenset((f-off, rk) for f, rk in bs))
            try:
                g = pawns.value(board, pos); val, outc = cgt.show(g), cgt.outcome(g)
            except pawns.RaceError:
                val, outc = None, "race"
            base = " ".join(z + [f"P{nm(*s)}" for s in ws] + [f"p{nm(*s)}" for s in bs])
            rows.append({"P": "W: " + " ".join(nm(*s) for s in ws) + " / B: " + " ".join(nm(*s) for s in bs),
                         "nw": nw, "nb": nb, "model_value": val, "model_class": outc, "wtm": base+" w -", "btm": base+" b -"})
            lines += [base+" w -", base+" b -"]
open(f"{outdir}/positions.txt", "w").write("\n".join(lines) + "\n")
open(f"{outdir}/rows.jsonl", "w").write("".join(json.dumps(x)+"\n" for x in rows))
json.dump({"board": spec, "trebuchet": z, "pfiles": [FILES[f] for f in pfiles], "layout": layout_kind,
           "rows": len(rows), "positions": len(lines)}, open(f"{outdir}/meta.json", "w"))
print(spec, layout_kind, "pfiles", [FILES[f] for f in pfiles], "rows", len(rows), "positions", len(lines))
