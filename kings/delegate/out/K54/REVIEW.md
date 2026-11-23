# K54 review: Codex read of the new 1.11(c) frontier proof and the corrected Theorem 2.7 (2026-11-23)

Codex (OpenAI Codex CLI v0.169.0, model gpt-6.2-astra) read both texts as printed at commit 62ae99cc
(`FINDINGS.md`, `REPORT.md`, scripts, `height6.txt`, `height7.txt`).

- Theorem 1.11(c), quiet-move frontier: every step SOUND (repeated splits, the stopped tempo bound, all three race
  rules). Both no-(E) witnesses confirmed.
- Theorem 2.7(a), Steps 5 and 6, the reply-mate example and its variant: SOUND.
- Wording corrections, verified by one agent and applied (`integrate/EDITS.md`: 11 applied, 0 rejected, cell counts
  unchanged): the tempo bound is (H − 2)p, at most 6p only for H ≤ 8 (two places); the right inherited from the root
  in the frontier step; a witness for the strictness of B > N(X) over (B) (flat 2×7, `W a2 / B b3`); Theorem 2.7 Step 1,
  where a projected pass also ends an older projected e.p. right.
- New evidence on whether (E) can be dropped at a root with no right (COMPUTED-1, one implementation, not re-run):
  right-free, passer-free 3 + 3 roots on five files and six or seven ranks, three race rules: 48,576 comparisons, 0
  disagreements, 12,600 of them with a later failure of (E). The unrestricted question stays OPEN.

The raw CLI transcript is not committed.
