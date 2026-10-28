# K13c: re-check the one-sided chess bridge after the K13b repairs

**Output:** `kings/delegate/out/K13/CHECK_68f3ebf.md`. Write only that file. Do not edit any other file. Do not run git.

You checked this bridge before (`kings/delegate/out/K13/CHECK_774036f.md`). The integrator then rewrote it twice (commits
567af10 and 68f3ebf). Read the current text in `kings/theory/LOOPY.md` (search "**Chess bridge** (PROVED after repair"),
the sharp form of Theorem 1.14 (search "Theorem 1.14, sharp form": (S1)–(S3) and the setting), Proposition 3.2,
Lemma 2.2, Definition 2.1, the e.p. remark after Proposition 3.2′ (search "Remark on e.p."), and Theorem 3.2‴ for
comparison.

Check, with a verdict for each (OK / PROBLEM with the exact fix):
1. Your three earlier points (terminal moves of Σ, the e.p. flag under the shuttle, "Black is not stalemated") are
   now handled correctly.
2. X, N and π are well defined, X ∈ N, and the conclusion "X is a P-win for White" is exactly what the sharp form gives.
3. (S1), (S2) and (S3) are each discharged correctly, including checks, a Black promotion, a Black Z-pawn move, a White
   ⊕, and a pass by Σ.
4. Anything still missing or too strong, and whether the label "PROVED after repair" (conditional on the stated
   hypotheses) is right.

Start the file with a 3-line summary. No computations are needed.
