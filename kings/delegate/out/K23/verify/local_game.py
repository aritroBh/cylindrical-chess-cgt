# Referee's own local game L_T(Q_Z) of LOOPY Def 2.6, for the sortie 1...Kd2 2.Kxb4 on cyl:7x6.
# s = Black (may pass unless in check, k=inf, king unrestricted), sbar = White (king confined to files a,b,c, may not pass).
# Q_Z: Wk b4, Pb3 (white Z pawn), black king d2, Black Z pawn b4 was captured; context deleted. Black (s) to move.
import sys
from functools import lru_cache
W, H = 7, 6
def sq(f, r): return (f % W, r)
def nbrs(s):
    f, r = s
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df or dr:
                if 0 <= r + dr < H: yield ((f + df) % W, r + dr)
def adj(a, b): return b in set(nbrs(a))
def pawn_att(p, s):  # white pawn at p attacks s?
    return p is not None and s[1] == p[1] + 1 and ((s[0] - p[0]) % W in (1, W - 1))
QUEEN = len(sys.argv) > 1 and sys.argv[1] == 'queen'
def black_moves(wk, bk, wp):
    """legal black king moves (list of new bk); also returns (in_check, can_pass)"""
    chk = pawn_att(wp, bk)
    res = []
    for n in nbrs(bk):
        if n == wk or adj(n, wk): continue
        if wp is not None and n == wp: # capture of the pawn: legal if not adjacent to wk (already excluded)
            res.append((n, True)); continue
        if pawn_att(wp, n): continue
        res.append((n, False))
    return chk, res
@lru_cache(None)
def white_wins(wk, bk, wp, t, ):
    """Black to move; White must win within t of its moves (t>=1 means White still has t moves to make)."""
    if wp is None or t < 1: return False
    chk, mv = black_moves(wk, bk, wp)
    options = [(n, cap) for n, cap in mv]
    if not chk: options.append((bk, False))  # pass
    if not options: return chk  # mate: win for white; stalemate impossible (pass), so chk is True here
    for n, cap in options:
        if cap: return False  # black captures the pawn: white can never promote
        if not white_reply(wk, n, wp, t): return False
    return True
@lru_cache(None)
def white_reply(wk, bk, wp, t):
    # White to move, has t moves left including this one. Win by promotion or mate, else continue.
    # king moves confined to files 0..2
    for n in nbrs(wk):
        if n[0] > 2: continue
        if n == bk or adj(n, bk) or n == wp: continue
        if white_wins(n, bk, wp, t - 1): return True
    # pawn push
    tgt = (wp[0], wp[1] + 1)
    if tgt != wk and tgt != bk:
        # legal: white king not attacked (no black pawns) so always legal
        if tgt[1] == H - 1:
            # promotion
            if not QUEEN: return True
            # queen clause: win if black cannot capture the queen at once (legal black king capture of tgt)
            if not adj(bk, tgt) or adj(wk, tgt): return True
            # black king adjacent to tgt and tgt not protected by white king -> capturable
        else:
            if white_wins(wk, bk, tgt, t - 1): return True
    return False
wk0, bk0, wp0 = (1, 3), (3, 1), (1, 2)
for t in range(1, 9):
    print('T', t, 'L1_P' if not QUEEN else 'L1', white_wins(wk0, bk0, wp0, t))
