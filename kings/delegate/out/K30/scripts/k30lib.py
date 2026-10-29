#!/usr/bin/env python3
"""k30lib.py -- K30: the strategies of PROOF.md written as finite rules, on top of kpm.py (own move generator, SPEC.md only).

Coordinates relative to the Black pawn p on file e (index 4) and rank r (1-based): (dx, dy) with dx the signed file
offset (on the cylinder reduced to -4..3) and dy = rank - r.  The squares used by the proof, for pawn rank r:
    F = (0,-1)  M = (0,-2)  L = (-1,-2)  R = (+1,-2)
"""
import sys
sys.path.insert(0, '.')
from kpm import *

E = 4


def rel(B, s, p):
    dx = B.f(s) - B.f(p)
    if B.cyl:
        dx = ((dx + B.W // 2) % B.W) - B.W // 2
    return (dx, B.r(s) - B.r(p))


def sq_at(B, p, dx, dy):
    """square at relative (dx,dy) from pawn square p, or -1"""
    return B.step(p, dx, dy)


def goto(B, pos, p, tx, ty):
    """the ordinary (non-capturing or capturing) king move of the side to move (White) to relative (tx,ty), as a position"""
    target = sq_at(B, p, tx, ty)
    for lab, k, t in gen(B, pos):
        if k == 'n' and t[1] == target and pos[3] == ():   # white king move
            return t
    return None


def white_rule(B, pos):
    """White to move in a king vs king+pawn position (pawn on the e-file).  Returns the position after the rule move,
       or None if White has no legal move.  Raises AssertionError if the rule is not defined (which would refute PROOF.md)."""
    stm, wk, bk, wp, bp, ep = pos
    assert stm == 0 and wp == () and len(bp) == 1
    p = bp[0]
    moves = gen(B, pos)
    if not moves:
        return None
    # R1: capture the pawn if that is legal
    for lab, k, t in moves:
        if k == 'n' and t[4] == ():
            return t
    dx, dy = rel(B, wk, p)
    bx, by = rel(B, bk, p)
    t = None
    if (dx, dy) == (0, -1):                              # F: retreat to M
        t = goto(B, pos, p, 0, -2)
    elif (dx, dy) == (0, -2):                            # M: go to F, or take the opposition square on the king's file
        t = goto(B, pos, p, 0, -1)
        if t is None:
            assert (bx, by) in ((-1, 0), (1, 0)), ('M rule', fmt(B, pos))
            t = goto(B, pos, p, bx, -2)
    elif (dx, dy) in ((-1, -2), (1, -2)):                # L or R, not in check: to M, else to F
        t = goto(B, pos, p, 0, -2)
        if t is None:
            t = goto(B, pos, p, 0, -1)
    elif dy == -1 and abs(dx) == 1:                      # L or R after the pawn push (in check): to the square below the pawn
        t = goto(B, pos, p, 0, -1)
    assert t is not None, ('rule undefined', fmt(B, pos))
    return t


def inS(B, pos):
    """membership of a Black-to-move king+pawn position in the invariant S of PROOF.md"""
    stm, wk, bk, wp, bp, ep = pos
    if stm != 1 or wp != () or len(bp) != 1:
        return False
    p = bp[0]
    if B.f(p) != E:
        return False
    r = B.r(p) + 1
    w = rel(B, wk, p)
    b = rel(B, bk, p)
    if r >= 4:
        if w in ((0, -1), (0, -2)):
            return True
        if w == (-1, -2):
            return not (b[0] in (1, 2) and -3 <= b[1] <= 0)
        if w == (1, -2):
            return not (b[0] in (-1, -2) and -3 <= b[1] <= 0)
        return False
    if r == 3:
        if w == (0, -1):
            return True
        if w == (0, -2):
            return b not in ((-1, 0), (1, 0))
        if w == (-1, -2):
            return b == (-1, 0)
        if w == (1, -2):
            return b == (1, 0)
        return False
    if r == 2:
        return w == (0, -1) and b in ((-1, 1), (1, 1))
    return False


def all_S(B):
    """every legal position of S (enumerated by brute force over king squares and pawn ranks)"""
    out = []
    for r in range(2, B.H):          # pawn rank r (1-based), 2..H-1
        ps = (r - 1) * B.W + E
        for wk in range(B.N):
            for bk in range(B.N):
                pos = norm(B, (1, wk, bk, (), (ps,), -1))
                if legal(B, pos) and inS(B, pos):
                    out.append(pos)
    return out


def check_S_closure(B, S, log=print):
    """for every position of S and every Black move: no promotion, no mate of White, and the rule reply is legal and lands
       in S (or captures the pawn, or White is stalemated).  Returns the number of (position, Black move) pairs."""
    pairs = 0
    white_states = set()
    stats = dict(capture=0, stalemate_white=0, black_stalemate=0, ok=0)
    for pos in S:
        ms = gen(B, pos)
        if not ms:
            assert not in_check(B, pos, 1)          # a mated Black king cannot occur (White has no attacker)
            stats['black_stalemate'] += 1
            continue
        for lab, k, t in ms:
            pairs += 1
            assert k == 'n', ('Black promotes', fmt(B, pos), lab)
            assert legal(B, t)
            white_states.add(t)
            rep = white_rule(B, t)
            if rep is None:
                assert not in_check(B, t, 0), ('White mated', fmt(B, t))
                stats['stalemate_white'] += 1
            elif rep[4] == ():
                stats['capture'] += 1
            else:
                assert legal(B, rep) and inS(B, rep), ('leaves S', fmt(B, pos), lab, fmt(B, rep))
                stats['ok'] += 1
    return pairs, white_states, stats


def make_sigma(B):
    """White's strategy sigma of PROOF.md part B as a function (pos, sortie_square) -> list of options"""
    X0 = parse(B, 'Ke6 Pd7 kd8 pe7 w -')
    sq = B.sq
    d7, e7, c7, d8, e6, e5, d5, f5 = (sq(x) for x in 'd7 e7 c7 d8 e6 e5 d5 f5'.split())

    def king_move_to(pos, target):
        for lab, k, t in gen(B, pos):
            if k == 'n' and t[1] == target:
                return t
        return None

    def sigma(pos, sortie):
        """list of White options (positions after the move); [] means White has no legal move (stalemate); raises if undefined"""
        stm, wk, bk, wp, bp, ep = pos
        assert stm == 0
        ms = gen(B, pos)
        if not ms:
            assert not in_check(B, pos, 0), ('White mated', fmt(B, pos))
            return []
        if wp == ():                                         # king + Black pawn against king
            if bp == ():
                raise AssertionError('K v K should be terminal')
            r = white_rule(B, pos)
            return [r]
        assert wp == (d7,), fmt(B, pos)
        if pos == X0:
            t = king_move_to(pos, sortie)
            assert t is not None
            return [t]
        if bp == (e7,):
            if wk in (e5, d5, f5) and bk == c7:               # after the sortie and ...Kc7
                t = king_move_to(pos, e6)
                assert t is not None
                return [t]
            if wk == e6 and bk not in (c7, d8):               # Black king has left c7 for the queenside: take the pawn
                for lab, k, t in ms:
                    if k == 'n' and t[4] == ():
                        return [t]
                raise AssertionError(('cannot take e7', fmt(B, pos)))
            raise AssertionError(('sigma undefined', fmt(B, pos)))
        if bp:                                               # a Black pawn pushed next to the sortie king: take it
            for lab, k, t in ms:
                if k == 'n' and t[4] == ():
                    return [t]
            raise AssertionError(('cannot take pushed pawn', fmt(B, pos)))
        # free mode: White king and pawn d7 against a lone king: any king move (never the pawn)
        km = [t for lab, k, t in ms if k == 'n' and t[3] == (d7,) and t[2] == bk]
        assert km, ('only promotions left for White', fmt(B, pos))
        return km


    return X0, sigma
