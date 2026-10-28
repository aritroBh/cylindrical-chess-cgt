"""Independent small solver (written for K17; does not use kpsolve.c) for the P model and the frozen-king model.
  mode 'P'      : real kings, first promotion wins at once for the promoter; checkmate = loss, stalemate = draw
  mode 'frozen' : a legal king move loses at once for the mover; a promotion wins at once for the promoter
Value of a state = W / L / D for the side to move (least fixed point of retrograde analysis; infinite play = draw).
Board: cyl:WxH or flat:WxH, e.p. on.  State: (wk, bk, wp, bp, stm, ep) with ep = (target, captured) or None.
"""
import sys
from collections import deque
sys.setrecursionlimit(10**6)

def parse(txt):
    t = txt.split()
    ep = None if t[-1] == "-" else t[-1]
    stm = t[-2]
    wp, bp = set(), set(); wk = bk = None
    sq = lambda s: ("abcdefgh".index(s[0]), int(s[1:]))
    for x in t[:-2]:
        c, s = x[0], sq(x[1:])
        if c == "K": wk = s
        elif c == "k": bk = s
        elif c == "P": wp.add(s)
        elif c == "p": bp.add(s)
    return wk, bk, frozenset(wp), frozenset(bp), stm, ep and (sq(ep),)

class Game:
    def __init__(self, W, H, wrap, mode):
        self.W, self.H, self.wrap, self.mode = W, H, wrap, mode
    def nf(self, f):
        if self.wrap: return f % self.W
        return f if 0 <= f < self.W else None
    def adj(self, s):
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == dr == 0: continue
                f = self.nf(s[0] + df); r = s[1] + dr
                if f is None or not (1 <= r <= self.H): continue
                out.append((f, r))
        return out
    def pawn_attacks(self, colour_pawns, white):
        d = 1 if white else -1
        out = set()
        for (f, r) in colour_pawns:
            for df in (-1, 1):
                g = self.nf(f + df)
                if g is not None and 1 <= r + d <= self.H: out.add((g, r + d))
        return out
    def in_check(self, k, own_white, wp, bp):
        return k in self.pawn_attacks(bp if own_white else wp, not own_white)
    def moves(self, st):
        """list of (kind, child) kind: 'n' normal child state, 'P' promotion (mover wins), 'K' frozen king move."""
        wk, bk, wp, bp, stm, ep = st
        white = stm == "w"
        own = wp if white else bp; opp = bp if white else wp
        ok, ek = (wk, bk) if white else (bk, wk)
        d = 1 if white else -1
        start = 2 if white else self.H - 1
        last = self.H if white else 1
        out = []
        epc = None
        if ep and self.epside(st): epc = ep[0]
        def legal(nok, nown, nopp):
            if nok in self.adj(ek) or nok == ek: return False
            nw, nb = (nown, nopp) if white else (nopp, nown)
            return not self.in_check(nok, white, nw, nb)
        # king moves
        for n in self.adj(ok):
            if n in own or n == ek or n in self.adj(ek): continue
            nopp = opp - {n}
            if not legal(n, own, nopp): continue
            if self.mode == "frozen":
                out.append(("K", None, ("K", ok, n)))
            else:
                nwk, nbk = (n, bk) if white else (wk, n)
                nwp, nbp = (own, nopp) if white else (nopp, own)
                out.append(("n", (nwk, nbk, nwp, nbp, "b" if white else "w", None), ("K", ok, n)))
        # pawn moves
        occ = set(wp) | set(bp) | {wk, bk}
        for (f, r) in own:
            r1 = r + d
            rest = own - {(f, r)}
            tgts = []
            if (f, r1) not in occ:
                tgts.append(((f, r1), None, None))
                r2 = r + 2 * d
                if r == start and (f, r2) not in occ:
                    tgts.append(((f, r2), None, ((f, r1),)))
            for df in (-1, 1):
                g = self.nf(f + df)
                if g is None: continue
                t = (g, r1)
                if t in opp: tgts.append((t, t, None))
                elif epc is not None and epc == t: tgts.append((t, ep_cap(ep, st), None))
            for (t, cap, newep) in tgts:
                nopp = opp - {cap} if cap else opp
                nown = rest | {t}
                if t[1] == last:
                    # promotion: legality with the pawn removed (a promoted officer does not change king safety vs pawns)
                    if legal(ok, rest, nopp): out.append(("P", None, ("P", (f, r), t)))
                    continue
                if not legal(ok, nown, nopp): continue
                nw, nb = (nown, nopp) if white else (nopp, nown)
                out.append(("n", (wk, bk, nw, nb, "b" if white else "w", newep), ("P", (f, r), t)))
        return out
    def epside(self, st): return True

def ep_cap(ep, st):
    # ep = ((target,),)  -> captured pawn stands on the rank of the capturer, file of target
    (t,) = ep
    wk, bk, wp, bp, stm, _ = st
    return (t[0], t[1] - 1) if stm == "w" else (t[0], t[1] + 1)

FULL = {}

def _core(roots, W, H, wrap, mode):
    g = Game(W, H, wrap, mode)
    idx = {}; states = []; kids = {}; descs = {}
    order = deque()
    for r in roots:
        if r not in idx:
            idx[r] = len(states); states.append(r); order.append(r)
    while order:
        s = order.popleft(); i = idx[s]; lst = []; ds = []
        for kind, ch, desc in g.moves(s):
            if kind == "n":
                if ch not in idx:
                    idx[ch] = len(states); states.append(ch); order.append(ch)
                lst.append(idx[ch])
            elif kind == "P": lst.append(-1)
            else: lst.append(-2)
            ds.append(desc)
        kids[i] = lst; descs[i] = ds
    n = len(states)
    val = [0] * n; parents = [[] for _ in range(n)]; q = deque()
    for i in range(n):
        for c in kids[i]:
            if c >= 0: parents[c].append(i)
    for i in range(n):
        L = kids[i]
        if -1 in L: val[i] = 1; q.append(i)
        elif len(L) == 0:
            wk, bk, wp, bp, stm, ep = states[i]
            if g.in_check(wk if stm == "w" else bk, stm == "w", wp, bp): val[i] = 2; q.append(i)
        elif all(c == -2 for c in L): val[i] = 2; q.append(i)
    cnt = [sum(1 for c in kids[i] if c != -2) for i in range(n)]
    while q:
        c = q.popleft()
        for p in parents[c]:
            if val[p]: continue
            if val[c] == 2: val[p] = 1; q.append(p)
            else:
                cnt[p] -= 1
                if cnt[p] == 0: val[p] = 2; q.append(p)
    return dict(states=states, idx=idx, kids=kids, descs=descs, val=val)

def sqs(s): return "abcdefgh"[s[0]] + str(s[1])

def white_view(v, stm):
    if v == 0: return "D"
    return "W" if (v == 1) == (stm == "w") else "L"

def report(G, txt):
    """(White-view result, move tokens with White-view values) for a position inside graph G"""
    st = parse(txt); i = G["idx"][st]; stm = st[4]
    toks = []
    for c, d in zip(G["kids"][i], G["descs"][i]):
        if c == -1: v = "W" if stm == "w" else "L"
        elif c == -2: v = "L" if stm == "w" else "W"
        else: v = white_view(G["val"][c], G["states"][c][4])
        letter = d[0] if stm == "w" else d[0].lower()
        toks.append(f"{letter}{sqs(d[1])}{sqs(d[2])}:{v}")
    return white_view(G["val"][i], stm), toks

def solve_many(texts, W, H, wrap, mode):
    G = _core([parse(t) for t in texts], W, H, wrap, mode)
    return {t: (lambda r: (r[0], r[0], r[1]))(report(G, t)) for t in texts}, len(G["states"])

def solve(txt, W, H, wrap, mode):
    G = _core([parse(txt)], W, H, wrap, mode)
    return report(G, txt)[0], len(G["states"])

if __name__ == "__main__":
    spec, mode = sys.argv[1], sys.argv[2]
    kind, dims = spec.split(":"); W, H = map(int, dims.split("x"))
    for ln in sys.stdin:
        ln = ln.strip()
        if not ln: continue
        r, n = solve(ln, W, H, kind == "cyl", mode)
        print(f"{ln} | {r} [{n} states]")


def sqs(s): return "abcdefgh"[s[0]] + str(s[1])

def tokens_of(txt, W, H, wrap, mode):
    """White-view result and the move tokens 'K<from><to>:<val>' (val from White's view), like kp --moves.
    Uses the graph just built by solve()."""
    r, n = solve(txt, W, H, wrap, mode)
    st = FULL["states"][0]; stm = st[4]
    toks = []
    for c, d in zip(FULL["kids"][0], FULL["descs"].get(0, [])):
        if c == -1: v = "W" if stm == "w" else "L"
        elif c == -2: v = "L" if stm == "w" else "W"
        else:
            cv = FULL["val"][c]; cstm = FULL["states"][c][4]
            if cv == 0: v = "D"
            else:
                white_wins = (cv == 1) == (cstm == "w")
                v = "W" if white_wins else "L"
        letter = d[0] if stm == "w" else d[0].lower()
        toks.append(f"{letter}{sqs(d[1])}{sqs(d[2])}:{v}")
    return r, toks
