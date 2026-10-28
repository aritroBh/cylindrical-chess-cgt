# K18 review: tempo matching (§8 open question 1) (integrated 2026-10-28)

**Outcome: accepted with fixes.** The integrator applied `EDITS_FINAL3.md`: 3 blocks, 0 rejected, cell counts
unchanged.

How it got there:
- `EDITS.md`: the investigator's edits.
- `VERIFY.md`: the first referee, ACCEPT_WITH_FIXES. It found the e.p.-lapse gap in Proposition 8.1.
- `EDITS_FINAL.md`: the first fix round. It repaired Proposition 8.1 with (P1e).
- `verify/P81_RECHECK.md`: a fresh referee (Sonnet) re-derived the repair: ACCEPT_REPAIR, with four wording fixes.
- `EDITS_FINAL2.md`: the second fix round. It applied those fixes, made 256 → 248, reworded the 292 cases, and added the
  referee's μ_s fact as data.
- `EDITS_FINAL3.md`: the integrator's two wording fixes, below.

## Result in LOOPY (§8 item 1, Appendix A)

- **Tempo matching as worded is FALSE in P.**
  - 42 of 2,305 legal cases are not punished (ES 29, ES7 7, E3 6). The ES and ES7 cases are CHECKED-2: the referee
    rebuilt them cell by cell. The E3 failures were confirmed with `ref3`.
  - The smallest counterexample is `Ka1 Pa2 kc1 pa3`, sortie Ka1–h1, context `Pe2 Pg2 pf4`.
  - In all 29 ES failures a free White context pawn promotes within 3 moves (μ_s ≤ 3 ≤ T). This is data, COMPUTED-1.
- **It held in the 292 promotion-free cases.** 123 of them are CHECKED-2. Beyond those cases it is a CONJECTURE.
- **Proposition 8.1 (tempo pairing) is PROVED after repair.** It is re-derived by a second referee of the same model
  family. The lapse game, which might make (P1e) unnecessary, is a CONJECTURE.

## Integrator fixes in EDITS_FINAL3.md (from the second Haiku check)

- "The referee added the option 's may let a pending e.p. right lapse'" now names the first K18 referee
  (`VERIFY.md`). That experiment (5,293,277 won states) and the 36 e.p.-only states are in `VERIFY.md`, §4.
- "No mechanism is claimed for the rest. A guess is …" now reads "No mechanism is established for the rest; one guess
  (a CONJECTURE) is …".

## Checker points not changed

- The 292 cases. The text gives the reason that s has no more spare moves than s̄ in all of them: the 153 shared-gap
  cases have contexts of value 0, and the 139 reservoir cases have Δ ≤ 0. The checker wanted a measured Δ for the 153;
  a context of value 0 has no spare-move surplus for either side, so the sentence stands.
- `summary.json` is the investigator's output and stays verbatim. It is stale: 2,233 punished, where VERIFY.md
  recounts 2,263.
- Disclosure: the second referee ran its four sweep jobs at nice 15 without `heavy.sh`. Appendix A records this.
