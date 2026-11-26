"""K68: mechanical test of White's strategy S_A of PROOF.md (Lemmas A1-A3), written on python-chess,
independently of the oracle o68.cpp.

For every starting position of PROOF.md section 3 (White to move) it plays White's strategy exactly as written in
the proof against every Black reply (and, in the token mode, every use of Black's one move elsewhere), and checks:
  - every White move prescribed by S_A is legal;
  - Black never promotes and is never stalemated (Black always has a legal board move);
  - White promotes on the b-file, at the latest on White's move 8 (P) or 9 (beside -1);
  - the side facts used in the proof: the Black king never stands on rank 7 or 8 before White takes on b7,
    Black takes on c5 no earlier than its 3rd turn, and at the promotion b8 is not attacked by the Black king
    unless the White king guards it; the Black c-pawn's rank at the promotion (for the chess reading).
Run: .venv/bin/python kings/delegate/out/K68/src/check_lemmaA.py   (a few seconds)
"""
import sys
import chess

sq = chess.parse_square

STARTS = []
# (O1): positions after the six bad Black root moves; White Kd4, Pb6, Pc5, Pc2, Black pb7, pc6.
for k in ["a3", "a4", "a5", "a6"]:
    STARTS.append(("O1 bad move to " + k, k, "c2"))
# (O3): q1 = after c2-c4 at the b4 root, Black to move: ...Ka3, Ka4, Ka5, Kb3.
for k in ["a3", "a4", "a5", "b3"]:
    STARTS.append(("O3 q1 ...K" + k, k, "c4"))
# (O3): q2 = after c2-c3 at the b5 root, Black to move: ...Ka4, Ka5, Ka6.
for k in ["a4", "a5", "a6"]:
    STARTS.append(("O3 q2 ...K" + k, k, "c3"))


def board_of(bk, gamma):
    b = chess.Board(None)
    b.set_piece_at(sq("d4"), chess.Piece(chess.KING, chess.WHITE))
    b.set_piece_at(sq(bk), chess.Piece(chess.KING, chess.BLACK))
    for s in ["b6", "c5", gamma]:
        b.set_piece_at(sq(s), chess.Piece(chess.PAWN, chess.WHITE))
    for s in ["b7", "c6"]:
        b.set_piece_at(sq(s), chess.Piece(chess.PAWN, chess.BLACK))
    b.turn = chess.WHITE
    assert b.is_valid(), b.fen()
    return b


def kadj(a, b):
    return a != b and chess.square_distance(a, b) == 1


def white_move(b):
    """S_A exactly as written in PROOF.md section 3."""
    wk, bk = b.king(chess.WHITE), b.king(chess.BLACK)
    wp = b.pieces(chess.PAWN, chess.WHITE)
    bp = b.pieces(chess.PAWN, chess.BLACK)
    if sq("b7") in wp:
        return chess.Move(sq("b7"), sq("b8"), promotion=chess.QUEEN)
    if sq("b7") not in bp:  # b7 has been taken
        if wk == sq("b7"):
            to = sq("c7") if not kadj(sq("c7"), bk) else sq("a7")
            return chess.Move(wk, to)
        return chess.Move(sq("b6"), sq("b7"))
    route = {sq("d4"): sq("e5"), sq("e5"): sq("d6"), sq("d6"): sq("c7")}
    if wk in route:
        return chess.Move(wk, route[wk])
    if wk == sq("c7"):
        return chess.Move(wk, sq("b8")) if kadj(bk, sq("b7")) else chess.Move(wk, sq("b7"))
    if wk == sq("b8"):
        return chess.Move(wk, sq("c7")) if kadj(bk, sq("b7")) else chess.Move(wk, sq("b7"))
    raise RuntimeError("no rule for " + b.fen())


stats = {}


def explore(b, tok, wmoves, bturns, took_b7, memo, path):
    """White to move.  Returns the largest number of White moves needed (over Black's choices)."""
    key = (b.board_fen(), tok, took_b7, bturns)
    if key in memo:
        return memo[key]
    m = white_move(b)
    if m not in b.legal_moves:
        raise AssertionError("illegal S_A move %s at %s via %s" % (m, b.fen(), path))
    wmoves += 1
    if m.promotion:
        if m.from_square != sq("b7"):
            raise AssertionError("promotion not on b8")
        bk = b.king(chess.BLACK)
        guarded = kadj(b.king(chess.WHITE), sq("b8"))
        if kadj(bk, sq("b8")) and not guarded:
            raise AssertionError("b8 attacked and not guarded at " + b.fen())
        # chess reading: after b8=Q Black is not stalemated and cannot take the queen
        bq = b.copy(stack=False)
        bq.push(m)
        if not any(True for _ in bq.legal_moves):
            raise AssertionError("Black stalemated or mated after b8=Q at " + bq.fen())
        if any(r.to_square == sq("b8") for r in bq.legal_moves):
            raise AssertionError("Black can take the new queen at " + bq.fen())
        stats.setdefault("black king rank at promotion", set()).add(chess.square_rank(b.king(chess.BLACK)) + 1)
        cp = [chess.square_rank(s) + 1 for s in b.pieces(chess.PAWN, chess.BLACK)]
        stats.setdefault("black pawn ranks at promotion", set()).update(cp or [0])
        stats.setdefault("white moves", set()).add(wmoves)
        memo[key] = wmoves
        return wmoves
    if m.to_square == sq("b7") and b.piece_at(sq("b7")) is not None:
        took_b7 = True
        if chess.square_rank(b.king(chess.BLACK)) > 4:
            raise AssertionError("Black king above rank 5 when White takes on b7: " + b.fen())
    b2 = b.copy(stack=False)
    b2.push(m)
    worst = wmoves
    replies = list(b2.legal_moves)
    if not replies:
        raise AssertionError("Black stalemated/mated (no board move) at " + b2.fen())
    # Lemma A2 of PROOF.md: the Black king can step to the rank below (on the first rank: along it)
    bk = b2.king(chess.BLACK)
    r0 = chess.square_rank(bk)
    want = r0 - 1 if r0 > 0 else 0
    if not any(r.from_square == bk and chess.square_rank(r.to_square) == want for r in replies):
        raise AssertionError("Lemma A2 fails at " + b2.fen())
    for r in replies:
        if r.promotion:
            raise AssertionError("Black promotes at " + b2.fen())
        b3 = b2.copy(stack=False)
        cap_c5 = r.to_square == sq("c5") and b2.piece_at(sq("c5")) is not None
        b3.push(r)
        if cap_c5 and bturns + 1 < 3:
            raise AssertionError("Black took c5 on turn %d" % (bturns + 1))
        if not took_b7 and chess.square_rank(b3.king(chess.BLACK)) >= 6:
            raise AssertionError("Black king on rank 7/8 before Kxb7: " + b3.fen())
        worst = max(worst, explore(b3, tok, wmoves, bturns + 1, took_b7, memo, path + [r.uci()]))
    if tok and not b2.is_check():
        b3 = b2.copy(stack=False)
        b3.push(chess.Move.null())
        worst = max(worst, explore(b3, tok - 1, wmoves, bturns + 1, took_b7, memo, path + ["pass"]))
    memo[key] = worst
    return worst


def main():
    ok = True
    for tok, bound in [(0, 8), (1, 9)]:
        for name, bk, gamma in STARTS:
            if tok and not name.startswith("O1"):
                continue  # (B1) is asked only after the bad root moves
            b = board_of(bk, gamma)
            try:
                w = explore(b, tok, 0, 0, False, {}, [])
                flag = "ok" if w <= bound else "TOO SLOW"
                ok &= w <= bound
            except AssertionError as e:
                flag, w, ok = "FAIL: %s" % e, -1, False
            print("%-6s %-22s gamma=%s  White promotes by move %2d (bound %d)  %s"
                  % ("P" if tok == 0 else "beside-1", name, gamma, w, bound, flag))
    print("Black pawn ranks seen at the promotion (0 = none left):", sorted(stats.get("black pawn ranks at promotion", [])))
    print("Black king ranks seen at the promotion:", sorted(stats.get("black king rank at promotion", [])))
    print("ALL OK" if ok else "SOME FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
