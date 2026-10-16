# Literature: ML / RL / LLMs × CGT and chess engines (survey, 2026-10-15)

*Compiled by a Claude research subagent using web search; citations not yet individually re-verified. Absence claims ("no one has…") are from searching, not exhaustive.*

## A. What exists

**Zhou & Riis line (impartial games / parity)**
- Zhou & Riis, *Impartial Games: A Challenge for Reinforcement Learning*, arXiv 2205.12787; *Machine Learning* 115, 54 (2026). AlphaZero-style agents learn 5-heap Nim (~90% value accuracy), degrade at 6 heaps (~60%), and are near random at 7. They separate "champion" (Elo) from "expert" (optimal-move) mastery. Their partizan control ("partisan Nim") is a sum of integers, so it has no parity structure. **Partizan sums with nimber or infinitesimal parts are untested.**
- Zhou & Riis, arXiv 2312.05379: label noise collapses parity learning.
- Riis, arXiv 2411.06403: fixed-depth quantised nets lie in AC0 and cannot do parity at scale; proposed fixes are Lean-checked.
- Nearest neighbours:
  - Nicholson, *What Value Forgets* (NeurIPS 2026): neural search for positions that share an exact CGT value, on Domineering and Digraph Placement.
  - Nicholson's `partizan` repos (GPL-3): `bitmesh` (chess decomposition certificates from locked-pawn barriers) and `astralbase` (bounded chess retrograde analysis), Rust, alpha stage. **Closest existing tooling — check before building B1/C1.**

**Engines on sums and endgames**
- Husna & Müller, CG 2024 (LNCS 15550): KataGo on Go endgames with CGT ground truth. It fails on "long corridors of similar values", and deeper search sometimes flips correct moves to wrong ones. **The number of components was not varied.** This is the closest prior work to C1.
- Müller, *Decomposition Search*, IJCAI-99: alpha-beta is impractical at about 15 moves, while CGT local search solves endgames of 60 or more moves.
- Haque, Wei & Müller (ACG 2021) and Sadmine, Husna & Müller (ACG 2023): Lc0 and Stockfish policies compared against tablebases on 3–5 pieces.
- Fortresses: Guid & Bratko 2012; Monroe & Chalmers arXiv 2409.12272. Penrose positions: Zahavy et al. arXiv 2308.09175. Null-move pruning is blind to zugzwang.
- Consistency and adversarial work: Fluri, Paleka & Tramèr arXiv 2306.09983 (inconsistent engine evaluations); Wang et al. ICML 2023 (KataGo cyclic blind spot); Tseng et al. arXiv 2406.12843. **No adversarial-policy attack on Lc0 was found.**

**LLMs and RLVR**
- LLM chess benchmarks:
  - Ruoss et al. arXiv 2402.04494 (ChessBench; searchless 270M transformer, 2895 blitz).
  - ChessArena arXiv 2509.24239 (no LLM beats Maia-1100).
  - LLM CHESS arXiv 2512.01992.
  - Song et al. arXiv 2512.15033 (collapse under board rotation or mirroring).
- Game benchmarks: GTBench (arXiv 2402.12348) and MetaNIM Arena (arXiv 2503.16814) test *playing* Nim, not computing values.
- RLVR:
  - Hwang et al. arXiv 2507.00726 (GRPO on chess plateaus).
  - SPIRAL arXiv 2506.24119.
  - Reasoning Gym arXiv 2505.24760 (100+ tasks, **no Nim or CGT task**).
  - Enigmata, SynLogic, Logic-RL, Sudoku-Bench, TinyZero.
  - **No GRPO work on Grundy values, canonical forms or game sums was found.**

**Neural CGT and compositionality**
- No neural predictor of canonical forms or temperatures was found apart from Nicholson.
- Parity is hard: Barak et al. arXiv 2207.08799; Hahn & Rofin arXiv 2402.09963.
- Group addition is learnable in-distribution: grokking arXiv 2201.02177; Nanda et al. arXiv 2301.05217.
- Deep Sets (arXiv 1703.06114) is the natural architecture for disjunctive sums.

**Tooling on an Apple M4 Pro**
- `mlx-lm` 0.32 does LoRA, DoRA and QLoRA but not GRPO. `mlx-lm-lora` 5.8.6 has GRPO, DAPO, GSPO and PPO with custom Python rewards via `@register_reward_function`.
- OpenSpiel 2.0.2 has macOS arm64 wheels for Python 3.11–3.14. LightZero arm64 wheels only cover Python ≤3.11.
- nnue-pytorch documents MPS via conda; the variant fork assumes CUDA.
- **Fairy-Stockfish has no cylinder support**: issue #753 was closed as not planned because it "requires big changes to move generation".
- Lc0 has a Metal backend; Stockfish runs natively on ARM.

## B. Gaps (where this project is new)
1. No benchmark of Stockfish, Lc0 or LLMs on chess positions with **certified CGT sum structure**, and no scaling study over the number of components k.
2. Untested: is it the **nimber or infinitesimal part**, rather than partizanship, that drives difficulty?
3. No train-on-components / test-on-sums study.
4. No RLVR environment for CGT.
5. No LLM evaluation on zugzwang or tablebase-verified endgames.
6. No AlphaZero study on Dawson's chess or Elkies pawn games.
7. No engine, NNUE or equivariant-network study for cylinder chess.

## C. Ranked experiments (novelty × feasibility)
1. **ChessSums benchmark** (20). Hypothesis: accuracy falls with the number of \*-components, not integer ones, and nodes-to-solve grow exponentially in k. Success: a parity gap of at least 20 points at k ≥ 4, p < 0.01.
2. **Compositional value learning** (20). Train on k ≤ 2 and test on k = 3–8. Compare an MLP/CNN, a transformer, Deep Sets with a structured latent (a Z₂^m part for nimbers and a real part for numbers), and two-frame input.
3. **AlphaZero on Dawson's chess and Elkies pawn boards** (17.5). Ground truth from OEIS A002187; measure Elo against expert accuracy as n grows.
4. **GRPO on Conway arithmetic for 0.5–3B LLMs** with `mlx-lm-lora` (16).
5. **Circular-padding CNN for cylinder chess** (9). Measure sample efficiency and inconsistency under file rotation.
