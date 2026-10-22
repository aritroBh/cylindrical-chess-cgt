#!/usr/bin/env python3
"""Enumerate every legal KPK position on a flat, cylinder or Mobius board (kings/SPEC.md rules).

Usage (from the project root):
    .venv/bin/python research/mobius/gen_kpk_positions.py --board mob:8x8 > positions.txt

Board kinds:
    flat:WxH  ordinary board
    cyl:WxH   file a glued straight to the last file (kings/SPEC.md)
    mob:WxH   file seam glued with a half twist: square (last file, r) ~ (a, H-1-r), 0-based,
              as in research/mobius/RULES.md section 1.1 and 5.

Legality (SPEC.md): distinct squares; kings not adjacent (adjacency uses the board's own step,
including the seam); the pawn is not on rank 1 or rank H; the side not to move is not in check.
With one White pawn and no Black pawn the only possible check on the side not to move is a
White pawn attacking the Black king. En passant is always '-' (Black has no pawn).
"""
import argparse
import sys

FILES = "abcdefgh"


def make_step(W, H, kind):
    """Return step(s, df, dr) -> square index or None, for the given topology."""

    def step(s, df, dr):
        f = s % W + df
        r = s // W + dr
        if not 0 <= r < H:
            return None
        if kind == "cyl":
            f %= W
        elif kind == "mob":
            if not 0 <= f < W:
                f %= W
                r = H - 1 - r
        elif not 0 <= f < W:
            return None
        return r * W + f

    return step


def sq_name(s, W):
    return "%s%d" % (FILES[s % W], s // W + 1)


def positions(W, H, kind):
    step = make_step(W, H, kind)
    N = W * H
    king_adj = {}
    for s in range(N):
        adj = set()
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                t = step(s, df, dr)
                if t is not None and t != s:
                    adj.add(t)
        king_adj[s] = adj
    # pawn_targets[p]: squares a White pawn on p attacks (diagonally forward, with the board's wrap)
    pawn_targets = {}
    for p in range(N):
        tg = set()
        for df in (-1, 1):
            t = step(p, df, 1)
            if t is not None and t != p:
                tg.add(t)
        pawn_targets[p] = tg
    for wk in range(N):
        for bk in range(N):
            if bk == wk or bk in king_adj[wk]:
                continue
            for p in range(N):
                rp = p // W
                if rp == 0 or rp == H - 1:
                    continue
                if p == wk or p == bk:
                    continue
                for stm in ("w", "b"):
                    if stm == "w" and bk in pawn_targets[p]:
                        continue  # White to move while Black is in check: illegal
                    # stm == 'b': White not in check (no Black pawn, kings not adjacent)
                    yield "K%s P%s k%s %s -" % (sq_name(wk, W), sq_name(p, W), sq_name(bk, W), stm)


def parse_board(text):
    kind, dims = text.split(":")
    W, H = (int(x) for x in dims.lower().split("x"))
    if kind not in ("flat", "cyl", "mob"):
        raise SystemExit("bad board kind %r" % kind)
    return W, H, kind


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--board", required=True, help="flat:WxH, cyl:WxH or mob:WxH")
    ap.add_argument("--count-only", action="store_true")
    args = ap.parse_args(argv)
    W, H, kind = parse_board(args.board)
    n = 0
    wtm = 0
    for line in positions(W, H, kind):
        n += 1
        if line.endswith(" w -"):
            wtm += 1
        if not args.count_only:
            sys.stdout.write(line + "\n")
    sys.stderr.write("[gen_kpk_positions %s: %d legal, %d with White to move]\n" % (args.board, n, wtm))
    return 0


if __name__ == "__main__":
    sys.exit(main())
