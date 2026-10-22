# K5: an independent check of cylcgt's canonical forms (a stand-in for CGSuite)

**Output directory:** `kings/delegate/out/K5/` (create it). Write only there.

## Why

Every canonical form in this project was computed by `cylcgt/cgt.py` alone. So far a second program has
checked only outcomes and nimbers (`atlas/flat8/rerun/REPORT.md`, item C11). CGSuite would be the natural
second opinion, but it is not installed and nothing may be installed (rule 2). You write that second opinion
yourself.

## Independence rule

- **Do not open, read or import `cylcgt/cgt.py`.** Write your own short-game engine from the textbook
  definitions:
  - Siegel, *Combinatorial Game Theory* (AMS 2013), ch. II;
  - Berlekamp–Conway–Guy, *Winning Ways*, vol. 1, ch. 1–2.
- You may import `cylcgt.pawns`, but only for the pawn rules: `Board`, `Pos`, `moves`, `passed`,
  `components`, `promote_distance`, and the globals `BIG`, `RACE_RULE` and `PASSED_RESPECTS_EP`.
- Read `cylcgt/pawns.py` lines 208–250 (`value`, `_value`, `_child`) and re-implement exactly that recursion
  with your own engine. Copy the convention exactly:
  - a passer check comes before the split into components;
  - a race is scored at the child, by the race rule;
  - an e.p. right exists only for the side that may capture.

## Your engine (`canon.py`)

- Games are pairs of option sets.
- Implement these operations:
  - ≤ by the recursive definition;
  - = as ≤ both ways;
  - negation;
  - disjunctive sum;
  - canonical form: delete dominated options, then bypass reversible options, repeated until nothing
    changes.
- Numbers: represent dyadic rationals directly. When adding a number x to a non-number G, use the
  translation theorem, x + G = {x + G^L | x + G^R}. Integers up to BIG = 256 must stay cheap.
- Memoise on canonical forms.
- Test file `test_canon.py` (pytest). It must include at least:
  - \* + \* = 0, ↑ + ↓ = 0, 1/2 + 1/2 = 1;
  - {0, \* | 0, \*} = \*2, and \*2 + \*2 = 0;
  - ↑ + \* is fuzzy with 0;
  - ↑² := {0 | ↓\*} is > 0 and < ↑;
  - ↑² + \* has canonical form {0, \* | ↓};
  - tiny(1) := {0 ‖ 0 | −1} is > 0. Also record how your engine compares it with ↑ and with ↑²; do not
    assume an answer;
  - 1/8 = {0 | 1/4};
  - G := {2 + {1 | −1} | −2 + {1 | −1}} satisfies G = −G, so G + G = 0.

## Targets

The flat 8×8 board is `pawns.Board(8, 8, False, True)`; the 3-file cylinder is `pawns.Board(3, 8, True, True)`.

| # | Board | Position | Claimed value (RESULTS.md, atlas reports) |
|---|---|---|---|
| 1 | flat 8×8 | `W: a2 a3 b2 / B: a6 b5 b6` | 1/8 under all 9 settings |
| 2 | flat 8×8 | `W: a2 b2 b3 / B: a5 a6 b6` | 1/8 (the mirror of #1) |
| 3 | flat 8×8 | `W: a2 b4 c4 / B: a7 b7 d6` | 1/8 under the e.p.-aware test, count rule |
| 4 | flat 8×8 | `W: a2 b2 c3 / B: b5 b6 c7` | 1/16 under the e.p.-aware test, count rule |
| 5 | flat 8×8 | `W: a2 b2 d4 / B: a7 c6 d7` | ↑² = {0 \| ↓\*} under the e.p.-aware test, count rule |
| 6 | flat 8×8 | `W: a2 b2 b6 / B: a6 b7 c5` | ↑²\* = {0, \* \| ↓} under every setting |
| 7 | flat 8×8 | `W: a2 b2 b6 / B: a6 b7 c6` | tiny(1) under the e.p.-aware test, count rule |
| 8 | flat 8×8 | `W: a2 c2 / B: b7 d7` | \*2 under the textbook test with the count and mover rules; 0 with opponent; the same with e.p. off; {2±1 \| −2±1} under the e.p.-aware test, count rule |
| 9 | cyl 3×8 | `W: a2 a3 b2 / B: b7 c6 c7` | \*2 under the e.p.-aware test, count rule |

**Settings.** There are 9 settings: race rule count, mover or opponent, times three e.p. treatments:
- e.p. off: `Board(..., ep=False)`;
- textbook: e.p. on, `PASSED_RESPECTS_EP = False`;
- e.p.-aware: e.p. on, `PASSED_RESPECTS_EP = True`.

Run every target under all 9. Call `pawns._value.cache_clear()` and clear your own caches after each
change.

**For every target and setting**, compute:
- V_own, with your engine;
- V_cyl = `cylcgt.pawns.value(board, pos)`. Calling it is allowed, since you are not reading its code.
  Convert the result into your engine's representation by walking its option sets (`.L` and `.R`, or
  whatever the Game object exposes; inspect the object, not the source), then test V_own = V_cyl with
  **your** comparison;
- whether V_own equals the claimed value, built from its definition in your engine, where a claim exists for
  that setting.

A race inside the recursion raises nothing in your version, since the race rule scores it. If cylcgt raises
`RaceError`, record that.

## Deliverables

- `canon.py`, `test_canon.py`, `check_targets.py` and `run.sh` (the exact commands).
- `targets.tsv`: target, setting, V_own (your printed form), equals V_cyl (yes/no), equals claim
  (yes/no/no claim), seconds.
- `REPORT.md`. Start with the 5-line summary. Then:
  - the pytest result;
  - the 9 × 9 table;
  - every disagreement, with the smallest subposition where the two engines first differ. Find it by walking
    down the game tree.

  Label agreement between your engine and cylcgt as CHECKED-2, and anything only you computed as COMPUTED-1.

## Limits

- One Python process, under `nice -n 10`, under 3 GB RSS.
- At most 45 minutes in total.
- If one target and setting takes more than 5 minutes, skip it and say so.
