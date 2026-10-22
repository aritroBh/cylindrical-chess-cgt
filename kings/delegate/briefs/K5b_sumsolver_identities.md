# K5b: check cylcgt's values by playing G − V, with the existing brute-force solver

**Output directory:** `kings/delegate/out/K5b/` (create it). Write only there.

## Why

Every canonical form in this project comes from `cylcgt/cgt.py`. K5 tried to give a second opinion and copied that
file instead (see `kings/delegate/out/K5/REVIEW.md`). This task uses a different method, which needs no canonical
forms at all:

> G = V if and only if G + (−V) is a second-player win (outcome 𝓟).

`sumtest/sumsolver.py` is the project's brute-force outcome solver. It plays a pawn position G plus an explicit game
tree out by exhaustive minimax. It computes no canonical forms and does not import cylcgt. Read its module docstring
and its classes `Trees`, `Rules` and `SumSolver`.

**Independence rule.** Do not read `cylcgt/cgt.py`. Build every V from its definition, with `Trees.node`,
`Trees.add` and `Trees.neg`.

## How to use sumsolver

The flat 8×8 board is `Geometry(8, False)`; the 3-file cylinder is `Geometry(3, True)`. Every board has 8 ranks.

- **Settings.** e.p. off is `Rules(geo, ep=False, ...)`. The textbook test is `ep=True, ep_aware=False`. The
  e.p.-aware test is `ep=True, ep_aware=True`. The race rule is `race_rule=` one of "count", "mover" or
  "opponent". Keep `race_double=True` and `ep_scope="component"`.
- **Add every tree before you build the solver.** `SumSolver.__init__` precomputes masks over the nodes that exist
  at that moment. So do not use `make()` and then add nodes. Build `Geometry`, `Rules` and `Trees`, add all your
  trees, then construct `SumSolver(rules, T, mode=...)`.
- `solver.solve(solver.start_state(W, B))` returns bit masks (wl, wr) over all tree nodes.
  `SumSolver.outcome(wl, wr, k)` gives 𝓛, 𝓡, 𝓝 or 𝓟 for G + node k.
- **Modes.** Run both:
  - "whole": the first passer ends the whole sum;
  - "comp": the position is re-split into components, as cylcgt does.

  Report both. Where they differ, say so.

## The values, from their definitions

- **Numbers:** n = {n−1 | } and −n = { | −n+1}; 1/2 = {0 | 1}, 1/4 = {0 | 1/2}, 1/8 = {0 | 1/4}, 1/16 = {0 | 1/8}.
- **Stars and ups:** \* = {0 | 0}; \*2 = {0, \* | 0, \*}; ↑ = {0 | \*}; ↓ = {\* | 0}; ↓\* = ↓ + \*, an explicit
  sum made with `Trees.add`.
- **↑²** = {0 | ↓\*}. ↑²\* = ↑² + \*, an explicit sum. Also test the literal form {0, \* | ↓}, and report whether
  both give the same outcomes.
- **tiny(1)** = {0 ‖ 0 | −1}, that is {0 | {0 | −1}}.
- **{2±1 | −2±1}** = {{3 | 1} | {−1 | −3}}.

**Sanity checks first.** `W: a4 / B: a5` on the flat board has no moves for either side, so it is the game 0, and
G0 + X has the outcome of X. Use it to check:
- V + (−V) is 𝓟 for each V above;
- 1/8 + 1/8 + (−1/4) is 𝓟;
- ↑² is 𝓛 and ↑ − ↑² is 𝓛;
- tiny(1) is 𝓛. Also record the outcome of ↑² − tiny(1); there is no expected answer, so it is not a pass or fail
  test;
- \*2 + \*2 is 𝓟;
- G + G is 𝓟 for G = {2±1 | −2±1}.

All must pass before you go on.

## Targets

| # | Board | Position | Claimed value |
|---|---|---|---|
| 1 | flat 8×8 | `W: a2 a3 b2 / B: a6 b5 b6` | 1/8 under all 9 settings |
| 2 | flat 8×8 | `W: a2 b2 b3 / B: a5 a6 b6` | 1/8 under all 9 settings |
| 3 | flat 8×8 | `W: a2 b4 c4 / B: a7 b7 d6` | 1/8, e.p.-aware, count |
| 4 | flat 8×8 | `W: a2 b2 c3 / B: b5 b6 c7` | 1/16, e.p.-aware, count |
| 5 | flat 8×8 | `W: a2 b2 d4 / B: a7 c6 d7` | ↑², e.p.-aware, count |
| 6 | flat 8×8 | `W: a2 b2 b6 / B: a6 b7 c5` | ↑²\* under all 9 settings |
| 7 | flat 8×8 | `W: a2 b2 b6 / B: a6 b7 c6` | tiny(1), e.p.-aware, count |
| 8 | flat 8×8 | `W: a2 c2 / B: b7 d7` | \*2 with count or mover, under e.p. off and textbook; 0 with opponent, under e.p. off and textbook; {2±1 \| −2±1}, e.p.-aware, count |
| 9 | cyl 3×8 | `W: a2 a3 b2 / B: b7 c6 c7` | \*2, e.p.-aware, count |

## Two passes

1. **Claims.** For every target and every setting that has a claim, solve G + (−V_claim) in both modes and record the
   outcome. "Confirmed" means 𝓟.
2. **cylcgt's value at every one of the 81 target × setting pairs.** Get V_cyl from `cylcgt.pawns.value(board, pos)`.
   Use `cylcgt.pawns.Board(8, 8, False, ep)` or `Board(3, 8, True, ep)` with the matching globals
   `pawns.RACE_RULE` and `pawns.PASSED_RESPECTS_EP`, and call `pawns._value.cache_clear()` after every change.
   - Convert V_cyl into a `Trees` node by walking its Left and Right option lists **only**. Inspect the object to
     find their attribute names. Do not use any number or nimber tags it carries.
   - Then solve G + (−V_cyl).
   - If V_cyl contains an integer of absolute value 64 or more (BIG translations), skip that pair and say so. sumsolver
     treats a passer as a win in "whole" mode and as 64 in "comp" mode, so such a test would not mean anything.

## Deliverables

- `identities.py` and `run.sh`, with the exact commands.
- `sanity.txt`.
- `claims.tsv`: target, setting, claim, outcome in "whole" mode, outcome in "comp" mode, confirmed yes/no.
- `cylcgt.tsv`: target, setting, cylcgt's printed value (`cylcgt.cgt.show` is allowed for display only), "whole",
  "comp", confirmed yes/no/skipped.
- `REPORT.md`, starting with a 5-line summary.
  - A confirmed identity is CHECKED-2: cylcgt's canonical form versus an independent search. Say that sumsolver was
    written by a Claude model, so the check is independent of cylcgt's code but not of the model family.
  - List every non-𝓟 result with its outcome.

## Limits

- One Python process, under `nice -n 10`, under 3 GB RSS.
- At most 45 minutes in total.
- If one target × setting × mode takes more than 5 minutes, skip it and say so.
