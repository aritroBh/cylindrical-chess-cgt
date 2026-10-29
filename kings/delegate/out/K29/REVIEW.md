# K29 review: universal zeros in P (open question 6; integrated 2026-10-29)

**Outcome: accepted with the referees' fixes.** The investigator's report is `findings.txt` (= `FINDINGS.md`) and
`summary.json`; the first referee wrote `VERIFY.md` (it corrected the candidate count to 1,236 groups in 446 classes);
after the continuation run, a second referee wrote `VERIFY2.md` (ACCEPT_WITH_FIXES) and replacement edits
`verify/EDITS2.md`, informed at the end by a parallel referee's summary (`verify/summary_refB.json`). The integrator
applied `verify/EDITS2.md`: 4 blocks, 0 rejected, table cell counts unchanged.

## Result

- On cyl:7×6 (F_Z = a–c, all 885 contexts of at most two pawns a side on e, f) four classes (14 groups) act as 0 beside
  every context, with T_P ≥ 2 on both sides. CHECKED-2 (kp_p + ref3 for P, kpsolve --frozen + ref3 --frozen for the
  frozen model, two parkings; the referee re-solved all 60 candidate groups and got the same 14).
- Two of the four fail beside `Pf2 pf3 pf4 pf5`: the zero depends on the context class (CHECKED-2). The other two have no
  failing context in the samples of at most three pawns a side (COMPUTED-1).
- T_P is not the T of Definition 2.6, which was not computed: the CONJECTURE of Proposition 2.10(b) is not refuted.

## What the referee changed in the edits

- "T ≥ 2" replaced by T_P where only T_P was measured.
- Flat 7×6 on e, f: only two of the four classes survive, not all four.
- The movers in the T_P sentence were reversed; "its mirror" named a different class.
- Of 107 re-checked classes, 90 were checked on one context file only (63 contexts); now said.
- The LOOPY guess (sortie king cannot reach the buffer in time) is "not necessary", not refuted.

## Not settled

- Lemma N1 of the addendum needs the hypothesis "not in check in the bare group" (all 47 witnesses satisfy it). Not in
  LOOPY.
- The investigator broke the 20-minute rule on several runs (its own report, `logs/pids.log`).
