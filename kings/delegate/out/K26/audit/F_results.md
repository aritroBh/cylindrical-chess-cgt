## 2. Exact two-shuttle groups (class a): LOOPY §8 item 2, the dud half

Search: every placement of F_Z = {a, b, c} with the kings on adjacent pairs (K1, K2), at most n_W + n_B pawns, no cut-off, both colours' shuttles, 8 roots per placement.
Counts of placements: 817,270 for 2 + 2 (H = 6), 1,886,421 for 3 + 2 and for 2 + 3 (H = 6), 4,040,080 for 2 + 2 (H = 7); all re-counted by `audit/count_cands.py`.
Fresh runs of this attempt (`logs/k26f_*`, merged by `audit/make_tables.py`, compared with the reused runs by `audit/compare_fresh.py`):

@@T2_FRESH@@

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

@@DUD_LIST@@

### 2.2 The same groups on other boards (named-group check, kpp and ref3m on the 8 roots; ref3m only for width 9 and more; ref3m collapses promotions)

@@NAMED@@

### 2.3 Examples of the smallest non-zero leak counts

@@LEAK_EX@@

With promotions counted once the counts of total 1 and 2 change a little and those of total 0 do not. The second-enumerator audit counts promotions once (`audit/audit_fresh.txt`): totals 0 / 1 / 2 are 2 / 12 / 6 on flat 7×6 and flat 8×6, 2 / 0 / 8 on cyl:7×6 and 4 / 0 / 4 on cyl:8×6 (the per-piece table above has 4 instead of 6 on the flat boards).
The collapsed-promotion search of the 3 + 2 and 2 + 3 limits and of flat 7×7 (`scripts/queueF_collapse.sh`) was not finished (the lock was never free); the earlier attempt's partial collapsed runs (`logs/c2_*`) agree where they exist (flat 7×6, 2 + 2: 2 / 12 / 6 / 86 for totals 0 to 3).
