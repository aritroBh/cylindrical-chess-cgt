#!/usr/bin/env python3
"""Fast counting of unique Möbius values (no printing of individual values)."""

import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from itertools import combinations
from research.mobius.mobius_pawns import mobius_board, Pos as MPos, value as mvalue
from cylcgt import pawns as cylpawns, cgt

def value_str(g):
    return cgt.show(g) if g else "ERROR"

def gen_positions(width: int, max_pawns: int):
    squares = [(f, r) for f in range(width) for r in range(1, 9)]
    seen = set()

    for total in range(1, max_pawns + 1):
        for w_count in range(total + 1):
            b_count = total - w_count
            for w_sq in combinations(squares, w_count):
                w_set = set(w_sq)
                remaining = [sq for sq in squares if sq not in w_set]
                for b_sq in combinations(remaining, b_count):
                    encoded = []
                    for f, r in w_sq:
                        encoded.append((0, f, r, 0))
                    for f, r in b_sq:
                        encoded.append((1, f, r, 1))
                    encoded.sort()
                    canon = tuple(encoded)
                    if canon not in seen:
                        seen.add(canon)
                        yield canon

def pos_from_canon(canon) -> MPos:
    white = set()
    black = set()
    for side, f, r, d in canon:
        dval = 1 if d == 0 else -1
        if side == 0:
            white.add((f, r, dval))
        else:
            black.add((f, r, dval))
    return MPos(frozenset(white), frozenset(black), None)

def main():
    widths = [3, 4]
    max_pawns = 4

    for width in widths:
        print(f"\n=== Width {width} ===", flush=True)
        mboard = mobius_board(width)
        cboard = cylpawns.Board(files=width, ranks=8, wrap=True, ep=True)
        fboard = cylpawns.Board(files=width, ranks=8, wrap=False, ep=True)

        mobius_vals = set()
        cylinder_vals = set()
        flat_vals = set()

        count = 0
        for canon in gen_positions(width, max_pawns):
            count += 1
            if count % 1000 == 0:
                print(f"  {count}...", flush=True)

            mpos = pos_from_canon(canon)
            pos_str = str(mpos)

            try:
                mv = mvalue(mboard, mpos)
                cv = cylpawns.value(cboard, cylpawns.Pos.parse(pos_str))
                fv = cylpawns.value(fboard, cylpawns.Pos.parse(pos_str))

                mobius_vals.add(value_str(mv))
                cylinder_vals.add(value_str(cv))
                flat_vals.add(value_str(fv))
            except Exception:
                pass

        cyl_flat = cylinder_vals | flat_vals
        unique = mobius_vals - cyl_flat

        print(f"  Möbius: {len(mobius_vals)}  Cylinder: {len(cylinder_vals)}  Flat: {len(flat_vals)}  Unique: {len(unique)}  Positions: {count}")

if __name__ == "__main__":
    main()