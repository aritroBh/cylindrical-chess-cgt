# K56 review (2026-11-23)

Question: is there a local condition on an exact group that forces the results of over in sums, and do the known
groups meet it?

Investigator: an Opus agent (`findings.txt`, `PROOF.md`, `EDITS.md`, `src/pr56.cpp`). Referee: a second Opus agent
that re-derived the proof step by step and wrote its own pass-game solver (`VERIFY.md`, `verify/`). AI work, no human
re-derivation.

## Verdict

- **Lemma 4.13 is PROVED.** A tempo-exact over group (Definition 4.12), as the P game of its own pieces, has the
  results of over beside every finite D-game, loopy or short, with or without terminals, at both roots and with either
  side to move; each q has the results of the test game alone. The referee found every step of the main proof sound.
  Weakest step: the termination count, which is correct when the ranks for different pass budgets are read in one
  game whose states record the passes left.
- **One false side claim, removed.** "More passes always help the passer" is false (a forced pass where a stalemate
  would have drawn), so "pass-robust exact implies tempo-exact" is withdrawn. Pass-robust exactness is still
  sufficient, by the same proof. An erratum is at the top of `PROOF.md`.
- **No known group meets the criterion.** All nine exact groups tried fail on White's side; the 3 + 3 group and its
  flat translates also fail on Black's side, at 1…e5–e4. For the 3 + 3 group on cyl:8×6 and the 2 + 3 group of
  cyl:10×6 the root results are CHECKED-2 (two solvers with no shared code); for the other seven COMPUTED-1.
- **Toy test (COMPUTED-1):** 2,000 random abstract tempo-exact groups agree with over at all 9,064,258 results, and
  543 of 3,954 exact groups that are not tempo-exact differ, so the test can tell them apart. It does not exercise
  checks or e.p. rights.
- **Whether the 2 + 3 group is over stays open.** It has the results of over on 600 further random D-games.

## Integration

The referee's replacement set `verify/EDITS.md` was applied to `kings/theory/LOOPY.md`: 2 applied, 0 rejected, table
cell counts unchanged. It differs from the investigator's set by removing the false implication, recording the
referee's check, splitting the labels of the computed part, adding the toy test, and saying plainly that no known
group meets the criterion.

## Process notes

Investigator peak memory 2.83 GB once (under the 3 GB limit, over the 2 GB design target), referee 1.28 GB. No
pattern kills; binaries removed.

## Open

A two-sided criterion that the 2 + 3 group meets, or a certificate that it is over (K57); necessity of the criterion.
