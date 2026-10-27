# K22 review: Lemma 2.9 without its added hypothesis (integrated 2026-10-27)

**Outcome: accepted with fixes.** `EDITS_FINAL.md` applies the referee's three fixes.

- Lemma 2.9 now holds under the hypothesis (B1), which is weaker than the old one. Without (B1) it is false:
  counterexamples on flat:4x5, cyl:7x6 and, newly, flat:3x5.
- **Integrator re-run.** For flat:3x5 `Kc4 ka5 Pa2 Pa3 pb3 pb4 b -`, the referee's `verify/mylocal.py` gives minT = 3
  with and without the queen clause, and every Black reply, the pass included, loses. K22's `scripts/local_py.py` gives
  WIN T=3. flat:4x5 `Kd4 kb5 Pb2 Pb3 pc3 pc4 b -` also gives minT = 3 with `mylocal.py`.
- **Integrator addition.** §5.2 applies Lemma 2.9 to Kd5 and Kf5, where s's king is not yet on f at Q_Z. The text now
  states the step: s plays Ke5 first, after which (J1) and (J2) hold, and the proof's induction starts at s̄'s next
  turn.
- **Labels.** The search over 74,469,430 roots is COMPUTED-1, a bounded search; the proof of (B1) is separate.
