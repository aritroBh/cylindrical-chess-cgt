#!/usr/bin/env python3
"""Small independent checks for K11; no K10 files or code are imported."""
from collections import deque

from cylcgt import cgt, pawns
from lemmas.common import W

BOARD = pawns.Board(8, 6, True, True)
WID, H = BOARD.files, BOARD.ranks


def orient(square, beta):
    f, r = square
    return f, r if beta == "W" else H + 1 - r


def coords(squares, beta):
    return frozenset(orient(s, beta) for s in squares)


def mu_omega(pos, beta, stm, wk, bk):
    """Shortest omega-only promotion distance, with static kings and beta pawns."""
    omega = "B" if beta == "W" else "W"
    op = coords(pos.black if omega == "B" else pos.white, beta)
    bp = coords(pos.white if beta == "W" else pos.black, beta)
    kings = frozenset((orient(wk, beta), orient(bk, beta)))
    ep_t = ep_c = None
    if stm == omega and pos.ep:
        ep_t, ep_c, entitled = pos.ep
        if entitled == omega:
            ep_t, ep_c = orient(ep_t, beta), orient(ep_c, beta)
        else:
            ep_t = ep_c = None
    start = (op, bp, ep_t, ep_c)
    q = deque([(start, 0)])
    seen = {start}
    while q:
        (own, theirs, target, victim), depth = q.popleft()
        occ = own | theirs | kings
        for f, r in own:
            candidates = []
            one = (f, r - 1)
            if one[1] >= 1 and one not in occ:
                candidates.append((one, None))
            two = (f, r - 2)
            if r == H - 1 and one not in occ and two[1] >= 1 and two not in occ:
                candidates.append((two, None))
            for df in (-1, 1):
                t = ((f + df) % WID, r - 1)
                if t[1] < 1:
                    continue
                if t in theirs:
                    candidates.append((t, t))
                elif target == t and victim in theirs:
                    candidates.append((t, victim))
            for t, captured in candidates:
                if t[1] == 1:
                    return depth + 1
                next_own = (own - { (f, r) }) | {t}
                next_theirs = theirs - ({captured} if captured else set())
                nxt = (frozenset(next_own), frozenset(next_theirs), None, None)
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, depth + 1))
    return 10**6


def certificate(pos, beta, stm, pawn, wk, bk):
    omega = "B" if beta == "W" else "W"
    p = orient(pawn, beta)
    mine = coords(pos.white if beta == "W" else pos.black, beta)
    theirs = coords(pos.black if beta == "W" else pos.white, beta)
    ep = None
    if pos.ep:
        t, c, side = pos.ep
        ep = (orient(t, beta), orient(c, beta), side)
    # H1: passed in the adopted e.p.-aware test, with an unobstructed file.
    passed = pawns.passed(BOARD, pos, beta)
    ep_hits_p = bool(ep and ep[1] == p and ep[2] != beta and
                     any(((p[0] + df) % WID, p[1]) in theirs for df in (-1, 1)))
    occupied = mine | theirs | {orient(wk, beta), orient(bk, beta)}
    clear = not any((p[0], r) in occupied for r in range(p[1] + 1, H + 1))
    h1 = passed and not ep_hits_p and clear

    # H2: the two files beside beta's king are pawn-free.
    beta_k = orient(wk if beta == "W" else bk, beta)
    omega_k = orient(wk if omega == "W" else bk, beta)
    pawn_files = {f for f, _ in mine | theirs}
    h2 = all((beta_k[0] + df) % WID not in pawn_files for df in (-1, 1))

    # H3: find omega king's permanently safe neighboring square.
    pawns_on = mine | theirs
    def king_distance(a, b):
        fd = min((a[0] - b[0]) % WID, (b[0] - a[0]) % WID)
        return max(fd, abs(a[1] - b[1]))
    h3 = False
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if not (df or dr):
                continue
            t = ((omega_k[0] + df) % WID, omega_k[1] + dr)
            if not 1 <= t[1] <= H or king_distance(t, beta_k) < 2:
                continue
            files = {(t[0] + x) % WID for x in (-1, 0, 1)}
            if not any(f in files for f, _ in pawns_on):
                h3 = True

    # H4: friendly pawns beside p are not more than one rho-step ahead.
    h4 = all(r <= p[1] + 1 for f, r in mine if f in {
        (p[0] - 1) % WID, (p[0] + 1) % WID
    })
    d = H - p[1] - (p[1] == 2)
    e = d if stm == omega else d - 1
    mu = mu_omega(pos, beta, stm, wk, bk)
    h5 = mu >= e + 1
    return {"H1": h1, "H2": h2, "H3": h3, "H4": h4, "H5": h5,
            "d": d, "e": e, "mu": mu}


def root_count_winner(pos, stm):
    """Explicit extension: the current side is first in a race already at root."""
    dw = pawns.promote_distance(BOARD, pos, "W")
    db = pawns.promote_distance(BOARD, pos, "B")
    winner = "W" if dw < db else "B" if db < dw else stm
    return dw, db, winner


def main():
    assert pawns.PASSED_RESPECTS_EP is True
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    # A root single-passer certificate with an unrelated usable e.p. capture.
    ep_root = pawns.Pos(frozenset({(2, 4), (4, 3), (6, 4)}), frozenset({(3, 4)}),
                        ((2, 3), (2, 4), "B"))
    cert = certificate(ep_root, "W", "B", (6, 4), (0, 1), (0, 6))
    assert all(cert[f"H{i}"] for i in range(1, 6)), cert
    assert cert["d"] == 2 and cert["e"] == 2 and cert["mu"] == 3, cert
    assert pawns.passed(BOARD, ep_root, "W") and not pawns.passed(BOARD, ep_root, "B")
    assert cgt.outcome(pawns.value(BOARD, ep_root)) == "L"
    comps = pawns.components(BOARD, ep_root)
    assert len(comps) == 2
    assert any((2, 3) in child.black and (2, 4) not in child.white
               for child in pawns.moves(BOARD, ep_root, "B"))
    print("single passer + initial e.p.:", cert,
          "components=2, usable e.p. (E fails at root), W(X)=White win")

    single_for_mover = pawns.Pos(frozenset({(3, 4)}), frozenset())
    assert cgt.outcome(pawns._child(BOARD, single_for_mover, "W")) == "L"
    single_for_next = pawns.Pos(frozenset({(2, 4), (4, 3)}), frozenset({(3, 4)}))
    assert pawns.passed(BOARD, single_for_next, "W")
    assert not pawns.passed(BOARD, single_for_next, "B")
    assert cgt.outcome(pawns._child(BOARD, single_for_next, "B")) == "L"
    print("single passer children: mover White credited White; mover Black credited next White")

    # Race terminals made by either mover: count gives the next mover a tie,
    # and the certificate has e=d or d-1 according to who owns the win.
    race_white = pawns.Pos(frozenset({(2, 3), (3, 4)}), frozenset({(5, 4)}))
    d_w = pawns.promote_distance(BOARD, race_white, "W")
    d_b = pawns.promote_distance(BOARD, race_white, "B")
    mu_b = mu_omega(race_white, "W", "B", (0, 1), (0, 6))
    assert (d_w, d_b, mu_b) == (2, 3, 3)
    assert cgt.outcome(pawns._child(BOARD, race_white, "W")) == "L"
    print("race after White move: dp=(2,3), beta=White=mover, d/e/mu=(2/2/3), W wins")

    race_black = pawns.Pos(frozenset({(2, 4)}), frozenset({(3, 4)}))
    d_w = pawns.promote_distance(BOARD, race_black, "W")
    d_b = pawns.promote_distance(BOARD, race_black, "B")
    mu_b = mu_omega(race_black, "W", "W", (0, 1), (0, 6))
    assert (d_w, d_b, mu_b) == (2, 3, 3)
    assert cgt.outcome(pawns._child(BOARD, race_black, "B")) == "L"
    print("race after Black move: dp=(2,3), beta=White=next, d/e/mu=(2/1/3), W wins")

    for text, stm in (("W: c4 / B: f4", "W"), ("W: c4 / B: f4", "B"),
                      ("W: c4 / B: f2", "W"), ("W: c4 / B: f2", "B")):
        pos = pawns.Pos.parse(text)
        assert pawns.passed(BOARD, pos, "W") and pawns.passed(BOARD, pos, "B")
        dw, db, winner = root_count_winner(pos, stm)
        try:
            W(BOARD, pos)
        except pawns.RaceError:
            api = "W=RaceError"
        else:
            raise AssertionError("whole-board W unexpectedly accepted a root race")
        print(f"root race stm={stm} dp(W/B)=({dw}/{db}) count-extension={winner}; "
              f"{api}, S={cgt.outcome(pawns.value(BOARD, pos))}")

    # A non-race root with one passer has a defined whole-board W value.
    single = pawns.Pos(frozenset({(2, 4), (4, 3)}), frozenset({(5, 4)}))
    assert pawns.passed(BOARD, single, "W") and not pawns.passed(BOARD, single, "B")
    print("single-passer W outcome:", cgt.outcome(W(BOARD, single)))

    check_root = pawns.Pos(frozenset({(2, 4), (5, 2)}), frozenset({(5, 3)}))
    assert pawns.passed(BOARD, check_root, "W") and not pawns.passed(BOARD, check_root, "B")
    print("outside-layout check-root convention:", cgt.outcome(W(BOARD, check_root)))

    uncertified = pawns.Pos(frozenset({(2, 4), (4, 2)}), frozenset({(5, 3)}))
    miss = certificate(uncertified, "W", "B", (2, 4), (0, 1), (0, 6))
    assert miss["H1"] and miss["H2"] and miss["H3"] and miss["H4"]
    assert miss["mu"] == 2 and miss["e"] == 2 and not miss["H5"]
    assert pawns.passed(BOARD, uncertified, "W")
    assert not pawns.passed(BOARD, uncertified, "B")
    assert cgt.outcome(W(BOARD, uncertified)) == "L"
    print("uncertified P11 root:", miss, "W(X)=White wins")


if __name__ == "__main__":
    main()
