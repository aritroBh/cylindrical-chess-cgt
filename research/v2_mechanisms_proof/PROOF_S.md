# Proof of the square rule S (certified passers), frozen-king pawn game

**Label: PROVED (by hand) for the frozen-king pawn game.** Real chess with active kings is excluded (a king can stop a certified passer); the 128 remaining mismatches after CC are king effects.

## 0. Summary (5 lines)

1. S says: a side X with a *front, e.p.-aware passed* pawn whose unobstructed promotion distance `n` is no greater than (or, if X is not to move, strictly less than) the fastest unobstructed promotion distance `d` of any enemy pawn, wins the frozen game by running that pawn.
2. The proof has three lemmas: the runner can never be captured or blocked, even after pushes (Lemma 1); no enemy pawn can promote in fewer than `d` moves, even with captures or when blocked (Lemma 2); the ply counts give the two inequalities (Lemma 3).
3. Together they show X promotes first, and a promotion wins at once; if Y has no pawn move, Y loses by rule.
4. The same argument works on cylinders (adjacency taken cyclically) and for any height `H ≥ 3`; it does not need an empty file.
5. Exhaustive check: `cc.py` found 0 unsound certifications in 158,544 (position, side, e.p.) cases on 2–3 files, 6–8 ranks.

## 1. Definitions

**Board/game.** `k` files (cyclic on a cylinder, linear otherwise), `H` ranks. White pawns move up (toward rank `H`), Black down (toward rank 1). Kings may not move; a king move loses at once. Reaching the last rank promotes and wins immediately. A side with no legal pawn move loses. Promotion is queen-equivalent in effect: the game ends on promotion, so underpromotion is irrelevant.

**Passed (e.p.-aware).** A pawn of X on `(f,r)` is passed iff (i) no enemy pawn lies on files `f-1,f,f+1` (mod `k`) at a rank strictly beyond `r` in X's direction, and (ii) it is not capturable en passant. Condition (ii) excludes a pawn that has just double-stepped past an enemy pawn that can take it.

**Front.** A passed pawn is *front* iff no own pawn lies on the same file strictly beyond `r` in X's direction. A *runner* is a front passed pawn.

**Distances.** For a White pawn on rank `r`:
`sdist_W(r) = H - r - (1 if r = 2 else 0)`.
For a Black pawn on rank `r`:
`sdist_B(r) = r - 1 - (1 if r = H-1 else 0)`.
These are the fewest moves to promote if nothing obstructs, counting one double step from the start rank. Then
`n = min{sdist_X(r) : (f,r) is a runner of X}` (or undefined if none),
`d = min{sdist_Y(r) : (f,r) is any pawn of Y}` (or `∞` if Y has none).

**S (corrected statement).** `S_cert(pos, mover, X)` is true iff X has at least one runner and
- `n ≤ d` when `mover = X`, or
- `n < d` when `mover = Y`.

## 2. Lemmas

**Lemma 1 (Passer safety).** A runner of X, when X pushes it straight ahead every turn (double step from the start rank if possible, else single), is never captured (normally or en passant) and never blocked, on any board including a cylinder, against any legal Y pawn moves.

*Proof.* At the moment it is a runner: no enemy pawn is beyond it on its or adjacent files, so no normal captor exists at `(f±1, r±1)` in X's direction; no own pawn is ahead on its file; and the e.p.-aware test removes any e.p. captor.

Pushes only increase the runner's rank in X's direction. Y's pawns move the opposite way, so their ranks in X's direction never increase; a pawn not beyond the runner before cannot become beyond it later, and a capture by Y moves downward in X's coordinate, never creating a captor at the needed square. Thus no normal capture appears after the start.

For en passant: an e.p. capture of the runner requires it to have just double-stepped from the start rank with an enemy pawn on an adjacent file at the landing rank. But that landing rank is strictly beyond the start rank, and such an enemy pawn would have been beyond the runner before the push, contradicting passedness. If the push is single, no e.p. right arises at all. Hence no e.p. capture.

Own pawns of X move in X's direction but cannot pass or capture onto the runner's square: the runner occupies it, and a capture needs an enemy pawn on the target square, which passedness forbids ahead on the same file. So the runner stays front. On a cylinder the same rank-monotonicity holds with files read mod `k`. ∎

**Lemma 2 (Y's promotion lower bound).** Every pawn of Y needs at least `sdist_Y(r)` moves to promote in the frozen game, even allowing captures and even if it is blocked; therefore Y cannot promote in fewer than `d` moves.

*Proof.* A pawn's progress toward its promotion rank is at most 2 ranks on its first move (only the straight double step from the start rank) and at most 1 rank on every other move, including every capture (captures never double-step). `sdist_Y(r)` is exactly the move count if maximal progress occurs each move. Captures change file but do not reduce the rank-step count below this; blockages and detours can only increase the number of moves needed, never create faster progress. Hence actual moves ≥ `sdist_Y(r)` for each pawn. Taking the minimum over Y's pawns gives `d`. If Y has no pawn, `d = ∞` and Y has no pawn move. ∎

**Lemma 3 (Ply accounting).** If X pushes one runner every X-turn, X promotes on ply `2n-1` (X to move first) or ply `2n` (Y to move first). By Lemma 2, Y's earliest promotion is no earlier than ply `2d` (X first) or ply `2d-1` (Y first).

*Proof.* X moves on plies 1,3,5,… (X first) or 2,4,6,… (Y first); the runner's distance `n` is a count of X-moves, so its `n`-th push is X's `n`-th move, at ply `2n-1` or `2n`. Y's `d`-th move occurs `d` Y-turns after the start, at ply `2d` or `2d-1`. ∎

## 3. Theorem (S soundness)

If `S_cert(pos, mover, X)` is true, then in the frozen-king pawn game X wins from `pos` with `mover` to move.

*Proof.* Take a runner `s` achieving `n`. X's strategy: every X turn, push `s` straight ahead maximally (double step from the start rank if legal, else single). By Lemma 1 this is always legal and `s` remains a runner, so the strategy is well-defined. By Lemma 3, X promotes `s` on ply `2n-1` (X first) or `2n` (Y first), while Y cannot promote before ply `2d` (X first) or `2d-1` (Y first).

- If X moves first, S gives `n ≤ d`, so `2n-1 ≤ 2d-1 < 2d`: X promotes first.
- If Y moves first, S gives `n < d`, so `2n ≤ 2d-2 < 2d-1`: X promotes first.

A promotion wins immediately, so X wins. If at some point Y has no legal pawn move, then by the frozen-game rule Y loses (any king move loses at once), and X still wins; this is covered by `d = ∞`. ∎

**Completeness note.** S is sufficient, not necessary: a runner may win without being certified (e.g. a nearer but permanently blocked enemy pawn). Multiple runners are handled because X needs only one whose `n` satisfies the inequality; `n` uses the minimum, and any runner may be run.

## 4. Scope

- **Cylinder:** the passed test uses cyclic file adjacency; rank monotonicity is unchanged, so Lemmas 1–3 and the theorem hold on cylinders and rings. No empty file is required for S itself.
- **Height:** `sdist` uses `H` and the start ranks 2 and `H-1`, so the proof holds for any `H ≥ 3`.
- **Real chess:** false. An active king can step in front of a certified runner (or take it), so S certifies only the frozen game. The 128 mismatches remaining after CC are exactly these king effects.
- **Sums:** the inequality uses the global minimum over all Y pawns, so the strategy wins even when several components are present.

## 5. Reproduce

```sh
cd /Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms
python3 -I cc.py   # exhaustive soundness (S_UNSOUND = 0) and re-score
```

The `cc_result.json` field `exhaustive_soundness` reports `S_UNSOUND: 0` and `RP_UNSOUND: 0` for all four board configurations (2 files × 6 ranks, 3 × 6, 2 × 8, 1 × 8).