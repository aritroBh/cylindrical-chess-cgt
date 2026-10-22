"""T33 appendix: every move of both roots (default setting), resulting position and canonical value,
recomputed with cylcgt. Output: research/c3_star2/appendix_moves.txt (printed to stdout as well).
Run: PYTHONPATH=. .venv/bin/python research/c3_star2/appendix.py"""
from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val

ROOTS = [
    ("C3 W a2 a3 b2 / B b7 c6 c7", 3, "W: a2 a3 b2 / B: b7 c6 c7"),
    ("C4 W a4 b2 c2 / B b6 c5 d6 d7", 4, "W: a4 b2 c2 / B: b6 c5 d6 d7"),
]

def main():
    setup("count", True)
    lines = []
    for label, files, text in ROOTS:
        B = pawns.Board(files, 8, True, True)
        P = pawns.Pos.parse(text)
        G = pawns.value(B, P)
        lines.append(f"== {label} (default: count rule, e.p. on, aware test); value {cgt.show(G)}; nimber check *2: {G is cgt.make([cgt.ZERO, cgt.STAR],[cgt.ZERO, cgt.STAR])}")
        for side in ("W", "B"):
            for i, c in enumerate(pawns.moves(B, P, side), 1):
                v = val(B, c, side)
                ep = " [double step: e.p. right for the opponent]" if c.ep else ""
                lines.append(f"  {side}{i:02d}  {c}{ep}")
                lines.append(f"       value: {cgt.show(v)}   outcome {cgt.outcome(v)}")
        lines.append("")
    out = "\n".join(lines)
    print(out, flush=True)
    open("/Users/aritro/Downloads/Research/Chessendgames/research/c3_star2/appendix_moves.txt", "w").write(out + "\n")

if __name__ == "__main__":
    main()
