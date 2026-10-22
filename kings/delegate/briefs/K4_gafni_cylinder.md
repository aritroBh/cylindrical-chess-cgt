# K4: K+P vs K as a loopy combinatorial game, with and without edges

**Output directory:** `kings/delegate/out/K4/` (create it). Write only there.

## Background

Plan item A8 asks us to re-examine Gafni's K+P vs K values "without edges", i.e. on a cylinder. All we have
of Gafni (thesis, 2011) is a second-hand summary in `notes/lit_cgt_chess.md`: K+P vs K on 3×3 and 3×4 boards
treated as loopy games, with values on\*, {on | 0} and 1\*. Our own literature check
(`notes/novelty_check/REPORT.md`) could not locate the thesis. Do not search the web for it (rule 3).
So this task does not re-check Gafni. It computes the same kind of object under a convention fixed below,
on flat boards and on cylinders of the same size, and reports what changes when the edges go.

## The game

**Boards.** flat and cyl, W×H in this order: 3×4, 4×4, 3×5, 4×5, then 5×5 if time allows (see "Limits").
The 3×3 board is outside `kings/SPEC.md` (it needs H ≥ 4); say so in the report rather than hacking it.

**Chess part X.** Positions reachable from a White king, one White pawn and a Black king, under the rules of
`kings/SPEC.md`: all four promotions (Q, R, B, N), so the graph also contains K+officer vs K and K vs K.
Use the move generator of the project's reference solver, `kings/ref/solve.py`. The calls you need are
`kings.ref.solve.make_solver(board=..., ep='on', promote='QRBN', cap=1)`, then `solver.moves(pos, full=True)`
(read its docstring: it returns quiet successors and (tag, successor) exits) and `solver.in_check(pos)`.
Its position tuple format is described at the top of the file. With one pawn, cap 1 never caps a promotion;
assert that no exit has tag CAPPED.

**Test games T.** Each is a small explicit game graph with Left = White and Right = Black, no terminals:
- 0 (no options); the integers 1, 2, −1, −2 (n = {n−1 | }, −n = { | −n+1});
- \* = {0 | 0}; ↑ = {0 | \*}; ↓ = {\* | 0}; 1/2 = {0 | 1}; −1/2 = {−1 | 0}; ±1 = {1 | −1};
- on = {on | }; off = { | off}; dud = {dud | dud}; over = {0 | over}; under = {under | 0}.

That is 17 games. Also write a function that forms the sum of two test games (the product graph), so
that candidates like on + \* can be built.

**The sum x ⊞ T.** State (x, t, s): chess position x, test-game position t, side s to move.
- s moves either in x (any legal chess move of s) or in T (any s-option of t).
- A move in T is not allowed while s is in check in x.
- **Normal play:** if s has no move at all, s loses. This covers checkmate, and it also makes a stalemate in
  the sum a loss, unlike chess. State this convention prominently.
- Infinite play is a draw.
- The result r(x, t, s) ∈ {W, D, L} (White's view) is the least fixed point computed by retrograde analysis,
  as in Definition 1.2 of `kings/theory/LOOPY.md`.

Build the chess move graph once per board (adjacency lists), then solve each product over it.

**Signature.** For a *quiet placement* x (White K, White P, Black K, neither king in check, so either side may
start), its signature is the 34 results r(x ⊞ T) for the 17 test games T, with White starting and with Black
starting.

**Candidate values.** Compute the signature of each candidate V the same way, as V ⊞ T with V itself a test
game:
- the 17 test games;
- on + \*, off + \*, 1 + \*, −1 + \*, ↑ + \*;
- {on | 0}, {0 | off}, {on | off}, {0 | on}, {off | 0}.

Then for each quiet placement:
- list every candidate whose signature equals its own (a signature cannot separate every value, so
  several may match; list them all);
- if none matches, mark it "unmatched" and keep its signature;
- also mark the two extremes: "White wins against every T" and "Black wins against every T". These are
  decisive events (a forced mate or promotion), not CGT values;
- for every matched candidate V, run the difference test: solve x ⊞ (−V), where −V swaps Left and Right.
  Record whether it is a second-player survival: with White starting the result is D or L, and with Black
  starting it is D or W. For stoppers this is the usual test of x = V (Siegel, *Combinatorial Game Theory*,
  ch. VI). x is generally not a stopper, so treat the test as a consistency check only.

## Checks you must pass before reporting anything

1. **Against the exact chess solver.** Run the solver in a chess variant: T = 0, and a stalemate is a draw
   instead of a loss. The results must equal kpsolve's for every KPK position with either side to move, on
   every board you report. Build kpsolve with `cc -O2 -o kings/delegate/out/K4/kp kings/kpsolve.c`. Run it as
   `nice -n 10 kings/delegate/out/K4/kp --board <flat|cyl>:WxH --ep on --promote QRBN --cap 1 --threads 2 < in.txt`.
   The input format is one position per line, like `Kb1 Pa2 kc4 w -`. The output is `<pos> | <A> <B>`, with
   A = B = W, D or L from White's view when exact. Report the number of positions compared and the number of
   differences, which must be 0. If it is not 0, stop and report the differences.
2. **Against known CGT facts.** Solve pure sums of test games and check these outcomes:
   - 1 + (−1), \* + \*, ↑ + ↓ and 1/2 + 1/2 + (−1): second player wins;
   - on + (−2): Left wins either way; on + off: draw either way; dud + 1: draw either way;
   - over + (−1/2): Right wins either way; over: Left wins either way;
   - ↑ + \*: first player wins.

   Report each fact as pass or fail. Fix your code until all pass.

## Deliverables

- The solver, split into modules of at most about 200 lines, each written in its own step (for example
  `graph.py`, `testgames.py`, `product.py`, then `gafni.py` as the driver). Long single-file writes have
  timed out on this provider. Also `run.sh` with the exact commands, and one `<board>.jsonl` per board with one line
  per quiet placement: placement, signature, matched candidates and difference-test results.
- `REPORT.md`. Start with the 5-line summary. Then:
  - check 1 and check 2 results;
  - for each W×H, a flat-versus-cylinder table: each class (matched candidate set, unmatched, the two
    decisive extremes), with its count and one example placement on each board;
  - the classes that occur on only one of the two boards;
  - for each, an example where the same placement changes class when the edges go (when that placement
    exists on both boards);
  - whether on + \*, {on | 0} and 1 + \* occur on flat 3×4 and on cyl 3×4. Label every comparison with
    Gafni as "against a second-hand summary; the source was not located";
  - where the classes on, off, dud and the numbers occur, and what that says about Proposition 4.3 of
    `kings/theory/LOOPY.md` (no finite king tempo in isolated groups). An integer class here would be
    finite king tempo. Look for one.
- Label every claim COMPUTED-1, CHECKED-2 or PROVED, following `delegate/COMMON.md`.

## Limits

This is a light job (rule 7):
- one Python process at a time, under `nice -n 10`, staying under 3 GB RSS;
- at most 20 minutes per board;
- if 4×5 takes more than 10 minutes, skip 5×5 and say so.
