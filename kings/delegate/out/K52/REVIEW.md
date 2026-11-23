# K52 review: Codex read of Theorems 1.11(c) and 1.14, and the integration of K51 and K52 (2026-11-23)

Codex (OpenAI Codex CLI v0.169.0, model gpt-6.2-astra) read both theorems as they stood after the repairs of
2026-11-23 (`FINDINGS.md`, `REPORT.md`, `check.py`, `examples.py`). Verdict: both statements hold; the printed proof
of 1.11(c) had a gap in its tempo step; (E) cannot be dropped; several sub-assertions were false.

Integration: one agent verified every Codex claim (by hand and in `cylcgt`) and drafted 26 edits
(`integrate/EDITS.md`, `integrate/findings.txt`); an independent referee re-derived the new proof, re-checked the
examples with its own implementation (`integrate/verify/ref.py`) and wrote a replacement set of 29 edits
(`integrate/verify/EDITS.md`, `VERIFY.md`). Applied: 29 applied, 0 rejected, table cell counts unchanged.

- **Theorem 1.11(c), proof.** The frontier step is replaced by the quiet-move argument: project the opponent's later
  play onto each component live at the frontier, omit its freezing moves; the quiet moves are a legal sequence in the
  stopped D-game of that component, so at most M of them; each freeze supplies a fresh +B (the sign follows from
  (HSS)). It needs only (B) as stated. Withdrawn: "a race needs both threats", "M(Y) ≤ M(X)" for re-split Y, "its
  moves are moves of D". Codex read the statement and the earlier proof and sketched the argument; it has not read
  the printed text.
- **(E) cannot be dropped** (PROVED by hand; CHECKED-2 in two implementations, both passed tests, three race rules):
  flat 5×7 after a2–a4, `W a4 b3 e2 / B a5 b4 e4`: o(S) = 𝓡, whole board 𝓝. Second witness on the chess turn:
  `W a4 b2 b3 e2 e4 / B a5 b4 b6 e6`, Black to move, S = 𝓝, whole board 𝓛 (CHECKED-2). Still open: whether (E) can
  fail only later, at a root with no right.
- **Threats.** τ_P (passer-colour) is defined for pawn positions and is what `hereditarily_safe` checks; (HSS) and (V4)
  use it. Definition 1.10's scored τ is unchanged for abstract D-games.
- **Theorem 1.14.** (i) needs a root before the first decisive event (cyl:8×6 `Ka1 ka6 Pc2 Pd4 pd3`, Black to move: D
  credits White, Black promotes first in P). (iii) is not a tautology: (A_Q) is one-way, so it needs (i).
- **Theorem 3.4 (K51).** "So Left's winning moves are always G-moves" was false; now "some winning G-move exists".
  Lemma B's title and the sentence after it are corrected the same way.
- Not re-run: K51's 22,522,464 comparisons and K52's census of 10,960 roots. The raw CLI transcripts are not committed.
