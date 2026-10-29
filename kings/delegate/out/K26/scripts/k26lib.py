#!/usr/bin/env python3
"""K26 library: own geometry, candidate enumeration and leak classification for king groups on files a-c.
Written for K26 from LOOPY.md section 3-4 and K14/VERIFY.md section 5 (method only; no K14 code is used).

Conventions
  F_Z = files a,b,c.  A square of F_Z is index i = (file-1)*H + (rank-1), file 1..3, rank 1..H.
  Pawns of the group stand on ranks 2..H-1 of F_Z.
  K1: no king square of the group is attacked by an enemy group pawn.
  K2: the king distance between any square of the White shuttle and any square of the Black king(s) is >= 2.
  A 'leak' of a root = a legal move of the side to move that is not a shuttle move and does not lose at once
  for the mover (value L for a White move, W for a Black move, in the P model, as printed by kpp --pmodel --moves).
"""
import itertools, os, subprocess, sys, collections

def safe_nice():
    """raise the niceness to 15, but never beyond it (a process started by heavy.sh already has niceness 15; os.nice(15) again raises EPERM on macOS)"""
    try:
        cur = os.nice(0)
        if cur < 15:
            os.nice(15 - cur)
    except OSError:
        pass


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
BIN = os.environ.get('K26_BIN', os.path.join(OUT, 'bin'))   # K26_BIN=<dir> selects a private build (the final attempt used bin_r/)
FILES = 'abcdefgh'
COLLAPSE_PROMO = os.environ.get('K26_COLLAPSE_PROMO', '0') == '1'   # default 0 = the convention of the original runs (one leak per promotion piece)


class Geo:
    def __init__(self, H, NF=3):
        self.H = H
        self.NF = NF
        n = self.n = NF * H
        self.f = [i // H + 1 for i in range(n)]
        self.r = [i % H + 1 for i in range(n)]
        self.name = [FILES[self.f[i] - 1] + str(self.r[i]) for i in range(n)]
        self.byname = {self.name[i]: i for i in range(n)}
        self.dist = [[max(abs(self.f[i] - self.f[j]), abs(self.r[i] - self.r[j])) for j in range(n)] for i in range(n)]
        self.all = (1 << n) - 1
        self.pawnsq = [i for i in range(n) if 2 <= self.r[i] <= H - 1]
        # attack masks (inside F_Z only) of a pawn on square i
        self.watt = [0] * n
        self.batt = [0] * n
        for i in range(n):
            for df in (-1, 1):
                f2 = self.f[i] + df
                if 1 <= f2 <= NF:
                    r2 = self.r[i] + 1
                    if 1 <= r2 <= H:
                        self.watt[i] |= 1 << ((f2 - 1) * H + r2 - 1)
                    r2 = self.r[i] - 1
                    if 1 <= r2 <= H:
                        self.batt[i] |= 1 << ((f2 - 1) * H + r2 - 1)
        # adjacent pairs
        self.pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if self.dist[i][j] == 1]
        self.pmask = [(1 << i) | (1 << j) for (i, j) in self.pairs]
        npr = len(self.pairs)
        self.compat = [0] * npr  # bitmask over pairs q: K2 between pair p and pair q
        for p, (a, b) in enumerate(self.pairs):
            for q, (c, d) in enumerate(self.pairs):
                if all(self.dist[x][y] >= 2 for x in (a, b) for y in (c, d)):
                    self.compat[p] |= 1 << q
        self.scompat = [0] * npr  # bitmask over squares s: distance >= 2 from both squares of pair p
        for p, (a, b) in enumerate(self.pairs):
            for s in range(n):
                if self.dist[a][s] >= 2 and self.dist[b][s] >= 2:
                    self.scompat[p] |= 1 << s

    def configs(self, nW, nB):
        """all disjoint pawn placements: <= nW white and <= nB black pawns on pawn squares of F_Z.
        returns list of tuples (wp, bp, occ, wa, ba, passW, passB, string)"""
        ps = self.pawnsq
        out = []
        for kw in range(nW + 1):
            for wp in itertools.combinations(ps, kw):
                wocc = 0
                wa = 0
                for i in wp:
                    wocc |= 1 << i
                    wa |= self.watt[i]
                for kb in range(nB + 1):
                    for bp in itertools.combinations(ps, kb):
                        bocc = 0
                        ba = 0
                        for i in bp:
                            bocc |= 1 << i
                            ba |= self.batt[i]
                        if wocc & bocc:
                            continue
                        # textbook passed pawn (no e.p. flag at a root, so identical to the e.p.-aware test)
                        passW = any(not any(abs(self.f[j] - self.f[i]) <= 1 and self.r[j] > self.r[i] for j in bp) for i in wp)
                        passB = any(not any(abs(self.f[j] - self.f[i]) <= 1 and self.r[j] < self.r[i] for j in wp) for i in bp)
                        s = ' '.join(['P' + self.name[i] for i in wp] + ['p' + self.name[i] for i in bp])
                        out.append((wp, bp, wocc | bocc, wa, ba, passW, passB, s))
        return out

    # candidates ---------------------------------------------------------------------------------------------
    def t2(self, cfg):
        """both kings shuttle: yields (wpair, bpair)"""
        wp, bp, occ, wa, ba = cfg[:5]
        wsafe = self.all & ~occ & ~ba
        bsafe = self.all & ~occ & ~wa
        wpairs = [p for p in range(len(self.pairs)) if self.pmask[p] & ~wsafe == 0]
        bbits = 0
        for q in range(len(self.pairs)):
            if self.pmask[q] & ~bsafe == 0:
                bbits |= 1 << q
        for p in wpairs:
            m = self.compat[p] & bbits
            while m:
                lsb = m & -m
                yield (p, lsb.bit_length() - 1)
                m ^= lsb

    def t1(self, cfg):
        """White shuttles (pair p), Black king on a single square s (safe from white pawns): yields (p, s)"""
        wp, bp, occ, wa, ba = cfg[:5]
        wsafe = self.all & ~occ & ~ba
        bsafe = self.all & ~occ & ~wa
        for p in range(len(self.pairs)):
            if self.pmask[p] & ~wsafe:
                continue
            m = self.scompat[p] & bsafe
            while m:
                lsb = m & -m
                yield (p, lsb.bit_length() - 1)
                m ^= lsb


def pos_str(geo, cfg, wk, bk, stm):
    if cfg[7]:
        return 'K%s k%s %s %s -' % (geo.name[wk], geo.name[bk], cfg[7], stm)
    return 'K%s k%s %s -' % (geo.name[wk], geo.name[bk], stm)


# ------------------------------------------------------------------------------------------------------------
# solver access
# ------------------------------------------------------------------------------------------------------------
def solver_cmd(board, solver='kpp', moves=True):
    if solver == 'kpp':
        c = [os.path.join(BIN, 'kpp'), '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel']
    elif solver == 'kp':
        c = [os.path.join(BIN, 'kp'), '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1']
    elif solver in ('ref3', 'ref3m'):
        b = board.replace(':', '') if board.startswith('flat') else board  # ref3 reads the size at offset 4
        c = [os.path.join(BIN, solver), '--board', b]
        if solver == 'ref3m' and moves:
            c.append('--moves')
        return c
    else:
        raise ValueError(solver)
    if moves:
        c.append('--moves')
    return c


def run_solver(lines, board, solver='kpp', moves=True):
    cmd = solver_cmd(board, solver, moves)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         preexec_fn=safe_nice)
    out, err = p.communicate('\n'.join(lines) + '\n')
    if p.returncode != 0:
        raise RuntimeError('solver failed: %s\n%s' % (cmd, err[-500:]))
    res = out.split('\n')
    if res and res[-1] == '':
        res.pop()
    if len(res) != len(lines):
        raise RuntimeError('line count mismatch %d vs %d' % (len(res), len(lines)))
    return res, err


def parse_line(line):
    """-> (stm, rootvalue, moves) with moves = list of (name, value); rootvalue from White's view; 'X' = illegal."""
    parts = line.split(' | ')
    pos = parts[0].split()
    stm = pos[-2]
    r = parts[1].split()
    mv = []
    if len(parts) > 2:
        if parts[2].startswith('A:'):
            raise RuntimeError('two bounds in P model: ' + line)
        for tok in parts[2].split():
            nm, v = tok.rsplit(':', 1)
            mv.append((nm, v))
    return stm, r[0], mv


def classify_moves(stm, moves, shuttle_names):
    """shuttle_names: set of the two square names of the mover's shuttle (or None).
    returns (n_shuttle, shuttle_vals, n_nonshuttle, leaks)  with leaks = [(move, value)]"""
    lose = 'L' if stm == 'w' else 'W'
    nsh = 0
    shv = []
    leaks = []
    nn = 0
    if COLLAPSE_PROMO:      # a promotion is one move whatever the piece (kpp prints one entry per piece): keep the first entry of each (from, to)
        seen_p = set()
        mv2 = []
        for nm, v in moves:
            if '=' in nm:
                key = nm.split('=')[0]
                if key in seen_p:
                    continue
                seen_p.add(key)
            mv2.append((nm, v))
        moves = mv2
    for nm, v in moves:
        if shuttle_names and nm[0] == 'K' and len(nm) == 5 and {nm[1:3], nm[3:5]} == shuttle_names:
            nsh += 1
            shv.append(v)
            continue
        nn += 1
        if v != lose:
            leaks.append((nm, v))
    return nsh, shv, nn, leaks
