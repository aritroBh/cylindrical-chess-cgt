# K53 review: blind proof of Proposition 2.10(a) by Codex (2026-11-23)

Codex (OpenAI Codex CLI; model not recorded) proved Proposition 2.10(a) blind from a packet of definitions and the
statement (`PROOF.md`), then compared with LOOPY's proof (`FINDINGS.md`): every step SOUND; label "PROVED after
repair" kept, for the side to move, in a chess-legal non-terminal context, H ≥ 5.

- Its enumeration (COMPUTED-1): 145,444,720 context states on 5–8 ranks (3–5 files, flat and cylinder, at most 3 + 3
  pawns, both turns, with and without an e.p. target), 0 failures under either test; on 4 ranks 1,492 failures of 68,644.
- A note on LOOPY's side remark: of the 156 five-rank pairs quoted for the stronger either-colour claim, 120 have a
  legal double-step origin; the other 36 cannot arise.
- `test_differences.csv` is compressed (`.xz`); `compare.py` regenerates it. The raw CLI transcript is not committed.
