"""Independent referee check (no cylcgt/lemmas code in the models).
Own pawn rules, own whole-board D (global right, alternating), own unfolded S as F = (components with own
rights, White tokens, Black tokens), own tau_P / scored tau / HSS / (E) / stopped tempo counts.
cylcgt.pawns.value is called only as a cross-check at the end."""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)

FILES = "abcdefghijklmnopqrstuvwxyz"
CFG = {"ep_aware": True, "rule": "count"}

class Bd:
    def __init__(s, W, H, wrap=False, ep=True): s.W, s.H, s.wrap, s.ep = W, H, wrap, ep
    def nb(s, f, d):
        g = f + d
        if s.wrap: return g % s.W
        return g if 0 <= g < s.W else None

def P(txt, ep=None):
    w, b = txt.split("/")
    sq = lambda t: (FILES.index(t[0]), int(t[1:]))
    return (frozenset(map(sq, w.split())), frozenset(map(sq, b.split())), ep)

def show(p):
    n = lambda s: f"{FILES[s[0]]}{s[1]}"
    return "W " + " ".join(sorted(map(n, p[0]))) + " / B " + " ".join(sorted(map(n, p[1]))) + (f" ep{n(p[2][0])}" if p[2] else "")

# ep = (target_square, double-stepped pawn square, side allowed to capture)
def epcap(bd, p, side, sqr):
    """side's pawn on sqr is capturable e.p. now (e.p.-aware passed test)."""
    if not CFG["ep_aware"] or not p[2] or p[2][1] != sqr or p[2][2] == side: return False
    f, r = sqr; enemy = p[1] if side == "W" else p[0]
    return any((g, r) in enemy for g in (bd.nb(f, -1), bd.nb(f, 1)) if g is not None)

def is_passed(bd, p, side, sqr):
    f, r = sqr; enemy = p[1] if side == "W" else p[0]
    fs = {f} | {g for g in (bd.nb(f, -1), bd.nb(f, 1)) if g is not None}
    ahead = (lambda s: s > r) if side == "W" else (lambda s: s < r)
    return not any(g in fs and ahead(s) for g, s in enemy) and not epcap(bd, p, side, sqr)

def passers(bd, p, side):
    return [q for q in (p[0] if side == "W" else p[1]) if is_passed(bd, p, side, q)]

def dist(bd, p, side):
    best = 10**9
    occ = p[0] | p[1]
    for f, r in passers(bd, p, side):
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, bd.H + 1)): continue
            d = bd.H - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)): continue
            d = r - 1 - (1 if r == bd.H - 1 else 0)
        best = min(best, d)
    return best

def credit(bd, p, mover):
    """None if no passer, else 'W'/'B' credited (race rule applied, mover = side that just moved)."""
    w, b = bool(passers(bd, p, "W")), bool(passers(bd, p, "B"))
    if not (w or b): return None
    if w != b: return "W" if w else "B"
    other = "B" if mover == "W" else "W"
    rule = CFG["rule"]
    if rule == "mover": return mover
    if rule == "opponent": return other
    return other if dist(bd, p, other) <= dist(bd, p, mover) else mover

def gen(bd, p, side):
    """moves of side from p; a right of the opponent's is dropped, own right usable."""
    W_, B_, ep = p
    mine, theirs = (W_, B_) if side == "W" else (B_, W_)
    occ = W_ | B_; d = 1 if side == "W" else -1; start = 2 if side == "W" else bd.H - 1
    out = set()
    def emit(m, t, e=None):
        out.add((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))
    for (f, r) in mine:
        rest = mine - {(f, r)}; r1 = r + d
        if not 1 <= r1 <= bd.H: continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= bd.H and (f, r2) not in occ:
                e = ((f, r1), (f, r2), "B" if side == "W" else "W") if bd.ep else None
                emit(rest | {(f, r2)}, theirs, e)
        for df in (-1, 1):
            g = bd.nb(f, df)
            if g is None: continue
            t = (g, r1)
            if t in theirs: emit(rest | {t}, theirs - {t})
            elif ep and ep[2] == side and ep[0] == t: emit(rest | {t}, theirs - {ep[1]})
    return out

def comps(bd, p):
    files = sorted({f for f, _ in p[0] | p[1]})
    if not files: return []
    groups = []
    for f in files:
        if groups and f == groups[-1][-1] + 1: groups[-1].append(f)
        else: groups.append([f])
    if bd.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bd.W - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for g in groups:
        s = set(g); e = p[2] if (p[2] and p[2][0][0] in s) else None
        out.append((frozenset(q for q in p[0] if q[0] in s), frozenset(q for q in p[1] if q[0] in s), e))
    return out

# ---- D: whole board, global right, alternating
def Dwin(bd, p, tm, memo):
    k = (p, tm)
    if k in memo: return memo[k]
    other = "B" if tm == "W" else "W"
    res = other
    for c in gen(bd, p, tm):
        cr = credit(bd, c, tm)
        r = cr if cr else Dwin(bd, c, other, memo)
        if r == tm: res = tm; break
    memo[k] = res
    return res

# ---- F: unfolded S. state: sorted tuple of live components (own rights), tokens tW, tB
def Fwin(bd, comps_, tW, tB, tm, memo):
    k = (comps_, tW, tB, tm)
    if k in memo: return memo[k]
    other = "B" if tm == "W" else "W"
    if not comps_:
        n = tW - tB
        res = ("W" if n >= 1 else "B") if tm == "W" else ("B" if n <= -1 else "W")
        memo[k] = res; return res
    res = other
    opts = []
    if tm == "W" and tW > 0: opts.append((comps_, tW - 1, tB))
    if tm == "B" and tB > 0: opts.append((comps_, tW, tB - 1))
    for i, c in enumerate(comps_):
        rest = comps_[:i] + comps_[i + 1:]
        src = c if (c[2] and c[2][2] == tm) else (c[0], c[1], None)
        for ch in gen(bd, src, tm):
            cr = credit(bd, ch, tm)  # whole moved component tested before re-split
            if cr == "W": opts.append((rest, tW + CFG["B"], tB))
            elif cr == "B": opts.append((rest, tW, tB + CFG["B"]))
            else: opts.append((tuple(sorted(rest + tuple(comps(bd, ch)), key=repr)), tW, tB))
    for (cc, a, b) in opts:
        if Fwin(bd, cc, a, b, other, memo) == tm: res = tm; break
    memo[k] = res
    return res

def outcome(wf, bf):  # winners with White first, Black first
    return {("W", "W"): "L", ("B", "B"): "R", ("W", "B"): "N", ("B", "W"): "P"}[(wf, bf)]

def o_D(bd, p):
    m = {}; return outcome(Dwin(bd, p, "W", m), Dwin(bd, p, "B", m))

def o_F(bd, p):
    m = {}; c = tuple(sorted(comps(bd, p), key=repr))
    return outcome(Fwin(bd, c, 0, 0, "W", m), Fwin(bd, c, 0, 0, "B", m))

# ---- any-order reach (D semantics: a right lapses unless its owner... any move by the non-owner drops it;
# a move by the owner of the right may use it)
def succ(bd, p):
    for side in "WB":
        src = p if (p[2] and p[2][2] == side) else (p[0], p[1], None)
        for c in gen(bd, src, side): yield side, c

def reach(bd, p):
    seen = {p}; st = [p]
    while st:
        x = st.pop()
        if passers(bd, x, "W") or passers(bd, x, "B"): continue
        for _, c in succ(bd, x):
            if c not in seen: seen.add(c); st.append(c)
    return seen

def tauP(bd, y, memo):
    if y in memo: return memo[y]
    s = set()
    if passers(bd, y, "W"): s.add("+")
    if passers(bd, y, "B"): s.add("-")
    if not s:
        for _, c in succ(bd, y): s |= tauP(bd, c, memo)
    memo[y] = frozenset(s); return memo[y]

def tauS(bd, y, memo):
    """scored tau: options into a credited terminal, by either player, from positions reached without passing one."""
    if y in memo: return memo[y]
    s = set()
    for side, c in succ(bd, y):
        cr = credit(bd, c, side)
        if cr: s.add("+" if cr == "W" else "-")
        else: s |= tauS(bd, c, memo)
    memo[y] = frozenset(s); return memo[y]

def Mstop(bd, y, side, memo):
    k = (y, side)
    if k in memo: return memo[k]
    best = 0
    for s2, c in succ(bd, y):
        add = 1 if s2 == side else 0
        if passers(bd, c, "W") or passers(bd, c, "B"): best = max(best, add)
        else: best = max(best, add + Mstop(bd, c, side, memo))
    memo[k] = best; return best

def usable(bd, p):
    if not p[2]: return False
    t, cap, side = p[2]
    mine = p[0] if side == "W" else p[1]
    f, r = cap
    return any((g, r) in mine for g in (bd.nb(f, -1), bd.nb(f, 1)) if g is not None)

def hyp(bd, X):
    mP, mS, mM = {}, {}, {}
    hssP = hssS = E = True; tmax = 0
    for y in reach(bd, X):
        if passers(bd, y, "W") or passers(bd, y, "B"): continue
        cs = comps(bd, y)
        tp = [tauP(bd, c, mP) for c in cs]; ts = [tauS(bd, c, mS) for c in cs]
        for i in range(len(cs)):
            for j in range(len(cs)):
                if i != j and "+" in tp[i] and "-" in tp[j]: hssP = False
                if i != j and "+" in ts[i] and "-" in ts[j]: hssS = False
        if len(cs) >= 2 and usable(bd, y): E = False
        tmax = max(tmax, sum(Mstop(bd, c, "W", mM) for c in cs), sum(Mstop(bd, c, "B", mM) for c in cs))
    return dict(passer_free=not (passers(bd, X, "W") or passers(bd, X, "B")), HSS_tauP=hssP, HSS_scored=hssS, E=E, tempo_max=tmax)

if __name__ == "__main__":
    b57 = Bd(5, 7)
    a3 = ((0, 3), (0, 4), "B")
    w1 = P("a4 b3 e2/a5 b4 e4", a3)
    w2 = P("a4 b2 b3 e2 e4/a5 b4 b6 e6", a3)
    from cylcgt import pawns, cgt
    for name, X in (("witness1", w1), ("witness2", w2)):
        for epa in (True, False):
            for rule in ("count", "mover", "opponent"):
                CFG.update(ep_aware=epa, rule=rule)
                outs = []
                for B in (9, 256):
                    CFG["B"] = B
                    outs.append(f"oF(B={B})={o_F(b57, X)}")
                pawns.RACE_RULE = rule; pawns.PASSED_RESPECTS_EP = epa; pawns._value.cache_clear()
                cx = pawns.Pos(X[0], X[1], X[2])
                print(name, f"ep_aware={epa} rule={rule}", *outs, f"oD={o_D(b57, X)}",
                      f"cylcgt_oS={cgt.outcome(pawns.value(pawns.Board(5, 7, False, True), cx))}", hyp(b57, X))
    CFG.update(ep_aware=True, rule="count"); pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
    pawns._value.cache_clear()
    # predecessor of witness 1
    pre = P("a2 b3 e2/a5 b4 e4")
    print("pred w1", show(pre), "passer-free", not (passers(b57, pre, "W") or passers(b57, pre, "B")))
    # HSS necessity
    b56n = Bd(5, 6, ep=False); X = P("a4 d4/b5 e5")
    for rule in ("count", "mover", "opponent"):
        CFG.update(rule=rule, B=5); print("HSS-nec", rule, o_F(b56n, X), o_D(b56n, X), hyp(b56n, X))
    CFG.update(rule="count")
    # B necessity, B=1 on flat 4x7
    b47 = Bd(4, 7); X = P("a4 d2/b5 d3 d6"); CFG["B"] = 1
    print("B-nec B=1", o_F(b47, X), o_D(b47, X), hyp(b47, X))
    CFG["B"] = 256; b4t = Bd(4, 263); X = P("a4 d2/b5 d3 d261")
    print("B-nec 4x263 B=256 oD", o_D(b4t, X))
    # M example
    b56 = Bd(5, 6, ep=False); X = P("a2 a3 c2 d2 d3 e3/a4 b3 d4"); m = {}
    print("M ex: comps", len(comps(b56, X)), "M_B", Mstop(b56, X, "B", m))
    Y = P("a2 a3 b3 d2 d3 e3/a4 d4")
    print("   after c2xb3 comps", [show(c) + f" M_B={Mstop(b56, c, 'B', m)}" for c in comps(b56, Y)],
          "passer-free", not (passers(b56, Y, "W") or passers(b56, Y, "B")))
    # tau example
    b88 = Bd(8, 8); X = P("b2 d6/c7")
    print("tau ex", sorted(tauP(b88, X, {})), sorted(tauS(b88, X, {})))
