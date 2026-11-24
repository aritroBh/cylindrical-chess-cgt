# K60 review (2026-11-23)

Question: Lemma 4.15's Black-side condition (B1) is sufficient for an exact over group to have the results of over.
What is the exact condition, and can it be computed?

Investigator: an Opus agent (`PROOF.md`, `findings.txt`, `EDITS.md`, `src/`). Referee: a second Opus agent that
re-derived every proof, ran its own brute force with separate code and two Büchi solvers, and rechecked the 3 + 3
group with a program on a different move generator (`verify/VERIFY.md`, `verify/`). The referee's edit set was used.
A blind proof attempt from outside the Claude family is K61 (`kings/delegate/briefs/K61_over_test_blind.md`).
AI work, no human re-derivation.

## Verdict

- **Theorem 4.18(a): PROVED.** For every exact over group the q's have the results of 0_D, and Black never does worse
  beside the group than beside over. (B1) is not used.
- **Theorem 4.18(b): PROVED.** The group has the results of over iff (C): after every non-shuttle Black root move,
  White to move does at least as well beside any t as over ⊞ t gives with Black to move. It holds game by game (added
  by the referee). The comparison with White to move is sufficient but not necessary.
- **Theorem 4.18(c): PROVED,** using the known positional determinacy of Büchi games. (C) holds at a move iff White
  wins the position beside under, where an infinite play is a White win only if White passed infinitely often.
  Equivalently White wins beside the short game T_N for one N at least the number of states.
- **Corollary 4.19: PROVED.** One short test game decides; (B1) is "White wins without passing"; an abstract exact
  group with ten boards fails (B1) and has the results of over.
- **Brute force (COMPUTED-1 each):** investigator 7,509 toy groups, 83,127,655 results; referee 9,012 toy groups,
  63,607,102 results; no violation in either.
- **Real groups:** the 3 + 3 group of cyl:8×6 fails (C) exactly at 1…e5–e4 (CHECKED-2: two sum solvers on two
  separately written move generators). The 2 + 3 group of cyl:10×6 passes through (B1) (CHECKED-2); the direct
  result of the Büchi solver is COMPUTED-1. No known real group has the results of over without (B1).

## Not done

- No second Büchi program on a real group. The flat translates of the 3 + 3 group, the cyl:8×7 groups and the K59
  groups were not run through the new test.
- Open: a fixed finite test family that does not depend on the group.
- The toy groups model checks and e.p. rights as flags, not chess geometry.
- Nothing about P contexts or chess.

## Notes

Three wording slips in `PROOF.md` are listed at its top. The investigator's `EDITS.md` numbered the new statements
4.17 and 4.18; the note uses 4.18 and 4.19 because K59 takes 4.17.
