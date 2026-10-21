# T4 (opencode): rerun the cylinder atlas under the e.p.-aware test

Output directory: `atlas/cylinder/ep_aware/`.

The atlas in `atlas/cylinder/` (read its REPORT.md and scripts) used the textbook passed test. cylcgt now defaults to the e.p.-aware test.

1. Rerun the same enumeration with the current cylcgt: <=5 pawns, widths 3-8, cylinder and flat, count rule, e.p. on. Use the existing scripts by importing them or copying them into your directory; do not edit the originals. If the full run takes over 45 minutes, do widths 3-5 first.
2. Compare with the textbook atlas:
   - the number of values that change;
   - the cylinder-only value set before and after;
   - whether any *k (k >= 2) now appears or disappears on any cylinder;
   - whether the ring values 3/4, 1/4±1/4 and {3/2±1/2 | -3/2±1/2} survive.
3. Write `atlas/cylinder/ep_aware/REPORT.md`.
