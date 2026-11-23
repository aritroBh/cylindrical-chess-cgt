# K49 review: the ON class of K+P v K on the cylinder (integrated 2026-11-23)

**Outcome: accepted with the referee's fixes.** `verify/EDITS.md` applied (3 applied, 0 rejected, cell counts unchanged).

- K49 reduces K40's three classes (DEC, ON, DUD) under normal play, W ≠ 4, to Lemma P (no reciprocal zugzwang in the
  bare game). Given Lemma P: r(x ⊞ n) = r(x ⊞ 0) for every integer n, the lower bound against every terminal-free T, and
  the trichotomy are proved by hand. Lemma P is PROVED for the pawn on rank H−1 and computed below it (CHECKED-2 on
  K40's boards and on cyl:3×10, 5×10, 9×8, 10×10; COMPUTED-1 on the other boards with W ≤ 10, H ≤ 10).
- The referee's solver `verify/vk.c` matches K40's tables on 9,376,224 results and reproduces every count.
- Fixes: the written proof of Theorem 1 argued "White needs no spare" from monotonicity, which gives the other
  direction; the statement holds by the argument of Theorem 4(iii), now cited. Proposition 3 does not need Lemma P.
  The 4-file Black wins come from White being stalemated, not from Lemma P's failure. "No short rule exists two ranks
  down" became "none was found". "The fortress needs height" is limited to 7 and 9 files (cyl:5×6 has 30).
- Open: Lemma P below rank H−1 by hand; Conjecture 7 (two types of ON); the odd-width fortresses.
