# E3, E5, E6: what the networks know before any search

The results and their reading are in [`../ENGINES.md`](../ENGINES.md) §5.3 and §5.4.

**Material.** The 275 tablebase-probed positions of `../suite/results.json`, and for each one its twin: the same
men with the other side to move. All 275 twins are legal.

**Labels.**
- For the originals: the Lichess tablebase root result.
- For every position: the CGT outcome class of its queenside component. It is computed by `cylcgt` on the 4-file
  flat 8-rank board, e.p. on, race rule `count`, with the textbook passed test. The suite's predictions are
  unchanged under the e.p.-aware test (`../suite/ep_aware_check.py`).
- Twins are judged against the CGT class only, because they were not probed.

| File | What it is |
|---|---|
| `static_eval.py` | Stockfish's `eval` command on every position and twin: the raw NNUE output and the final static evaluation, White's point of view. No search |
| `lc0_value.py` | Lc0 `go nodes 1` on every position and twin: the value head's score and the policy head's move |
| `compare.py` | Side-by-side tables (ENGINES.md §5.3), plus Lc0's one-node policy on the 233 EPD positions (§5.4) |
| `results/static_eval.json` | Per-position data from `static_eval.py` |
| `results/lc0_value_n1.json` | Per-position data from `lc0_value.py` |

The engines were Stockfish 19 (`engine/vendor/Stockfish/src/stockfish`, network `nn-1a298aa575a0.nnue`) and
Lc0 0.32.1 from Homebrew (network `42850.pb.gz`, Metal backend, default options).

Status: computed once. Each engine has one network, and the sample is stratified.

## Reproduce

Run from the project root, one command per block.

```bash
PYTHONPATH=. .venv/bin/python engine/experiments/static_eval.py --engine engine/vendor/Stockfish/src/stockfish
```

```bash
PYTHONPATH=. .venv/bin/python engine/experiments/lc0_value.py --engine /opt/homebrew/bin/lc0 --nodes 1
```

```bash
.venv/bin/python engine/experiments/compare.py
```

Re-print the per-engine tables without rerunning the engines:

```bash
PYTHONPATH=. .venv/bin/python engine/experiments/static_eval.py --summary
```

```bash
PYTHONPATH=. .venv/bin/python engine/experiments/lc0_value.py --nodes 1 --summary
```
