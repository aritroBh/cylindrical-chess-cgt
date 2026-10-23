# K10 second round: two fresh Sonnet reviewers on Proposition 2.11 and P11

**Outcome (2026-10-22).** The proof stands, P11 was missing one case, and the rest was wording.

- **Proof.** Both reviewers read Steps 0–5 and Corollaries 2.11a and 2.11b against `cylcgt/pawns.py` and
  `kings/kpsolve.c`, and found no error.
- **Computation.** The search reviewer's own checker found 0 violations in 5,730,596 certified positions with side
  to move, or 6,783,482 instances (position, side to move, β, p). The boards were cyl:4×6 to 8×6, 6×7 and 6×5,
  with parked kings (exhaustive) and free kings. The flat boards 5×6, 6×6, 7×6 and 6×7 added 434,429 positions,
  also with 0 violations.
- **One real gap: P11's root.** P11 claimed `--frozen` = o(W(X)) whenever the terminals are certified by
  Corollary 2.11a. That corollary covers only nodes reached by a move, so a root X that already has a passer was
  not covered. Counterexample: cyl:8×6 `Ka1 ka6 Pc2 Pd4 pd3 b -` is a White win in W(X) but (L, L) in `--frozen`;
  the integrator confirmed it on its own kpsolve build. Fix: P11 now also requires Proposition 2.11 at X itself,
  with s the side to move and β the side that W(X) credits. The end-to-end check had already restricted itself to
  roots without a passer.
- **Wording, all applied in `kings/theory/LOOPY.md`.**
  - y must be legal: kings not adjacent, and the side not to move not in check.
  - Corollary 2.11b's premise is now "every pawn on c–g". A pawn on the a-file breaks (H3), as in
    `Ka1 ka6 Pa3 Pc2 w -`. The king distance there is 4, not "four ranks apart".
  - In the §6 P11 row:
    - (V1) is credited to the layout, not "by fiat".
    - HSS is now (HSS) and (B) of Theorem 1.11(c), that is (V4) of Theorem 1.14. The old "every component is
      sum-safe" was weaker than what those theorems need.
    - A root is a position with its side to move.
  - In the status row P11: condition (E) is added to (V1), and (V2) at king moves holds by fiat.
  - The examples now say that (L, L) is kpsolve's printed pair of bounds for one side to move, not (r_w, r_b).
  - K10's counts (954,392; 60,000) are positions with side to move, not instances.
  - The flat-board case is no longer "not run".
- **Labels.** Proposition 2.11 is PROVED in P (frozen), sufficient only. P11 is PROVED in P in a conditional
  form, now with the root clause. No model outside the Sonnet family has re-derived the proof.

## Who did what

- Two Sonnet 5.5 reviewers ran in fresh contexts (workflow `wf_71cdbcd4-f28`). They were told not to open
  `K10/` or `K10v/`.
  - "proofcheck" refereed the proof and ran its own end-to-end check. Its verdict was GAP: the P11 root case
    plus six minor points.
  - "search" wrote its own (H1)–(H5) checker and ran the sweeps. Its verdict was SOUND, with three minor wording
    points.
- An earlier launch (`wf_320423e8-2d1`) was stopped by a false-positive safety flag. Haiku 5.5 checked the labels
  in that round; its fixes are commit 61fde1b.
- The integrator (the kings/ side session) did the following:
  - confirmed the counterexample and the (H4)-bound control `Ka1 ka6 Pe2 pc5 pd3 pe5 w -` (cyl:6×6, (W, W));
  - summed the result JSONs (5,730,596 positions, 6,783,482 instances);
  - checked that K10's `direct.py` and `direct2.py` count positions with side to move, each certified for one β;
  - applied the edits.
- Haiku 5.5 then checked the diff for consistency. It found 11 points: the flat boards were counted inside the
  5.7M total, the root clause was missing in three more places, and there were unit and wording slips. All were applied.

## Files

- `verdicts.json`: the workflow's return value, with both verdicts and every problem.
- `search/`: the search reviewer's checker (`chk.py`), drivers (`run_all.py`, `sweep.py`, `flat.py`,
  `ablate.py`, `abl_exh.py`, `remark.py`, `repro.py`), logs, and one result JSON per run. Each JSON has counts
  and tight-case feature tallies.
- `proofcheck/`: the proofcheck reviewer's scripts (`chk.py`, `e2e.py`, `cons.py`, `term.py` and the shell
  drivers). The reviewers shared this directory for a while, so `ex.py` and `sweep.py` here are the search
  reviewer's first versions.
- The kpsolve binaries and the bulk input and output batches were deleted. The scripts point at the old
  scratchpad.
