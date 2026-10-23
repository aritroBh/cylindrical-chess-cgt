#!/usr/bin/env python3
import sys, os, json, random, itertools, collections
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from cylcgt import pawns as P
P.PASSED_RESPECTS_EP = True
P._value.cache_clear() if hasattr(P, "_value") else None

INF = 10**9

def nb(W, wrap, f, df):
    g = f + df
    if wrap:
        return g % W
    return g if 0 <= g < W else None

def rho_beta(rank, beta, H):
    return rank if beta == "W" else H + 1 - rank

def ep_capturable(W, H, wrap, pos, side, sq):
    # pos: dict with ep tuple or None
    if not (P.PASSED_RESPECTS_EP and pos.get("ep") and pos["ep"][1] == sq and pos["ep"][2] != side):
        return False
    f, r = sq
    theirs = pos["B"] if side == "W" else pos["W"]
    for g in (nb(W, wrap, f, -1), nb(W, wrap, f, 1)):
        if g is not None and (g, r) in theirs:
            return True
    return False

def pawn_passed(W, H, wrap, pos, side, sq):
    mine = pos["W"] if side == "W" else pos["B"]
    theirs = pos["B"] if side == "W" else pos["W"]
    f, r = sq
    files = {f} | {g for g in (nb(W, wrap, f, -1), nb(W, wrap, f, 1)) if g is not None}
    if side == "W":
        blocked = any(g in files and s > r for (g, s) in theirs)
    else:
        blocked = any(g in files and s < r for (g, s) in theirs)
    if blocked:
        return False
    if ep_capturable(W, H, wrap, pos, side, sq):
        return False
    return True

def path_ahead_empty(W, H, wrap, pos, beta, p):
    f, r = p
    if beta == "W":
        ranks = range(r + 1, H + 1)
    else:
        ranks = range(r - 1, 0, -1)
    occ = pos["W"] | pos["B"] | {pos["wk"], pos["bk"]}
    for rr in ranks:
        if (f, rr) in occ:
            return False
    return True

def H1(W, H, wrap, pos, beta, p):
    if p not in (pos["W"] if beta == "W" else pos["B"]):
        return False
    if not pawn_passed(W, H, wrap, pos, beta, p):
        return False
    if not path_ahead_empty(W, H, wrap, pos, beta, p):
        return False
    return True

def H2(W, H, wrap, pos, beta):
    king = pos["wk"] if beta == "W" else pos["bk"]
    kf = king[0]
    adj = {nb(W, wrap, kf, -1), nb(W, wrap, kf, 1)}
    adj.discard(None)
    occ_files_pawns = {sq[0] for sq in (pos["W"] | pos["B"])}
    return adj.isdisjoint(occ_files_pawns)

def H3(W, H, wrap, pos, omega):
    # omega king has neighbouring square t not adjacent to beta king, no pawn on files around t
    beta = "B" if omega == "W" else "W"
    kw = pos["wk"] if omega == "W" else pos["bk"]
    kb = pos["bk"] if omega == "W" else pos["wk"]
    occ_pawn_files = {sq[0] for sq in (pos["W"] | pos["B"])}
    # king neighbours
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            f = kw[0] + df
            r = kw[1] + dr
            if wrap:
                f = f % W
            if not (0 <= f < W and 1 <= r <= H):
                continue
            # Chebyshev distance to beta king >=2
            if wrap:
                dfile = min(abs(f-kb[0]), W-abs(f-kb[0]))
            else:
                dfile = abs(f-kb[0])
            dr = abs(r-kb[1])
            if max(dfile, dr) <= 1:
                continue
            t = (f, r)
            # no pawn on file t or adjacent
            files_around = {nb(W, wrap, t[0], -1), t[0], nb(W, wrap, t[0], 1)}
            files_around.discard(None)
            if files_around & occ_pawn_files:
                continue
            # also not occupied by king? beta king distance condition already
            return True
    return False

def H4(W, H, wrap, pos, beta, p):
    pf = p[0]
    pr = rho_beta(p[1], beta, H)
    adj_files = {nb(W, wrap, pf, -1), nb(W, wrap, pf, 1)}
    adj_files.discard(None)
    mine = pos["W"] if beta == "W" else pos["B"]
    for q in mine:
        if q == p:
            continue
        if q[0] not in adj_files:
            continue
        if rho_beta(q[1], beta, H) > pr + 1:
            return False
    return True

def d_beta(rank, beta, H):
    if beta == "W":
        return H - rank - (1 if rank == 2 else 0)
    else:
        return rank - 1 - (1 if rank == H - 1 else 0)

def mu_omega(W, H, wrap, omega, beta, pos_without_p, allow_ep, ep, wk, bk):
    # pos_without_p has W/B sets excluding p; kings wk (white king), bk
    ow = set(pos_without_p["W"] if omega == "W" else pos_without_p["B"])  # omega pawns
    # Actually pos stores white/black; need pass omega pawns separately. We'll restructure caller.
    pass

# We'll implement mu with explicit sets.
def omega_moves_and_states(W, H, wrap, omega, omega_pawns, beta_pawns, wk, bk, allow_ep, ep):
    occ = set(omega_pawns) | set(beta_pawns) | {wk, bk}
    dir_ = 1 if omega == "W" else -1
    start = 2 if omega == "W" else H - 1
    prom = H if omega == "W" else 1
    res = []  # list of (new_ow, new_bw, promotes)
    for (f, r) in list(omega_pawns):
        # single push
        r1 = r + dir_
        if 1 <= r1 <= H:
            dest = (f, r1)
            if dest not in occ:
                if r1 == prom:
                    res.append((None, None, True))
                else:
                    new_ow = set(omega_pawns); new_ow.discard((f, r)); new_ow.add(dest)
                    res.append((frozenset(new_ow), frozenset(beta_pawns), False))
                # double
                if r == start:
                    r2 = r + 2 * dir_
                    if 1 <= r2 <= H:
                        mid = (f, r1)
                        dest2 = (f, r2)
                        if mid not in occ and dest2 not in occ:
                            if r2 == prom:
                                res.append((None, None, True))
                            else:
                                new_ow = set(omega_pawns); new_ow.discard((f, r)); new_ow.add(dest2)
                                res.append((frozenset(new_ow), frozenset(beta_pawns), False))
        # captures
        for df in (-1, 1):
            g = nb(W, wrap, f, df)
            if g is None:
                continue
            r1 = r + dir_
            if not (1 <= r1 <= H):
                continue
            dest = (g, r1)
            # normal capture of beta pawn
            if dest in beta_pawns:
                if r1 == prom:
                    res.append((None, None, True))
                else:
                    new_ow = set(omega_pawns); new_ow.discard((f, r)); new_ow.add(dest)
                    new_bw = set(beta_pawns); new_bw.discard(dest)
                    res.append((frozenset(new_ow), frozenset(new_bw), False))
            # ep
            if allow_ep and ep is not None and ep[0] == dest:
                # captured square ep[1] must be beta pawn
                if ep[1] in beta_pawns and dest not in occ:
                    if r1 == prom:
                        res.append((None, None, True))
                    else:
                        new_ow = set(omega_pawns); new_ow.discard((f, r)); new_ow.add(dest)
                        new_bw = set(beta_pawns); new_bw.discard(ep[1])
                        res.append((frozenset(new_ow), frozenset(new_bw), False))
    return res

def mu_omega_val(W, H, wrap, omega, beta, omega_pawns, beta_pawns, wk, bk, allow_ep, ep):
    if not omega_pawns:
        return INF
    start_key = (frozenset(omega_pawns), frozenset(beta_pawns), allow_ep)
    visited = {start_key}
    q = collections.deque()
    q.append((frozenset(omega_pawns), frozenset(beta_pawns), allow_ep, 0))
    while q:
        ow, bw, ae, d = q.popleft()
        moves = omega_moves_and_states(W, H, wrap, omega, ow, bw, wk, bk, ae, ep)
        for (now, nbw, prom) in moves:
            if prom:
                return d + 1
            key = (now, nbw, False)
            if key not in visited:
                visited.add(key)
                q.append((now, nbw, False, d + 1))
    return INF

def cylcgt_pos(W, H, wrap, pos):
    # build P.Board and P.Pos for passed test
    board = P.Board(W, H, wrap, True)
    w = frozenset(pos["W"]); b = frozenset(pos["B"])
    ep = pos.get("ep")
    # P.Pos ep tuple same: (target, captured, side)
    pp = P.Pos(w, b, ep)
    return board, pp

def passed_side(W, H, wrap, pos, side):
    board, pp = cylcgt_pos(W, H, wrap, pos)
    # need p-specific? cylcgt passed returns any. For H1 we use pawn_passed own.
    return P.passed(board, pp, side)

def certify(W, H, wrap, pos, beta, stm):
    # returns list of p squares satisfying H1-H5
    omega = "B" if beta == "W" else "W"
    wk = pos["wk"]; bk = pos["bk"]
    mine = pos["W"] if beta == "W" else pos["B"]
    res = []
    for p in mine:
        if not H1(W, H, wrap, pos, beta, p):
            continue
        if not H2(W, H, wrap, pos, beta):
            continue
        if not H3(W, H, wrap, pos, omega):
            continue
        if not H4(W, H, wrap, pos, beta, p):
            continue
        # H5
        # remove p from pos
        pos2 = {"W": set(pos["W"]), "B": set(pos["B"]), "wk": wk, "bk": bk, "ep": pos.get("ep")}
        if beta == "W":
            pos2["W"].discard(p)
        else:
            pos2["B"].discard(p)
        pos2["W"] = frozenset(pos2["W"]); pos2["B"] = frozenset(pos2["B"])
        # omega pawns set
        omega_pawns = pos2["B"] if omega == "B" else pos2["W"]  # careful: omega color
        # omega color's pawn set:
        if omega == "W":
            omega_pawns = pos2["W"]
            beta_pawns = pos2["B"]
        else:
            omega_pawns = pos2["B"]
            beta_pawns = pos2["W"]
        d = d_beta(p[1], beta, H)
        e = d if stm == omega else d - 1
        allow_ep = (stm == omega and pos.get("ep") is not None and pos["ep"][2] == omega)
        mu = mu_omega_val(W, H, wrap, omega, beta, omega_pawns, beta_pawns, wk, bk, allow_ep, pos.get("ep"))
        if mu >= e + 1:
            res.append(p)
    return res

def pos_to_str(W, H, wrap, pos, stm):
    # kpsolve input
    toks = []
    for (f, r) in pos["W"]:
        toks.append("P" + chr(ord('a')+f) + str(r))  # placeholder? need piece letters
    # Actually use K/P
    toks = []
    wk = pos["wk"]; bk = pos["bk"]
    toks.append("K" + chr(ord('a')+wk[0]) + str(wk[1]))
    toks.append("k" + chr(ord('a')+bk[0]) + str(bk[1]))
    for (f, r) in pos["W"]:
        toks.append("P" + chr(ord('a')+f) + str(r))
    for (f, r) in pos["B"]:
        toks.append("p" + chr(ord('a')+f) + str(r))
    ep = pos.get("ep")
    eptarget = "-"
    if ep is not None:
        eptarget = chr(ord('a')+ep[0][0]) + str(ep[0][1])
    return " ".join(toks) + " " + ("w" if stm == "W" else "b") + " " + eptarget

# Self-test passed against cylcgt on random positions
def self_test_passed(n=2000):
    random.seed(1)
    W, H = 8, 6
    wrap = True
    mism = 0
    for _ in range(n):
        # random pawns
        sqs = [(f, r) for f in range(W) for r in range(2, H)]
        random.shuffle(sqs)
        nw = random.randint(0, 4)
        nbp = random.randint(0, 4)
        ws = set(sqs[:nw])
        bs = set(sqs[nw:nw+nbp])
        # kings
        wk = (random.randrange(W), 1)
        bk = (random.randrange(W), H)
        ep = None
        pos = {"W": frozenset(ws), "B": frozenset(bs), "wk": wk, "bk": bk, "ep": ep}
        board, pp = cylcgt_pos(W, H, wrap, pos)
        for side in ("W", "B"):
            c1 = P.passed(board, pp, side)
            # our pawn_passed aggregate: true if any pawn of side passed
            mine = pos["W"] if side == "W" else pos["B"]
            c2 = any(pawn_passed(W, H, wrap, pos, side, sq) for sq in mine)
            if c1 != c2:
                mism += 1
                if mism <= 5:
                    print("MISMATCH", side, pos)
    print("self-test mismatches:", mism, "of", n)
    return mism

if __name__ == "__main__":
    self_test_passed()
