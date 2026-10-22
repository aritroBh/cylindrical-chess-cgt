"""Chess move graph for K4: all positions reachable from K+P vs K, built once per board.

Uses the reference solver's move generator (kings/ref/solve.py) unchanged:
    solver.moves(pos, full=True) -> (n_quiet, quiet_successors, exits)
    solver.in_check(pos)
A position is the tuple (stm, wk, bk, offs, wp, bp, ep); here ep is always -1 (Black has no pawn).

Node set = closure of {every legal K+P vs K position, either side to move} under
  * chess moves (promotion gives K+officer vs K, a king capture gives K vs K), and
  * the PASS (same placement, other side to move), which exists exactly when the mover is not in
    check.  The pass is the chess half of a move made in a test game T (see product.py).
CSR arrays: succ (chess moves), pred (reverse), flip (pass target or -1), incheck (mover in check).
"""

from array import array

from kings.ref.solve import make_solver, CAPPED

WHITE, BLACK = 0, 1


class ChessGraph:
    def __init__(self, board):
        self.board = board
        self.solver = make_solver(board=board, ep='on', promote='QRBN', cap=1)
        self.pos = []            # node id -> position tuple
        self.idx = {}            # position tuple -> node id
        self.stm = bytearray()
        self.incheck = bytearray()
        self.flip = array('i')
        self.succ_off = array('i', [0])
        self.succ = array('i')
        self.kpk = []            # node ids of KPK positions (no officer, one white pawn)
        self.quiet_kpk = []      # placements (wk, wp, bk) with neither king in check, as node pairs
        self._build()

    # -- construction -------------------------------------------------------------------
    def _add(self, p, todo):
        i = self.idx.get(p)
        if i is None:
            i = self.idx[p] = len(self.pos)
            self.pos.append(p)
            todo.append(i)
        return i

    def initial(self):
        g = self.solver.g
        out = []
        for wk in range(g.N):
            for bk in range(g.N):
                if wk == bk or g.king_mask[wk] >> bk & 1:
                    continue
                for wp in range(g.N):
                    if wp in (wk, bk) or g.rank[wp] in (0, g.H - 1):
                        continue
                    for stm in (WHITE, BLACK):
                        p = (stm, wk, bk, (), 1 << wp, 0, -1)
                        if not self.solver.in_check(p, 1 - stm):   # side not to move in check: illegal
                            out.append(p)
        return out

    def _build(self):
        S = self.solver
        todo = []
        for p in self.initial():
            self._add(p, todo)
        self.n_initial = len(self.pos)
        rows, flips, chk = {}, {}, {}
        while todo:
            i = todo.pop()
            p = self.pos[i]
            nq, quiet, exits = S.moves(p, full=True)
            succs = list(quiet)
            for tag, q in exits:
                assert tag != CAPPED, 'capped promotion with one pawn: %r' % (p,)
                succs.append(q)
            rows[i] = [self._add(q, todo) for q in succs]
            chk[i] = S.in_check(p)
            flips[i] = -1 if chk[i] else self._add((1 - p[0],) + p[1:], todo)
        n = len(self.pos)
        for i in range(n):
            self.stm.append(self.pos[i][0])
            self.incheck.append(1 if chk[i] else 0)
            self.flip.append(flips[i])
            self.succ.extend(rows[i])
            self.succ_off.append(len(self.succ))
        self.n = n
        # reverse adjacency (CSR)
        cnt = [0] * (n + 1)
        for j in self.succ:
            cnt[j + 1] += 1
        for k in range(n):
            cnt[k + 1] += cnt[k]
        self.pred_off = array('i', cnt)
        fill = list(cnt[:n])
        self.pred = array('i', [0]) * len(self.succ)
        for i in range(n):
            for k in range(self.succ_off[i], self.succ_off[i + 1]):
                j = self.succ[k]
                self.pred[fill[j]] = i
                fill[j] += 1
        # K+P vs K nodes and quiet placements
        for i, p in enumerate(self.pos):
            if not p[3] and p[4] and not p[5] and bin(p[4]).count('1') == 1:
                self.kpk.append(i)
        for i in self.kpk:
            if self.stm[i] == WHITE and self.flip[i] >= 0:
                self.quiet_kpk.append((i, self.flip[i]))   # (white to move, black to move)

    # -- helpers ------------------------------------------------------------------------
    def sqname(self, s):
        return self.solver.g.sqname(s)

    def placement(self, i):
        """'Ka1 Pb2 kc3' (squares of WK, P, BK) for a K+P vs K node."""
        stm, wk, bk, offs, wp, bp, ep = self.pos[i]
        return 'K%s P%s k%s' % (self.sqname(wk), self.sqname(wp.bit_length() - 1), self.sqname(bk))

    def kp_line(self, i):
        """Input line for kpsolve."""
        stm, wk, bk, offs, wp, bp, ep = self.pos[i]
        toks = ['K' + self.sqname(wk), 'k' + self.sqname(bk)]
        if wp:
            toks.append('P' + self.sqname(wp.bit_length() - 1))
        for c, ty, s in offs:
            ch = 'QRBN'[ty]
            toks.append((ch if c == WHITE else ch.lower()) + self.sqname(s))
        return ' '.join(toks) + (' w -' if stm == WHITE else ' b -')


class DummyGraph:
    """No chess at all: two nodes (White to move, Black to move) that pass to each other.
    dummy x T is then exactly the CGT game T under normal play."""
    n = 2
    stm = bytearray([0, 1])
    incheck = bytearray([0, 0])
    flip = array('i', [1, 0])
    succ_off = array('i', [0, 0, 0])
    succ = array('i')
    pred_off = array('i', [0, 0, 0])
    pred = array('i')
    board = 'none'
