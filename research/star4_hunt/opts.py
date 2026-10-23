import sys
from cylcgt import pawns, cgt
def run(files, text, wrap=False, depth=1, split=False):
    b = pawns.Board(files, 8, wrap, True)
    if not split:
        pawns.components = lambda bd, p: [p]
    pos = pawns.Pos.parse(text)
    g = pawns.value(b, pos)
    print(text, '=>', cgt.show(g))
    def short(x):
        s = cgt.show(x)
        return s if len(s) < 60 else s[:57] + '...'
    for side in 'WB':
        pos2 = pos
        for p in pawns.moves(b, pos, side):
            v = pawns._child(b, p, side)
            print(' ', side, '->', p, ':', short(v))
if __name__ == '__main__':
    run(int(sys.argv[1]), sys.argv[2])
