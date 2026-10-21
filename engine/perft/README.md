# Cylinder perft: two reference move generators

This is step 1 of the perft plan in [`../FAIRY_CYLINDER.md`](../FAIRY_CYLINDER.md) §3, and the first half of
plan item B1. It provides reference numbers that a cylinder Fairy-Stockfish, or any other cylinder engine, must
reproduce.

| File | What it is |
|---|---|
| `cylperft.c` | Mailbox generator in C. Attacks are found by looking *backwards* from the target square along rays. Has `divide` and `stats` modes; `stats` counts captures, e.p., castles, promotions, checks and mates |
| `cylperft.py` | A second generator in pure Python, written separately and structured differently: a dict board, attacks found *forwards* from every enemy piece, moves kept in a set |
| `check.py` | Runs both programs against published flat-board perft and against each other on the cylinder, and tests the symmetry invariants. Writes `results.json` |
| `check_output.txt` | The output of the last run of `check.py` |

**Rules** (plan B0):
- files a and h are adjacent, and every file step wraps modulo 8;
- ranks are not joined;
- a slider ray stops at the first piece and never returns to its own square, so there is no rook "pass";
- **a move is (from, to, promotion piece)**, so a square reachable along two routes counts once. The two routes are
  east and west along a rank, or the two helices when |Δrank| = |Δfile| = 4;
- castling is the flat rule, and the attacks on the king's squares are cylinder attacks;
- e.p. and pawn captures work across the seam;
- legal means the mover's king is not attacked after the move.

## Results (`check_output.txt`)

**Flat board, as an anchor.** Both programs reproduce the published perft of the start position, Kiwipete and
positions 3-5 of the chessprogramming.org table:
- the C program to depths 4-5;
- the Python program to depths 2-3.

**Cylinder, start position** (C to depth 6; Python agrees to depth 4):

| depth | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| flat 8×8 | 20 | 400 | 8,902 | 197,281 | 4,865,609 | 119,060,324 |
| **8-file cylinder** | **20** | **392** | **9,162** | **211,036** | **5,633,208** | **149,017,571** |

The flat depth-6 value is the published one; this C program was not run on it.

- Depth 2 is *smaller* on the cylinder. After 1.c3 the queen pins f7 along the helix d1-c2-b3-a4-h5-g6-f7-e8.
  After 1.g3 the bishop pins d7 along f1-g2-h3-a4-b5-c6-d7-e8. Each pin takes away two Black replies.
- `stats` reproduces the published flat-board columns: 34 captures and 12 checks at depth 3; 1,576 captures,
  469 checks and 8 mates at depth 4.
- On the cylinder, `stats` gives 252 captures and 198 checks at depth 3, and 7,475 captures, 5,866 checks and
  8 mates at depth 4.

**Cylinder, Kiwipete** (`r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -`): 51, 2,599, 135,626,
6,664,502 (Python agrees to depth 3).

**Seam positions.** Cylinder perft at depths 1-4 against flat. The two programs agree to depth 3, and each
depth-1 count was also checked by hand.

| Position | FEN | Cylinder | Flat |
|---|---|---|---|
| Rook on a rank, both routes | `7k/8/8/8/8/8/8/R3K3 w - -` | 18, 62, 1134, 6365 | 15, 42, 762, 4046 |
| One bishop gives double check along two helices | `8/8/8/4k3/8/8/8/B3K3 b - -` | 4, 72, 397, 6938 | 6, 72, 439, 6143 |
| E.p. across the seam, a5xh6 | `4k3/8/8/P6p/8/8/8/4K3 w - h6` | 7, 41, 299, 2211 | 6, 36, 269, 2019 |
| Castling forbidden by Ba3's attack on g1 through h2 | `4k3/8/8/8/8/b7/8/4K2R w K -` | 18, 298, 4612, 73919 | 15, 165, 2741, 32644 |
| Helix pin after 1.c3 | `rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b KQkq -` | 18, 425, 9208, 260754 | 20, 420, 9272, 222861 |
| Pawn capture across the seam with promotion, h7xa8 | `r3k3/7P/8/8/8/8/8/4K3 w - -` | 13, 145, 1802, 24875 | 9, 110, 1128, 18004 |

**Symmetry.** There were 150 random cylinder positions, from 6-40 random legal moves from the start with
castling rights dropped.
- Perft at depth 3 is unchanged under all 8 file rotations and the mirror: **0 violations in 2,250
  comparisons**.
- The C and Python programs agree at depth 2 on all 150.

## Status and caveats

- **Two implementations, one author.** Both programs were written by the same model (Claude) in one session, so
  this is not yet independent confirmation.
  - The flat-board anchor and the symmetry tests catch most seam bugs, but not a shared misreading of the rules.
  - Plan B1 asks for agreement with an implementation by a different author, such as Jocly/Ludii, a Codex
    rewrite, or a corrected Fairy-Stockfish.
- **Rules are a convention.** Other cylinder rule sets (castling, or a rook allowed to "pass" around an empty
  rank) give different numbers. These numbers are for the B0 rules above.
- **Novelty.** The literature survey (`notes/lit_cylinder.md`) found no published cylinder perft numbers. That
  is a statement about our search, not proof that none exist.

## Reproduce

Run from the project root, one command per block.

```bash
cc -O2 -o engine/perft/cylperft engine/perft/cylperft.c
```

Run the full check (about 3 minutes, most of it the Python program):

```bash
.venv/bin/python engine/perft/check.py
```

One number:

```bash
engine/perft/cylperft cyl 6 "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
```

Move-by-move counts, for localising a disagreement:

```bash
engine/perft/cylperft cyl 2 "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" divide
```

The extended columns of plan §3 step 3:

```bash
engine/perft/cylperft cyl 4 "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" stats
```
