# T5 (cursor-agent): ML baselines on ChessSums

Output directory: `ml/chesssums_baseline/`. Use `.venv-ml/bin/python` (PyTorch 2.14 with the MPS backend, MLX 0.32).

Read `bench/README.md` and `bench/REPORT.md`. The data is in `bench/data/*.jsonl`: train 20k, val/test 2k, test_heldout 2k (held-out component types), plus 8-file subsets.

1. Train two small models to predict the outcome class (L/R/N/P) of an instance from its board:
   - (a) an MLP or small CNN on a one-hot board encoding;
   - (b) a small transformer over per-file tokens.
   Keep each training run under 20 minutes on MPS.
2. Report accuracy by number of components k, on test (k in the training range) and on 4-6 components (compositional generalisation), plus test_heldout.
3. Compare with a "CGT oracle" baseline that sums the true component values, which is 100% by construction, and with a majority-class baseline.
4. If time remains, add a value-string or best-move task.
5. Use the scorer in `bench/score.py` wherever it applies.
6. Write `ml/chesssums_baseline/REPORT.md`, with the accuracy-vs-k table and exact training commands.
