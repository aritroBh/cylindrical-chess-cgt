#!/usr/bin/env python3
"""Fast enumeration of pawn-only positions on Möbius strips using component decomposition."""

import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from itertools import combinations, product
from functools import lru_cache
from research.mobius.mobius_pawns import mobius_board, Pos as MPos, value as mvalue, components as mcomponents, passed as mpassed, _value as m_value
from cylcgt import pawns as cylpawns, cgt

BIG = 256

# Canonical file shift for Möbius: shift by k files (with rank flip on odd shifts)
def canonical_shift(pos: MPos, board_files: int) -> MPos:
    """Apply file shift to get canonical representative."""
    best = None
    best_pos = pos
    for k in range(board_files):
        shifted_white = set()
        shifted_black = set()
        for f, r, d in pos.white:
            nf = (f + k) % board_files
            # On Möbius, odd shifts flip rank
            if k % 2 == 1:
                nr = 9 - r
                nd = -d
            else:
                nr = r
                nd = d
            shifted_white.add((nf, nr, nd))
        for f, r, d in pos.black:
            nf = (f + k) % board_files
            if k % 2 == 1:
                nr = 9 - r
                nd = -d
            else:
                nr = r
                nd = d
            shifted_black.add((nf, nr, nd))
        # Also consider reflection (file mirror + rank flip)
        for reflect in [False, True]:
            if reflect:
                rwhite = set()
                rblack = set()
                for f, r, d in shifted_white:
                    nf = (board_files - 1 - f) % board_files
                    nr = 9 - r
                    nd = -d
                    rwhite.add((nf, nr, nd))
                for f, r, d in shifted_black:
                    nf = (board_files - 1 - f) % board_files
                    nr = 9 - r
                    nd = -d
                    rblack.add((nf, nr, nd))
                candidate = MPos(frozenset(rwhite), frozenset(rblack), pos.ep)
            else:
                candidate = MPos(frozenset(shifted_white), frozenset(shifted_black), pos.ep)
            # Sort to get canonical string
            cand_str = str(candidate)
            if best is None or cand_str < best:
                best = cand_str
                best_pos = candidate
    return best_pos


def value_to_str(g):
    if g is None:
        return "ERROR"
    return cgt.show(g)


@lru_cache(maxsize=None)
def component_value_cached(board_key: str, comp_key: str) -> str:
    """Cache component values to avoid recomputation."""
    return comp_key  # placeholder, we'll compute directly


def enumerate_components(width: int, max_pawns: int):
    """Enumerate all possible connected components (no empty files inside)."""
    # A component is a set of occupied files that are consecutive (mod width)
    # For each component size (number of files), generate all pawn placements
    pass


def main():
    widths = [3, 4, 5, 6]
    max_total_pawns = 4

    # We'll use a smarter approach: enumerate all positions but skip symmetries
    # and use component caching

    from collections import defaultdict

    mobius_values = {w: set() for w in widths}
    cylinder_values = {w: set() for w in widths}
    flat_values = {w: set() for w in widths}
    mobius_examples = {w: {} for w in widths}

    seen_canonical = {w: set() for w in widths}

    for width in widths:
        print(f"\n=== Width {width} ===")
        mboard = mobius_board(width)
        cboard = cylpawns.Board(files=width, ranks=8, wrap=True, ep=True)
        fboard = cylpawns.Board(files=width, ranks=8, wrap=False, ep=True)

        squares = [(f, r) for f in range(width) for r in range(1, 9)]

        count = 0
        canonical_count = 0

        for total in range(1, max_total_pawns + 1):
            for w_count in range(total + 1):
                b_count = total - w_count
                for w_squares in combinations(squares, w_count):
                    w_set = set(w_squares)
                    remaining = [sq for sq in squares if sq not in w_set]
                    for b_squares in combinations(remaining, b_count):
                        count += 1
                        w_str = " ".join(f"{chr(ord('a')+f)}{r}" for f, r in sorted(w_squares))
                        b_str = " ".join(f"{chr(ord('a')+f)}{r}" for f, r in sorted(b_squares))
                        pos_str = f"W: {w_str} / B: {b_str}"

                        # Parse as Möbius position to get canonical form
                        try:
                            mpos = MPos.parse(pos_str)
                            canon = canonical_shift(mpos, width)
                            canon_str = str(canon)
                            if canon_str in seen_canonical[width]:
                                continue
                            seen_canonical[width].add(canon_str)
                            canonical_count += 1

                            # Compute values
                            mv = mvalue(mboard, canon)
                            cv = cylpawns.value(cboard, cylpawns.Pos.parse(canon_str))
                            fv = cylpawns.value(fboard, cylpawns.Pos.parse(canon_str))

                            mvs = value_to_str(mv)
                            cvs = value_to_str(cv)
                            fvs = value_to_str(fv)

                            mobius_values[width].add(mvs)
                            cylinder_values[width].add(cvs)
                            flat_values[width].add(fvs)

                            if mvs not in mobius_examples[width]:
                                mobius_examples[width][mvs] = canon_str

                        except Exception as e:
                            pass

        print(f"  Raw positions: {count}, Canonical: {canonical_count}")

    # Report unique values
    print("\n\n=== VALUES UNIQUE TO MÖBIUS STRIP ===")
    for width in widths:
        cyl_flat = cylinder_values[width] | flat_values[width]
        unique = mobius_values[width] - cyl_flat
        print(f"\nWidth {width}: {len(unique)} unique values out of {len(mobius_values[width])} total Möbius values")
        for val in sorted(unique, key=lambda x: (len(x), x)):
            example = mobius_examples[width].get(val, "?")
            print(f"  {val}  (e.g. {example})")

    print("\n\n=== VALUES UNIQUE TO CYLINDER (vs flat) ===")
    for width in widths:
        unique = cylinder_values[width] - flat_values[width]
        print(f"\nWidth {width}: {len(unique)} unique values")
        for val in sorted(unique, key=lambda x: (len(x), x)):
            print(f"  {val}")

if __name__ == "__main__":
    main()