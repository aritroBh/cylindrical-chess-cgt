import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e2e as E
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
from lemmas import common
tot = diff = 0; bad_cert = 0; certroots=0
for spec in sys.argv[1:]:
    tag, W, H = spec.split(':'); W=int(W); H=int(H)
    board = Board(W, H, True, True)
    res = {}
    for ln in open(f"{tag}.res"):
        if ' | ' in ln:
            a, b = ln.rstrip().split(' | '); res[a] = b.split()
    for ln in open(f"{tag}.pos"):
        L = ln.strip(); toks = L.split(); stm = toks[-2].upper()
        w = [pawns.sq(t[1:]) for t in toks[:-2] if t[0] == 'P']; b = [pawns.sq(t[1:]) for t in toks[:-2] if t[0] == 'p']
        pos = Pos(frozenset(w), frozenset(b), None)
        dw = common.alt_winner(board, pos, stm) == 'W'
        fw = res[L][0] == 'W'
        tot += 1
        memo = {}
        ac = E.all_cert(board, pos, stm, W, H, memo)
        if ac: certroots += 1
        if dw != fw:
            diff += 1
            if ac: bad_cert += 1; print("DIFF with all certified", L)
print("lines", tot, "differ from D:", diff, "all-certified lines", certroots, "differ AND all-certified", bad_cert)
