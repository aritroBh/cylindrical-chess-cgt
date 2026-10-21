# T14: Dawson's chess on new surfaces, and misère on the cylinder

Output directory: `research/dawson_variants/`.

**Context:** `dawson/REPORT.md` covers:
- normal play = octal 0.137;
- the cylinder ring rule R_n = mex{g(n-3)};
- the misère partial quotient (order 638 for strips <= 32).

1. **Misère cylinder.** Prove or refute that the misère ring's first player wins iff the strip of n-3 files is a misère P-position. Compute misère ring outcomes for n <= 100 with the existing C code (`dawson/`, read-only; copy if needed), and look for periodicity.
2. **New surfaces.** Define Dawson's chess on a 3×n Möbius strip (twisted seam: a pawn crossing the seam becomes the other colour's direction — choose and justify a convention) and on a 3×n torus-like ring of two rows. Solve them directly from the pawn rules for n <= 16 (normal and misère) and identify any octal or other closed form.
3. **Wider boards.** Dawson's chess on 4×n and 5×n boards and cylinders (extra empty ranks) for small n: does any simple rule survive?
4. Label every claim PROVED, CHECKED-2 or COMPUTED-1.

Write `research/dawson_variants/REPORT.md`.
