# T6 (muse): ML on Dawson's chess (plan item C3)

Output directory: `ml/dawson/`. Python: `.venv-ml/bin/python`.

## 5-line summary

1. Built an exact environment for normal-play Dawson's chess as sums of strips: a position is a multiset of strip lengths; outcome = (XOR of g(length_i)) != 0, with g from octal 0.137 (period 34, last exception 51).
2. Trained an LSTM value network (64 hidden) on 12,000 positions with total <= 30; tested on 10,000 positions with totals 31-80.
3. Test accuracy 0.820 overall (train 0.862), only ~0.03-0.05 above the majority-class baseline (~0.79); accuracy is flat across total length (0.806-0.826).
4. Probing: strip features encode single-strip win/loss (binary outcome) at 0.80 (train) / 0.84 (test), but exact Grundy g(n) poorly (0.33 / 0.06); the net does not recover full nimbers.
5. Conclusion (COMPUTED-1, negative): supervised outcome training does not induce the XOR-of-Grundy rule in a way that extrapolates; the net learns a binary hot/cold signal, not nimber magnitudes.

## 1. Environment

- `ml/dawson/env.py` reuses `dawson/octal.py` (read-only) for g(n).
- `g(n)` for n=0..200, period 34 for n>=52 (last exception 51), max value 9.
- Position representation: padded list of strip lengths (up to 80 strips), plus mask.
- Ground truth: `outcome_strips(lengths) = 1 if xor_i g(length_i) != 0 else 0`.
- Data: `ml/dawson/gen_data.py` generates train (totals 1-30, 400 per total = 12,000) and test (totals 31-80, 200 per total = 10,000), seeded.

Reproduce data:
```
PYTHONPATH=. .venv-ml/bin/python -m ml.dawson.gen_data
```

## 2. Model and training

- `ml/dawson/model.py`: LSTM over strips. Each strip length (scalar, normalized by 80) -> embedding (64) -> LSTM (64) -> linear head -> logit.
- `ml/dawson/train.py`: Adam lr=1e-3, BCEWithLogitsLoss, batch 256, 40 epochs, MPS.

Reproduce training:
```
PYTHONPATH=. .venv-ml/bin/python -m ml.dawson.train
```
Output (final): train_acc 0.8619, test_acc 0.8201.

We also tried an MLP on a count histogram (test 0.748) and a DeepSets with sum (0.714 majority collapse) and product aggregation (0.753); the LSTM performed best and is the reported model.

## 3. Accuracy vs total length

Evaluated by `ml/dawson/eval.py`:

| total range | n | net acc | majority baseline |
|---|---|---|---|
| 31-40 | 1800 | 0.806 | 0.769 |
| 41-50 | 2000 | 0.817 | 0.777 |
| 51-60 | 2000 | 0.824 | 0.802 |
| 61-70 | 2000 | 0.826 | 0.794 |
| 71-80 | 2200 | 0.826 | 0.804 |
| overall | 10000 | 0.820 | 0.790 |

Reproduce:
```
PYTHONPATH=. .venv-ml/bin/python -m ml.dawson.eval
```

Single-strip outcome accuracy on lengths 1-80: 0.825 (exact rule 1.0).

## 4. Probing features vs g(n)

`ml/dawson/probe.py`: linear probe from LSTM strip embedding (64-dim) to Grundy value g(n) (10 classes) or binary outcome.

| probe | train (n=1..30) | test (n=31..80) |
|---|---|---|
| g(n) (10-class) | 0.333 | 0.060 |
| g(n)!=0 (binary) | 0.800 | 0.840 |

Majority baseline for g(n) on test: 0.24.

Reproduce:
```
PYTHONPATH=. .venv-ml/bin/python -m ml.dawson.probe
```

Interpretation: the network's per-strip features carry enough information to decide whether a single strip is a first-player win, but not the exact Grundy value. Since the XOR-of-Grundy rule needs full nimber values, the net cannot have learned that rule; it approximates outcome via a binary signal. This is consistent with the small margin over the majority baseline on multi-strip sums.

## 5. Ring (cylinder) positions

Not included in the supervised training set; the environment supports ring components (`ring_value(n) = 1 iff g(n-3)==0`) but the ML task focuses on flat strip sums as stated. Extending to ring components is straightforward and left as future work.

## 6. Optional AlphaZero self-play

Not attempted (optional). The exact solver is available via nim-sum, so a future loop could compare MCTS+net move choices against optimal; skipped due to time budget.

## Status labels

- Environment and ground truth: CHECKED-2 (agrees with `dawson/octal.py` and `dawson/pawnboard.py`).
- Training numbers: COMPUTED-1 (single run, seeded; not replicated across architectures beyond the reported comparison).
- Probing conclusion: COMPUTED-1.
- Claim "net does not learn XOR-of-Grundy rule": CONJECTURE-level interpretation of the probing result; the negative result on g(n) probe supports it but does not prove absence of an internal representation not linearly decodable.
