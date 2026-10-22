#!/usr/bin/env python3
"""Optimized enumeration using component decomposition and integer encoding."""

import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from functools import lru_cache
from research.mobius.mobius_pawns import mobius_board, Pos as MPos, value as mvalue, components as mcomponents, _value as m_value, passed as mpassed, moves as mmoves
from cylcgt import pawns as cylpawns, cgt

BIG = 256

# Encode position as integer for fast canonicalization
# Each square: file (0..w-1), rank (1..8), dir (+1/-1)
# We'll use a compact representation

def encode_pos(pos: MPos, width: int) -> int:
    """Encode a position as a sorted tuple of (side, file, rank, dir) for canonicalization."""
    items = []
    for f, r, d in pos.white:
        items.append((0, f, r, 0 if d == 1 else 1))
    for f, r, d in pos.black:
        items.append((1, f, r, 0 if d == 1 else 1))
    items.sort()
    return tuple(items)

def decode_pos(encoded, width: int) -> MPos:
    white = set()
    black = set()
    for side, f, r, d in encoded:
        dval = 1 if d == 0 else -1
        if side == 0:
            white.add((f, r, dval))
        else:
            black.add((f, r, dval))
    return MPos(frozenset(white), frozenset(black), None)

def canonicalize(encoded, width: int):
    """Return canonical representative under file shifts (Möbius: odd shifts flip rank+dir)."""
    best = None
    for k in range(width):
        shifted = []
        for side, f, r, d in encoded:
            nf = (f + k) % width
            if k % 2 == 1:
                nr = 9 - r
                nd = 1 - d  # flip direction
            else:
                nr = r
                nd = d
            shifted.append((side, nf, nr, nd))
        shifted.sort()
        t = tuple(shifted)
        if best is None or t < best:
            best = t
    return best


def enumerate_components(width: int, max_pawns: int):
    """Generate all connected components (no empty files) with up to max_pawns pawns."""
    # A component occupies a consecutive set of files (mod width)
    # For each component file-span size (1 to width), and each starting file
    # But on Möbius, a component can wrap around the seam
    pass


# Instead, let's just do a direct but optimized enumeration for small widths
# Width 3: 24 squares, width 4: 32 squares, etc.
# Use integer encoding throughout

def gen_positions(width: int, max_pawns: int):
    """Generate canonical positions directly."""
    squares = [(f, r) for f in range(width) for r in range(1, 9)]
    seen = set()

    for total in range(1, max_pawns + 1):
        for w_count in range(total + 1):
            b_count = total - w_count
            from itertools import combinations
            for w_sq in combinations(squares, w_count):
                w_set = set(w_sq)
                remaining = [sq for sq in squares if sq not in w_set]
                for b_sq in combinations(remaining, b_count):
                    # Build encoded position with default directions
                    encoded = []
                    for f, r in w_sq:
                        encoded.append((0, f, r, 0))  # White dir = +1 (0)
                    for f, r in b_sq:
                        encoded.append((1, f, r, 1))  # Black dir = -1 (1)
                    encoded.sort()
                    canon = canonicalize(tuple(encoded), width)
                    if canon not in seen:
                        seen.add(canon)
                        yield canon


def pos_from_canon(canon, width: int) -> MPos:
    """Convert canonical encoded tuple to MPos."""
    white = set()
    black = set()
    for side, f, r, d in canon:
        dval = 1 if d == 0 else -1
        if side == 0:
            white.add((f, r, dval))
        else:
            black.add((f, r, dval))
    return MPos(frozenset(white), frozenset(black), None)


def value_str(g):
    return cgt.show(g) if g else "ERROR"


def main():
    widths = [3, 4]  # Start with just 3 and 4
    max_pawns = 4

    mobius_vals = {w: set() for w in widths}
    cylinder_vals = {w: set() for w in widths}
    flat_vals = {w: set() for w in widths}
    mobius_examples = {w: {} for w in widths}

    for width in widths:
        print(f"\n=== Width {width} ===")
        mboard = mobius_board(width)
        cboard = cylpawns.Board(files=width, ranks=8, wrap=True, ep=True)
        fboard = cylpawns.Board(files=width, ranks=8, wrap=False, ep=True)

        count = 0
        for canon in gen_positions(width, max_pawns):
            count += 1
            if count % 500 == 0:
                print(f"  {count} canonical positions...")

            mpos = pos_from_canon(canon, width)
            pos_str = str(mpos)

            try:
                mv = mvalue(mboard, mpos)
                cv = cylpawns.value(cboard, cylpawns.Pos.parse(pos_str))
                fv = cylpawns.value(fboard, cylpawns.Pos.parse(pos_str))

                mvs = value_str(mv)
                cvs = value_str(cv)
                fvs = value_str(fv)

                mobius_vals[width].add(mvs)
                cylinder_vals[width].add(cvs)
                flat_vals[width].add(fvs)

                if mvs not in mobius_examples[width]:
                    mobius_examples[width][mvs] = pos_str
            except Exception as e:
                pass

        print(f"  Total canonical: {count}")

    print("\n=== VALUES UNIQUE TO MÖBIUS ===")
    for width in widths:
        cyl_flat = cylinder_vals[width] | flat_vals[width]
        unique = mobius_vals[width] - cyl_flat
        print(f"\nWidth {width}: {len(unique)} unique Möbius values")
        for val in sorted(unique, key=lambda x: (len(x), x)):
            ex = mobius_examples[width].get(val, "?")
            print(f"  {val}  (e.g. {ex})")

    print("\n=== VALUES UNIQUE TO CYLINDER (vs flat) ===")
    for width in widths:
        unique = cylinder_vals[width] - flat_vals[width]
        print(f"\nWidth {width}: {len(unique)} unique cylinder values")
        for val in sorted(unique, key=lambda x: (len(x), x)):
            print(f"  {val}")


if __name__ == "__main__":
    main()