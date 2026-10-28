# K13 review: non-Claude re-check of the sharp form of Theorem 1.14 (integrated 2026-10-27)

**Outcome: accepted.** Codex (gpt-6-luna, max effort) wrote `REPORT.md`. The integrator applied
`EDITS_INTEGRATOR.md` (7 blocks, 0 rejected; table cell counts unchanged).

## What K13 did

- **Its own proof.** It re-derived the sharp form. It defines the attractor stages A₀ ⊆ A₁ ⊆ … of σ's winning
  region on the finite D, induces on the first stage, and uses (S1)–(S3) as the winner's step, the loser's step and the
  no-stalemate condition. The proof is in its own words: 15 of the report's 1,971 5-grams (0.76 percent) and none of
  its 8-grams occur in LOOPY's sharp-form section (lines 549–640 at 774036f~1; `overlap.py` in this directory).
- **Per-step verdicts.** Every step of LOOPY's proof is SOUND, including the check and checkmate cases.
  - The brief said that D is short, so the rank induction is well founded. K13 correctly marks that justification
    FALSE if asserted: D may be loopy, as G ⊞ on_D is.
  - LOOPY's proof does not assert it. It defines ρ as the stage of a least fixed point on a finite game, and that is
    enough. The status row now says so.
- **Uses.**
  - Corollary 2.7′ follows, in P. K13 builds its own D and N.
  - The one-sided chess bridge after Proposition 3.2 has a wording gap (next section).
- **No computations.** K13 ran none (they were optional). It left the old `kp` binary in `out/K13/` untouched; the
  integrator deleted it.

## The gap in the one-sided chess bridge (checked by the integrator)

The bridge's first hypothesis read "(V1a) every legal chess move of the side to move is one of the D-options of the
D-model". With D = G ⊞ on_D, Black has no move in on_D, so a legal Black Z-move is never a D-option. Read literally,
(V1a) therefore excludes exactly the moves that the second hypothesis ("every Black Z-move is decisively punished in
P") is about. It also asked that every legal White move be modelled, although White plays only Σ's moves.

Two further problems:
- The bridge's proof line still cited "the proof of Theorem 1.14(i)", although its own header said that the sharp form
  replaces that citation.
- Theorem 3.2‴ (the two-sided bridge, K14) already had the correctly scoped (V1a-ctx) and a sharp-form proof.

The integrator rewrote the one-sided bridge in the same way:
- (V1a) covers Σ's White moves and Black's context moves;
- the proof exhibits the White-certified set N and checks (S1), (S2) and (S3) one by one;
- the old wording is recorded in the text.

The bridge's mathematical content is unchanged. With the old wording it applied only in positions where Black had no
legal Z-move.

## Edits (`EDITS_INTEGRATOR.md`)

- the K9 caveat in the preamble;
- the status rows T1.14 sharp form, C2.7′, P3.2, and T1.14 in the second table;
- the label paragraph after the sharp form;
- the one-sided chess bridge;
- `kings/REPORT.md`: the K9 bullet now mentions K13.

## Files

- `REPORT.md`: K13's output, verbatim.
- Logs in `kings/delegate/logs/`:
  - `K13.log`: the successful run, 22:31–22:39;
  - `K13_codex_limit.log`: the 19:12 run, stopped by the usage limit;
  - `K13_codex_neterr.log`: an earlier run lost to a network error;
  - `K13_opencode_attempt.log`: an OpenCode attempt;
  - `K13_chain.out`.

## Post-commit check K13b (Codex, `CHECK_774036f.md`) and the follow-up commit

Codex checked commit 774036f. Its points and what was done (`EDITS_K13b.md`, applied: 3 blocks, 0 rejected, cell counts
unchanged):
- (S1) and terminals: a ⊕ prescribed by Σ has no matching position. (V1a) now asks for matching only when Σ prescribes a
  position; a ⊕ is closing by the decisive-event hypothesis. The same for Black context moves to a terminal.
- e.p.: a king shuttle ends an e.p. right, but the pass of on_D left G unchanged. G now carries the e.p. flag as a
  coordinate and the pass resets it, as in the e.p. remark after Proposition 3.2′; condition (E) is stated for both
  sides' context moves.
- (S3): "Black always has a legal move" also excluded checkmate, a White win. It is now "Black is not stalemated".
- The stale sentence after the sharp form ("its proof cites the proof of (i)") now says that the earlier proof did.
- `kings/REPORT.md` said the bridge "uses the scoped form of Theorem 3.2‴"; it now says that it has scoped hypotheses, as
  Theorem 3.2‴ already had, and a proof by the sharp form.
- The overlap statistic now has a script, `overlap.py`.
- Codex's S2 coverage argument (every Black move before promotion is a context move or a Z-move) is now in the proof.

## Second re-check K13c (Codex, `CHECK_68f3ebf.md`, 2026-10-28)

After the rewrites in 567af10 and 68f3ebf (the latter defines the root X and puts X in N), Codex re-checked the bridge.
- K13b's three points are now handled correctly.
- X, N and π are well defined, and the conclusion "X is a P-win for White" is exactly what the sharp form gives.
- (S1), (S2) and (S3) are each discharged, including checks, Black promotions, Black Z-pawn moves, a White ⊕ and a
  pass by Σ.
- The label "PROVED after repair", conditional on the stated hypotheses, is right.

One wording point: shuttle legality comes from the hypothesis of Proposition 3.2. Lemma 2.2 only secures it against
context pawns. The text now says so.
