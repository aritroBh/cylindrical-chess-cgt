"""Non-visual-model transcription of the 12 board diagrams, from pixels only (stdlib).
For each square: count near-black pixels (piece ink) and pure-white pixels (white-piece fill);
classify empty / white / black; classify pawn vs king by the ink bounding-box width.
Prints a board FEN per diagram and compares with the worker's MINE dict in verify/diagrams/rerun.py
and with cylcgt.verify_paper.CLAIMS.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/T1-theory/pixel_transcribe.py
"""
import importlib.util, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pngsample_lib import load, px, isblue  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
PIC = os.path.join(ROOT, 'prior_work', 'Pictures')
FILES = {"2.1": "ZeroGame1", "2.2": "ZeroGame2", "2.3": "ZeroGame3", "3.1": "OneGame1", "3.2": "TwoGame1",
         "4.1": "StarGame1", "4.2": "UpGame1", "4.3": "TinyGame1", "5.1": "TrebuchetPosition1",
         "7.1": "ChessPuzzle1", "7.2": "ChessPuzzle2", "7.3": "ChessPuzzle3"}


def board_extent(w, h, bpp, rows):
    xs = [x for x in range(w) if sum(isblue(px(rows, bpp, x, y)) for y in range(0, h, 7)) > 3]
    ys = [y for y in range(h) if sum(isblue(px(rows, bpp, x, y)) for x in range(0, w, 7)) > 3]
    return min(xs), max(xs), min(ys), max(ys)


def transcribe(path):
    w, h, bpp, rows = load(path)
    x0, x1, y0, y1 = board_extent(w, h, bpp, rows)
    sq = (x1 - x0 + 1) / 8
    out = {}
    for r in range(8):
        for f in range(8):
            ink = white = 0
            minx, maxx = 10**9, -1
            for yy in range(int(y0 + r * sq + 0.06 * sq), int(y0 + (r + 1) * sq - 0.06 * sq)):
                for xx in range(int(x0 + f * sq + 0.06 * sq), int(x0 + (f + 1) * sq - 0.06 * sq)):
                    c = px(rows, bpp, xx, yy)
                    if max(c) < 70:
                        ink += 1
                        minx, maxx = min(minx, xx), max(maxx, xx)
                    elif min(c) > 248:
                        white += 1
            area = (0.88 * sq) ** 2
            if ink / area < 0.01:
                continue
            colour = 'B' if ink > white else 'W'  # black glyphs are mostly ink; white glyphs mostly white fill
            width = (maxx - minx + 1) / sq
            kind = 'K' if width > 0.66 else 'P'
            out[(f, 8 - r)] = (colour, kind, round(ink / area, 3), round(white / area, 3), round(width, 2))
    return out


def fen(pcs):
    rows = []
    for rank in range(8, 0, -1):
        s, e = '', 0
        for f in range(8):
            if (f, rank) in pcs:
                if e: s += str(e); e = 0
                c, k = pcs[(f, rank)][:2]
                s += k if c == 'W' else k.lower()
            else:
                e += 1
        if e: s += str(e)
        rows.append(s)
    return '/'.join(rows)


if __name__ == '__main__':
    spec = importlib.util.spec_from_file_location('rerun', os.path.join(ROOT, 'verify', 'diagrams', 'rerun.py'))
    rerun = importlib.util.module_from_spec(spec); spec.loader.exec_module(rerun)
    allok = True
    for key, name in FILES.items():
        pcs = transcribe(os.path.join(PIC, name + '.png'))
        f = fen(pcs)
        ok = f == rerun.MINE[key]
        allok &= ok
        print(f"{key} {name:20s} pixel FEN {f:45s} worker {'MATCH' if ok else 'DIFF ' + rerun.MINE[key]}")
        widths = sorted({v[1] + ':' + str(v[4]) for v in pcs.values()})
        print(f"      piece widths (fraction of square): {widths}")
    print('ALL MATCH' if allok else 'SOME DIFF')
