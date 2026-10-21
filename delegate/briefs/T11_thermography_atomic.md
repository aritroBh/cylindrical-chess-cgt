# T11: thermography and atomic weights of pawn endgames (no prior study exists)

Output directory: `research/thermo/`.

**Inputs:**
- `atlas/flat8/values_aware.jsonl.gz`: e.p.-aware values; flat, widths 1-4, <= 6 pawns;
- `atlas/cylinder/` (read its REPORT.md): textbook values, cylinder and flat, widths 3-8.

Recompute values with `cylcgt` (current default: e.p.-aware) wherever you need exact game objects.

1. **Thermography.** For every BIG-free value, find its mean and temperature (`cylcgt.cgt` has thermograph tools). Report:
   - the temperature distribution by width and pawn count;
   - the hottest positions;
   - whether the cylinder is hotter or colder than the flat board on average;
   - the "orthodox" first moves of the hottest positions.
2. **Atomic weights.** For every infinitesimal (all-small) value, compute its atomic weight (Conway / Berlekamp–Conway–Guy atomic weight calculus; ↑ has weight 1, ↑* weight 1, ⇑* weight 2, ↑² weight 0, and so on).
   - Implement the atomic-weight algorithm and validate it on at least 15 textbook values.
   - Report the weights that occur, which ones are cylinder-only, and the "two-ahead rule" outcomes they imply.
3. **Mean value under sums.** Check that sums of components follow the mean-value theorem.
4. Give exact reproduce commands. Label every claim COMPUTED-1, CHECKED-2 or PROVED.

Write `research/thermo/REPORT.md`.
