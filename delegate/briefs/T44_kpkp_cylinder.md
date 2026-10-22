# T44: king and pawn against king and pawn (KPKP) on the cylinder, analysed (light to moderate compute)

**Output directory:** `research/kpkp/` (only add new files; do not delete or overwrite existing ones).

The solver runs are done. `research/kpkp/kpkp_cyl.out.zst` and `kpkp_flat.out.zst` hold `kings/kpsolve`
results for every KPKP position on the 8×8 cylinder and the ordinary 8×8 board. Read them with
`zstdcat FILE | head`. Read `kings/SPEC.md` for the output format: `pos | A B` gives lower and upper bounds,
exact when A == B, values in White's view. `research/kpkp/analyze_kpkp.py` is an unfinished analysis script;
`kpkp_*.err` hold the run settings.

**Task:**
1. **Settings.** Check from the `.err` files and SPEC which promotions and caps were used, and say how many
   positions are exact.
2. **Statistics.** For each board give legal positions with each side to move, and White wins / draws / Black
   wins. Also give the positions whose result differs between the boards. Pair positions by the same squares;
   count changes in each direction.
3. **Mutual zugzwangs.** Count positions where the side to move does worse than the side not to move, on each
   board. Give a few cylinder-only examples, including any where a pawn race across the seam decides.
4. **Spot check with a second program.** Re-solve at least 200 random positions from each board with the
   independent reference solver `kings/ref/solve.py` (read `kings/ref/test_ref.py` for usage), plus 20 of the
   cylinder-only mutual zugzwangs. Report agreement (CHECKED-2 if all agree).
5. **Rules:** at most 2 processes, nice -n 15, under 4 GB each. Stream the `.zst` files; never write an
   uncompressed copy over 500 MB.

**Report** (final message): a short table suitable for a paper, the examples with FEN, the labels, and
reproduce commands.
