import sys, os, itertools, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e2e as E
chk = E.chk
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
from lemmas import common
W, H, maxp, flo, fhi, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
board = Board(W, H, True, True)
sqs = [(f, r) for f in range(flo, fhi+1) for r in range(2, H)]
roots = []
for a in range(1, maxp+1):
    for wp in itertools.combinations(sqs, a):
        rest = [s for s in sqs if s not in wp]
        for b in range(1, maxp+1):
            for bp in itertools.combinations(rest, b):
                pos = Pos(frozenset(wp), frozenset(bp), None)
                if common.terminal(board, pos) is not None: continue
                roots.append(pos)
print(len(roots), "roots without passer", file=sys.stderr)
tmemo = {}
def term_val(c, mover):
    k = (c, mover)
    if k not in tmemo:
        b, kind = E.credit(board, c, mover)
        tmemo[k] = (b, E.certified(board, c, mover, W, H))
    return tmemo[k]
cmemo = {}
def cons(pos, stm, X):
    key = (pos, stm, X)
    if key in cmemo: return cmemo[key]
    lpos, rpos = common.split_ep(pos)
    src = lpos if stm == 'W' else rpos
    other = 'B' if stm == 'W' else 'W'
    vals = []
    for c in pawns.moves(board, src, stm):
        t = common.terminal(board, c)
        if t is not None:
            b, cert = term_val(c, stm)
            vals.append(b == X and cert)
        else:
            vals.append(cons(c, other, X))
    if stm == X: r = any(vals)
    else: r = all(vals)   # empty -> True (opponent has no move: loses)
    cmemo[key] = r
    return r
def line(pos, stm):
    toks = ["Ka1", f"ka{H}"] + [f"P{pawns.name(s)}" for s in sorted(pos.white)] + [f"p{pawns.name(s)}" for s in sorted(pos.black)]
    return " ".join(toks) + f" {stm.lower()} -"
items = []
with open(out + '.pos', 'w') as fh:
    for pos in roots:
        for stm in 'WB':
            L = line(pos, stm)
            cw = cons(pos, stm, 'W'); cb = cons(pos, stm, 'B')
            items.append((L, cw, cb)); fh.write(L + "\n")
json.dump(items, open(out + '.json', 'w'))
print(len(items), "lines;", sum(1 for i in items if i[1]), "cons white wins;", sum(1 for i in items if i[2]), "cons black wins", file=sys.stderr)
