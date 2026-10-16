"""Independent re-check of claim C3 (engine workstream): race-rule accuracy
at depth-1 promotion-race nodes, and root-outcome accuracy on race-sensitive
positions.  Imports NOTHING from cylcgt/ or engine/: it reads the raw Lichess
JSON files on disk directly and uses its own FEN parser, its own pawn-move
generator, its own passed-pawn test, its own promotion distance and its own
minimax for the frozen-king pawn game.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python -I verify/engines/C3-refute/indep_race.py
"""
import collections
import functools
import glob
import json
import os
import sys

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
CACHES = [os.path.join(ROOT, "engine/suite/tbcache"), os.path.join(ROOT, "realchess/cache")]
FILES = "abcdefgh"
RULES = ("count", "mover", "opponent")


def parse_fen(fen):
    place, stm, _cast, ep = fen.split()[:4]
    board = {}
    for i, row in enumerate(place.split("/")):
        rank = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                board[(f, rank)] = ch
                f += 1
    epsq = None if ep == "-" else (FILES.index(ep[0]), int(ep[1]))
    return board, stm, epsq


def classify(board):
    """Return (trebuchet name, white q-side pawns, black q-side pawns) or None."""
    if any(f == 4 for f, _ in board):
        return None
    q = {s: p for s, p in board.items() if s[0] <= 3}
    k = {s: p for s, p in board.items() if s[0] >= 5}
    if any(p not in "Pp" for p in q.values()):
        return None
    if sorted(k.values()) != sorted("KPkp"):
        return None
    inv = {p: s for s, p in k.items()}
    P, p, K, kk = inv["P"], inv["p"], inv["K"], inv["k"]
    if not (P[0] == 6 and p == (6, P[1] + 1)):
        return None
    r = P[1]
    if K == (5, r + 1) and kk == (7, r):
        tname = f"A{r}"
    elif K == (7, r + 1) and kk == (5, r):
        tname = f"B{r}"
    else:
        return None
    W = frozenset(s for s, x in q.items() if x == "P")
    B = frozenset(s for s, x in q.items() if x == "p")
    return tname, W, B


def is_passed_pawn(sq, side, W, B):
    f, r = sq
    theirs = B if side == "W" else W
    for g, s in theirs:
        if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)):
            return False
    return True


def has_passer(side, W, B):
    mine = W if side == "W" else B
    return any(is_passed_pawn(s, side, W, B) for s in mine)


def distance(side, W, B):
    """Fewest moves for `side` to promote some passed pawn, ignoring the other side."""
    mine = W if side == "W" else B
    occ = W | B
    best = None
    for f, r in mine:
        if not is_passed_pawn((f, r), side, W, B):
            continue
        if side == "W":
            ahead = [(f, s) for s in range(r + 1, 9)]
            d = 8 - r
            if r == 2 and (f, 3) not in occ and (f, 4) not in occ:
                d -= 1
        else:
            ahead = [(f, s) for s in range(1, r)]
            d = r - 1
            if r == 7 and (f, 6) not in occ and (f, 5) not in occ:
                d -= 1
        if any(a in occ for a in ahead):
            continue  # own pawn in front on the same file
        best = d if best is None else min(best, d)
    return best


def apply_uci(uci, side, W, B, epsq):
    """Apply a q-side pawn move given in UCI; returns (W', B', ep_for_opponent)."""
    fr = (FILES.index(uci[0]), int(uci[1]))
    to = (FILES.index(uci[2]), int(uci[3]))
    mine, theirs = (set(W), set(B)) if side == "W" else (set(B), set(W))
    assert fr in mine, (uci, side)
    mine.discard(fr)
    if to in theirs:
        theirs.discard(to)
    elif fr[0] != to[0]:  # diagonal onto an empty square: must be e.p.
        assert epsq == to, (uci, epsq)
        cap = (to[0], fr[1])
        assert cap in theirs
        theirs.discard(cap)
    mine.add(to)
    newep = None
    if abs(to[1] - fr[1]) == 2:
        newep = (fr[0], (fr[1] + to[1]) // 2)
    if side == "W":
        return frozenset(mine), frozenset(theirs), newep
    return frozenset(theirs), frozenset(mine), newep


def gen_moves(side, W, B, epsq):
    """Own pawn-move generator on files a-d, 8 ranks (for the minimax)."""
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else 7
    out = []
    for f, r in sorted(mine):
        r1 = r + d
        if not 1 <= r1 <= 8:
            continue
        if (f, r1) not in occ:
            out.append(f"{FILES[f]}{r}{FILES[f]}{r1}")
            if r == start and (f, r + 2 * d) not in occ:
                out.append(f"{FILES[f]}{r}{FILES[f]}{r + 2 * d}")
        for g in (f - 1, f + 1):
            if 0 <= g <= 3 and ((g, r1) in theirs or epsq == (g, r1)):
                out.append(f"{FILES[f]}{r}{FILES[g]}{r1}")
    return out


def race_winner(rule, mover, W, B):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    dm, do = distance(mover, W, B), distance(other, W, B)
    return other if do <= dm else mover


def terminal(rule, mover, W, B):
    """Winner if the position after `mover`'s move is decided, else None."""
    wp, bp = has_passer("W", W, B), has_passer("B", W, B)
    if wp and bp:
        return race_winner(rule, mover, W, B)
    if wp:
        return "W"
    if bp:
        return "B"
    return None


@functools.lru_cache(maxsize=None)
def stm_wins(rule, side, W, B, epsq):
    for u in gen_moves(side, W, B, epsq):
        W2, B2, ep2 = apply_uci(u, side, W, B, epsq)
        t = terminal(rule, side, W2, B2)
        other = "B" if side == "W" else "W"
        if t is not None:
            if t == side:
                return True
            continue
        if not stm_wins(rule, other, W2, B2, ep2):
            return True
    return False  # no move, or every move loses (normal play)


def move_wins(rule, side, W, B, epsq, u):
    W2, B2, ep2 = apply_uci(u, side, W, B, epsq)
    t = terminal(rule, side, W2, B2)
    if t is not None:
        return t == side
    return not stm_wins(rule, "B" if side == "W" else "W", W2, B2, ep2)


MOVER = {"loss": "win", "blessed-loss": "win", "win": "loss", "cursed-win": "loss", "draw": "draw"}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "engine"
    caches = {"engine": CACHES[:1], "shared": CACHES[1:], "both": CACHES}[which]
    print(f"cache set: {which} -> {caches}")
    recs = {}
    for c in caches:
        for p in glob.glob(os.path.join(c, "*", "*.json")):
            d = json.load(open(p))
            if d.get("status") == 200 and d.get("data"):
                recs.setdefault(d["fen"], d)
    print(f"raw cached records with status 200: {len(recs)}")
    race_rows, root_rows = [], []
    nstruct = 0
    for fen, d in sorted(recs.items()):
        board, stm, epsq = parse_fen(fen)
        cl = classify(board)
        if cl is None:
            continue
        tname, W, B = cl
        if has_passer("W", W, B) or has_passer("B", W, B):
            continue
        nstruct += 1
        side = "W" if stm == "w" else "B"
        tbmoves = {m["uci"]: m["category"] for m in d["data"]["moves"]}
        pawn_uci = sorted(u for u in tbmoves if FILES.index(u[0]) <= 3)
        mine = gen_moves(side, W, B, epsq)
        # my generator must reproduce the tablebase's legal q-side pawn moves
        mine_n = sorted(u + ("q" if (u[3] == "8" and side == "W") or (u[3] == "1" and side == "B") else "")
                        for u in mine)
        assert mine_n == pawn_uci, (fen, mine_n, pawn_uci)
        # depth-1 race nodes
        for u in pawn_uci:
            W2, B2, _ = apply_uci(u[:4], side, W, B, epsq)
            if has_passer("W", W2, B2) and has_passer("B", W2, B2):
                other = "B" if side == "W" else "W"
                race_rows.append({"fen": fen, "treb": tname, "uci": u, "mover": side,
                                  "dm": distance(side, W2, B2), "do": distance(other, W2, B2),
                                  "tb": MOVER.get(tbmoves[u], tbmoves[u]),
                                  "W": " ".join(sorted(f"{FILES[f]}{r}" for f, r in W2)),
                                  "B": " ".join(sorted(f"{FILES[f]}{r}" for f, r in B2))})
        # root outcome under each rule
        wsets = {ru: frozenset(u for u in pawn_uci if move_wins(ru, side, W, B, epsq, u[:4]))
                 for ru in RULES}
        rsens = len(set(wsets.values())) > 1
        root_tb = d["data"]["category"]
        root_tb = "win" if root_tb in ("win", "cursed-win") else "loss" if root_tb in ("loss", "blessed-loss") else root_tb
        tbwin_pawn = frozenset(u for u in pawn_uci if MOVER.get(tbmoves[u]) == "win")
        root_rows.append({"fen": fen, "treb": tname, "stm": side, "rs": rsens, "tb_root": root_tb,
                          "pred_root": {ru: "win" if wsets[ru] else "loss" for ru in RULES},
                          "pawnset_ok": {ru: wsets[ru] == tbwin_pawn for ru in RULES}})
    print(f"records with trebuchet + q-side structure, no initial passer: {nstruct}")
    unk = [r for r in race_rows if r["tb"] not in ("win", "loss", "draw")]
    print(f"race nodes with unresolved tablebase category (dropped): {len(unk)}")
    race_rows = [r for r in race_rows if r["tb"] in ("win", "loss", "draw")]
    root_rows = [r for r in root_rows if r["tb_root"] in ("win", "loss", "draw")]

    # ---- depth-1 race nodes
    print(f"\ndepth-1 race nodes: {len(race_rows)}  (distinct (fen, move): "
          f"{len({(r['fen'], r['uci']) for r in race_rows})})")
    print("  by trebuchet:", dict(collections.Counter(r["treb"] for r in race_rows)))
    print("  tablebase result for the mover:", dict(collections.Counter(r["tb"] for r in race_rows)))
    for ru in RULES:
        ok = sum(("win" if race_winner(ru, r["mover"], *map(lambda s: frozenset(
            (FILES.index(t[0]), int(t[1:])) for t in s.split()), (r["W"], r["B"]))) == r["mover"] else "loss")
            == r["tb"] for r in race_rows)
        print(f"  rule {ru:9s} correct {ok}/{len(race_rows)}")
    print("  count-rule misses:")
    for r in race_rows:
        pred = "loss" if r["do"] <= r["dm"] else "win"
        if pred != r["tb"]:
            print(f"    {r['fen']}  {r['uci']} -> W: {r['W']} / B: {r['B']}  mover={r['mover']} "
                  f"d_mover={r['dm']} d_opp={r['do']} tb(mover)={r['tb']}")
    print("  by d_mover - d_opp:")
    by = collections.defaultdict(collections.Counter)
    for r in race_rows:
        by[r["dm"] - r["do"]][r["tb"]] += 1
    for k in sorted(by):
        print(f"    {k:+d}: {dict(by[k])}")

    # ---- root outcome on race-sensitive positions
    for tr in sorted({r["treb"] for r in root_rows if r["rs"]}):
        grp = [r for r in root_rows if r["rs"] and r["treb"] == tr]
        print(f"\nrace-sensitive positions at trebuchet {tr}: {len(grp)}; tb roots "
              f"{dict(collections.Counter(r['tb_root'] for r in grp))}")
        for ru in RULES:
            print(f"  {ru:9s} root agree {sum(r['pred_root'][ru] == r['tb_root'] for r in grp)}/{len(grp)}"
                  f"   pawn-move win set agree {sum(r['pawnset_ok'][ru] for r in grp)}/{len(grp)}")
    nrs = [r for r in root_rows if not r["rs"]]
    print(f"\nrace-insensitive positions: {len(nrs)}; count-rule root agree "
          f"{sum(r['pred_root']['count'] == r['tb_root'] for r in nrs)}/{len(nrs)}")
    json.dump({"race": race_rows, "root": root_rows},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"indep_race_out_{which}.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
