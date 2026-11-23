# K46: post-commit check of 3cc612a8, dc9c51a6 and a85b211a (2026-11-23)

**Verdict: PASS WITH MINOR FIXES.** Every edit file named in the REVIEW.md files was applied exactly. The table changed
only by K42's new row. No number in the new text contradicts a VERIFY.md. The findings are four places where a label
claims more than VERIFY gives, two wording points, and four stale passages (two in LOOPY, two in REPORT).

Method: `git show` only (no other git). Inputs were extracted to a scratch directory outside the repository, and
`kings/delegate/apply_edits.py` was re-run there. Line numbers refer to `git show a85b211a:kings/theory/LOOPY.md` and
`git show a85b211a:kings/REPORT.md`. Both are byte-identical to the working tree. No heavy runs; nothing was built or
killed.

## 1. Mechanical check (the earlier pass, re-run independently)

| commit | edit files (from REVIEW.md) | apply_edits result | output vs `git show <commit>:kings/theory/LOOPY.md` |
|---|---|---|---|
| 3cc612a8 | K38/verify/EDITS.md, K40/verify/EDITS.md, K41/EDITS_K41.md | 7 + 1 + 6 = 14 applied, 0 rejected | identical (cmp) |
| dc9c51a6 | K39/verify/EDITS.md | 8 applied, 0 rejected | identical |
| a85b211a | K42/verify/EDITS.md, K43/verify/EDITS.md, K44/verify/EDITS.md, K44/EDITS_MERGED_K43.md | 15 applied, 1 rejected | identical |

- The parent files equal `git show <commit>^:kings/theory/LOOPY.md` (cmp).
- The one rejected edit is K44's "over, none found, pointer" (OLD occurs 0 times, because K43 rewrote that bullet). The
  integrator's re-anchored version in `EDITS_MERGED_K43.md` applied once. K44/REVIEW.md describes this.
- Without `EDITS_MERGED_K43.md` the output lacks only child lines 3373–3374 (the K44 parenthesis), as the earlier pass
  said. That pass's wording "0 rejected for 'over' but 1 rejected" is garbled; the counts are 5 applied, 1 rejected.
- REPORT: `K41/EDITS_K41_REPORT.md` (F5) applied to `3cc612a8^:kings/REPORT.md` gives 1 applied, 0 rejected. Apart
  from that edit, the commit's only REPORT change is the new K38/K40/K41 bullets. The REPORT bullets for K39, K42, K43 and
  K44 were written by hand (no edit file), so §2 checks them against VERIFY.
- Table: separator-free status-table rows/cells are unchanged in 3cc612a8 and dc9c51a6. In a85b211a there is +1 row and
  +3 cells, the new row `| §8 Q1, P8.1′ |` at line 118 (the only differing table line). The earlier pass counts
  117 → 118 rows and 435 → 438 cells. Its counter includes separator rows, so its totals differ from mine, but the change
  is the same.

## 2. Findings (numbers and labels against VERIFY.md; VERIFY takes precedence)

Severity: MEDIUM = a label stronger than VERIFY gives; MINOR = wording or scope; NIT = cosmetic.

**F1. REPORT.md:440–441, MEDIUM (K40 label for H = 7).**
K40/VERIFY.md row 5: "CHECKED-2 for H = 6, 8; COMPUTED-1 for H = 7" (K40 did not run H = 7; the 71,842,272 compared
results come from K40's own tables). LOOPY §8 item 5 states this correctly. REPORT puts all three heights under one
CHECKED-2 and also leaves out the convention (N); under (C) there are thresholds θ and parity classes.
- OLD: `on cyl:W×H, 3 ≤ W ≤ 8, H ∈ {6, 7, 8}: on 3 and 5–8 files every position has the signature of a win, of on, or of dud, and no number or infinitesimal occurs (CHECKED-2: two sum solvers, 71,842,272 results)`
- NEW: `on cyl:W×H, 3 ≤ W ≤ 8, H ∈ {6, 7, 8}: under (N), on 3 and 5–8 files every position has the signature of a win, of on, or of dud, and no number or infinitesimal occurs (CHECKED-2 for H = 6, 8: two sum solvers, 71,842,272 results; COMPUTED-1 for H = 7, the referee's solver only)`

**F2. REPORT.md:450–451 and LOOPY.md:118, MEDIUM (K42 totals and mechanism inside a CHECKED-2 bracket).**
K42/VERIFY.md §2 says the referee re-ran four context rows and the mechanism for c1 of cyl:8×6 only. "The per-context
totals other than the four rows" and "the mechanism counts other than c1" stay COMPUTED-1. LOOPY's body (lines 3296–3297
and 3303) labels them this way. The status row and REPORT put 68,395 / 6,033,423 and "every failure uses the sortie king"
inside the CHECKED-2 bracket of "FALSE". FALSE itself is CHECKED-2.
- REPORT OLD: `it is FALSE in P (CHECKED-2: 68,395 failures in 6,033,423 sortie and context pairs on cyl:7×6, 8×6 and 9×6, every one using the king that made the sortie).`
- REPORT NEW: `it is FALSE in P (CHECKED-2: the referee's solver reproduces the examples and four full context rows; in all, 68,395 failures in 6,033,423 sortie and context pairs on cyl:7×6, 8×6 and 9×6, every one using the king that made the sortie, COMPUTED-1).`
- LOOPY:118 OLD: `is FALSE (CHECKED-2, K42, 2026-11-22: 68,395 failures in 6,033,423 sortie–context pairs on cyl:7×6, 8×6, 9×6, K18's context family included; every failure uses the sortie king).`
- LOOPY:118 NEW: `is FALSE (CHECKED-2, K42, 2026-11-22; the totals, 68,395 failures in 6,033,423 sortie–context pairs on cyl:7×6, 8×6, 9×6, K18's context family included, and "every failure uses the sortie king" are COMPUTED-1 outside the four context rows the referee re-ran).`

**F3. LOOPY.md:3164–3165, MINOR (same point as F2).**
OLD: `counterexamples in every promotion-free context class tested, K18's family included; CHECKED-2, three P solvers; see the K42 item below)`
NEW: `counterexamples in every promotion-free context class tested, K18's family included; FALSE is CHECKED-2 (three P solvers on the examples, two on four full context rows), the per-class counts COMPUTED-1; see the K42 item below)`
(K42/VERIFY.md §5: "Three P solvers … agree on the examples, and two of them agree on four full context rows.")

**F4. LOOPY.md:3506–3507, MINOR (K44 multiset comparison scope).**
K44/VERIFY.md row 2: the fsig files of 129 cases (W = 6 m0, m1, m2 and W = 7 m2) were deleted. rk ran those cases
"without a comparison file", and they enter only the class totals. So the multiset comparison covers 2,002 of the 2,131
cases.
- OLD: `gives the same multiset of B34 signatures as `kg44` in every one of the 2,131 cases (1,756,517 root entries)`
- NEW: `gives the same multiset of B34 signatures as `kg44` in every case that has a kg44 signature file (2,002 of the 2,131; for the other 129, whose files were deleted, the class counts agree), 1,756,517 root entries in all`

**F5. REPORT.md:457, MINOR (K44 "+1 and -1 on odd widths 7 to 12").**
K44/VERIFY.md: the three-pair family has "+1 on W = 7..12" (every width, even ones included), and free +1 totals exist for
W = 6..12. What is new is the odd widths 7, 9, 11. "Odd widths 7 to 12" reads as if 8, 10, 12 had none.
- OLD: `and finite tempi +1 and -1 on odd widths 7 to 12 (CHECKED-2, four implementations).`
- NEW: `and finite tempi +1 and -1 with three pairs on every width 7 to 12, including the odd widths 7, 9 and 11, where one or two pairs give none (CHECKED-2, four implementations).`
(The LOOPY heading at line 3516, "+1 and -1 on odd widths", is fine because its body says "for every width 7 to 12".)

**F6. REPORT.md:424, NIT (K41 F5 edit leaves two parentheses in a row).**
- OLD: `K15 finds G8a and G8b on cyl:8×6 (re-solved by its referee K15b) (two blocked pairs on files a and e, no pawn move),`
- NEW: `K15 finds G8a and G8b on cyl:8×6 (two blocked pairs on files a and e, no pawn move; re-solved by its referee K15b),`

Checked and found consistent with VERIFY (no finding):
- K38: 296 positions per board, Lemma K′, the chess values CHECKED-2 on both boards, no `ownref`.
- K39: 28/30 and 24/32 deviations, Kc3–d2 from (c3, b5) and from (c3, a4), 60/64 roots, 8 contexts.
- K40: LOOPY 0.75–3.4% (2.5–3.4% on the four boards), the 24 underpromotion wins on 4 files, θ = −1 for H ∈ {7, 8}.
- K42: 91,548/91,622/91,640, 26/56/100 contexts and 13/36/53 classes, the four context rows, 2,205,120 not quoted,
  Proposition 8.1′ PROVED and re-derived.
- K43: 6,363,129,120 placements, loose groups 13.4–54.7 million, 631,179 and 120/118/142/142, the ranges 63,378/455,385/132,
  the near misses as 6 placements and 3 up to reflection, 8 of 10 captures, the Lemma 4.10(3) legality condition, 817,270
  only as K26's count, and "38 roots" labelled COMPUTED-1.
- K44: over/under roots, 13x6–16x6 and 10x7, the class totals, 1,909/2,976, 135,000 lines, and 80 short roots
  (kg44 + lk).
- No solver result is labelled PROVED.

## 3. Stale text

**S1. LOOPY.md:3330 (§8 item 2 summary), MINOR.** The header still cites only K15 and K26, and the summary says only
"Over groups: none found (Conjecture 4.7)". K43 (the exact search to 3 + 3 on four files) and K44 (over as an LK value)
appear only in the bullet at 3371–3374.
- OLD: `Over groups: none found (Conjecture 4.7).`
- NEW: `Over groups: none found (Conjecture 4.7; K43, 2026-11-22, extended the exact search to 3 + 3 pawns on four files). Over and under do occur as values of the king-fight game LK with three pairs on cyl:10x6 and wider (K44, §8 question 3), which is not a group of Definition 4.8 in P.`

**S2. LOOPY.md:2351 (Conjecture 4.7) and status row C4.7 (line 101), MINOR.** "No over-type group is known" and
"CONJECTURE, no support" are still true in P, but neither has a K44 pointer. Conjecture 4.7 says over is realisable "with
wider groups", and K44's over roots need W ≥ 10 and a third pair. A reader of §4 should see that these roots exist and that
they are not groups.
- OLD (2351): `No over-type group is known.`
- NEW: `No over-type group is known in P. (K44, 2026-11-22: the local king game LK of §8 question 3 has roots equal to over and under on the batteries with three blocked pairs on cyl:10x6 and wider, CHECKED-2; these are D-model values of a king fight, not groups of Definition 4.8, and no P context was run beside them.)`
- Add the same pointer to the C4.7 row after the K43 sentence, and add "K44" to its source cell.

**S3. REPORT.md:477–478 (§8 Open questions, `dud`), MINOR; stale since K15b/K26 (2026-10-27), not caused by these commits.**
OLD: `No small king-and-pawn group with both kings able to shuttle and no pawn break was found (CONJECTURE, theory §5.3).`
NEW: `Found on the cylinder: Z_B and Z_C (K15b, K26; exactly two-shuttle in P, CHECKED-2 for width ≤ 8), not two-shuttle in chess (K39). See §7 and theory §5.7 and §8 item 2.`
REPORT:421 already says that dud groups with no pawn break exist, so the two passages contradict each other.

**S4. REPORT.md:486 (§8 Open questions, Gafni), MINOR; stale since K40 (3cc612a8).** The bullet describes only K4, K6
and K8 and still lists the question as open. K40 answered it for cyl:3–8 × 6–8 (REPORT:439, LOOPY §8 item 5). Add one line:
`K40 (2026-10-29) answers it without edges on cyl:W×H, 3 ≤ W ≤ 8, H ∈ {6, 7, 8} (see §7 and theory §8 item 5).`

Not stale (checked): LOOPY:218 (P4.3, finite king tempo against a non-frozen opponent), LOOPY:3417–3423 and 3429 (already
revised after K44), LOOPY:3442 and 3447 (K31's parity rule, now scoped to one or two pairs), LOOPY:3040–3041 (§8 item 1
header), the L2.7a and P5 rows (K38 pointers present), and LOOPY:3385–3386 (K39 closing paragraph).

## 4. Housekeeping

Read-only except this file. No git command other than `git show`. No heavy runs, no binaries, no kills. Scratch outputs
are outside the repository.
