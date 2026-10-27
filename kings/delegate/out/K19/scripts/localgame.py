"""K19: the local promotion game of Definition 2.6 (LOOPY.md), the stalemate condition (L3), the mu search
(L2), written from the definitions only.

Roles: A = the attacker (s-bar in the text, the side that wants to promote), D = the defender (s, the side
that made the sortie m; it may pass).  Root = the position Q with D to move.

Options (all explicit so that the pre-K7 and the K7 versions can both be run):
  conf       set of files A's king may step onto (None = no confinement)
  queen      queen clause: A's promotion wins only if the new queen cannot be captured at once
  mate_win   a move of A that leaves D in check without a legal move wins for A (K7 rule 4)
  k          pass budget of D: None = unlimited, int = that many passes (pre-K7 had k <= 4 and unlimited)
  D stalemated (no legal move, no pass available, not in check) = failure for A.
"""
import sys
from collections import deque
from k19engine import *


class Local:
    def __init__(self, B, A, conf=None, queen=True, mate_win=True, ep_on=True):
        self.B, self.A, self.D = B, A, 1 - A
        self.conf = None if conf is None else set(conf)
        self.queen, self.mate_win, self.ep_on = queen, mate_win, ep_on
        self.memoA, self.memoD = {}, {}
        self.lm = {}

    # ---- move helpers -------------------------------------------------
    def moves(self, pos):
        r = self.lm.get(pos)
        if r is None:
            r = legal_moves(self.B, pos, self.ep_on)
            self.lm[pos] = r
        return r

    def a_moves(self, pos):
        B = self.B
        mv = self.moves(pos)
        if self.conf is None:
            return mv
        ksq = pos[0] if self.A == 0 else pos[1]
        out = []
        for m in mv:
            if m.frm == ksq and m.kind == 'n' and B.file[m.to] not in self.conf and self.is_king_move(pos, m):
                continue
            out.append(m)
        return out

    def is_king_move(self, pos, m):
        ksq = pos[0] if pos[5] == 0 else pos[1]
        return m.frm == ksq

    def mated(self, pos):
        return in_check(self.B, pos) and not self.moves(pos)

    # ---- bounded game ---------------------------------------------------
    def Awin(self, pos, t, k):
        if t <= 0:
            return False
        key = (pos, t, k)
        r = self.memoA.get(key)
        if r is not None:
            return r
        res = False
        for m in self.a_moves(pos):
            if m.kind == 'p':
                if not self.queen:
                    res = True
                    break
                if not promo_capturable(self.B, m.pos, self.A, m.to, self.ep_on):
                    res = True
                    break
                continue
            if self.mate_win and self.mated(m.pos):
                res = True
                break
            if t >= 2 and self.Dwin(m.pos, t - 1, k):
                res = True
                break
        self.memoA[key] = res
        return res

    def Dwin(self, pos, t, k):
        """D to move, A has t moves left; True iff A forces the win."""
        key = (pos, t, k)
        r = self.memoD.get(key)
        if r is not None:
            return r
        mv = self.moves(pos)
        chk = in_check(self.B, pos)
        can_pass = (not chk) and (k is None or k > 0)
        res = True
        if not mv and not can_pass:
            res = bool(chk and self.mate_win)
        else:
            for m in mv:
                if m.kind == 'p' or not self.Awin(m.pos, t, k):
                    res = False
                    break
            if res and can_pass:
                if not self.Awin(pass_move(pos), t, None if k is None else k - 1):
                    res = False
        self.memoD[key] = res
        return res

    def minT(self, root, k, tmax=14):
        for T in range(1, tmax + 1):
            if self.Dwin(root, T, k):
                return T
        return None

    # ---- (L3): s never stalemated in the real window --------------------------
    def L3(self, pos, t, memo=None):
        """A to move with t moves left. True iff A has a guided strategy (each move winning in the local game with
        unlimited passes and the remaining time) such that the real D (no pass) is never stalemated."""
        if memo is None:
            memo = self.memoL3 = getattr(self, 'memoL3', {})
        key = (pos, t)
        r = memo.get(key)
        if r is not None:
            return r
        res = False
        for m in self.a_moves(pos):
            if m.kind == 'p':
                if not self.queen or not promo_capturable(self.B, m.pos, self.A, m.to, self.ep_on):
                    res = True
                    break
                continue
            if self.mate_win and self.mated(m.pos):
                res = True
                break
            if t >= 2 and self.Dwin(m.pos, t - 1, None):
                reps = self.moves(m.pos)
                if not reps:
                    continue          # D stalemated (not mated: mate handled above): (L3) violated on this branch
                if all(self.L3(r2.pos, t - 1, memo) for r2 in reps):
                    res = True
                    break
        memo[key] = res
        return res

    def L3_root(self, root, T):
        """root = Q with D to move. Real D has no pass."""
        if not self.Dwin(root, T, None):
            return None           # (L1) fails
        reps = self.moves(root)
        if not reps:
            return not False if self.mated(root) else False
        return all(self.L3(r.pos, T) for r in reps)

    # ---- unbounded game (least fixed point), passes unlimited or none ----------------------
    def lfp(self, root, passes):
        """Least fixed point of the local game without a time bound. passes: True = D may pass whenever not in
        check, False = D never passes. Returns (A_wins_from_root, number_of_states). Infinite play = failure for A."""
        idx = {}
        nodes = []          # (pos, role) role 0 = A to move, 1 = D to move
        def get(pos, role):
            key = (pos, role)
            i = idx.get(key)
            if i is None:
                i = len(nodes)
                idx[key] = i
                nodes.append(key)
                stack.append(i)
            return i
        stack = []
        succ = []
        imm = []      # A node: immediate win available; D node: dead (cannot be won)
        get(root, 1)
        while stack:
            i = stack.pop()
            pos, role = nodes[i]
            while len(succ) <= i:
                succ.append(None)
                imm.append(False)
            if role == 0:
                s_l = []
                win = False
                for m in self.a_moves(pos):
                    if m.kind == 'p':
                        if not self.queen or not promo_capturable(self.B, m.pos, self.A, m.to, self.ep_on):
                            win = True
                        continue
                    if self.mate_win and self.mated(m.pos):
                        win = True
                        continue
                    s_l.append(get(m.pos, 1))
                succ[i] = s_l
                imm[i] = win
            else:
                s_l = []
                mv = self.moves(pos)
                chk = in_check(self.B, pos)
                can_pass = passes and not chk
                dead = False
                if not mv and not can_pass:
                    dead = not (chk and self.mate_win)
                    imm[i] = dead       # dead
                    succ[i] = []
                    if not dead:
                        imm[i] = False
                    continue
                for m in mv:
                    if m.kind == 'p':
                        dead = True
                        break
                    s_l.append(get(m.pos, 0))
                if not dead and can_pass:
                    s_l.append(get(pass_move(pos), 0))
                succ[i] = s_l
                imm[i] = dead
        n = len(nodes)
        pred = [[] for _ in range(n)]
        for i in range(n):
            for j in succ[i]:
                pred[j].append(i)
        win = [False] * n
        cnt = [0] * n
        work = deque()
        for i in range(n):
            pos, role = nodes[i]
            if role == 0:
                if imm[i]:
                    win[i] = True
                    work.append(i)
            else:
                if imm[i]:
                    continue                  # dead
                cnt[i] = len(succ[i])
                if cnt[i] == 0:
                    win[i] = True             # D mated
                    work.append(i)
        while work:
            j = work.popleft()
            for i in pred[j]:
                if win[i]:
                    continue
                pos, role = nodes[i]
                if role == 0:
                    win[i] = True
                    work.append(i)
                else:
                    if imm[i]:
                        continue
                    cnt[i] -= 1
                    if cnt[i] == 0:
                        win[i] = True
                        work.append(i)
        return win[idx[(root, 1)]], n


# ---- (L2): mu_s ------------------------------------------------------------------------
def mu_search(B, s, ksq, s_pawns, sbar_pawns, ep=-1, ep_on=True, limit=40):
    """Least number of consecutive s-moves (s-bar never moves; s-bar's king and all Z-pawns absent) after which
    a pawn of s promotes. s_pawns / sbar_pawns are the context pawns. ep = e.p. target usable at the first move
    only. A king may not step onto a square attacked by an s-bar pawn; no move may leave s's king attacked by an
    s-bar pawn. Returns None if impossible."""
    W, H = B.W, B.H
    sg = 1 if s == 0 else -1
    last = H - 1 if s == 0 else 0
    start_rank = 1 if s == 0 else H - 2
    enemy = 1 - s

    def pawn_attacks_sq(sq, pawns):
        return any(p in pawns for p in B.pfrom[enemy][sq])

    start = (ksq, tuple(sorted(s_pawns)), tuple(sorted(sbar_pawns)), ep)
    seen = {start}
    frontier = [start]
    for depth in range(1, limit + 1):
        nxt = []
        for (k, sp, ep_, e) in frontier:
            occ = set(sp) | set(ep_) | {k}
            # king moves
            for t in B.kn[k]:
                if t in sp:
                    continue
                nep = ep_
                if t in ep_:
                    nep = tuple(x for x in ep_ if x != t)
                if pawn_attacks_sq(t, nep):
                    continue
                st = (t, sp, nep, -1)
                if st not in seen:
                    seen.add(st)
                    nxt.append(st)
            for p in sp:
                r = B.rank[p]
                tgt = p + sg * W
                moves = []
                if tgt not in occ:
                    moves.append((tgt, None, ep_, -1))
                    if r == start_rank:
                        t2 = tgt + sg * W
                        if t2 not in occ:
                            moves.append((t2, None, ep_, -1))
                for c in B.pcap[s][p]:
                    if c in ep_:
                        moves.append((c, None, tuple(x for x in ep_ if x != c), -1))
                    elif ep_on and c == e and e >= 0:
                        victim = c - sg * W
                        if victim in ep_:
                            moves.append((c, None, tuple(x for x in ep_ if x != victim), -1))
                for (dest, _, nep, _e) in moves:
                    if B.rank[dest] == last:
                        # promotion (the king must not be left attacked)
                        if not pawn_attacks_sq(k, nep):
                            return depth
                        continue
                    nsp = tuple(sorted(dest if x == p else x for x in sp))
                    if pawn_attacks_sq(k, nep):
                        continue
                    st = (k, nsp, nep, -1)
                    if st not in seen:
                        seen.add(st)
                        nxt.append(st)
        frontier = nxt
        if not frontier:
            break
    return None
