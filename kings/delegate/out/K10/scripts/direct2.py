"""Random kings anywhere; all hypotheses (incl. K1s,K2s,kpath) checked; compare with kpsolve --frozen."""
import sys, random, collections
sys.path.insert(0, '.')
from cert import *
from direct import line, run_kp
W, H, maxp, N, seed = map(int, sys.argv[1:6])
bd = Board(W, H, True, True)
rnd = random.Random(seed)
FL = "abcdefgh"
allsq = [(f, r) for f in range(W) for r in range(1, H+1)]
pawnsq = [(f, r) for f in range(W) for r in range(2, H)]
inst = []; ablate = collections.defaultdict(list)
tried = 0
while len(inst) < N and tried < 40_000_000:
    tried += 1
    wk, bk = rnd.sample(allsq, 2)
    if kdist(bd, wk, bk) < 2: continue
    nw, nb = rnd.randint(1, maxp), rnd.randint(0, maxp)
    ps = rnd.sample(pawnsq, nw + nb)
    ps = [p for p in ps if p != wk and p != bk]
    if len(ps) != nw + nb: continue
    w, b = frozenset(ps[:nw]), frozenset(ps[nw:])
    pos = Pos(w, b)
    stm = rnd.choice('WB')
    # legality for kpsolve: side not to move must not be in check
    def attacked(king, pawns, color):   # king attacked by pawns of `color`
        return any(a in pawns for a in attackers_of(bd, king, color))
    from cylcgt.pawns import Board as _B
    # attackers_of is in cert? define locally
    def att(king, pawns, color):
        f, r = king
        r0 = r-1 if color == 'W' else r+1
        if not (1 <= r0 <= H): return False
        return any(((f+df) % W, r0) in pawns for df in (-1, 1))
    if stm == 'W' and att(bk, w, 'W'): continue
    if stm == 'B' and att(wk, b, 'B'): continue
    for beta in 'WB':
        if not (w if beta == 'W' else b): continue
        ok, info = check(bd, pos, wk, bk, stm, beta)
        if ok:
            inst.append((pos, wk, bk, stm, beta))
        else:
            for h in ('K1', 'K2', 'kpath', 'N'):
                use = tuple(x for x in ('P1','front','kpath','K1','K2','N','M') if x != h)
                if check(bd, pos, wk, bk, stm, beta, use=use)[0]:
                    ablate[h].append((pos, wk, bk, stm, beta))
print("tried", tried, "FULL instances", len(inst), {k: len(v) for k, v in ablate.items()}, flush=True)
def evaluate(lst, label):
    lines = [line(bd, pos, wk, bk, stm) for pos, wk, bk, stm, beta in lst]
    res = {}
    uniq = sorted(set(lines))
    for i in range(0, len(uniq), 30000): res.update(run_kp(bd, uniq[i:i+30000]))
    v = 0; ill = 0; ex = []
    for (pos, wk, bk, stm, beta), L in zip(lst, lines):
        r = res.get(L)
        if r is None or r[0] == 'X': ill += 1; continue
        want = 'W' if beta == 'W' else 'L'
        if r != [want, want]:
            v += 1
            if len(ex) < 4: ex.append((L, beta, r))
    print(label, "n", len(lst), "illegal", ill, "violations", v, ex, flush=True)
evaluate(inst, "FULL")
for h, lst in ablate.items(): evaluate(lst[:20000], "drop_"+h)
