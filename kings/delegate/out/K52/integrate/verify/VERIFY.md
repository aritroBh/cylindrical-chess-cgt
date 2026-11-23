# Referee report on the K52 integration edits (K51 + K52 into kings/theory/LOOPY.md), 2026-11-23

Scope: `../EDITS.md` (26 edits), `../findings.txt`, the integrator's scripts. LOOPY.md not edited (md5
c5a83e4f7c43b521fc36568f862f8b22 before and after). Replacement set: `EDITS.md` here (29 edits).
Own evidence: `ref.py` / `ref.out` (separately written pawn rules, whole-board D, unfolded S as F with token
counters, τ_P, scored τ, HSS, (E), stopped tempo counts; cylcgt only as a final cross-check).

**Overall: ACCEPT WITH FIXES.** No mathematical error found in the edits. Fixes are wording, provenance and
leftovers; three edits added.

## a. The quiet-move proof (EDIT 12, as written): SOUND WITH FIX

Re-derived line by line against `cylcgt/pawns.py` (`passed`, `ep_capturable`, `moves`, `_value`, `_child`,
`promote_distance`).
- What is used: + ∈ τ_P(Z) (the post-move Z is reachable in Z's game and has a White passer); (HSS) at Y gives no
  − in any C of Y″; (B) at Y gives B > Σ_{C∈Y″} M_R(C) since M of a sum is the sum. Correct.
- Rights. The text said "by (E) [at Y] no right in Y is usable". F can keep older rights in Y″ that D has dropped;
  those are covered by (E) at the position their double step led to (that position had ≥ 2 components, else the
  next move would have been in the same component and replaced the right), and the component is unchanged since.
  Not a gap (E is assumed everywhere) but the instance cited was wrong. **Fixed** (EDIT 12, and EDIT 14's "(E) at
  Y itself").
- Unusable right ⇒ no e.p. capture and no protection from the e.p.-aware test: both need an enemy pawn beside the
  double-stepped pawn on its rank (`ep_capturable`, `moves`). Correct.
- Step 1 (legality in the D-game of C): pushes use one file; captures land on a file holding an enemy pawn, so a
  daughter's file set only shrinks and the separating empty files stay empty, also after a sister freezes and its
  pawns leave F. So a parked daughter is never adjacent to a played one. Correct. A capture of a pawn in a sister
  daughter is impossible for the same reason (target file is adjacent, hence in the same daughter).
- Step 2: the moved daughter is tested by F with the right the move set or dropped, which is D's right; other
  daughters' pawns and neighbours are unchanged; the only rights F keeps and D drops are post-frontier Black
  double-step rights (only these can make a Black pawn passed; `ep_capturable` with side B) and unusable older
  ones (no effect). So a first terminal P_k is Black-only and reached by a Black move: − ∈ τ_P(C) and − ∈ τ(C).
  Correct. An e.p. right created by Black's own double step in the projected play is exactly this case.
- Step 3 (sign of a freeze, including a race): White's passers and distance in P′ equal those in the moved
  daughter (`promote_distance` tests each pawn against all enemy pawns, which in other daughters are ≥ 2 files
  away; "front pawn" is per file; the right is the same); extra Black passers only lower Black's distance; the
  mover is Black in both; so a Black credit in F is a Black credit in P′ under count, mover and opponent rules.
  Correct.
- Count: quiet moves of C are a Black-only sequence through non-terminal positions, ≤ M_R(C); q < B; White to
  move has made ≤ q + f moves; tokens ≥ (B − q) + f(B − 1) ≥ 1. White's token moves never touch the pawns.
  Finite play (pawns advance, finite tokens), Black runs out. Correct.
- M stops at the first terminal: harmless, the projection passes none (wording tightened). (B) at the
  pre-freeze Y is exactly what (B) provides (Y is a D-position before the first event). Correct.
- Several splits: handled; daughters never merge. Colour reverse: rules are colour-symmetric.
- N(X) bullet: true, but "step 3 is still needed ...; this is the route of the appendix A.6" misattributes: the
  appendix (`dist/tog/supp_src/s12a_core.tex`) gets the sign from the inheritance Lemma A.5 and the count from
  A.6 with N(X). So A.6 has no sign gap (findings.txt §2 left this open). **Fixed.**

## b. Witnesses and the 1.14(i) root

- Witness 1 (flat 5×7, `W a4 b3 e2 / B a5 b4 e4`, Black's right on a3): hand-checked. a/b: White has no move, Black
  only b4×a3 e.p. giving a passer, so { | −B} = −B − 1; e-file {0 | 0} = *; −B − 1 + * is 𝓡 for B ≥ 1. D: White
  first e2–e3, right lapses, Black has no move; Black first takes e.p. So 𝓝. Root and predecessor `W a2 b3 e2 /
  B a5 b4 e4` passer-free under both tests. **PROVED justified.** `ref.py`: o(F) = 𝓡 (BIG 9 and 256), o(D) = 𝓝,
  HSS(τ_P) and HSS(scored) true, (E) false, tempo max 2, under all six settings; cylcgt agrees.
- Witness 2 (`W a4 b2 b3 e2 e4 / B a5 b4 b6 e6`, same right): e-file {2 | 1} checked by hand; the rest by
  `ref.py`: o(F) = 𝓝, o(D) = 𝓛, HSS true, (E) false, tempo max 8, all six settings. COMPUTED-1 was justified;
  with `ref.py` it is now CHECKED-2 (cylcgt + `common` vs a separately written implementation). Upgraded.
- 1.14(i) root `Ka1 ka6 Pc2 Pd4 pd3 b -` (cyl 8×6): d4 passed, d3 blocked by c2, so D credits White at the root;
  d3–d2 then d2–d1; White needs two moves to promote, c2 cannot take d2, the king on a1 cannot reach d1/d2 in one
  move, and no White move gives check (pawn attacks c6/e6, b4/d4, b5/d5; a6 untouched). Black wins P. PROVED.
- Also confirmed by `ref.py`: (HSS)-necessity `W a4 d4 / B b5 e5` (𝓟 vs 𝓝, all three rules, (E) and tempo ok),
  (B)-necessity B = 1 (𝓡 vs 𝓝) and 4×263 D = 𝓝, M example (one component M_B = 1; daughters 1 + 1), τ example
  (τ_P = {+, −}, scored {+}); one-component race root `W a5 / B b4` raises RaceError, `W a2 / B h7` gives 0.
- EDIT 5 cited `verify.out` for `W a5 / B b4`; verify.out has `W b2 / B d6` passed to `_value` (two components).
  Citation **fixed** to `ref.out`.
- EDIT 10 cited the K52 census (no failing-(E) root with ≤ 2 + 2 pawns) as evidence for the OPEN question. With ≤ 4
  pawns (E) cannot fail at all (usable right needs 3 pawns in a passer-free component, a second component 2 more),
  so the census is vacuous there. **Fixed.**

## c. τ_P

- Every τ_P statement is true: Definition (any-order, root included, stop at passers, race gives both) equals
  `common.threats` and `notes/lemmas.md` Definition 2.0; τ ⊆ τ_P; strict at `W b2 d6 / B c7`; τ_P monotone.
  (HSS) of 1.11(c) and (V4) of 1.14 with τ_P: true by the proof. The scored-τ variant of (c) (EDIT 9): true, the
  proof only uses the credited sign (steps 2 and 3 produce an option into a Black-credited terminal).
- Scored τ unaffected: Theorem 1.11(b), Proposition 1.12, Theorem 3.8, Corollary 3.8b, §4 use τ of abstract
  D-games, whose definition text is unchanged. 1.14(ii) has a stronger hypothesis now (τ_P ⊇ τ), still proved,
  and the scored version follows from EDIT 9's remark. P11's "HSS" is `hereditarily_safe`, now consistent.
- Direction. In LOOPY, τ_P *strengthens* (HSS)/(V4) (more threats, fewer qualifying roots) relative to the old
  scored-τ text, which is still what the supplement's mirror `dist/tog/supp/s12.tex` prints (it needs a rebuild).
  Relative to the appendix `s12a_core.tex`, whose threat is already the passer-colour one over the smaller
  play-reach Reach(X), the new (HSS) implies the appendix's HSS (A.3 remark). Nothing is weakened silently.

## d. Leftovers after the original 26 edits (line numbers in the edited file)

| line | text | status |
|---|---|---|
| 67, 501, 598, 603, 607 | "a race needs both threats", "moves of D", "M(Y) ≤ M(X)", "OPEN" | inside withdrawal notes or the new OPEN (rootless (E)); correct |
| 72, 731 | "tautology" | negated; correct |
| 90, 1985, 2304 | "always G-moves", "never passes" | quoted as withdrawn; correct (2567 "If Black never passes" is unrelated) |
| 244 | "every board height" | quoted; correct |
| 301, 352 | "computes P" | correct (F, not P); 3148 "it computes P, not C" is another solver, correct |
| 71 | T1.14(ii) row "with the corrected τ" | now inaccurate (τ_P); **EDIT 27** |
| 422–424 | reason for any-order reach cites the withdrawn split-prefix argument; "threats computes it" | stale; **EDIT 28** |
| 638 | "(HSS) ... uses the either-player τ" | now wrong (τ_P); **EDIT 29** |
| 74, 75 | (V1a) clause (E) "stays a CONJECTURE"; P1.15 "(E) can be dropped when (HSS) holds" bounded | about chess (V1a) in the searched boundary; still correct |
| 198 | T1.11 summary "a threat is a move into a terminal by either player" | true for (a)/(b) and for the scored-τ form of (c); left |

## e. Labels and status rows

- PROVED: witness 1, (HSS)/(B) B = 1 necessity, 1.14(i) root, K51 example, quiet-move proof: all re-derived here.
  Engine results COMPUTED-1 or CHECKED-2 as stated.
- EDIT 1 said "re-derived step by step by the integrator" and "Read by Codex ...: true with its hypotheses", which
  could be read as Codex having checked the new frontier text. **Fixed**: Codex read the statement and the earlier
  proof (theorem true, old frontier a GAP, census COMPUTED-1) and sketched the argument; it has not read the
  printed text. Same note in EDIT 12. EDITS 2, 3, 4 correctly report what Codex read. K51's 22.5M count stays
  CHECKED-2 as K51 labels it (two solvers written for the check; not re-run here).

## f. Apply check

Copy of LOOPY.md in the scratchpad: original set 26 applied, 0 rejected; replacement set 29 applied, 0 rejected;
cell counts of every table row unchanged (row-by-row diff of `$2|NF`).

## Verdict per edit

| EDIT | verdict |
|---|---|
| 1 | ACCEPT WITH FIX (Codex scope; witness 1 CHECKED-2; referee re-derivation) |
| 2, 3, 4 | ACCEPT |
| 5 | ACCEPT WITH FIX (citation) |
| 6, 7, 8, 9 | ACCEPT |
| 10 | ACCEPT WITH FIX (CHECKED-2 for both witnesses; census remark replaced by the ≤ 4-pawn argument) |
| 11 | ACCEPT |
| 12 | ACCEPT WITH FIX (older rights and (E); stop-rule wording; N(X) bullet attribution; Codex scope) |
| 13 | ACCEPT |
| 14 | ACCEPT WITH FIX ("(E) at Y itself") |
| 15–26 | ACCEPT |
| 27, 28, 29 | new (leftovers) |

Not re-run: K52 census (32,880), K51 comparisons (22.5M). After LOOPY changes, rebuild `dist/tog/supp/s12.tex`.
