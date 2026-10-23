#!/usr/bin/env python3
"""Referee's end-to-end check of P11 / Corollary 2.11a (own code).
gen SEED N W H MAXP OUT : random roots (kings parked a1/aH, pawns on files c..W-2), no passer, keep those
   whose D-game has every passer/race terminal certified; write OUT.pos (w and b lines) and OUT.json (D-outcomes).
cmp OUT : compare with kpsolve results OUT.res
"""
import sys, random, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
from lemmas import common
import importlib.util
spec = importlib.util.spec_from_file_location("chk", os.path.join(os.path.dirname(os.path.abspath(__file__)), "chk.py"))
# chk.py runs main() on import; guard by setting argv
_argv = sys.argv; sys.argv = ["x", "none"]
try:
    chk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(chk)
except SystemExit:
    pass
sys.argv = _argv

def to_pos(pos, W, H, stm):
    ep = None
    if pos.ep is not None:
        ep = pos.ep[0]
    return dict(wk=(0, 1), bk=(0, H), wp=frozenset(pos.white), bp=frozenset(pos.black), stm=stm, ep=ep)

def credit(board, pos, mover):
    wp, bp = pawns.passed(board, pos, "W"), pawns.passed(board, pos, "B")
    if not wp and not bp: return None, None
    if wp and not bp: return 'W', 'single'
    if bp and not wp: return 'B', 'single'
    other = "B" if mover == "W" else "W"
    w = other if pawns.promote_distance(board, pos, other) <= pawns.promote_distance(board, pos, mover) else mover
    return w, 'race'

stats = {}
def certified(board, pos, mover, W, H):
    b, kind = credit(board, pos, mover)
    N = "B" if mover == "W" else "W"
    d = to_pos(pos, W, H, N)
    ps = pos.white if b == 'W' else pos.black
    ok = False
    for p in ps:
        c = chk.certify(d, b, p, W, H)
        if all(c[i] for i in (1, 2, 3, 4, 5) if i != chk.DROP): ok = True
    key = (kind, 'M' if b == mover else 'N', ok)
    stats[key] = stats.get(key, 0) + 1
    return ok

def all_cert(board, pos, stm, W, H, memo):
    key = (pos, stm)
    if key in memo: return memo[key]
    memo[key] = True  # acyclic anyway
    lpos, rpos = common.split_ep(pos)
    src = lpos if stm == 'W' else rpos
    other = 'B' if stm == 'W' else 'W'
    res = True
    for c in pawns.moves(board, src, stm):
        t = common.terminal(board, c)
        if t is not None:
            if not certified(board, c, stm, W, H):
                res = False
        else:
            if not all_cert(board, c, other, W, H, memo): res = False
        if not res: break
    memo[key] = res
    return res

def gen_root(rng, W, H, maxp):
    files = list(range(2, W-1))
    wp = set(); bp = set()
    nw = rng.randint(1, maxp); nb = rng.randint(1, maxp)
    occ = set()
    for n, S in ((nw, wp), (nb, bp)):
        t = 0
        while len(S) < n and t < 50:
            t += 1
            f = rng.choice(files); r = rng.randint(2, H-1)
            if (f, r) in occ: continue
            S.add((f, r)); occ.add((f, r))
    return Pos(frozenset(wp), frozenset(bp), None)

def main():
    cmd = sys.argv[1]
    if cmd == 'gen':
        seed, N, W, H, maxp, out = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
        board = Board(W, H, True, True)
        rng = random.Random(seed)
        roots = []; seen = set(); tries = 0; uncert = 0
        while len(roots) < N and tries < N*50:
            tries += 1
            pos = gen_root(rng, W, H, maxp)
            if pos in seen: continue
            seen.add(pos)
            if common.terminal(board, pos) is not None: continue
            memo = {}
            ok = all_cert(board, pos, 'W', W, H, memo) and all_cert(board, pos, 'B', W, H, memo)
            if not ok: uncert += 1; continue
            ow = common.alt_winner(board, pos, 'W') == 'W'
            ob = common.alt_winner(board, pos, 'B') == 'W'
            def line(stm):
                toks = ["Ka1", f"ka{H}"] + [f"P{pawns.name(s)}" for s in sorted(pos.white)] + [f"p{pawns.name(s)}" for s in sorted(pos.black)]
                return " ".join(toks) + f" {stm} -"
            roots.append(dict(w=line('w'), b=line('b'), Dw=ow, Db=ob))
        with open(out+'.json', 'w') as fh: json.dump(roots, fh)
        with open(out+'.pos', 'w') as fh:
            for r in roots: fh.write(r['w']+"\n"+r['b']+"\n")
        print(len(roots), "all-certified roots;", uncert, "with an uncertified terminal;", tries, "tries; stats", stats, file=sys.stderr)
    else:
        out = sys.argv[2]
        roots = json.load(open(out+'.json'))
        res = {}
        for ln in open(out+'.res'):
            if ' | ' in ln:
                a, b = ln.rstrip().split(' | '); res[a] = b.split()
        bad = 0; ok = 0
        for r in roots:
            kw = res[r['w']]; kb = res[r['b']]
            exp_w = 'W' if r['Dw'] else 'L'; exp_b = 'W' if r['Db'] else 'L'
            if kw[0] != exp_w or kb[0] != exp_b or kw[0] != kw[1] or kb[0] != kb[1]:
                bad += 1; print("DIFF", r, kw, kb)
            else: ok += 1
        print("ok", ok, "violations", bad)
if __name__ == "__main__":
    main()
