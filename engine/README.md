# engine/ — engines versus CGT, a cylinder engine design, and a verified test suite

| Path | What it is |
|---|---|
| [`ENGINES.md`](ENGINES.md) | How the search heuristics of Stockfish and of Lc0/AlphaZero-style MCTS interact with zugzwang, tempo battles, nimbers and sums. Includes failure-mode predictions P1–P11 and L1–L5, and experiments E1–E8 |
| [`FAIRY_CYLINDER.md`](FAIRY_CYLINDER.md) | The state of cylinder support (Fairy-Stockfish issue #753; the `mtaktikos/CylindricalChess` copy, read-only review) and a design: bitboard wrap, slider tables, two-route lines, the perft plan, NNUE features |
| [`suite/`](suite/) | An EPD suite of real 8×8, ≤ 7-man king-and-pawn positions whose winning moves CGT dictates, each checked against the Lichess 7-man tablebase. See [`suite/README.md`](suite/README.md) |
| [`run_suite.py`](run_suite.py) | Runs any UCI engine on an EPD file and scores it. Supports node, depth and time sweeps, records the solution depth, and writes JSON output. Stdlib only |
| [`mock_uci.py`](mock_uci.py) | A random-legal-move "engine", used only to self-test the harness |
| [`test_suite_files.py`](test_suite_files.py) | Offline consistency tests for the EPD files |

No engine is installed: plan §8 leaves that decision to the user.

## Reproduce

Run everything from the project root, `/Users/aritro/Downloads/Research/Chessendgames`, one command per block.

Run the consistency tests (offline):

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q engine/test_suite_files.py
```

Self-test the harness with the random mover. It solves about 17% of the verified suite, which is the chance
baseline:

```bash
.venv/bin/python engine/run_suite.py --engine ".venv/bin/python engine/mock_uci.py" --epd engine/suite/cgt_verified.epd --movetime 10
```

Run a real engine, once one is installed. Do not give it Syzygy:

```bash
.venv/bin/python engine/run_suite.py --engine /path/to/stockfish --epd engine/suite/cgt_verified.epd engine/suite/cgt_disagree.epd --nodes 100 1000 10000 100000 --json engine/results_stockfish.json
```

The suite build pipeline, and the network use behind it, are documented in `suite/README.md`.
