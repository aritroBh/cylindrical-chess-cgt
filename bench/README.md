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
> **Which passed-pawn test.** The ground truth is the same under the *textbook* test and under the
> *e.p.-aware* test adopted on 2026-10-16 (a pawn that can still be taken en passant is not passed). This
> is by construction (filter 5′, §2) and was re-checked by direct computation (§2.3, §7).
> This is library **version 2** (418 components). Version 1 (518 components, textbook test only) is in git
> commit 28d790f. 100 of its components are not in version 2, because the e.p.-aware test judges some
> position in their game trees differently; for 48 of them it changes the value.
>
> **How far the ground truth is checked.**
> - Every value comes from one implementation, `cylcgt`.
> - Outcome classes were re-derived by two searches that do not use `cylcgt`:
>   - Codex's `crosscheck/minimax.py` (textbook test): 4,887 rows, plus full winning-move sets on 600 rows;
>   - our `bench/ab.c` α-β: all 26,000 rows except 5 that hit its cap. It also certifies that the
>     e.p.-aware test would give the same searches (§7, check D′).
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
- En passant is part of the rules, but no ChessSums position can ever use it (§2, filters 5 and 5′).
- **Normal play:** a side with no legal move loses.
- **Elkies convention:** as soon as exactly one side has a passed pawn, that side wins. In the CGT model
  this is the number ±BIG, with BIG = 256.
- **Passed-pawn test.** Two versions exist in this project:
  - *textbook*: no enemy pawn stands ahead of the pawn on its own file or an adjacent file
    (`cylcgt` on the main checkout);
  - *e.p.-aware* (adopted): the same, except that a pawn that can still be taken en passant is not passed
    (`cylcgt.pawns.PASSED_RESPECTS_EP`, git branch `ep-aware-passed`).

  The generator computes with the textbook test. Every ChessSums component has the same game tree under
  both tests, so every value, outcome and winning move below holds under both (§2.3).
- A move that gives *both* sides a passed pawn starts a promotion race. `cylcgt` resolves races by
  `RACE_RULE`. Every ChessSums component is certified to give the same value, and the same move values,
  under all three race rules (§2).

Pawns change file only by capturing, so an empty file stays empty forever. Groups of pawns separated by
an empty file are therefore independent, and the position is their **disjunctive sum**.

On a cylinder, a group that straddles the a/h seam is one component; one example is files g, h, a, b in
`val-00214` below. A group that leaves at least one file empty plays exactly as it would on a flat strip,
and `components.py` asserts this for every component. A "ring" that fills every file cannot be a summand,
so ChessSums has none.

## 2. The component library (`bench/components.py`, `data/components.jsonl`)

**Candidates.**
- Widths w = 1–4, with every file occupied.
- 2–4 pawns, of both colours, on ranks 2–7.
- No passed pawn at the start.
- One pawn alone is always passed, so 1-pawn components do not exist.

That gives **5,290 candidates**. A component is **kept** only if it passes every filter below. The value
filters are checked under all six settings `RACE_RULE` ∈ {count, mover, opponent} × en passant {on, off}.

| filter | dropped |
|---|---:|
| value depends on the race rule | 2,898 |
| value depends on the race rule and on e.p. | 118 |
| value depends on e.p. only | 50 |
| value is ±BIG (a passed pawn already decides it) | 194 |
| (4) canonical form still contains a ±BIG threat somewhere (a hot "passer" game such as `{+W \| *}`) | 1,161 |
| (3) some move leads to a position whose value depends on the race rule or e.p. | 326 |
| (5) an e.p. capture becomes available somewhere in the game tree | 25 |
| (5′) a double step can create a passed pawn that the opponent could take e.p. | 100 |
| **kept** | **418** |

Filters 3 to 5′ go beyond the task statement, which asked for "no ±BIG", "value independent of the race
rule and e.p." and "the same value under both passed tests":
- **Filter 3 (moves).** Every one-move child value must also be independent of the race rule and e.p.
  Without this, the *set of winning moves* in a sum could still depend on the rule.
- **Filter 4 (BIG-free).** No ±BIG may survive anywhere in the canonical form. This keeps every sum
  `sum_safe` and removes the known "+BIG and −BIG cancel" failure of disjunctive sums (`crosscheck/REPORT_after_fix.md`).
- **Filter 5 (no e.p.).** No e.p. capture may ever arise. `cylcgt` models e.p. per component, but in a real
  sum the right expires after *any* move. With filter 5 the difference cannot arise.
- **Filter 5′ (passed-test independence; new in version 2).** Filter 5 does not look inside positions
  that the textbook test has already ended. Filter 5′ does: at no such position may the pawn that has just
  double-stepped be passed and capturable en passant.

### 2.1 Why filter 5′ makes the two passed tests agree

The e.p.-aware test differs from the textbook test only about a pawn that has just double-stepped and can
be taken en passant, and only if the textbook test calls that pawn passed. The race rule's promotion
distance skips the same pawns, so it changes only there too. A position the textbook test does not end
has no passed pawn at all, so only the game-ending positions need checking, and filter 5′ checks them.
After filters 5 and 5′, no reachable position is judged differently. So both tests build the same game
tree, and every component, and every child of it, has the same value under both. Since no e.p. capture
is ever playable, `cylcgt`'s per-component e.p. model is exact under both tests.

This is a sufficient condition. `bench/conventions.py` checks it, and its converse, by direct computation
with the e.p.-aware `cylcgt` (§2.3).

### 2.2 Sanity example

The KEY-FACT position `W a2 c2 / B b7 d7` (4 flat files) is dropped under either test, so **ChessSums
contains no \*2 component**:

| | count | mover | opponent |
|---|---|---|---|
| textbook, e.p. on | \*2 | \*2 | 0 |
| textbook, e.p. off | \*2 | \*2 | 0 |
| e.p.-aware, e.p. on | {2±1 \| −2±1} | {2±1 \| −2±1} | 0 |
| e.p.-aware, e.p. off | \*2 | \*2 | 0 |

(computed once, by `cylcgt`, in `results/conventions_report.md`).

### 2.3 What the e.p.-aware test changes (`bench/conventions.py`, `results/conventions_report.md`)

Run once, with the e.p.-aware `cylcgt` from the `ep-aware-passed` worktree; values computed once by
`cylcgt`, under both tests by flipping `PASSED_RESPECTS_EP`.

| quantity | value |
|---|---:|
| candidates whose root value differs between the two tests (count rule, e.p. on) | 330 of 5,290 |
| … (mover rule / opponent rule, e.p. on) | 988 / 302 |
| … (any rule, e.p. off) | 0 (no e.p. right is ever set) |
| library v1: filters 1–5 under the textbook test | 518 |
| library: filters 1–5 under the e.p.-aware test alone | 470, all inside v1 |
| v1 components whose root or some child value changes under the e.p.-aware test | 48 (28 at the root) |
| v1 components with equal values everywhere, but some position judged differently | 52 |
| **version 2 = v1 minus the 100 filter-5′ hits** | **418** |
| version-2 components with any root or child value differing in any of the 12 settings | **0** |

Checked in the same run:
- filter 5′ fires exactly on the v1 components whose game tree contains a position the two tests judge
  differently (100 = 48 + 52);
- version 2 is v1 minus those 100.

**The 48 v1 components whose values change.** All 20 v1 components of value ±1/2 or ±1/2\* are among
them. Under the e.p.-aware test they become ↑ / ↓, games with ±BIG inside, or `{*, 0 | {* | −1}}`-type
games. Examples (count rule, e.p. on):

| position (flat strip) | textbook | e.p.-aware |
|---|---|---|
| `W a2 c2 / B a3 b6` | 1/2 | ↑ |
| `W a2 c2 / B a3 b5` | 1 | \* |
| `W a2 c2 / B a4 b6` | 1/2\* | {\*, 0 \| {\* \| −1}} |
| `W a6 b3 / B a7 c7` | −1/2 | ↓ |
| `W a2 c3 / B b6 c4` | 1/2 | {0 \| {0 \| {−256, ±256 \| −256, {−256, ±256 \| −256}}}} |

All 48, with every child that changes, are listed in `results/conventions_report.md`. The other 52 keep
all their values; they also pass filters 1–5 under each test separately. They were dropped anyway, so
that the game *trees*, not just the values, agree (§9 discusses keeping them).

**Consequence for the benchmark.** Version 2 has **no component whose value is a non-integer number**.
The non-integer numbers of version 1 (±1/2, ±1/2\*) all depended on the textbook test. The `number`
value kind therefore no longer occurs in any split. Fractions remain only inside switches such as
3/2±1/2.

### 2.4 Value spectrum and checks

**Value spectrum** of the 418 kept components (37 distinct values):
- 0 ×144, \* ×108, ↑/↓ ×18 each, ±1 and ±2 integers ×14 each, ↑\*/↓\* ×6 each, ±3 ×4 each, ±4 ×3 each,
  ⇑\*/⇓\* ×3 each;
- switches ±1, 1±1, 3/2±1/2, 1/2±1/2, 3±1, 2±1, 5/2±1/2, and their negatives;
- a few hot games such as {5/2±1/2 | 1}, {{5/2±1/2 | 1} | 1} and {3±1 | 0}.

By width: 115 one-file, 159 two-file, 114 three-file and 30 four-file components. The full list is printed
by `python -m bench.components`.

**Symmetry checks** (asserted for every kept component):
- mirroring the files leaves the value unchanged;
- swapping colours (with the ranks flipped) negates it;
- embedding the strip in a wider flat board, or in a cylinder with one empty file, leaves it unchanged.

**Hold-outs.** Components are grouped into **144 orbits** under mirror × colour-swap.
- **Value class:** every orbit whose value is ↑\* or ↓\* (3 orbits, 12 components).
- **Structure:** a seeded random 10% of the remaining orbits (14 orbits, 39 components).
- Held-out components never appear in train, val or test, only in `test_heldout`.
- Their values are mostly ones that training components also have (0, \*, ↑, ±1, …). The exceptions are
  ↑\*/↓\* (the value-class hold-out) and, by chance of the 10% draw, ⇑\*/⇓\* and ±(2±1), whose only
  orbits fell into the structure hold-out. So "structure" mostly tests whether a model can value an
  unseen pawn shape.
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
| `train` | 20,000 | 1: 3,000 · 2: 7,000 · 3: 10,000 | 367 non-held-out | 16,324 | outcome-balanced per k |
| `val` | 2,000 | same shares | same | 1,626 | i.i.d. with train (positions disjoint) |
| `test` | 2,000 | 4, 5, 6: about 667 each | same | 364 | half of the k = 4 rows were drawn to fit 8 files |
| `test_heldout` | 2,000 | 1: 400 · 2: 800 · 3: 800 | ≥ 1 held-out per row | 1,642 | each slot is held-out with p = ½, at least one forced |

Each `{split}_8file.jsonl` holds exactly the rows of `{split}` whose board has 8 files. They are **not**
outcome-balanced on their own. The worst case is `test_8file`, with L 139, R 147, N 67, P 11.
- On a flat 8-file board at most four components fit; on an 8-file cylinder, at most four 1-file ones.
  So the 8-file test rows all have k = 4.
- The 400 k = 1 rows of `test_heldout` reuse the 51 held-out components in different placements.
- Board widths: train and val use 8–16 files, test 8–25, test_heldout 8–15.

Run time on this machine: 407 s for the whole dataset, about 190 s of it for the component library. The
machine was heavily shared (load average 60–180 on 14 cores).

**Determinism.** The generator is seeded (`--seed`, default 20261015). It never relies on object ids
or on string-hash order. The output is sorted where order is otherwise arbitrary. `data/manifest.json`
records the library version and the sha256 of every file. A second full run with the same seed, written
to a scratch directory, reproduced all ten files in `bench/data/` byte for byte (checked with `cmp`; that
run took 804 s on the loaded machine). A third run with the e.p.-aware `cylcgt` first on the path also
reproduced all ten files: the generator pins the textbook flag while it builds the library, and filter 5′
makes the result independent of it anyway. That run was

```bash
cd <ep-aware-passed checkout> && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<that checkout>:/Users/aritro/Downloads/Research/Chessendgames \
  /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python -m bench.generate --seed 20261015 --out <scratch dir>
```

(run from the checkout, because `python -m` puts the current directory first on `sys.path`).

### Record format (one JSON object per line)

```json
{"id": "val-00214", "split": "val", "k": 2,
 "board": {"files": 8, "ranks": 8, "cylinder": true},
 "position": "W: b4 d2 e3 h3 / B: a7 d3 d7 g5",
 "placement": "8/p2p4/8/6p1/1P6/3pP2P/3P4/8",
 "white": ["b4", "d2", "e3", "h3"], "black": ["a7", "d3", "d7", "g5"],
 "components": [{"comp_id": "C0154", "files": "de",   "position": "W: d2 e3 / B: d3 d7", "value": "↓"},
                {"comp_id": "C0414", "files": "ghab", "position": "W: b4 h3 / B: a7 g5", "value": "*"}],
 "value": "↓*", "value_ascii": "v*", "kind": "number+ups(+nimber)",
 "outcome": "N", "mean": "0", "temperature": "0",
 "legal_moves":   {"W": ["b4-b5", "e3-e4", "h3-h4"], "B": ["a7-a5", "a7-a6", "d7-d5", "d7-d6", "g5-g4"]},
 "winning_moves": {"W": ["e3-e4"], "B": ["a7-a6", "d7-d6"]},
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
| **value** | one per row | canonical value | the answer is **parsed** and compared as a game, so `1 + *`, `1*` and `{1 \| 1}` all count; exact-string match is reported too |

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

**Read these baselines before reading any score** (`score.py --baseline random-legal --seed 0`):

| split | random letter, outcome | constant "0", value | random legal move, move (expected) | on items with chance ≤ 1/4 |
|---|---:|---:|---:|---:|
| val | 0.24 | 0.25 | 0.65 | 0.22 (272 items) |
| test | 0.24 | 0.25 | 0.56 | 0.16 (551 items) |
| test_heldout | 0.24 | 0.25 | 0.59 | 0.22 (299 items) |

- **Outcome P ⇔ value 0.** On outcome-balanced splits the constant answer `0` therefore gets 25% on the
  value task. Read the `value!=0` row instead.
- **Many moves win.** The median share of legal moves that win is 0.5–0.6 depending on the split.
  `score.py` reports `random_legal_expected` for every group, and rows for `move: chance<=1/4` (551 test
  items) and `move: unique winning move` (554 test items). Those are the informative move numbers. In the
  N-positions of `test`, a random move wins 33% of the time.

### Text prompt for LLMs (`bench/prompts.py`)

```
$ PYTHONPATH=. .venv/bin/python -m bench.prompts --split val --task move --limit 1   # (this example is val-00214, White)
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
7 p . . p . . . .
6 . . . . . . . .
5 . . . . . . p .
4 . P . . . . . .
3 . . . p P . . P
2 . . . P . . . .
1 . . . . . . . .
  a b c d e f g h
White pawns: b4 d2 e3 h3
Black pawns: a7 d3 d7 g5

Question: White to move and win. Give one winning move as from-square and to-square, with '-' for a step
and 'x' for a capture, e.g. <answer>e2-e4</answer> or <answer>d4xe5</answer>.
```

(Lines are wrapped here; the real prompt has one line per rule. The example was rendered with
`bench.prompts.render(row, "move", "W")`; `--limit 1` prints the first item of the split instead.)

The passed-pawn rule in the prompt is the textbook one. That is exact here, because en passant never
arises, so the e.p.-aware exception never applies.

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

## 7. Verification (`bench/verify.py`, `bench/conventions.py`)

Full output is in `results/verify_report.md` and `results/verify_summary.json` (run time 1,273 s with 4
worker processes, on a machine with load average 120–180), and in `results/conventions_report.md` and
`results/conventions_summary.json` (1,304 s, 6 workers). **No disagreements.**

| check | what is compared | implementations | agree / total |
|---|---|---|---|
| A1 | outcome of every component alone, e.p. on and off | `cylcgt` vs Codex `crosscheck/minimax.py` | 836 / 836 |
| A2 | component c next to a component r of value −v(c): must be P, so v(c) = −v(r). For 406 of 418, r comes from a *different* orbit | same | 418 / 418 |
| A3 | outcome of random component pairs vs the CGT outcome of the summed values | same | 300 / 300 |
| B | value of the whole board (e.p. on and off) and the win/loss of every move, re-solved by `pawns.value` with its own decomposition | `cylcgt` vs `cylcgt` (different code path) | 9,000 / 9,000 rows (all val, test and test_heldout, plus 3,000 train) |
| B′ | the same under race rules "mover" and "opponent" | same | 2,000 / 2,000 |
| C | outcome class of whole instances, with real-chess e.p. and the first passer ending the game | `cylcgt` vs Codex minimax | 4,887 / 4,887 (all 8-file rows of val, test and test_heldout; 600 + 200 train; wide samples) |
| C′ | full winning-move sets for both sides | same | 600 / 600 |
| D | outcome class of **every** instance | `cylcgt` vs `bench/ab.c` α-β + TT | 25,995 / 25,995 |
| D′ | double steps met in the D searches that leave a passed pawn the opponent could take e.p. | `bench/ab.c` counter | **0** in every split (so the e.p.-aware test gives the same searches) |
| E1 | every component and every child, in all 12 settings (2 passed tests × 3 race rules × e.p. on/off) | `cylcgt`, textbook vs e.p.-aware flag | 418 / 418 identical |
| E2 | as B (count rule), but with the e.p.-aware test | `cylcgt` (e.p.-aware) vs stored truth | 9,000 / 9,000 rows (all val, test and test_heldout, plus a different sample of 3,000 train) |
| E3 | filter 5′ (written in `bench`, textbook test only) vs "some position is judged differently" (computed with the e.p.-aware `cylcgt`) on all 518 v1 components | two code paths | agree on 518 / 518 |

Not finished:
- **C:** 5 test rows with k = 6 hit the 10 s limit.
- **D:** 5 test rows with k = 6 hit the 3 CPU-second cap. The other 25,995 of the 26,000 rows are all
  confirmed.

Reading the table:
- Checks C and D are whole-board searches. Their agreement shows that, for these components, the
  disjunctive-sum model matches the "first passed pawn ends the game" rule.
- C uses e.p. that expires after one ply, so it also matches real-chess e.p. on the rows it covers.
- Codex's minimax uses the textbook passed test. `ab.c` uses it too, but its counter (D′) certifies, for
  each search, that the e.p.-aware test would have visited the same nodes and returned the same result. So
  D also confirms the outcomes under the e.p.-aware test, independently of `cylcgt`.
- The counter is a one-way certificate. As a positive control (`bench.conventions --positive-control`), it
  fires in plain α-β searches of 20 of the 100 components that filter 5′ removed (each searched alone,
  both sides to move), and never for the 418 kept ones; α-β pruning skips the relevant double step in the
  other 80.
- `bench/ab.c` and the CGT generator share the author (this session), but not code: `ab.c` has its own
  move generator and rules. Codex's minimax is fully independent.
- E1–E3 use a single CGT implementation with one flag flipped. Values under the e.p.-aware test are
  computed once.

## 8. Baseline: whole-board α-β that ignores the decomposition (`bench/baseline.py`, `bench/ab.c`)

The search plays the whole board:
- terminal rules as in §1, with the race rule "count" and the textbook passed test;
- real-chess e.p. that expires after one ply.

Every search below also reports the e.p. counter of check D′. It was 0 in all 544 searches, so the
e.p.-aware test would give the same node counts and results.

Values are win/loss, so α-β with the window (−1, +1) stops at the first winning move.
- *plain*: no transposition table and no move ordering, as the task asked;
- *+TT*: adds a transposition table, which is fairer to search.

`ab.c` is a C port with the same move order. It reproduces the Python solver's results, node counts **and
e.p. counters** exactly on 447 searches: 150 random positions and 80 benchmark rows, each side to move,
keeping only searches under 50,000 nodes (`tests/test_bench.py::test_c_solver_matches_python_exactly`;
run pytest with `-s` to see the counts). The counter is non-zero in 17 of them, all from the random
positions.

The CGT columns time two things:
- `cgt.total` of the cached component values plus `cgt.outcome`;
- `pawns.value` of the whole board in a fresh interpreter with empty caches, which includes computing
  every component's value.

All times are **CPU** seconds. The machine was shared with other heavy jobs (load average 120–180 on
14 cores), so the times are inflated and noisy. **Node counts are deterministic** and are the main measure:
two runs of this experiment on the version-2 data gave identical node counts.

Engine: c (bench/ab.c); cap per search: 30,000,000 nodes / 60 s (CPU). Each instance is searched twice (White first, Black first); medians are over all searches, with unsolved searches counted as infinite. Times are CPU seconds.

#### Nested chains (instance k+1 = instance k plus one more component)

| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | CGT from scratch, median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 8 | 4 | 16/16 | 2 | 4e-06 | 16/16 | 2 | 4e-06 | 3e-05 | 0.00013 |
| 2 | 8 | 8 | 16/16 | 6 | 5e-06 | 16/16 | 6 | 9e-06 | 0.0001 | 0.009 |
| 3 | 8 | 11 | 16/16 | 22 | 1e-05 | 16/16 | 22 | 3.4e-05 | 0.0002 | 0.011 |
| 4 | 8 | 15 | 16/16 | 429 | 0.00011 | 16/16 | 194 | 0.00015 | 0.0001 | 0.024 |
| 5 | 8 | 19 | 16/16 | 1,482 | 0.00037 | 16/16 | 543 | 0.00039 | 0.0002 | 0.026 |
| 6 | 8 | 22.5 | 15/16 | 48,792 | 0.012 | 16/16 | 4,434 | 0.0019 | 0.0003 | 0.042 |
| 7 | 8 | 26.5 | 13/16 | 149,440 | 0.034 | 16/16 | 8,442 | 0.005 | 0.0003 | 0.04 |
| 8 | 8 | 30 | 11/16 | 1,402,298 | 0.3 | 14/16 | 24,837 | 0.015 | 0.0004 | 0.052 |

Growth per added component (chains): median over chains and sides of nodes(k) / nodes(k-1), where both searches finished.

| k | plain α-β | α-β+TT |
|---|---|---|
| 2 | 3.2 (n=16) | 3.2 (n=16) |
| 3 | 2.9 (n=16) | 2.5 (n=16) |
| 4 | 23.3 (n=16) | 11.5 (n=16) |
| 5 | 5.5 (n=16) | 3.0 (n=16) |
| 6 | 8.8 (n=15) | 5.5 (n=16) |
| 7 | 1.7 (n=13) | 1.8 (n=16) |
| 8 | 1.8 (n=11) | 1.8 (n=14) |

Least-squares fit of ln(median nodes) against k, over k >= 3 where the median is finite (unsolved searches count as infinite in the median):

- plain α-β: about x8.9 nodes per added component (k = 3..8, 6 points)
- α-β+TT: about x4.0 nodes per added component (k = 3..8, 6 points)

#### Benchmark rows (k <= 3 from val, k >= 4 from test)

| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | CGT from scratch, median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 12 | 4 | 24/24 | 3 | 3e-06 | 24/24 | 3 | 1e-05 | 2e-05 | 0.0018 |
| 2 | 12 | 7.5 | 24/24 | 14 | 6e-06 | 24/24 | 14 | 1.5e-05 | 3e-05 | 0.012 |
| 3 | 12 | 11 | 24/24 | 93 | 1.9e-05 | 24/24 | 70 | 3.7e-05 | 0.0002 | 0.011 |
| 4 | 12 | 14 | 24/24 | 602 | 7.3e-05 | 24/24 | 199 | 8.8e-05 | 0.0003 | 0.0098 |
| 5 | 12 | 18 | 24/24 | 3,516 | 0.0022 | 24/24 | 835 | 0.00039 | 0.0003 | 0.025 |
| 6 | 12 | 22 | 19/24 | 247,822 | 0.05 | 24/24 | 16,633 | 0.0046 | 0.0002 | 0.04 |

Outcome agreement between the searches and CGT wherever both searches of an instance finished: 262/262.

Double steps that left a passed pawn the opponent could take en passant, over all 544 searches: 0 (0 means the e.p.-aware passed test would give identical searches).

**Reading the tables** (median-based, so rough):

| method | growth per added component (log-linear fit, k = 3–8) | median nodes, chains |
|---|---|---|
| plain α-β | about ×9 | 22 at k = 3 → 1.4 million at k = 8; at k = 8, 5 of 16 searches hit the 30-million-node cap |
| α-β + TT | about ×4 | 22 → 25,000; 2 of 16 searches hit the cap at k = 8 |
| CGT | none | summing cached values: median ≤ 0.0005 s, max 0.024 s; whole position from scratch: median ≤ 0.05 s, max 0.18 s |

- The step-to-step factor is irregular, between ×1.7 and ×23. It depends on the component added.
- Ratios exist only where both searches finished. That biases them low at large k, because the hardest
  chains drop out: plain α-β at k = 8 uses 11 of 16 searches. This may be part of why the k = 7 and
  k = 8 step factors are small (×1.7–1.8).
- Every search was run. No search was skipped on the assumption that a larger instance is harder.
- The C solver runs about 3.9 million nodes per CPU-second here (searches over 10⁶ nodes).
- On the benchmark's own test rows, plain α-β fails to finish within 30 million nodes on 5 of 24 searches
  at k = 6. The TT search finishes all of them.
- The growth is milder than in version 1 (plain about ×16 per component, k = 3 → 7, in git 28d790f).
  Version 2 has different components, so the two runs are not directly comparable.

An earlier pilot with the Python solver, on version-1 data, showed the same pattern at about 10⁵ nodes per
second. It used an older, unsorted move order and skipped searches once a chain hit its cap
(`results/baseline_scaling_python_pilot.md`, `logs/baseline_scaling_python_pilot.log`).

## 9. Caveats and open issues

- **Convention, not chess.** The truth is exact for the pawn game with "passed pawn = win".
  - In real chess with kings, a passed pawn can be caught, kings provide tempo moves, and zugzwang structure
    differs.
  - Embedding ChessSums positions into legal 8×8 chess positions (for example with a locked king group,
    as in RESEARCH_PLAN C1) is future work. The race-rule and passed-test dependence of the 4-file \*2
    (§2.2) shows why every such embedding must be engine-certified.
- **One CGT implementation.** All values (component and sum) come from `cylcgt.cgt`/`pawns`. That
  engine is unit-tested, and its single-component outcomes match Codex's minimax 1070/1070 (RESEARCH_PLAN
  §1.1).
  - Here the independent checks confirm outcome classes and value *equalities* (check A2: c + r = 0 with r
    from a different orbit).
  - They do not confirm the absolute canonical forms, such as "this class is ↑ rather than some other
    infinitesimal".
  - The canonical forms of sums are computed once, by `cgt.add`.
  - The e.p.-aware values come from the same `cylcgt` with one flag flipped, so §2.3 is a single
    implementation too. What is independent of `cylcgt` there is filter 5′ itself (written in `bench`) and
    the ab.c counter of check D.
- **Race-rule and passed-test robustness come from filtering**, not from modelling races properly. 57% of
  all candidates (3,016 of 5,290) are race-dependent and are simply excluded. So the benchmark
  under-represents positions where promotion races matter.
- **No non-integer numbers.** Under the e.p.-aware test, every v1 component of value ±1/2 or ±1/2\*
  changes value (§2.3), so version 2 has none. Fractions survive only inside switches. A benchmark that
  needs pure fractions must use larger components or other boards; the flat-8 atlas
  (`atlas/flat8/compare_ep_aware.out`) still has 1/8 and 1/16 under the e.p.-aware test.
- **Stricter than required.** The task requires the same *value* under both passed tests. 470 v1
  components meet that, with every child value equal too. Version 2 keeps only the 418 whose game trees
  are identical. The other 52 differ only in how some game-ending positions deep in the tree are scored,
  and no e.p. capture is ever playable in them under either test. Re-admitting them would add back ±3 and
  more hot games, but the check-D certificate would no longer cover rows that contain them.
- **The value-string task can be long.** Test values have median length 9 characters, 90th percentile
  66, maximum 424.
- **Distribution choices are ours.** These are sqrt-of-class-size sampling, outcome balancing, the
  hold-out sizes and k ∈ {1,2,3} for `test_heldout`. Change them in `generate.py` (`SPLITS`) or in
  `components.py` (`HOLDOUT_*`).
- No model or engine has been evaluated. The Stockfish, Lc0 and LLM runs of C1/C2 are next.

## 10. Reproduce

All commands run from the project root. `PYTHONDONTWRITEBYTECODE=1` keeps `.pyc` files out of the
read-only packages.

Print the component library summary (about 80 s on an idle machine):

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

Run the tests (25 tests):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider bench/tests
```

Run the verification, which writes `bench/results/verify_report.md` (about 25 min on the loaded machine):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.verify
```

Run the passed-test comparison, which writes `bench/results/conventions_report.md` (about 22 min on the
loaded machine). It needs a checkout of branch `ep-aware-passed`; this one is the worktree named in the
2026-10-16 run notes:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.conventions --cylcgt-root /private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt
```

Run the scaling experiment, which writes `bench/results/baseline_scaling_c.md`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.baseline --engine c --chains 8 --kmax 8 --per-k 12 --node-cap 30000000 --time-cap 60 --seed 1
```

Print the descriptive statistics quoted in §2–§4 (value spectrum, 8-file outcome mix, value-string
lengths, winning-move shares):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.stats
```

Run the positive control for the ab.c e.p. counter (§7), which writes
`bench/results/conventions_positive_control.json` (about 4 min):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.conventions --positive-control
```

Score the chance baselines (repeat with `val.jsonl` and `test_heldout.jsonl`):

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
| `components.py` | enumerate, certify (filters 1–5′), hold out |
| `generate.py` | instances, splits, manifest |
| `conventions.py` | textbook vs e.p.-aware passed test, by direct computation; ab.c counter positive control |
| `stats.py` | descriptive statistics of the data |
| `cgtfmt.py` | deterministic value printing; safe parser |
| `board.py` | move generator with names, diagram, FEN-style placement, move parsing |
| `prompts.py` | LLM prompts, answer extraction |
| `score.py` | scorer |
| `reward.py` | GRPO reward draft |
| `baseline.py` | Python α-β solver and the scaling harness |
| `ab.c` | C port of the solver, with the e.p. certificate counter |
| `verify.py` | cross-checks |
| `tests/test_bench.py` | 25 tests |
| `data/` | dataset (version 2) and manifest |
| `results/` | verification, passed-test comparison and scaling outputs |
| `logs/` | run logs. `*_v2.log`: version 2. `*_v2_counter_overbroad.log`: first version-2 runs of verify and
  baseline, with an earlier e.p. counter that also counted harmless double steps (no disagreements; identical
  node counts). The rest: version 1 |
