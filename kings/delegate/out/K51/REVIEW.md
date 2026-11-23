# K51 review: blind proof of Theorem 3.4 by Codex (2026-11-23)

Codex (OpenAI Codex CLI; model not recorded) proved Theorem 3.4 blind (`PROOF.md`), then compared (`FINDINGS.md`): the
theorem holds as stated; every step of LOOPY's proof is SOUND except one sentence of (a), "So Left's winning moves are
always G-moves", which is false (X = {x}, L(x) = {⊕}, R(x) = ∅ with dud_D: the pass is a winning move). The correct
statement is that some winning G-move exists. Exhaustive test: 763,440 games, 22,522,464 comparisons, 0 disagreements.
The LOOPY sentence is corrected with the K52 integration. The raw CLI transcript is not committed.
