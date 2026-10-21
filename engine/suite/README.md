# A CGT-dictated king-and-pawn suite, checked against the 7-man tablebase

Every position is a legal standard-chess 8×8 position with ≤ 7 men, made of two parts:

- **A trebuchet** (4 men) that, in the model, freezes both kings. Two layouts, each at any rank `r = 2…6`:
  - `A_r`: W Pg*r*, B Pg*(r+1)*, WK f*(r+1)*, BK h*r*. `A4` is the standard
    `8/…/5Kp1/6Pk/…` freeze with WK f5 and BK h4. The White king stands next to the e-file.
  - `B_r`: the same pawns, with WK h*(r+1)* and BK f*r*. Here the Black king is the one next to the e-file.
- **One queenside component** of 2–3 pawns on files a–d, with the e-file empty and no passed pawn at the start.
  `cylcgt` values it on the 4-file flat 8-rank board, en passant on.

**The model's prediction for every legal move:**
- a pawn move wins iff the CGT value of the resulting component is ≥ 0 (White moved) or ≤ 0 (Black moved);
- **every king move loses**, because it drops that side's g-pawn.

Each position was sent to the Lichess tablebase once. One response gives the result of the root **and of every
legal move**, so each position checks the model on all of its moves at once.

## Files

| File | Contents |
|---|---|
| `cgt_verified.epd` | **181 positions** whose tablebase-winning set equals the CGT(`count`) predicted winning set. 177 have White to move, 4 Black. `bm` = those moves. **This is the suite.** |
| `cgt_disagree.epd` | **52 positions** where the tablebase differs from CGT(`count`). `bm` = the tablebase-winning moves (35 positions), or the drawing moves when the root is a tablebase draw (17). **The interesting ones.** |
| `results.json` | Per position: FEN, component, CGT values under all three race rules, the tablebase category of every move, agreement flags, and features |
| `race_nodes.json` | Depth-1 promotion-race nodes with tablebase truth, from `race_nodes.py` |
| `candidates.json` | All 2,860 component / side-to-move records (2- and 3-pawn components on files a–d), with CGT predictions under `count`, `mover` and `opponent` |
| `selection.json`, `selection_ext.json` | The 204 + 71 probed positions, in two rounds |
| `tbcache/`, `tb_ledger.jsonl` | Raw Lichess responses, one JSON file per position, and a log of every HTTP attempt |

**EPD opcodes.**
- `bm` — solution moves in SAN.
- `id`
- `c0` — the component and its CGT value under each race rule.
- `c1` — the CGT(`count`) predicted winning moves and the tablebase root category.
- `c2` — the solution moves in UCI. `run_suite.py` uses this field.
- `c3` — the label, tier and trebuchet.
- `c4` — the tablebase result of every legal move, for the mover.
- `c5` — features: value class, number of solutions, maximum pawn-play length, and whether only a "slow" single
  push wins.

ASCII value notation: `^` = ↑, `v` = ↓, `^^*` = ⇑*, `+-` = ±. `+W` means a passed-pawn win (±BIG).

## Reproduce

Run everything from the project root, one command per block. Network is used only by `probe` and `probe_ext`, and
both are already cached. The other commands are offline.

Step 1. Enumerate the components and their CGT predictions (about 5 s):

```bash
PYTHONPATH=. .venv/bin/python engine/suite/gen_candidates.py
```

Step 2. Choose the 204 round-one positions:

```bash
PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py select
```

Step 3. Probe them (cached now):

```bash
PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py probe
```

Step 4. Build `results.json` and the two EPD files:

```bash
PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py report
```

Step 5. Choose the 71 round-two positions:

```bash
PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py select_ext
```

Step 6. Probe them (cached now):

```bash
PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py probe_ext
```

Step 7. Run the report again over both rounds:

```bash
PYTHONPATH=. .venv/bin/python engine/suite/build_suite.py report
```

Step 8. Print every number quoted below:

```bash
PYTHONPATH=. .venv/bin/python engine/suite/summarize.py
```

Step 9. Print the race-rule accuracy:

```bash
PYTHONPATH=. .venv/bin/python engine/suite/race_nodes.py
```

Step 10. Replay the tablebase lines quoted below (cached):

```bash
PYTHONPATH=. .venv/bin/python engine/suite/pv.py "8/8/3p4/8/3P2pK/5kP1/8/8 w - - 0 1" d4d5 5
```

```bash
PYTHONPATH=. .venv/bin/python engine/suite/pv.py "8/8/3p4/5Kp1/6Pk/2P5/8/8 w - - 0 1" f5e6 5
```

**Network accounting.**
- 287 HTTP requests to `tablebase.lichess.ovh`, under a cap of 300:
  - 275 positions;
  - 10 steps of the two lines above;
  - 2 answers of HTTP 429, after which the client backed off for 60 s.
- Requests went through `realchess/probe.py`'s `Prober`, used read-only, with its cache and ledger inside this
  directory.
- The shared `realchess/cache` was read but never written: it gave 0 hits. Request spacing was raised from 1.05 s
  to 5 s after the 429s, because another workstream was probing from the same machine.

## Results

The table is a stratified sample, *not* an exhaustive census. The tiers are:
- T1: 2 random components for each (value, #moves, #winning moves) group of tame White wins;
- X2: 2 more per group, each on a random trebuchet;
- T2: 1 per group of tame losses;
- T3: up to 8 for each pattern of race-rule disagreement;
- T5: 5 components on all 10 trebuchets;
- X1 / X3: the B4 trebuchet for selected T1 / T3 components.

"Tame" means the canonical form contains no ±BIG. "Race-sensitive" means the CGT winning set changes with
`RACE_RULE`.

| Group (positions) | Root outcome | Winning *pawn* moves | Full winning set | Every move's result exact | All king moves lose |
|---|---|---|---|---|---|
| Tame, race-insensitive, A-trebuchets (94) | 92/94 | **94/94** | 90/94 | 70/94 | 73/94 |
| Tame, race-insensitive, B-trebuchets (54) | 52/54 | 50/54 | 50/54 | 46/54 | 50/54 |
| BIG-valued, race-insensitive (40) | 39/40 | 40/40 | 35/40 | 27/40 | 28/40 |
| Race-sensitive, A4, `count` rule (72) | 60/72 | 60/72 | 46/72 | 26/72 | 32/72 |
| Race-sensitive, A4, `opponent` rule (72) | 57/72 | 44/72 | 28/72 | 19/72 | — |
| Race-sensitive, A4, `mover` rule (72) | 34/72 | 25/72 | 22/72 | 7/72 | — |
| Race-sensitive, B4, `count` / `opponent` / `mover` (15) | 12 / 11 / 8 | 14 / 6 / 8 | 14 / 6 / 8 | 9 / 5 / 3 | 11/15 |

**Tame, race-insensitive positions by value class** (CGT `count`; the three rules coincide here):

| Value class | Root | Pawn set | Full set |
|---|---|---|---|
| Infinitesimals (↑, ↓, ⇑*, …) | 29/29 | 29/29 | 29/29 |
| Switches (x ± y) | 39/40 | 40/40 | 40/40 |
| Other tame | 22/22 | 22/22 | 22/22 |
| Numbers | 45/47 | 44/47 | 40/47 |
| Nimbers (\*) | 9/10 | 9/10 | 9/10 |

**Depth-1 promotion races.** These are moves that create a position where both sides have a passed pawn, which is
where `cylcgt` applies `RACE_RULE`. There are 33 such nodes, and the tablebase result is known for each:

| Rule | Correct |
|---|---|
| `count` | **30/33** |
| `opponent` | 22/33 |
| `mover` | 9/33 |

The three `count` misses:
- two equal-length races that are tablebase **draws**;
- one race where the side with two passed pawns beats the side with one, even though the single pawn queens first.

This sample is small (A4 and B4 only, 3-pawn components). The *2 candidate's tree has about 398 race nodes,
mostly in 8-man positions, and this sample does not settle them. It does say that **`count` is the best of the three
simple rules, and none of them is exact.**

**The suite** (`cgt_verified.epd`, 181 positions):
- By value class: 37 numbers, 16 nimbers, 27 infinitesimals, 36 switches, 20 other tame, 44 hot ±BIG, 1 decided.
- 126 have a *unique* winning move.
- In 38, the only winning moves are single pushes even though a double step or a capture exists ("slow-move"
  positions, prediction P3 in `ENGINES.md`).
- The longest pawn-play line in a component is 1–6 plies.
- A uniformly random legal mover (`engine/mock_uci.py`) solves 40/181 (22%). That is the chance baseline.

## Why CGT and the tablebase disagree

The 52 disagreements fall into four kinds. The counts overlap.

1. **The kings are not really frozen. This is the most common kind.**
   - The model's only king assumption is "a king move loses".
   - In tame positions with the A-trebuchet, **41 of 449 king moves draw and 7 win.**
   - The White king on f5 is next to the e-file. It can give up g4 and still reach a c- or d-file target in time.
     Tablebase line for `8/8/3p4/5Kp1/6Pk/2P5/8/8 w` (component W c3 / B d6, value \*): Ke6! Kxg4 Kxd6 Kf3 c4 is a
     draw. The model says Ke6 loses. The pawn move c4 is the only win, and the model gets that right.
   - With the White king on h5 (B-trebuchets) these escapes mostly vanish for White: 115 losses and 5 draws over
     all king moves. The Black king on f4 then has the same freedom (`T6`/`X1` rows).
2. **The zugzwanged king takes compensation.**
   - Example: `8/8/3p4/8/3P2pK/5kP1/8/8 w` (B3; component W d4 / B d6, value \*). CGT plays d5, reaching a
     zugzwang for Black.
   - The tablebase continues d5 Ke3! Kxg4 Ke4 Kh3, and rates every step a **draw**. Black gives up g4 and heads
     for the blocked d5 pawn. The line was followed for 5 plies only, so the capture on d5 itself is not shown.
   - The model treats component pawns as untouchable by kings.
3. **A passed pawn is probably not always a win.** A king next to the e-file can presumably catch a c- or d-file
   passer. This is my reading of cases such as `cgt052` (W c2 / B d5 d6, A4): CGT says White to move loses, but the
   tablebase says c3 draws. I did not trace that line.
4. **Races** (above). Of the 52 disagreements, 36 are race-sensitive (33 from T3, 3 from X3).

**Taxonomy** of the 52, counted against the CGT(`count`) prediction:

| Kind | Positions |
|---|---|
| Only extra tablebase-winning king moves | 22 |
| Root outcome differs, with or without other differences | 20 |
| A predicted winning pawn move does not win | 10 |
| Extra winning pawn moves | 7 |

## The e.p.-aware passed test (adopted 2026-10-16)

The suite was built with `cylcgt`'s textbook passed test, under which a pawn that double-steps past an enemy pawn
counts as passed before the e.p. capture. The project has since adopted the e.p.-aware test (`RESULTS.md`,
"Conventions").

`ep_aware_check.py` recomputes every prediction with sumtest's independent move generator and passer test
(`sumtest/sumsolver.py`, `ep_aware=True`), using canonical forms from `cylcgt.cgt`:
- **`count` rule: 0 of 275 predicted winning sets change.** So `cgt_verified.epd` and `cgt_disagree.epd` are
  unchanged under the adopted convention. A verifier's own minimax found the same
  (`verify/engines/C1-refute/indep_out_epaware.txt`), so this is checked two ways.
- **`opponent` rule:** 0 change.
- **`mover` rule:** 20 change. Agreement of the pawn-move set with the tablebase rises from 217/275 to 236/275.
  The two tests differ only on a pawn that has just double-stepped past an enemy pawn, at the root move or
  later in the line. Under `count` and `opponent` that difference never changes who wins a race here.

Run it from the project root (offline):

```bash
PYTHONPATH=. .venv/bin/python engine/suite/ep_aware_check.py
```

## Caveats

- **The CGT side** is a single implementation (`cylcgt`). It was cross-checked separately against `crosscheck/`
  on single components; see `RESEARCH_PLAN.md` §1.1. The move labels used here were asserted equal to
  `pawns.moves()`, and the legal-move sets equal to `realchess/movegen.py`, for every position.
- **The tablebase side** is Lichess (Syzygy WDL/DTZ), an independent ground truth. No position had a cursed-win
  or blessed-loss move, and none was unresolved, so the 50-move rule played no role.
- **The selection is stratified**, so the percentages describe this sample, not all 2,860 records.
- Colour-reversed and mirrored twins were *not* probed; only 4 Black-to-move sanity checks were. All 4 agreed at the
  root and on pawn moves.
- **Every position has ≤ 7 men.** An engine given Syzygy solves the suite at the root. Run it without tablebases.
