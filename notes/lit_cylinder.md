# Literature & software: cylinder / torus chess (survey, 2026-10-15)

*Compiled by a Claude research subagent. chessvariants.org returned 403 to every fetch, so statements about those pages rest on search snippets. Gik (1983) and Pritchard's ECV were not accessible.*

## Rules and history
- **Core rule:** files a and h are joined; ranks are not. Standard array. En passant works across the seam, and check and mate work across it too. Pritchard, ECV p.79; Wikipedia "Cylinder chess".
- **Castling** has three conventions: normal only, none, or castling across the edge.
- **Null-move rule.** A rook or queen goes round an empty rank back to its own square. Mongredien allowed it (1926); most play forbids it. **This must be fixed before building any tablebase**, because a free pass destroys zugzwang.
- **Colours and lines:**
  - On 8 files, square colours stay consistent, so bishops remain colour-bound. On odd-width cylinders bishops change colour.
  - Diagonals become 8-square helices, so double check or a double pin by a single piece is possible (Jelliss).
- **Piece values** (H.G. Muller): P1, N3¼, B4, R5, Q11.
- **History:** al-Mas'udi (disputed), Ciccolini 1836, Piccinini 1907, Mongredien/Roese 1926, Dawson 1931, Kipping 1934, Jelliss (*Variant Chess* 1996–97).
- "Serge Clair, Échecs cylindriques" is only a Wikimedia photo of a home-made set — **not a publication**. The 2025 draft's figure credit should say so.

## Mathematical results
- Scattered, unrefereed claims:
  - Cylinder: K+R cannot force mate; two rooks cannot ladder-mate (Wikipedia).
  - Torus: K+Q cannot mate, K+2R can (Gik 1983, via Wikipedia).
  - H.G. Muller: no minor-piece pair can force mate on the cylinder.
- **Our 4-man retrograde check** (`tablebase/egt_prototype.c`; agent-written, re-run in this session):
  - On the flat board it reproduces the known maxima: KQK 10, KRK 16, KBBK 19, KBNK 33.
  - Results (% of white-to-move positions won, longest mate in moves):

| Material | Flat | Cylinder | Torus |
|---|---|---|---|
| KQK | 100%, 10 | 100%, 10 | 0% (no mate position exists) |
| KRK | 100%, 16 | 2.8% (not forced) | 0% |
| KBBK, opposite colours | 99.98%, 19 | **100%, 14** | 0% (mate positions exist but cannot be reached by a legal move) |
| KBNK | 99.5%, 33 | **0.024% — not a forced win** | 0% |
| KNNK | 0.011% | 0.008% | 0% |
| KRBK | 100%, 16 | 99.7%, 13 | 0.02% |

  - These contradict Muller on the bishop pair (forced on the cylinder) and agree with him on B+N.
  - **Status: replicated.** An independent solver (`tablebase/replica/replica.c`) agrees on every position of all 24 tables, for both sides to move; see `tablebase/replica/REPORT.md`.
- **Classic combinatorics on these surfaces:**
  - Toroidal n-queens exist iff gcd(n,6)=1 (Pólya 1918).
  - Queens graphs on the torus: Burger–Cockayne–Mynhardt 2001.
  - Knight's tours: Watkins–Hoenigman 1997; Watkins, *Across the Board*; Forrest–Teehan (arXiv 1507.02917); Forrest–Lague (arXiv 2406.05226).

## Software
- **Fairy-Stockfish: no support.** Issue #753 was closed in 2024 ("requires big changes to move generation").
- **mtaktikos/CylindricalChess** (2026) is an unofficial Fairy-Stockfish copy with `cylindrical = true`.
  - Slider attacks are loop-based ray scans.
  - Works around the problem by forcing non-evasion move generation when in check.
  - No perft, no NNUE, not reviewed. A possible starting point for B4.
- Playable without strong AI: Jocly, Ludii, Zillions, XBoard (with legality checks off), the chessvariants Interactive Diagram, cylinderchess.com, and hobby repositories.
- **Tablebase generators:**
  - Muller's FairyGen: 8-fold symmetry is hard-coded, so it is wrong for a cylinder.
  - de Man's syzygy1/tb: magic sliders, ≥16 GB for 6-man, x86 builds. It would need cylinder magics and different symmetry handling.
- **Standard-chess tablebases for context:**
  - Syzygy 7-man (2018).
  - Lomonosov 7-man DTM (offline).
  - Lichess **Op1** partial 8-man (Feb 2026): positions with an opposed pawn pair, ~63 TiB. Possibly usable to verify 8-man king-and-pawn CGT claims on the standard board.

## Cheapest technical routes
- **Move generator:**
  - Leapers: rotate within each rank byte, e.g. east = `((b<<1)&~FileA) | ((b>>7)&FileA)`.
  - Rank sliders: table indexed by [file][occupancy].
  - Helix sliders: a kindergarten multiply into a [64][256] table.
  - Legality: pseudo-legal moves plus an "is the king attacked" test, because there are two routes between squares.
  - Validate with perft against a mailbox implementation, Jocly and Ludii. **Publishing cylinder perft numbers is itself a small contribution.**
- **Tablebases:**
  - Symmetry on the cylinder: 8 file shifts × mirror (× rank flip when pawnless).
  - King-pair classes: 138 pawnless and 276 with pawns, vs 462 and 1806 on the flat board.
  - 6-man pawnless ≈ 2×10⁹ positions per side to move, which fits easily in 48 GB.
- **Engine:** Fairy-Stockfish (or the mtaktikos copy) with proper cylinder slider tables, then variant-NNUE training. Probe our own tablebases during search.
