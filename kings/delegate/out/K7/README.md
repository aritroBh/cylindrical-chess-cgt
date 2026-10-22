# K7 and K9: repairs of LOOPY Theorem 2.7 and of the sharp form of Theorem 1.14 (2026-10-22)

Both repairs are applied in `kings/theory/LOOPY.md` (commit "kings/: K7 and K9 ..."). Their status rows and
caveats are there.

## K7 (Theorem 2.7)

- A Sonnet 5.5 drafter wrote the repair.
- First review round: three Sonnet reviewers refuted the draft's window form (b), which mishandled an e.p. right
  at Q. A fixer then added the e.p. clause.
- Second review round: three more reviewers rated the final text SOUND, with minor points only, and a final fixer
  applied those points.
- The result is PROVED after repair, in the promotion model P, with μ ≥ T + 1, which is sharp. The theorem gives
  no chess win, and no margin on μ replaces (A_Q); counterexamples are in LOOPY.

Workflows: `wf_f11a89e0-288` and `wf_f944f724-3c1`.

## K9 (sharp form of Theorem 1.14)

- An opencode beam-free agent drafted it, with errors.
- Two Sonnet reviewers and a fixer rewrote it as a simulation lemma (`wf_64932c3e-d58`).
- The integrator then read the rewrite.

## Files

- `final_edits5.txt`: the 26 K7 edits as applied.
- `../K9/scripts/edits_K9_final.txt`: the 3 K9 edits.
- `scripts/draft/`, `scripts/final/` and `scripts/review2/`: the drafter's, fixer's and reviewers' scripts. Their
  paths point at the old scratchpad. `kp_p.c` is the private kpsolve build with a promotion-wins switch.
- `k7_k9_scratch.tar.zst`: local only, not in git, 15.7 MB. It holds the raw rows and intermediate files (290
  files). Unpack it with `zstd -dc kings/delegate/out/K7/k7_k9_scratch.tar.zst | tar -xf - -C /tmp`.
