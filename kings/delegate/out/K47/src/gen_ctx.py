"""K47 item 3: P contexts beside the K45 over group Z_O.
For a cylinder cyl:Wx6 and a set of context files, enumerate every context of at most 2 White and 2 Black pawns on those
files (ranks 2..5), and write
  ctx_<tag>.pos   positions for ref3m / kp_p (group + context, both roots, both sides to move, no e.p.)
  ctx_<tag>.tg    the context as a D-game for za.cpp/zb.cpp (pawn moves of the context alone, e.p. on, a promotion is a
                  terminal for the promoter; C= gives the position with the e.p. right cleared)
  ctx_<tag>.pred  r(over + C) for both sides to move, computed here by a small fixed point (own code)
usage: python3 gen_ctx.py <W> <files, e.g. h or h,i> <tag> [convention N|C]"""
import itertools
import sys

W = int(sys.argv[1]); FILES = [ord(c) - 97 for c in sys.argv[2].split(',')]; TAG = sys.argv[3]
CONV = sys.argv[4] if len(sys.argv) > 4 else 'N'
H = 6
GROUP = [("Kf5 kd4", "Pb2 Pb4 Pe2 pa4 pb5 pe5"), ("Kf5 kd5", "Pb2 Pb4 Pe2 pa4 pb5 pe5")]
SQS = [(f, r) for f in FILES for r in range(1, H - 1)]
name = lambda f, r: chr(97 + f) + str(r + 1)


def contexts():
    out = []
    for nw in range(3):
        for ws in itertools.combinations(SQS, nw):
            rest = [s for s in SQS if s not in ws]
            for nb in range(3):
                for bs in itertools.combinations(rest, nb):
                    out.append((frozenset(ws), frozenset(bs)))
    return out


def moves(pos, white):
    """moves of the context pawns alone; returns list of positions or 'W'/'B' terminals"""
    wp, bp, ep = pos
    own, opp = (wp, bp) if white else (bp, wp)
    d = 1 if white else -1
    last = H - 1 if white else 0
    start = 1 if white else H - 2
    res = []
    occ = wp | bp
    for (f, r) in own:
        r1 = r + d
        def go(t, cap):
            o2 = (own - {(f, r)})
            p2 = opp - ({cap} if cap else set())
            if t[1] == last:
                res.append('W' if white else 'B'); return
            o2 = o2 | {t}
            res.append((o2, p2, None) if white else (p2, o2, None))
        if (f, r1) not in occ:
            go((f, r1), None)
            if r == start and (f, r1 + d) not in occ:
                o2 = (own - {(f, r)}) | {(f, r1 + d)}
                res.append((o2, opp, (f, r1)) if white else (opp, o2, (f, r1)))
        for df in (-1, 1):
            t = ((f + df) % W, r1)
            if t in opp:
                go(t, t)
            elif ep == t and ((f + df) % W, r) in opp:
                go(t, ((f + df) % W, r))
    return res


def build(start):
    idx = {start: 0}; order = [start]; L = []; R = []; C = []
    i = 0
    while i < len(order):
        p = order[i]; i += 1
        row = []
        for white in (True, False):
            opts = []
            for q in moves(p, white):
                if isinstance(q, str):
                    opts.append(q)
                else:
                    if q not in idx: idx[q] = len(order); order.append(q)
                    opts.append(idx[q])
            row.append(opts)
        L.append(row[0]); R.append(row[1])
        c = (p[0], p[1], None)
        if c not in idx: idx[c] = len(order); order.append(c)
        C.append(idx[c])
    return L, R, C


def over_plus(L, R, C):
    """r(over + C) from position 0 of C with over at omega; returns {'w': .., 'b': ..} in White's view"""
    m = len(L)
    val = {}
    states = [(o, t, s) for o in (0, 1) for t in range(m) for s in (0, 1)]
    def opts(o, t, s):
        res = []
        if s == 0 and o == 0: res.append((1, C[t], 1))
        if s == 1 and o == 0: res.append((0, C[t], 0))
        for x in (L[t] if s == 0 else R[t]):
            res.append(x if isinstance(x, str) else (o, x, 1 - s))
        return res
    changed = True
    while changed:
        changed = False
        for st in states:
            if st in val: continue
            o, t, s = st
            op = opts(o, t, s)
            me, him = ('W', 'B') if s == 0 else ('B', 'W')
            v = None
            if not op:
                v = 'lose' if CONV == 'N' else None
                if v is None: continue
            elif any(x == me or (not isinstance(x, str) and val.get(x) == 'lose') for x in op):
                v = 'win'
            elif all(x == him or (not isinstance(x, str) and val.get(x) == 'win') for x in op):
                v = 'lose'
            if v: val[st] = v; changed = True
    out = {}
    for s, c in ((0, 'w'), (1, 'b')):
        v = val.get((0, 0, s))
        out[c] = 'D' if v is None else ('W' if (v == 'win') == (s == 0) else 'L')
    return out


ctxs = contexts()
with open('ctx_%s.pos' % TAG, 'w') as fp, open('ctx_%s.tg' % TAG, 'w') as ft, open('ctx_%s.pred' % TAG, 'w') as fr:
    for k, (ws, bs) in enumerate(ctxs):
        cstr = " ".join(["P" + name(*s) for s in sorted(ws)] + ["p" + name(*s) for s in sorted(bs)])
        for kings, pawns in GROUP:
            for stm in 'bw':
                fp.write(" ".join(x for x in (kings, pawns, cstr, stm, '-') if x) + "\n")
        L, R, C = build((ws, bs, None))
        parts = []
        for i in range(len(L)):
            parts.append("%d: L=%s R=%s C=%d" % (i, ",".join(map(str, L[i])), ",".join(map(str, R[i])), C[i]))
        ft.write("ctx%d[%s] | %d | %s\n" % (k, cstr if cstr else 'empty', len(L), " ; ".join(parts)))
        pr = over_plus(L, R, C)
        fr.write("ctx%d[%s] w %s b %s\n" % (k, cstr if cstr else 'empty', pr['w'], pr['b']))
print(len(ctxs), "contexts")
