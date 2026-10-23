# K10 review: the frozen-king passer certificate (Proposition 2.11) and P11

**Outcome (2026-10-22).**
- The opencode (beam-free) draft in `REPORT.md` and `EDITS.md` is **FALSE**.
- The applied text is `EDITS_final.md`: 8 edits, applied 8, rejected 0. Edits 1–4 replace Remark 2.11 and the rows
  R2.11, P11 (status table) and P11 (§6). Edits 5–8 bring the preamble, the K3 remark and §7 items 1 and 5 up to date.
- New labels:
  - Proposition 2.11 is PROVED in P (frozen), as a sufficient condition.
  - P11 is PROVED in P in a conditional form: every passer and race terminal must be certified (and, after the
    second round, a root that already has a passer must itself satisfy Proposition 2.11).
  - The real-king square rule is a CONJECTURE.

## Who did what

1. **Draft.** opencode beam-free (`REPORT.md`, `EDITS.md`) drafted a certificate "μ ≥ d + 1", with labels "PROVED in P"
   for both 2.11 and P11.
2. **Two Sonnet 5.5 reviewers** (workflow `wf_be7404d6-399`) both returned FALSE.
   - The logic lens found 12 problems, the computational lens 9; each lens had its own enumerator and compared
     against `kpsolve --frozen`.
   - The fatal error is the step "a passed pawn stays passed". An ω pawn can capture a β pawn on a neighbouring
     file, land beside p's path, and then capture p, or take it e.p. after its double step.
     Example: `Ka1 ka6 Pc2 Pd4 Pe2 pe5 b -` (cyl:8x6 or 7x6, `--frozen`) is (L, L), with 1…exd4 and dxc3.
   - The draft also ignored:
     - checks (`Ke2 ka6 Pc4 pf4 b -` is (L, L));
     - a king of either colour on the path;
     - the move order in which the beneficiary moves first, where the threshold is μ ≥ d;
     - non-passers of the opponent. The count rule is not a certificate: `Ka1 ka6 Pc2 Pd4 pd3 b -` is (L, L),
       although cylcgt credits White.
3. **Sonnet 5.5 fixer.**
   - It rebuilt the statement with hypotheses (H1)–(H5):
     - (H1) clear path, kings included;
     - (H2) no check;
     - (H3) no stalemate;
     - (H4) every other β pawn on a neighbouring file has ρ ≤ ρ(p) + 1;
     - (H5) μ_ω ≥ e + 1 over all ω pawns, with e = d or d − 1 by the move order.
   - It added Corollaries 2.11a ((V2) at every terminal shape, races included) and 2.11b (P11's layout needs only
     (H4) and (H5)).
   - It checked these against `kpsolve --frozen`, with 0 violations everywhere:
     - 954,392 parked-king positions with side to move (each certified for one β);
     - 60,000 random-king positions with side to move;
     - 56,872 roots end to end (roots without a passer).
   - Dropping any one hypothesis produces violations.
4. **Integrator (this session).**
   - Read the proof step by step: Step 0 (F1–F3), king safety, the invariants (J_β), (J_ω) and (I1), the e.p.
     cases, and the timing. It found no false step.
   - Re-ran every cited example on a separate kpsolve build and confirmed all of them.
   - Corrected these points:
     - The (H3) example P1a also fails (H1), since the black king stands on c6, the promotion square. It was
       replaced by `Ke1 ka6 Pa4 Pc5 Pg5 pa5 b -`, which is (D, D); there only (H3) fails, and without g5 the
       position is (W, W).
     - H ≥ 5 is now required, because the double-step formula for d needs it.
     - The count-rule remark's inequality dp ≥ μ now carries its proviso: no king may stand on the passer's path.
     - The attributions now say who drafted the proof and who checked it.

## Files

- `EDITS_final.md`: the applied edits.
- `scripts/`: the fixer's scripts and logs, copied from the session scratchpad; their paths still point there.
  - `cert.py` decides (H1)–(H5) with its own move generator.
  - `direct.py` and `direct2.py` run the enumerations against `kpsolve --frozen`.
  - `e2e.py` runs the end-to-end D → P check.
  - `realk.py` is the real-king scratch check, run with the P-model build of `../K7/scripts/draft/kp_p.c`.
- `REPORT.md` and `EDITS.md`: the opencode draft, kept as a record. Do not use them.

## Still open

- No model outside the Sonnet family has re-derived Proposition 2.11. K10v checked the computation, and the second
  round (`../K10r2/REVIEW.md`) read the proof again and fixed P11's root case.
- P11's own harness does not test (H4) and (H5). Only `scripts/e2e.py` does, on the roots listed in LOOPY.
- With real kings nothing is proved. `Ka1 ka6 Pc2 w -` satisfies (H1)–(H5) and is (W, W) frozen, but (D, D) both
  in P with real kings and in chess.
