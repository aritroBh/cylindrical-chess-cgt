#!/usr/bin/env python3
"""Referee's own implementation of the local game L_T(Q_Z) of LOOPY Definition 2.6 for the case needed here:
s has a bare king (no pawn), s-bar has a king (confined to the files F_Z) and exactly ONE pawn.
s = White: s-bar's pawn is a black pawn moving down.  s = Black is the mirror image, handled by the self-duality
(here we also run it directly by colour-reversing the position, to test the duality claim).
State: (sk, bk, pp, stm) with stm 0 = s to move, 1 = s-bar to move.  pp = square of s-bar's pawn.
Rules (Definition 2.6):
 - s may pass when not in check (pass clears e.p. - no e.p. is possible here: s has no pawn)
 - s-bar may not pass; its king may step only on squares of F_Z; its pawn moves freely (push, double push from start rank)
 - first promotion by s-bar wins for s-bar if (queen clause) no legal s move captures the new queen, else it is a failure;
   with clause=False (L1_P) every promotion wins
 - s mated (in check, no legal move) = s-bar wins;  s cannot be stalemated (pass);  s-bar with no move = failure
 - s captures the pawn -> s-bar can never win (lone king cannot mate) = failure
 - s-bar must win with one of its first T moves
Colour handling: we solve the game with s-bar = the side whose pawn goes DOWN when flip=False  (s = White at the bottom).
Use mirror(): rank r -> H-1-r, to run a position in which s = Black.
Usage: lg2.py BOARD "pos with s to move"  Fz_files  clause(0/1)   e.g.  lg2.py cyl:8x8 "wk=g4 bk=a4 pp=a5" hab 1
"""
import sys
from psolve import setup, nbr, king_nb, adj
import psolve

def run(board, sk, bk, pp, fz, clause, Tmax=60, verbose=False):
    setup(board)
    W, H, WRAP = psolve.W, psolve.H, psolve.WRAP
    fzset = set(ord(c) - ord('a') for c in fz)
    d = -1   # s-bar pawn goes down (rank index decreasing); s-bar promotes on rank index 0
    start = H - 2
    last = 0
    def pawn_attacks(p):   # squares attacked by the s-bar pawn at p (it attacks diagonally downward)
        out = []
        for df in (-1, 1):
            t = nbr(p, df, d)
            if t >= 0:
                out.append(t)
        return out
    def s_in_check(sk_, pp_):
        return pp_ >= 0 and sk_ in pawn_attacks(pp_)
    def s_moves(sk_, bk_, pp_):
        """legal king moves of s (list of (newsk, newpp)); newpp = -1 if the pawn is captured"""
        out = []
        for t in king_nb(sk_):
            if adj(t, bk_):
                continue
            if t == pp_:
                out.append((t, -1))
                continue
            if pp_ >= 0 and t in pawn_attacks(pp_):
                continue
            out.append((t, pp_))
        return out
    # states
    from functools import lru_cache
    def sbar_moves(sk_, bk_, pp_):
        """list of ('promo', square) or ('mv', newbk, newpp)"""
        out = []
        for t in king_nb(bk_):
            if t == pp_ or t % W not in fzset:
                continue
            if adj(t, sk_):
                continue
            out.append(('mv', t, pp_))
        t = nbr(pp_, 0, d)
        if t >= 0 and t != sk_ and t != bk_:
            if t // W == last:
                out.append(('promo', t))
            else:
                out.append(('mv', bk_, t))
                if pp_ // W == start:
                    t2 = nbr(t, 0, d)
                    if t2 >= 0 and t2 != sk_ and t2 != bk_:
                        out.append(('mv', bk_, t2))
        return out
    def promo_wins(sk_, bk_, sq):
        if not clause:
            return True
        # queen on sq can be captured at once iff s king adjacent and not protected by s-bar king
        if adj(sk_, sq) and sk_ != sq and not adj(bk_, sq):
            return False
        return True
    # compute A_k sets by iteration.  A[k] = set of s-to-move states (sk,bk,pp) from which s-bar wins within k moves
    # B[k] = set of s-bar-to-move states (sk,bk,pp) from which s-bar wins within k of its moves
    # enumerate reachable states first (forward from the root, ignoring time)
    root = (sk, bk, pp)
    seenS, seenB = set([root]), set()
    stack = [('S', root)]
    while stack:
        kind, st = stack.pop()
        if kind == 'S':
            sk_, bk_, pp_ = st
            mv = s_moves(sk_, bk_, pp_)
            nxt = [(a, bk_, b) for a, b in mv]
            if not s_in_check(sk_, pp_):
                nxt.append((sk_, bk_, pp_))
            for n in nxt:
                if n[2] < 0:
                    continue   # pawn captured: failure, no need to explore
                if n not in seenB:
                    seenB.add(n); stack.append(('B', n))
        else:
            sk_, bk_, pp_ = st
            for m in sbar_moves(sk_, bk_, pp_):
                if m[0] == 'promo':
                    continue
                n = (sk_, m[1], m[2])
                if n not in seenS:
                    seenS.add(n); stack.append(('S', n))
    def s_has_move(sk_, bk_, pp_):
        return len(s_moves(sk_, bk_, pp_)) > 0
    def mated(sk_, bk_, pp_):
        return s_in_check(sk_, pp_) and not s_has_move(sk_, bk_, pp_)
    A_prev = set()   # A_0 = empty ; B_0 empty
    B_prev = set()
    Tmin = None
    A_hist = [set()]
    B_hist = [set()]
    for k in range(1, Tmax + 1):
        # B_k: exists sbar move that wins at once or leads to S with A_{k-1}
        Bk = set()
        for st in seenB:
            sk_, bk_, pp_ = st
            ok = False
            for m in sbar_moves(sk_, bk_, pp_):
                if m[0] == 'promo':
                    if promo_wins(sk_, bk_, m[1]):
                        ok = True; break
                else:
                    n = (sk_, m[1], m[2])
                    if mated(*n) or n in A_hist[k - 1]:
                        ok = True; break
            if ok:
                Bk.add(st)
        Ak = set()
        for st in seenS:
            sk_, bk_, pp_ = st
            nxt = [(a, bk_, b) for a, b in s_moves(sk_, bk_, pp_)]
            if not s_in_check(sk_, pp_):
                nxt.append((sk_, bk_, pp_))
            if not nxt:
                continue      # mated state: handled at the s-bar move that created it
            if all((n[2] >= 0 and n in Bk) for n in nxt):
                Ak.add(st)
        A_hist.append(Ak); B_hist.append(Bk)
        if root in Ak and Tmin is None:
            Tmin = k
        if Ak == A_hist[k - 1] and Bk == B_hist[k - 1]:
            break
    # (L3) check: along lines where s-bar plays only winning moves (for T = Tmin), does s ever lack a legal non-pass move
    # while not in check?  (that would be a stalemate of the real s)
    stale = 0; snodes = 0
    if Tmin is not None:
        seen = set()
        stack = [(root, Tmin)]
        while stack:
            st, kk = stack.pop()
            if (st, kk) in seen: continue
            seen.add((st, kk))
            sk_, bk_, pp_ = st
            snodes += 1
            mv = s_moves(sk_, bk_, pp_)
            if not mv and not s_in_check(sk_, pp_):
                stale += 1
            nxt = [(a, bk_, b) for a, b in mv]
            if not s_in_check(sk_, pp_):
                nxt.append((sk_, bk_, pp_))
            for n in nxt:
                if n[2] < 0: continue
                # s-bar winning moves from n with budget kk
                for m in sbar_moves(*n):
                    if m[0] == 'promo':
                        continue
                    n2 = (n[0], m[1], m[2])
                    if mated(*n2):
                        continue
                    if kk - 1 >= 1 and n2 in A_hist[kk - 1]:
                        stack.append((n2, kk - 1))
    return Tmin, stale, snodes

def sqn(name):
    return (int(name[1:]) - 1) * psolve.W + (ord(name[0]) - ord('a'))

if __name__ == '__main__':
    board = sys.argv[1]
    setup(board)
    args = dict(a.split('=') for a in sys.argv[2].split())
    T = run(board, sqn(args['sk']), sqn(args['bk']), sqn(args['pp']), sys.argv[3], int(sys.argv[4]))
    print(T)
