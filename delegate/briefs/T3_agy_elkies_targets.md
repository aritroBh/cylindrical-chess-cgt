# T3 (agy): Elkies targets, finishing workstream A3-targets

Output directory: `atlas/targets/`. A previous agent left partial work there; read and reuse it. Put new files in `atlas/targets/final/` if you'd rather not touch the old ones.

Inputs:
- `atlas/flat8/values_aware.jsonl.gz`: e.p.-aware values, count rule;
- `atlas/flat8/rerun/values.jsonl.gz`: textbook values;
- `atlas/flat8/rerun/REPORT.md`.

1. For every position in the e.p.-aware database whose value is one of these targets, recompute its value in all 9 settings ({count, mover, opponent} × {e.p. off, textbook, aware}) with cylcgt. Targets: 1/8, -1/8, 1/16, -1/16, ↑² = {0 | ↓*}, ↑²* = {0,* | ↓}, tiny(1), tiny(2), tiny(1*).
2. Mark each position ROBUST if it has the same value in all 9 settings.
3. Check reachability of the pawn structure in a real game: pawn counts, capture parity per file, and no pawn on a file it could not have reached. Hand-build a move history for the best ROBUST position of each target, as the rerun did for 1/8.
4. For each robust target, give the 8×8 FEN with the trébuchet (component on files a-d, file e empty, W Pg4 / B Pg5, WK f5, BK h4) and state its man count.
5. Write `atlas/targets/REPORT.md`, including a table: target → number of positions → robust ones → best reachable example and FEN.
