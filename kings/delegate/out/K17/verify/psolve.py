"""Referee's own P-model solver (K17 verification). Written from kings/SPEC.md only; shares no code with
kpsolve.c, kp_p.c or K17/scripts.  P model: chess with kings and pawns, the first promotion ends the game as a
win for the promoter; checkmate = loss for the mover; stalemate and infinite play = draw.
Position: (wk, bk, wpawns(frozenset), bpawns(frozenset), side, ep) ; squares are (file, rank0) rank0 in 0..H-1.
ep = (target_square, color_of_pawn_that_can_be_captured) or None  (target is the skipped square)
"""
import sys
from collections import defaultdict, deque


class Board:
    def __init__(self, w, h, wrap):
        self.w, self.h, self.wrap = w, h, wrap

    def sq(self, f, r):
        if r < 0 or r >= self.h:
            return None
        if self.wrap:
            return (f % self.w, r)
        if f < 0 or f >= self.w:
            return None
        return (f, r)

    def king_n(self, s):
        out = set()
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                t = self.sq(s[0] + df, s[1] + dr)
                if t is not None and t != s:
                    out.add(t)
        return out

    def pawn_att(self, color, s):
        """squares attacked by a pawn of `color` standing on s"""
        dr = 1 if color == 0 else -1
        out = set()
        for df in (-1, 1):
            t = self.sq(s[0] + df, s[1] + dr)
            if t is not None:
                out.add(t)
        return out


def parse(b, text):
    toks = text.split()
    wk = bk = None
    wp, bp = set(), set()
    for t in toks[:-2]:
        c = t[0]
        f = ord(t[1]) - 97
        r = int(t[2:]) - 1
        if c == 'K': wk = (f, r)
        elif c == 'k': bk = (f, r)
        elif c == 'P': wp.add((f, r))
        elif c == 'p': bp.add((f, r))
        else: raise ValueError(t)
    side = 0 if toks[-2] == 'w' else 1
    ep = None
    if toks[-1] != '-':
        f = ord(toks[-1][0]) - 97
        r = int(toks[-1][1:]) - 1
        ep = ((f, r), 1 - side)   # captured pawn belongs to the opponent of the mover
    return (wk, bk, frozenset(wp), frozenset(bp), side, ep)


def fmt(b, pos):
    wk, bk, wp, bp, side, ep = pos
    n = lambda s: chr(97 + s[0]) + str(s[1] + 1)
    parts = ['K' + n(wk), 'k' + n(bk)] + ['P' + n(s) for s in sorted(wp)] + ['p' + n(s) for s in sorted(bp)]
    return ' '.join(parts) + (' w ' if side == 0 else ' b ') + (n(ep[0]) if ep else '-')


def attacked(b, pos, color_attacker, s, removed=None, wp=None, bp=None):
    """is square s attacked by attacker `color_attacker` (king or pawns), given pawn sets"""
    wk, bk, wpp, bpp = pos[0], pos[1], (wp if wp is not None else pos[2]), (bp if bp is not None else pos[3])
    if color_attacker == 0:
        if s in b.king_n(wk): return True
        for p in wpp:
            if p != removed and s in b.pawn_att(0, p): return True
    else:
        if s in b.king_n(bk): return True
        for p in bpp:
            if p != removed and s in b.pawn_att(1, p): return True
    return False


def moves(b, pos, frozen=False):
    """legal moves: list of (kind, newpos or None, label). kind 'P' = promotion (immediate win for mover)"""
    wk, bk, wp, bp, side, ep = pos
    out = []
    me, op = side, 1 - side
    my_k = wk if me == 0 else bk
    op_k = bk if me == 0 else wk
    my_p = wp if me == 0 else bp
    op_p = bp if me == 0 else wp
    last = b.h - 1 if me == 0 else 0
    start = 1 if me == 0 else b.h - 2
    dr = 1 if me == 0 else -1

    def mk(nk, nmy, nop, nep):
        if me == 0:
            return (nk, bk, frozenset(nmy), frozenset(nop), 1, nep)
        return (wk, nk, frozenset(nop), frozenset(nmy), 0, nep)

    def my_king_safe_after(nk, nmy, nop):
        # king at nk, own pawns nmy, opponent pawns nop, opponent king op_k
        if nk in b.king_n(op_k):
            return False
        for p in nop:
            if nk in b.pawn_att(op, p): return False
        return True

    # king moves
    for t in b.king_n(my_k):
        if t in my_p: continue
        if t == op_k: continue
        nop = op_p - {t} if t in op_p else op_p
        if not my_king_safe_after(t, my_p, nop): continue
        if frozen:
            out.append(('F', None, 'K' + str(t)))
        else:
            out.append(('K', mk(t, my_p, nop, None), 'K' + str(t)))
    # pawn moves
    for p in my_p:
        f, r = p
        # forward
        t = b.sq(f, r + dr)
        if t is not None and t not in my_p and t not in op_p and t != wk and t != bk:
            nmy = (my_p - {p}) | {t}
            if my_king_safe_after(my_k, nmy, op_p):
                if t[1] == last:
                    out.append(('P', None, 'P' + str(p) + '-' + str(t)))
                else:
                    out.append(('p', mk(my_k, nmy, op_p, None), 'P' + str(p) + '-' + str(t)))
                    if r == start:
                        t2 = b.sq(f, r + 2 * dr)
                        if t2 is not None and t2 not in my_p and t2 not in op_p and t2 != wk and t2 != bk:
                            nmy2 = (my_p - {p}) | {t2}
                            if my_king_safe_after(my_k, nmy2, op_p):
                                out.append(('p', mk(my_k, nmy2, op_p, (t, me)), 'P' + str(p) + '-' + str(t2)))
        # captures
        for t in b.pawn_att(me, p):
            if t in op_p:
                nmy = (my_p - {p}) | {t}
                nop = op_p - {t}
                if my_king_safe_after(my_k, nmy, nop):
                    if t[1] == last:
                        out.append(('P', None, 'P' + str(p) + 'x' + str(t)))
                    else:
                        out.append(('p', mk(my_k, nmy, nop, None), 'P' + str(p) + 'x' + str(t)))
            elif ep is not None and ep[1] == op and t == ep[0]:
                # en passant: captured pawn stands behind target from the mover's view
                cap = (t[0], t[1] - dr)
                if cap in op_p:
                    nmy = (my_p - {p}) | {t}
                    nop = op_p - {cap}
                    if my_king_safe_after(my_k, nmy, nop):
                        out.append(('p', mk(my_k, nmy, nop, None), 'P' + str(p) + 'x' + str(t) + 'ep'))
    return out


def in_check(b, pos):
    wk, bk, wp, bp, side, ep = pos
    if side == 0:
        return attacked(b, pos, 1, wk)
    return attacked(b, pos, 0, bk)


class Solver:
    def __init__(self, b, frozen=False):
        self.b = b
        self.frozen = frozen
        self.succ = {}

    def explore(self, roots):
        stack = list(roots)
        while stack:
            p = stack.pop()
            if p in self.succ: continue
            ms = moves(self.b, p, self.frozen)
            self.succ[p] = ms
            for kind, q, lab in ms:
                if q is not None and q not in self.succ:
                    stack.append(q)

    def solve(self):
        """value for side to move: 'W' (mover wins), 'L' (mover loses), 'D'. Least fixed point."""
        succ = self.succ
        val = {}
        pred = defaultdict(list)
        cnt = {}
        q = deque()
        for p, ms in succ.items():
            if any(k == 'P' for k, _, _ in ms):
                val[p] = 'W'
                q.append(p)
                continue
            if not ms:
                if in_check(self.b, p):
                    val[p] = 'L'
                    q.append(p)
                else:
                    val[p] = 'D'
                continue
            cnt[p] = sum(1 for k, c, lab in ms if k not in ('F',))
            if cnt[p] == 0:
                val[p] = 'L'; q.append(p); continue
            for k, c, lab in ms:
                if k != 'F': pred[c].append(p)
        while q:
            c = q.popleft()
            vc = val[c]
            for p in pred.get(c, []):
                if p in val: continue
                if vc == 'L':
                    val[p] = 'W'; q.append(p)
                else:   # vc == 'W': child is a win for the opponent
                    cnt[p] -= 1
                    if cnt[p] == 0:
                        val[p] = 'L'; q.append(p)
        for p in succ:
            val.setdefault(p, 'D')
        self.val = val
        return val

    def white_view(self, p):
        v = self.val[p]
        if v == 'D': return 'D'
        mover_white = (p[4] == 0)
        if v == 'W': return 'W' if mover_white else 'L'
        return 'L' if mover_white else 'W'

    def move_values(self, p):
        """list of (label, value of the resulting position from the MOVER's point of view)"""
        res = []
        for k, q, lab in self.succ[p]:
            if k == 'P': res.append((lab, 'W'))
            elif k == 'F': res.append((lab, 'L'))
            else:
                v = self.val[q]
                res.append((lab, {'W': 'L', 'L': 'W', 'D': 'D'}[v]))
        return res


if __name__ == '__main__':
    spec = sys.argv[1]
    kind, dims = spec.split(':')
    w, h = map(int, dims.split('x'))
    b = Board(w, h, kind == 'cyl')
    roots = [parse(b, line.strip()) for line in sys.stdin if line.strip()]
    s = Solver(b, frozen='--frozen' in sys.argv)
    s.explore(roots)
    s.solve()
    print('# states', len(s.succ), file=sys.stderr)
    for r in roots:
        print(fmt(b, r), '|', s.white_view(r), '|', ' '.join(f'{l}:{v}' for l, v in s.move_values(r)))
