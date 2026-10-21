# engine/: engines versus CGT, a cylinder engine design, and a verified test suite

| Path | What it is |
|---|---|
| [`ENGINES.md`](ENGINES.md) | How the search heuristics of Stockfish 19 (cited by file and line at tag `sf_19`) and of Lc0/AlphaZero-style MCTS interact with zugzwang, tempo battles, nimbers and sums. Predictions P1–P11 and L1–L5, experiments E1–E8, and a scorecard of what the measurements say |
| [`FAIRY_CYLINDER.md`](FAIRY_CYLINDER.md) | The state of cylinder support (Fairy-Stockfish issue #753; a read-only review of the `mtaktikos/CylindricalChess` copy) and a design: bitboard wrap, slider tables, two-route lines, the perft plan, NNUE features |
| [`suite/`](suite/) | An EPD suite of real 8×8, ≤ 7-man king-and-pawn positions whose winning moves CGT dictates, each checked against the Lichess 7-man tablebase. See [`suite/README.md`](suite/README.md) |
| [`run_suite.py`](run_suite.py) | Runs any UCI engine on an EPD file and scores it. Supports node, depth and time sweeps, records the solution depth, and writes JSON output. Stdlib only |
| [`ablation/`](ablation/) | E2: Stockfish 19 rebuilt with one search heuristic off at a time, run to depth 16 on the suite |
| [`experiments/`](experiments/) | E3/E5/E6: Stockfish's static eval and Lc0's one-node value and policy, on the probed positions and their side-to-move twins |
| [`runs/`](runs/) | Earlier node and depth sweeps of Stockfish 19 and Lc0 0.32.1 on the suite |
| [`perft/`](perft/) | Two reference move generators for the 8-file cylinder (C and Python), checked against published flat perft and each other; cylinder perft of the start position to depth 6 and of seam test positions |
| [`mock_uci.py`](mock_uci.py) | A random-legal-move "engine", used only to self-test the harness |
| [`test_suite_files.py`](test_suite_files.py) | Offline consistency tests for the EPD files, including the e.p.-aware re-check |

Engines used (installed earlier with the user's approval; nothing was installed by this workstream):
- Stockfish 19, built from tag `sf_19` in `engine/vendor/Stockfish/`;
- Lc0 0.32.1 from Homebrew.

`engine/vendor/` is git-ignored. It also holds the ablation builds.

## Main results (details and caveats in ENGINES.md §0 and §5; each computed once)

- **Static evaluation.** Stockfish's NNUE static eval gets the side to move's fate right for 96% of CGT-number
  positions, but for only 25% of nimber positions. Lc0's value head gets 88% of the nimber positions.
- **Pruning.** Null-move pruning and Step-15 pruning are inert in king-and-pawn positions until a promotion,
  and reverse futility pruning is the zugzwang-relevant cut. Every heuristic changes the cost of these shallow
  positions by at most about 10%.
- **Search.** Both engines solve the ≤ 7-man suite at 1,000 nodes. The stress test has to be sums beyond 7 men.

## Reproduce

Run everything from the project root, `/Users/aritro/Downloads/Research/Chessendgames`, one command per block.

Run the consistency tests (offline):

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q engine/test_suite_files.py
```

Self-test the harness with the random mover. It solves about 22% of the verified suite (40/181), which is
the chance baseline:

```bash
.venv/bin/python engine/run_suite.py --engine ".venv/bin/python engine/mock_uci.py" --epd engine/suite/cgt_verified.epd --movetime 10
```

Run a real engine. Do not give it Syzygy:

```bash
.venv/bin/python engine/run_suite.py --engine engine/vendor/Stockfish/src/stockfish --option Threads=1 --option Hash=64 --epd engine/suite/cgt_verified.epd engine/suite/cgt_disagree.epd --nodes 1000 10000 100000 --json engine/results_stockfish.json
```

The experiment commands are in `ENGINES.md` §8, `ablation/README.md` and `experiments/README.md`. The suite
build pipeline, and the network use behind it, are documented in `suite/README.md`.
