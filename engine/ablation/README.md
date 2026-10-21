# E2: Stockfish 19 with one search heuristic switched off

Question: which of Stockfish's search heuristics matter on positions whose correct move is decided by a
CGT tempo or parity fight? The results and their reading are in [`../ENGINES.md`](../ENGINES.md) §2 and §5.2.

| File | What it is |
|---|---|
| `sf19_ablate.patch` | Adds nine compile-time switches to `src/search.cpp` of Stockfish 19 (tag `sf_19`, commit `edb0d9db`). Each one only adds `!ablX &&` to the guard of one step, or makes `correction_value()` return 0 |
| `build.sh` | Copies the vendored `sf_19` source (and its network) to `engine/vendor/sf19_ablate/`, applies the patch, and builds `sf_base` plus one binary per switch with `make all ARCH=apple-silicon EXTRACXXFLAGS=-DABL_X`. It never runs the `net` or `build` targets, so nothing is downloaded |
| `run_ablation.py` | Searches all 233 suite positions with `go depth D` (1 thread, 64 MB hash, `ucinewgame` each time) and keeps every completed iteration's score, cumulative nodes and PV head |
| `analyze.py` | Prints every number in ENGINES.md §5.2, the depth part of §5.1, and the P3/P6 splits |
| `results/*.json` | One file per build, depth 16 |
| `logs/` | stdout of the runs |

The switches:
- `NMP`: Step 10, null-move pruning.
- `SHALLOW`: Step 15, move-count, futility, history and SEE pruning.
- `RFP`: Step 9, reverse futility pruning.
- `RAZOR`: Step 8, razoring.
- `SE`: Step 16, singular extensions.
- `PROBCUT`: Steps 12 and 13.
- `LMR`: Step 18. Moves are then searched at full depth in Step 19.
- `CORR`: correction history off.
- `IIR`: Step 11.

Checks:
- `sf_base` gives the same `bench 16 1 13` node count as the vendored binary (2,497,913).
- Iteration *k* of the depth-16 baseline equals the earlier, separate `go depth k` runs in
  `engine/runs/sf19_depth.json` in all 1398 cases (`analyze.py` section 0).

Status: computed once. The runs are deterministic, so a rerun gives the same numbers on the same machine and
build.

## Reproduce

Run from the project root, one command per block.

Build all ten binaries (about 15 s each):

```bash
sh engine/ablation/build.sh
```

Run them. This is one process per build; each takes 10-150 s at depth 16 (LMR-off is the slowest):

```bash
for v in base NMP SHALLOW RFP RAZOR SE PROBCUT LMR CORR IIR; do .venv/bin/python engine/ablation/run_ablation.py --depth 16 --timeout 300 --bin "$v=engine/vendor/sf19_ablate/bin/sf_$v"; done
```

Analyse:

```bash
.venv/bin/python engine/ablation/analyze.py
```
