## 1. Setting and exact definitions (all statements are in the P model unless "chess" is written)

**P model** = `kp_p.c` / `kpp --pmodel`: real kings, the first promotion wins at once for the promoter, e.p. on, promotion pieces Q R B N, no capture of the new
piece is needed. Values are from White's view: W (White wins), D (draw), L (White has lost). `kpp --moves` prints, for each legal move, the P value of the position
after the move; kpp prints one entry for each promotion piece, `ref3m` prints one entry for each promoting push or capture.

**Boards.** `flat:W×H` and `cyl:W×H` (files wrap on the cylinder). Files a, b, c are F_Z; ranks 1..H; the pawns of a group stand on F_Z ranks 2..H−1.
On a cylinder every three adjacent files are equivalent by rotation, so F_Z = {a, b, c} loses nothing there. On a flat board it is the edge position only;
interior F_Z (b–d and so on) was not searched.

**Placement.** White king square(s), Black king square(s), at most n_W White and n_B Black pawns on F_Z pawn squares (disjoint, no e.p. flag at a root).
- **K1:** no king square of the group (both shuttle squares of a shuttling king, the one square of a fixed king) is occupied by a pawn or attacked by an enemy pawn of the placement.
- **K2:** every White king square is at king distance 2 or more from every Black king square. So the kings are never adjacent in any combined state.
- **Passers.** A *textbook passer* is a pawn with no enemy pawn ahead on its own or a neighbouring file (the test of `cylcgt.pawns.passed`; for these placements, with no e.p. flag at a root, the e.p.-aware test is the same; checked on all 4,579 + 11,371 placements, `logs/check_passer.log`).
  Z_B (below) has textbook passers (Pa3, Pb4 and the Black pawns pb3, pc4 are all passed, but each is blocked by a king in P). The task statement lists "no passer at any root" among the enumerator's conditions and also requires that the flat 7×6 regression finds Z_B.
  Both cannot hold for the textbook test. K14's referee searched the same 817,270 placements of flat 7×6 (2 + 2 pawns) with no passer filter and found Z_B, so **the enumerator here does not filter on passers: it records the flag**, and every count is given with and without a textbook passer
  Of the 10 exact duds of section 2.1, 8 (the Z_B family) have textbook passers and 2 (Z_C and its mirror) have none. With a passer filter the exact duds would be Z_C and its mirror on cyl:8×6 and nothing on any other board.
- **Roots.** A *state* is a choice of one square of each king's group. A *root* is a state with a side to move.

**Moves of the mover at a root.** The *shuttle move* is the king move between the two shuttle squares of the mover's king. A move *loses at once* (is *decisively punished*) if the position after it
has value L (a White move) or W (a Black move). A **leak** is a legal move of the mover that is neither the shuttle move nor loses at once. The leak count of a root is the number of its leaks;
the *total* of a placement is the sum over its roots. Promotions: kpp counts a promotion that does not lose as 4 leaks (one per piece); the collapsed convention counts it as 1 (`K26_COLLAPSE_PROMO=1`).
Both counts are given. They differ only for placements with a pawn on the 6th/2nd rank, never for an exact group (which has no leak at all).

### The classes

- **(a) Exact dud (type T2).** Both kings have an adjacent pair of safe squares (K1 and K2 hold at all four combined states). At all **8 roots** (4 states × 2 sides to move) the shuttle move exists exactly once and
  the mover has **no leak**. (Then every root value is D; the script also tests this.) This is Z_B's property "every non-shuttle move loses by force", with no cut-off, and it is the hypothesis (Pun) of Theorem 3.2‴ for both colours.
  A pawn move that is a legal non-shuttle move counts too, so "no pawn break" is part of the definition: a dud has no pawn move that does not lose at once.
- **(b) Exact under group, exact over group (mutual zugzwang; Definition 4.8 of EDITS.md).** White's king shuttles on a pair z (K1); Black's king stands on one square b0 (K1, K2 against both z squares).
  Four roots (z0 or z1; White or Black to move). In P:
  - (U1) at both White-to-move roots every non-shuttle White move loses at once and the shuttle is legal;
  - (U2) at both Black-to-move roots Black has at least one legal move that does not lose at once (a *freeze*);
  - (U3) after every freeze m, in the position q_m (no promotion), White to move has a legal move and every legal White move loses at once;
  - (U4) the same q_m with Black to move: Black has a legal move and every legal Black move loses at once. So q_m is a mutual zugzwang, the position 0_D of Definition 4.4.
  
  Then the group is {shuttle on z | freeze to 0}, the mirror of over = {0 | over}. The **colour mirror** (ranks flipped, colours swapped, side to move swapped) is an exact **over** group; so the searches for under with (n_W, n_B) cover over with (n_B, n_W).
  **Loose under group:** (U1)–(U3) without (U4) (only White is in zugzwang after the freeze). The older class `over_exact` of `search.py --type t1` is "loose with exactly one freeze at each root".
- **(c) Exact on (and off).** White's king shuttles on a pair z (K1), Black's king stands on one square b0 (K1, K2). At the **4 roots**: at both White-to-move roots White has no leak; at both Black-to-move roots Black has at least
  one legal move and *every* Black move loses at once. This is Proposition 3.2's hypothesis for White (T1, T2, T4) with Black frozen, so r(G ⊞ Z) ≥ r(G ⊞ on_D) in the D-model and equality when White has no other Z-move that helps. `on_weak` keeps only the Black half.
  **Exact off** is the colour mirror (search with (n_W, n_B) swapped).
- **(d) Minimum leak count.** The minimum of the total over all placements of a board and pawn limit (stage 1 keeps every placement whose total at the two roots (z0, w0) is at most T; T goes up
  until the minimum is at most T and T ≥ 2, so the counts of total 0, 1 and 2 are complete; the total of all 8 roots is at least the total of those two roots, which makes the filter exact).

**Search range** (F_Z = {a, b, c}, no cut-off of any kind): `flat:7×6`, `cyl:7×6`, `cyl:8×6`, `flat:8×6`, `flat:7×7` with at most 2 + 2 pawns; `flat:7×6`, `cyl:7×6`, `cyl:8×6` also with at most 3 + 2 and at most 2 + 3;
for under/over: `cyl:7×6`, `cyl:8×6`, `flat:7×6`, `flat:8×6` with at most 2 + 2 (3 files), `cyl:8×6` also with 3 + 2, 2 + 3 and with four files a–d and at most 2 + 2.
