"""Pawn-capture histories and legality checks for the five-file *2 positions (T32).

Board: files 0..7 = a..h, ranks 1..8.  Only pawns are modelled; kings are ignored
for reachability.  Conventions (fixed for T32, stated in REPORT.md):

  * Pawn-only game.  Non-pawn men are assumed to have left the board by non-pawn
    play that is not part of the history, so the only captures are pawn captures
    of enemy pawns.  Each side starts with 8 pawns (rank 2 / rank 7).
  * No promotion: a pawn never moves onto rank 1 or 8 (in a pawn-only game that
    would create a piece).
  * En passant is included (it is a real-chess move that changes files).
  * Exact counts: every enemy pawn missing from the target was captured, so White
    makes exactly 8 - n_black captures and Black makes exactly 8 - n_white.

Reachability is decided by a forward depth-first search from the start position.
Pruning uses only necessary conditions for reaching the target:
  (a) each target pawn is matched to a distinct current pawn of its colour, with
      rank advance >= file shift (captures move a pawn one file and one rank);
  (b) the matching's total file shift is at most the number of captures the side
      still has to make (= enemy pawns still to be removed).
Exhaustion of the search is therefore a proof of IMPOSSIBLE under the conventions above.

Legality beside the trebuchet (files f-h) is checked by `legality`.
"""
from __future__ import annotations

import time

FILES = "abcdefgh"

START_W = frozenset((f, 2) for f in range(8))
START_B = frozenset((f, 7) for f in range(8))

# trébuchet of the paper: W pawn g4, B pawn g5, WK f5, BK h4
TREB = {"W_pawn": (6, 4), "B_pawn": (6, 5), "WK": (5, 5), "BK": (7, 4)}
# its mirror image (files reversed): W pawn b4, B pawn b5, WK c5, BK a4
TREB_MIRROR = {"W_pawn": (1, 4), "B_pawn": (1, 5), "WK": (2, 5), "BK": (0, 4)}


def sq(f, r):
    return f"{FILES[f]}{r}"


def ranks_advanced(f, r, white):
    """Ranks a pawn has advanced from its home rank (white: 2, black: 7)."""
    return (r - 2) if white else (7 - r)


def allowed_start_files(f, r, white):
    adv = ranks_advanced(f, r, white)
    return [f0 for f0 in range(8) if abs(f - f0) <= adv]


def min_captures(pawns, white):
    """Least total file shift needed to end with `pawns` (distinct start files).

    This is a lower bound on the number of captures the side must make.
    Returns (cost, feasible).
    """
    pl = sorted(pawns, key=lambda q: (q[1], q[0]))
    INF = float("inf")
    dp = {0: 0}
    for (f, r) in pl:
        ok = set(allowed_start_files(f, r, white))
        nxt = {}
        for mask, cost in dp.items():
            for f0 in ok:
                if mask >> f0 & 1:
                    continue
                m2 = mask | (1 << f0)
                c2 = cost + abs(f - f0)
                if c2 < nxt.get(m2, INF):
                    nxt[m2] = c2
        dp = nxt
        if not dp:
            return None, False
    return min(dp.values()), True


# --------------------------------------------------------------------------------------
# forward search for a pawn-only history (bitboards: bit index = (rank-1)*8 + file)
# --------------------------------------------------------------------------------------

def _bit(f, r):
    return 1 << ((r - 1) * 8 + f)


def _mask(pawns):
    m = 0
    for f, r in pawns:
        m |= _bit(f, r)
    return m


def _unmask(m):
    out = []
    for idx in range(64):
        if m >> idx & 1:
            out.append((idx % 8, idx // 8 + 1))
    return out


def _match_cost(cur, tgt, side):
    """Min total file shift over injective matchings of targets to current pawns.

    A current pawn (f, r) can be matched to target (g, s) iff its rank advance
    (s - r for White, r - s for Black) is at least |g - f|.  Returns None if no
    matching exists.
    """
    INF = 10 ** 9
    dp = {0: 0}
    for (g, s) in tgt:
        nxt = {}
        for used, c in dp.items():
            for j, (f, r) in enumerate(cur):
                if used >> j & 1:
                    continue
                adv = (s - r) if side == "W" else (r - s)
                d = abs(g - f)
                if adv < d:
                    continue
                u2 = used | (1 << j)
                c2 = c + d
                if c2 < nxt.get(u2, INF):
                    nxt[u2] = c2
        dp = nxt
        if not dp:
            return None
    return min(dp.values())


def _feasible(Wm, Bm, TWm, TBm, nw, nb):
    cw = _unmask(Wm)
    cb = _unmask(Bm)
    if len(cw) < nw or len(cb) < nb:
        return False
    tw = _unmask(TWm)
    tb = _unmask(TBm)
    # a White pawn on rank 7 never moves again and is never captured: it must be a target
    # square already; symmetrically a Black pawn on rank 2.
    for (f, r) in cw:
        if r == 7 and (f, 7) not in tw:
            return False
    for (f, r) in cb:
        if r == 2 and (f, 2) not in tb:
            return False
    c = _match_cost(cw, tw, "W")
    if c is None or c > len(cb) - nb:      # future White captures = Black pawns still to go
        return False
    c = _match_cost(cb, tb, "B")
    if c is None or c > len(cw) - nw:      # future Black captures = White pawns still to go
        return False
    return True


def _moves(W, B, last):
    """All legal pawn-only moves.  Tuples (kind, side, from, to)."""
    occ = W | B
    out = []
    for f in range(8):
        for r in range(2, 8):                      # White pawns on ranks 2..7
            if not W & _bit(f, r):
                continue
            if r + 1 <= 7 and not occ & _bit(f, r + 1):
                out.append(("push", "W", (f, r), (f, r + 1)))
            if r == 2 and not occ & _bit(f, 3) and not occ & _bit(f, 4):
                out.append(("double", "W", (f, 2), (f, 4)))
            if r + 1 <= 7:
                for g in (f - 1, f + 1):
                    if 0 <= g <= 7 and B & _bit(g, r + 1):
                        out.append(("capture", "W", (f, r), (g, r + 1)))
            if r == 5 and last is not None and last[0] == "B" and abs(last[1] - f) == 1:
                out.append(("ep", "W", (f, 5), (last[1], 6)))
        for r in range(3, 8):                      # Black pawns on ranks 3..7 can move
            if not B & _bit(f, r):
                continue
            if r - 1 >= 2 and not occ & _bit(f, r - 1):
                out.append(("push", "B", (f, r), (f, r - 1)))
            if r == 7 and not occ & _bit(f, 6) and not occ & _bit(f, 5):
                out.append(("double", "B", (f, 7), (f, 5)))
            if r - 1 >= 2:
                for g in (f - 1, f + 1):
                    if 0 <= g <= 7 and W & _bit(g, r - 1):
                        out.append(("capture", "B", (f, r), (g, r - 1)))
            if r == 4 and last is not None and last[0] == "W" and abs(last[1] - f) == 1:
                out.append(("ep", "B", (f, 4), (last[1], 3)))
    return out


def _apply(W, B, mv):
    kind, side, frm, to = mv
    if side == "W":
        W = (W & ~_bit(*frm)) | _bit(*to)
        if kind == "capture":
            B &= ~_bit(*to)
        elif kind == "ep":
            B &= ~_bit(to[0], frm[1])
        last = ("W", frm[0]) if kind == "double" else None
    else:
        B = (B & ~_bit(*frm)) | _bit(*to)
        if kind == "capture":
            W &= ~_bit(*to)
        elif kind == "ep":
            W &= ~_bit(to[0], frm[1])
        last = ("B", frm[0]) if kind == "double" else None
    return W, B, last


def find_history(target_w, target_b, start_w=START_W, start_b=START_B, prune=True,
                 node_cap=3_000_000, max_seconds=900):
    """Depth-first forward search for a pawn-only history from start to target.

    Returns (moves, info).  `moves` is a list of (kind, side, from, to) or None.
    info['status'] is 'found', 'exhausted' (proof of impossibility under the
    conventions) or 'cap' (search aborted, undecided).
    """
    TWm, TBm = _mask(target_w), _mask(target_b)
    nw, nb = len(target_w), len(target_b)
    W0, B0 = _mask(start_w), _mask(start_b)
    stack = [(W0, B0, None, ())]
    seen = set()
    t0 = time.time()
    nodes = 0
    while stack:
        W, B, last, path = stack.pop()
        if W == TWm and B == TBm:
            return list(path), {"status": "found", "nodes": nodes, "states": len(seen)}
        key = (W, B, last)
        if key in seen:
            continue
        seen.add(key)
        nodes += 1
        if nodes > node_cap or time.time() - t0 > max_seconds:
            return None, {"status": "cap", "nodes": nodes, "states": len(seen)}
        if prune and not _feasible(W, B, TWm, TBm, nw, nb):
            continue
        for mv in _moves(W, B, last):
            W2, B2, last2 = _apply(W, B, mv)
            stack.append((W2, B2, last2, path + (mv,)))
    return None, {"status": "exhausted", "nodes": nodes, "states": len(seen)}


def format_history(moves):
    """Paper-style strings: 'W c2xd3', 'B b7xa6', pushes 'W a2-a3', double 'W b2-b4', e.p. 'W e5xd6ep'."""
    out = []
    for kind, side, frm, to in moves:
        a, b = sq(*frm), sq(*to)
        if kind == "push":
            s = f"{a}-{b}"
        elif kind == "double":
            s = f"{a}-{b}"
        elif kind == "capture":
            s = f"{a}x{b}"
        else:
            s = f"{a}x{b} e.p."
        out.append(f"{side} {s}")
    return out


# --------------------------------------------------------------------------------------
# legality of the position beside the trébuchet
# --------------------------------------------------------------------------------------

def pawn_attacks(f, r, white):
    """Squares attacked by the pawn on (f, r)."""
    d = 1 if white else -1
    return {(f - 1, r + d), (f + 1, r + d)}


def king_attacks(f, r):
    return {(ff, rr) for ff in (f - 1, f, f + 1) for rr in (r - 1, r, r + 1)
            if (ff, rr) != (f, r)}


def legality(white, black, treb):
    """Legality of a full 8x8 position (pawn sets + trébuchet).

    Returns a dict with the checks the brief asks for.
    """
    W = set(white) | {treb["W_pawn"]}
    B = set(black) | {treb["B_pawn"]}
    WK, BK = treb["WK"], treb["BK"]
    res = {"checks": [], "king_capture_conflicts": [], "adjacent_enemy_pawns": [],
           "efile_touching": [], "kings_adjacent": False}

    # 1. no pawn may give check
    for (f, r) in B:
        if WK in pawn_attacks(f, r, False):
            res["checks"].append(f"black pawn {sq(f, r)} attacks WK {sq(*WK)}")
    for (f, r) in W:
        if BK in pawn_attacks(f, r, True):
            res["checks"].append(f"white pawn {sq(f, r)} attacks BK {sq(*BK)}")
    # kings must not be adjacent
    if BK in king_attacks(*WK):
        res["kings_adjacent"] = True
        res["checks"].append(f"kings {sq(*WK)} and {sq(*BK)} are adjacent")

    # 2. a king may not stand next to an enemy pawn that it could capture
    def scan(king, kingcol, enemy):
        for (f, r) in sorted(enemy):
            if (f, r) in king_attacks(*king):
                defended = any((f, r) in pawn_attacks(ef, er, not kingcol == "W") for (ef, er) in enemy
                               if (ef, er) != (f, r))
                defended = defended or any((f, r) in king_attacks(*ek)
                                           for ek in ([treb["BK"]] if kingcol == "W" else [treb["WK"]]))
                capturable = not defended
                res["adjacent_enemy_pawns"].append(
                    {"king": sq(*king), "pawn": sq(f, r), "pawn_colour": "B" if kingcol == "W" else "W",
                     "defended": defended, "king_can_capture": capturable})
                if capturable:
                    res["king_capture_conflicts"].append(
                        f"{'White' if kingcol == 'W' else 'Black'} king {sq(*king)} can capture "
                        f"{sq(f, r)}")
    scan(WK, "W", B)
    scan(BK, "B", W)

    # 3. e-file pawns touching the king group (the file next to the king file)
    kf = WK[0]
    edge = kf - 1 if kf > 3 else kf + 1        # the component's outermost file
    for (f, r) in sorted(W | B):
        if f != edge:
            continue
        touching = (f, r) in king_attacks(*WK) or (f, r) in king_attacks(*BK)
        if touching:
            res["efile_touching"].append(
                {"square": sq(f, r), "colour": "W" if (f, r) in W else "B",
                 "adjacent_to_WK": (f, r) in king_attacks(*WK),
                 "adjacent_to_BK": (f, r) in king_attacks(*BK)})
    return res


def mirror(pos_set):
    return frozenset((7 - f, r) for (f, r) in pos_set)
