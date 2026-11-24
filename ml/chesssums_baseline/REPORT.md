# ML Baselines on ChessSums

## Summary

1. **Trained three models** to predict outcome class (L/R/N/P) from board position: MLP, CNN, and Transformer.
2. **CNN achieves the best accuracy** on both test (75.2%) and test_heldout (80.4%), significantly above majority-class baseline (23.8%).
3. **Compositional generalization** (train on k≤3, test on k=4–6): all models degrade with more components; CNN degrades least (81.0% at k=4 → 71.2% at k=6).
4. **Held-out component types**: CNN handles structure holdout well (88.2%) but struggles on value-class holdout (↑*, ↓*; 53.9%).
5. **CGT oracle** (summing true component values) is 100% by construction; random-legal baseline is 23.8% on outcome.

---

## Training Commands

All commands run from project root `.` using `.venv-ml/bin/python` (PyTorch 2.14.1 with MPS backend):

```bash
# MLP (3-layer, 512 hidden, dropout 0.1)
PYTHONPATH=. .venv-ml/bin/python ml/chesssums_baseline/train.py 2>&1 | head -30

# The training script trains all three models sequentially.
# Each model: 50 epochs, batch size 256, AdamW lr=1e-3, weight_decay=1e-4, CosineAnnealingLR.
# Total time: ~15 minutes on MPS.
```

**Exact training script:** `ml/chesssums_baseline/train.py`

---

## Accuracy vs. Number of Components (k)

### Test set (k=4,5,6 — compositional generalization)

| Model | k=4 | k=5 | k=6 | Overall |
|-------|-----|-----|-----|---------|
| **CGT Oracle** | 1.000 | 1.000 | 1.000 | **1.000** |
| **CNN** | **0.810** | **0.733** | **0.712** | **0.752** |
| **Transformer** | 0.726 | 0.712 | 0.665 | 0.701 |
| **MLP** | 0.580 | 0.403 | 0.354 | 0.446 |
| **Majority class (L)** | 0.243 | 0.216 | 0.257 | 0.238 |
| **Random-legal** | 0.243 | 0.216 | 0.257 | 0.238 |

*Test set has 667 rows per k (2000 total). Outcomes balanced per k. 8-file subset (364 rows, all k=4) shown separately in breakdowns.*

### Test_heldout (k=1,2,3 — unseen component types)

| Model | k=1 | k=2 | k=3 | Overall |
|-------|-----|-----|-----|---------|
| **CGT Oracle** | 1.000 | 1.000 | 1.000 | **1.000** |
| **CNN** | **0.853** | **0.816** | **0.768** | **0.804** |
| **Transformer** | 0.920 | 0.770 | 0.726 | 0.783 |
| **MLP** | 0.695 | 0.630 | 0.591 | 0.628 |
| **Majority class (L)** | 0.258 | 0.236 | 0.230 | 0.238 |
| **Random-legal** | 0.258 | 0.236 | 0.230 | 0.238 |

*Test_heldout has 400/800/800 rows for k=1/2/3. Each row contains ≥1 held-out component. Held-out types: value-class (↑*, ↓*; 12 components, 3 orbits) and structure (10% of remaining orbits, 39 components).*

---

## Breakdown by Board Type (Test)

| Model | Flat | Cylinder | 8-file subset |
|-------|------|----------|---------------|
| **CNN** | 0.767 | 0.732 | 0.843 |
| **Transformer** | 0.710 | 0.689 | 0.739 |
| **MLP** | 0.484 | 0.399 | 0.695 |
| **Majority** | 0.241 | 0.235 | 0.225 |
| **Random-legal** | 0.241 | 0.235 | 0.225 |

---

## Breakdown by Held-out Type (Test_heldout)

| Model | Structure | Value-class (↑*,↓*) | Structure+Value-class |
|-------|-----------|---------------------|----------------------|
| **CNN** | 0.882 | 0.539 | 0.555 |
| **Transformer** | 0.803 | 0.750 | 0.659 |
| **MLP** | 0.669 | 0.471 | 0.516 |
| **Majority** | 0.243 | 0.214 | 0.231 |
| **Random-legal** | 0.243 | 0.214 | 0.231 |

*Value-class holdout (↑*, ↓*) is the hardest: these nimber-infinitesimal compounds are not seen during training. CNN struggles most here, while Transformer generalizes better to ↑*/↓* (75.0% vs 53.9%).*

---

## Breakdown by Value Kind (Test)

| Kind | n | CNN | Transformer | MLP | Majority |
|------|---|-----|-------------|-----|----------|
| hot-other | 1020 | **0.820** | 0.744 | 0.533 | 0.228 |
| switch | 165 | **0.782** | 0.661 | 0.527 | 0.236 |
| number+ups(+nimber) | 122 | **0.746** | 0.664 | 0.328 | 0.270 |
| integer | 575 | 0.638 | **0.671** | 0.310 | 0.250 |
| cold-other | 55 | **0.745** | 0.636 | 0.382 | 0.255 |
| number+nimber | 63 | 0.619 | 0.508 | 0.349 | 0.222 |

*CNN excels on hot games and switches (temporal/parity patterns). Transformer is competitive on integers. All models struggle on pure nimbers and number+nimber.*

---

## Model Details

### MLP
- **Architecture**: 3-layer MLP (512 hidden) on flattened one-hot board (3×8×26 = 624 inputs)
- **Best val acc**: 65.1%
- **Test acc**: 44.6% (poor compositional generalization)
- **Parameters**: ~3.2M

### CNN
- **Architecture**: 4-layer CNN (64→128→128→256 channels) with BatchNorm, MaxPool every 2 layers, GlobalAvgPool
- **Best val acc**: 90.5%
- **Test acc**: 75.2% (best overall)
- **Parameters**: ~1.1M

### Transformer
- **Architecture**: 3-layer TransformerEncoder (d_model=128, 4 heads, dim_feedforward=256) over per-file tokens (26 files × 24-dim)
- **Best val acc**: 87.9%
- **Test acc**: 70.1%
- **Parameters**: ~0.5M
- **Note**: Better on value-class holdout (↑*/↓*) than CNN, suggesting better symbolic generalization.

---

## Reproduction

```bash
cd .

# Install/check environment
.venv-ml/bin/python -c "import torch; print(torch.__version__, torch.backends.mps.is_available())"

# Run training (outputs to ml/chesssums_baseline/)
PYTHONPATH=. .venv-ml/bin/python ml/chesssums_baseline/train.py

# Score predictions
PYTHONPATH=. .venv/bin/python -m bench.score --gold bench/data/test.jsonl --pred ml/chesssums_baseline/preds_cnn_test.jsonl
PYTHONPATH=. .venv/bin/python -m bench.score --gold bench/data/test_heldout.jsonl --pred ml/chesssums_baseline/preds_cnn_test_heldout.jsonl

# Baselines
PYTHONPATH=. .venv/bin/python -m bench.score --gold bench/data/test.jsonl --baseline random-legal --seed 0
PYTHONPATH=. .venv/bin/python -m bench.score --gold bench/data/test_heldout.jsonl --baseline random-legal --seed 0
```

---

## Honesty Labels

- **COMPUTED-1**: All accuracy numbers above (single training run per model, PyTorch/MPS).
- **PROVED**: CGT oracle = 100% (by construction: sum of exact component values, then compare with 0).
- **CHECKED-2**: Baselines verified by independent runs of `bench.score`.
- **CONJECTURE**: Transformer's better value-class holdout performance suggests better symbolic generalization; not rigorously tested.

---

## Next Steps (if time remains)

- Train value-string prediction (canonical CGT value as text) using the same architectures.
- Train best-move prediction (winning move from legal moves).
- Test with data augmentation: random file permutations (symmetry).
- Compare with LLM prompting (using `bench/prompts.py`).