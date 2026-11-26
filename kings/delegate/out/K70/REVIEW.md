# K70 review (orchestrator), 2026-11-25

Item: Lemma B of Proposition 4.25 (White to move, Black Kb6, pb7, pc6 against a White king and one pawn on c2, c3
or c4: a Black win in P for every king square not next to b6, except Kb4 with the pawn on c4, a draw).
Author: a model of another vendor, blind (it saw only `kings/delegate/briefs/K70_lemmaB_blind.md`). Referee:
K73, independent (`verify/VERIFY.md`).

**Installed:** the referee's edit of the Lemma B sentence of Proposition 4.25 (`verify/EDITS.md`), with two
wording changes of mine ("by a model of another vendor"; the referee's estimate of 30 to 50 hours in place of
"several days"). **The label of Lemma B stays CHECKED-2** and Proposition 4.25 stays "PROVED, given one CHECKED-2
lemma".

**What K70 delivered.** A certificate: an opening rule for Black's first reply; Table B, 486 rows (Black king
square, zone of White king squares, Black's move, and for every legal White reply a lower-numbered row), 6,742
positions; Table D, 97 rows, with a blockade lemma F, for the one drawn start. The author labels it PROVED.

**What the referee found.**
- Its own checker, written from the prose before reading the author's code: 0 failures on both tables, the
  opening (162 starts, 1,149 first moves) and F (716 instances). Ten one-row corruptions are all detected.
- An independent solver (r68) agrees: all 6,742 Table B positions are Black wins; no Table D or F position is.
- By hand: 42 rows and every prose argument; no error in a row; two wording slips and one ambiguous convention
  (noted at the top of PROOF.md).
- The 42 positions that Proposition 4.25 uses reach 484 of the 486 rows, so the needed part is no shorter
  (`verify/TABLE42.md`).
- A full check by hand is possible in principle (the induction is well founded) and would take 30 to 50 hours.

**Why the label does not change.** PROVED is kept for proofs a person has checked or can check in reasonable
time from the text. Here the rows were found by search and all of them have been checked only by programs. What
changed is the kind of evidence: besides three solvers that agree on the values there is now an explicit strategy
for Black that two checkers accept and that anyone can audit row by row.

**Open.** A short hand proof of Lemma B, or the full table checked by hand.

**Process.** The author stayed blind as far as its files show. One small breach: a temporary copy of a source
file outside its folder, deleted at once. No binaries, no home paths.
