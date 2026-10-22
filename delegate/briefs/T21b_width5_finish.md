# T21b: finish the flat 5-file 8-pawn census (T21 stopped before its report)

**Output directory:** `research/star2_width5/`. Keep T21's files. Add new files and write `REPORT.md`.

**What T21 left.**
- `summary.txt`: 14,680,983 roots on the flat 5-file board, 8 pawns, all 9 settings.
- `hits.tsv`: 183 hits, all \*2 or \*3:
  - 21 positions are \*2 under count / e.p.-aware;
  - there is no \*3 under count or mover;
  - there are \*3 hits under the opponent rule: 16 at O/T, 2 at O/off, 32 at O/aware.
- `verify_headline_chunk{0..5}`: chunks 3 and 5 finished. Chunks 0, 1, 2 and 4 were cut off.

**Task.**
1. Finish the `cylcgt` verification of all 183 hits in their claimed settings.
   - Rerun the unfinished chunks with `verify_hits.py`: at most 3 processes, each chunk under 40 minutes,
     resumable.
   - Use `Board(5, 8, False, ep)`, and set `RACE_RULE` and `PASSED_RESPECTS_EP` per setting.
   - Record agree or disagree for every hit.
2. Check with the independent whole-board solver. Use `verify_ext/codex/solver.py`:
   `PawnGame(5, race, ep, test)`, `parse_position(text.replace(":", ""), 5)` and `value(w, b)`. Check:
   - every C/aware \*2 hit (21);
   - every \*3 hit (all opponent-rule settings).

   Note: `cylcgt` sums components, while the Codex solver ends the game at the first passed pawn. They may
   legitimately differ under the opponent rule. Report both values for each hit, and say which model each
   \*3 holds in.
3. Trébuchet fit. Check every hit for whether it sits legally beside the trébuchet (W Kf5 Pg4, B Kh4 Pg5).
   Flag a position if:
   - any pawn on the e-file attacks f5 or h4 (a black pawn on e6 checks Kf5);
   - a king could capture a pawn next to it.
4. **Report** (`REPORT.md`), with labels and reproduce commands:
   - the root count;
   - the hit table, with values in both solvers;
   - the trébuchet-fit flag for each hit;
   - the answer to "is there a \*3 under count or mover?" (expected: no);
   - the answer to "which \*3 positions hold in both models?".
