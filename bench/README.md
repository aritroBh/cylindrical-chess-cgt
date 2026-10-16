# ChessSums: pawn-endgame sums with exact ground truth

ChessSums is a generator and dataset of pawn-only positions built from several independent pawn groups
("components") on one wide board. Each position comes with its exact combinatorial-game value, its
outcome class, and every winning move for each side.

- **Ground truth.** It is computed with `cylcgt`, the project's exact CGT engine. Combinatorial game theory
  (CGT) makes these sums instant to solve: add the component values, then compare the total with 0.
- **Why it is hard for search.** A whole-board search that ignores the decomposition needs a number of
  nodes that grows exponentially with the number of components (table in §8).
- **What it tests.** Whether a model has learned the algebra of sums, through two kinds of held-out data:
  1. *length generalisation*: train on k ≤ 3 components, test on k = 4–6;
  2. *unseen component types*: whole symmetry orbits and one whole value class are held out.

This is workstream C1 of `RESEARCH_PLAN.md`.

> **Status, stated plainly.**
>
> **What this is.** A pawn-only game under the Elkies (1996) convention, *not* full chess. There are no kings.
> A passed pawn wins outright.
>
> **How far the ground truth is checked.**
> - Every value comes from one implementation, `cylcgt`.
> - Outcome classes were re-derived by two searches that do not use `cylcgt`:
>   - Codex's `crosscheck/minimax.py`: 4,607 rows, plus full winning-move sets on 596 rows;
>   - our `bench/ab.c` α-β: all 26,000 rows except 28 that hit its cap.
>
>   There were zero disagreements.
> - Value equalities between components were confirmed independently through difference games
>   (§7, check A2).
>
> **What has not been done.**
> - No LLM or engine has been run on the benchmark yet.
> - Nothing here has been embedded in real chess with kings.

---

## 1. The game

Board: W files (a, b, c, …) by 8 ranks. The board is flat, or a **cylinder**, on which file a and the last
file are adjacent.

Rules:
- White (Left) pawns move up and Black (Right) pawns move down.
- Single steps, double steps from rank 2 or 7, and diagonal captures (across the seam on a cylinder).
- En passant is part of the rules, but no ChessSums position can ever use it (§2, filter 5).
- **Normal play:** a side with no legal move loses.
- **Elkies convention:** as soon as exactly one side has a passed pawn, that side wins. In the CGT model
  this is the number ±BIG, with BIG = 256.
- A move that gives *both* sides a passed pawn starts a promotion race. `cylcgt` resolves races by
  `RACE_RULE`. Every ChessSums component is certified to give the same value, and the same move values,
  under all three race rules (§2).

Pawns change file only by capturing, so an empty file stays empty forever. Groups of pawns separated by
an empty file are therefore independent, and the position is their **disjunctive sum**.

On a cylinder, a group that straddles the a/h seam is one component; one example is files f, g, h, a in
`val-00097` below. A group that leaves at least one file empty plays exactly as it would on a flat strip,
and `components.py` asserts this for every component. A "ring" that fills every file cannot be a summand,
so ChessSums has none.

## 2. The component library (`bench/components.py`, `data/components.jsonl`)

**Candidates.**
- Widths w = 1–4, with every file occupied.
- 2–4 pawns, of both colours, on ranks 2–7.
- No passed pawn at the start.
- One pawn alone is always passed, so 1-pawn components do not exist.

That gives **5,290 candidates**. A component is **kept** only if it passes all five filters below. Each
filter is checked under all six settings: `RACE_RULE` ∈ {count, mover, opponent} × en passant {on, off}.

| filter | dropped |
|---|---:|
| value depends on the race rule | 2,898 |
| value depends on the race rule and on e.p. | 118 |
| value depends on e.p. only | 50 |
| value is ±BIG (a passed pawn already decides it) | 194 |
| canonical form still contains a ±BIG threat somewhere (a hot "passer" game such as `{+W \| *}`) | 1,161 |
| some move leads to a position whose value depends on the race rule or e.p. | 326 |
| an e.p. capture becomes available somewhere in the game tree | 25 |
| **kept** | **518** |

Filters 3 to 5 (the last three rows above) go beyond the task statement, which asked only for "no ±BIG"
and "value independent of the race rule and e.p.":
- **Filter 3 (moves).** Every one-move child value must also be independent of the race rule and e.p.
  Without this, the *set of winning moves* in a sum could still depend on the rule.
- **Filter 4 (BIG-free).** No ±BIG may survive anywhere in the canonical form. This keeps every sum
  `sum_safe` and removes the known "+BIG and −BIG cancel" failure of disjunctive sums (`crosscheck/REPORT_after_fix.md`).
- **Filter 5 (no e.p.).** No e.p. capture may ever arise. `cylcgt` models e.p. per component, but in a real
  sum the right expires after *any* move. With filter 5 the difference cannot arise.

**Sanity example.** The KEY-FACT position `W a2 c2 / B b7 d7` (4 flat files) is \*2 under "count" and
"mover" but 0 under "opponent". It is therefore dropped, and **ChessSums contains no \*2 component**.

**Value spectrum** of the 518 kept components (42 distinct values):
- 0 ×170, \* ×116, ±1 integers ×24 each, ↑/↓ ×20 each, ±2 ×16 each, ±1/2 ×8 each, ↑\*/↓\* ×6 each, ⇑\*/⇓\* ×3 each;
- switches ±1, ±3, 1±1, 3/2±1/2, 5/2±1/2, …;
- a few hot games such as {5/2±1/2 | 1} and {{5/2±1/2 | 1} | 1}.

The full list is printed by `python -m bench.components`.

**Symmetry checks** (asserted for every kept component):
- mirroring the files leaves the value unchanged;
- swapping colours (with the ranks flipped) negates it;
- embedding the strip in a wider flat board, or in a cylinder with one empty file, leaves it unchanged.

**Hold-outs.** Components are grouped into **171 orbits** under mirror × colour-swap.
- **Value class:** every orbit whose value is ↑\* or ↓\* (3 orbits, 12 components).
- **Structure:** a seeded random 10% of the remaining orbits (17 orbits, 47 components).
- Held-out components never appear in train, val or test, only in `test_heldout`.
- Their values are mostly ones also seen in training (0, \*, ↑, ±1, …), except ↑\*/↓\*.
  So "structure" tests whether a model can value an unseen pawn shape.
- Sums in training can still *produce* ↑\* (for example ↑ + \*).
  So "value-class" tests whether a model can value an unseen *component* whose value is ↑\*. It does not
  test a value the model has never seen at all.

## 3. Instances and splits

An instance places k components side by side, with at least one empty file between neighbours.
- **Board.** It is flat or a cylinder, 50/50.
- **Width.** If the components fit, the board has exactly 8 files. Otherwise the width is the minimum
  plus 0–2 extra empty files (at most 26).
- **Placement.** Order, gaps and, on a cylinder, the rotation are random, so components can straddle the seam.
- **Sampling.**
  - A value class is drawn with probability ∝ √(class size), then a component from that class.
  - Rejection sampling **balances the outcome classes L/R/N/P within every (split, k)**.
- **Uniqueness.** Positions (board, wrap, pawns) are unique across all splits.

| split | rows | k | components used | 8-file subset | notes |
|---|---:|---|---|---:|---|
| `train` | 20,000 | 1: 3,000 · 2: 7,000 · 3: 10,000 | 459 non-held-out | 14,271 | outcome-balanced per k |
| `val` | 2,000 | same shares | same | 1,440 | i.i.d. with train (positions disjoint) |
| `test` | 2,000 | 4, 5, 6: about 667 each | same | 344 | half of the k = 4 rows were drawn to fit 8 files |
| `test_heldout` | 2,000 | 1: 400 · 2: 800 · 3: 800 | ≥ 1 held-out per row | 1,574 | each slot is held-out with p = ½, at least one forced |

Each `{split}_8file.jsonl` holds exactly the rows of `{split}` whose board has 8 files. They are **not**
outcome-balanced on their own. The worst case is `test_8file`, with L 140, R 139, N 58, P 7.
- On a flat 8-file board at most four components fit; on an 8-file cylinder, at most four 1-file ones.
  So the 8-file test rows all have k = 4.
- The 400 k = 1 rows of `test_heldout` reuse 59 held-out components in different placements.

Run time on this machine: 339 s for the whole dataset, of which about 80 s builds the component library.

**Determinism.** The generator is seeded (`--seed`, default 20261015). It never relies on object ids
or on string-hash order. The output is sorted where order is otherwise arbitrary. `data/manifest.json`
records the sha256 of every file. A second full run with the same seed, written to a scratch directory,
reproduced all ten files in `bench/data/` byte for byte (checked with `cmp`).

### Record format (one JSON object per line)

```json
{"id": "val-00097", "split": "val", "k": 2,
 "board": {"files": 8, "ranks": 8, "cylinder": true},
 "position": "W: c6 d3 f3 h2 / B: a4 c7 d5 g7",
 "placement": "8/2p3p1/2P5/3p4/p7/3P1P2/7P/8",
 "white": ["c6","d3","f3","h2"], "black": ["a4","c7","d5","g7"],
 "components": [{"comp_id": "C0283", "files": "cd",   "position": "W: c6 d3 / B: c7 d5", "value": "*"},
                {"comp_id": "C0463", "files": "fgha", "position": "W: f3 h2 / B: a4 g7", "value": "↓"}],
 "value": "↓*", "value_ascii": "v*", "kind": "number+ups(+nimber)",
 "outcome": "N", "mean": "0", "temperature": "0",
 "legal_moves":   {"W": ["d3-d4", "f3-f4", "h2-h3", "h2-h4"], "B": ["a4-a3", "d5-d4", "g7-g5", "g7-g6"]},
 "winning_moves": {"W": ["f3-f4"], "B": ["d5-d4", "g7-g6"]},
 "fits8": true, "heldout": []}
```

Field notes:
- `position` uses the `cylcgt` text format (`pawns.Pos.parse` reads it).
- `placement` is FEN-style, rank 8 first. It has no kings, so it is not a legal chess FEN.
- `kind` is a coarse value class used in score breakdowns.
- `temperature` is `null` for numbers.

`components.jsonl` has one row per component, with:
- its value, outcome, mean and temperature;
- its orbit and hold-out tag;
- every local move with the value of the position it leads to.

## 4. Tasks

| task | item | gold | metric |
|---|---|---|---|
| **outcome** | one per row | L (White wins either way), R, N (player to move wins), P (player to move loses) | accuracy |
| **move** | one per (row, side) **that has a winning move** | the set `winning_moves[side]` | fraction answering a winning move; legality rate |
| **value** | one per row | canonical value | the answer is **parsed** and compared as a game, so `1/2 + *`, `1/2*` and `{1/2 \| 1/2}` all count; exact-string match is reported too |

A move wins iff the position after it has outcome L or P (White moved) or R or P (Black moved).

Value notation is standard CGT:
- numbers `3/2`;
- nimbers `*`, `*2`;
- ups `↑`, `⇑*`, `-1↓`, juxtaposed with numbers;
- switches `±1`, `3/2±1/2`;
- anything else as `{A, B | C}`, with options sorted.

There is also an ASCII form (`^`, `v`, `+-`). The parser in `cgtfmt.py` accepts both forms, explicit `+`
sums, parentheses and `+/-`. It has size limits (nimbers ≤ \*32, ≤ 128 arrows, |numbers| ≤ 1024, ≤ 500 terms,
nesting ≤ 12, ≤ 2000 characters), so malicious answers fail fast.

**Read these baselines before reading any score** (`score.py --baseline random-legal`):

| split | random letter, outcome | constant "0", value | random legal move, move (expected) | on items with chance ≤ 1/4 |
|---|---:|---:|---:|---:|
| val | 0.25 | 0.25 | 0.58 | 0.21 |
| test | 0.26 | 0.25 | 0.52 | 0.15 |
| test_heldout | 0.26 | 0.25 | 0.59 | 0.21 |

- **Outcome P ⇔ value 0.** On outcome-balanced splits the constant answer `0` therefore gets 25% on the
  value task. Read the `value!=0` row instead.
- **Many moves win.** The median share of legal moves that win is 1/2. `score.py` reports
  `random_legal_expected` for every group, and rows for `move: chance<=1/4` (675 test items) and
  `move: unique winning move` (616 test items). Those are the informative move numbers. In the
  N-positions of `test`, a random move wins 27% of the time.

### Text prompt for LLMs (`bench/prompts.py`)

```
$ PYTHONPATH=. .venv/bin/python -m bench.prompts --split val --task move --limit 1   # (this example is val-00097, White)
This is a pawn-only game on a board with 8 files (a-h) and 8 ranks. The board is a CYLINDER: files a and h
are adjacent, so pawns on them attack each other across that edge (for example a White pawn on h4 attacks
a5, and a White pawn on a4 attacks h5). White pawns (P) move up the board and Black pawns (p) move down.
There are no kings or other pieces.
Rules:
- A pawn moves one square straight forward to an empty square, or two squares from its starting rank
  (rank 2 for White, rank 7 for Black) if both squares are empty. It captures one square diagonally
  forward. En passant is legal but can never occur in these positions.
- A pawn is passed if no enemy pawn is ahead of it on its own file or on an adjacent file (adjacency wraps
  around the cylinder). As soon as exactly one side has a passed pawn, that side wins at once.
- A player who has no legal move on their turn loses.
- (A move that gives both sides a passed pawn at once cannot change any answer in these positions.)

Position (rank 8 at the top):
8 . . . . . . . .
7 . . p . . . p .
6 . . P . . . . .
5 . . . p . . . .
4 p . . . . . . .
3 . . . P . P . .
2 . . . . . . . P
1 . . . . . . . .
  a b c d e f g h
White pawns: c6 d3 f3 h2
Black pawns: a4 c7 d5 g7

Question: White to move and win. Give one winning move as from-square and to-square, with '-' for a step
and 'x' for a capture, e.g. <answer>e2-e4</answer> or <answer>d4xe5</answer>.
```

(Lines are wrapped here; the real prompt has one line per rule.)

The outcome and value prompts differ only in the last paragraph:
- *outcome*: answer L/R/N/P;
- *value*: give the canonical value in standard or ASCII notation, with examples.

Answers are read from the last `<answer>…</answer>` block, or from the last line if there is none.
`--write items.jsonl` writes one JSON object per item, with the key `score.py` expects.

## 5. Scoring (`bench/score.py`)

```bash
PYTHONPATH=. .venv/bin/python -m bench.score --gold bench/data/test.jsonl --pred preds.jsonl [--json out.json]
```

`preds.jsonl` rows look like `{"item": "test-00012:move:W", "answer": "<raw model output>"}`. You can also
give `{"id", "task", "side"}` instead of `item`. A missing item counts as wrong.

Results are broken down by:
- k;
- flat or cylinder;
- 8-file or wide;
- held-out kind;
- value kind and outcome class;
- for the move task, chance ≤ 1/4 and unique-win.

## 6. Reward for GRPO / RLVR (`bench/reward.py`, draft)

`reward(text, row, task, side)`. The function `chesssums_reward(prompts, completions, gold, task, side)`
has the signature TRL's `GRPOTrainer` expects.

| component | reward |
|---|---|
| exactly one `<answer>` block | +0.1 |
| outcome correct | +1 |
| move: winning | +1 |
| move: legal but losing | +0.1 |
| move: illegal, unparseable or wrong side | −0.5 |
| value: same canonical game | +1 |
| value: optional `partial=True`, wrong game but right outcome class | +0.2 (off by default; gameable) |

`legality_reward` is a separate 0/1 legality signal. Nothing calls a model or a network. This is a draft
and has not been used in training.

## 7. Verification (`bench/verify.py`; report in `results/verify_report.md`)

Full output is in `results/verify_report.md` and `results/verify_summary.json`. The run took 854 s with
4 worker processes. **No disagreements.**

| check | what is compared | implementations | agree / total |
|---|---|---|---|
| A1 | outcome of every component alone, e.p. on and off | `cylcgt` vs Codex `crosscheck/minimax.py` | 1,036 / 1,036 |
| A2 | component c next to a component r of value −v(c): must be P, so v(c) = −v(r). For 504 of 518, r comes from a *different* orbit | same | 518 / 518 |
| A3 | outcome of random component pairs vs the CGT outcome of the summed values | same | 300 / 300 |
| B | value of the whole board (e.p. on and off) and the win/loss of every move, re-solved by `pawns.value` with its own decomposition | `cylcgt` vs `cylcgt` (different code path) | 9,000 / 9,000 rows (all val, test and test_heldout, plus 3,000 train) |
| B′ | the same under race rules "mover" and "opponent" | same | 2,000 / 2,000 |
| C | outcome class of whole instances, with real-chess e.p. and the first passer ending the game | `cylcgt` vs Codex minimax | 4,607 / 4,607 (all 8-file rows of val, test and test_heldout; 600 + 200 train; wide samples) |
| C′ | full winning-move sets for both sides | same | 596 / 596 |
| D | outcome class of **every** instance | `cylcgt` vs `bench/ab.c` α-β + TT | 25,972 / 25,972 |

Not finished:
- **C:** 11 test rows with k = 5–6 hit the 10 s limit.
- **D:** 28 test rows with k = 5–6 hit the 3 CPU-second cap. The other 25,972 of the 26,000 rows are
  all confirmed.

Reading the table:
- Checks C and D are whole-board searches. Their agreement shows that, for these components, the
  disjunctive-sum model matches the "first passed pawn ends the game" rule.
- C uses e.p. that expires after one ply, so it also matches real-chess e.p. on the rows it covers.
- `bench/ab.c` and the CGT generator share the author (this session), but not code: `ab.c` has its own
  move generator and rules. Codex's minimax is fully independent.

## 8. Baseline: whole-board α-β that ignores the decomposition (`bench/baseline.py`, `bench/ab.c`)

The search plays the whole board:
- terminal rules as in §1, with the race rule "count";
- real-chess e.p. that expires after one ply.

Values are win/loss, so α-β with the window (−1, +1) stops at the first winning move.
- *plain*: no transposition table and no move ordering, as the task asked;
- *+TT*: adds a transposition table, which is fairer to search.

`ab.c` is a C port with the same move order. It reproduces the Python solver's results **and node counts
exactly** on 434 searches: 150 random positions and 80 benchmark rows, each side to move, keeping only
searches under 50,000 nodes (`tests/test_bench.py::test_c_solver_matches_python_exactly`).

The CGT columns time two things:
- `cgt.total` of the cached component values plus `cgt.outcome`;
- `pawns.value` of the whole board in a fresh interpreter with empty caches, which includes computing
  every component's value.

All times are **CPU** seconds. The machine was shared with other heavy jobs (load average about 130 on
14 cores), so the times are inflated and noisy. **Node counts are deterministic** and are the main measure.

Engine: c (bench/ab.c); cap per search: 30,000,000 nodes / 60 s (CPU). Each instance is searched twice (White first, Black first); medians are over all searches, with unsolved searches counted as infinite. Times are CPU seconds.

#### Nested chains (instance k+1 = instance k plus one more component)

| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | CGT from scratch, median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 8 | 4 | 16/16 | 3 | 3e-06 | 16/16 | 3 | 5e-06 | 3e-05 | 0.0061 |
| 2 | 8 | 7.5 | 16/16 | 10 | 7e-06 | 16/16 | 10 | 1.1e-05 | 6e-05 | 0.013 |
| 3 | 8 | 11 | 16/16 | 40 | 1.5e-05 | 16/16 | 32 | 2e-05 | 0.0001 | 0.015 |
| 4 | 8 | 15 | 16/16 | 386 | 0.0001 | 16/16 | 230 | 0.0001 | 0.0002 | 0.023 |
| 5 | 8 | 19 | 16/16 | 5,317 | 0.0014 | 16/16 | 1,235 | 0.00046 | 0.0003 | 0.052 |
| 6 | 8 | 23 | 15/16 | 182,011 | 0.032 | 16/16 | 11,770 | 0.0048 | 0.0002 | 0.063 |
| 7 | 8 | 26.5 | 12/16 | 2,330,852 | 0.5 | 16/16 | 55,772 | 0.02 | 0.0003 | 0.064 |
| 8 | 8 | 30 | 6/16 | > cap | > cap | 14/16 | 256,457 | 0.086 | 0.0004 | 0.073 |

Growth per added component (chains): median over chains and sides of nodes(k) / nodes(k-1), where both searches finished.

| k | plain α-β | α-β+TT |
|---|---|---|
| 2 | 5.1 (n=16) | 4.8 (n=16) |
| 3 | 3.6 (n=16) | 3.5 (n=16) |
| 4 | 8.3 (n=16) | 6.5 (n=16) |
| 5 | 5.3 (n=16) | 3.4 (n=16) |
| 6 | 18.0 (n=15) | 8.9 (n=16) |
| 7 | 2.9 (n=12) | 3.4 (n=16) |
| 8 | 31.8 (n=6) | 10.0 (n=14) |

#### Benchmark rows (k <= 3 from val, k >= 4 from test)

| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | CGT from scratch, median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 12 | 4 | 24/24 | 3 | 4e-06 | 24/24 | 3 | 5e-06 | 2e-05 | 0.0055 |
| 2 | 12 | 8 | 24/24 | 16 | 8e-06 | 24/24 | 16 | 1.4e-05 | 6e-05 | 0.0079 |
| 3 | 12 | 11 | 24/24 | 188 | 4.8e-05 | 24/24 | 100 | 4.8e-05 | 0.0002 | 0.026 |
| 4 | 12 | 14.5 | 22/24 | 249 | 8.1e-05 | 24/24 | 141 | 5.3e-05 | 0.0003 | 0.011 |
| 5 | 12 | 19 | 23/24 | 27,563 | 0.0085 | 24/24 | 3,565 | 0.0016 | 0.0008 | 0.06 |
| 6 | 12 | 23 | 18/24 | 1,826,316 | 0.69 | 22/24 | 39,468 | 0.013 | 0.002 | 0.074 |

Outcome agreement between the searches and CGT wherever both searches of an instance finished: 254/254.

**Reading the tables** (median-based fits, so rough):

| method | growth per added component | median nodes |
|---|---|---|
| plain α-β | about ×16 (k = 3 → 7) | 40 → 2.3 million; at k = 8, 10 of 16 searches hit the 30-million-node cap |
| α-β + TT | about ×6 (k = 3 → 8) | 32 → 256,000 |

- The step-to-step factor is irregular, between ×2.9 and ×32. It depends on the component added.
- Ratios exist only where both searches finished. That biases them low at large k, because the hardest
  chains drop out: plain α-β at k = 7 uses 12 of 16 searches.
- Every search was run. No search was skipped on the assumption that a larger instance is harder.
- The CGT route stays flat:
  - summing cached component values and comparing with 0 takes 0.002 s or less at every k (median);
  - computing the whole position from scratch in a fresh interpreter takes 0.005–0.08 s median and at
    most 0.26 s.
- The C solver runs about 4.6 million nodes per CPU-second here.
- On the benchmark's own test rows (k = 4–6), plain α-β fails to finish within 30 million nodes on 6 of
  24 searches at k = 6.

An earlier pilot with the Python solver showed the same pattern at about 10⁵ nodes per second. It used an older,
unsorted move order and skipped searches once a chain hit its cap (`results/baseline_scaling_python_pilot.md`,
`logs/baseline_scaling_python_pilot.log`).

## 9. Caveats and open issues

- **Convention, not chess.** The truth is exact for the pawn game with "passed pawn = win".
  - In real chess with kings, a passed pawn can be caught, kings provide tempo moves, and zugzwang structure
    differs.
  - Embedding ChessSums positions into legal 8×8 chess positions (for example with a locked king group,
    as in RESEARCH_PLAN C1) is future work. The race-rule dependence of the 4-file \*2 shows why every such
    embedding must be engine-certified.
- **One CGT implementation.** All values (component and sum) come from `cylcgt.cgt`/`pawns`. That
  engine is unit-tested, and its single-component outcomes match Codex's minimax 1070/1070 (RESEARCH_PLAN
  §1.1).
  - Here the independent checks confirm outcome classes and value *equalities* (check A2: c + r = 0 with r
    from a different orbit).
  - They do not confirm the absolute canonical forms, such as "this class is ↑ rather than some other
    infinitesimal".
  - The canonical forms of sums are computed once, by `cgt.add`.
- **Race-rule and e.p. robustness come from filtering**, not from modelling races properly. 57% of all
  candidates (3,016 of 5,290) are race-dependent and are simply excluded. So the benchmark under-represents positions
  where promotion races matter.
- **The value-string task can be long.** Test values have median length 10 characters, 90th percentile
  62, maximum 400.
- **Distribution choices are ours.** These are sqrt-of-class-size sampling, outcome balancing, the
  hold-out sizes and k ∈ {1,2,3} for `test_heldout`. Change them in `generate.py` (`SPLITS`) or in
  `components.py` (`HOLDOUT_*`).
- No model or engine has been evaluated. The Stockfish, Lc0 and LLM runs of C1/C2 are next.

## 10. Reproduce

All commands run from the project root. `PYTHONDONTWRITEBYTECODE=1` keeps `.pyc` files out of the
read-only packages.

Print the component library summary (about 80 s):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.components
```

Generate the dataset, which writes `bench/data/*` (about 6 min):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.generate --seed 20261015
```

Build the C baseline:

```bash
cc -O2 -o bench/ab bench/ab.c
```

Run the tests:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider bench/tests
```

Run the verification, which writes `bench/results/verify_report.md`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.verify
```

Run the scaling experiment, which writes `bench/results/baseline_scaling_c.md`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.baseline --engine c --chains 8 --kmax 8 --per-k 12 --node-cap 30000000 --time-cap 60 --seed 1
```

Score the chance baselines:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.score --gold bench/data/test.jsonl --baseline random-legal --seed 0
```

Print prompts:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.prompts --split test --task value --limit 2
```

## Files

| file | role |
|---|---|
| `components.py` | enumerate, certify, hold out |
| `generate.py` | instances, splits, manifest |
| `cgtfmt.py` | deterministic value printing; safe parser |
| `board.py` | move generator with names, diagram, FEN-style placement, move parsing |
| `prompts.py` | LLM prompts, answer extraction |
| `score.py` | scorer |
| `reward.py` | GRPO reward draft |
| `baseline.py` | Python α-β solver and the scaling harness |
| `ab.c` | C port of the solver |
| `verify.py` | cross-checks |
| `tests/test_bench.py` | 23 tests |
| `data/` | dataset and manifest |
| `results/` | verification and scaling outputs |
| `logs/` | run logs |
