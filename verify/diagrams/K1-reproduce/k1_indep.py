"""K1 (REPRODUCE lens), second independent check, written without reusing rerun.py's code.

Squares are (file 0..7, rank 1..8).  wrap=True: files a and h adjacent.
Checks, for the full 7.2 diagram and for the isolated d/e group, on cylinder and flat:
  * complete legal-move lists (king + pawn moves, incl. double steps and captures),
  * that neither d7 nor e7 can move,
  * what each king move allows (enemy king captures),
  * after ...Kc7 Kxe7 that Black cannot stop d8=Q (nor win the new queen),
  * a tiny minimax of the isolated group under the paper's convention
    (first pawn capture = win for the capturer; promotion that survives = win).
Run:  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/K1-reproduce/k1_indep.py
"""
from functools import lru_cache

F = "abcdefgh"


def sq(s):
    return F[s[0]] + str(s[1])


def parse(board_fen):
    d = {}
    for i, row in enumerate(board_fen.split("/")):
        r, f = 8 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                d[(f, r)] = ch
                f += 1
    return d


def adj(s, wrap):
    f, r = s
    out = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df or dr:
                nf, nr = f + df, r + dr
                if wrap:
                    nf %= 8
                if 0 <= nf < 8 and 1 <= nr <= 8:
                    out.append((nf, nr))
    return out


def pawn_caps(s, white, wrap):
    f, r = s
    nr = r + (1 if white else -1)
    out = []
    for nf in (f - 1, f + 1):
        if wrap:
            nf %= 8
        if 0 <= nf < 8 and 1 <= nr <= 8:
            out.append((nf, nr))
    return out


def attacked_by(pcs, white, wrap):
    a = set()
    for s, c in pcs.items():
        if c == ("K" if white else "k"):
            a.update(adj(s, wrap))
        elif c == ("P" if white else "p"):
            a.update(pawn_caps(s, white, wrap))
    return a


def is_white(c):
    return c.isupper()


def legal(pcs, white, wrap):
    """List of (description, new_pcs). No e.p. needed here (no double step lands beside an enemy pawn
    that could take it e.p. in these positions; e.p. is checked separately below)."""
    res = []
    for s, c in list(pcs.items()):
        if is_white(c) != white:
            continue
        cand = []
        if c in "Kk":
            for t in adj(s, wrap):
                if t in pcs and is_white(pcs[t]) == white:
                    continue
                cand.append(t)
        else:
            dr = 1 if white else -1
            one = (s[0], s[1] + dr)
            if one not in pcs and 1 <= one[1] <= 8:
                cand.append(one)
                two = (s[0], s[1] + 2 * dr)
                if s[1] == (2 if white else 7) and two not in pcs:
                    cand.append(two)
            for t in pawn_caps(s, white, wrap):
                if t in pcs and is_white(pcs[t]) != white:
                    cand.append(t)
        for t in cand:
            new = dict(pcs)
            del new[s]
            cap = new.pop(t, None)
            piece = c
            promo = c in "Pp" and t[1] in (1, 8)
            if promo:
                piece = "Q" if white else "q"
            new[t] = piece
            k = next(x for x, y in new.items() if y == ("K" if white else "k"))
            if k in attacked_by(new, not white, wrap):
                continue
            name = ("K" if c in "Kk" else "") + sq(s) + ("x" if cap else "-") + sq(t) + ("=Q" if promo else "")
            res.append((name, new, cap))
    return res


def show(label, fen, wrap):
    pcs = parse(fen)
    print(f"\n### {label} [{'cylinder' if wrap else 'flat'}] {fen}")
    for white in (True, False):
        mv = legal(pcs, white, wrap)
        print(f"  {'W' if white else 'B'} legal ({len(mv)}): {', '.join(m for m, _, _ in mv)}")
        for m, new, _ in mv:
            if m.startswith("K") and m[1:3] in ("e6", "d8"):
                caps = [m2 for m2, _, c2 in legal(new, not white, wrap) if c2]
                print(f"     {m}: enemy replies that capture: {caps}")
        for p in (("d", 7),):
            pass
    pawn_moves = [m for w in (True, False) for m, _, _ in legal(pcs, w, wrap) if m[:2] in ("d7", "e7")]
    print(f"  moves by the d7/e7 pawns: {pawn_moves or 'none'}")


def kc7_line(fen, wrap):
    pcs = parse(fen)
    after_kc7 = dict(next(n for m, n, _ in legal(pcs, False, wrap) if m == "Kd8-c7"))
    kxe7 = [n for m, n, _ in legal(after_kc7, True, wrap) if m == "Ke6xe7"]
    print(f"  [{'cyl' if wrap else 'flat'}] after ...Kc7: Kxe7 legal = {bool(kxe7)};"
          f" d8=Q at once legal = {any(m == 'd7-d8=Q' for m, _, _ in legal(after_kc7, True, wrap))}"
          f" but then B can take it: {any(c == 'Q' for m, n, c in [(m2, n2, c2) for m2, n2, c2 in legal(next(n for m, n, _ in legal(after_kc7, True, wrap) if m == 'd7-d8=Q'), False, wrap)])}")
    pos = kxe7[0]
    worst = []
    for m, n, c in legal(pos, False, wrap):
        if c == "P":
            worst.append(m + " (takes d7!)")
            continue
        q = [n2 for m2, n2, _ in legal(n, True, wrap) if m2 == "d7-d8=Q"]
        if not q:
            worst.append(m + " (stops d8=Q)")
            continue
        if any(c2 == "Q" for _, _, c2 in legal(q[0], False, wrap)):
            worst.append(m + " (wins the queen)")
    print(f"     Black replies after Kc7 Kxe7: {[m for m, _, _ in legal(pos, False, wrap)]}; refutations: {worst or 'NONE'}")


def convention_minimax(fen, wrap, depth_cap=12):
    """Isolated group, paper's convention: the first pawn capture or surviving promotion decides.
    Returns +1 (side to move wins), -1, or 0 (no decision within depth_cap plies)."""
    start = parse(fen)

    @lru_cache(maxsize=None)
    def solve(key, white, depth):
        pcs = dict(key)
        mv = legal(pcs, white, wrap)
        if not mv:
            return -1  # normal play (isolated group): no move loses
        if depth == 0:
            return 0
        best = -1
        for m, n, c in mv:
            if c in ("P", "p", "Q", "q"):
                v = 1  # capturer wins by convention
            elif "=Q" in m:
                # promotion survives unless the enemy king can take the queen at once
                taken = any(c2 in ("Q", "q") for _, _, c2 in legal(n, not white, wrap))
                v = 1 if not taken else -solve(tuple(sorted(n.items())), not white, depth - 1)
            else:
                v = -solve(tuple(sorted(n.items())), not white, depth - 1)
            best = max(best, v)
            if best == 1:
                break
        return best

    key = tuple(sorted(start.items()))
    return {("W" if w else "B") + " to move": solve(key, w, depth_cap) for w in (True, False)}


if __name__ == "__main__":
    FULL = "3k4/1p1Pp2p/p3K3/8/8/7P/PP6/8"
    GROUP = "3k4/3Pp3/4K3/8/8/8/8/8"
    for wrap in (True, False):
        show("7.2 full diagram", FULL, wrap)
        show("7.2 isolated d/e group", GROUP, wrap)
    print("\n### Kc7 follow-up")
    for wrap in (True, False):
        kc7_line(GROUP, wrap)
        kc7_line(FULL, wrap)
    print("\n### Isolated group under the paper's convention (+1 = side to move wins, -1 = loses)")
    for wrap in (True, False):
        print(f"  [{'cyl' if wrap else 'flat'}]", convention_minimax(GROUP, wrap))
    # cross-check legal lists against realchess.movegen (separate implementation, flat board only)
    try:
        from realchess import movegen
        print("\n### flat cross-check vs realchess.movegen.legal_uci")
        for fen in (FULL, GROUP):
            for stm in "wb":
                ref = sorted(movegen.legal_uci(f"{fen} {stm} - - 0 1"))
                mine = sorted(m.replace("K", "").replace("x", "").replace("-", "").replace("=Q", "q")
                              for m, _, _ in legal(parse(fen), stm == "w", False))
                print(f"  {fen} {stm}: movegen {ref}\n      mine == movegen: {mine == ref}")
    except Exception as e:  # pragma: no cover
        print("movegen cross-check failed:", repr(e))
