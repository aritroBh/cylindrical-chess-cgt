"""Write ab.c job lines for every row of the 4 main splits, both sides to move.
Own square parser (files a.. -> 0-based, rank 1..8); cross-checked against bench.board.parse_sq."""
import json, sys
from pathlib import Path
P = Path("/Users/aritro/Downloads/Research/Chessendgames")
sys.path.insert(0, str(P))
from bench import board as bd
out = Path(sys.argv[1]); tcap = sys.argv[2]
def psq(s):
    return (ord(s[0]) - ord('a'), int(s[1:]))
lines, meta = [], []
for sp in ["train", "val", "test", "test_heldout"]:
    for l in (P / "bench/data" / f"{sp}.jsonl").read_text().splitlines():
        r = json.loads(l)
        W = r["board"]["files"]; cyl = r["board"]["cylinder"]
        w = sorted(psq(s) for s in r["white"]); b = sorted(psq(s) for s in r["black"])
        assert w == sorted(bd.parse_sq(s) for s in r["white"]) and b == sorted(bd.parse_sq(s) for s in r["black"])
        assert all(0 <= f < W and 1 <= x <= 8 for f, x in w + b)
        assert len(set(w + b)) == len(w) + len(b)
        # placement string cross-check: rank 8 first
        rowsP = r["placement"].split("/")
        assert len(rowsP) == 8
        for i, rs in enumerate(rowsP):
            rank = 8 - i; f = 0; num = ""
            cells = []
            j = 0
            while j < len(rs):
                c = rs[j]
                if c.isdigit():
                    k = j
                    while k < len(rs) and rs[k].isdigit(): k += 1
                    f += int(rs[j:k]); j = k; continue
                cells.append((c, f, rank)); f += 1; j += 1
            assert f == W, (r["id"], rs)
            for c, ff, rk in cells:
                assert ((ff, rk) in w) if c == "P" else ((ff, rk) in b), (r["id"], c, ff, rk)
        assert sum(1 for x in r["placement"] if x in "Pp") == len(w) + len(b)
        for side in (1, 0):
            lines.append(f"{W} {int(cyl)} {side} 1 0 {tcap} {len(w)} " + " ".join(f"{f} {x}" for f, x in w)
                         + f" {len(b)} " + " ".join(f"{f} {x}" for f, x in b))
            meta.append((r["id"], side, r["outcome"], r["k"]))
out.write_text("\n".join(lines) + "\n")
(out.with_suffix(".meta.json")).write_text(json.dumps(meta))
print(len(lines), "jobs")
