# T25: skeptical, independent check of T12 (odd-width cylinders)

**Output directory:** `research/odd_cylinders_verify/`. Create it. Do not edit `research/odd_cylinders/`.

**T12's claims** (`research/odd_cylinders/REPORT.md`, all COMPUTED-1 by one free-model run):
- (a) The 5.1 trébuchet (W Pa(r), B Pa(r+1), WK on file n−1, BK on file 1) is a mutual zugzwang on every
  cylinder Cn×R with n ≥ 4, and illegal on C3.
- (b) **Suspicious:** in K+P vs K on every cylinder with n ≥ 4, "direct opposition (kings on the same file) is
  always a draw for both sides to move, while diagonal opposition is a White win".
- (c) On C3, every K+P vs K position is a draw.
- (d) There is no parity (odd/even n) effect for n ≥ 4.

**Your job is to try to refute each claim.** Use a method that does not depend on T12's scripts.

1. **For (b) and (c), take the full KPK tables.**
   - Two KPK solvers already exist for cylinders: `research/kp_tablebases/` (see its `REPORT.md`) and
     `./kings/kpsolve --board cyl:NxR`.
   - Compute every legal K+P vs K position on C3, C4, C5, C6, C7 and C8 with 8 ranks (and C5 and C7 with 6
     ranks, if cheap).
   - Classify each by the kings' relation:
     - same file, two ranks apart (direct opposition);
     - adjacent files, two ranks apart (diagonal);
     - other.
   - Count W, D and L for each side to move.
   - (b) is false if any direct-opposition position is not a draw. Give the first 5 counterexamples, with
     FENs and the board.
2. **For (a),** recompute the 5.1 pattern with `kpsolve` on C4–C9, R = 5–8, and check legality by hand. A
   position is illegal if the kings are adjacent, including across the seam.
3. **For (d),** compare the outcome statistics of odd and even n from step 1, such as the % of White wins and the
   number of mutual zugzwangs. Report any difference that is not explained by the number of squares.

**Limits.**
- `kpsolve --threads 2`, under `nice -n 10`.
- At most 2 processes at once.
- Each job under 40 minutes.

**Deliverable** (`REPORT.md`):
- a verdict for each of (a)–(d): CONFIRMED (CHECKED-2), REFUTED (with counterexamples) or UNCLEAR;
- the tables;
- reproduce commands.
