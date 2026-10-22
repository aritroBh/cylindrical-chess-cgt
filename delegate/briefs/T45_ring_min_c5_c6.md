# T45: second program for the ring \*2 minimum on C5 and C6 (moderate to heavy compute)

**Output directory:** `research/ring_min_c5c6/`. Write everything there.

**Claims** (from our C scanner; one program so far):
- On C5 the first ring \*2 has 8 pawns: no ring with at most 7 pawns is \*2, and there are exactly 14 eight-pawn
  ring \*2 positions (see `research/star3_hunt/` and `research/star26_rings/` summaries for the scanner's list).
- On C6 no ring with at most 8 pawns is \*2, and the nine-pawn ring \*2 positions are exactly six: three, among
  them `W a4 c4 d2 e2 / B b6 b7 d6 e5 f6`, and their colour-reversed twins.

**Method:** `research/ring_min_independent/ring.c` is an independent ring solver (written from the rules by a
different agent; it does not share code with the scanner). It handles C3 and C4. Extend it, or write your
own, to C5 and C6, keeping it independent of `research/star26_rings/` and `cylcgt/`. Read
`research/ring_min_independent/REPORT.md` for its rules and the default setting (count rule, e.p. on, e.p.-aware
test). Then enumerate every ring on C5 with 5–8 pawns and on C6 with 6–8 pawns (and 9 if it fits in the
limits), up to rotation and reflection, and count \*2.

**Limits:** at most 2 processes, nice -n 15, under 4 GB each; split into chunks; bounded memo tables that
replace entries when full. Compress any output over 100 MB with zstd once it is summarised.

**Report** (final message): counts by pawn number, the \*2 lists, agreement with the claims (CHECKED-2 if
so), runtime, reproduce commands.
