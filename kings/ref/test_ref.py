"""Tests for the reference solver kings/ref/solve.py.

Run from the project root:
    .venv/bin/python -m pytest -q kings/ref/test_ref.py

Three kinds of test:
  * hand-checked positions (move lists and values worked out by hand in the comments);
  * a second, deliberately naive move generator written in this file (coordinates and dicts,
    no bitmasks) compared move for move with the solver's generator on random positions;
  * a brute-force solver (naive generator + explicit reachable game graph + counting
    retrograde) compared value for value with the layered solver.

Interpretation choices for points SPEC.md leaves open (also documented in solve.py):
  * a promotion is capped iff the resulting position would hold more than C officers;
  * on H = 4 a double step reaches the last rank and promotes;
  * an input e.p. target inconsistent with the position is X; with --ep off it is ignored.
"""

import os
import random
import subprocess
import sys
import zlib
from collections import defaultdict

import pytest

from kings.ref.solve import CAPPED, DRAW, EXIT, LOSS, WHITE, WIN, make_solver

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------- helpers

def solve(board, line, cap=1, ep='on', promote='QRBN'):
    s = make_solver(board, ep, promote, cap)
    return ''.join(s.solve_line(line))


def pos_of(solver, line):
    p = solver.parse_position(line)
    assert p is not None, line
    return p


def to_text(solver, pos):
    """Canonical text of a solver position: sorted piece tokens, side, e.p."""
    g = solver.g
    stm, wk, bk, offs, wp, bp, ep = pos
    toks = ['K' + g.sqname(wk), 'k' + g.sqname(bk)]
    for c, t, s in offs:
        ch = 'QRBN'[t]
        toks.append((ch if c == WHITE else ch.lower()) + g.sqname(s))
    for s in range(g.N):
        if wp >> s & 1:
            toks.append('P' + g.sqname(s))
        if bp >> s & 1:
            toks.append('p' + g.sqname(s))
    return ' '.join(sorted(toks)) + ' ' + 'wb'[stm] + ' ' + (g.sqname(ep) if ep >= 0 else '-')


def successor_texts(solver, pos):
    nq, quiet, exits = solver.moves(pos, full=True)
    assert nq == len(quiet)
    out = [to_text(solver, q) for q in quiet]
    out += ['CAPPED' if tag == CAPPED else to_text(solver, s) for tag, s in exits]
    return sorted(out)


# ---------------------------------------------------------------------------- naive model

FILES = 'abcdefgh'


class Naive:
    """A second, straightforward implementation of the SPEC move rules.

    A position is (frozenset of (char, (file, rank))), 'w' or 'b', ep square (f, r) or None).
    Files and ranks are 0-based here.
    """

    def __init__(self, W, H, cyl, ep_on=True, promote='QRBN', cap=1):
        self.W, self.H, self.cyl = W, H, cyl
        self.ep_on, self.promote, self.cap = ep_on, promote, cap

    def norm(self, f, r):
        if r < 0 or r >= self.H:
            return None
        if self.cyl:
            return (f % self.W, r)
        if f < 0 or f >= self.W:
            return None
        return (f, r)

    @staticmethod
    def white(ch):
        return ch.isupper()

    def piece_targets(self, board, sq, ch):
        """Squares the piece on sq attacks / may move to (ignoring own pieces and pawn pushes)."""
        f, r = sq
        kind = ch.upper()
        out = []
        if kind == 'K':
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if df or dr:
                        t = self.norm(f + df, r + dr)
                        if t is not None and t != sq and t not in out:
                            out.append(t)
        elif kind == 'N':
            for df, dr in ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)):
                t = self.norm(f + df, r + dr)
                if t is not None and t != sq and t not in out:
                    out.append(t)
        elif kind == 'P':
            dr = 1 if self.white(ch) else -1
            for df in (-1, 1):
                t = self.norm(f + df, r + dr)
                if t is not None and t not in out:
                    out.append(t)
        else:
            dirs = []
            if kind in 'RQ':
                dirs += [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if kind in 'BQ':
                dirs += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for df, dr in dirs:
                cf, cr = f, r
                while True:
                    cf, cr = cf + df, cr + dr
                    t = self.norm(cf, cr)
                    if t is None or t == sq:
                        break
                    if t not in out:
                        out.append(t)
                    if t in board:
                        break
                    cf, cr = t
        return out

    def attacked(self, board, sq, by_white):
        for s, ch in board.items():
            if self.white(ch) == by_white and sq in self.piece_targets(board, s, ch):
                return True
        return False

    def king_sq(self, board, white):
        for s, ch in board.items():
            if ch == ('K' if white else 'k'):
                return s
        raise AssertionError('no king')

    def legal_after(self, board, white):
        return not self.attacked(board, self.king_sq(board, white), not white)

    def n_officers(self, board):
        return sum(1 for ch in board.values() if ch.upper() in 'QRBN')

    def moves(self, pos):
        """List of successors; a capped promotion appears as the string 'CAPPED'."""
        items, stm, ep = pos
        board = dict(items)
        white = stm == 'w'
        nstm = 'b' if white else 'w'
        out = []
        for sq, ch in list(board.items()):
            if self.white(ch) != white:
                continue
            kind = ch.upper()
            if kind != 'P':
                for t in self.piece_targets(board, sq, ch):
                    victim = board.get(t)
                    if victim is not None and (self.white(victim) == white or victim.upper() == 'K'):
                        continue
                    nb = dict(board)
                    del nb[sq]
                    nb[t] = ch
                    if self.legal_after(nb, white):
                        out.append((frozenset(nb.items()), nstm, None))
                continue
            f, r = sq
            dr = 1 if white else -1
            last = self.H - 1 if white else 0
            start = 1 if white else self.H - 2
            cand = []   # (dest, captured square or None, ep target)
            one = (f, r + dr)
            if one not in board:
                cand.append((one, None, None))
                two = (f, r + 2 * dr)
                if r == start and two not in board:
                    cand.append((two, None, one if self.ep_on and two[1] != last else None))
            for t in self.piece_targets(board, sq, ch):
                victim = board.get(t)
                if victim is not None and self.white(victim) != white and victim.upper() != 'K':
                    cand.append((t, t, None))
                if ep is not None and t == ep:
                    cand.append((t, (t[0], t[1] - dr), None))
            for t, cap_sq, nep in cand:
                nb = dict(board)
                del nb[sq]
                if cap_sq is not None:
                    del nb[cap_sq]
                if t[1] == last:
                    nb[t] = 'Q' if white else 'q'
                    if not self.legal_after(nb, white):
                        continue
                    for pc in self.promote:
                        nb2 = dict(nb)
                        nb2[t] = pc if white else pc.lower()
                        if self.n_officers(nb2) > self.cap:
                            out.append('CAPPED')
                        else:
                            out.append((frozenset(nb2.items()), nstm, None))
                else:
                    nb[t] = ch
                    if self.legal_after(nb, white):
                        out.append((frozenset(nb.items()), nstm, nep))
        return out

    def in_check(self, pos):
        items, stm, ep = pos
        board = dict(items)
        return not self.legal_after(board, stm == 'w')

    def parse(self, line):
        toks = line.split()
        board = {}
        for tok in toks[:-2]:
            board[(FILES.index(tok[1]), int(tok[2:]) - 1)] = tok[0]
        ep = None if toks[-1] == '-' else (FILES.index(toks[-1][0]), int(toks[-1][1:]) - 1)
        if not self.ep_on:
            ep = None           # with --ep off an input e.p. target is ignored
        return (frozenset(board.items()), toks[-2], ep)

    def text(self, pos):
        if pos == 'CAPPED':
            return 'CAPPED'
        items, stm, ep = pos
        board = dict(items)
        # e.p. targets nobody can use are dropped, as the solver does
        if ep is not None:
            dr = 1 if stm == 'w' else -1
            usable = any(board.get(self.norm(ep[0] + df, ep[1] - dr)) == ('P' if stm == 'w' else 'p')
                         for df in (-1, 1))
            if not usable:
                ep = None
        toks = sorted(ch + FILES[f] + str(r + 1) for (f, r), ch in items)
        return ' '.join(toks) + ' ' + stm + ' ' + ('-' if ep is None else FILES[ep[0]] + str(ep[1] + 1))


def brute_values(naive, starts):
    """Values (A, B) from White's point of view for each start, by explicit graph retrograde."""
    graph = {}
    stack = list(starts)
    while stack:
        p = stack.pop()
        if p in graph:
            continue
        succ = naive.moves(p)
        graph[p] = succ
        for q in succ:
            if q != 'CAPPED' and q not in graph:
                stack.append(q)
    preds = defaultdict(list)
    for p, succ in graph.items():
        for q in succ:
            if q != 'CAPPED':
                preds[q].append(p)
    results = []
    for bound in ('A', 'B'):
        winner = 'w' if bound == 'A' else 'b'
        val, cnt, queue = {}, {}, []
        for p, succ in graph.items():
            stm = p[1]
            if not succ:
                val[p] = LOSS if naive.in_check(p) else DRAW
                if val[p] == LOSS:
                    queue.append(p)
                continue
            n = 0
            win = False
            for q in succ:
                if q == 'CAPPED':
                    if stm == winner:
                        win = True
                else:
                    n += 1
            if win:
                val[p] = WIN
                queue.append(p)
            elif n == 0:
                val[p] = LOSS
                queue.append(p)
            else:
                cnt[p] = n
        while queue:
            q = queue.pop()
            for p in preds[q]:
                if p in val:
                    continue
                if val[q] == LOSS:
                    val[p] = WIN
                    queue.append(p)
                else:
                    cnt[p] -= 1
                    if cnt[p] == 0:
                        val[p] = LOSS
                        queue.append(p)
        results.append(val)
    out = []
    for s in starts:
        row = []
        for val in results:
            v = val.get(s, DRAW)
            if v == DRAW:
                row.append('D')
            elif (v == WIN) == (s[1] == 'w'):
                row.append('W')
            else:
                row.append('L')
        out.append(''.join(row))
    return out


def random_position(solver, rng, n_wp, n_bp, n_off, tries=1000):
    """A random legal position (as a text line) with the given material."""
    g = solver.g
    for _ in range(tries):
        squares = rng.sample(range(g.N), 2 + n_wp + n_bp + n_off)
        toks = ['K' + g.sqname(squares[0]), 'k' + g.sqname(squares[1])]
        rest = squares[2:]
        bad = False
        for i, s in enumerate(rest):
            if i < n_wp + n_bp and g.rank[s] in (0, g.H - 1):
                bad = True
            if i < n_wp:
                toks.append('P' + g.sqname(s))
            elif i < n_wp + n_bp:
                toks.append('p' + g.sqname(s))
            else:
                ch = rng.choice('QRBN')
                toks.append((ch if rng.random() < 0.5 else ch.lower()) + g.sqname(s))
        if bad:
            continue
        line = ' '.join(toks) + ' ' + rng.choice('wb') + ' -'
        if solver.parse_position(line) is not None:
            return line
    raise AssertionError('no legal random position found')


# ---------------------------------------------------------------------------- geometry / moves

def rook_dests(solver, line):
    _, quiet, exits = solver.moves(pos_of(solver, line))
    out = []
    for q in quiet + [x[1] for x in exits]:
        out += [t for t in to_text(solver, q).split() if t[0] == 'R' and t != 'Ra1']
    return sorted(out)


def test_rook_ray_wraps_and_stops_at_own_square():
    # 4-wide cylinder, rook a1, kings off rank 1 and file a.  The rank gives b1 c1 d1 once
    # each (the left and right rays meet), never a1 itself (no null move); the file a2 a3 a4.
    s = make_solver('cyl:4x4', cap=2)
    assert rook_dests(s, 'Kb3 kd3 Ra1 w -') == ['Ra2', 'Ra3', 'Ra4', 'Rb1', 'Rc1', 'Rd1']
    # an enemy bishop on c1 is reached from both sides: still one capture, and no d1->a1 pass
    assert rook_dests(s, 'Kb3 kd3 Ra1 bc1 w -') == ['Ra2', 'Ra3', 'Ra4', 'Rb1', 'Rc1', 'Rd1']
    # 2-wide cylinder: the left and right rays reach b1 only, one move
    s2 = make_solver('cyl:2x6')
    assert rook_dests(s2, 'Ka4 ka6 Ra1 w -') == ['Ra2', 'Ra3', 'Rb1']
    # flat board for contrast: no wrap
    s3 = make_solver('flat:4x4', cap=2)
    assert rook_dests(s3, 'Kb3 kd3 Ra1 bc1 w -') == ['Ra2', 'Ra3', 'Ra4', 'Rb1', 'Rc1']


def test_rook_attacks_across_the_seam():
    # Black king e1, rook a1, white king c1 blocks the direct rank path.  On the cylinder the
    # rook still attacks e1 across the seam, on the flat board it does not.
    assert solve('cyl:5x5', 'Kc1 ke1 Ra1 w -') == 'XX'   # side not to move in check
    assert make_solver('flat:5x5').parse_position('Kc1 ke1 Ra1 w -') is not None
    s = make_solver('cyl:5x5')
    assert s.in_check(pos_of(s, 'Kc1 ke1 Ra1 b -'))
    s = make_solver('flat:5x5')
    assert not s.in_check(pos_of(s, 'Kc1 ke1 Ra1 b -'))


def test_pawn_wrap_capture_moves():
    # SPEC example: on a width-5 cylinder a white pawn on e2 captures on a3 and on d3.
    line = 'Kc1 kc5 Pe2 pa3 pd3 w -'
    s = make_solver('cyl:5x5')
    succ = successor_texts(s, pos_of(s, line))
    pawn_moves = sorted(x for x in succ if 'Kc1' in x and 'Pe2' not in x)
    assert pawn_moves == [
        'Kc1 Pa3 kc5 pd3 b -',          # exa3 across the seam
        'Kc1 Pd3 kc5 pa3 b -',          # exd3
        'Kc1 Pe3 kc5 pa3 pd3 b -',      # e3
        'Kc1 Pe4 kc5 pa3 pd3 b -',      # e4 double step (no black pawn can take on e3)
    ]
    # on the flat board only exd3 is a capture
    s = make_solver('flat:5x5')
    succ = successor_texts(s, pos_of(s, line))
    assert not any('Pa3' in x for x in succ)
    assert any('Pd3' in x for x in succ)


def test_king_wrap_capture_value():
    # Black pawn e2 is about to promote.  On the cylinder the white king on a3 is adjacent
    # to e2 and captures it (bare kings: draw).  On the flat board it cannot reach it, Black
    # queens next move and K vs KQ is lost.
    assert solve('cyl:5x5', 'Ka3 kc5 pe2 w -') == 'DD'
    assert solve('flat:5x5', 'Ka3 kc5 pe2 w -') == 'LL'
    s = make_solver('cyl:5x5')
    succ = successor_texts(s, pos_of(s, 'Ka3 kc5 pe2 w -'))
    assert 'Ke2 kc5 b -' in succ


def test_kings_adjacent_across_seam_illegal():
    assert solve('cyl:5x5', 'Ka1 ke1 w -') == 'XX'
    assert solve('cyl:5x5', 'Ka3 ke4 b -') == 'XX'
    assert solve('flat:5x5', 'Ka1 ke1 w -') == 'DD'


def test_double_step_sets_ep_only_when_capturable():
    s = make_solver('flat:5x5')
    succ = successor_texts(s, pos_of(s, 'Ka1 ke5 Pb2 pc4 w -'))
    assert 'Ka1 Pb4 ke5 pc4 b b3' in succ          # c4 pawn can take e.p.
    succ = successor_texts(s, pos_of(s, 'Ka1 ke5 Pb2 pe4 w -'))
    assert 'Ka1 Pb4 ke5 pe4 b -' in succ           # nobody can take e.p.
    s = make_solver('flat:5x5', ep='off')
    succ = successor_texts(s, pos_of(s, 'Ka1 ke5 Pb2 pc4 w -'))
    assert 'Ka1 Pb4 ke5 pc4 b -' in succ


def test_double_step_on_four_ranks_promotes():
    # H = 4: the double step from rank 2 lands on rank 4, the last rank, and promotes.
    s = make_solver('flat:4x4')
    succ = successor_texts(s, pos_of(s, 'Kd1 kd4 Pa2 w -'))
    for pc in 'QRBN':
        assert ' '.join(sorted(['Kd1', pc + 'a4', 'kd4'])) + ' b -' in succ
    assert ' '.join(sorted(['Kd1', 'Pa3', 'kd4'])) + ' b -' in succ
    assert len(succ) == 8          # Kc1 Kc2 Kd2, a3, a4=Q/R/B/N


def test_en_passant_only_move():
    # 3x5 flat (files a-c).  White has just played b2-b4.  Black king a5 is in check from the
    # b4 pawn: a4 (Ka3, Nc3), b5 (Nc3) and b4 (defended by Ka3) are covered, the c4 pawn is
    # blocked by Nc3, so the only legal move is c4xb3 e.p.  Afterwards it is K+N vs K+P with
    # White to move.  Kxb3 draws at once (K+N cannot mate a bare king).  White has no other
    # move that keeps the a4/b4/b5 box (only Nc3 covers both a4 and b5, and every king move
    # but Kxb3 uncovers a4 or b4), so Black is never forced into the (capped) promotion and the
    # value is a draw under both bounds; the brute-force solver agrees.  Without e.p. the
    # position is checkmate.
    board = 'flat:3x5'
    line_ep = 'Ka3 ka5 Nc3 Pb4 pc4 b b3'
    line_no = 'Ka3 ka5 Nc3 Pb4 pc4 b -'
    s = make_solver(board)
    assert successor_texts(s, pos_of(s, line_ep)) == ['Ka3 Nc3 ka5 pb3 w -']
    assert successor_texts(s, pos_of(s, line_no)) == []
    assert s.in_check(pos_of(s, line_no))
    assert ''.join(s.solve_line(line_ep)) == 'DD'
    assert ''.join(s.solve_line(line_no)) == 'WW'                 # e.p. only immediately
    n = naive_for(board)
    assert brute_values(n, [n.parse(line_ep), n.parse(line_no)]) == ['DD', 'WW']
    s = make_solver(board, ep='off')                               # no e.p. at all
    assert successor_texts(s, pos_of(s, line_ep)) == []
    assert ''.join(s.solve_line(line_ep)) == 'WW'
    assert ''.join(s.solve_line(line_no)) == 'WW'


def test_en_passant_across_seam():
    # 5x5 cylinder: White pawn a2 double-steps to a4; the black pawn on e4 is beside it across
    # the seam and may capture e4xa3 e.p.
    s = make_solver('cyl:5x5')
    succ = successor_texts(s, pos_of(s, 'Kc1 kc5 Pa2 pe4 w -'))
    assert 'Kc1 Pa4 kc5 pe4 b a3' in succ
    p = pos_of(s, 'Kc1 kc5 Pa4 pe4 b a3')
    assert 'Kc1 kc5 pa3 w -' in successor_texts(s, p)
    s = make_solver('flat:5x5')
    succ = successor_texts(s, pos_of(s, 'Kc1 kc5 Pa2 pe4 w -'))
    assert 'Kc1 Pa4 kc5 pe4 b -' in succ
    assert s.parse_position('Kc1 kc5 Pa4 pe4 b a3') is not None
    assert 'Kc1 kc5 pa3 w -' not in successor_texts(s, s.parse_position('Kc1 kc5 Pa4 pe4 b a3'))


def test_bad_ep_target_is_illegal():
    assert solve('flat:5x5', 'Ka1 ke5 Pb4 pc4 b c3') == 'XX'   # no white pawn on c4... wrong
    assert solve('flat:5x5', 'Ka1 ke5 Pb4 pc4 w b3') == 'XX'   # wrong side to move
    assert solve('flat:5x5', 'Ka1 ke5 Pb4 Nb2 pc4 b b3') == 'XX'   # origin square occupied
    assert make_solver('flat:5x5').parse_position('Ka1 ke5 Pb4 pc4 b b3') is not None


def test_promotion_moves():
    s = make_solver('flat:4x5')
    p = pos_of(s, 'Ka1 kd1 Pc4 w -')
    succ = successor_texts(s, p)
    promo = sorted(x for x in succ if 'Pc4' not in x and 'Ka1' in x)
    assert promo == sorted(' '.join(sorted(['Ka1', pc + 'c5', 'kd1'])) + ' b -' for pc in 'QRBN')
    s = make_solver('flat:4x5', promote='Q')
    succ = successor_texts(s, pos_of(s, 'Ka1 kd1 Pc4 w -'))
    assert sum('Pc4' not in x and 'Ka1' in x for x in succ) == 1
    # cap 0: every promotion is capped, one capped move per allowed piece
    s = make_solver('flat:4x5', cap=0)
    assert successor_texts(s, pos_of(s, 'Ka1 kd1 Pc4 w -')).count('CAPPED') == 4
    # promotion capturing an officer when already at the cap is not capped (count stays C)
    s = make_solver('flat:4x5', cap=1)
    succ = successor_texts(s, pos_of(s, 'Ka1 kd1 Pc4 rb5 w -'))
    assert 'CAPPED' in succ                                          # c5 (count would be 2)
    assert ' '.join(sorted(['Ka1', 'Nb5', 'kd1'])) + ' b -' in succ   # cxb5=N (count 1)


def test_underpromotion_avoids_stalemate():
    # 4x4 flat, White to move: Ka1 Pc3 against ka3.
    #   White king: a2 and b2 touch the black king, so Kb1 is its only move.
    #   c4=Q stalemates: a2 b2 (Ka1), b3 (Qc4 diagonal), a4 b4 (Qc4 rank), and a3 is not
    #        attacked.  So with --promote Q the value is a draw.
    #   c4=R leaves b3 free (no stalemate) and K+R vs K wins: the only winning move.
    #   c4=B and c4=N are bare-minor draws.
    board, line = 'flat:4x4', 'Ka1 ka3 Pc3 w -'
    s = make_solver(board)
    p = pos_of(s, line)
    stalemated = pos_of(s, 'Ka1 Qc4 ka3 b -')
    assert s.moves(stalemated)[0] == 0 and not s.moves(stalemated)[2]
    assert not s.in_check(stalemated)
    assert s.moves(p)[0] == 1
    expected = {'QRBN': 'WW', 'Q': 'DD', 'R': 'WW', 'B': 'DD', 'N': 'DD', 'QBN': 'DD'}
    for promo, want in expected.items():
        assert solve(board, line, promote=promo) == want, promo
        n = naive_for(board, promote=promo)
        assert brute_values(n, [n.parse(line)]) == [want], promo


def test_checkmate_and_stalemate_flat_and_cyl():
    # mate: rook a4 checks a1 along the file, Kc2 covers b1 b2 (and on the 4-wide cylinder
    # also d1 d2, the squares beside a1 across the seam)
    for board in ('flat:4x4', 'cyl:4x4'):
        s = make_solver(board)
        p = pos_of(s, 'Kc2 ka1 Ra4 b -')
        assert s.moves(p)[0] == 0 and not s.moves(p)[2] and s.in_check(p)
        assert solve(board, 'Kc2 ka1 Ra4 b -') == 'WW'
    # 5x5: flat mate, but on the cylinder e1 and e2 are flight squares
    s = make_solver('cyl:5x5')
    p = pos_of(s, 'Kc2 ka1 Ra5 b -')
    assert sorted(to_text(s, q).split()[2] for q in s.moves(p)[1]) == ['ke1', 'ke2']
    assert solve('flat:5x5', 'Kc2 ka1 Ra5 b -') == 'WW'
    # stalemate on the flat board; on the cylinder Black escapes to e1 only and loses
    s = make_solver('flat:5x5')
    p = pos_of(s, 'Ke5 ka1 Qc2 b -')
    assert s.moves(p)[0] == 0 and not s.moves(p)[2] and not s.in_check(p)
    assert solve('flat:5x5', 'Ke5 ka1 Qc2 b -') == 'DD'
    s = make_solver('cyl:5x5')
    p = pos_of(s, 'Ke5 ka1 Qc2 b -')
    assert [to_text(s, q) for q in s.moves(p)[1]] == ['Ke5 Qc2 ke1 w -']
    assert solve('cyl:5x5', 'Ke5 ka1 Qc2 b -') == 'WW'
    # bare kings
    assert solve('cyl:4x4', 'Ka1 kc3 w -') == 'DD'


def test_cap_bounds_disagree():
    # 4x4 flat.  White: Ka1 Pd3.  Black: ka3 pc2.  White's king has no move (a2 b2 by the
    # black king, b1 by the c2 pawn), so White must promote on d4.
    line = 'Ka1 ka3 Pd3 pc2 w -'
    # cap 0: the promotion is capped: bound A counts it as a White win, bound B as a loss.
    assert solve('flat:4x4', line, cap=0) == 'WL'
    # cap 1: White's promotion is allowed, but after it Black's c2-c1 promotion (the second
    # one) is capped and always legal; under bound B it is an immediate Black win, so B = L.
    # Under bound A Black must never promote, and White wins.
    assert solve('flat:4x4', line, cap=1) == 'WL'
    # cap 2: both promotions are allowed and the bounds agree (exact value).
    v = solve('flat:4x4', line, cap=2)
    assert v[0] == v[1]
    for cap in (0, 1):
        n = naive_for('flat:4x4', cap=cap)
        assert brute_values(n, [n.parse(line)]) == ['WL']


def test_illegal_positions():
    b = 'flat:5x5'
    assert solve(b, 'Ka1 ka1 w -') == 'XX'            # two pieces on one square
    assert solve(b, 'Ka1 kc3 Pa1 w -') == 'XX'
    assert solve(b, 'Ka1 kb2 w -') == 'XX'            # kings adjacent
    assert solve(b, 'Ka1 kc3 Pb1 w -') == 'XX'        # pawn on its first rank
    assert solve(b, 'Ka1 kc3 Pb5 w -') == 'XX'        # pawn on its last rank
    assert solve(b, 'Ka1 kc3 pb5 w -') == 'XX'
    assert solve(b, 'Ka1 kc3 pb1 w -') == 'XX'
    assert solve(b, 'Ka1 kc3 Pb2 w -') == 'XX'        # side not to move (Black) in check
    assert solve(b, 'Ka1 kc3 Rc1 w -') == 'XX'
    assert make_solver(b).parse_position('Ka1 kc3 Rc1 b -') is not None   # Black to move: ok
    assert solve(b, 'Ka1 Qc3 Rc1 w -') == 'XX'        # missing king
    assert solve(b, 'Ka1 kc5 Qe4 re2 w -', cap=1) == 'XX'   # more officers than the cap
    assert make_solver(b, cap=2).parse_position('Ka1 kc5 Qe4 re2 w -') is not None
    assert solve(b, 'Ka1 kc3 Pf2 w -') == 'XX'        # off the board
    assert solve(b, 'Ka1 kc3 Xb2 w -') == 'XX'


def test_sanity_positions_against_brute_force():
    for board in ('flat:4x4', 'cyl:4x4'):
        n = naive_for(board)
        lines = ['Ka1 kc3 Pb2 b -']
        assert [solve(board, l) for l in lines] == brute_values(n, [n.parse(l) for l in lines])
        assert solve(board, 'Ka1 kc3 Pb2 w -') == 'XX'


# ---------------------------------------------------------------------------- cross-checks

def naive_for(board, ep='on', promote='QRBN', cap=1):
    kind, dims = board.split(':')
    W, H = map(int, dims.split('x'))
    return Naive(W, H, kind == 'cyl', ep == 'on', promote, cap)


@pytest.mark.parametrize('board', ['flat:4x4', 'cyl:4x4', 'cyl:2x5', 'cyl:3x5', 'flat:5x5',
                                   'cyl:5x5', 'cyl:4x6', 'flat:3x6', 'cyl:6x5'])
def test_move_generator_matches_naive(board):
    rng = random.Random(zlib.crc32(board.encode()))
    for cap in (1, 3):
        s = make_solver(board, cap=cap)
        n = naive_for(board, cap=cap)
        for _ in range(150):
            material = (rng.randint(0, 2), rng.randint(0, 2), rng.randint(0, cap))
            try:
                line = random_position(s, rng, *material)
            except AssertionError:
                continue
            ours = successor_texts(s, pos_of(s, line))
            theirs = sorted(n.text(q) for q in n.moves(n.parse(line)))
            assert ours == theirs, line


@pytest.mark.parametrize('board', ['cyl:5x5', 'flat:4x5', 'cyl:2x5', 'cyl:3x6'])
def test_ep_moves_match_naive(board):
    # positions just after a double step, with e.p. capture available
    rng = random.Random(7)
    s = make_solver(board, cap=2)
    n = naive_for(board, cap=2)
    found = 0
    for _ in range(3000):
        line = random_position(s, rng, rng.randint(1, 2), rng.randint(1, 2), rng.randint(0, 1))
        for q in s.moves(pos_of(s, line))[2]:
            if q[0] == EXIT and q[1][6] >= 0:
                found += 1
                t = to_text(s, q[1])
                p2 = pos_of(s, t)
                assert successor_texts(s, p2) == sorted(n.text(x) for x in n.moves(n.parse(t))), t
    assert found > 5


@pytest.mark.parametrize('board', ['cyl:4x4', 'flat:4x5', 'cyl:5x5', 'cyl:2x5', 'cyl:3x6'])
def test_unmoves_invert_quiet_moves(board):
    rng = random.Random(3)
    s = make_solver(board, cap=2)
    for _ in range(300):
        line = random_position(s, rng, rng.randint(0, 1), rng.randint(0, 1), rng.randint(0, 2))
        p = pos_of(s, line)
        for q in s.moves(p)[1]:
            assert p in s.unmoves(q), (line, to_text(s, q))
        for pp in s.unmoves(p):
            assert s.parse_position(to_text(s, pp)) is not None
            assert p in s.moves(pp)[1], (line, to_text(s, pp))


BRUTE_CASES = [
    # board, ep, promote, cap, material (white pawns, black pawns, officers), count
    ('flat:4x4', 'on', 'QRBN', 1, (1, 0, 0), 6),
    ('cyl:4x4', 'on', 'QRBN', 1, (1, 0, 0), 6),
    ('flat:4x4', 'on', 'QRBN', 1, (1, 1, 0), 4),
    ('cyl:4x4', 'on', 'QRBN', 1, (1, 1, 0), 4),
    ('cyl:4x4', 'on', 'QRBN', 0, (1, 1, 0), 4),
    ('cyl:3x5', 'on', 'RN', 2, (1, 1, 0), 2),
    ('cyl:4x4', 'on', 'QRBN', 1, (0, 0, 1), 4),
    ('flat:3x5', 'on', 'QRBN', 1, (1, 1, 0), 4),
    ('cyl:3x5', 'on', 'QRBN', 1, (1, 1, 0), 4),
    ('cyl:3x5', 'off', 'QRBN', 1, (1, 1, 0), 4),
    ('cyl:2x6', 'on', 'QRBN', 1, (1, 1, 0), 4),
    ('cyl:4x5', 'on', 'Q', 1, (1, 1, 0), 2),
    ('flat:4x5', 'off', 'B', 1, (1, 1, 0), 2),
    ('cyl:2x6', 'on', 'QRBN', 2, (1, 1, 0), 3),
]


@pytest.mark.parametrize('board,ep,promote,cap,material,count', BRUTE_CASES)
def test_layered_solver_matches_brute_force(board, ep, promote, cap, material, count):
    rng = random.Random(zlib.crc32(repr((board, ep, promote, cap, material)).encode()))
    s = make_solver(board, ep, promote, cap)
    n = naive_for(board, ep, promote, cap)
    lines = [random_position(s, rng, *material) for _ in range(count)]
    got = [''.join(s.solve_line(l)) for l in lines]
    want = brute_values(n, [n.parse(l) for l in lines])
    assert got == want, list(zip(lines, got, want))


def test_ep_input_matches_brute_force():
    board = 'cyl:3x5'
    s = make_solver(board)
    n = naive_for(board)
    # e4xa3 / c4xa3 e.p. across the seam is available in the first two, b3 in the third
    lines = ['Kb1 kb5 Pa4 pc4 b a3', 'Kc2 kc5 Pa4 pb4 b a3', 'Ka1 ka5 Pb4 pc4 b b3',
             'Kc1 kc5 Pa2 pb4 w -']
    got = [''.join(s.solve_line(l)) for l in lines]
    assert got == brute_values(n, [n.parse(l) for l in lines])


# ---------------------------------------------------------------------------- command line

def test_command_line(tmp_path):
    inp = tmp_path / 'in.txt'
    inp.write_text('# a comment\nKa1 kc3 Pb2 w -\nKa1 kc3 Pb2 b -\n\nKc2 ka1 Ra4 b -\n')
    res = subprocess.run([sys.executable, '-m', 'kings.ref.solve', '--board', 'flat:4x4',
                          '--ep', 'on', '--promote', 'QRBN', '--cap', '1'],
                         stdin=open(inp), capture_output=True, text=True, cwd=ROOT, check=True)
    lines = res.stdout.split('\n')
    assert lines[0] == '# a comment'
    assert lines[1] == 'Ka1 kc3 Pb2 w - | X X'
    assert lines[2].startswith('Ka1 kc3 Pb2 b - | ')
    assert lines[3] == ''
    assert lines[4] == 'Kc2 ka1 Ra4 b - | W W'


# ---------------------------------------------------------------------------- symmetry / bounds

def transform_line(line, W, H, fmap=None, flip_colours=False):
    """Apply a file map (and optionally the colour flip: swap colours, mirror ranks, swap side)."""
    toks = line.split()
    out = []
    for tok in toks[:-2]:
        ch, f, r = tok[0], FILES.index(tok[1]), int(tok[2:])
        if fmap:
            f = fmap(f)
        if flip_colours:
            ch = ch.swapcase()
            r = H + 1 - r
        out.append(ch + FILES[f] + str(r))
    stm, ep = toks[-2], toks[-1]
    if ep != '-':
        f, r = FILES.index(ep[0]), int(ep[1:])
        if fmap:
            f = fmap(f)
        if flip_colours:
            r = H + 1 - r
        ep = FILES[f] + str(r)
    if flip_colours:
        stm = 'b' if stm == 'w' else 'w'
    return ' '.join(out) + ' ' + stm + ' ' + ep


NEG = {'W': 'L', 'L': 'W', 'D': 'D', 'X': 'X'}
ORDER = {'L': 0, 'D': 1, 'W': 2}


@pytest.mark.parametrize('board,cap', [('cyl:5x4', 1), ('flat:5x4', 1), ('cyl:4x5', 1),
                                       ('cyl:3x5', 2)])
def test_symmetries_and_bound_order(board, cap):
    kind, dims = board.split(':')
    W, H = map(int, dims.split('x'))
    rng = random.Random(11)
    s = make_solver(board, cap=cap)
    lines = [random_position(s, rng, rng.randint(0, 1), rng.randint(0, 1), rng.randint(0, cap))
             for _ in range(12 if cap == 1 else 5)]
    vals = [''.join(s.solve_line(l)) for l in lines]
    for l, v in zip(lines, vals):
        assert ORDER[v[0]] >= ORDER[v[1]], (l, v)          # A >= true value >= B
        # colour flip swaps the bounds and negates the value
        f = ''.join(s.solve_line(transform_line(l, W, H, flip_colours=True)))
        assert f == NEG[v[1]] + NEG[v[0]], (l, v, f)
        # mirror the files
        m = ''.join(s.solve_line(transform_line(l, W, H, fmap=lambda x: W - 1 - x)))
        assert m == v, (l, v, m)
        if kind == 'cyl':
            k = rng.randint(1, W - 1)
            t = ''.join(s.solve_line(transform_line(l, W, H, fmap=lambda x: (x + k) % W)))
            assert t == v, (l, v, t, k)


def test_large_cap_is_exact():
    # with room for every possible promotion no promotion is ever capped: A == B
    rng = random.Random(5)
    s = make_solver('cyl:3x5', cap=2)
    for _ in range(6):
        l = random_position(s, rng, *rng.choice([(1, 0, 1), (0, 1, 1), (1, 1, 0)]))
        v = ''.join(s.solve_line(l))
        assert v[0] == v[1], (l, v)


def test_cap_bounds_bracket_exact_value():
    # one pawn each and no officers: at cap 2 nothing is ever capped, so cap 2 is exact and the
    # cap-1 bounds must bracket it
    rng = random.Random(9)
    s1 = make_solver('cyl:3x5', cap=1)
    s2 = make_solver('cyl:3x5', cap=2)
    for _ in range(8):
        l = random_position(s1, rng, 1, 1, 0)
        a, b = s1.solve_line(l)
        e, e2 = s2.solve_line(l)
        assert e == e2, l
        assert ORDER[a] >= ORDER[e] >= ORDER[b], (l, a, b, e)
