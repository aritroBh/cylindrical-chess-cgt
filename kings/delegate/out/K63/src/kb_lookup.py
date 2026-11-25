"""K63 question 1: is there exact chess evidence in the repository for the F-group positions?  Looks every input
position and every child of it up in the offline knowledge base of cached tablebase records (realchess/kb.py; read
only, no network).  Run from the repository root: PYTHONDONTWRITEBYTECODE=1 .venv/bin/python <this> <positions file>"""
import sys
sys.path.insert(0, '.')
import chess  # noqa: E402
from realchess import kb as KBM  # noqa: E402


def fen_of(line):
    t = line.split()
    stm, ep = t[-2], t[-1]
    b = chess.Board(None)
    for x in t[:-2]:
        piece = chess.Piece.from_symbol(x[0])
        b.set_piece_at(chess.parse_square(x[1:]), piece)
    b.turn = stm == 'w'
    b.ep_square = chess.parse_square(ep) if ep != '-' else None
    return b


kb = KBM.default_kb()
print('KB:', kb.stats())
hits = tot = 0
for line in open(sys.argv[1]):
    line = line.strip()
    if not line:
        continue
    b = fen_of(line)
    cands = [('root', b.fen())] + [(b.san(m), (b.copy(), m)) for m in b.legal_moves]
    for name, x in cands:
        if isinstance(x, tuple):
            bb, m = x; bb.push(m); fen = bb.fen()
        else:
            fen = x
        tot += 1
        c = kb.category(fen)
        if c is not None:
            hits += 1
            print('HIT', line, name, fen, c)
print('%d positions looked up (inputs and their children), %d found in the KB' % (tot, hits))
