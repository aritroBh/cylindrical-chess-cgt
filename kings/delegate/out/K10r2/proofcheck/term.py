import sys, os, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e2e as E
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
from lemmas import common
mode = sys.argv[1]
if mode == 'gen':
    seed, N, W, H, maxp, out = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    board = Board(W, H, True, True)
    rng = random.Random(seed)
    terms = {}
    memo = set()
    def walk(pos, stm):
        if (pos, stm) in memo: return
        memo.add((pos, stm))
        lpos, rpos = common.split_ep(pos)
        src = lpos if stm == 'W' else rpos
        other = 'B' if stm == 'W' else 'W'
        for c in pawns.moves(board, src, stm):
            t = common.terminal(board, c)
            if t is not None:
                b, kind = E.credit(board, c, stm)
                ok = E.certified(board, c, stm, W, H)
                terms[(c, other)] = (b, kind, 'M' if b == stm else 'N', ok)
            else:
                walk(c, other)
    for _ in range(N):
        pos = E.gen_root(rng, W, H, maxp)
        if common.terminal(board, pos) is not None: continue
        walk(pos, 'W'); walk(pos, 'B')
    info = []
    with open(out + '.pos', 'w') as fh:
        for (c, stm), (b, kind, who, ok) in terms.items():
            toks = ["Ka1", f"ka{H}"] + [f"P{pawns.name(s)}" for s in sorted(c.white)] + [f"p{pawns.name(s)}" for s in sorted(c.black)]
            ep = '-' if c.ep is None else pawns.name(c.ep[0])
            L = " ".join(toks) + f" {stm.lower()} {ep}"
            fh.write(L + "\n"); info.append((L, b, kind, who, ok))
    json.dump(info, open(out + '.json', 'w'))
    print(len(info), "terminals", file=sys.stderr)
else:
    out = sys.argv[2]
    info = json.load(open(out + '.json'))
    res = {}
    for ln in open(out + '.res'):
        if ' | ' in ln:
            a, b = ln.rstrip().split(' | '); res[a] = b.split()
    from collections import Counter
    C = Counter(); bad = 0
    for L, b, kind, who, ok in info:
        r = res[L]
        win = (r[0] == ('W' if b == 'W' else 'L'))
        C[(kind, who, ok, win)] += 1
        if ok and not win: bad += 1; print("VIOLATION", L, b, kind, who, r)
    for k in sorted(C): print(k, C[k])
    print("violations", bad)
