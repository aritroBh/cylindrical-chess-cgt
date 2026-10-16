# A8 test data: frozen kings against real chess

Extracted on 2026-10-16, offline, from `realchess/` and `engine/suite/`. No network requests and no new
tablebase probes. Every real-chess number comes from the existing result files or the existing cached Lichess
records.

| File | Contents |
|---|---|
| `star2_tree.json` | The \*2 candidate's game tree. Contains every terminal that realchess attempted, the node-level and root comparisons, the certificates, the consistency check, and a `failures` list with diagnoses |
| `suite_king_moves.json` | All 275 engine-suite positions. For each: every king move, its real result, and the convention's prediction (always "loss") |
| `scripts/extract_star2.py`, `scripts/extract_suite.py` | The extraction scripts. They read only and write only to this folder. Run with `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/data/scripts/<name>.py` |

**Conventions.**
- Results are from **White's** point of view, as `[White moves first, Black moves first]`.
- Classes:
  - **L**: White wins either way.
  - **R**: Black wins either way.
  - **N**: the side to move wins.
  - **P**: the side to move loses.
  - **D**: a draw for at least one side to move.
- The convention is cylcgt with `RACE_RULE = count`, unless a rule is named.
- A *terminal* is the first position with a passed pawn. It uses the textbook passed test (e.p. ignored), which is
  what these runs used.
- `frozen_king_wrong` means the real result differs from the convention. It flags **every** convention failure,
  whatever the cause. The `diagnosis` fields and the tables below sort out which failures are really about kings.
- **Data** marks what the files record. **Inference** marks my reading of it.

---

## 1. The \*2 candidate (`star2_tree.json`)

The candidate is W a2 c2 / B b7 d7 plus the trébuchet: WK f5, Pg4 / BK h4, Pg5.

### Sources (data)

| Source | Written | What it adds |
|---|---|---|
| `comp_Wa2c2_Bb7d7_oracle_pure.json` (run 3) | 00:29 | 84 terminals resolved for both sides, 9 for one side. RESULTS.md §1 quotes the run-2 snapshot (65 resolved, 59 agreeing) |
| `comp_Wa2c2_Bb7d7_oracleall_pure_textbook_offline.json` | **01:32** | Every one of the 670 terminals, resolved offline from the tablebase cache. 115 resolved both ways, 350 one way, 205 not at all |
| `nodes_pure`, `roots_pure` (`model_nodes`), `nodes_pure_offline`, `nodes_pure_offline_ext6` | 00:09 – 01:30 | Real results for internal nodes |
| `comp_Wa2c2_Bb7d7_kings_pure_offline.json`, `comp_Wa2c2_Bb7d7_kings_pure_root.json` | **01:29**, **01:32** | realchess's `kings` stage: every king move at every internal node, and at the root |

**Data.**
- The files marked in bold were written by another workstream *while this extraction ran*. Their timestamps and
  hashes are in `_about.input_files`.
- No two sources ever contradict each other on a result, and the run-1, run-2 and run-3 snapshots agree.

### Terminals (data)

**Merged sources.**
- 670 terminals in total: 115 resolved both ways, 350 resolved one way, 205 unresolved.
- Agreement on the 115 fully resolved, by RACE_RULE: `count` **85/115**, `mover` 84/115, `opponent` 73/115.
- Convention class → real class, under `count`:

| | → L | → R | → N | → D |
|---|---|---|---|---|
| convention L | 47 | – | 9 | – |
| convention R | 4 | 38 | 14 | 3 |

**Run 3 alone.** 84 resolved, `count` 74/84, `mover` 73/84, `opponent` 63/84.

**Failures.**
- **114 terminals** have at least one resolved side-to-move result that contradicts the convention. 14 of them are
  in run 3. In 108 of the 114, the wrong result is on the side that moves after the move into the terminal.

**Roots.**
- Real chess gives N, as the convention predicts under `count` and `mover`.
- `cert_root_w`: White to move wins with c4. `cert_root_b`: Black to move wins with b5.
- `roots_pure` left the root king moves unresolved. The later `kings_pure_root` audit (01:32) finds that all 6 lose,
  as the convention says.

### Terminal failures by cause

The 14 run-3 failures were checked by hand. The other 100 were sorted by a fixed rule: the docstring of
`auto_category`, copied into `_about.conventions.rule_based_diagnosis`. The rule reads the best moves from the
position's own cached record when one exists. Otherwise it looks at what the position allows: whether it is a race,
an e.p. right, an available capture. **Every category is an inference.**

| Cause (inference) | Terminals | Typical data |
|---|---|---|
| Counter-passer: the side the convention scores as lost replies with a capture that makes a faster passer | 31 with a record + 50 probable (no record, but a capture exists) | e.g. W a4 d3 / B b5: model L, but Black to move wins. In recorded cases the best moves are captures such as cxb7 |
| En passant: the pawn counted as passed can be taken e.p. | 8 with a record + 8 probable, plus 1 mixed with counter-passer | the only winning reply is the e.p. capture (bxa3, cxd6, dxc3) |
| Counter-passer plus e.p. (hand-checked) | 1 | W a4 c5 / B b6 d5 (ep d6): see the table below |
| Race (both sides passed; no RACE_RULE is exact) | 7 | W a2 / B c5 d7 and similar: N, while `count` says R |
| **King leaves the trébuchet** | 1 shown + 1 probable | W a5 / B b7 c5, and W c4 / B a6 d6 |
| Unclear: no record and no capture, so a king move or a pawn push | 5, plus 1 hand-checked | W a4 / B b7 c6, W a5 / B b7 c6, W c5 / B a6 d7 (all three: White to move **draws** where the model says Black's passer wins); W a4 c4 / B b6 d4 and W a5 c5 / B b7 d5 (White to move wins) |

**Inference.** The three "unclear" draws have the shape of W a5 / B b7 c5: a lone Black passer on the a- or c-file,
the White king on f5 and White to move. They are the best candidates for further frozen-king failures, but no record
shows the drawing move.

**The 14 run-3 failures** (hand-checked). "Next" is the side that moves after the move into the terminal; ✓ means
the wrong result is on that side.

| Terminal (board part of the FEN; full FENs in `failures`) | Entered by / next | Conv. | Real [W-first, B-first] | Data (cached Lichess records, certificates) | Diagnosis (**inference**) |
|---|---|---|---|---|---|
| W a2 / B c5 d7 `8/3p4/8/2p2Kp1/6Pk/8/P7/8` | B / W ✓ | R | [win, loss] = N | B-first: c4, d5 win; Kg3 draws. W-first: from a parent record, no moves | **Race**: no rule is exact. `count`/`mover` say R, `opponent` says L |
| W a3 / B c5 d6 `8/8/3p4/2p2Kp1/6Pk/P7/8/8` | B / W ✓ | R | N | B-first: c4, d5 win | **Race**, same pattern |
| W a3 / B c5 d7 `8/3p4/8/2p2Kp1/6Pk/P7/8/8` | B / W ✓ | R | N | W-first: **a4** is the only win; Ke4 and Ke5 only draw. B-first: c4, d5 win | **Race**. White wins with the pawn, not the king |
| **W a5 / B b7 c5** `8/1p6/8/P1p2Kp1/6Pk/8/8/8` | B / W ✓ | R | [**draw**, loss] | W-first: the **only non-losing moves are Ke4 and Ke5**; a6, Ke6, Kf6 and Kg6 lose | **Frozen king.** The WK gives up g4 and catches the c-pawn |
| **W c4 / B a6 d6** `8/8/p2p4/5Kp1/2P3Pk/8/8/8` | B / W ✓ | R | [**draw**, loss] | W-first: from a parent record, so the drawing move is not recorded. B-first: a5 wins | **Probably a frozen king** (not shown). The WK f5 stands inside the square of the a6 pawn |
| W a4 c2 / B b4 d5 (ep a3) | W / B ✓ | L | N | B-first: **bxa3 e.p.** is the only win | **En passant** |
| W a4 c2 / B b4 d6 (ep a3) | W / B ✓ | L | N | B-first: bxa3 e.p. is the only win | **En passant** |
| W a4 c3 / B b4 d5 (ep a3) | W / B ✓ | L | N | B-first: bxa3 e.p. or bxc3 wins (`cert_T1_bfirst`: bxa3). W-first: cxb4 wins | **En passant** |
| W a4 c4 / B b6 d4 (ep c3) | W / B — | R | N | B-first: dxc3 e.p. wins (the convention is right here). W-first (an 8-man search, no moves recorded): White wins | **Unclear.** The wrong side arises only if Black passes |
| W a4 c5 / B b6 d5 (ep d6) `8/8/1p6/2Pp1Kp1/P5Pk/8/8/8 w - d6` | B / W ✓ | R | [win, **win**] = L | W-first: cxb6 or cxd6 e.p. wins. B-first: **every** move loses, including d4, Kg3 and Kh3 (`cert_T2_*`) | **Counter-passer after the terminal, plus e.p.**: cxb6 gives White a faster passer. Not about kings |
| W a2 c5 / B b7 d5 (ep d6) | B / W ✓ | R | [win, ?] | W-first: cxd6 e.p. is the only win | **En passant** |
| W a3 c5 / B b7 d5 (ep d6) | B / W ✓ | R | [win, ?] | W-first: cxd6 e.p. is the only win | **En passant** |
| W a4 c5 / B b7 d5 (ep d6) | B / W ✓ | R | [win, ?] | W-first: cxd6 e.p. is the only win | **En passant** |
| W a4 c2 / B b4 d7 (ep a3) | W / B ✓ | L | [?, loss] | B-first: bxa3 e.p. is the only win | **En passant** |

The e.p. cases are no longer terminals under the adopted e.p.-aware passed test (inference).

**King moves in the terminals' own records** (data).
- Where the convention says the side to move loses: 243 king moves. 150 lose, 89 are unknown, and only 4 draw.
- The 4 draws: Ke4 and Ke5 in W a3 / B c5 d7, where a4 wins anyway, and Ke4 and Ke5 in W a5 / B b7 c5.

### King-move audit at internal nodes (data, `kings_pure_offline`)

- 1431 king moves at 462 node positions: 117 lose, **6 draw**, and 1308 are unresolved (search budget ext 2).
- In 5 of the 6 draws, the convention says the side to move loses. These are **direct frozen-king failures**:

| Node (White to move) | FEN | Convention | Drawing king move | Real node result |
|---|---|---|---|---|
| W a2 c5 / B b4 d7 | `8/3p4/8/2P2Kp1/1p4Pk/8/P7/8 w` | loss | Kg6 | draw. Every pawn move is known to lose, so the king move is the best move |
| W a3 c5 / B b5 d7 | `8/3p4/8/1pP2Kp1/6Pk/P7/8/8 w` (no e.p. right) | loss | Kg6 | not resolved, but at least a draw |
| W a5 c3 / B b7 d5 | `8/1p6/8/P2p1Kp1/6Pk/2P5/8/8 w` | loss | Ke5, Ke6 | draw. Both pawn moves (c4, a6) are known losses |
| W a5 c4 / B b7 d6 | `8/1p6/3p4/P4Kp1/2P3Pk/8/8/8 w` | loss | Kf6 | draw. The pawn moves c5 and a6 also draw |

- The sixth draw is W a3 c5 / B b5 d7 *with* the e.p. right b6. There White already wins by cxb6 e.p., as the
  convention says.

### Node failures (data, with derived breakdowns)

**Counts.**
- 453 node positions, one per FEN, from the four node tables. 297 are resolved.
- **32 contradict the convention.** That is 34 as recorded: realchess keys a node by its component *without* the
  e.p. right, so I re-derived the convention with the e.p. right where the FEN carries one, which clears 2.
- The recorded tables report: `nodes_pure` 53/84 agreement; `nodes_pure_offline_ext6` 90 (`count`), 89 (`mover`),
  85 (`opponent`).

**Traces.**
- Each failure is traced one level at a time: each pawn move's convention value against that child's real result,
  recursively. The cause is then read off the terminal that is reached.
- **King-related:**
  - the 4 audit nodes above;
  - W a5 c5 / B b7 d6, Black to move: dxc5 leads to W a5 / B b7 c5;
  - W a6 c4 / B b7 d6, Black to move: bxa6 leads to W c4 / B a6 d6.
- **Everything else** traces to counter-passer, e.p. or unresolved terminals. 24 node failures have their own cached
  record. In every one of them **every king move loses** (or is unknown), and none shows a king move as the best
  move.
  - Example: W a2 c2 / B b3 d3. The convention says White to move wins; in reality every White move loses, and Black
    to move wins by bxa2, bxc2 or dxc2.

**Consistency check** (`comp_*_consistency.json`, computed before run 3). 228 node positions were compared with the
CGT value rebuilt from the real terminal classes. 15 disagree, and in every one CGT says the side to move wins while
real chess says it loses.

---

## 2. Engine-suite king moves (`suite_king_moves.json`)

### Counts (data)

The convention says every king move loses. Results are from the mover's point of view.

| Group | Positions | King moves | Lose | Draw | Win | Positions with a non-losing king move | King move beats every pawn move |
|---|---|---|---|---|---|---|---|
| Tame, race-insensitive, A-trébuchets (README headline) | 94 | **449** | 401 | **41** | **7** | 21 | 1 |
| Tame, race-insensitive, B-trébuchets | 54 | 120 | 115 | 5 | 0 | 4 | 0 |
| BIG-valued, race-insensitive | 40 | 164 | 115 | 24 | 25 | 12 | 0 |
| Race-sensitive, A-trébuchets | 72 | 350 | 206 | 80 | 64 | 40 | 2 |
| Race-sensitive, B-trébuchets | 15 | 30 | 24 | 6 | 0 | 4 | 2 |
| **All** | 275 | 1113 | 861 | 156 | 96 | 81 | **5** |

The 94 / 449 / 41 / 7 headline is reproduced exactly. No king move gives immediate stalemate: every record's
`stalemate` flag is false.

### Positions where the frozen-king assumption gives the wrong outcome (data)

In these 5 positions a king move is strictly better than every pawn move. Every one has White to move.

| id | FEN | Component, value | Real root | Convention | Non-losing moves |
|---|---|---|---|---|---|
| cgt055 | `8/2p5/2p5/2P2Kp1/6Pk/8/8/8 w` (A4) | W c5 / B c6 c7, 0 | **draw** | loss (no pawn move) | **Ke6** draws, the only non-losing move |
| cgt120 | `8/8/8/3p1Kp1/3P2Pk/2P5/8/8 w` (A4) | W c3 d4 / B d5, 0 | **win** | loss | **Ke5, Ke6 win**; Kf6, Kg6, c4 draw |
| cgt123 | `8/8/8/2p2Kp1/2P3Pk/1P6/8/8 w` (A4) | W b3 c4 / B c5, 0 | **draw** | loss | all five king moves draw; b4 loses |
| cgt262 | `8/8/8/2p3pK/2P2kP1/3P4/8/8 w` (B4) | W c4 d3 / B c5, 0 | **draw** | loss | **Kg6** draws; d4 loses |
| cgt270 | `8/8/8/3p2pK/3P1kP1/2P5/8/8 w` (B4) | W c3 d4 / B d5, 0 | **draw** | loss | **Kg6** draws; c4 loses |

All 5 have CGT value 0, so the side to move loses in the convention.

**Inference.**
- In cgt120 the king walks to the blockaded d5 pawn.
- In cgt055 and cgt123 the king trades g4 for the queenside pawns.
- The B4 cases show that the White king on h5 can also escape by Kg6. The mechanism is not recorded.

### Headline group: non-losing king moves where the outcome is unchanged (data)

All 21 positions have White to move: 17 on A4, 2 on A5, 2 on A6, and **none on A2 or A3**. In 20 of the 21 a pawn
move already wins, so only the predicted *set* of winning moves is wrong. The exception is cgt055 above.

| id | FEN (White to move) | Component | Value | King moves that draw | King moves that win |
|---|---|---|---|---|---|
| cgt002 | `8/8/3p4/5Kp1/6Pk/2P5/8/8` | W c3 / B d6 | \* | Ke6 | – |
| cgt007 | `8/8/2p5/5Kp1/1P4Pk/1P6/8/8` | W b3 b4 / B c6 | 1 | Ke5, Ke6 | – |
| cgt008 | `8/3p4/3P4/5Kp1/3P2Pk/8/8/8` | W d4 d6 / B d7 | 1 | Ke5, Kg6 | **Kf6** |
| cgt010 | `8/3p4/8/3P1Kp1/3P2Pk/8/8/8` | W d4 d5 / B d7 | ½±½ | Ke5, Kf6 | – |
| cgt011 | `8/3p4/3P4/5Kp1/6Pk/3P4/8/8` | W d3 d6 / B d7 | 2 | Ke5, Kg6 | **Kf6** |
| cgt013 | `8/1p6/8/2P2Kp1/6Pk/2P5/8/8` | W c3 c5 / B b7 | 2 | Ke5, Ke6 | – |
| cgt014 | `8/1p6/8/P4Kp1/6Pk/P7/8/8` | W a3 a5 / B b7 | 2 | Ke5, Ke6 | – |
| cgt015 | `8/8/2p5/5Kp1/1P4Pk/8/1P6/8` | W b2 b4 / B c6 | 2 | Ke5, Ke6 | – |
| cgt016 | `8/8/2p5/5Kp1/3P2Pk/8/3P4/8` | W d2 d4 / B c6 | 2 | Ke5, Ke6 | – |
| cgt017 | `8/1p6/1P6/5Kp1/6Pk/8/1P6/8` | W b2 b6 / B b7 | 3 | Ke5, Ke6 | – |
| cgt019 | `8/2p5/8/3P1Kp1/6Pk/8/3P4/8` | W d2 d5 / B c7 | 3 | – | **Ke6** |
| cgt020 | `8/2p5/8/1P3Kp1/6Pk/8/1P6/8` | W b2 b5 / B c7 | 3 | Ke4, Ke5, Ke6, Kf6 | – |
| cgt022 | `8/2p5/8/5Kp1/1P4Pk/1P6/8/8` | W b3 b4 / B c7 | 3/2±½ | Ke6 | – |
| cgt025 | `8/3p4/8/5Kp1/2P3Pk/8/2P5/8` | W c2 c4 / B d7 | 5/2±½ | Ke5, Kf6 | – |
| cgt221 | `8/8/8/3p1Kp1/6Pk/8/2P5/8` | W c2 / B d5 | \* | Ke5, Ke6 | – |
| cgt236 | `8/3p4/3P1Kp1/6Pk/8/8/3P4/8` | W d2 d6 / B d7 | 3 | – | **Ke5, Ke7, Kf7, Kg7** |
| cgt237 | `8/1p6/8/2P2Kp1/6Pk/8/2P5/8` | W c2 c5 / B b7 | 3 | Ke5, Ke6 | – |
| cgt238 | `8/1p3Kp1/6Pk/P7/8/8/P7/8` | W a2 a5 / B b7 | 3 | Ke6, Ke7, Ke8, Kf8 | – |
| cgt254 | `8/2p2Kp1/6Pk/8/2P5/8/2P5/8` | W c2 c4 / B c7 | {5/2±½ \| 1} | Ke6, Ke7, Ke8 | – |
| cgt259 | `8/8/2p2Kp1/6Pk/8/8/2P5/8` | W c2 / B c6 | ⇑\* | Ke5, Ke6, Ke7 | – |

With cgt055's Ke6 that makes 41 draws and 7 wins. 14 of the 21 positions have a *number* value, against 28 numbers among all 94.

**Data on the mechanism.**
- The one recorded line is from engine/suite/README.md, for cgt002: **Ke6! Kxg4 Kxd6 Kf3 c4**, rated a draw. The
  king gives up g4 and captures the d6 pawn.
- Geometry, derived from the FENs: 32 of the 48 non-losing king moves step closer to the nearest Black pawn on files
  a–d, 13 keep the distance and 3 move away. Among the 401 losing king moves, 194 step closer.

**Inference.**
- The king trades its g-pawn for a queenside pawn, or wins one outright (cgt008, cgt011, cgt019, cgt236). This works
  only when the trébuchet king already stands level with the Black pawns (A4–A6), never from A2 or A3.
- Moving closer is not enough on its own: about half the losing king moves also move closer.
- Positive numbers are over-represented: White has spare tempi, so giving up g4 costs less than the whole game.

---

## What A8 can take from this

**Data.** Positions where the frozen-king assumption alone gives the wrong outcome:
- **\*2 tree, terminals:** W a5 / B b7 c5 (Ke4 and Ke5 draw). Probable: W c4 / B a6 d6. Candidates: W a4 / B b7 c6,
  W a5 / B b7 c6, W c5 / B a6 d7.
- **\*2 tree, nodes:** W a2 c5 / B b4 d7, W a5 c3 / B b7 d5, W a5 c4 / B b7 d6, and W a3 c5 / B b5 d7 without the e.p.
  right. White is to move in all four, and a king move draws where the convention says White loses.
- **Suite:** cgt055, cgt120, cgt123, cgt262, cgt270.

**Data.** Most failures in the \*2 tree are not about kings. They come from counter-passers (about 81), e.p. (about
17) and races (7). In every such position that has a cached record, every king move loses.

**Inference.** On this data, the frozen-king model fails in two distinct ways:
1. the trébuchet king abandons its pawn to catch a lone passer or win a blockaded pawn;
2. a king move breaks a pawn zugzwang. This covers cgt055, W a5 c3 / B b7 d5 and W a2 c5 / B b4 d7.

The other main flaw of the \*2 convention is that "the first passed pawn wins" ignores an immediate capture that
makes a faster passer. That flaw is independent of the kings.

A loopy or explicit-king model should be tested first on the 9 king positions of the \*2 tree (1 shown terminal,
4 nodes, 1 probable terminal and 3 candidate terminals) and the 5 suite positions.

---

## Review notes (added after an adversarial review of this file)

An independent reviewer re-ran both extraction scripts and rechecked every count against the source files.
Every count matches, but it found the following. Where these notes and the text above conflict, these notes
win.

1. **Two frozen-king failures were missed.** Their evidence is cached Lichess categories of the positions
   reached by king moves (8-man categories, which realchess does not trust by default):
   - **W a4 c4 / B b6 d4**, White to move (`8/8/1p6/5Kp1/P1Pp2Pk/8/8/8 w`): **Ke4 wins**. a5 and Ke6 lose.
     The "unclear" label above should read "king leaves the trébuchet".
   - **Node W a5 c5 / B b7 d7**, White to move: the convention says loss, and **Kg6 and Kf6 draw**.
   - In W a5 c5 / B b7 d5 (White to move), a6, c6 and Ke5 all win. That "unclear" case is not a king case.
2. **Double counting.** A terminal with an e.p. right and its twin without it share one real position for
   the side that does not own the right. The 118 wrong (terminal, side) pairs are 110 distinct positions.
   The king-move tallies in terminal records deduplicate from 243 (150 lose / 89 unknown / 4 draw) to 209
   (126 / 79 / 4).
3. **Over-labelled claims.**
   - The "What A8 can take from this" list mixes probable cases and candidates under the **Data** label.
     W a5 c4 / B b7 d6 is not a clean king case: c5 and a6 also draw there.
   - "Most failures come from counter-passers (about 81)" includes 50 rule-based guesses with no record.
4. **Four node failures trace only to "unclear" terminal draws**, not to counter-passers or e.p.: W a4 c6 /
   B b7 d7 (Black to move), W a5 c5 / B b7 d7 (White), W a5 c6 / B b7 d7 (Black), W a6 c5 / B b7 d7 (Black).
5. **Sampling artefact.** "Every one has White to move" carries no information: 271 of the 275 suite positions,
   and all 94 headline positions, have White to move.
6. **Most of the 21 "non-losing king move" positions do not change the winning set.** Only 4 of the 20
   (cgt008, cgt011, cgt019, cgt236) have a king move that *wins*. In the other 16 the king moves only draw,
   so the set of winning moves is unchanged (consistent with the README's 90/94).
7. **The source snapshot is stale.** Another workstream rewrote the oracle-all file at 01:57. A re-run now
   resolves 128 terminals both ways (not 115). The failure list is unchanged.
