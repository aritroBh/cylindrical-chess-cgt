# K26 FINDINGS: dud groups without a pawn break on the cylinder; over groups (LOOPY §8 item 2, Conjecture 4.7), P model

1. **Dud: YES on the cylinder, in P.** An exhaustive search of F_Z = {a, b, c} (kings on adjacent pairs, ≤ 2 + 2, 3 + 2, 2 + 3 pawns, no cut-off) finds exactly: Z_B and its mirror on flat 7×6, flat 8×6 and **cyl:7×6**; Z_B, its mirror, and a new passer-free group **Z_C (Pa2 Pc4 / pa3 pc5, kings c2/c3 and a4/a5, every pawn blocked) with its mirror on cyl:8×6**; nothing on flat 7×7 (minimum leak count 1). Every non-shuttle move loses at once at all 8 roots. Roots CHECKED-2; the 2 + 2 search CHECKED-2 on four boards (second enumerator and solver on four boards, a third on two); no hand proof on the cylinder.
2. **Z_B equals dud_D beside every one of 2,049 + 577 + 2,049 exhaustive contexts of ≤ 3 pawns** (cyl:8×6, cyl:7×6, flat 7×6; COMPUTED-1); **Z_C does not** (131 of 2,049 contexts on cyl:8×6 differ, smallest Pe2 pe3: (W, W)). Z_C is exact alone only on cyl:8×6 and cyl:9×6.
3. **Over/under: no exact group (mutual zugzwang, (U1)–(U4)) in any searched range** (≤ 2 + 2 on cyl:7×6, cyl:8×6, flat 7×6, flat 8×6; 3 + 2 and 2 + 3 and four files on cyl:8×6 only): Conjecture 4.7 first half supported, second half open; loose under/over groups exist (120 on cyl:8×6) and are not over_D. Lemma 4.9 (no king freeze) is PROVED.
4. **Exact on/off groups exist on every board (103 on groups, 78 passer-free) and match Theorem 3.4(b), (c) beside contexts except in a few contexts where (Pun) fails.** Minimum leak count: 0 on every board but flat 7×7 (1).
5. **Provenance:** an earlier attempt's scripts and logs were audited and reused; all four binaries rebuilt; the two-shuttle and one-shuttle searches for ≤ 2 + 2 on all five boards, the 3 + 2 and 2 + 3 two-shuttle searches on cyl:8×6, the 2 + 3 search on flat 7×6 and the 3 + 2 search on cyl:7×6, and the one-shuttle searches on cyl:7×6 for 3 + 2 and 2 + 3 were re-run fresh and are identical (counts, histograms, group sets); the exact under/over searches, the one-shuttle searches for 3 + 2 and 2 + 3 on cyl:8×6 and flat 7×6, and the exhaustive contexts are reused (section 8); proposed LOOPY edits in `EDITS.md` (all OLD blocks occur exactly once), counts in `summary.json`.

Output directory: `/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/`.

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

## 2. Exact two-shuttle groups (class a): LOOPY §8 item 2, the dud half

Search: every placement of F_Z = {a, b, c} with the kings on adjacent pairs (K1, K2), at most n_W + n_B pawns, no cut-off, both colours' shuttles, 8 roots per placement.
Counts of placements: 817,270 for 2 + 2 (H = 6), 1,886,421 for 3 + 2 and for 2 + 3 (H = 6), 4,040,080 for 2 + 2 (H = 7); all re-counted by `audit/count_cands.py`.
Fresh runs of this attempt (`logs/k26f_*`, merged by `audit/make_tables.py`, compared with the reused runs by `audit/compare_fresh.py`):

| board | pawns W+B | placements | shards | exact duds (total 0) | total 1 | total 2 | min total | exact duds with textbook passer / without |
|---|---|---|---|---|---|---|---|---|
| flat:7x6 | 2+2 | 817,270 | 1/1 | 2 | 12 | 4 | 0 | 2 / 0 |
| flat:7x6 | 2+3 | 1,886,421 | 2/2 | 2 | 17 | 13 | 0 | 2 / 0 |
| cyl:7x6 | 2+2 | 817,270 | 2/2 | 2 | 0 | 8 | 0 | 2 / 0 |
| cyl:7x6 | 3+2 | 1,886,421 | 4/4 | 2 | 2 | 10 | 0 | 2 / 0 |
| cyl:8x6 | 2+2 | 817,270 | 2/2 | 4 | 0 | 4 | 0 | 2 / 2 |
| cyl:8x6 | 2+3 | 1,886,421 | 4/4 | 4 | 2 | 6 | 0 | 2 / 2 |
| cyl:8x6 | 3+2 | 1,886,421 | 4/4 | 4 | 2 | 6 | 0 | 2 / 2 |
| flat:8x6 | 2+2 | 817,270 | 1/1 | 2 | 12 | 4 | 0 | 2 / 0 |
| flat:7x7 | 2+2 | 4,040,080 | 4/4 | 0 | 12 | 28 | 1 | 0 / 0 |

**The regression on flat 7×6 passes.** With at most 2 + 2 pawns exactly two placements have total 0: Z_B and its mirror (below). They are the only ones with at most 3 + 2 and at most 2 + 3 pawns too. Nothing else has zero leaks. The next best placements have 1 leak
(12 placements for 2 + 2, Z_A type: the leak is Ka5×b4, K14's Z_A has exactly this break).
The result for flat 8×6 is the same as for flat 7×6, count for count (flat width does not matter here).

**Z_B** (K14, K27): White king b2/c3 (shuttle), Black king a4/b5 (shuttle), pawns Pa3 Pb4 / pb3 pc4; the mirror (rank flip, colours swapped) is Ka3/Kb2, kb5/kc4, Pb4 Pc3 / pa4 pb3.
It is exact on flat 7×6, flat 8×6, **cyl:7×6 and cyl:8×6**, and (named-group check, `audit/named_groups.txt`) on every six-rank board tried: flat widths 5, 7, 8, 9, 10, 12 and cylinders of width 5 to 12 (kpp and ref3m agree up to width 8; wider boards ref3m only).
It fails with 8 to 13 leaks on every board with 5, 7 or 8 ranks that was tried (flat 7×5, 7×7, 8×8, cyl 8×5, 6×7, 7×7, 8×7, 9×7, 8×8).
On the cylinder Black has two more legal moves than on the flat board at the roots with the king on a4 (the wrap Ka4–g3 and Ka4–g5 on cyl:7×6, Ka4–h3 and Ka4–h5 on cyl:8×6) and they lose at once (value W). K27's 26 certificates are for the flat board, so Z_B is **not PROVED** exact on the cylinder.

**Z_C (new).** White king c2/c3 (shuttle), Black king a4/a5 (shuttle), pawns **Pa2 Pc4 / pa3 pc5**; mirror (a ↔ c): Ka2/Ka3, kc4/kc5, Pa4 Pc2 / pa5 pc3.
- **All four pawns are blocked** (a2–a3, c4–c5), no pawn move and no pawn capture exists at any root, and **no pawn is a textbook passer**. The only legal non-shuttle moves are king moves; all of them lose at once at all 8 roots.
- Move lists on cyl:8×6 (value after the move, White view; kpp = ref3m on all 8 roots; `audit/movelists.txt`):
  (c2, a4) White: Kc2–c3 D (shuttle), Kb1 L, Kc1 L, Kd1 L, Kd2 L, Kd3 L; Black: Ka4–a5 D (shuttle), Kb4 W, Kh4 W, Kh5 W.
  (c3, a5) White: Kc3–c2 D, Kd3 L, Kd2 L, Kb3 L; Black: Ka5–a4 D, Ka6 W, Kb6 W, Kh4 W, Kh5 W, Kh6 W (Kb4 is illegal next to Kc3). (All eight roots are in `audit/movelists.txt`.)
- **Exact only on cyl:8×6 and cyl:9×6.** It has 8 leaks on cyl 6×6, 7×6 (the two kings can run round the wrap: Kd2 wins for White, Ka4–g5 for Black), 10×6, 11×6, 12×6; 12 on cyl 5×6; 16 on every flat board of six ranks and on flat 7×7 (18 on flat 8×8); on cylinders with 7 or 8 ranks 4 to 8 (6×7 and 7×7: 8; 8×7 and 9×7: 4; 8×8: 6). Table in section 2.2.
- **Beside contexts it is not a dud.** With at most 3 context pawns on files e–g of cyl:8×6 many contexts give a P-result that differs from r(G ⊞ dud_D) (section 6). The smallest is Pe2 pe3 (a blocked pair on file e): the P-result is (W, W) at all 8 roots,
  because White's king move Kc2–d3 (or Kc3–d3) wins there; alone it loses. So (Pun) fails for Z_C beside a pawn that its king can reach, and Z_C is a two-shuttle component only in isolation (and in the contexts that its kings cannot reach).
- Chess (one probe, COMPUTED-1): `kpsolve --board cyl:8x6 --ep on --promote QRBN --cap 1` on the 8 roots of Z_C gives the bounds (W, L) at every root (15 s), so cap 1 does not decide Z_C in chess. Not pursued (K28 works on chess for Z_B).

Diagrams (files a–c, ranks 1–6; K and k are the kings on one of their two shuttle squares each, marked * on the squares they shuttle between; P White pawn, p Black pawn):

```
        Z_B                        Z_C
     a   b   c                  a   b   c
 6   .   .   .              6   .   .   .
 5   .   k*  .              5   k*  .   p
 4   k*  P   p              4   k*  .   P
 3   P   p   K*             3   p   .   K*
 2   .   K*  .              2   P   .   K*
 1   .   .   .              1   .   .   .
```

### 2.1 Every exact dud found

| board | White king shuttle | Black king shuttle | White pawns | Black pawns | textbook passer | first found at |
|---|---|---|---|---|---|---|
| flat:7x6 | b2/c3 | a4/b5 | a3 b4 | b3 c4 | yes | 2+2 |
| flat:7x6 | a3/b2 | b5/c4 | b4 c3 | a4 b3 | yes | 2+2 |
| cyl:7x6 | b2/c3 | a4/b5 | a3 b4 | b3 c4 | yes | 2+2 |
| cyl:7x6 | a3/b2 | b5/c4 | b4 c3 | a4 b3 | yes | 2+2 |
| cyl:8x6 | c2/c3 | a4/a5 | a2 c4 | a3 c5 | no | 2+2 |
| cyl:8x6 | b2/c3 | a4/b5 | a3 b4 | b3 c4 | yes | 2+2 |
| cyl:8x6 | a2/a3 | c4/c5 | a4 c2 | a5 c3 | no | 2+2 |
| cyl:8x6 | a3/b2 | b5/c4 | b4 c3 | a4 b3 | yes | 2+2 |
| flat:8x6 | b2/c3 | a4/b5 | a3 b4 | b3 c4 | yes | 2+2 |
| flat:8x6 | a3/b2 | b5/c4 | b4 c3 | a4 b3 | yes | 2+2 |

### 2.2 The same groups on other boards (named-group check, kpp and ref3m on the 8 roots; ref3m only for width 9 and more; ref3m collapses promotions)

| board | Z_B | Z_B mirror | Z_C | Z_C mirror |
|---|---|---|---|---|
| flat:7x6 | 0 leaks (root values D) | 0 leaks (root values D) | 16 leaks (root values W) | 16 leaks (root values L) |
| flat:8x6 | 0 leaks (root values D) | 0 leaks (root values D) | 16 leaks (root values W) | 16 leaks (root values L) |
| flat:9x6 | 0 leaks (root values D) | 0 leaks (root values D) | 16 leaks (root values W) | 16 leaks (root values L) |
| flat:5x6 | 0 leaks (root values D) | 0 leaks (root values D) | 16 leaks (root values W) | 16 leaks (root values L) |
| flat:7x7 | 8 leaks (root values L) | 9 leaks (root values L) | 16 leaks (root values W) | 6 leaks (root values L) |
| flat:7x5 | 13 leaks (root values W) | 9 leaks (root values W) | illegal root | illegal root |
| flat:8x8 | 8 leaks (root values L) | 11 leaks (root values L) | 18 leaks (root values WDWDDWWD) | 6 leaks (root values L) |
| cyl:5x6 | 0 leaks (root values D) | 0 leaks (root values D) | 12 leaks (root values D) | 12 leaks (root values D) |
| cyl:6x6 | 0 leaks (root values D) | 0 leaks (root values D) | 8 leaks (root values WLWLWLWL) | 8 leaks (root values WLWLWLWL) |
| cyl:7x6 | 0 leaks (root values D) | 0 leaks (root values D) | 8 leaks (root values WLWLWLWL) | 8 leaks (root values WLWLWLWL) |
| cyl:8x6 | 0 leaks (root values D) | 0 leaks (root values D) | 0 leaks (root values D) | 0 leaks (root values D) |
| cyl:9x6 | 0 leaks (root values D) | 0 leaks (root values D) | 0 leaks (root values D) | 0 leaks (root values D) |
| cyl:10x6 | 0 leaks (root values D) | 0 leaks (root values D) | 8 leaks (root values D) | 8 leaks (root values D) |
| cyl:11x6 | 0 leaks (root values D) | 0 leaks (root values D) | 8 leaks (root values D) | 8 leaks (root values D) |
| cyl:12x6 | 0 leaks (root values D) | 0 leaks (root values D) | 8 leaks (root values D) | 8 leaks (root values D) |
| flat:10x6 | 0 leaks (root values D) | 0 leaks (root values D) | 16 leaks (root values W) | 16 leaks (root values L) |
| flat:12x6 | 0 leaks (root values D) | 0 leaks (root values D) | 16 leaks (root values W) | 16 leaks (root values L) |
| cyl:8x5 | 13 leaks (root values W) | 13 leaks (root values W) | illegal root | illegal root |
| cyl:6x7 | 9 leaks (root values L) | 9 leaks (root values L) | 8 leaks (root values D) | 8 leaks (root values D) |
| cyl:7x7 | 9 leaks (root values L) | 9 leaks (root values L) | 8 leaks (root values D) | 8 leaks (root values D) |
| cyl:8x7 | 9 leaks (root values L) | 9 leaks (root values L) | 4 leaks (root values L) | 4 leaks (root values L) |
| cyl:9x7 | 9 leaks (root values L) | 9 leaks (root values L) | 4 leaks (root values L) | 4 leaks (root values L) |
| cyl:8x8 | 11 leaks (root values L) | 11 leaks (root values L) | 6 leaks (root values L) | 6 leaks (root values L) |

### 2.3 Examples of the smallest non-zero leak counts

| board | pawns | total | White king shuttle | Black king shuttle | White pawns | Black pawns | the non-losing non-shuttle moves (one root) |
|---|---|---|---|---|---|---|---|
| flat:7x6 | 2+2 | 1 | a5/a6 | c5/c6 | a2 b3 | b4 b5 | Ka5b4:W |
| flat:7x6 | 2+2 | 1 | a5/a6 | c5/c6 | a2 c2 | b4 b5 | Ka5b4:D |
| flat:7x6 | 2+3 | 1 | a5/a6 | c5/c6 | a2 b3 | b4 b5 | Ka5b4:W |
| flat:7x6 | 2+3 | 1 | a5/a6 | c5/c6 | a2 c2 | b4 b5 | Ka5b4:D |
| cyl:7x6 | 2+2 | 2 | a1/a2 | c1/c2 | a3 b2 | a4 | Pb2b3:W Pb2b4:W |
| cyl:7x6 | 2+2 | 2 | a1/b1 | b4/c4 | a2 c2 | a3 a5 | Kb1c1:W |
| cyl:7x6 | 3+2 | 1 | a1/a2 | c1/c2 | a3 b2 b4 | a4 b5 | Pb2b3:W |
| cyl:7x6 | 3+2 | 1 | c1/c2 | a1/a2 | b2 b4 c3 | b5 c4 | Pb2b3:W |
| cyl:8x6 | 2+2 | 2 | a1/a2 | c1/c2 | a3 b2 | a4 | Pb2b3:W Pb2b4:W |
| cyl:8x6 | 2+2 | 2 | a5/a6 | c5/c6 | c3 | b5 c4 | Pb5b4:L Pb5b3:L |
| cyl:8x6 | 2+3 | 1 | a5/a6 | c5/c6 | b2 c3 | b3 b5 c4 | Pb5b4:L |
| cyl:8x6 | 2+3 | 1 | c5/c6 | a5/a6 | a3 b2 | a4 b3 b5 | Pb5b4:L |
| cyl:8x6 | 3+2 | 1 | a1/a2 | c1/c2 | a3 b2 b4 | a4 b5 | Pb2b3:W |
| cyl:8x6 | 3+2 | 1 | c1/c2 | a1/a2 | b2 b4 c3 | b5 c4 | Pb2b3:W |
| flat:8x6 | 2+2 | 1 | a5/a6 | c5/c6 | a2 b3 | b4 b5 | Ka5b4:W |
| flat:8x6 | 2+2 | 1 | a5/a6 | c5/c6 | a2 c2 | b4 b5 | Ka5b4:D |
| flat:7x7 | 2+2 | 1 | a6/a7 | c6/c7 | a3 b4 | b5 b6 | Ka6b5:W |
| flat:7x7 | 2+2 | 1 | a6/a7 | c6/c7 | a3 c3 | b5 b6 | Ka6b5:D |

With promotions counted once the counts of total 1 and 2 change a little and those of total 0 do not. The second-enumerator audit counts promotions once (`audit/audit_fresh.txt`): totals 0 / 1 / 2 are 2 / 12 / 6 on flat 7×6 and flat 8×6, 2 / 0 / 8 on cyl:7×6 and 4 / 0 / 4 on cyl:8×6 (the per-piece table above has 4 instead of 6 on the flat boards).
The collapsed-promotion search of the 3 + 2 and 2 + 3 limits and of flat 7×7 (`scripts/queueF_collapse.sh`) was not finished (the lock was never free); the earlier attempt's partial collapsed runs (`logs/c2_*`) agree where they exist (flat 7×6, 2 + 2: 2 / 12 / 6 / 86 for totals 0 to 3).

## 3. Exact under and over groups (class b): the over half of §8 item 2, and Conjecture 4.7

Search: White's king shuttles on a pair z, Black's king stands on one square b0 (K1, K2), at most n_W + n_B pawns on F_Z, four roots; then the freezes at the two Black-to-move roots are followed to the positions q (`over3.py`, written for K26).
The search for under with (n_W, n_B) covers over with (n_B, n_W) by the colour mirror.

**Lemma 4.9 (no king freeze) — PROVED (hand proof; the filter of `over3.py` rests on it, and the unfiltered runs `over2.py` agree).**
*In an exact under group (U1)–(U4) no freeze is a king move that captures nothing.*
*Proof.* Let m be a freeze b0 → b1 that captures nothing, q the position after it. In q Black can play b1 → b0: b0 is empty (the king just left it), no White pawn attacks it (K1), and it is not next to the White king, which has not moved (K2 at the root); no pawn has moved, so there is no e.p. right.
The result is the root with White to move. By (U2) and (U3) the other Black-to-move root has a freeze to a position of value L (White has lost), so that root has value L. At the first root every non-shuttle White move loses at once (U1) and the shuttle leads to the second root, value L.
So the first root has value L: the move b1 → b0 is a legal Black move at q that does not lose at once, and (U4) fails. ∎
So the freeze of an exact group is a pawn move or a king capture of a pawn of the group. (A Black promotion as a freeze is a decisive event, not a group move; those placements are counted separately.)

**Result: no exact under or over group was found in any searched range.** The fresh run of `over3.py` (`scripts/queueF_over.sh`) did not get a slot of the shared lock before the time limit of this attempt; the table therefore lists the earlier attempt's runs (reused; same scripts, same source md5, the fresh two-shuttle and one-shuttle searches that feed them reproduced exactly). Rows from a fresh run appear first if there are any.

| source | board | pawns W+B | files | placements | survivors of (king filter and) (U1)-(U3) at one root | at all four roots | dropped at (U4) | dropped (a freeze is a promotion) | exact groups |
|---|---|---|---|---|---|---|---|---|---|
| earlier attempt, reused (over3.py, king filter) | cyl:8x6 | 2+3 | a-c | 1,517,293 | 23,661 | 20,444 | 13,376 | 7,068 | 0 |
| earlier attempt, reused (over3.py, king filter) | cyl:8x6 | 3+2 | a-c | 1,602,414 | 16,700 | 13,526 | 6,759 | 6,767 | 0 |
| earlier attempt, reused (over3.py, king filter) | cyl:8x6 | 2+2 | a-d | 5,793,156 | 66,476 | 55,331 | 41,169 | 14,162 | 0 |
| earlier attempt, reused (over2.py, NO king filter) | flat:7x6 | 2+2 | a-c | 631,179 | 164,776 | 140,389 | 136,864 | 3,525 | 0 |
| earlier attempt, reused (over2.py, NO king filter) | cyl:7x6 | 2+2 | a-c | 631,179 | 168,920 | 144,411 | 141,545 | 2,866 | 0 |
| earlier attempt, reused (over2.py, NO king filter) | cyl:8x6 | 2+2 | a-c | 631,179 | 168,461 | 144,159 | 141,293 | 2,866 | 0 |
| earlier attempt, reused (over2.py, NO king filter) | flat:8x6 | 2+2 | a-c | 631,179 | 164,776 | 140,389 | 136,864 | 3,525 | 0 |

(Reused, not re-run: four files a–d on cyl:8×6 with at most 2 + 2 pawns, 5,793,156 placements: 66,476 pass the king filter and (U1)–(U3) at one root, 55,331 at all four roots, 41,169 fail (U4), 14,162 have a promotion as the freeze, **0 exact groups**; `logs/over3_cyl_8x6_22_nf4_*`.
The unfiltered runs `over2.py` (no use of Lemma 4.9) on cyl:7×6, cyl:8×6, flat 7×6, flat 8×6 with at most 2 + 2 pawns also give 0 exact groups: `logs/over2_*_22.json`.)

**Loose under/over groups are plentiful, but they are not over_D.** Loose = (U1)–(U3) with exactly one freeze at each Black-to-move root (`over_exact` in the t1 table of section 4): 118 on cyl:7×6, 120 on cyl:8×6, 142 on flat 7×6 and flat 8×6, 586 on flat 7×7 for at most 2 + 2 pawns (see the t1 table; 626 on cyl:8×6 with four files, reused).
After the freeze only White is in zugzwang; Black still has a move that does not lose. Beside contexts Proposition 4.6 (and its mirror) holds in 537 of the 552 premise roots of the fresh sampled run (section 6; 762 of 768 in the earlier attempt's different sample), so the loose groups are not over_D. The failing roots were not diagnosed.

**Verdict on Conjecture 4.7 (P model, COMPUTED-1 as a search; exact boundaries above).**
- First half ("no over-type group with at most 2 + 2 pawns fits on 3 files of the 8×6 cylinder"): **supported**. No exact under/over group exists with at most 2 + 2, 3 + 2 or 2 + 3 pawns on 3 files of cyl:8×6, nor with at most 2 + 2 on cyl:7×6, flat 7×6 and flat 8×6 (the 2 + 2 runs without the king filter); nor with at most 2 + 2 on 4 files of cyl:8×6.
  Not searched for exact under/over: 3 + 2 and 2 + 3 on cyl:7×6 and flat 7×6, and flat 7×7 (the queue for them never got a lock slot).
  Lemma 4.9 shrinks the freeze to pawn moves and king captures.
- Second half ("over is realisable on the cylinder with wider groups"): **neither supported nor refuted.** Nothing wider than 4 files, 3 + 2 pawns, or the pawns-on-F_Z-only setting was searched.

## 4. Exact on and off groups (class c)

Search: White shuttles on z, Black's king on one square (K1, K2), at most n_W + n_B pawns, four roots; `on_strong` = exact on as defined in section 1(c); `on_weak` = only the Black half; the loose under/over column is the one used in section 3.
Black-shuttler versions (exact off) are the colour mirror: the exact off groups for (n_W, n_B) are the exact on groups for (n_B, n_W) with colours swapped.
Fresh runs (`logs/k26f_*_t1_*`):

| board | pawns W+B | placements | exact on (on_strong) | on_weak (Black frozen only) | loose under/over (old class over_exact: (U1)-(U3) as tested there, exactly one freeze at each Black-to-move root; section 3) |
|---|---|---|---|---|---|
| flat:7x6 | 2+2 | 631,179 | 17 | 146,766 | 142 |
| cyl:7x6 | 2+2 | 631,179 | 4 | 152,554 | 118 |
| cyl:7x6 | 2+3 | 1,517,293 | 4 | 244,245 | 167 |
| cyl:7x6 | 3+2 | 1,602,414 | 6 | 604,876 | 216 |
| cyl:8x6 | 2+2 | 631,179 | 4 | 152,262 | 120 |
| flat:8x6 | 2+2 | 631,179 | 17 | 146,766 | 142 |
| flat:7x7 | 2+2 | 2,790,987 | 29 | 681,775 | 586 |

Exact on / loose under groups for 2 + 3 and 3 + 2 pawns: cyl:7×6 4 / 167 and 6 / 216 (fresh run, identical to the earlier attempt); cyl:8×6 6 / 175 and 4 / 198 and flat 7×6 28 / 334 and 34 / 228 (reused from `logs/merged.json`, not re-run).

- **Exact on groups exist on every board searched**: 4 on cyl:7×6 and cyl:8×6 for 2 + 2, up to 34 on flat 7×6 (3 + 2). The union over all pawn limits is 103 exact on groups on the five boards (`logs/exact_groups_all.json`, reused list, re-confirmed fresh by ref3m: section 6),
  of which 78 have no textbook passer. Together with the 10 exact duds that makes the 113 groups of the ref3m confirmation (2 of the 10 duds, Z_C and its mirror, are passer-free).
  The smallest example is `Ka5 Ka6 | kc6 | Pb4 | pb5` on flat 7×6 (White's king shuttles on a5/a6, Black's king on c6, one blocked pair on file b: every Black move loses at once).
- **Beside contexts** (section 6) the P-result equals the D-model prediction for on_D / off_D (Theorem 3.4(b), (c)) at every root on flat 7×6 (260 roots of the on group, 28 of its mirror) and, on the cylinders, at all roots but 9 roots in 3 of 258 sampled on-contexts (fresh sample: 8 roots in 2 contexts on cyl:7×6, 1 root in 1 context on cyl:8×6; the earlier attempt's sample had 12 roots in 5 contexts).
  Examples (`logs/ctx_phase2.json`, earlier sample): P = W where the D-model says L (White's extra king moves help, the direction of Proposition 3.2's inequality) and P = L where the D-model says W (a Black king move that loses alone does not lose beside that context, so (Pun) fails for the frozen king).
  The mismatching contexts have pawns on files f, g (cyl:8×6) or e, f (cyl:7×6), next to the wrap square. They were not diagnosed further.

## 5. Minimum leak count per board (class d), with examples

The minimum total over all placements of a board and pawn limit (counts of totals 0, 1 and 2 are complete, section 1(d); per promotion piece; the same table is in section 2). The 3 + 2 and 2 + 3 results are equal on every board (the colour mirror τ is a symmetry of the P model).

| board | limits | minimum | placements at total 0 | at total 1 | at total 2 | example of the best non-exact placement (total, leak) |
|---|---|---|---|---|---|---|
| flat 7×6 | 2+2 | **0** | 2 (Z_B, mirror) | 12 | 4 | total 1: Ka5/a6, kc5/c6, Pb3 / pb4 pb5, leak Ka5×b4 (Z_A) |
| flat 7×6 | 3+2, 2+3 | **0** | the same 2 | 17 | 13 | |
| flat 8×6 | 2+2 | **0** | 2 (same as flat 7×6) | 12 | 4 | the same placements |
| cyl:7×6 | 2+2 | **0** | 2 (Z_B, mirror) | 0 | 8 | total 2: Ka1/a2, kc1/c2, Pa3 Pb2 / pa4: Pb2–b3 and Pb2–b4 both win |
| cyl:7×6 | 3+2, 2+3 | **0** | the same 2 | 2 | 10 | total 1: Ka1/a2, kc1/c2, Pa3 Pb2 Pb4 / pa4 pb5: Pb2–b3 wins |
| cyl:8×6 | 2+2 | **0** | 4 (Z_B, Z_C, mirrors) | 0 | 4 | total 2: as on cyl:7×6 |
| cyl:8×6 | 3+2, 2+3 | **0** | the same 4 | 2 | 6 | |
| flat 7×7 | 2+2 | **1** | 0 | 12 | 28 | total 1: Ka6/a7, kc6/c7, Pa3 Pb4 / pb5 pb6, leak Ka6×b5 (value W) |

- No exact dud has a third pawn on a side (every exact dud has 2 + 2 pawns), so the 3 + 2 and 2 + 3 searches add no group.
- On flat 7×7 (7 ranks) there is **no** exact dud and the minimum is 1; the next total is 2 (28 placements). The counts are COMPUTED-1 (one solver pair, no second enumerator for 7 ranks).
- With promotions counted once (section 2) the total-1 and total-2 counts of some boards change (a promotion that does not lose then counts 1, not 4), the minimum does not.

## 6. The selected groups: root values, move lists (ref3m too) and small pawn contexts

**Selection (20 groups, `logs/groups_final.json`, chosen by the earlier attempt's `final_select.py`; I audited the choice and kept it):** all 10 exact duds (Z_B and Z_C and their mirrors on the boards where they are exact), 5 exact on groups (passer-free, spread over cyl:7×6, cyl:8×6, flat 7×6),
and 5 *loose* under/over groups (labelled: no exact over group exists, section 3). The first 15 are exact groups. Each group is also tested in its colour-mirror orientation (the mirror of an on group is an off group, of a dud a dud, of a loose under group a loose over group).

**Roots and move lists.** For the 20 groups in both orientations, **240 roots**: `kpp --pmodel --moves` and `ref3m --moves` (fresh builds) agree at every root on the root value and on the complete multiset of (move, value), with promotions normalised: **240 of 240, CHECKED-2**
(`logs/f/confirm/confirm_final.json`; readable lists in `audit/movelists_20groups.txt`; the colour-flip symmetry of the values holds at all of them). The 113 exact groups of the whole search (10 duds and 103 on) were re-verified directly from the definition of the class with ref3m alone:
**113 groups, 492 roots, 0 failures** (`logs/f/confirm/confirm_all.json`); the negative control (Z_A, and Z_B on flat 7×7) fails 9 times as it must.

**Contexts.** A context is a set of White and Black pawns on files at distance 2 or more from F_Z (files f, g on flat 7×6 and cyl:8×6; e, f on cyl:7×6), at most 2 + 2 pawns on ranks 2..H−1, no e.p. right at the root. At every root (king state × side to move)
the P value (`kpp --pmodel`, ref3m for a part) is compared with the D-model prediction r(G ⊞ Z) of `dmodel.py` (an independent implementation of Definitions 3.1 and 4.4 and Theorem 3.4; cross-checked against K14's D solver: 885 contexts, 7,080 roots, 0 differences, `logs/dm_crosscheck.log`):
dud for dud groups (Theorem 3.4(a)), on or off for exact on/off groups (Theorem 3.4(b), (c)), the over/under reservoir for the loose groups (Proposition 4.6 and its mirror: if White wins G moving second then White wins G ⊞ over_D with either side to move).
The sample for the orientation as given is the empty context plus a random sample stratified by the number of context pawns (0 to 2, 3, 4; shares 35, 40, 25 per cent), half drawn uniformly and half among the contexts whose D-prediction is decisive (`--nbase 66`), so at least 60 contexts per group; the colour-flipped orientation gets about 7 (`--nflip 6`; 21 in the earlier runs).

Sampled contexts (fresh run, 20 groups, both orientations; reading = the D-model reservoir that was compared):

| group (orientation ~ = colour mirror) | board | kings W / B | pawns W / B | reading | ctx files | contexts | roots | roots = D-model | contexts with a difference | ref3 roots (mismatches) | Prop 4.6 conclusion holds / premise roots |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dud_cyl7x6_a3b4-b3c4_b2c3 | cyl:7x6 | b2 c3 / a4 b5 | a3 b4 / b3 c4 | dud | ef | 65 | 520 | 520 | 0 | 96 (0) | 0 / 0 |
| dud_cyl7x6_a3b4-b3c4_b2c3~ | cyl:7x6 | a3 b2 / b5 c4 | b4 c3 / a4 b3 | dud | ef | 7 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| dud_cyl7x6_b4c3-a4b3_a3b2 | cyl:7x6 | a3 b2 / b5 c4 | b4 c3 / a4 b3 | dud | ef | 67 | 536 | 536 | 0 | 96 (0) | 0 / 0 |
| dud_cyl7x6_b4c3-a4b3_a3b2~ | cyl:7x6 | b2 c3 / a4 b5 | a3 b4 / b3 c4 | dud | ef | 7 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| dud_cyl8x6_a2c4-a3c5_c2c3 | cyl:8x6 | c2 c3 / a4 a5 | a2 c4 / a3 c5 | dud | fg | 63 | 504 | 492 | 3 | 96 (0) | 0 / 0 |
| dud_cyl8x6_a2c4-a3c5_c2c3~ | cyl:8x6 | a3 a2 / c5 c4 | a4 c2 / a5 c3 | dud | fg | 7 | 56 | 48 | 1 | 56 (0) | 0 / 0 |
| dud_cyl8x6_a4c2-a5c3_a2a3 | cyl:8x6 | a2 a3 / c4 c5 | a4 c2 / a5 c3 | dud | fg | 67 | 536 | 512 | 4 | 96 (0) | 0 / 0 |
| dud_cyl8x6_a4c2-a5c3_a2a3~ | cyl:8x6 | c3 c2 / a5 a4 | a2 c4 / a3 c5 | dud | fg | 7 | 56 | 52 | 1 | 56 (0) | 0 / 0 |
| dud_cyl8x6_a3b4-b3c4_b2c3 | cyl:8x6 | b2 c3 / a4 b5 | a3 b4 / b3 c4 | dud | fg | 64 | 512 | 512 | 0 | 96 (0) | 0 / 0 |
| dud_cyl8x6_a3b4-b3c4_b2c3~ | cyl:8x6 | a3 b2 / b5 c4 | b4 c3 / a4 b3 | dud | fg | 7 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| dud_cyl8x6_b4c3-a4b3_a3b2 | cyl:8x6 | a3 b2 / b5 c4 | b4 c3 / a4 b3 | dud | fg | 63 | 504 | 504 | 0 | 96 (0) | 0 / 0 |
| dud_cyl8x6_b4c3-a4b3_a3b2~ | cyl:8x6 | b2 c3 / a4 b5 | a3 b4 / b3 c4 | dud | fg | 7 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| dud_flat7x6_a3b4-b3c4_b2c3 | flat:7x6 | b2 c3 / a4 b5 | a3 b4 / b3 c4 | dud | fg | 65 | 520 | 520 | 0 | 96 (0) | 0 / 0 |
| dud_flat7x6_a3b4-b3c4_b2c3~ | flat:7x6 | a3 b2 / b5 c4 | b4 c3 / a4 b3 | dud | fg | 7 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| dud_flat7x6_b4c3-a4b3_a3b2 | flat:7x6 | a3 b2 / b5 c4 | b4 c3 / a4 b3 | dud | fg | 67 | 536 | 536 | 0 | 96 (0) | 0 / 0 |
| dud_flat7x6_b4c3-a4b3_a3b2~ | flat:7x6 | b2 c3 / a4 b5 | a3 b4 / b3 c4 | dud | fg | 7 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| dud_flat8x6_a3b4-b3c4_b2c3 | flat:8x6 | b2 c3 / a4 b5 | a3 b4 / b3 c4 | dud | fg | 66 | 528 | 528 | 0 | 96 (0) | 0 / 0 |
| dud_flat8x6_a3b4-b3c4_b2c3~ | flat:8x6 | a3 b2 / b5 c4 | b4 c3 / a4 b3 | dud | fg | 7 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| dud_flat8x6_b4c3-a4b3_a3b2 | flat:8x6 | a3 b2 / b5 c4 | b4 c3 / a4 b3 | dud | fg | 65 | 520 | 520 | 0 | 96 (0) | 0 / 0 |
| dud_flat8x6_b4c3-a4b3_a3b2~ | flat:8x6 | b2 c3 / a4 b5 | a3 b4 / b3 c4 | dud | fg | 7 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| on_strong_cyl7x6_a2b3-a3b4_a4a5 | cyl:7x6 | a4 a5 / c5 | a2 b3 / a3 b4 | on | ef | 64 | 256 | 256 | 0 | 48 (0) | 0 / 0 |
| on_strong_cyl7x6_a2b3-a3b4_a4a5~ | cyl:7x6 | c2 / a3 a2 | a4 b3 / a5 b4 | off | ef | 7 | 28 | 28 | 0 | 28 (0) | 0 / 0 |
| on_strong_cyl7x6_a3b2-a4c5_b6c6 | cyl:7x6 | b6 c6 / c4 | a3 b2 / a4 c5 | on | ef | 63 | 252 | 244 | 2 | 48 (0) | 0 / 0 |
| on_strong_cyl7x6_a3b2-a4c5_b6c6~ | cyl:7x6 | c3 / b1 c1 | a3 c2 / a4 b5 | off | ef | 7 | 28 | 28 | 0 | 28 (0) | 0 / 0 |
| on_strong_cyl8x6_a2b3-a3b4_a4a5 | cyl:8x6 | a4 a5 / c5 | a2 b3 / a3 b4 | on | fg | 65 | 260 | 259 | 1 | 48 (0) | 0 / 0 |
| on_strong_cyl8x6_a2b3-a3b4_a4a5~ | cyl:8x6 | c2 / a3 a2 | a4 b3 / a5 b4 | off | fg | 7 | 28 | 28 | 0 | 28 (0) | 0 / 0 |
| on_strong_cyl8x6_a3b2-a4c5_b6c6 | cyl:8x6 | b6 c6 / c4 | a3 b2 / a4 c5 | on | fg | 66 | 264 | 264 | 0 | 48 (0) | 0 / 0 |
| on_strong_cyl8x6_a3b2-a4c5_b6c6~ | cyl:8x6 | c3 / b1 c1 | a3 c2 / a4 b5 | off | fg | 7 | 28 | 28 | 0 | 28 (0) | 0 / 0 |
| on_strong_flat7x6_b4-b5_a5a6 | flat:7x6 | a5 a6 / c6 | b4 / b5 | on | fg | 65 | 260 | 260 | 0 | 48 (0) | 0 / 0 |
| on_strong_flat7x6_b4-b5_a5a6~ | flat:7x6 | c1 / a2 a1 | b2 / b3 | off | fg | 7 | 28 | 28 | 0 | 28 (0) | 0 / 0 |
| over_cyl7x6_a3c3-a4b5_b6c6 | cyl:7x6 | b6 c6 / c4 | a3 c3 / a4 b5 | under | ef | 67 | 268 | 268 | 0 | 48 (0) | 116 / 116 |
| over_cyl7x6_a3c3-a4b5_b6c6~ | cyl:7x6 | c3 / b1 c1 | a3 b2 / a4 c4 | over | ef | 7 | 28 | 28 | 0 | 28 (0) | 12 / 12 |
| over_cyl7x6_a2c3-a5c4_c1c2 | cyl:7x6 | c1 c2 / b5 | a2 c3 / a5 c4 | under | ef | 65 | 260 | 250 | 3 | 48 (0) | 76 / 84 |
| over_cyl7x6_a2c3-a5c4_c1c2~ | cyl:7x6 | b2 / c6 c5 | a2 c3 / a5 c4 | over | ef | 7 | 28 | 28 | 0 | 28 (0) | 8 / 8 |
| over_cyl8x6_a3-a4b5_a5b4 | cyl:8x6 | a5 b4 / c6 | a3 / a4 b5 | under | fg | 66 | 264 | 259 | 2 | 48 (0) | 72 / 72 |
| over_cyl8x6_a3-a4b5_a5b4~ | cyl:8x6 | c1 / a2 b3 | a3 b2 / a4 | over | fg | 7 | 28 | 27 | 1 | 28 (0) | 19 / 20 |
| over_cyl8x6_a3b4-a4b5_a1a2 | cyl:8x6 | a1 a2 / c1 | a3 b4 / a4 b5 | under | fg | 65 | 260 | 258 | 1 | 48 (0) | 106 / 108 |
| over_cyl8x6_a3b4-a4b5_a1a2~ | cyl:8x6 | c6 / a6 a5 | a3 b2 / a4 b3 | over | fg | 7 | 28 | 24 | 1 | 28 (0) | 16 / 20 |
| over_flat7x6_c3-b5c4_c1c2 | flat:7x6 | c1 c2 / a1 | c3 / b5 c4 | under | fg | 65 | 260 | 256 | 2 | 48 (0) | 100 / 100 |
| over_flat7x6_c3-b5c4_c1c2~ | flat:7x6 | a6 / c6 c5 | b2 c3 / c4 | over | fg | 7 | 28 | 28 | 0 | 28 (0) | 12 / 12 |

groups tested in the sampled runs: 20 group ids (base orientation) + 20 colour mirrors; base orientations with >= 60 contexts: 20 of 20

Aggregates by reading, board, files:

| reading | board | files | group-orientations | contexts | roots | roots = prediction | contexts differ | ref3 roots (mismatches) | Prop 4.6 conclusion holds / premise roots |
|---|---|---|---|---|---|---|---|---|---|
| dud | cyl:7x6 | ef | 4 | 146 | 1168 | 1168 | 0 | 304 (0) | 0 / 0 |
| dud | cyl:8x6 | fg | 4 | 141 | 1128 | 1128 | 0 | 304 (0) | 0 / 0 |
| dud | flat:7x6 | fg | 4 | 146 | 1168 | 1168 | 0 | 304 (0) | 0 / 0 |
| dud | flat:8x6 | fg | 4 | 145 | 1160 | 1160 | 0 | 304 (0) | 0 / 0 |
| dud(blocked, Z_C-type) | cyl:8x6 | fg | 4 | 144 | 1152 | 1104 | 9 | 304 (0) | 0 / 0 |
| off | cyl:7x6 | ef | 2 | 14 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| off | cyl:8x6 | fg | 2 | 14 | 56 | 56 | 0 | 56 (0) | 0 / 0 |
| off | flat:7x6 | fg | 1 | 7 | 28 | 28 | 0 | 28 (0) | 0 / 0 |
| on | cyl:7x6 | ef | 2 | 127 | 508 | 500 | 2 | 96 (0) | 0 / 0 |
| on | cyl:8x6 | fg | 2 | 131 | 524 | 523 | 1 | 96 (0) | 0 / 0 |
| on | flat:7x6 | fg | 1 | 65 | 260 | 260 | 0 | 48 (0) | 0 / 0 |
| over | cyl:7x6 | ef | 2 | 14 | 56 | 56 | 0 | 56 (0) | 20 / 20 |
| over | cyl:8x6 | fg | 2 | 14 | 56 | 51 | 2 | 56 (0) | 35 / 40 |
| over | flat:7x6 | fg | 1 | 7 | 28 | 28 | 0 | 28 (0) | 12 / 12 |
| under | cyl:7x6 | ef | 2 | 132 | 528 | 518 | 3 | 96 (0) | 192 / 200 |
| under | cyl:8x6 | fg | 2 | 131 | 524 | 517 | 3 | 96 (0) | 178 / 180 |
| under | flat:7x6 | fg | 1 | 65 | 260 | 256 | 2 | 48 (0) | 100 / 100 |

**Exhaustive small contexts (reused from the earlier attempt: its runs `logs/exh/`, kpp, complete; the fresh runs did not get a lock slot).** Every placement of at most 3 context pawns, either colour, on the context files, ranks 2..H−1, each at the 8 roots of the group (unbiased rates):

| group | board | context files | shards done | contexts | contexts with a difference | roots | roots that differ |
|---|---|---|---|---|---|---|---|
| ZB | cyl:7x6 | ef | 4 | 577 | 0 | 4616 | 0 |
| ZB | cyl:8x6 | efg | 12 | 2049 | 0 | 16392 | 0 |
| ZB | flat:7x6 | efg | 12 | 2049 | 0 | 16392 | 0 |
| ZC | cyl:8x6 | efg | 12 | 2049 | 131 | 16392 | 754 |

By number of context pawns (source column: the fresh run if all its shards exist, else the earlier attempt's run):

| group | board | files | source | contexts with 0, 1, 2, 3 pawns | of which differ from the dud_D prediction (0, 1, 2, 3 pawns) |
|---|---|---|---|---|---|
| ZB | cyl:8x6 | efg | earlier attempt | 1, 24, 264, 1760 | 0, 0, 0, 0 |
| ZC | cyl:8x6 | efg | earlier attempt | 1, 24, 264, 1760 | 0, 0, 35, 96 |
| ZB | cyl:7x6 | ef | earlier attempt | 1, 16, 112, 448 | 0, 0, 0, 0 |
| ZB | flat:7x6 | efg | earlier attempt | 1, 24, 264, 1760 | 0, 0, 0, 0 |

- **Z_B equals dud_D in every one of these contexts** (cyl:8×6 files e–g, cyl:7×6 files e–f, flat 7×6 files e–g): 0 contexts and 0 roots differ. This is COMPUTED-1 (kpp; the sampled runs were partly re-solved with ref3m, 0 mismatches).
- **Z_C does not**: no context of one pawn differs, but 35 of 264 two-pawn and 96 of 1,760 three-pawn contexts do (131 of 2,049; 754 of 16,392 roots). The differing contexts always have pawns of both colours in the context files (examples: Pe2 pe3, Pe2 pe5, Pe3 pe4, Pf2 pf3). The smallest example is Pe2 pe3 (see section 2).
- Exact on/off groups agree with Theorem 3.4(b)/(c) except in the few contexts discussed in section 4. The loose under/over groups agree with the over_D reading at almost every root; Proposition 4.6's conclusion fails at 15 of 552 premise roots in the fresh sample (6 of 768 in the earlier one), which is why they are not over_D (section 3).

## 7. Verdicts (P model; labels as defined below; every boundary is explicit)

**Open question 2, first half: do dud groups without a pawn break exist on the cylinder? YES, in P.**
- cyl:7×6: Z_B and its mirror. cyl:8×6: Z_B, Z_C and their mirrors. Each has every non-shuttle move losing at once at all 8 roots (no pawn move that does not lose at once exists, so there is no pawn break).
- Z_C has no pawn move at all and no textbook passer; Z_B has pawn pushes at its roots (b4–b5 or a3–a4 for White, c4–c3 or b3–b2 for Black) that all lose at once, and all four of its pawns are textbook passers (each blocked by a king in P).
- Roots and move lists: **CHECKED-2** (kpp and ref3m, fresh builds). The exhaustive searches: **CHECKED-2** for at most 2 + 2 pawns on flat 7×6, flat 8×6, cyl:7×6, cyl:8×6 (a second enumerator and a second solver on all four, a third enumerator on two boards, 2.4 to 2.8 million root move lists per board, 0 differences); **COMPUTED-1** for 3 + 2, 2 + 3 and flat 7×7 (the 3 + 2 / 2 + 3 results are partly fresh, partly reused, section 8).
- Exact boundary: F_Z = {a, b, c}; at most 2 + 2 (five boards), 3 + 2 and 2 + 3 (flat 7×6, cyl:7×6, cyl:8×6); every placement with K1 and K2 and both kings on adjacent pairs, no cut-off. Nothing else is exact there. Not searched: other F_Z on flat boards, 4 or more files for duds, more than 3 + 2 pawns, 5 or 7 or 8 ranks beyond flat 7×7 (and Z_B and Z_C themselves fail on those).
- No hand proof on the cylinder (K27's 26 certificates cover flat 7×6 only). In chess nothing is claimed (the one cap-1 probe of Z_C, section 2, gives bounds (W, L): undecided).
- "No dud on the cylinder" (the earlier scratch statement of §5.3 and Appendix A) is **false in P**.

**Open question 2, second half, and Conjecture 4.7: no exact over or under group exists in any searched range (COMPUTED-1).** First half of the conjecture supported; second half (wider groups) neither supported nor refuted. Section 3 has the exact boundaries and Lemma 4.9 (PROVED).

**Exact on and off groups exist on every board searched, passer-free ones included; beside contexts they agree with Theorem 3.4(b), (c) except in a few contexts where (Pun) fails** (sections 4 and 6; COMPUTED-1).

**Z_B beside contexts:** equal to dud_D in every one of the exhaustive ≤ 3-pawn contexts (section 6). **Z_C is not** a two-shuttle component beside every context.

## 8. What was reused, what was re-run, what was audited

**What I found in the directory.** Earlier attempts (the task says three were stopped, the last by the reboot) had left `scripts/`, `logs/` (files dated 2026-10-27 16:14 to 2026-10-28 03:44), a `summary.json` and an `EDITS.md` (both written 2026-10-28 02:28 to 02:31),
and `verify/` (a from-scratch enumerator that uses ref3m only; 2026-10-28 02:34 to 03:44), but **no FINDINGS.md**. The machine's uptime shows the reboot was at about 2026-10-27 20:43, so those files come from runs after it; I did not rely on any process or PID from them.
This attempt audited those files and did the following.

**Reused after audit (read, and every number below that comes from them was either re-computed fresh or is marked "reused").**
- Scripts: `scripts/k26lib.py` (geometry, enumeration, classifier; read in full), `search.py` (t2 and t1 searches; read in full), `over3.py` (exact under/over; read in full, the king-freeze filter is Lemma 4.9, re-proved below),
  `enum2.py` (second enumerator, read in full), `audit_s1.py`, `audit_t1.py`, `confirm.py`, `confirm_all.py`, `ctxtest.py`, `ctx_exh.py`, `dmodel.py`, `final_ctx.py`, `build_edits.py`, and the referee's `verify/scripts/my_t2.py` (third enumerator, read in full).
- Logs of the earlier attempt that were **not** re-run here (marked "reused" where they appear): the four-file search (`logs/cyl_8x6_22_t1_nf4_*`, `logs/over3_cyl_8x6_22_nf4_*`, and the earlier `over2_*` runs without the king filter), the sampled context tables for the other 26 − 20 group ids and the older runs of the exhaustive contexts (`logs/exh/`, `logs/ctx_*`), `logs/zc_boards*` (widths beyond 10), the first audit (`logs/audit_*`, `logs/audit1_*`), `verify/logs/`.
- The old `EDITS.md` was re-checked: all ten OLD blocks occur exactly once in the current LOOPY.md (`scripts/build_edits.py --check-only`), and the new one is built from this attempt's numbers.

**Rebuilt by me:** all four binaries (`bin/kp`, `bin/kpp`, `bin/ref3`, `bin/ref3m`), from the sources whose md5 are: kpsolve.c 8ff499658aa67448c89ad0955dfcbcfe, kp_p.c f668d4d4861e1d89792245632e01516c,
ref3.cpp a9cd9ed267e3016c789138d86974d658, ref3m.cpp 1b0c8cd670ab54a9e3b385e14717cd63 (the same as in the earlier attempt's `summary.json`). Binaries are deleted at the end.

**Re-run fresh with the rebuilt binaries (tag prefix `k26f_`; `logs/f/`):** the two-shuttle (t2) and one-shuttle (t1) searches for at most 2 + 2 pawns on flat 7×6, cyl:7×6, cyl:8×6, flat 8×6 and flat 7×7; the t2 searches for 3 + 2 and 2 + 3 on cyl:8×6,
for 2 + 3 on flat 7×6 and for 3 + 2 on cyl:7×6; the t1 searches for 3 + 2 and 2 + 3 on cyl:7×6; the second-enumerator audits of both types (≤ 2 + 2); the ref3m confirmation of every exact group; the sampled contexts of the 20 selected groups. `audit/compare_fresh.txt` compares each fresh result with the earlier attempt's merged result:
candidate counts, stage-1 histograms, class counts and the *sets* of exact groups are identical on every line that was re-run.
**Not re-run (the shared lock was held by other jobs for most of the time; the chains `scripts/queueF*.sh` were killed by me at the end by their recorded PIDs, so nothing is left running):**
the t2 searches cyl:7×6 2 + 3 and flat 7×6 3 + 2 (colour mirrors of searches that were re-run, with equal counts in the earlier attempt); the t1 searches for 3 + 2 and 2 + 3 on cyl:8×6 and flat 7×6 (their counts are quoted in section 4 as reused);
the exact under/over searches (`over3.py`, `over2.py`); the collapsed-promotion searches; the exhaustive ≤ 3-pawn contexts; the third-enumerator run for flat 7×7. All of these are reused from the earlier attempt and are labelled so where they appear.

**Independent audits of this attempt.**
- A from-scratch candidate counter (`audit/count_cands.py`, no solver, no K26 code): 817,270 (2+2, H = 6), 1,886,421 (3+2 and 2+3, H = 6), 4,040,080 (2+2, H = 7) two-shuttle placements; 631,179, 1,602,414, 1,517,293 and 2,790,987 one-shuttle placements.
  All equal the counts of the searches (`audit/count_cands.log`).
- Three implementations of the two-shuttle search agree on every count of total leaks 0, 1, 2 for 2 + 2 on flat 7×6 and cyl:8×6: `search.py` (k26lib + kpp), `enum2.py` + `audit_s1.py` (kpp and ref3m on the same roots, full move lists compared), and the referee's `my_t2.py` (own enumerator, ref3m only).
- Negative control: `confirm_all.py` run on two groups that are *not* exact (Z_A, and Z_B placed on flat 7×7) reports 9 failures (`logs/f/confirm/negcontrol.json`); on the 113 found groups it reports 0.
- The passer flags of `k26lib` equal `cylcgt.pawns.passed` on all 2 + 2 placements of H = 6 and 7 (`logs/check_passer.log`).

**Fresh second-enumerator and second-solver audit (`audit/audit_fresh.txt`; both solvers run on the same roots, complete move lists compared, promotions normalised to one entry per push or capture, 8 shards per board):**

```
t1 cyl:7x6   shards 8/8 placements 631,179 roots compared 1,942,330 | value mismatches 0, move-list mismatches 0 | classes {'on_weak': 152554, 'over_pre': 392, 'over_pre_no_passer': 32, 'on_strong': 4, 'on_strong_no_passer': 4}
t1 cyl:8x6   shards 8/8 placements 631,179 roots compared 1,940,730 | value mismatches 0, move-list mismatches 0 | classes {'on_weak': 152262, 'over_pre': 398, 'over_pre_no_passer': 38, 'on_strong': 4, 'on_strong_no_passer': 4}
t1 flat:7x6  shards 8/8 placements 631,179 roots compared 1,917,022 | value mismatches 0, move-list mismatches 0 | classes {'over_pre': 508, 'over_pre_no_passer': 73, 'on_weak': 146766, 'on_strong': 17, 'on_strong_no_passer': 14}
t2 cyl:7x6   shards 8/8 placements 817,270 roots compared (full move lists) 2,424,988 | value mismatches 0, move-list mismatches 0, leak-count disagreements 0 | total0 kpp/ref3m 2/2 total1 0/0 total2 8/8
t2 cyl:8x6   shards 8/8 placements 817,270 roots compared (full move lists) 2,420,716 | value mismatches 0, move-list mismatches 0, leak-count disagreements 0 | total0 kpp/ref3m 4/4 total1 0/0 total2 4/4
t2 flat:7x6  shards 8/8 placements 817,270 roots compared (full move lists) 2,754,108 | value mismatches 0, move-list mismatches 0, leak-count disagreements 0 | total0 kpp/ref3m 2/2 total1 12/12 total2 6/6
t2 flat:8x6  shards 8/8 placements 817,270 roots compared (full move lists) 2,754,108 | value mismatches 0, move-list mismatches 0, leak-count disagreements 0 | total0 kpp/ref3m 2/2 total1 12/12 total2 6/6
```

The older audit (`logs/audit_merged.json`) has exactly the same counts. The third implementation (the referee's `verify/scripts/my_t2.py`, ref3m only, own enumerator and leak classifier; `verify/logs/my_*.json`, reused) gives, for 2 + 2:
flat 7×6: 817,270 placements, totals 0 / 1 / 2 = 2 / 12 / 6; cyl:8×6: 817,270 placements, totals 0 / 1 / 2 = 4 / 0 / 4 (promotions once). The same as the other two.

## 9. Labels

- PROVED: Lemma 4.9 (section 3; hand proof, re-derived by me against the definitions; its use in `over3.py` is also checked by the unfiltered runs). Nothing else in this note is proved by hand.
- CHECKED-2: the 8 roots and complete move lists of every exact group (kpp and ref3m, 113 groups, 492 roots; 20 groups in both orientations, 240 roots with full move lists); the exhaustive two-shuttle search for ≤ 2 + 2 pawns on flat 7×6, flat 8×6, cyl:7×6, cyl:8×6 (enum2 + kpp + ref3m: 0 differences on every value and move list).
- COMPUTED-1: all other search counts (3 + 2, 2 + 3, flat 7×7, the one-shuttle and under/over searches, the four-file search; partly reused, section 8), and every context result (the D-model prediction is an independent implementation, but the P values come from kpp, partly re-solved with ref3m).
- CONJECTURE: that Z_B is exactly two-shuttle in P in every context; that Z_B is exact on the cylinder in the sense of a hand proof; "over is realisable on the cylinder with wider groups".
- Solver results are never PROVED.

## 10. Reproduce (all paths under `kings/delegate/out/K26/`; `PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames`, python `/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python`)

- Build: `cc -O2 -o bin/kpp ../K7/scripts/draft/kp_p.c -lpthread`, `c++ -O2 -std=c++17 -o bin/ref3m ../K23/verify/ref3m.cpp`, also `bin/kp` from `kings/kpsolve.c` and `bin/ref3` from `ref3.cpp`.
- Z_B / Z_C roots: `printf 'Kb2 ka4 Pa3 Pb4 pb3 pc4 w -\nKb2 ka4 Pa3 Pb4 pb3 pc4 b -\n' | bin/kpp --board cyl:7x6 --ep on --promote QRBN --cap 1 --pmodel --moves` and `... | bin/ref3m --board cyl:7x6 --moves` (for flat boards `--board flat7x6` with ref3m); Z_C: `Kc2 ka4 Pa2 Pc4 pa3 pc5 w -` on `cyl:8x6`.
  All eight roots of the four named groups on three boards: `audit/movelists.sh`; on 32 boards: `audit/named_groups.py`.
- Two-shuttle search (class a, d): `scripts/search.py --board cyl:8x6 --nw 2 --nb 2 --type t2 --tmax 12 [--shard i/n] --tag NAME` (through `../../heavy.sh`), output `logs/NAME_summary.json`, `logs/NAME_groups.jsonl`. `--type t1` is the one-shuttle search (classes c and loose). `K26_COLLAPSE_PROMO=1` counts promotions once.
  The whole fresh set: `scripts/queueF.sh`, `scripts/queueF_over.sh`, `scripts/queueF_collapse.sh`, `scripts/queueF_ctx.sh`, `audit/queue_audit.sh`, `audit/queue_audit1.sh`.
- Exact under/over (class b): `scripts/over3.py --board cyl:8x6 --nw 2 --nb 2 [--nf 4] [--shard i/n] --tag NAME` (output `logs/NAME.json`).
- Counts without a solver: `audit/count_cands.py H nW nB`. Comparison of fresh and reused runs: `audit/compare_fresh.py`. Audits: `audit/audit_s1_fresh.py`, `audit/audit_t1_fresh.py`, merged by `audit/audit_merge_fresh.py`.
- Confirmation of exact groups with ref3m: `scripts/confirm_all.py`, `scripts/confirm.py logs/groups_final.json OUT.json`. Contexts: `scripts/ctxtest.py groups.json OUT.json --nbase 66 --nflip 6 --ncheck 12 --seed 3`, `scripts/ctx_exh.py ZB cyl:8x6 efg 3 i/12 OUT.json`.
- Tables: `audit/make_tables.py`, `audit/final_ctx_fresh.py`. `summary.json`: `audit/make_summary.py`. `EDITS.md`: `scripts/build_edits.py`.

## 11. Not done

- A hand proof of Z_B on the cylinder or of Z_C; chess results for Z_C beyond the cap-1 probe; the five open chess deviations of Z_B (K28).
- F_Z elsewhere on a flat board, more than four files, more than 3 + 2 pawns, king groups with a king outside F_Z, groups with both kings on single squares (zero-type), 7 or more ranks for duds beyond flat 7×7.
- A diagnosis of the six roots where Proposition 4.6 fails for loose groups and of the on-group context mismatches (section 4).
- Flat 8×6 gives the same counts as flat 7×6, flat 7×7 was searched for 2 + 2 only.

