# K15 + K26 merge notes (LOOPY §8 open question 2, Conjecture 4.7)

Merger, 2026-10-29. Files written: `EDITS_MERGED.md` (9 blocks), `LOOPY_merged_check.md` (the edits applied to a copy of the current
`kings/theory/LOOPY.md`), `work/` (two small ref3m checks, below). Nothing else was written. The ref3m binary was built from
`kings/delegate/out/K23/verify/ref3m.cpp` (md5 1b0c8cd670ab54a9e3b385e14717cd63, the md5 the K26 referee lists) into `bin/` and deleted after use.

## 1. Sources and how they were combined

| block | K15 | K26 | merged |
|---|---|---|---|
| status row P3.2′ tail | standing | referee | one block, rebased on K28's row |
| status row C4.7 | standing | referee | one block |
| §3 loopy kings text | standing | standing | one block, rebased on K28's text |
| Conjecture 4.7 (+ Def. 4.8, Lemma 4.9) | referee | referee | one block |
| §5.3 scratch evidence | none | standing | K26's block, with K15's identification of Z_C added |
| §5.7 cylinder bullet | standing | referee | one block |
| §7 dud bullet | standing | standing | one block |
| §8 item 2 | referee (whole item) | referee (head) + standing (tail) | one block for the whole item, K28's chess sentence kept verbatim |
| Appendix A group search | referee | standing | one block |

Four OLD texts of the sources occur 0 times now because K28 (commit 2061cea4) rewrote them: the P3.2′ row tail, the §3 text, §8 item 2 (whole item, head
and tail). All merged OLDs are taken from the current file. Result: 9 applied, 0 rejected; the number of table cells per row is unchanged.

## 2. Reconciliation

### 2.1 Definitions of "dud"

- **K26, exact (two-shuttle).** F_Z = {a, b, c}, both kings on adjacent pairs, four combined king states, pawns on F_Z; every non-shuttle move of
  either side loses at once (by value) in plain P, at all 8 roots (total leak count 0). This is the empty-context hypothesis of Proposition 3.2′.
- **K15, dud in plain P (reading B).** In the closure of the root under the safe (drawing) moves of both sides, every state has at least one safe move
  for each side, and there is no check, no winning move and no safe king move off the group files. A state may have several safe moves and the closure
  may have more than four states.
- **K15, dud against free passes (reading A).** The same with passes allowed; a deviation must lose even when the deviator may pass. Stricter for the
  deviations, not nested with B in a stalemate corner case (K15 §2.1). Z_B is B but not A; G8a, G8b are both.

So an exact group of K26 is a K15 reading-B dud group whose closure is its four king states with exactly one safe move per side and state. The converse
fails (for example D2: White has two drawing king moves at `Ka1 ka4 Pb4 Pc3 pb3 pc4`, below). "Exactly two-shuttle" in LOOPY means K26's notion.

### 2.2 Scopes

- **Does K26's search exclude G8a, G8b by scope? Yes.** Their pawns stand on files a and e, with the kings on b–d, so the group spans five files in either
  direction on cyl:8×6. K26's dud search puts all pawns (and the kings) on F_Z = {a, b, c}. K26's four-file run (a–d) was an under/over search only.
- **Would K15's search have seen Z_C? Yes, and it did.** Z_C (cyl:8×6, kings c2/c3 and a4/a5, Pa2 Pc4 / pa3 pc5) has 2 + 2 pawns on three files and no
  passer for `cylcgt.passed`, inside K15's cyl:8×6 F = 3 ranges. K15's `fin2/dud_groups.md`, cyl:8×6 #38, is `Ka2 kc4 Pa4 Pc2 pa5 pc3`, labelled "B, no
  passer": this is Z_C under the file mirror a↔c (it is literally K26's `zcm` in `K26/verify/scripts/roots.py`). K15 lists Z_B too (cyl:7×6 #35 and
  cyl:8×6 #33, `Ka3 kb5 Pb4 Pc3 pa4 pb3`, the colour flip of Z_B).
- **Beside contexts both find Z_C is not dud_D.** K15: 46 of 192 context positions disagree for #38 (`dud_groups.md`), and with Pe2 pe3 beside #38 all four king
  states are W (`ref3`, K15b, VERIFY_K15b 3.6). K26: 131 of 2,049 contexts on files e–g, Pe2 pe3 beside Z_C gives (W, W) (CHECKED-2, K26 VERIFY claim 4). The
  two Pe2 pe3 positions are not images of each other under the mirror (it sends e to g), so these are two separate observations that agree in kind.
- **Z_C one rank up on cyl:8×8.** K26's named-group table says Z_C (pawns on ranks 2 to 5) is exact only on cyl:8×6 and cyl:9×6 among the boards tried, cyl:8×8
  included. K15's cyl:8×8 census lists `Kc3 ka5 Pa3 Pc5 pa4 pc6` (#22, "B, no passer", K15's root check (D, D)): Z_C translated one rank up. No contradiction (a
  different placement; rank translation is not a symmetry of the board), but K26's sentence must say "with these ranks"; the merged §5.7 does. Merger's check:
  `ref3m --board cyl:8x8 --moves` at all 8 roots (`work/zc88.ref3m.out`): (D, D), exactly one drawing move at each root (the shuttle), every other move
  loses for the mover. The same check reproduces Z_C on cyl:8×6 (`work/zc86.ref3m.out`).

### 2.3 Counts

- K15's 43 / 40 / 25 / 9 groups (refuted as invariants by K15b; recount 24 / 23 / 14 / 7 up to translation, mirror and colour flip, 74 / 68 / 40 / 10 before)
  count reading-B dud groups with up to 4 + 4 pawns on up to 5 files. K26's counts (exact placements: cyl:7×6 2, cyl:8×6 4, flat 7×6 2, flat 8×6 2, flat 7×7 0)
  count exact groups on F_Z = {a, b, c} with at most 3 + 2 pawns. Different classes; no contradiction in the numbers. The merged text uses only K15b's counts and
  states that K15's own counts are not invariants.
- **Consistency check where the scopes overlap (merger, COMPUTED-1, ref3m only; `work/exactcheck.py`, output `work/exactcheck.tsv`).** For each of the 83 six-rank
  groups of `K15/fin2/dud_groups.md` (cyl:7×6 43, cyl:8×6 40) I followed the drawing moves from the listed root with ref3m and tested K26's definition (four
  king configurations, value D and exactly one drawing move, a king move, at every root). 17 are exact. Those with all pieces on three consecutive files are
  exactly Z_B (cyl:7×6 #35, cyl:8×6 #33) and Z_C (cyl:8×6 #38). The other exact ones are outside K26's scope: 3 + 3 pawns on four files (cyl:7×6 #33, #34, #40,
  #42; cyl:8×6 #31, #32) and five-file groups (G8a, G8b and two 3 + 2 relatives on each board: cyl:7×6 #36–#39, cyl:8×6 #34–#37). The other 3-file 2 + 2 groups
  (D2, D2m) have two or three drawing king moves at some root, so they are not exact. Flat 7×6: K15's fourth 2 + 2 group `Ka1 ka5 Pa4 Pb3 pa3 pb4` has two drawing
  moves for each side, so it is not exact either, consistent with K26's "exactly Z_B and its mirror". So K15's list agrees with K26's result inside K26's scope,
  and K26 found every exact group of K15's list that lies there. (Limit: this starts from K15's representative roots, which K15b showed are not canonical; it
  checks consistency, not K15's census.) These new numbers are kept out of the NEW texts, which point here.

### 2.4 Conjecture 4.7 ("no over group")

- **Different definitions, same answer.** K26's exact under/over group (Definition 4.8) lives in plain P: White shuttles, Black's freeze wins at once (q with White
  to move is lost for White), and (U4) asks that q is a zugzwang for Black too. K15's "over" is a structural closure label of `grp.c` that can only appear in the
  free-pass reading (in plain P the freeze is a winning move and the root is labelled "threat"; K15b 3.7 confirms that the 40 plain-P rows say nothing about
  over). K26 thus tests the case K15 calls its blind spot, in plain P. Neither finds a group: K26 none in its 3-file and four-file ranges, K15 0 over and 0 under
  roots in its 40 free-pass rows. Both are compatible with the old first half being true in both readings.
- **K15's plain-P tempo-signature candidates vs K26's four-file search.** K15b found 4 over-signature roots on cyl:8×6 and 6 on cyl:7×6 (4 files, ≤ 2 + 2, plain-P
  rules), all refuted beside contexts (COMPUTED-1). K26's four-file search on cyl:8×6 (≤ 2 + 2) found no exact over group. No conflict: an over signature
  against tempo contexts is a weaker property, and the candidates are refuted anyway.
- **K15's near-over groups vs K26's loose groups.** Different relaxations (K15: free-pass shuttle with every White safe move freezing but the closure test failing;
  K26: (U4) dropped, one freeze per root). Counts (12 / 12 / 4 / 1 / 1 vs 120 / 142 / 118 / 626) are of different objects; not comparable, not contradictory.
- **Wording.** K15's referee block dropped the first half from the conjecture ("over is realisable with wider groups; no over-type group is known"); K26 kept the
  two-halved conjecture with "first half: supported". The merged text follows K15's form and states the first half as computed in both readings, because both
  searches are exhaustive within their ranges and both have a second implementation for the relevant part (K15b; the K26 referee).
- Lemma 4.9 (PROVED) and K15's near-over survivor (`Kd5 kb5 ...`, "no Black king shuttle in P") do not interact: the survivor is not an exact under/over group.

### 2.5 Other points

- **Appendix A.** K15's original reason (a flaw of `K15/classify.py`) was rejected by K15b as an attribution to the wrong script; the merged block uses K15b's
  wording and adds K26's "false for dud groups on the cylinder".
- **Chess.** Kept as each source and K28 state it: G8a, G8b exactly two-shuttle at cap 2 (COMPUTED-1, kpsolve only); D2, D2m not two-shuttle (52 of 108);
  Z_C bounds (W, L) at cap 1; Z_B on cyl:7×6 bounds (W, L) at cap 1, cyl:8×6 not run; Z_B on flat 7×6 not exactly two-shuttle (K28, CHECKED-2). The merged text
  does not transfer K28's flat-board Kc3–d2 draw to the cylinder.
- **K26's "Wider searches: not done (more than 4 files, more than 3 + 2 pawns)"** is no longer true once K15 is in: K15's census goes to 5 files and 4 + 4 pawns. The
  merged "Open" list states the boundary of each search instead.

## 3. Contradictions

None real. Two apparent ones, resolved by scope, are written into the merged text:
1. K26 "Z_C exact alone only on cyl:8×6 and cyl:9×6 (cyl:8×8 tried)" vs K15 "Z_C-type dud group on cyl:8×8": different ranks; both true.
2. K15's group counts vs K26's exact-group counts: different classes; inside K26's scope they agree (2.3).
One reporting defect in a source (not a contradiction between the two): K15's counts 43 / 40 / 25 / 9 are not invariants (K15b); they are replaced.

## 4. Checks on the result

- `apply_edits.py` on the current LOOPY: 9 applied, 0 rejected (`LOOPY_merged_check.md`).
- Cell counts per table row: unchanged (`diff <(awk -F'|' '/^\|/{print NF}' ...)` empty).
- Grep of the copy for leftover contradictions: no "the cylinder, other boards" / "cylinder and other boards are open" / "open on the cylinder" / "need wider
  searches" / "Wider searches: not done" / "remains a CONJECTURE for chess and for the cylinder"; the only "43, 40, 25 and 9" is the sentence saying they are not
  invariants; "none found" occurs only for over groups; Appendix A's "no dud and no over group" is followed by "Withdrawn".

## 5. Fix round (2026-10-29)

Three checkers read `EDITS_MERGED.md` (two FIX, one OK). Every problem was checked against the sources before acting. Output: `EDITS_FINAL.md`, 9 blocks.
Applying it to a copy of the current `kings/theory/LOOPY.md` gives 9 applied and 0 rejected, the table cell counts per row are unchanged, and the copy was deleted afterwards.
Numbering below: C1, C2, C3 are the checkers, and the number after the dot is the problem's position in that checker's list. Accepted fixes:

1. **C1.1 = C2.2, unlabelled merger check (§8 item 2, "How the two fit"). Accepted.** The label "(COMPUTED-1, merger, ref3m only; it starts from K15's
   representative roots, which are not canonical, so it checks consistency, not K15's census)" was added (§2.3 above).
2. **C1.2 = C2.1, CHECKED-2 on cyl:9×6 and widths 9 and 10 (§8 item 2, "Exact groups on F_Z"). Accepted.** K26 VERIFY Claim 3 (line 75) says kpp refuses
   widths above 8. The block now reads: CHECKED-2 on boards of width at most 8 (kpp and ref3m); widths 9 and 10 (Z_C on cyl:9×6, Z_B on widths 9 and 10) are
   ref3m only, COMPUTED-1. This now matches §5.7.
3. **C1.3 = C2.3, the dangling "two survivors below" (tempo-signature bullet of Conjecture 4.7). Accepted.** VERIFY_K15b 3.10 says only that the four
   cyl:8×6 roots are among K15's 20, including `Kc4 kd6 Pd3 Pd5 pa5 pd4` and `Kb4 ka6 Pa3 Pa5 pa4 pd4`, the survivors of the 40 random contexts (K15
   FINDINGS 7.2). The text now says that, names both groups, and adds that the 6 roots on cyl:7×6 were not compared with K15's list.
4. **C1.4, the 46-of-192 count of Z_C's mirror (§5.7 Z_C bullet). Accepted.** VERIFY_K15b 3.6 re-solved only the Pe2 pe3 position. The text now reads "46
   disagree (COMPUTED-1, K15)", and the Pe2 pe3 result is "re-solved by K15b with `ref3`, CHECKED-2".
5. **C1.5 = C2.7, the P3.2′ row cylinder sentence. Accepted.** The earlier samples (68, 12 and 660 contexts) are flat 7×6, so "COMPUTED-1 for the earlier
   samples" was dropped from the cylinder sentence (the row states those samples earlier, as COMPUTED-1). The contexts are now named: cyl:8×6 files e–g and
   cyl:7×6 files e–f, CHECKED-2. "(CHECKED-2)" was added after Z_C's "exact at its 8 roots".
6. **C1.6 = C3.1, the a–d boundary in the "Second half" bullet. Accepted.** K26 FINDINGS 1 (search range) and its table confirm that a–d was searched only
   with ≤ 2 + 2 pawns and only for under/over. The bullet now reads: "F_Z = {a, b, c} with at most 3 + 2 or 2 + 3 pawns, or a–d with at most 2 + 2 (under/over
   search only)".
7. **C3.2, the a–d wording in the §8 "Open" bullet. Accepted.** It now reads: "beyond F_Z = {a, b, c} and 3 + 2 or 2 + 3 pawns for K26's dud search, beyond
   a–d and 2 + 2 pawns for its under/over search".
8. **C2.4, the missing label on K15's earlier classifier check (Conjecture 4.7). Accepted.** VERIFY_K15b 3.8 says the Python cross-checks were not re-run
   (their dumps were deleted) and were replaced by K15b's solver. The label is now "COMPUTED-1 as reported by K15; not re-run by K15b, because its dumps were
   deleted; superseded by K15b's own solver above, CHECKED-2".
9. **C2.5, the §7 lead ("in chess it is an open question"). Accepted.** The block's OLD was widened to the whole bullet. The lead now reads: in P, flat 7×6
   PROVED by hand and the cylinder CHECKED-2, not proved by hand; in chess, a computed answer on cyl:8×6 (G8a, G8b at cap 2, COMPUTED-1), not a proof, and
   open elsewhere. K28's chess sentence inside the bullet is unchanged.
10. **C2.6, "the cylinder" dropped from the open lists. Accepted.** Chess on the cylinder is still open: Z_B is (W, L) at cap 1 on cyl:7×6 and not run on
    cyl:8×6, and Z_C is (W, L). There is also no hand proof on the cylinder.
    - The P3.2′ row and §3 now say: "Open: chess contexts of Z_B, chess on the cylinder (Z_B, Z_C), a hand proof on the cylinder, other boards".
    - The historical tail of §8 item 2 now says: "Open: chess contexts of Z_B, chess on the cylinder (Z_B, Z_C), other boards". Its own Open bullet already
      lists hand proofs.
    - K28's chess sentences are kept word for word.
11. **C2.8, numbering order in §4. Accepted.** The Conjecture 4.7 bullet now comes first (it continues the list of §4), followed by a blank line and then
    Definition 4.8 ("used in Conjecture 4.7 above") and Lemma 4.9. "Counted separately below" in Definition 4.8 now reads "counted separately in Conjecture
    4.7 above". This also ends the Markdown problem of a paragraph glued to the end of a bullet list.
12. **C2.9, the range summary. Accepted.** K15 FINDINGS (table rows for F = 4 ≤ 4 + 2) and VERIFY_K15b 3.7 list the 20 ranges.
    - The Conjecture 4.7 K15 bullet now lists all 20: on each of cyl:8×6 and cyl:7×6, F = 3 ≤ 3 + 3 and ≤ 4 + 4; F = 4 ≤ 3 + 2, ≤ 3 + 3 and ≤ 4 + 2; F = 5
      ≤ 2 + 2 and ≤ 3 + 2. Then cyl:8×8 (2 ranges), cyl:7×7 and cyl:8×7 (1 range each), and flat 7×6 ≤ 2 + 2 and ≤ 3 + 3.
    - The C4.7 status row gives the largest ranges, with "≤ 4 + 2" added on 4 files and "3 files ≤ 3 + 3" for flat 7×6. No new table cells.
13. **C2.10, the unlabelled chess cap-1 contexts of G8a/G8b and the scope of the 18/41 label (§8 item 2). Accepted.**
    - Chess cap-1 contexts: "(COMPUTED-1, K15, one solver family)" was added.
    - 18/41 context split: "(COMPUTED-1, K15; K15b re-derived the split from K15's table, not by re-solving)" was added. Only the Pe2 pe3 position is
      CHECKED-2 ("re-solved by K15b").
14. **C3.3, the optional upgrade of the cyl:8×8 check of `Kc3 ka5 Pa3 Pc5 pa4 pc6`. Accepted.** The checker's files `check2/zc88.kpp.out` (kp_p --pmodel) and
    `check2/zc88.ref.out` (ref3m) were read here. At all 8 roots both give D, exactly one drawing move (the shuttle) and every other move losing for the mover,
    with identical move lists. Two solvers agree, and the merger's own ref3m run (`work/zc88.ref3m.out`) agrees as well. The §5.7 text now says CHECKED-2 and
    cites `check2/zc88.*`. The integrator may revert this to COMPUTED-1 if a checker's run should not count toward CHECKED-2.

Rejected: none. Every problem was confirmed against its source. C3's side note (ref3m does not parse `--board flat:WxH`; use a three-letter prefix such as
`pln:7x6`) does not affect the text. It concerns anyone who re-checks flat boards with ref3m.

Not changed:
- Numbers. No number in the text was changed.
- K28's chess sentences.
- The content of the source blocks (standing and referee replacements) outside the passages above.
