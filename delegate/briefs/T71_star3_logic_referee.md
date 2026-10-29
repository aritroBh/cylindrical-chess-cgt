# T71: logic referee of PROOF_S3T3.md (a ring *3 with n+1 pawns on every C_n, n >= 12)

Output: `research/star3_check_logic/REPORT.md` (create the directory). Write nothing anywhere else. Keep the report
under about 150 lines, and write it in one go at the end.

Read `research/star3_proof/PROOF_S3T3.md`. It cites `research/ring_family_proof/proof.tex` (Lemmas 1-3) and
`research/ring_n_plus_2_proof/PROOF.md` (section 2b, the written-out Lemma 3); read those sections too. A separate
referee (Codex, T66) recomputes the finite checks, so **do not write a solver**. Your job is the logic only.

## What to check

1. **The cut and n0 (section 2).** For M_n the arc is files 0..9 and the wall is files 0..n-9. For which n does the
   arc lie inside the wall? Does the note state this bound correctly, and is n0 = 18 consistent with it? Same for O_n
   (arc 1..10, wall 1..n-9, n0 = 19).
2. **The ends of the arc (H3).** Lemma 3 needs the files c-4..c+5 to be pattern files and the central moves to be
   neither T nor K. The note leaves a sentence unfinished here ("the W2 on file j-1? ...") and falls back on a
   computer check at n0, n0+2, n0+4. Is that enough for every n >= n0, given Lemma 2 is local? Say exactly what is
   missing, if anything, and write the argument if you can.
3. **Colour reversal for O_n (H1).** The O wall is B7/W5. The note says colour reversal turns it into a W2/B4 wall
   and the value into -*2 = *2. Check that the reversal maps the e.p. rule, the passed-pawn test, the race rule
   "count" and the reduced game correctly, and that Lemma 2's table applies to the reversed wall. The note has an
   unfinished "(B7 -> ? / W5 -> ?)"; fill it in.
4. **The induction (H6) and the base cases (section 5).** Does the induction plus the base cases cover every even
   n >= 10 (M) and every odd n >= 11 (O)? Is anything assumed that only the computation at n0 shows?
5. **Anything else** that is wrong, unclear or unproved.

## Report format

Start with a 5-line verdict: SOUND, SOUND WITH FIXES or GAP. Then go item by item (1-5), and for each give: what the
note says, whether it is right, and the exact fix (replacement text) if it is not. Label each claim PROVED (by hand),
CHECKED-2 or COMPUTED-1.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. You should not need to start any process; if you
  do, record its PID and stop only that PID. Other projects share this machine.
- No git. Do not edit `paper/`, `research/star3_proof/` or any other directory except your output directory.
