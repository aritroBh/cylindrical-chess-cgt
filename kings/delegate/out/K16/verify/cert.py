#!/usr/bin/env python3
"""Referee's own certificate for Theorem 2.11K (and the old conjecture), written from the LOOPY text only."""
import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/verify')
from mine import *

def rho(b, color, sq):  # rank from beta's side, 1-based
    return sq[1] + 1 if color == 0 else b.H - sq[1]

def pdist(b, color, sq):  # d for a pawn of color 'color' at sq: H - rho - [rho == 2]
    r = rho(b, color, sq)
    return b.H - r - (1 if r == 2 else 0)

def cert_static(b, pos, beta, p, variant=0):
    """H1, H2, H4, H5K, SQ for pawn p of beta. Returns None if not certified, else dict(e,d,...).
    variant 0 = G^K, 1 = G^K1 (king may not step on squares attacked by a remaining beta pawn)"""
    wk, bk, wp, bp, stm, ep = pos
    omega = 1 - beta
    bpawns = wp if beta == 0 else bp
    opawns = bp if beta == 0 else wp
    kb = wk if beta == 0 else bk
    ko = bk if beta == 0 else wk
    H = b.H
    f, r0 = p
    rp = rho(b, beta, p)
    # H1
    for g in [f] + b.adjfiles(f):
        for q in opawns:
            if q[0] == g and rho(b, beta, q) > rp: return None
    # p cannot be taken e.p. at y: only if omega to move and ep square is p's skipped square
    if stm == omega and ep is not None:
        # skipped square directly behind p (for beta)
        beh = (f, r0 - (1 if beta == 0 else -1))
        if ep == beh:
            for g in b.adjfiles(f):
                if (g, r0) in opawns: return None
    # path free of pawns and kings (promotion square included)
    dirb = 1 if beta == 0 else -1
    rr = r0 + dirb
    while 0 <= rr < H:
        sq = (f, rr)
        if sq in wp or sq in bp or sq == wk or sq == bk: return None
        rr += dirb
    # H2
    for g in b.adjfiles(kb[0]):
        for q in wp | bp:
            if q[0] == g: return None
    # H4
    for q in bpawns:
        if q == p: continue
        if q[0] in b.adjfiles(f) and rho(b, beta, q) > rp + 1: return None
    d = pdist(b, beta, p)
    e = d if stm == omega else d - 1
    # SQ
    # squares: q_0 = p, then each push (double step first if rp == 2)
    qs = []
    cur = r0
    qs.append((f, cur))
    if rp == 2:
        cur += 2 * dirb; qs.append((f, cur))
    while True:
        cur += dirb
        if not (0 <= cur < H): break
        qs.append((f, cur))
    assert len(qs) == d + 1, (qs, d)
    for j, q in enumerate(qs):
        if j == 0 and stm != omega: continue
        n = j if stm == omega else j - 1
        if b.dist(ko, q) < n + 2: return None
    # H5K: DFS over G^K_omega
    if e >= 1 and mu_within(b, beta, opawns, bpawns - {p}, ko, kb, ep if stm == omega else None, e, variant):
        return None
    return dict(e=e, d=d, qs=qs)

import os
KV2 = bool(os.environ.get('KV2'))
def mu_within(b, beta, opawns, bpaw, ko, kb, ep, e, variant):
    """Can omega promote a pawn within e moves in G^K_omega (p deleted)? omega = 1-beta."""
    omega = 1 - beta
    H = b.H
    dr = 1 if omega == 0 else -1
    start = 1 if omega == 0 else H - 2
    last = H - 1 if omega == 0 else 0
    def rec(opw, bpw, k, ep_, left):
        if left == 0: return False
        occ = set(opw) | set(bpw) | {k, kb}
        for pw in opw:
            f, r = pw
            t = (f, r + dr)
            if t not in occ:
                if t[1] == last: return True
                if rec((opw - {pw}) | {t}, bpw, k, None, left - 1): return True
                if r == start:
                    t2 = (f, r + 2 * dr)
                    if t2 not in occ and rec((opw - {pw}) | {t2}, bpw, k, None, left - 1): return True
            for df in (-1, 1):
                g = b.ff(f, df)
                if g is None: continue
                t = (g, r + dr)
                if t in bpw:
                    if t[1] == last: return True
                    if rec((opw - {pw}) | {t}, bpw - {t}, k, None, left - 1): return True
                elif ep_ is not None and t == ep_:
                    vic = (g, r)
                    if vic in bpw:
                        if rec((opw - {pw}) | {t}, bpw - {vic}, k, None, left - 1): return True
        for t in ([] if KV2 else b.nb(k)):
            if t in opw or t == kb or b.dist(t, kb) < 2: continue
            if variant == 1:
                # attacked by a remaining beta pawn
                bc = beta
                pawns_att = False
                for q in bpw:
                    if t in pawn_attacks_sq(b, bc, q): pawns_att = True
                if pawns_att: continue
            if rec(opw, bpw - {t}, t, None, left - 1): return True
        return False
    return rec(frozenset(opawns), frozenset(bpaw), ko, ep, e)

def ns_sim(b, pos, beta, p):
    """Play Pi (beta pushes p every turn) against ALL omega legal moves in the real P game.
    Returns (ok, kind). kind in {'ok','stalemate','other'}; 'other' = beta cannot push / p captured / omega promotes."""
    omega = 1 - beta
    H = b.H
    dirb = 1 if beta == 0 else -1
    startb = 1 if beta == 0 else H - 2
    lastb = H - 1 if beta == 0 else 0
    res = {'stalemate': False, 'other': False}
    def beta_move(pos, pp):
        wk, bk, wp, bp, stm, ep = pos
        own = wp if beta == 0 else bp
        opp = bp if beta == 0 else wp
        if pp not in own: return None  # captured
        f, r = pp
        mv = moves(b, pos)
        if r + dirb == lastb:
            for (np_, flag) in mv:
                nown = np_[2] if beta == 0 else np_[3]
                nopp = np_[3] if beta == 0 else np_[2]
                if flag and nown == own - {pp} and nopp == opp and np_[0] == wk and np_[1] == bk:
                    return ('win', None, None)
            return None
        tgt = (f, r + (2 if r == startb else 1) * dirb)
        for (np_, flag) in mv:
            nown = np_[2] if beta == 0 else np_[3]
            nopp = np_[3] if beta == 0 else np_[2]
            if (not flag) and nown == (own - {pp}) | {tgt} and nopp == opp and np_[0] == wk and np_[1] == bk:
                return ('move', np_, tgt)
        return None
    def rec(pos, pp, beta_to_move):
        if beta_to_move:
            r = beta_move(pos, pp)
            if r is None:
                res['other'] = True; return
            if r[0] == 'win': return
            rec(r[1], r[2], False)
        else:
            mv = moves(b, pos)
            if not mv:
                if in_check(b, pos, omega): return  # mate, beta wins
                res['stalemate'] = True; return
            for (np_, flag) in mv:
                if flag:
                    res['other'] = True; continue
                pawns = np_[2] if beta == 0 else np_[3]
                if pp not in pawns:
                    res['other'] = True; continue
                rec(np_, pp, True)
    rec(pos, p, pos[4] == beta)
    if res['other']: return False, 'other'
    if res['stalemate']: return False, 'stalemate'
    return True, 'ok'

def h3k(b, pos, beta, e):
    """(H3K) for every square x with d(x,k_omega) <= e-1 there is a king neighbour t, d(t,k_beta)>=2, no pawn on files of t, t-1, t+1."""
    wk, bk, wp, bp, stm, ep = pos
    ko = bk if beta == 0 else wk
    kb = wk if beta == 0 else bk
    if e < 1: return True
    pf = {q[0] for q in wp | bp}
    def fileclear(t):
        for g in [t[0]] + b.adjfiles(t[0]):
            if g in pf: return False
        return True
    for f in range(b.W):
        for r in range(b.H):
            x = (f, r)
            if b.dist(x, ko) <= e - 1:
                if not any(b.dist(t, kb) >= 2 and fileclear(t) for t in b.nb(x)): return False
    return True

def h3_at_ko(b, pos, beta):
    wk, bk, wp, bp, stm, ep = pos
    ko = bk if beta == 0 else wk
    kb = wk if beta == 0 else bk
    pf = {q[0] for q in wp | bp}
    def fileclear(t):
        for g in [t[0]] + b.adjfiles(t[0]):
            if g in pf: return False
        return True
    return any(b.dist(t, kb) >= 2 and fileclear(t) for t in b.nb(ko))
