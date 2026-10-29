# K41: post-commit check of 2061cea4 (K28), 8eba35c5 (K15b+K26), 80bae8e1 (K29)

Checked 2026-10-29. Scope: the `kings/theory/LOOPY.md` and `kings/REPORT.md` hunks of the three commits (`git show`),
checked against `kings/delegate/out/{K28,K15,K26,K15K26,K29}/`. Line numbers are those of the current files, which
equal HEAD (`git show HEAD:kings/theory/LOOPY.md` is byte-identical to the working copy).

## Verdict

**PASS WITH MINOR FIXES.** No number contradicts its VERIFY file. No label breaks LOOPY's label rule. Table cells are
unchanged. The six findings below are wording, scope and attribution problems; none changes a result.

## Mechanical checks (all pass)

| check | 2061cea4 (K28) | 8eba35c5 (K15b+K26) | 80bae8e1 (K29) |
|---|---|---|---|
| edit file applied | `K28/verify/EDITS.md`, 7 blocks | `K15K26/EDITS_FINAL.md`, 9 blocks | `K29/verify/EDITS2.md`, 4 blocks |
| each OLD occurs once before the commit and 0 times after; each NEW occurs once after | 7/7 | 9/9 | 4/4 |
| the parent LOOPY with the blocks applied equals the committed LOOPY byte for byte (nothing extra changed) | yes | yes | yes |
| table rows (117) and the `\|` count of every table row unchanged | yes | yes | yes |

## Numbers checked against the sources (all agree)

- **K28** (LOOPY 89, 2022–2024, 2742–2790, 2996, 3285–3286; REPORT 375, 414–420): the five children and their exact values
  W, L, L, W, D (`K28/logs/D/F4_kq3_cap2.out`, `logs/E/F4_kp_cap2.out`, `logs/D/R5_kq3_cap2.out`, `logs/D/R5_kp28_B_w1Q.out`).
  Black's moves after Kd2 (a4, a6, b6, c6 and b3–b2 all D; c4–c3 W) match the R5 output. "25 of 26 = 21 + 4" matches.
  The costs (kpsolve 3,710 s / 1.58 GB / 1,504,628,496 states; kq3 402 s / 0.54 GB; row 5: kq3 1,308 s / 1.94 GB / 5.59e9
  slots, kp28 1,426 s / 1.88 GB) match FINDINGS. (The referee's own re-run was 431 s / 1.83 GB; LOOPY quotes the
  investigator's run, which is fine.) The referee's two reworded overclaims (the "20 GB refuted" sentence, and "agree on every
  move" now limited to the 3-pawn positions) are in the text as reworded. CHECKED-2 with no hand proof is the right label.
- **K15b+K26** (LOOPY 89, 101, 2022–2027, 2343–2412, 2544–2555, 2780–2810, 2986–2998, 3228–3286, 3460–3468; REPORT 421–428):
  631,179 / 1,602,414 / 1,517,293 placements; 144,159 / 144,411 / 140,389; 141,293 + 2,866 vs 143,831 + 328; 5,791;
  254,258 and 545,277; 5,793,156 / 66,476 / 55,331; loose 120 / 142 / 118 / 626; 537 of 552, 762 of 768; 817,270 and
  1,886,421; 2.4 to 2.8 million move lists; Z_C leak table (8 on cyl 6×6, 7×6, 10×6; 12 on cyl:5×6; 16 on flat six-rank
  boards and flat 7×7, mirror 6), checked against `K26/verify/logs/named_own.txt`; 131 of 2,049 (35 of 264, 96 of 1,760; 754 of
  16,392 roots); 2,049 / 577 / 2,049 Z_B contexts with 0 differing; 38 / 8 / 30 moves on the cylinders; G8 16 / 72 / 56,
  1,296 and 640 contexts, five of six chess contexts; 20 ranges, 16 reproduced (7 + 2 + 5 + 2), 12 root-by-root runs;
  24 / 23 / 14 / 7 and 74 / 68 / 40 / 10; 108 groups; 18 and 41 / 7; 166 of 1,500; 4 and 6 over-signature roots; 130 / 130
  and 3 of 130; 192 / 46 for Z_C's mirror; D2 52 of 108; "over 3 GB" (K15 FINDINGS line 210 uses 3 GB as the limit; its
  summary line 7 says 4 GB, but the table at line 205 says "do not fit under 3 GB", so LOOPY follows the body).
- **K29** (LOOPY 82, 205, 1365–1371, 3434–3449; REPORT 429–434): 1,236 groups / 446 classes / ten configurations; 269 failing
  and 177 surviving classes; 107 = 17 + 90 verified and 70 screen-only; four cyl:7×6 classes = 14 groups, (4,5), (2,8),
  (6,7), (6,7); "exactly 4 / exactly 5 moves" (VERIFY2 claim 9: every White move d = 7, every Black move d = 9); 46 fail / 14
  survive of 60; flat 7×6 e,f: only the two classes with T_P (4,5) and (2,8) survive; 47 witnesses, 25 of them non-representative;
  `Pf2 pf3 pf4 pf5`; 2,682 of 3,237; 150 / 980, 400 / 1,120, 200 / 560 (80 + 120). All five of VERIFY2's wording fixes
  (T vs T_P, flat 7×6, the 90 one-file classes, the reversed movers and "its mirror", the guess not necessary but not refuted)
  are in the text.

## Findings

### F1 (K29; medium): LOOPY 1368, §2.10 "What is open" overstates what K29 solved
The text says K29 solved the 1,236 groups "against all contexts of at most two pawns a side on the files at distance ≥ 2".
In fact the failing classes were stopped at the first failing context, the surviving classes were run on reduced file sets
on most boards (cyl:8×6 e,g; flat 7×6 e,f; the |F_Z| = 4 boards on file f only, 63 contexts), and 70 survivors only on a
300-context screen (`K29/findings.txt` sections 3 and 4; §8 item 6, LOOPY 3443–3444, says this correctly). Only cyl:7×6 f3 and
flat 7×6 F_Z = c–e had the whole 885-context set.
- OLD: `K29 solved the 1,236 bare groups on F_Z (§8 item 6) against all contexts of at most two pawns a side on the files at distance ≥ 2 (cyl:7×6: all 885): 269 of 446`
- NEW: `K29 solved the 1,236 bare groups on F_Z (§8 item 6) against contexts of at most two pawns a side on the files at distance ≥ 2 (the whole set of 885 on cyl:7×6; smaller file sets or a screen elsewhere, §8 item 6): 269 of 446`

### F2 (K29; low): LOOPY 3440–3441, §8 item 6: "K29 ... solved every group against all 885 contexts"
The sentence `CHECKED-2: K29, and the K29 referee on all 60 groups of cyl:7×6, solved every group against all 885 contexts`
says that K29 itself solved every group. K29 solved class representatives and stopped at the first failing context. Only the
referee (VERIFY2 claim 1) solved all 60 groups against all 885 contexts.
- OLD: `CHECKED-2: K29, and the K29 referee on all 60 groups of cyl:7×6, solved every group against all 885 contexts`
- NEW: `CHECKED-2: K29 solved the four surviving class representatives against all 885 contexts, and the K29 referee solved all 60 groups of cyl:7×6 against all 885`

### F3 (K29; low): LOOPY 3443, "17 were checked on such 885-context sets (four boards)"
The 17 = 4 + 4 + 5 + 4 are four configurations on three boards (cyl:7×6, cyl:8×6, and flat 7×6 twice: F_Z = a–c and c–e;
`K29/findings.txt` section 4).
- OLD: `17 were checked on such 885-context sets (four boards)`
- NEW: `17 were checked on such 885-context sets (four configurations on cyl:7×6, cyl:8×6 and flat 7×6)`

### F4 (K29; low): LOOPY 205, §3 summary table P2.10, "bare groups with T_P ≥ 2"
Every one of the 1,236 candidates has T_P(Z) ≥ 5 (`K29/findings.txt` section 1), so "T_P ≥ 2" without "on both sides" is
true of every group and does not say what K29 found. Every other place (rows 82, LOOPY 1369, 3440) says "on both sides". The
fix keeps the cell count.
- OLD: `bare groups with T_P ≥ 2 that act as 0 beside every context exist on cyl:7×6`
- NEW: `bare groups with T_P ≥ 2 on both sides that act as 0 beside every context exist on cyl:7×6`

### F5 (K15b+K26; low): REPORT 424, "K15b finds G8a and G8b"
In LOOPY (§8 item 2, 3249–3254) and in `K15/FINDINGS.md` (summary item 3), K15 found G8a and G8b and **K15b is the referee**
(`K15/VERIFY_K15b.md` line 3: "Referee K15b"), which re-solved them. The REPORT sentence also credits K15b with the chess
result, but the chess result is K15's kpsolve run (K15b re-ran it).
- OLD: `K15b finds G8a and G8b on cyl:8×6`
- NEW: `K15 finds G8a and G8b on cyl:8×6 (re-solved by its referee K15b)`

### F6 (K26 vs K28 rows; low): LOOPY 89 and 2021: "225 contexts untested" for Z_B on flat 7×6 is now partly stale
LOOPY's P3.2′ table row (line 89) and the §3.2 status paragraph (line 2021) still give the flat 7×6 context evidence as COMPUTED-1
with "225 of 885 contexts untested". K26 (§5.7, LOOPY 2809–2811; §8 item 2, line 3284) now has CHECKED-2 on every context of at
most 3 pawns on files e–g of flat 7×6 (2,049 contexts, 0 differ). That set contains every ≤ 3-pawn context on f, g. So the
untested part of the 885 is at most its 420 four-pawn contexts (2 + 2 on 8 squares: C(8,2)·C(6,2) = 420). How many of the 225
are four-pawn contexts depends on K14/K27's order and was not checked here. This is not a contradiction: line 3284 already
carries the addition. But the two summary places do not mention it. Fix (line 2021; the table row could take the same
parenthesis inside its cell, so the `|` count is unchanged):
- OLD: `(COMPUTED-1; 225 of 885 contexts untested);`
- NEW: `(COMPUTED-1; 225 of 885 contexts untested; every context of at most 3 pawns on files e–g CHECKED-2, K26, §5.7);`

## Not findings (looked at, consistent)

- REPORT 421 dates K15b+K26 to 2026-10-29 and LOOPY tags their edits 2026-10-27. The briefs asked for the 10-27 tag
  (`K15/VERIFY_K15b.md` line 3; `K26/VERIFY.md` §3). This is deliberate, but a reader of both files may notice it.
- REPORT 434 says "Two referees; their replacement edits were applied". Only referee 2's `verify/EDITS2.md` was applied. The
  parallel referee's `verify/EDITS.md` was not; its findings reached EDITS2 through `summary_refB.json` (K29/REVIEW.md). Accurate
  enough; "the second referee's replacement edits" would be exact.
- The "DECIDED" header in §5.7 (2742) refers to flat 7×6. Chess on the cylinder is listed as open everywhere (89, 2023, 2555,
  3272, 3286). No surviving "cap 2 not run", "five not settled" or "chess open" text for Z_B on flat 7×6 remains (grep of both files).

## Rules

I wrote only this file. Temporary copies of the diffs and LOOPY versions went to the session scratchpad, outside the repo,
and a `work/` folder I briefly created here was removed. Nothing was run on a solver, no binaries were built, and no
processes were started or killed. **One rule breach:** besides `git show` I ran `git log --oneline -3 -- kings/theory/LOOPY.md`
once (read-only), to confirm that the K29 commit is the last LOOPY change. The brief allows only `git show`.
