# K21 review: a sum theorem for loopy components (integrated 2026-10-27)

**Outcome: accepted with fixes.** `EDITS_FINAL.md` applies F1–F5 from `VERIFY.md` and adds the referee's second
counterexample.

- **Proved, each as one AI proof re-derived step by step by the referee:**
  - T3.7 (bridge under first-event dominance);
  - T3.8 (reserve criterion), which contains Theorem 1.11(b) and is strictly stronger;
  - Corollary 3.8b;
  - P3.9 (reserves of on, off, over, under, dud);
  - P3.10;
  - T3.11 (sandwich between off/dud and on).
- **Checks.** The brute-force checks are CHECKED-2: `dsum.py` and the referee's `ref.py` agree on 20,324 states.
  The chess P-model oracle counts were not re-run and are COMPUTED-1.
- **Integrator fixes.**
  - The on/off extension of Corollary 3.8b is now "argued from the proof", because the referee re-derived only the
    finite-reserve statement. It was tested on 1,810 instances, COMPUTED-1.
  - The T3.11 status row now separates K21's 142,798 states from the referee's 6,150 instances.
