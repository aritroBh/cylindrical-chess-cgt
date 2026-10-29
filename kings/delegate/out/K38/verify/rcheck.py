# rcheck.py -- K38 referee: mechanical checks of K38's PROOF.md with the referee's own generator rgen.py.
# Codes the invariant S and the rules rho / sigma / tau from the text of PROOF.md (not from K38's p5check.py).
import sys, itertools
sys.dont_write_bytecode = True
from rgen import Board, solve

FILES = 'abcdefg'
def S_(B, n):
    return ('abcdefgh'.index(n[0]), int(n[1:]) - 1)

def rel(B, s, pf, pr):
    """relative coords of s w.r.t. pawn at (pf, pr): x in -3..3 on cyl, plain on flat."""
    x = s[0] - pf
    if B.wrap:
        x = (x + 3) % B.W - 3
    return (x, s[1] - pr)

def in_S(B, pos, mut=None):
    wk, bk, wp, bp, stm, ep = pos
    if stm != 1 or wp or len(bp) != 1:
        return False
    if not B.legal_pos(pos):
        return False
    (p,) = tuple(bp)
    if p[0] != 2:  # c-file
        return False
    r = p[1] + 1  # 1-based rank
    wx, wy = rel(B, wk, 2, p[1])
    bx, by = rel(B, bk, 2, p[1])
    ZL = lambda x, y: x in (1, 2) and -3 <= y <= 0
    ZR = lambda x, y: x in (-1, -2) and -3 <= y <= 0
    if mut == 'cutZL':
        ZL = lambda x, y: x in (1, 2) and -2 <= y <= 0
    if mut == 'cutZR':
        ZR = lambda x, y: x in (-1, -2) and -2 <= y <= 0
    if r in (4, 5):
        if (wx, wy) == (0, -1): return True
        if (wx, wy) == (0, -2): return True
        if (wx, wy) == (-1, -2): return not ZL(bx, by)
        if (wx, wy) == (1, -2): return not ZR(bx, by)
        return False
    if r == 3:
        n = lambda s: B.name(s)
        if n(wk) == 'c2': return True
        if n(wk) == 'c1': return mut == 'nob3d3' or n(bk) not in ('b3', 'd3')
        if n(wk) == 'b1': return n(bk) == 'b3'
        if n(wk) == 'd1': return n(bk) == 'd3'
        return False
    if r == 2:
        return B.name(wk) == 'c1' and B.name(bk) in ('b3', 'd3')
    return False

def enum_S(B, mut=None):
    out = []
    sqs = [(f, r) for f in range(B.W) for r in range(B.H)]
    for r in range(1, 5):  # 0-based pawn rank 1..4 = ranks 2..5
        p = (2, r)
        for wk in sqs:
            for bk in sqs:
                pos = (wk, bk, frozenset(), frozenset([p]), 1, None)
                if in_S(B, pos, mut):
                    out.append(pos)
    return out

def rho(B, pos):
    """White's rule (White to move, Black pawn on c-file or gone). Returns child or None."""
    wk, bk, wp, bp, stm, ep = pos
    ms = [(lab, c) for k, c, lab in B.moves(pos) if k == 'n']
    by_to = {c[0]: c for lab, c in ms}
    if not bp:
        return None
    (p,) = tuple(bp)
    # 1. capture
    if p in by_to:
        return by_to[p]
    F = B.sq(p[0], p[1] - 1); M = B.sq(p[0], p[1] - 2)
    L = B.sq(p[0] - 1, p[1] - 2); R = B.sq(p[0] + 1, p[1] - 2)
    if wk == F:
        return by_to.get(M)
    if wk == M:
        if F in by_to: return by_to[F]
        x, y = rel(B, bk, p[0], p[1])
        if x == -1: return by_to.get(L)
        if x == 1: return by_to.get(R)
        return None
    if wk in (L, R):
        if M in by_to: return by_to[M]
        return by_to.get(F)
    x, y = rel(B, wk, p[0], p[1])
    if (x, y) in ((-1, -1), (1, -1)):
        return by_to.get(F)
    return None

def check_lemmaD(B, mut=None):
    S = enum_S(B, mut)
    Sset = set(S)
    cnt = {}
    for pos in S:
        r = tuple(pos[3])[0][1] + 1
        cnt[r] = cnt.get(r, 0) + 1
    fails = 0; pairs = 0; stats = {'cap': 0, 'stale': 0, 'S': 0, 'blackstuck': 0}
    for pos in S:
        ms = B.moves(pos)
        if not ms:
            stats['blackstuck'] += 1
        for k, c, lab in ms:
            pairs += 1
            if k == 'promo':
                fails += 1; continue
            wm = B.moves(c)
            if not wm:
                if B.in_check(c, 0): fails += 1
                else: stats['stale'] += 1
                continue
            nx = rho(B, c)
            if nx is None:
                fails += 1; continue
            if not nx[3]:
                stats['cap'] += 1; continue
            if nx in Sset: stats['S'] += 1
            else: fails += 1
    return len(S), cnt, pairs, fails, stats

def check_partA(B):
    """After each White move from X: Kxb5 legal; then tau (Black never moves the pawn) vs every White move."""
    X = B.parse('Kc4 Pb5 kb6 pc5 w -')
    fails = 0; nodes = 0
    starts = []
    for k, c, lab in B.moves(X):
        kx = [cc for kk, cc, ll in B.moves(c) if kk == 'n' and cc[1] == S_(B, 'b5')]
        if not kx: fails += 1
        else: starts.append(kx[0])
    seen = set(starts); stack = list(starts)
    while stack:
        p = stack.pop(); nodes += 1
        if p[2]: fails += 1  # White pawn present: should never happen after Kxb5
        wm = B.moves(p)
        if not wm: continue  # stalemate or K vs K end: no White win (White has no pawn, cannot mate)
        for k, c, lab in wm:
            if k == 'promo': fails += 1; continue
            # Black: any king move (tau). Need at least one; explore all.
            km = [cc for kk, cc, ll in B.moves(c) if kk == 'n' and cc[1] != c[1] and cc[3] == c[3]]
            if B.in_check(c, 1): fails += 1
            if not km: fails += 1
            for cc in km:
                if cc not in seen: seen.add(cc); stack.append(cc)
    return len(starts), nodes, fails

def check_partC(B):
    X = B.parse('Kc4 Pb5 kb6 pc5 w -')
    c = [cc for kk, cc, ll in B.moves(X) if cc and cc[0] == S_(B, 'd5')][0]
    c3 = [cc for kk, cc, ll in B.moves(c) if cc and cc[3] == frozenset([S_(B, 'c3')])]
    if not c3: return 'no c3'
    fails = 0; n = 0
    frontier = [c3[0]]
    for step in range(2):
        nxt = []
        for p in frontier:
            wm = B.moves(p)
            if not wm: fails += 1
            for k, w, lab in wm:
                n += 1
                if k == 'promo': fails += 1; continue
                bm = B.moves(w)
                push = [x for x in bm if x[2].startswith('Pc')]
                if step == 0:
                    pc = [x for x in push if x[0] == 'n' and x[1][3] == frozenset([S_(B, 'c2')])]
                    if not pc: fails += 1
                    else: nxt.append(pc[0][1])
                else:
                    if not any(x[0] == 'promo' for x in push): fails += 1
        frontier = nxt
    return n, fails

def check_partB(B):
    """sigma after each of Kb3, Kc3, Kd3: explore all Black moves; White replies by sigma."""
    X = B.parse('Kc4 Pb5 kb6 pc5 w -')
    res = {}
    for sortie in ('b3', 'c3', 'd3'):
        def sigma(p):
            wk, bk, wp, bp, stm, ep = p
            ms = {c: (k, lab) for k, c, lab in B.moves(p) if k == 'n'}
            bym = {}
            for k, c, lab in B.moves(p):
                if k == 'n': bym[lab] = c
            if p == X:
                return bym['Kc4' + sortie]
            if not wp:  # after ...Kxb5: rho
                return rho(B, p)
            if not bp:  # free mode: any king move, never the pawn
                km = [c for lab, c in bym.items() if lab.startswith('K')]
                return km[0] if km else None
            # White pawn b5 and Black pawn present, not X
            if B.name(bk) == 'a5' and B.name(p[0]) in ('b3', 'c3', 'd3'):
                return bym.get('K' + B.name(p[0]) + 'c4')
            # capture the pawn (after ...c4, ...c3, or after ...Ka5 Kc4 K-move)
            (q,) = tuple(bp)
            caps = [c for lab, c in bym.items() if lab.startswith('K') and c[0] == q]
            return caps[0] if caps else None
        start = [c for k, c, lab in B.moves(X) if lab == 'Kc4' + sortie][0]
        seen = {start}; stack = [start]; fails = 0; wnodes = 0
        while stack:
            p = stack.pop()  # Black to move
            for k, c, lab in B.moves(p):
                if k == 'promo': fails += 1; continue
                wm = B.moves(c)
                if not wm:
                    if B.in_check(c, 0): fails += 1
                    continue
                wnodes += 1
                n = sigma(c)
                if not c[2] and not c[3]: continue  # K against K: a draw, nothing to check
                if n is None: fails += 1; print('  sigma undefined at', B.fmt(c)) if fails < 4 else None; continue
                if len(n[2]) < len(c[2]): fails += 1  # sigma never moves... (pawn count only drops by capture)
                if n[2] != c[2] and n[2]: fails += 1  # White pawn moved
                if not B.moves(n): continue
                if n not in seen: seen.add(n); stack.append(n)
        res[sortie] = (wnodes, len(seen), fails)
    return res

def main():
    for name, wrap in (('cyl:7x6', True), ('flat:7x6', False)):
        B = Board(7, 6, wrap)
        X = B.parse('Kc4 Pb5 kb6 pc5 w -')
        print('==', name)
        print('statement 0, White moves at X:', sorted(lab for k, c, lab in B.moves(X)))
        n, cnt, pairs, fails, stats = check_lemmaD(B)
        print('Lemma D: |S| =', n, 'by rank', dict(sorted(cnt.items())), 'Black moves', pairs, 'fails', fails, stats)
        for mut in ('cutZL', 'cutZR', 'nob3d3'):
            n2, cnt2, pairs2, f2, st2 = check_lemmaD(B, mut)
            print('  mutation', mut, '|S| =', n2, 'fails', f2)
        print('Part A (Kxb5 + tau): starts, nodes, fails =', check_partA(B))
        print('Part C (Kd5 c3 c2 c1): W-moves, fails =', check_partC(B))
        print('Part B (sigma) per sortie: (White nodes, Black nodes, fails) =', check_partB(B))
        # start positions after sortie + Kxb5: rho reply and membership in S
        for s in ('b3', 'c3', 'd3'):
            p = B.parse('K%s kb5 pc5 w -' % s)
            n = rho(B, p)
            print('  K%s kb5: rho ->' % s, B.fmt(n), 'in S:', in_S(B, n))
        # own solver values
        for model in ('P', 'EPW', 'EPB'):
            res, seen = solve(B, [X, B.parse('Kc4 Pb5 kb6 pc5 b -')], model)
            vals = [res[B.parse(t)] for t in ('Kc4 Pb5 kb6 pc5 w -', 'Kc4 Pb5 kb6 pc5 b -')]
            extra = ''
            if model == 'P':
                with open('reach_%s.txt' % name.split(':')[0], 'w') as fh:
                    for p in res:
                        fh.write(B.fmt(p) + ' | ' + res[p] + '\n')
                extra = ' after sorties: ' + ' '.join(
                    s + ':' + res[B.parse('K%s Pb5 kb6 pc5 b -' % s)] for s in ('b3', 'c3', 'd3', 'd5'))
                # values of S positions
                Svals = {}
                for q in enum_S(B):
                    if q in res: Svals[res[q]] = Svals.get(res[q], 0) + 1
                extra += ' | S positions reached: ' + str(Svals)
            print('own solver', model, ': reachable', len(res), 'X w =', vals[0], 'X b =', vals[1], extra)

if __name__ == '__main__':
    main()
