# Lc0 on the CGT suite

**Setup.**
- Engine: Lc0 v0.32.1 (Homebrew bottle) with its bundled network `42850.pb.gz`, on the Metal backend
  (Apple M4 Pro). Shipped defaults, so smart pruning is on.
- Suite: the same 233 positions and the same node limits as the Stockfish run
  ([`../sf19_nodes.json`](../sf19_nodes.json)).
- Commands: [`run_lc0.sh`](run_lc0.sh); scored by [`analyze_lc0.py`](analyze_lc0.py), which uses
  `analyze_sf.py`'s verdict rule (mate by sign; otherwise ±150 cp).
- Raw results: `lc0_nodes_<limit>.json` and `.txt`.

**Status.** Complete: all four budgets, 233 positions each. The merged file is `lc0_nodes.json`.

## Results

| node limit | positions | best move wins | eval matches tablebase |
|---|---|---|---|
| 1,000 | 233 | 233 (100%) | 233 (100%) |
| 10,000 | 233 | 233 (100%) | 233 (100%) |
| 100,000 | 233 | 233 (100%) | 233 (100%) |
| 1,000,000 | 233 | 233 (100%) | 233 (100%) |

For comparison, Stockfish 19 ([`../analysis.md`](../analysis.md)):
- at 1,000 nodes: 232 best moves win, and 229 evals match;
- at 10,000 nodes and above: at least 232 of 233 on both counts.

### Eval agreement by CGT value class

| CGT class | n | 1k | 10k | 100k | 1M |
|---|---|---|---|---|---|
| hot-BIG | 68 | 100% | 100% | 100% | 100% |
| number | 57 | 100% | 100% | 100% | 100% |
| switch | 37 | 100% | 100% | 100% | 100% |
| infinitesimal | 27 | 100% | 100% | 100% | 100% |
| other-tame | 20 | 100% | 100% | 100% | 100% |
| nimber | 17 | 100% | 100% | 100% | 100% |
| decided | 7 | 100% | 100% | 100% | 100% |

Stockfish's depth sweep has its weakest class at depth 1–2: infinitesimals, at 26–30%.

## Caveats

- **The eval test is easy for 216 of the 233 positions.** 216 are tablebase wins, so any engine that
  says "clearly winning" passes them. The discriminating cases are the **17 tablebase draws**.
  - Lc0 rates all 17 within ±69 cp at 1k nodes, so it calls every one a draw.
  - Stockfish at 1k nodes rates one of them +183 cp.
- **Lc0's node limit is a ceiling, not a target.** Smart pruning stops once the best move is settled.
  - At the 1k limit the median search was 536 nodes (433 to 1,210).
  - At the 100k limit it was 43,586.
  - At the 1M limit it was 431,450 (maximum 996,017).
  - So Lc0 solves the suite with fewer nodes than the limits suggest. Node counts are not comparable
    to Stockfish's, whose nodes are far cheaper.
- **The suite has no Lc0-hard positions.** These are king-and-pawn endings with at most 7 men, which
  the network evidently handles from the policy and value heads alone.
  - The interesting engine tests in `engine/ENGINES.md` (zugzwang, tempo battles, nimbers in sums)
    need larger or more composite positions than this suite contains.
- **The run was slow** (about 35 minutes for the 100k budget and 4.5 hours for 1M) because the machine
  was heavily shared with other jobs. Timing figures are not engine benchmarks.
