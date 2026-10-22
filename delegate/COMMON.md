# Shared brief for every delegated task

Project root: `/Users/aritro/Downloads/Research/Chessendgames`. This continues a 2025 high-school paper,
"Analysis of Chess Endgames on a Cylindrical Chessboard" (`prior_work/main.tex`): combinatorial game theory
(CGT) of king-and-pawn endgames on cylinder (files a and h glued) and flat boards.

Read first:
- `RESULTS.md`, the status page;
- `RESEARCH_PLAN.md` §3;
- the REPORT.md files your task names.

## Conventions (Elkies 1996, as used in `cylcgt/`)

- **Sides and normal play.** White = Left, Black = Right. A side with no move loses.
- **Passed pawns.** One side having a passed pawn is worth ±BIG (BIG = 256). If both sides have one, it is a
  race, resolved by `cylcgt.pawns.RACE_RULE` ("count", "mover" or "opponent").
- **En passant (adopted 2026-10-16).** A pawn that can still be taken en passant is NOT passed
  (`cylcgt.pawns.PASSED_RESPECTS_EP = True`). Setting it to False gives the older "textbook" test. Many earlier
  results were computed with the textbook test; say which test you use.
- **Components.** An empty file stays empty forever, so pawn groups separated by one are disjunctive summands.
- **King freeze.** The trébuchet king group (W Pg4 / B Pg5, WK f5, BK h4 on the flat 8×8 board) is assumed to
  be 0.
- **API.**
  - `cylcgt/pawns.py`: `Board(files, ranks, wrap, ep)`, `Pos.parse("W: a2 c2 / B: b7 d7")`,
    `value(board, pos)`, `describe(board, pos)`.
  - `cylcgt/cgt.py`: `show`, `outcome`, `add`, `neg`, `le`.
  - Call `pawns._value.cache_clear()` after changing a global.

## Rules

1. **Where to write.** Only inside your task's output directory; create it. Never edit existing files elsewhere.
   Never run git commands.
2. **Software.**
   - Use `.venv/bin/python` (stdlib + pytest) with `PYTHONPATH=.` from the project root.
   - The ML tasks use `.venv-ml/bin/python` (PyTorch with MPS, MLX).
   - Do not install anything.
   - Compiling your own C with `cc -O2` is fine.
3. **Network.** Use none, except the Lichess tablebase. Go through `realchess/probe.py`, whose disk cache
   already holds about 2,000 positions. Keep to at most 200 new requests and 1 per second.
4. **Long jobs.** Keep any single job under 45 minutes. Run long jobs in the background and poll them.
5. **Honesty.**
   - Label every claim **PROVED**, **CHECKED-2** (two independent implementations agree), **COMPUTED-1** or
     **CONJECTURE**.
   - Give an exact reproduce command for every number.
   - Report negative results plainly, and never overstate novelty.
6. **Deliverable.** Finish by writing `REPORT.md` in your output directory. Its first section is a 5-line
   summary of what you established.
7. **Shared machine (added 2026-10-22).**
   - Other projects and other agents run on this machine.
   - **Never kill, stop or signal a process you did not start yourself.** No `pkill`, `killall` or `kill` on
     anything but your own PIDs.
   - Memory is tight. Keep every process under 4 GB RSS, and run at most 2 heavy processes at once, under
     `nice -n 10`.
   - Never feed kpsolve a whole-board position list larger than 100 MB.
   - Never commit, push or edit `paper/`.
   - Do not create a file over 50 MB.
