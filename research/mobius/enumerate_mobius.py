#!/usr/bin/env python3
"""Enumerate all pawn-only positions with <= 4 pawns on Möbius strips of width 3-6,
and compare values with cylinder and flat boards of the same width."""

import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from itertools import combinations, product
from research.mobius.mobius_pawns import mobius_board, Pos as MPos, value as mvalue, components as mcomponents, passed as mpassed
from cylcgt import pawns as cylpawns, cgt

BIG = 256

def enumerate_positions(width: int, max_pawns: int = 4):
    """Generate all legal pawn-only positions with up to max_pawns total pawns."""
    files = width
    ranks = 8
    squares = [(f, r) for f in range(files) for r in range(1, ranks + 1)]
    results = []

    # For each total number of pawns from 1 to max_pawns
    for total in range(1, max_pawns + 1):
        # Split between white and black
        for w_count in range(total + 1):
            b_count = total - w_count
            # Choose squares for white and black (disjoint)
            for w_squares in combinations(squares, w_count):
                w_set = set(w_squares)
                remaining = [sq for sq in squares if sq not in w_set]
                for b_squares in combinations(remaining, b_count):
                    # Build position strings
                    w_str = " ".join(f"{chr(ord('a')+f)}{r}" for f, r in sorted(w_squares))
                    b_str = " ".join(f"{chr(ord('a')+f)}{r}" for f, r in sorted(b_squares))
                    pos_str = f"W: {w_str} / B: {b_str}"
                    try:
                        yield pos_str
                    except Exception:
                        pass

def get_value(board, pos_str, board_type: str):
    """Get CGT value for a position on the given board type."""
    try:
        if board_type == "mobius":
            from research.mobius.mobius_pawns import value as mvalue
            pos = MPos.parse(pos_str)
            return mvalue(board, pos)
        elif board_type == "cylinder":
            pos = cylpawns.Pos.parse(pos_str)
            return cylpawns.value(board, pos)
        elif board_type == "flat":
            pos = cylpawns.Pos.parse(pos_str)
            return cylpawns.value(board, pos)
    except Exception as e:
        return None

def value_to_str(g):
    """Convert game to canonical string representation."""
    if g is None:
        return "ERROR"
    return cgt.show(g)

def main():
    widths = [3, 4, 5, 6]
    max_pawns = 4

    # Store values seen on each board type
    mobius_values = {w: set() for w in widths}
    cylinder_values = {w: set() for w in widths}
    flat_values = {w: set() for w in widths}

    # Also track which positions produce which values
    mobius_positions = {w: {} for w in widths}

    total_positions = 0

    for width in widths:
        print(f"\n=== Width {width} ===")
        mboard = mobius_board(width)
        cboard = cylpawns.Board(files=width, ranks=8, wrap=True, ep=True)
        fboard = cylpawns.Board(files=width, ranks=8, wrap=False, ep=True)

        count = 0
        for pos_str in enumerate_positions(width, max_pawns):
            count += 1
            if count % 1000 == 0:
                print(f"  Processed {count} positions...")

            mv = get_value(mboard, pos_str, "mobius")
            cv = get_value(cboard, pos_str, "cylinder")
            fv = get_value(fboard, pos_str, "flat")

            mvs = value_to_str(mv)
            cvs = value_to_str(cv)
            fvs = value_to_str(fv)

            mobius_values[width].add(mvs)
            cylinder_values[width].add(cvs)
            flat_values[width].add(fvs)

            if mvs not in mobius_positions[width]:
                mobius_positions[width][mvs] = pos_str

        print(f"  Total positions: {count}")
        total_positions += count

    # Find values unique to Möbius
    print("\n\n=== VALUES UNIQUE TO MÖBIUS STRIP ===")
    for width in widths:
        cyl_flat = cylinder_values[width] | flat_values[width]
        unique = mobius_values[width] - cyl_flat
        print(f"\nWidth {width}: {len(unique)} unique values")
        for val in sorted(unique, key=lambda x: (len(x), x)):
            example = mobius_positions[width].get(val, "?")
            print(f"  {val}  (e.g. {example})")

    # Also find values unique to cylinder vs flat
    print("\n\n=== VALUES UNIQUE TO CYLINDER (vs flat) ===")
    for width in widths:
        unique = cylinder_values[width] - flat_values[width]
        print(f"\nWidth {width}: {len(unique)} unique values")
        for val in sorted(unique, key=lambda x: (len(x), x)):
            print(f"  {val}")

    print(f"\n\nTotal positions examined: {total_positions}")

if __name__ == "__main__":
    main()