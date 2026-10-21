# Cylinder support for Fairy-Stockfish: state of the art and a design

*Workstream engine-analysis, 2026-10-15; Stockfish references updated 2026-10-16 to Stockfish 19 (tag `sf_19`),
read from the local checkout. This is a design document. No Fairy-Stockfish or fork code was compiled or run.*

## 1. Where things stand

### 1.1 Upstream: Fairy-Stockfish issue #753 ("Support Cylinder Chess")
- **History.**
  - Opened 2024-01-02 by eskopp, with labels *variant* and *enhancement*.
  - The discussion drifted to toroidal boards.
  - The opener closed it on 2024-10-26, first as completed, then as *not planned*.
- **The maintainer's reason.** ianfab answered the next day: the variant is not irrelevant, but it "requires big
  changes to move generation". No workaround was suggested in the thread.
- **Source.** Read via WebFetch of github.com/fairy-stockfish/Fairy-Stockfish/issues/753 on 2026-10-15. This is a
  model summary of the page; the short quote above is from it.

### 1.2 The unofficial copy: `mtaktikos/CylindricalChess`
Inspected read-only on 2026-10-15 with `gh api` (commit list, file lists, and file contents grepped for `cylind`).

**Repository facts.**
- Five commits, all titled "Add files via upload":
  - three on 2026-03-23, which add `src/` plus the top-level files;
  - two on 2026-07-20, which add a second tree `srchgm/`.
- GPL-3.0, 0 stars, no description. No perft results, no NNUE net, no tests specific to the cylinder.
- **`srchgm/` contains no cylinder code.** I grepped `bitboard.h`, `position.cpp` and `movegen.cpp` there for
  `cylind` and got nothing. The cylinder work is all in `src/`.

**What `src/` implements** (file:line in that tree):
| Piece | Where | How |
|---|---|---|
| Variant flag | `variant.h:114` `bool cylindrical`; `parser.cpp:478`; `variants.ini:2056-2064` `[cylinder:chess] cylindrical = true` | Inherits all chess rules, castling included |
| Rank sliders | `bitboard.h:794` `cylindrical_rank_attacks()` | Loop over `i = 1 … numFiles-1` east and west with `% numFiles`; stops at the first blocker. **It never reaches its own square, so there is no "rook pass" null move.** |
| Diagonal sliders | `bitboard.h:822` `cylindrical_diag_attacks()` | Four directions; the file wraps, the rank stops at the edges |
| All piece attacks | `position.h:1295-1345` `Position::cylindrical_piece_attacks()` | Leaper steps with the file wrapped modulo `numFiles`. Riders dispatched: `RIDER_ROOK_H` and `RIDER_BISHOP` use the loops above, `RIDER_ROOK_V` and other riders use the flat tables |
| Use sites | `position.h:1224-1230` `attacks_from()`, `:1258-1264` `moves_from()`; `position.cpp:973-975` `attackers_to()`; `:1375-1377` `pseudo_legal()`; `:2530-2569` SEE | Branch on `var->cylindrical` |
| Fast paths off | `variant.cpp:2010-2020` | `fastAttacks` and `fastAttacks2` are false when `cylindrical` is set, so `attackers_to()` takes the slow, topology-aware path |
| Pawn captures across the seam | `movegen.cpp:163-184`, `:308-320` | Separate `wrapBrc` and `wrapBlc` bitboards, with the from-square computed explicitly |
| Evasions | `movegen.cpp:585-589` | When in check, generate `NON_EVASIONS` and filter with `legal()`, because `between_bb` does not know the seam |

**Gaps found by reading the code.** None of these were executed. Each needs a test that confirms it (§3).
1. **Checks delivered across the seam are probably not detected.**
   - `StateInfo::checkSquares` is filled with the free function `attacks_bb(~stm, pt, ksq, pieces())`
     (`position.cpp:585`), which is not seam-aware.
   - `gives_check()` uses `check_squares(pt) & to` for direct checks (`position.cpp:1458`).
   - `do_move()` then sets `checkersBB = givesCheck ? attackers_to(...) : 0` (`position.cpp:2088`).
   - So a move that checks *only through the seam* would leave `checkers()` empty. `legal()` still filters moves
     with a full `attackers_to` test (`position.cpp:1287`, the end of `Position::legal`), so **perft node counts should stay correct**. But search
     sees "not in check": a mate across the seam would be scored as **stalemate** (no legal moves and
     `!inCheck` gives a draw), check extensions are lost, and qsearch would stand pat while in check.
2. **Pins and discovered checks across the seam.** `slider_blockers()` (`position.cpp:843-880`) builds its snipers
   from the flat `PseudoAttacks`/`attacks_bb`. Seam pins are therefore missing from `blockersForKing`. This breaks
   discovered-check detection in `gives_check()` (`:1463`) and the pinned-piece filter in SEE (`:2511`).
3. **En passant across the seam looks missing.**
   - `do_move()` sets an e.p. square only if `pawn_attacks_bb(us, to - push) & pieces(them, PAWN)`
     (`position.cpp:1853-1857`), and generation uses `pawn_attacks_bb(Them, epSquare)` (`movegen.cpp:299`).
   - Both are flat-board tables. So after …h7-h5 a White pawn on a5 cannot capture a5×h6 e.p.
   - **This matters for this project:** the 2025 paper's Position 3.1 is value `1` only *because* of wrap-around
     en passant (`notes/audit.md`). Plain perft *does* catch this one, through a node-count difference.
4. **Evaluation is flat.** `pawns.cpp` (`passed_pawn_span`, `adjacent_files_bb`, `edge_distance`: lines 128-132,
   186, 262) and `evaluate.cpp` (lines 558, 779 `KingFlank`, 1048, 1073) contain no seam handling. Consequences:
   - a- and h-pawns are not neighbours, so passed, isolated and backward pawns are misjudged on those files;
   - edge-distance terms are meaningless on a board with no edges.
5. **Flat-board endgame knowledge is still active.** `endgame.cpp`, `bitbase.cpp` (the KPK bitbase) and
   `material.cpp` contain no `cylind`, so flat-geometry evaluators such as KBNK corner-driving stay live. Our
   4-man prototype finds KBNK and KRK are **not** forced wins on the cylinder (`RESEARCH_PLAN.md` §1.3; single
   implementation).
6. **No cylinder NNUE.** The HalfKAv2 feature code is unchanged.
7. **Not checked:** whether any code path could probe standard Syzygy tables for this variant. They would be wrong
   for the cylinder.

Verdict: a useful proof of concept for move *generation*. It is not yet a correct *engine*. Items 1–3 are cheap to
fix, and §2 removes the per-move loops altogether.

---

## 2. Design

Rules follow plan **B0**: files a and h are adjacent; ranks are not joined; en passant and pawn captures work across
the seam; no rook "pass"; castling is standard (king and rook never cross the seam); no castling in endgame tables.
The design keeps Fairy-Stockfish's runtime-variant architecture. Everything is behind one `Topology` value, so flat
variants pay nothing.

### 2.1 Topology and board geometry
- Add `enum Topology { FLAT, CYLINDER /*, TORUS later */ }` to `Variant`. Keep the fork's `cylindrical = true` key
  as an alias.
- Board width `W = maxFile + 1`, which can be any value up to `FILE_NB`: 8 in 64-bit builds, 12 in largeboard
  builds (12×10 squares in a 128-bit `Bitboard`).
- **Wrap shifts.** These replace `shift<EAST>` and `shift<WEST>` when the topology is `CYLINDER`:
  ```
  east(b) = ((b & ~file_bb(maxFile)) << 1) | ((b & file_bb(maxFile)) >> maxFile)
  west(b) = ((b & ~FileABB)          >> 1) | ((b & FileABB)          << maxFile)
  ```
  Diagonal shifts compose these with `NORTH`/`SOUTH`. Pawn attack bitboards, pawn-capture generation and the
  e.p. attacker test (`pawn_attacks_bb`) then all wrap automatically, which fixes gap 3.
- **Never compute a from-square as `to - direction`** across the seam. Use the wrap-aware inverse shift, or store
  the from-square, as the fork does for captures.

### 2.2 Leaper tables
`Bitboards::init()` fills `PseudoAttacks[c][pt][s]` and `LeaperAttacks` from step lists. Its `safe_destination()`
rejects any step that changes file by more than about 2. For a cylinder, build a second set of tables with
`f' = (f + df) mod W`, and select the set with the topology. The per-call loop in
`cylindrical_piece_attacks()` then becomes a single table lookup, done once at start-up.

### 2.3 Slider tables
- **Vertical rides** (`RIDER_ROOK_V` and friends) are unchanged.
- **Horizontal rides** on a ring of `W` squares. The ray goes east and west until the first blocker in each
  direction, and stops before the origin square.
  - The relevant occupancy is the `W-1` other squares of the rank. There are no edges, so no square can be dropped
    from the mask.
  - That gives a `[W][2^(W-1)]` table of `W`-bit masks, shifted to the rank: 8 × 128 entries on 8 files.
  - Alternatively, give each square magic or PEXT entries with a 7-bit index.
- **Diagonal rides are helices.** NE: `(f+k mod W, r+k)`. NW: `(f-k mod W, r+k)`. Both run until the rank edge.
  - On 8×8 every helix has exactly one square per rank, so each has 8 squares.
  - The relevant mask is the two helices minus the origin and minus their rank-1 and rank-8 end squares: at most
    6 + 6 = 12 bits. A flat bishop on d4 has 9 bits, so this fits easily in Fairy-Stockfish's magic/PEXT
    machinery.
  - Generate the attack sets with a slow ray loop, like the fork's code, inside `init_magics()`, by generalising
    its `sliding_attack()` with a topology argument. Then look up with the existing magic code. This is correct by
    construction.
  - Optional optimisation: rotating each rank byte by its rank index turns NE helices into files, which allows
    kindergarten file tricks.
- **Two routes between two squares.**
  - Squares on one rank are always joined by two arcs, east and west.
  - Two squares lie on both a NE and a NW helix exactly when `Δrank ≡ Δfile` and `Δrank ≡ −Δfile (mod W)`. With
    `W = 8` this means `|Δrank| = 4` and `|Δfile| = 4`. Example: a1–e5, through b2-c3-d4 and through h2-g3-f4.
  - So **one bishop or queen can give check along two lines at once**, a single-piece double check (Jelliss), and
    can pin along two lines.

### 2.4 Lines, checks, pins and evasions
- Precompute `RouteBB[s1][s2][k]` for `k < 2` per line type: the interior squares of each route. Then:
  - `between_bb(s1,s2)` is the union of the routes, used only for fast filters.
  - **Evasions:** for each checker, collect its *open* routes to the king, those with no piece on the interior.
    The block mask is the AND of the interiors of all open routes over all checkers. The interiors of distinct
    routes are disjoint, so a two-route check can only be met by a king move or by capturing the checker. This
    generalises the double-check rule.
  - **Pins:** a piece is pinned when it is the only occupant of some route from an enemy slider to its king, and no
    other route from that slider is open (if one were, it would be check). Its legal destinations are that
    route's interior plus the pinner.
- `checkSquares[pt]` must come from the topology-aware `attacks_bb` (fixes gap 1). `slider_blockers()` must use
  the topology-aware pseudo-attacks plus the route logic (fixes gap 2).
- **First correct version:** `legal()` = pseudo-legal + "own king not attacked after the move", with a
  topology-aware `attackers_to()`. Fairy-Stockfish's slow path already does this. Get perft (§3) clean on that
  basis before optimising pins and evasions.

### 2.5 Pawns, castling, game end
- Pawn pushes and promotions are unchanged. Captures and e.p. wrap (§2.1).
- The e.p. square is set iff an enemy pawn attacks it *with the wrapped table*.
- Castling uses the flat definition. The "squares attacked" test goes through the topology-aware
  `attackers_to()`, so an attack across the seam on f1 or d1 forbids castling.
- Mate and stalemate are unchanged once `checkers()` is right.

### 2.6 Evaluation (classical fallback)
- Make `adjacent_files_bb`, `passed_pawn_span`, `pawn_attack_span` and `KingFlank` topology-aware, through
  precomputed tables.
- Replace `edge_distance()` terms with constants on the cylinder.
- Disable the flat-geometry endgame evaluators (KBNK, KRK, KPK bitbase) for `CYLINDER`. The KPK bitbase can later
  be regenerated from our own tablebase (B2).
- Disable Syzygy for the variant.

### 2.7 NNUE features
- Fairy-Stockfish uses HalfKAv2-style features (king square × piece square × piece type) with horizontal
  mirroring. The cylinder's symmetry group includes all `W` file translations (plus a reflection).
- **Translation-canonical features:**
  - Rotate files so that the perspective king is on file a. A feature is then (king rank, piece file offset
    `(f − f_K) mod W`, piece rank, piece type, colour).
  - King buckets drop from 64 (or 32 with mirroring) to 8, and the evaluation is **exactly** invariant under file
    rotation.
  - Reflection cannot also be fixed by the king alone. Either leave it free or break the tie with a second piece.
  - Every lateral king move changes the frame, so it forces an accumulator refresh. HalfKA already refreshes on
    king-bucket changes, so the cost is similar.
- **Pawn-pair and threat features**, if ported from Stockfish 19 (`ENGINES.md` §2.6).
  - The pawn-pair band is `PawnPairBB[s] = (file | shift(file, EAST) | shift(file, WEST)) & ~(Rank1BB | Rank8BB) &
    ~square_bb(s)` (`bitboard.h:130-144`).
  - On the cylinder the two `shift` calls must be the wrap shifts of §2.1. Otherwise a- and h-pawns never form a
    pair, and passed-pawn structure across the seam is invisible to the first layer.
  - `FullThreats::OrientTBL` (`nnue/features/full_threats.h:47`) mirrors the board by the half the king stands
    in. Reflection is still a symmetry of the cylinder, so this stays valid, but it becomes redundant once
    features are made translation-canonical as above.
  - Threat features need the seam-aware attack tables of §2.2-§2.3.
- **Training data.** No cylinder games exist.
  - Bootstrap by self-play with the corrected classical evaluation, using Fairy-Stockfish's training-data
    generator and the `variant-nnue-pytorch` trainer.
  - Validate the resulting nets against our cylinder tablebases (B2) and against `cylcgt` pawn values (Track A).
- **For Lc0-style nets**, use circular padding along files. It is exactly equivariant and the cheapest change
  (plan C2).

### 2.8 Search
- No changes are needed apart from a correct `checkers()`.
- In Stockfish 19, null-move pruning and the Step-15 shallow-depth pruning are guarded by `non_pawn_material(us)`,
  so they are inert in king-and-pawn positions until a promotion (`ENGINES.md` §2.0). I did not check whether
  Fairy-Stockfish, which forks an older search, has the same guards. Cylinder K+P endgames, such as every
  position of the 2025 paper, would then be searched mainly under reverse futility pruning, the cut measured
  as zugzwang-relevant in `ENGINES.md` §5.2.
- Two warnings carry over from `ENGINES.md` §2.1 and §2.3. Null-move pruning and reverse futility pruning are
  zugzwang-blind. On the cylinder the null move is *not* available in the rules, because rays stop before the
  origin square. So any pruning that assumes a pass is available is as wrong here as on the flat board.

---

## 3. Perft and validation plan (plan B1)

**Status (2026-10-16).** Step 1 now has a prototype in [`perft/`](perft/README.md): two reference generators
(C and Python, both by one author). They reproduce published flat-board perft, agree with each other on the
cylinder, and pass the rotation and mirror invariants of step 4 on 150 random positions.
- Cylinder start-position perft: **20, 392, 9,162, 211,036, 5,633,208, 149,017,571** (depths 1-6).
- Depth 2 is below the flat 400 because of helix pins across the seam: after 1.c3, Qd1 pins f7.
- Six of the seam positions of step 2 are tabulated there.
- What is still missing is agreement with an implementation by another author (steps 1 and 5).

1. **Reference generator.** An independent mailbox generator in pure Python: a cylinder version of
   `realchess/movegen.py`'s design, with modular file arithmetic and legality by "make the move, then is the king
   attacked". Two authors, or two models, write it separately.
2. **Hand-made seam positions** (about 30), each with perft 1–4 and a divide listing:
   - rank pins and checks through the seam;
   - helix pins and checks;
   - the **two-route bishop check** (a1–e5 type) and its pinned twin;
   - e.p. across the seam (a5×h6, h5×a6);
   - promotions with a capture across the seam;
   - a rook on an empty rank, where no move may go to its own square;
   - castling forbidden by an attack across the seam;
   - **mate and stalemate across the seam.**
3. **Extended perft columns.** Count nodes, captures, e.p., castles, promotions, **checks, discovered checks, double
   checks, mates**. Gap 1 changes none of the node counts, but it does change the check and mate columns.
4. **Symmetry invariants unique to the cylinder.**
   - Without castling rights, `perft(P) = perft(rotate_files(P, k))` for all `k < W`, and
     `perft(P) = perft(mirror(P))`.
   - Run this on about 1,000 random legal positions to depth 3–4. It is cheap and catches any asymmetric seam bug.
5. **Cross-implementation.** Fairy-Stockfish-cylinder, the mailbox reference, the `mtaktikos` fork as an
   *expected-to-differ* baseline (for gaps 1–3), and Jocly/Ludii move lists where they can be exported.
   Disagreements are localised with `divide`.
6. **Publish** the start-position perft table for depths 1–6, plus the seam-test suite. As far as the literature
   survey found (`notes/lit_cylinder.md`), no cylinder perft numbers are published.
7. **Engine-level checks after perft is clean:**
   - mate-in-*n* across the seam;
   - the 4-man tablebase positions (B2), compared with the engine's reported mates;
   - the cylinder CGT positions from `cylcgt` with a frozen-king embedding;
   - the 2025 paper's Position 3.1, which needs e.p. across the seam.

## 4. Effort estimate (rough)
| Step | Size |
|---|---|
| Topology flag, wrap shifts, leaper tables | ~150 lines of C++ |
| Slider tables via the generalised `sliding_attack` + magics | ~150 lines |
| Routes, checks, pins, evasions | ~250 lines, the risky part |
| Evaluation / endgame / Syzygy guards | ~100 lines |
| Mailbox reference + perft harness + seam suite | ~600 lines of Python |
| NNUE feature transform + training pipeline | the larger task: days of compute for data and training |
