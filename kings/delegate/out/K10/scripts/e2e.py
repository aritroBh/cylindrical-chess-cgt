import sys, collections, time
sys.setrecursionlimit(10000)
from cert import *
from direct import line, run_kp, enum_positions

USE = ('P1','front','kpath','K1','K2','N','M')
class D:
    def __init__(s, bd, wk, bk):
        s.bd, s.wk, s.bk = bd, wk, bk
        s.cw = {}; s.dw = {}; s.ac = {}; s.cc = {}; s.use = USE
    def norm(s, pos):
        if pos.ep:
            t, c, side = pos.ep
            theirs = pos.black if side == 'B' else pos.white
            if not any((g, c[1]) in theirs for g in (s.bd.nb(c[0], -1), s.bd.nb(c[0], 1)) if g is not None):
                return Pos(pos.white, pos.black, None)
        return pos
    def term(s, pos, mover):
        """None or credited winner W/B after `mover` moved to child pos."""
        bd = s.bd
        wp, bp = passed(bd, pos, 'W'), passed(bd, pos, 'B')
        if not wp and not bp: return None
        if wp and bp:
            other = opp(mover)
            return other if promote_distance(bd, pos, other) <= promote_distance(bd, pos, mover) else mover
        return 'W' if wp else 'B'
    def certified(s, pos, winner, stm):
        key = (pos, winner, stm)
        if key not in s.cc:
            s.cc[key] = check(s.bd, pos, s.wk, s.bk, stm, winner, use=s.use)[0]
        return s.cc[key]
    def children(s, pos, stm):
        return [s.norm(c) for c in moves(s.bd, pos, stm)]
    def dwin(s, pos, stm):
        """plain D-game winner (normal play), terminals as cylcgt."""
        key = (pos, stm)
        if key in s.dw: return s.dw[key]
        res = opp(stm)   # no move: stm loses
        for c in s.children(pos, stm):
            t = s.term(c, stm)
            w = t if t is not None else s.dwin(c, opp(stm))
            if w == stm: res = stm; break
        s.dw[key] = res
        return res
    def cw_(s, pos, stm, sigma):
        """True if sigma forces a D-win using only certified sigma-credited terminals."""
        key = (pos, stm, sigma)
        if key in s.cw: return s.cw[key]
        ch = s.children(pos, stm)
        if stm == sigma:
            res = False
            for c in ch:
                t = s.term(c, stm)
                if t is None:
                    if s.cw_(c, opp(stm), sigma): res = True; break
                elif t == sigma and s.certified(c, sigma, opp(stm)): res = True; break
        else:
            res = True   # sigma-bar always has a (suicidal) king move if no pawn move; layout supplies it
            for c in ch:
                t = s.term(c, stm)
                if t is None:
                    if not s.cw_(c, opp(stm), sigma): res = False; break
                elif t == sigma:
                    if not s.certified(c, sigma, opp(stm)): res = False; break
                else: res = False; break
        s.cw[key] = res
        return res
    def allcert(s, pos, stm):
        key = (pos, stm)
        if key in s.ac: return s.ac[key]
        s.ac[key] = True   # acyclic anyway
        res = True
        for c in s.children(pos, stm):
            t = s.term(c, stm)
            if t is None:
                if not s.allcert(c, opp(stm)): res = False; break
            else:
                if not s.certified(c, t, opp(stm)): res = False; break
        s.ac[key] = res
        return res

if __name__ == "__main__":
    W, H, maxp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    if len(sys.argv) > 4: USE = tuple(x for x in USE if x not in sys.argv[4].split(','))
    print('USE', USE)
    files = list(range(2, W-1)); ranks = range(2, H)
    bd = Board(W, H, True, True); wk, bk = (0, 1), (0, H)
    D_ = D(bd, wk, bk)
    roots = []
    for w, b in enum_positions(bd, files, maxp, ranks):
        pos = Pos(w, b)
        if passed(bd, pos, 'W') or passed(bd, pos, 'B'): continue
        if not w or not b: continue
        for stm in 'WB':
            roots.append((pos, stm))
    print("roots", len(roots), flush=True)
    rec = []
    for pos, stm in roots:
        cwW = D_.cw_(pos, stm, 'W'); cwB = D_.cw_(pos, stm, 'B')
        dw = D_.dwin(pos, stm); ac = D_.allcert(pos, stm)
        rec.append((pos, stm, cwW, cwB, dw, ac))
    lines = sorted({line(bd, p, wk, bk, st) for p, st, *_ in rec})
    res = {}
    for i in range(0, len(lines), 40000): res.update(run_kp(bd, lines[i:i+40000]))
    cnt = collections.Counter(); ex = collections.defaultdict(list)
    for pos, stm, cwW, cwB, dw, ac in rec:
        r = res[line(bd, pos, wk, bk, stm)]
        kpw = r[0] if r[0] == r[1] else '?'
        kpwin = {'W': 'W', 'L': 'B', 'D': 'D'}.get(kpw, '?')
        for sig, cw in (('W', cwW), ('B', cwB)):
            if cw:
                cnt['certified_win'] += 1
                if kpwin != sig:
                    cnt['CERT_VIOL'] += 1; ex['cert'].append((line(bd, pos, wk, bk, stm), sig, r))
        if ac:
            cnt['allcert'] += 1
            if kpwin != dw:
                cnt['ALLCERT_VIOL'] += 1; ex['all'].append((line(bd, pos, wk, bk, stm), dw, r))
        cnt['D_vs_kp_mismatch'] += (kpwin != dw)
        cnt['kp_draw'] += (kpwin == 'D')
        if (cwW or cwB): pass
        else: cnt['D_win_not_certified'] += 1
        cnt['n'] += 1
    print(dict(cnt))
    for k, v in ex.items(): print(k, v[:6])
