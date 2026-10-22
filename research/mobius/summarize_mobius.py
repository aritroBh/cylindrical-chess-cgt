#!/usr/bin/env python3
"""Extract summary of unique Möbius values from enumeration."""

import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from functools import lru_cache
from research.mobius.mobius_pawns import mobius_board, Pos as MPos, value as mvalue
from cylcgt import pawns as cylpawns, cgt

def value_str(g):
    return cgt.show(g) if g else "ERROR"

def gen_positions(width: int, max_pawns: int):
    from itertools import combinations
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
                    canon = tuple(encoded)  # simplified canonicalization for speed
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
        print(f"\n=== Width {width} ===")
        mboard = mobius_board(width)
        cboard = cylpawns.Board(files=width, ranks=8, wrap=True, ep=True)
        fboard = cylpawns.Board(files=width, ranks=8, wrap=False, ep=True)

        mobius_vals = set()
        cylinder_vals = set()
        flat_vals = set()
        mobius_examples = {}

        count = 0
        for canon in gen_positions(width, max_pawns):
            count += 1
            mpos = pos_from_canon(canon)
            pos_str = str(mpos)

            try:
                mv = mvalue(mboard, mpos)
                cv = cylpawns.value(cboard, cylpawns.Pos.parse(pos_str))
                fv = cylpawns.value(fboard, cylpawns.Pos.parse(pos_str))

                mvs = value_str(mv)
                cvs = value_str(cv)
                fvs = value_str(fv)

                mobius_vals.add(mvs)
                cylinder_vals.add(cvs)
                flat_vals.add(fvs)

                if mvs not in mobius_examples:
                    mobius_examples[mvs] = pos_str
            except Exception as e:
                pass

        cyl_flat = cylinder_vals | flat_vals
        unique = mobius_vals - cyl_flat

        print(f"  Total Möbius values: {len(mobius_vals)}")
        print(f"  Total Cylinder values: {len(cylinder_vals)}")
        print(f"  Total Flat values: {len(flat_vals)}")
        print(f"  Unique to Möbius: {len(unique)}")
        print(f"  Canonical positions: {count}")

        # Categorize unique values by type
        numbers = []
        switches = []
        infinitesimals = []
        hot = []
        other = []

        for val in unique:
            if val.startswith('+W') or val.startswith('-W'):
                hot.append(val)
            elif val[0] in '0123456789-+/' or (val[0] == '-' and val[1].isdigit()):
                # Check if it's a simple number or switch
                if '±' in val:
                    switches.append(val)
                else:
                    numbers.append(val)
            elif '↑' in val or '↓' in val or '*' in val or 'tiny' in val or 'miny' in val:
                infinitesimals.append(val)
            else:
                other.append(val)

        print(f"    Numbers: {len(numbers)}")
        print(f"    Switches: {len(switches)}")
        print(f"    Infinitesimals: {len(infinitesimals)}")
        print(f"    Hot (involving ±W): {len(hot)}")
        print(f"    Other: {len(other)}")

        # Show some examples of each category
        print(f"    Example numbers: {sorted(numbers)[:10]}")
        print(f"    Example switches: {sorted(switches)[:10]}")
        print(f"    Example infinitesimals: {sorted(infinitesimals)[:10]}")
        print(f"    Example hot: {sorted(hot)[:5]}")


if __name__ == "__main__":
    main()