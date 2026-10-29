#!/usr/bin/env python3
"""K15: independent Python re-implementation (own move generator, own solver, own classifier) used to
cross-check grp.c on a small cylinder.  It does not read grp.c.

usage: pycheck.py W H F wmax bmax out.tsv [ignore_leak] [allow_passer]
writes one line per root: "<group position> w -<TAB><class>" with the same class names as grp.c --dumproots.
"""
import sys, itertools
sys.setrecursionlimit(10000)

W, H, F, WM, BM = map(int, sys.argv[1:6])
OUT = sys.argv[6]
import os
FLAT = os.environ.get('FLAT') == '1'
IGNORE_LEAK = len(sys.argv) > 7 and sys.argv[7] == "1"
ALLOW_PASSER = len(sys.argv) > 8 and sys.argv[8] == "1"

FILES = "abcdefgh"
ALLSQ = [(f, r) for r in range(H) for f in range(W)]  # (file, rank0)
PSQ = [(f, r) for f in range(F) for r in range(1, H - 1)]


def nbrs(s):
    f, r = s
    out = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            q = r + dr
            if 0 <= q < H and (not FLAT or 0 <= f + df < W):
                out.append(((f + df) % W, q))
    return out


NB = {s: tuple(dict.fromkeys(nbrs(s))) for s in ALLSQ}


def adjacent(a, b):
    return b in NB[a]


def pawn_attacks(color, s):
    """squares attacked by a pawn of color on s (0 white, 1 black)"""
    f, r = s
    q = r + (1 if color == 0 else -1)
    if not (0 <= q < H):
        return ()
    return tuple(((f - 1) % W, q) if d < 0 else ((f + 1) % W, q) for d in (-1, 1) if not FLAT or 0 <= f + d < W)


def attacked_by(color, pawns, s):
    # is s attacked by any pawn of `color` in set pawns
    for p in pawns:
        if s in pawn_attacks(color, p):
            return True
    return False


# state: (wk, bk, wp, bp, stm, ep) ; ep = None or (target_sq, captured_sq)
def legal_pos(wk, bk, wp, bp, stm):
    if wk == bk or adjacent(wk, bk) or wk in wp or wk in bp or bk in wp or bk in bp:
        return False
    if stm == 0 and attacked_by(0, wp, bk):
        return False
    if stm == 1 and attacked_by(1, bp, wk):
        return False
    return True


def gen_moves(wk, bk, wp, bp, stm, ep, with_pass):
    """yield (kind, next_state or 'WIN', kleave); next_state = (wk,bk,wp,bp,stm',ep')"""
    me = stm
    ks, ko = (wk, bk) if me == 0 else (bk, wk)
    myp, opp = (wp, bp) if me == 0 else (bp, wp)
    oc = 1 - me
    res = []
    in_check = attacked_by(oc, opp, ks)
    if with_pass and not in_check:
        res.append(("pass", (wk, bk, wp, bp, 1 - me, None), False))
    for t in NB[ks]:
        if t in myp or t == ko or adjacent(t, ko):
            continue
        opp2 = opp - {t} if t in opp else opp
        if attacked_by(oc, opp2, t):
            continue
        nwp, nbp = (wp, opp2) if me == 0 else (opp2, bp)
        nwk, nbk = (t, bk) if me == 0 else (wk, t)
        res.append(("king", (nwk, nbk, nwp, nbp, 1 - me, None), t[0] >= F))
    d = 1 if me == 0 else -1
    start = 1 if me == 0 else H - 2
    last = H - 1 if me == 0 else 0
    occ = set(wp) | set(bp)
    for p in myp:
        f, r = p
        r1 = r + d
        # push
        t = (f, r1)
        if t != wk and t != bk and t not in occ:
            if r1 == last:
                if not attacked_by(oc, opp, ks):
                    res.append(("pawn", "WIN", False))
            else:
                if not attacked_by(oc, opp, ks):
                    nm = (myp - {p}) | {t}
                    nwp, nbp = (nm, opp) if me == 0 else (opp, nm)
                    res.append(("pawn", (wk, bk, nwp, nbp, 1 - me, None), False))
                    if r == start:
                        t2 = (f, r + 2 * d)
                        if t2 != wk and t2 != bk and t2 not in occ:
                            nm2 = (myp - {p}) | {t2}
                            nwp, nbp = (nm2, opp) if me == 0 else (opp, nm2)
                            res.append(("pawn", (wk, bk, nwp, nbp, 1 - me, (t, t2)), False))
        # captures
        for t in pawn_attacks(me, p):
            if t in opp:
                opp2 = opp - {t}
                if attacked_by(oc, opp2, ks):
                    continue
                nm = (myp - {p}) | {t}
                nwp, nbp = (nm, opp2) if me == 0 else (opp2, nm)
                res.append(("pawn", (wk, bk, nwp, nbp, 1 - me, None), False))
    if ep is not None:
        T, C = ep
        for p in myp:
            if p[1] == C[1] and T in pawn_attacks(me, p):
                opp2 = opp - {C}
                if attacked_by(oc, opp2, ks):
                    continue
                nm = (myp - {p}) | {T}
                nwp, nbp = (nm, opp2) if me == 0 else (opp2, nm)
                res.append(("pawn", (wk, bk, nwp, nbp, 1 - me, None), False))
    return res


VAL = {}  # (wk,bk,wp,bp,stm,ep) -> 0 draw, 1 win(mover), 2 loss(mover)


def solve_layer(wp, bp):
    """retrograde over all king placements of layer (wp,bp); relies on VAL of later layers."""
    states = {}
    for wk in ALLSQ:
        for bk in ALLSQ:
            for stm in (0, 1):
                if legal_pos(wk, bk, wp, bp, stm):
                    states[(wk, bk, stm)] = None
    cnt = {}
    drawopt = {}
    preds = {}
    queue = []
    val = {}
    for (wk, bk, stm) in states:
        ms = gen_moves(wk, bk, wp, bp, stm, None, True)
        win = False
        c = 0
        dr = False
        succ_in = []
        for kind, nxt, kl in ms:
            if nxt == "WIN":
                win = True
                break
            nwk, nbk, nwp, nbp, nstm, nep = nxt
            if nwp == wp and nbp == bp and nep is None:
                succ_in.append((nwk, nbk, nstm))
                c += 1
            else:
                v = value(nxt)
                if v == 2:
                    win = True
                    break
                if v == 0:
                    dr = True
        s = (wk, bk, stm)
        if win:
            val[s] = 1
            queue.append(s)
            continue
        if not ms:
            ks = bk if stm else wk
            if attacked_by(1 - stm, bp if stm == 0 else wp, ks):
                val[s] = 2
                queue.append(s)
            continue
        cnt[s] = c
        drawopt[s] = dr
        for t in succ_in:
            preds.setdefault(t, []).append(s)
        if c == 0 and not dr:
            val[s] = 2
            queue.append(s)
    qi = 0
    while qi < len(queue):
        v = queue[qi]
        qi += 1
        for u in preds.get(v, ()):
            if u in val:
                continue
            if val[v] == 2:
                val[u] = 1
                queue.append(u)
            else:
                cnt[u] -= 1
                if cnt[u] == 0 and not drawopt[u]:
                    val[u] = 2
                    queue.append(u)
    for s in states:
        wk, bk, stm = s
        VAL[(wk, bk, wp, bp, stm, None)] = val.get(s, 0)


def value(st):
    """value for mover of a state of an already solved layer (plain) or ep state"""
    wk, bk, wp, bp, stm, ep = st
    if ep is None:
        return VAL[st]
    ms = gen_moves(wk, bk, wp, bp, stm, ep, True)
    ks = bk if stm else wk
    if not ms:
        return 2 if attacked_by(1 - stm, wp if stm else bp, ks) else 0
    anyd = False
    for kind, nxt, kl in ms:
        if nxt == "WIN":
            return 1
        v = value(nxt)
        if v == 2:
            return 1
        if v == 0:
            anyd = True
    return 0 if anyd else 2


def subsets(sq, k):
    for c in range(k + 1):
        for comb in itertools.combinations(sq, c):
            yield frozenset(comb)


layers = []
for wp in subsets(PSQ, WM):
    for bp in subsets(PSQ, BM):
        if wp & bp:
            continue
        adv = sum(r for f, r in wp) + sum(H - 1 - r for f, r in bp)
        layers.append((len(wp) + len(bp), -adv, sorted(wp), sorted(bp), wp, bp))
layers.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
for _, _, _, _, wp, bp in layers:
    solve_layer(wp, bp)
print("solved", len(layers), "layers", file=sys.stderr)


# ---- classification -------------------------------------------------------------------------------------------
def analyze(wk, bk, wp, bp):
    """returns dict: safe[s] list of states (wk,bk,wp,bp), win[s], suic[s], leak, check"""
    info = {"safe": [[], []], "win": [0, 0], "suic": [0, 0], "leak": False, "check": False}
    if attacked_by(0, wp, bk) or attacked_by(1, bp, wk):
        info["check"] = True
    for s in (0, 1):
        for kind, nxt, kl in gen_moves(wk, bk, wp, bp, s, None, False):
            if nxt == "WIN":
                info["win"][s] += 1
                continue
            v = value(nxt)  # value for opponent to move
            if v == 1:
                info["suic"][s] += 1
            elif v == 2:
                info["win"][s] += 1
            else:
                if kl:
                    if IGNORE_LEAK:
                        continue
                    info["leak"] = True
                info["safe"][s].append(nxt[:4])
    return info


def bad(I):
    return I["check"] or I["win"][0] or I["win"][1] or I["leak"]


def has_shuttle(root, s, I, need_frozen_other):
    wk, bk, wp, bp = root
    for t in I["safe"][s]:
        if t[2] != wp or t[3] != bp:
            continue
        nk = t[1] if s else t[0]
        if nk[0] >= F:
            continue
        J = analyze(*t)
        if J["check"] or J["win"][0] or J["win"][1]:
            continue
        if need_frozen_other and J["safe"][1 - s]:
            continue
        if root in J["safe"][s]:
            return True
    return False


def passed_side(wp, bp, side):
    mine, theirs = (wp, bp) if side == 0 else (bp, wp)
    for (f, r) in mine:
        files = {f, (f - 1) % W, (f + 1) % W} if not FLAT else {f - 1, f, f + 1}
        blocked = any(g in files and (s > r if side == 0 else s < r) for g, s in theirs)
        if not blocked:
            return True
    return False


def closure(root, kind):
    """kind: 'on','off','dud','over','under' (pure bisimulation tests). returns True/False"""
    seen = {root}
    stack = [root]
    p = 1 if kind == "over" else 0
    q = 1 - p
    count = 0
    while stack:
        y = stack.pop()
        count += 1
        if count > 6000:
            return False
        I = analyze(*y)
        if bad(I):
            return False
        sw, sb = len(I["safe"][0]), len(I["safe"][1])
        if kind == "on":
            if not (sw >= 1 and sb == 0):
                return False
            nxt = I["safe"][0]
        elif kind == "off":
            if not (sb >= 1 and sw == 0):
                return False
            nxt = I["safe"][1]
        elif kind == "dud":
            if not (sw >= 1 and sb >= 1):
                return False
            nxt = I["safe"][0] + I["safe"][1]
        else:
            if len(I["safe"][p]) < 1 or len(I["safe"][q]) < 1:
                return False
            nxt = I["safe"][p]
            for z in I["safe"][q]:
                Z = analyze(*z)
                if bad(Z) or Z["safe"][0] or Z["safe"][1]:
                    return False
        for t in nxt:
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return True


def classify(root):
    wk, bk, wp, bp = root
    I = analyze(*root)
    if I["check"]:
        return "check"
    if I["win"][0] or I["win"][1]:
        return "threat"
    sw, sb = len(I["safe"][0]), len(I["safe"][1])
    if sw == 0 and sb == 0:
        return "frozen"
    cls = None
    if sw and not sb and has_shuttle(root, 0, I, True):
        cls = "on"
    elif sb and not sw and has_shuttle(root, 1, I, True):
        cls = "off"
    if sw and not sb and closure(root, "on"):
        return "on"
    if sb and not sw and closure(root, "off"):
        return "off"
    if sw and sb and not I["leak"]:
        for k in ("dud", "over", "under"):
            if closure(root, k):
                return k
    if cls:
        return cls
    return "leak" if I["leak"] else "mixed"


with open(OUT, "w") as fo:
    for _, _, _, _, wp, bp in layers:
        if len(wp) + len(bp) == 0:
            continue
        if not ALLOW_PASSER and (passed_side(wp, bp, 0) or passed_side(wp, bp, 1)):
            continue
        for wk in ALLSQ:
            if wk[0] >= F or wk in wp or wk in bp:
                continue
            for bk in ALLSQ:
                if bk[0] >= F or bk == wk or bk in wp or bk in bp or adjacent(wk, bk):
                    continue
                cls = classify((wk, bk, wp, bp))
                nm = lambda s: f"{FILES[s[0]]}{s[1] + 1}"
                pos = f"K{nm(wk)} k{nm(bk)} " + " ".join(sorted(["P" + nm(s) for s in wp]) + sorted(["p" + nm(s) for s in bp]))
                fo.write(pos + " w -\t" + cls + "\n")
print("done", file=sys.stderr)
