# Logic Referee of the Certified-Passer Test (Square Rule S)

## Verdict (5 lines)

**SOUND WITH FIXES** — The square rule S is sound for the frozen-king pawn game (no counterexamples in 158,544 exhaustive cases), but the proof sketch in `v2_mechanisms/REPORT.md` lines 107–109 is incomplete. The rule correctly certifies only the frozen game; it is false in real chess with active kings (explicitly acknowledged). Missing proof steps are identified below. Labels: rule soundness **COMPUTED-1** (exhaustive check), proof completeness **CONJECTURE** (sketch only), real-chess inapplicability **PROVED** (by counterexample: king stops passer).

## 1. Completeness of the proof sketch

The sketch argues: (a) a passed front pawn cannot be blocked or captured (no enemy pawn ahead on its file or adjacent files; enemy pawns only move toward promotion; an e.p. captor would be ahead, hence excluded), (b) X always has the move of the passer, (c) Y cannot promote in fewer than d moves (d = min unobstructed distance of any Y pawn). These three claims are true, but the sketch does not *prove* them; it merely states them. Specific gaps:

1. **E.p. after the passer moves**: The sketch only addresses the current position. It must show that after X pushes the passer (possibly two squares from the start rank), no new e.p. capture arises. This holds because a passed front pawn on its start rank has no enemy pawn on the intermediate rank (that pawn would be "ahead" now), but this requires a rank-by-rank induction not in the sketch.
2. **Y's promotion lower bound**: d is the minimum of `sdist` over *all* Y pawns, including blocked ones. The sketch must argue that obstacles (X's non-passer pawns) can only increase the actual moves needed, so d is a valid lower bound. This is true because pawns never move backward and captures do not reduce the number of rank steps to promotion, but the sketch omits this reasoning.
3. **Move-order accounting**: The conditions n ≤ d (X to move) and n < d (Y to move) correctly reflect that X promotes on ply 2n−1 and Y on ply 2d (or 2d−1 if Y moves first). The sketch states the inequalities without deriving them from the ply count.
4. **Y has no legal pawn moves**: If Y has no moves, Y loses immediately (king move loses). The code handles this (d = INF), but the sketch does not mention it.
5. **Choice among multiple runners**: X may have several front passed pawns; the code uses min n. The sketch must note that any runner pushed every turn promotes in its own n moves and is equally uncatchable, so the fastest one suffices.

## 2. Dependence on cylinder or board height

The rule does **not** depend on cylinder wrapping. The exhaustive test in `cc.py` runs on flat boards (k adjacent files, no wrap) of 6 and 8 ranks with up to 3 files; the cylinder is handled by decomposing into independent components separated by empty files. The `sdist` formula uses the board height H and start-rank positions (rank 2 for White, H−1 for Black), so it generalizes to any H ≥ 3. No wrap-around captures are used in the certificate.

## 3. What is NOT claimed (real chess with active kings)

The REPORT is clear (lines 107, 159): S certifies **only the frozen-king pawn game**. In real chess, a king can stop a certified passer (e.g., by moving into the promotion square's zone), so S is unsound for real chess. The 128 remaining mismatches after CC are all king effects (line 146). The REPORT correctly limits the claim to the frozen game.

## 4. Missing steps to make the proof complete

To turn the sketch into a rigorous proof, add:

- **Lemma 1 (Passer safety)**: In the frozen game with e.p.-aware passed test, a front passed pawn of X is never capturable (normal or e.p.) and never blocked, regardless of how many times X pushes it. Proof by induction on the number of pushes: base case holds by definition of passed/front; inductive step uses that enemy pawns move opposite to X's passer, so they never reach the passer's file or adjacent files ahead of it.
- **Lemma 2 (Y's promotion lower bound)**: For any Y pawn, the number of moves to promote in the frozen game is at least its unobstructed distance `sdist`. Proof: each move advances the pawn by at most one rank toward promotion (two on the initial double step, which `sdist` accounts for); captures change file but not the rank-progress rate; obstacles can only remove legal moves, not create shortcuts.
- **Lemma 3 (Race outcome)**: If X pushes a front passed pawn of distance n every turn, X promotes on ply 2n−1 (X to move) or 2n (Y to move). Y's earliest promotion is ply 2d (X to move) or 2d−1 (Y to move). Therefore X promotes first iff n ≤ d (X to move) or n < d (Y to move).
- **Theorem (S soundness)**: If S_cert returns True, X has a winning strategy (push the fastest runner). By Lemmas 1–3, this strategy promotes before Y can. If Y has no legal pawn moves, X wins immediately (FG rule).

These lemmas close all gaps. The exhaustive computational check (COMPUTED-1) already confirms no counterexample exists in the tested domain (2–3 files, 6–8 ranks, all legal e.p. rights).

## Reproduce command

```bash
cd /Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms
python3 -I cc.py   # prints exhaustive soundness tables and re-score; writes cc_result.json
```

The `cc_result.json` field `exhaustive_soundness` shows `S_UNSOUND: 0` and `RP_UNSOUND: 0` for all four board configurations.