"""Patched copy of kings/ref/solve.py for research/mobius (adds the mob:WxH Mobius board).

The only changes are Geometry.__init__ (takes the board kind), the step() rule for kind mob, and
parse_board. Everything else is the reference solver unchanged. Written for the T35 cross-check.
"""
"""Independent reference solver for kings/SPEC.md (pure Python 3, stdlib only).

Usage (from the project root):
    python3 -m kings.ref.solve --board cyl:5x5 --ep on --promote QRBN --cap 1 < in.txt > out.txt

Design
------
A *position* is the tuple (stm, wk, bk, offs, wp, bp, ep):
    stm   side to move (0 = White, 1 = Black)
    wk,bk king squares; a square is rank_index * W + file_index
    offs  officers as a sorted tuple of (colour, type, square), type 0..3 = Q R B N
    wp,bp pawn bitmasks
    ep    en passant target square, or -1

Pawn moves, captures and promotions are irreversible, so positions are grouped into *layers*
keyed by (wp, bp, sorted officer (colour, type) list).  Every move that leaves a layer lands in a
different layer that can never lead back, so layers are solved on demand, children first
(recursively, memoised for the whole run).  Inside a layer only king and officer non-captures
("quiet" moves) occur.  Each layer is solved by counting retrograde analysis over ALL legal
placements of its kings and officers:

  1. For every legal state, generate its legal moves.  Quiet moves are only counted.  Every other
     move (an "exit") is valued at once: a capped promotion is a terminal (White win under bound
     A, Black win under bound B), a double step that allows an e.p. capture leads to a transient
     position valued directly from its own successors, anything else is looked up in an
     already-solved layer.
  2. Seed: no legal move -> lost if in check, else drawn; an exit to a lost position -> won;
     no quiet move -> drawn if some exit draws, else lost.  Otherwise the counter is the number of
     quiet moves, plus one that never decrements if some exit draws (so it can never be lost).
  3. Propagate through quiet un-moves (quiet moves are reversible, so the predecessors of Q are
     the quiet moves of the side that just moved, filtered by legality of the predecessor).
  4. Everything left undetermined is drawn (least fixed point).

Both bounds are solved in the same pass; they differ only in the value of capped promotions.
A double step records an e.p. target only when an enemy pawn attacks the skipped square;
otherwise the position has exactly the moves of the plain position and is stored as one.
Use --verbose to print per-layer statistics (states, cumulative CPU seconds) on stderr.
Blank lines in the input are copied like comments.

Interpretation choices for points SPEC.md leaves open (also listed in test_ref.py):
  * A promotion is capped iff the position after it would hold more than C officers (so a
    promotion that captures an officer is not capped when the count stays at C).
  * On H = 4 a double step reaches the last rank and promotes (no e.p. target is set).
  * An input e.p. target that is inconsistent with the position (wrong rank, no enemy pawn just
    beyond it, skipped or origin square occupied) makes the input illegal (X).  With --ep off any
    e.p. target in the input is ignored.
  * Input with more than C officers, a missing or extra king, an off-board square or an
    unparseable token is reported as X.
"""

import argparse
import sys
import time
from array import array
from itertools import permutations

WHITE, BLACK = 0, 1
QUEEN, ROOK, BISHOP, KNIGHT = 0, 1, 2, 3
PIECE_CHARS = 'QRBN'

UNK, WIN, LOSS, DRAW, ILLEGAL = 0, 1, 2, 3, 4
QUIET, EXIT, CAPPED = 0, 1, 2

# value of a move for the mover, given the successor's value from the successor's mover's side
MOVER_OUTCOME = {WIN: LOSS, LOSS: WIN, DRAW: DRAW}
PREF = {LOSS: 0, DRAW: 1, WIN: 2}

ORTH = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIAG = ((1, 1), (1, -1), (-1, 1), (-1, -1))
KNIGHT_D = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))


def _mask(squares):
    m = 0
    for s in squares:
        m |= 1 << s
    return m


class Geometry:
    """Board geometry and precomputed move tables."""

    def __init__(self, W, H, kind):
        # kind: 'flat', 'cyl' (straight seam) or 'mob' (seam with rank flip r -> H-1-r), RULES.md 1.1
        self.W, self.H, self.cyl, self.kind = W, H, kind == 'cyl', kind
        N = self.N = W * H

        def step(s, df, dr):
            f, r = s % W + df, s // W + dr
            if not 0 <= r < H:
                return None
            if kind == 'cyl':
                f %= W
            elif kind == 'mob':
                if not 0 <= f < W:
                    f %= W
                    r = H - 1 - r
            elif not 0 <= f < W:
                return None
            return r * W + f

        def targets(s, deltas):
            out = []
            for df, dr in deltas:
                t = step(s, df, dr)
                if t is not None and t != s and t not in out:
                    out.append(t)
            return tuple(out)

        def rays(s, dirs):
            out = []
            for df, dr in dirs:
                ray = []
                t = s
                while True:
                    t = step(t, df, dr)
                    if t is None or t == s:      # board edge, or wrapped back to the start
                        break
                    ray.append(t)
                if ray:
                    out.append(tuple(ray))
            return tuple(out)

        self.step = step
        self.king = [targets(s, ORTH + DIAG) for s in range(N)]
        self.knight = [targets(s, KNIGHT_D) for s in range(N)]
        self.king_mask = [_mask(t) for t in self.king]
        self.knight_mask = [_mask(t) for t in self.knight]
        rook_rays = [rays(s, ORTH) for s in range(N)]
        bishop_rays = [rays(s, DIAG) for s in range(N)]
        self.rays = {ROOK: rook_rays, BISHOP: bishop_rays,
                     QUEEN: [a + b for a, b in zip(rook_rays, bishop_rays)]}
        # the same rays as tuples of single-bit masks
        self.bit_rays = {ty: [tuple(tuple(1 << t for t in ray) for ray in rs) for rs in r]
                         for ty, r in self.rays.items()}
        # paths[type][s*N+t]: tuple of masks of the squares strictly between s and t, one per
        # distinct ray path by which a slider of that type on s reaches t.
        self.paths = {}
        for ty in (QUEEN, ROOK, BISHOP):
            table = [()] * (N * N)
            for s in range(N):
                acc = {}
                for ray in self.rays[ty][s]:
                    between = 0
                    for t in ray:
                        acc.setdefault(t, set()).add(between)
                        between |= 1 << t
                for t, ms in acc.items():
                    table[s * N + t] = tuple(sorted(ms))
            self.paths[ty] = table
        # pawn capture targets per colour and square, and the reverse masks
        self.pawn_cap = [[targets(s, ((1, dr), (-1, dr))) for s in range(N)]
                         for dr in (1, -1)]
        self.pawn_cap_mask = [[_mask(t) for t in self.pawn_cap[c]] for c in (WHITE, BLACK)]
        self.pawn_from = [[0] * N, [0] * N]
        for c in (WHITE, BLACK):
            for s in range(N):
                for t in self.pawn_cap[c][s]:
                    self.pawn_from[c][t] |= 1 << s
        self.rank = [s // W for s in range(N)]

    def sqname(self, s):
        return 'abcdefgh'[s % self.W] + str(s // self.W + 1)

    def parse_square(self, text):
        if len(text) < 2 or not text[1:].isdigit():
            return None
        f = ord(text[0]) - ord('a')
        r = int(text[1:]) - 1
        if not (0 <= f < self.W and 0 <= r < self.H):
            return None
        return r * self.W + f


class Solver:
    def __init__(self, geom, ep_on=True, promos=(QUEEN, ROOK, BISHOP, KNIGHT), cap=1,
                 verbose=False):
        self.g = geom
        self.ep_on = ep_on
        self.promos = tuple(promos)
        self.cap = cap
        self.verbose = verbose
        self.layers = {}       # layer key -> (values bound A, values bound B), stm's view
        self.ep_cache = {}     # e.p. transient position -> (A, B), stm's view
        self.states_solved = 0

    # ------------------------------------------------------------------ basic rules

    def attacked(self, sq, by, wk, bk, offs, wp, bp, occ):
        """Is square sq attacked by side `by`, with total occupancy occ?"""
        g = self.g
        if by == WHITE:
            if g.king_mask[wk] >> sq & 1:
                return True
            if wp & g.pawn_from[WHITE][sq]:
                return True
        else:
            if g.king_mask[bk] >> sq & 1:
                return True
            if bp & g.pawn_from[BLACK][sq]:
                return True
        N = g.N
        for c, ty, s in offs:
            if c != by:
                continue
            if ty == KNIGHT:
                if g.knight_mask[s] >> sq & 1:
                    return True
            else:
                for m in g.paths[ty][s * N + sq]:
                    if not m & occ:
                        return True
        return False

    @staticmethod
    def occupancy(pos):
        stm, wk, bk, offs, wp, bp, ep = pos
        occ = wp | bp | (1 << wk) | (1 << bk)
        for _, _, s in offs:
            occ |= 1 << s
        return occ

    def in_check(self, pos, side=None):
        stm, wk, bk, offs, wp, bp, ep = pos
        if side is None:
            side = stm
        k = wk if side == WHITE else bk
        return self.attacked(k, 1 - side, wk, bk, offs, wp, bp, self.occupancy(pos))

    @staticmethod
    def _remove_at(offs, wp, bp, t):
        """Remove the (non-king) piece standing on t."""
        b = 1 << t
        if wp & b:
            return offs, wp & ~b, bp
        if bp & b:
            return offs, wp, bp & ~b
        return tuple(o for o in offs if o[2] != t), wp, bp

    def moves(self, pos, full=True):
        """Legal moves of the side to move.

        Returns (n_quiet, quiet, exits):
          n_quiet  number of legal quiet moves (king / officer non-captures)
          quiet    list of their successor positions (None unless full)
          exits    list of (tag, successor) for all other legal moves; tag EXIT or CAPPED
                   (a capped promotion, successor None).  Each promotion piece is its own move.
        """
        g = self.g
        W, H, N = g.W, g.H, g.N
        stm, wk, bk, offs, wp, bp, ep = pos
        wocc = wp | (1 << wk)
        bocc = bp | (1 << bk)
        for c, _, s in offs:
            if c:
                bocc |= 1 << s
            else:
                wocc |= 1 << s
        occ = wocc | bocc
        nstm = 1 - stm
        if stm == WHITE:
            own, opp, myk, oppk, mypawns, opppawns = wocc, bocc, wk, bk, wp, bp
        else:
            own, opp, myk, oppk, mypawns, opppawns = bocc, wocc, bk, wk, bp, wp
        allowed = ~own & ~(1 << oppk)     # destination squares (never the enemy king)
        attacked = self.attacked
        kb = 1 << myk
        occ_nok = occ & ~kb

        # Squares attacked by the opponent with our king lifted off the board (exactly the
        # squares our king may not step to), and our pieces that are the sole blocker on some
        # path from an enemy slider to our king (moves of those are checked one by one).
        att = g.king_mask[oppk]
        pcm = g.pawn_cap_mask[nstm]
        pm = opppawns
        while pm:
            b = pm & -pm
            pm ^= b
            att |= pcm[b.bit_length() - 1]
        pinned = 0
        bit_rays = g.bit_rays
        paths = g.paths
        for c, ty, s in offs:
            if c == stm:
                continue
            if ty == KNIGHT:
                att |= g.knight_mask[s]
            else:
                for ray in bit_rays[ty][s]:
                    for b in ray:
                        att |= b
                        if occ_nok & b:
                            break
                for m in paths[ty][s * N + myk]:
                    blk = m & occ
                    if blk and not blk & (blk - 1):
                        pinned |= blk
        in_check = att & kb
        pinned &= own

        n_quiet = 0
        quiet = [] if full else None
        exits = []

        # king
        for t in g.king[myk]:
            b = 1 << t
            if not allowed & b or att & b:
                continue
            nwk, nbk = (t, bk) if stm == WHITE else (wk, t)
            if opp & b:
                noffs, nwp, nbp = self._remove_at(offs, wp, bp, t)
                exits.append((EXIT, (nstm, nwk, nbk, noffs, nwp, nbp, -1)))
            else:
                n_quiet += 1
                if full:
                    quiet.append((nstm, nwk, nbk, offs, wp, bp, -1))

        # officers
        for i, (c, ty, s) in enumerate(offs):
            if c != stm:
                continue
            sb = 1 << s
            check_each = in_check or pinned & sb
            if ty == KNIGHT:
                tm = g.knight_mask[s] & allowed
            else:
                tm = 0
                for ray in bit_rays[ty][s]:
                    for b in ray:
                        if occ & b:
                            tm |= b & allowed
                            break
                        tm |= b
            rest = offs[:i] + offs[i + 1:]
            while tm:
                b = tm & -tm
                tm ^= b
                t = b.bit_length() - 1
                if opp & b:
                    r2, nwp, nbp = self._remove_at(rest, wp, bp, t)
                    if check_each and attacked(myk, nstm, wk, bk, r2, nwp, nbp, occ & ~sb):
                        continue
                    exits.append((EXIT, (nstm, wk, bk, tuple(sorted(r2 + ((c, ty, t),))),
                                         nwp, nbp, -1)))
                else:
                    if check_each and attacked(myk, nstm, wk, bk, offs, wp, bp,
                                               (occ & ~sb) | b):
                        continue
                    n_quiet += 1
                    if full:
                        quiet.append((nstm, wk, bk, tuple(sorted(rest + ((c, ty, t),))),
                                      wp, bp, -1))

        # pawns
        if mypawns:
            if stm == WHITE:
                fwd, last, second = W, H - 1, 1
            else:
                fwd, last, second = -W, 0, H - 2
            pm = mypawns
            while pm:
                pb = pm & -pm
                pm ^= pb
                p = pb.bit_length() - 1
                check_each = in_check or pinned & pb
                base_own = mypawns & ~pb
                # (destination, captured square or -1, new e.p. target)
                cands = []
                t = p + fwd
                if not occ >> t & 1:
                    cands.append((t, -1, -1))
                    if g.rank[p] == second:
                        t2 = t + fwd
                        if not occ >> t2 & 1:
                            nep = -1
                            if (self.ep_on and g.rank[t2] != last
                                    and opppawns & g.pawn_from[nstm][t]):
                                nep = t
                            cands.append((t2, -1, nep))
                for t in g.pawn_cap[stm][p]:
                    if opp >> t & 1 and t != oppk:
                        cands.append((t, t, -1))
                if ep >= 0 and ep in g.pawn_cap[stm][p]:
                    cands.append((ep, ep - fwd, -1))
                for t, cs, nep in cands:
                    tb = 1 << t
                    if cs >= 0:
                        noffs, nwp, nbp = self._remove_at(offs, wp, bp, cs)
                    else:
                        noffs, nwp, nbp = offs, wp, bp
                    is_ep = cs >= 0 and cs != t
                    if is_ep or check_each:
                        nocc = (occ & ~pb) | tb
                        if is_ep:
                            nocc &= ~(1 << cs)
                        if attacked(myk, nstm, wk, bk, noffs, nwp, nbp, nocc):
                            continue
                    if g.rank[t] == last:
                        if len(noffs) + 1 > self.cap:
                            for _ in self.promos:
                                exits.append((CAPPED, None))
                            continue
                        for pty in self.promos:
                            o2 = tuple(sorted(noffs + ((stm, pty, t),)))
                            if stm == WHITE:
                                exits.append((EXIT, (nstm, wk, bk, o2, base_own, nbp, -1)))
                            else:
                                exits.append((EXIT, (nstm, wk, bk, o2, nwp, base_own, -1)))
                    else:
                        if stm == WHITE:
                            exits.append((EXIT, (nstm, wk, bk, noffs, base_own | tb, nbp, nep)))
                        else:
                            exits.append((EXIT, (nstm, wk, bk, noffs, nwp, base_own | tb, nep)))
        return n_quiet, quiet, exits

    def _hits(self, ty, s, sq, occ):
        """Does an officer of type ty on s attack sq (occupancy occ)?"""
        g = self.g
        if ty == KNIGHT:
            return g.knight_mask[s] >> sq & 1
        for m in g.paths[ty][s * g.N + sq]:
            if not m & occ:
                return True
        return False

    def unmoves(self, pos):
        """Legal predecessors of a plain position reached by a quiet move (same layer).

        The side that just moved (`mover`) un-moves its king or an officer to an empty square;
        the predecessor is legal iff the king of the side now to move is not attacked in it.
        """
        g = self.g
        stm, wk, bk, offs, wp, bp, _ = pos
        mover = 1 - stm
        occ = self.occupancy(pos)
        if stm == WHITE:
            vk, k, mpawns = wk, bk, bp
        else:
            vk, k, mpawns = bk, wk, wp
        vkb = 1 << vk
        pawn_hit = mpawns & g.pawn_from[mover][vk]
        hits = self._hits
        attacked = self.attacked
        preds = []

        # king un-moves.  Other mover pieces attacking vk once k is vacated?  If none, the
        # only possible attack in the predecessor is king adjacency.
        occ_k = occ & ~(1 << k)
        others = pawn_hit or any(c == mover and hits(ty, s, vk, occ_k) for c, ty, s in offs)
        for s in g.king[k]:
            b = 1 << s
            if occ & b or g.king_mask[s] & vkb:
                continue
            if mover == WHITE:
                if others and attacked(vk, WHITE, s, bk, offs, wp, bp, occ_k | b):
                    continue
                preds.append((WHITE, s, bk, offs, wp, bp, -1))
            else:
                if others and attacked(vk, BLACK, wk, s, offs, wp, bp, occ_k | b):
                    continue
                preds.append((BLACK, wk, s, offs, wp, bp, -1))

        # officer un-moves
        for i, (c, ty, t) in enumerate(offs):
            if c != mover:
                continue
            if ty == KNIGHT:
                sm = g.knight_mask[t] & ~occ
            else:
                sm = 0
                for ray in g.bit_rays[ty][t]:
                    for b in ray:
                        if occ & b:
                            break
                        sm |= b
            rest = offs[:i] + offs[i + 1:]
            occ_t = occ & ~(1 << t)
            others = pawn_hit or any(c2 == mover and hits(ty2, s2, vk, occ_t)
                                     for c2, ty2, s2 in rest)
            while sm:
                b = sm & -sm
                sm ^= b
                s = b.bit_length() - 1
                nocc = occ_t | b
                noffs = tuple(sorted(rest + ((c, ty, s),)))
                if others:
                    if attacked(vk, mover, wk, bk, noffs, wp, bp, nocc):
                        continue
                elif hits(ty, s, vk, nocc):
                    continue
                preds.append((mover, wk, bk, noffs, wp, bp, -1))
        return preds

    # ------------------------------------------------------------------ layers

    def locate(self, pos):
        stm, wk, bk, offs, wp, bp, ep = pos
        N = self.g.N
        idx = wk * N + bk
        types = []
        for c, ty, s in offs:
            idx = idx * N + s
            types.append((c, ty))
        return (wp, bp, tuple(types)), idx * 2 + stm

    def value(self, pos):
        """(A, B) value of a legal position from the side to move's point of view."""
        if pos[6] >= 0:
            return self.eval_direct(pos)
        key, idx = self.locate(pos)
        lay = self.layers.get(key)
        if lay is None:
            lay = self.solve_layer(key)
        a, b = lay[0][idx], lay[1][idx]
        assert a in (WIN, LOSS, DRAW) and b in (WIN, LOSS, DRAW), (pos, a, b)
        return a, b

    def succ_values(self, tag, succ, mover):
        if tag == CAPPED:
            # bound A: White has won; bound B: Black has won.  View of the side to move next.
            if mover == BLACK:     # White to move next
                return WIN, LOSS
            return LOSS, WIN
        return self.value(succ)

    def eval_direct(self, pos):
        """Value a position directly from its successors (used for e.p. transients)."""
        cached = self.ep_cache.get(pos)
        if cached is not None:
            return cached
        _, quiet, exits = self.moves(pos, full=True)
        stm = pos[0]
        if not quiet and not exits:
            v = LOSS if self.in_check(pos) else DRAW
            res = (v, v)
        else:
            best = [LOSS, LOSS]
            for succ in quiet:
                sv = self.value(succ)
                for j in (0, 1):
                    o = MOVER_OUTCOME[sv[j]]
                    if PREF[o] > PREF[best[j]]:
                        best[j] = o
            for tag, succ in exits:
                sv = self.succ_values(tag, succ, stm)
                for j in (0, 1):
                    o = MOVER_OUTCOME[sv[j]]
                    if PREF[o] > PREF[best[j]]:
                        best[j] = o
            res = (best[0], best[1])
        self.ep_cache[pos] = res
        return res

    def solve_layer(self, key):
        wp, bp, types = key
        g = self.g
        N = g.N
        m = len(types)
        size = 2 * N ** (2 + m)
        val = [bytearray([ILLEGAL]) * size, bytearray([ILLEGAL]) * size]
        cnt = [array('H', bytes(2 * size)), array('H', bytes(2 * size))]
        pending = bytearray(size)
        queue = []
        attacked = self.attacked
        moves = self.moves
        succ_values = self.succ_values
        pawns = wp | bp
        free = [s for s in range(N) if not pawns >> s & 1]
        same = [i > 0 and types[i] == types[i - 1] for i in range(m)]
        king_mask = g.king_mask
        n_legal = 0

        for pl in permutations(free, 2 + m):
            wk, bk = pl[0], pl[1]
            if king_mask[wk] >> bk & 1:
                continue
            ok = True
            for i in range(1, m):
                if same[i] and pl[2 + i] < pl[1 + i]:
                    ok = False
                    break
            if not ok:
                continue
            offs = tuple((types[i][0], types[i][1], pl[2 + i]) for i in range(m))
            occ = pawns | (1 << wk) | (1 << bk)
            base = wk * N + bk
            for i in range(m):
                occ |= 1 << pl[2 + i]
                base = base * N + pl[2 + i]
            wk_att = attacked(wk, BLACK, wk, bk, offs, wp, bp, occ)
            bk_att = attacked(bk, WHITE, wk, bk, offs, wp, bp, occ)
            for stm in (WHITE, BLACK):
                if (bk_att if stm == WHITE else wk_att):
                    continue            # side not to move is in check: illegal
                n_legal += 1
                idx = base * 2 + stm
                pos = (stm, wk, bk, offs, wp, bp, -1)
                nq, _, exits = moves(pos, False)
                if nq == 0 and not exits:
                    v = LOSS if (wk_att if stm == WHITE else bk_att) else DRAW
                    val[0][idx] = val[1][idx] = v
                    if v == LOSS:
                        pending[idx] = 3
                        queue.append(idx)
                    continue
                best = [LOSS, LOSS]
                for tag, succ in exits:
                    sv = succ_values(tag, succ, stm)
                    for j in (0, 1):
                        o = MOVER_OUTCOME[sv[j]]
                        if PREF[o] > PREF[best[j]]:
                            best[j] = o
                for j in (0, 1):
                    bj = best[j]
                    if bj == WIN or nq == 0:
                        val[j][idx] = bj
                        if bj != DRAW:
                            if not pending[idx]:
                                queue.append(idx)
                            pending[idx] |= 1 << j
                    else:
                        val[j][idx] = UNK
                        cnt[j][idx] = nq + (1 if bj == DRAW else 0)

        # propagation through quiet un-moves
        unmoves = self.unmoves
        while queue:
            idx = queue.pop()
            fl = pending[idx]
            pending[idx] = 0
            if not fl:
                continue
            stm = idx & 1
            x = idx >> 1
            sq = [0] * (2 + m)
            for i in range(1 + m, -1, -1):
                x, sq[i] = divmod(x, N)
            offs = tuple((types[i][0], types[i][1], sq[2 + i]) for i in range(m))
            pos = (stm, sq[0], sq[1], offs, wp, bp, -1)
            vq = (val[0][idx], val[1][idx])
            for pp in unmoves(pos):
                pidx = pp[1] * N + pp[2]
                for o in pp[3]:
                    pidx = pidx * N + o[2]
                pidx = pidx * 2 + pp[0]
                for j in (0, 1):
                    if not fl >> j & 1:
                        continue
                    vj = val[j]
                    if vj[pidx] != UNK:
                        continue
                    if vq[j] == LOSS:
                        vj[pidx] = WIN
                    else:
                        c = cnt[j][pidx] - 1
                        cnt[j][pidx] = c
                        if c:
                            continue
                        vj[pidx] = LOSS
                    if not pending[pidx]:
                        queue.append(pidx)
                    pending[pidx] |= 1 << j

        table = bytes.maketrans(bytes([UNK]), bytes([DRAW]))
        va = val[0].translate(table)
        vb = val[1].translate(table)
        if va == vb:
            vb = va
        lay = (va, vb)
        self.layers[key] = lay
        self.states_solved += n_legal
        if self.verbose:
            print('layer %s: %d legal states (%d layers so far, %.1fs cpu)'
                  % (self.key_name(key), n_legal, len(self.layers), time.process_time()),
                  file=sys.stderr)
        return lay

    def key_name(self, key):
        wp, bp, types = key
        g = self.g
        parts = ['P' + g.sqname(s) for s in range(g.N) if wp >> s & 1]
        parts += ['p' + g.sqname(s) for s in range(g.N) if bp >> s & 1]
        parts += [(PIECE_CHARS[t] if c == WHITE else PIECE_CHARS[t].lower()) for c, t in types]
        return ' '.join(parts) or '-'

    # ------------------------------------------------------------------ input

    def parse_position(self, line):
        """Parse a position line.  Returns a legal position, or None if illegal/unparseable."""
        g = self.g
        toks = line.split()
        if len(toks) < 4:
            return None
        stm_tok, ep_tok = toks[-2], toks[-1]
        if stm_tok not in ('w', 'b'):
            return None
        stm = WHITE if stm_tok == 'w' else BLACK
        seen = set()
        wk = bk = None
        nwk = nbk = 0
        offs = []
        wp = bp = 0
        for tok in toks[:-2]:
            if len(tok) < 3:
                return None
            letter = tok[0]
            s = g.parse_square(tok[1:])
            if s is None or s in seen:
                return None
            seen.add(s)
            if letter == 'K':
                wk, nwk = s, nwk + 1
            elif letter == 'k':
                bk, nbk = s, nbk + 1
            elif letter == 'P':
                if g.rank[s] in (0, g.H - 1):
                    return None
                wp |= 1 << s
            elif letter == 'p':
                if g.rank[s] in (0, g.H - 1):
                    return None
                bp |= 1 << s
            elif letter in PIECE_CHARS:
                offs.append((WHITE, PIECE_CHARS.index(letter), s))
            elif letter in PIECE_CHARS.lower():
                offs.append((BLACK, PIECE_CHARS.lower().index(letter), s))
            else:
                return None
        if nwk != 1 or nbk != 1:
            return None
        if len(offs) > self.cap:
            return None
        if g.king_mask[wk] >> bk & 1:
            return None
        ep = -1
        if ep_tok != '-':
            e = g.parse_square(ep_tok)
            if e is None:
                return None
            if self.ep_on:
                W = g.W
                if stm == WHITE:   # Black just played a double step from rank H-1 over e
                    pawn_sq, origin, ok_rank = e - W, e + W, g.rank[e] == g.H - 3
                    ok_pawn = ok_rank and bp >> pawn_sq & 1
                else:              # White just played a double step from rank 2 over e
                    pawn_sq, origin, ok_rank = e + W, e - W, g.rank[e] == 2
                    ok_pawn = ok_rank and wp >> pawn_sq & 1
                if not ok_pawn or e in seen or origin in seen:
                    return None
                ep = e
        pos = (stm, wk, bk, tuple(sorted(offs)), wp, bp, ep)
        if self.in_check(pos, 1 - stm):
            return None
        return pos

    def solve_line(self, line):
        """Return (A, B) characters from White's point of view."""
        pos = self.parse_position(line)
        if pos is None:
            return 'X', 'X'
        vals = self.value(pos)
        out = []
        for v in vals:
            if v == DRAW:
                out.append('D')
            elif (v == WIN) == (pos[0] == WHITE):
                out.append('W')
            else:
                out.append('L')
        return out[0], out[1]


def parse_board(text):
    try:
        kind, dims = text.split(':')
        w, h = dims.lower().split('x')
        W, H = int(w), int(h)
    except ValueError:
        raise SystemExit('bad --board %r (expected flat:WxH or cyl:WxH)' % text)
    if kind not in ('flat', 'cyl', 'mob'):
        raise SystemExit('bad board kind %r' % kind)
    if not (2 <= W <= 8 and 4 <= H <= 8):
        raise SystemExit('board must have 2..8 files and 4..8 ranks')
    return Geometry(W, H, kind)


def make_solver(board='cyl:5x5', ep='on', promote='QRBN', cap=1, verbose=False):
    geom = parse_board(board)
    promos = []
    for ch in promote.upper():
        if ch not in PIECE_CHARS:
            raise SystemExit('bad --promote %r' % promote)
        t = PIECE_CHARS.index(ch)
        if t not in promos:
            promos.append(t)
    if not promos:
        raise SystemExit('empty --promote')
    if cap < 0:
        raise SystemExit('--cap must be >= 0')
    return Solver(geom, ep_on=(ep == 'on'), promos=promos, cap=cap, verbose=verbose)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Reference solver for kings/SPEC.md')
    ap.add_argument('--board', required=True, help='flat:WxH, cyl:WxH or mob:WxH')
    ap.add_argument('--ep', choices=('on', 'off'), default='on')
    ap.add_argument('--promote', default='QRBN')
    ap.add_argument('--cap', type=int, default=1)
    ap.add_argument('--verbose', action='store_true', help='layer statistics on stderr')
    args = ap.parse_args(argv)
    sys.setrecursionlimit(100000)
    solver = make_solver(args.board, args.ep, args.promote, args.cap, args.verbose)
    out = sys.stdout
    for raw in sys.stdin:
        line = raw.rstrip('\r\n')
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            out.write(line + '\n')
        else:
            a, b = solver.solve_line(line)
            out.write('%s | %s %s\n' % (line, a, b))
        out.flush()


if __name__ == '__main__':
    main()
