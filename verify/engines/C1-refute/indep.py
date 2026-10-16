"""Independent re-check of claim C1 (engine workstream), written from scratch.

Does NOT import cylcgt, crosscheck, realchess or engine/suite code.  It reads
  * engine/suite/results.json  only for the list of probed FENs, the tier label and
    the worker's canonical-form value string (used only to define "tame");
  * engine/suite/tbcache/**.json  raw Lichess responses (parsed here directly).

For every probed position it
  1. parses the FEN itself, checks the f-h files hold an A_r or B_r trebuchet and
     extracts the a-d queenside component;
  2. solves the component by plain minimax under the model (passed pawn = win,
     both passed = race by rule, no pawn move = loss, king move = loss);
  3. compares with the tablebase move categories.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python -I verify/engines/C1-refute/indep.py
"""
import collections
import functools
import glob
import json
import os
import sys

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
FILES = "abcdefgh"
NF = 4  # component files a-d, flat (e-file empty)
EPAWARE = "--ep-aware" in sys.argv


def sqn(f, r):
    return f"{FILES[f]}{r}"


def parse_fen(fen):
    parts = fen.split()
    board = {}
    for i, row in enumerate(parts[0].split("/")):
        r = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                board[(f, r)] = ch
                f += 1
    stm = parts[1]
    ep = None if parts[3] == "-" else (FILES.index(parts[3][0]), int(parts[3][1]))
    return board, stm, ep


# ----------------------------------------------------------------- model solver
def passed_side(W, B, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    for f, r in mine:
        ok = True
        for g, s in theirs:
            if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)):
                ok = False
                break
        if ok:
            return True
    return False


def dist(W, B, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    best = 10 ** 6
    for f, r in mine:
        if not passed_side(frozenset([(f, r)]), B, "W") if side == "W" else not passed_side(W, frozenset([(f, r)]), "B"):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, 9)):
                continue
            d = 8 - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == 7 else 0)
        best = min(best, d)
    return best


def gen(W, B, stm, ep):
    """Pawn moves of stm on files a-d: (uci, W', B', ep') ; ep is a target square usable by stm."""
    mine, theirs = (W, B) if stm == "W" else (B, W)
    occ = W | B
    d = 1 if stm == "W" else -1
    start = 2 if stm == "W" else 7
    out = []
    for (f, r) in sorted(mine):
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= 8:
            continue
        pr = "q" if r1 in (1, 8) else ""

        def emit(uci, nm, nt, nep=None):
            if stm == "W":
                out.append((uci, frozenset(nm), frozenset(nt), nep))
            else:
                out.append((uci, frozenset(nt), frozenset(nm), nep))
        if (f, r1) not in occ:
            emit(sqn(f, r) + sqn(f, r1) + pr, rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and (f, r2) not in occ:
                # e.p. right for the opponent only if an enemy pawn stands beside r2
                nep = None
                if any((g, r2) in theirs for g in (f - 1, f + 1) if 0 <= g < NF):
                    nep = (f, r1)
                emit(sqn(f, r) + sqn(f, r2), rest | {(f, r2)}, theirs, nep)
        for g in (f - 1, f + 1):
            if not 0 <= g < NF:
                continue
            t = (g, r1)
            if t in theirs:
                emit(sqn(f, r) + sqn(*t) + pr, rest | {t}, theirs - {t})
            elif ep is not None and ep == t:
                cap = (g, r)
                assert cap in theirs
                emit(sqn(f, r) + sqn(*t), rest | {t}, theirs - {cap})
    return out


OTHER = {"W": "B", "B": "W"}


@functools.lru_cache(maxsize=None)
def wins(W, B, stm, ep, rule, just_moved):
    """True iff stm wins (model) at this node.  just_moved = side that made the last move
    (None at the root)."""
    wp, bp = passed_side(W, B, "W"), passed_side(W, B, "B")
    term = None
    if wp and bp:
        assert just_moved is not None, "race at root"
        mover = just_moved
        if rule == "mover":
            winner = mover
        elif rule == "opponent":
            winner = OTHER[mover]
        else:
            o = OTHER[mover]
            winner = o if dist(W, B, o) <= dist(W, B, mover) else mover
        term = (winner == stm)
    elif wp or bp:
        term = ((wp and stm == "W") or (bp and stm == "B"))
    if term is not None:
        if EPAWARE and ep is not None and not term:
            # stm may still capture en passant before the "passed" pawn runs
            for uci, W2, B2, ep2 in gen(W, B, stm, ep):
                if uci[2:4] == sqn(*ep) and uci[0] != uci[2]:
                    if not wins(W2, B2, OTHER[stm], None, rule, stm):
                        return True
        return term
    kids = gen(W, B, stm, ep)
    if not kids:
        return False  # must move the king: drops the g-pawn
    return any(not wins(W2, B2, OTHER[stm], ep2, rule, stm) for _, W2, B2, ep2 in kids)


def predict(W, B, stm, ep, rule):
    """{uci: True if that pawn move wins for stm}"""
    return {uci: not wins(W2, B2, OTHER[stm], ep2, rule, stm) for uci, W2, B2, ep2 in gen(W, B, stm, ep)}


# ----------------------------------------------------------------- tablebase
FLIP = {"loss": "win", "blessed-loss": "cursed-win", "draw": "draw", "win": "loss",
        "cursed-win": "blessed-loss"}


def load_cache():
    out = {}
    for p in glob.glob(os.path.join(ROOT, "engine/suite/tbcache/*/*.json")):
        rec = json.load(open(p))
        out[rec["fen"]] = rec
    return out


def treb_kind(board):
    """Return 'A<r>' / 'B<r>' if files e-h hold exactly a trebuchet, else None."""
    k = {(f, r): p for (f, r), p in board.items() if f >= 4}
    for r in range(2, 7):
        A = {(6, r): "P", (6, r + 1): "p", (5, r + 1): "K", (7, r): "k"}
        Bt = {(6, r): "P", (6, r + 1): "p", (7, r + 1): "K", (5, r): "k"}
        if k == A:
            return f"A{r}"
        if k == Bt:
            return f"B{r}"
    return None


def main():
    rows = json.load(open(os.path.join(ROOT, "engine/suite/results.json")))
    cache = load_cache()
    out = []
    for row in rows:
        fen = row["fen"]
        key = " ".join(fen.split()[:4]) + " 0 1"
        rec = cache.get(key)
        if rec is None:
            # normalised key may have dropped the ep square
            p = fen.split()
            rec = cache.get(" ".join(p[:3] + ["-"]) + " 0 1")
        assert rec is not None and rec["status"] == 200, fen
        data = rec["data"]
        board, stm, ep = parse_fen(fen)
        tk = treb_kind(board)
        assert tk == row["treb"], (fen, tk, row["treb"])
        W = frozenset(s for s, p in board.items() if p == "P" and s[0] < 4)
        B = frozenset(s for s, p in board.items() if p == "p" and s[0] < 4)
        side = "W" if stm == "w" else "B"
        assert not passed_side(W, B, "W") and not passed_side(W, B, "B"), fen
        preds = {rule: predict(W, B, side, ep, rule) for rule in ("count", "mover", "opponent")}
        kingsq = [s for s, p in board.items() if p == ("K" if side == "W" else "k")][0]
        tbm = {m["uci"]: FLIP[m["category"]] for m in data["moves"]}
        king_moves = {u for u in tbm if u[:2] == sqn(*kingsq)}
        pawn_moves = set(tbm) - king_moves
        assert pawn_moves == set(preds["count"]), (fen, pawn_moves ^ set(preds["count"]))
        # independent legality check of king moves (no other piece types exist)
        out.append(dict(id=row["id"], tier=row["tier"], fen=fen, treb=tk, stm=side,
                        value=row["value"]["count"], tb_root=data["category"], tbm=tbm,
                        king_moves=sorted(king_moves), pawn_moves=sorted(pawn_moves), preds=preds,
                        wv=row["rules"]["count"]["pred_win"]))
    return out


def analyse(out):
    def tame(v):
        return "W" not in v

    def rs(o):
        s = {r: frozenset(u for u, w in o["preds"][r].items() if w) for r in o["preds"]}
        return len(set(s.values())) > 1

    # sanity: does my minimax reproduce the worker's cylcgt predictions?
    mism = [o["id"] for o in out if sorted(u for u, w in o["preds"]["count"].items() if w) != sorted(o["wv"])]
    print("positions:", len(out), "| my count-rule win set != worker pred_win:", mism)
    cats = collections.Counter(c for o in out for c in o["tbm"].values())
    print("mover-result categories over all moves of all 275 positions:", dict(cats))
    grp = [o for o in out if tame(o["value"]) and not rs(o) and o["treb"].startswith("A")]
    print("\nGROUP tame & race-insensitive (my minimax) & A-trebuchet:", len(grp),
          dict(collections.Counter(o["treb"] for o in grp)), dict(collections.Counter(o["tier"] for o in grp)))
    print("  stm:", dict(collections.Counter(o["stm"] for o in grp)))
    WIN = {"win", "cursed-win"}
    for rule in ("count", "mover", "opponent"):
        root = pawnset = full = exact = 0
        misses, fullmiss, emptyboth = [], [], 0
        pawn_loss_but_draw = 0
        pawn_loss_total = 0
        for o in grp:
            p = o["preds"][rule]
            pw = {u for u, w in p.items() if w}
            tbw = {u for u, c in o["tbm"].items() if c in WIN}
            tbroot = "win" if o["tb_root"] in WIN else ("loss" if o["tb_root"] in ("loss", "blessed-loss") else o["tb_root"])
            pr = "win" if pw else "loss"
            root += pr == tbroot
            if pr != tbroot:
                misses.append((o["id"], o["fen"], "pred", pr, "tb", o["tb_root"],
                               {u: c for u, c in o["tbm"].items() if c != "loss"}))
            ps = pw == (tbw & set(o["pawn_moves"]))
            pawnset += ps
            if not pw and not (tbw & set(o["pawn_moves"])):
                emptyboth += 1
            fs = pw == tbw
            full += fs
            if not fs:
                fullmiss.append((o["id"], o["fen"], sorted(tbw - pw), sorted(pw - tbw)))
            ex = all(((c in WIN) == (u in pw)) and c in WIN | {"loss", "blessed-loss"} for u, c in o["tbm"].items())
            exact += ex
            for u in o["pawn_moves"]:
                if u not in pw:
                    pawn_loss_total += 1
                    pawn_loss_but_draw += o["tbm"][u] == "draw"
        n = len(grp)
        print(f"  [{rule}] root {root}/{n}  pawn-win-set {pawnset}/{n} (both empty in {emptyboth})"
              f"  full-win-set {full}/{n}  every-move-exact {exact}/{n}")
        print(f"     pawn moves predicted to lose: {pawn_loss_total}, of which TB draw: {pawn_loss_but_draw}")
        if rule == "count":
            for m in misses:
                print("     ROOT MISS", m)
            for m in fullmiss:
                print("     FULL-SET MISS", m)
    tbroots = collections.Counter(o["tb_root"] for o in grp)
    print("  TB roots in group:", dict(tbroots))
    predw = sum(any(o["preds"]["count"].values()) for o in grp)
    print("  CGT predicts stm wins in", predw, "of", len(grp))
    return grp


if __name__ == "__main__":
    print("ep-aware variant:", EPAWARE)
    analyse(main())
