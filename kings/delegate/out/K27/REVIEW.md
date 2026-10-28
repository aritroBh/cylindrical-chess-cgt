# K27 review: Z_B on flat 7x6, hand proof in P, chess status (integrated 2026-10-27)

**Outcome: accepted with fixes.** `EDITS_FINAL.md` (fix round on the referee's `verify/EDITS.md`) is applied, plus the
integrator changes below. Do not also apply `EDITS.md` or `verify/EDITS.md`: their OLD texts overlap.

- **Proved.** Z_B alone is exactly two-shuttle in P: (D, D) at all 8 roots, and each of the 26 non-shuttle moves
  (15 White, 11 Black) loses by force within 11 plies. This is K27's hand proof, `PROOF.md`: 26 certificates, 286 entries.
  The referee re-derived it and parsed the text of every certificate with its own move generator (`verify/certcheck.py`,
  0 problems, mutation-tested). The mirror group follows by the symmetry τ (flip the ranks, swap the colours and the side
  to move). The file reflection a ↔ c alone is not a symmetry.
- **Computations: CHECKED-2.** Four implementations agree on the 16 root values and move lists: kp_p, ref3/ref3m,
  K27's `pm.py` and the referee's `own.cpp`. τ-equivariance holds on all 649,994 reachable states.
- **Chess.** K27 and its referee settled six pushes as losing, CHECKED-2 (kpsolve, plus the referee's
  `ownchess.cpp`, validated on 76 positions). After integration, 21 of the 26 deviations lose and five are not settled
  at cap 1 (next section). Whether Z_B is two-shuttle in chess is open, not a conjecture. The P certificates do not transfer: in
  22 of the 26, the promoted piece can be captured at once.

## Integrator changes on top of EDITS_FINAL.md

- **Label CHECKED-3 → CHECKED-2.** LOOPY defines only COMPUTED-1 and CHECKED-2 for computations, so "four
  implementations agree" is said in words.
- **Kxc4 and Kxa3 children.** The sentence now names their deviations: the two king captures at (c3, a4), White and
  Black to move. This was the Haiku checker's point 2.
- **Conjecture-list bullet "A dud group exists in small K+P positions".** It now says the statement holds in P on flat
  7×6 (Z_B, PROVED), and that in chess it is an open question, not a conjecture. This was the Haiku checker's point 1.
- **The 16 king moves that capture nothing.** `EDITS_FINAL.md` says they were not computed. In fact, a run left over
  from a duplicate K27 workflow, which I stopped, computed them with kpsolve at cap 1: `scripts/run16.sh`, outputs in
  `logs/run2/c16_*.out`. The referee's `ownchess` re-ran them as well (`scripts/run16_own.sh`,
  `logs/run2/own_*.out`).
  - **15 lose for the side that moved its king.** kpsolve gives A = B on each, and ownchess gives the deciding bound
    (A = L or B = W). The two solvers agree on all 15, so this is CHECKED-2.
  - **Kc3–d2 from (c3, b5)** has bounds (D, L) in both solvers, CHECKED-2.
  - None of the 17 ownchess runs saw a pawn on its second rank, and none hit the watchdog.
- **The two pushes c4–c3 at (b2, a4) and a3–a4 at (c3, b5).** K27 had computed only the position after one capture
  in each. The integrator solved their 4-pawn children with kpsolve and ownchess at cap 1 (`logs/integrator/`). Both
  have bounds (W, L) in both solvers.

## Chess split now in LOOPY (§5.7, the P3.2′ row, §3, §8 item 2, the conjecture list)

- **21 of the 26 deviations lose in chess**, CHECKED-2: the six pushes plus the 15 king moves.
- **5 are not settled at cap 1:**
  - four have bounds (W, L): c4–c3 at (b2, a4), a3–a4 at (c3, b5), and Kc3xc4 and Ka4xa3 at (c3, a4);
  - Kc3–d2 at (c3, b5) has bounds (D, L).
- If any of the five does not lose for the side that plays it, Z_B is not exactly two-shuttle in chess. Cap 2 was not
  run.

The diff was reviewed word by word, and the table cell counts are unchanged.

## Not carried into LOOPY

`REPORT.md` section 3, HA1, is not forcing: after 3...c2+ White has 4.Kxb2 and 4.Kxc2, as `VERIFY.md` §6.2 shows.
The REPORT's cap-2 cost phrases ("CPU time of the order of hours", "far beyond 20 minutes") are unsupported, per
`VERIFY.md` §6.3. Both are withdrawn. `REPORT.md` is kept verbatim as the delegate's output.
