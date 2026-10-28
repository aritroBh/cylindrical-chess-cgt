# K16 review: the real-king square rule (integrated 2026-10-27)

**Outcome: accepted with fixes.** `EDITS_FINAL.md` holds K16's blocks rebased after `VERIFY.md`. The integrator made
two more fixes when applying it.

- **The square-rule conjecture of Remark 2.11 is false as stated.** ω can be stalemated, or walk into a stalemate.
  Examples:
  - cyl:6x6 `Ka4 ka6 Pa5 Pd5 b -`;
  - flat:6x6 `Kc1 ka1 Pc2 pa2 w -`. The integrator checked it by hand: Black's king has no legal square, and a2 is
    blocked by its own king.

  The counterexamples are CHECKED-2 (kp_p, the referee's own P solver and K16's `pyp.py`).
- **Theorem 2.11K is PROVED in P.** It is one AI proof, read step by step by the referee. It is the corrected rule:
  (H5K), (SQ), and a no-stalemate condition, either (NS) along the pushing line or the static (H3K). The integrator
  read the statement and proof: (SQ) keeps ω's king off p and off the path, and (H3K) ⟹ (NS) follows from (F1).
- **The sweep total is now stated in both units.** The text said "7.6 · 10⁸ instances" next to per-sweep figures that
  are certified positions. `summary.json` gives 761,023,066 instances, which is 609,716,942 certified positions, over
  the five top sweeps; the text now gives both.
- **KV = 2 example.** cyl:6x6 `Ka1 ke1 Pc2 pe2 w -`: Black plays Kd1 and e1=Q on its second move, before White
  reaches c6. The integrator checked this by hand.
- **Wording.** The R2.11 row now calls Theorem 2.11K a corrected rule, not "the same rule".
