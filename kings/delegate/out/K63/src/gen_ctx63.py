"""K63 question 3: P contexts beside F2 = Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6 on flat 8x8.
Written for K63 after K47's gen_ctx.py (same idea, own code).  For a set of context files, every context X of at most
NW White and NB Black pawns on those files (White pawns ranks 2..7, Black pawns ranks 2..7), and writes
  in/ctx_<tag>.pos   8 positions per context for ref3m / kp_p: rootA (kc4) b, w; rootB (kc5) b, w;
                     qA (after b2-b4 at kc4) b with e.p. square b3, w; qB (after b2-b3 at kc5) b, w
  in/ctx_<tag>.pred  the D-sum prediction per context, White's view:
                     omega: r(over_D (+) X) with White / Black to move (prediction for the roots, Corollary 4.17)
                     zero:  r(0_D (+) X) = r(X) with White / Black to move (prediction for the q's)
                     plus a flag ep=1 if X can ever create an e.p. right (double step next to an enemy pawn's file)
  in/ctx_<tag>.tg    X as a finite D-game in the T format of vgsum59 / toyref (name|k|L/R;...), position 0 = start.
                     This format has no e.p. clearing by moves elsewhere: use it only for contexts with ep=0.
X as a D-game: the context pawns alone on the 8x8 board, pawn moves only (single and double steps, captures, e.p.),
a promotion is a terminal win for the promoter, a side with no move loses (normal play).  In a sum, a move in the other
component clears X's e.p. right (the right belongs to the side to move and lasts one move of that side).
Solver: least fixed point by repeated sweeps over (over state, X state with e.p. right, side).
usage: python3 gen_ctx63.py <files, e.g. g,h> <NW> <NB> <tag>"""
import itertools
import sys

W, H = 8, 8
FILES = [ord(c) - 97 for c in sys.argv[1].split(',')]
NW, NB, TAG = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
GROUP = {'A': ('Ka4 kc4', 'Pb2 Pf5 pb6 pf6'), 'B': ('Ka4 kc5', 'Pb2 Pf5 pb6 pf6'),
         'qA': ('Ka4 kc4', 'Pb4 Pf5 pb6 pf6'), 'qB': ('Ka4 kc5', 'Pb3 Pf5 pb6 pf6')}
SQS = [(f, r) for f in FILES for r in range(1, H - 1)]
nm = lambda f, r: chr(97 + f) + str(r + 1)


def contexts():
    out = []
    for nw in range(NW + 1):
        for ws in itertools.combinations(SQS, nw):
            rest = [s for s in SQS if s not in ws]
            for nb in range(NB + 1):
                for bs in itertools.combinations(rest, nb):
                    out.append((frozenset(ws), frozenset(bs)))
    return out


def xmoves(pos, white):
    """options of one side in X: list of 'W'/'B' (promotion terminal) or successor (wp, bp, ep)"""
    wp, bp, ep = pos
    own, opp = (wp, bp) if white else (bp, wp)
    d = 1 if white else -1
    last = H - 1 if white else 0
    start = 1 if white else H - 2
    occ = wp | bp
    res = []
    for (f, r) in sorted(own):
        r1 = r + d
        rest = own - {(f, r)}

        def put(to, captured, newep=None):
            if to[1] == last:
                res.append('W' if white else 'B')
                return
            o2, p2 = rest | {to}, opp - ({captured} if captured else frozenset())
            res.append((o2, p2, newep) if white else (p2, o2, newep))
        if (f, r1) not in occ:
            put((f, r1), None)
            if r == start and (f, r1 + d) not in occ:
                put((f, r1 + d), None, (f, r1))
        for df in (-1, 1):
            g = f + df
            if not 0 <= g < W:
                continue
            if (g, r1) in opp:
                put((g, r1), (g, r1))
            elif ep == (g, r1) and (g, r) in opp:
                put((g, r1), (g, r))
    return res


def build(start):
    """X graph from start (no right). Nodes carry the e.p. square; C[i] = the same node with the right cleared."""
    idx = {start: 0}; order = [start]; L, R, C = [], [], []
    i = 0
    while i < len(order):
        p = order[i]; i += 1
        row = []
        for white in (True, False):
            opts = []
            for q in xmoves(p, white):
                if isinstance(q, str):
                    opts.append(q)
                else:
                    if q not in idx:
                        idx[q] = len(order); order.append(q)
                    opts.append(idx[q])
            row.append(opts)
        L.append(row[0]); R.append(row[1])
        c = (p[0], p[1], None)
        if c not in idx:
            idx[c] = len(order); order.append(c)
        C.append(idx[c])
    has_ep = any(p[2] is not None for p in order)
    return L, R, C, has_ep


def solve(L, R, C, with_over):
    """r(over_D (+) X) (with_over) or r(X) from X position 0; returns {'w': .., 'b': ..} White's view."""
    m = len(L)
    ostates = (0, 1) if with_over else (1,)   # 0 = omega, 1 = 0_D
    val = {}

    def opts(o, t, s):
        res = []
        if o == 0:
            res.append((1, C[t], 1) if s == 0 else (0, C[t], 0))   # White omega -> 0_D; Black omega -> omega
        for x in (L[t] if s == 0 else R[t]):
            res.append(x if isinstance(x, str) else (o, x, 1 - s))
        return res
    states = [(o, t, s) for o in ostates for t in range(m) for s in (0, 1)]
    changed = True
    while changed:
        changed = False
        for st in states:
            if st in val:
                continue
            o, t, s = st
            op = opts(o, t, s)
            me, him = ('W', 'B') if s == 0 else ('B', 'W')
            if not op:
                v = 'lose'
            elif any(x == me or (not isinstance(x, str) and val.get(x) == 'lose') for x in op):
                v = 'win'
            elif all(x == him or (not isinstance(x, str) and val.get(x) == 'win') for x in op):
                v = 'lose'
            else:
                continue
            val[st] = v; changed = True
    o0 = ostates[0]
    out = {}
    for s, c in ((0, 'w'), (1, 'b')):
        v = val.get((o0, 0, s))
        out[c] = 'D' if v is None else ('W' if (v == 'win') == (s == 0) else 'L')
    return out


if __name__ == '__main__':
    ctxs = contexts()
    with open('in/ctx_%s.pos' % TAG, 'w') as fp, open('in/ctx_%s.tg' % TAG, 'w') as ft, open('in/ctx_%s.pred' % TAG, 'w') as fr:
        for k, (ws, bs) in enumerate(ctxs):
            cstr = " ".join(["P" + nm(*s) for s in sorted(ws)] + ["p" + nm(*s) for s in sorted(bs)])
            for key in ('A', 'B', 'qA', 'qB'):
                kings, pawns = GROUP[key]
                for stm in 'bw':
                    ep = 'b3' if (key == 'qA' and stm == 'b') else '-'
                    fp.write(" ".join(x for x in (kings, pawns, cstr, stm, ep) if x) + "\n")
            L, R, C, has_ep = build((ws, bs, None))
            parts = ["%s/%s" % (",".join(map(str, L[i])), ",".join(map(str, R[i]))) for i in range(len(L))]
            ft.write("ctx%d|%d|%s\n" % (k, len(L), ";".join(parts)))
            po, pz = solve(L, R, C, True), solve(L, R, C, False)
            fr.write("ctx%d [%s] omega w %s b %s zero w %s b %s ep %d n %d\n" % (
                k, cstr if cstr else 'empty', po['w'], po['b'], pz['w'], pz['b'], int(has_ep), len(L)))
    print(len(ctxs), "contexts")
