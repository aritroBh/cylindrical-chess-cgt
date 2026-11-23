# Core proofs appendix: notes

File written: `dist/tog/supp_src/s12a_core.tex` (LaTeX fragment, starts with `\subsection*{The Four Main Results, Self-Contained}`).
A standalone test compile (tectonic, the supplement's fonts and packages, `macros.tex` and `supp/mainlabels.tex`; done in the
session scratchpad, not in the repository) gives no errors, no undefined references and no overfull boxes: about 5.3 pages.
The paper was not built. Nothing else in the repository was changed.

Numbering in the appendix: A.1 Lemma (files), A.2 Lemma (no promotion, potential, H >= 6), A.3 Remark, A.4 Lemma (what (E) gives),
A.5 Lemma (threats are inherited), A.6 Lemma (frontier), A.7 Theorem (sum safety), A.8 Prop. ({B|0}+{0|-B}=0),
A.9 Remark (move bound 168 < 256), A.10 Lemma (buffer), A.11 Theorem (validity), A.12 Remark, A.13 Corollary,
A.14 Prop. (prop:sumcounter), A.15 Remark, A.16 Theorem (certificate), A.17 Remark.

## Status of the four results

1. **Theorem `thm:validity` (A.11): COMPLETE WITH A SHARPENED HYPOTHESIS.**
   - Added: X (the context) has no passed pawn. Without it W(X) is not defined. Implicit in the main text.
   - The proof is direct in chess: (V2) and (V3) are stated in chess in the main text, so no (A_Q) bridge from P to C is
     needed (S12's Theorem 1.14 proves P(X) = D(X) and gets C only under (A_Q); the main text's chess form is the right
     one given its chess hypotheses). The same proof works verbatim for P and for the frozen-king game F (Remark A.12(b)).
   - The check clauses of (V1) are not used by the proof (Remark A.12(a)); keeping them is harmless.
   - (E) is not needed here: (V1) compares chess with the whole-board W(X), whose e.p. rights lapse as in chess. In S12,
     (E) enters (V1a) only because S12's D-model keeps rights per component.

2. **Corollary `cor:v4` (A.13): COMPLETE WITH A SHARPENED HYPOTHESIS** (those of A.11 and A.7: X has no passed pawn; local
   race rule; H >= 6 under the e.p.-aware test). Proof: A.11 + A.7.

3. **Certificate statement (A.16, "In the promotion game ... such a move loses for its mover"): PROOF COMPLETE** for the
   precise definition (C1)-(C3) = S12's (L1_P), (L2), (L3) of Definition 2.6, form (a) of Theorem 2.7. The main-text
   definition is a loose paraphrase (Remark A.15): the count starts after a reply r in Z that keeps the punisher's king on
   F_Z; clause (i) is a local game with the context deleted, the defender may pass, and the punisher's king is confined to
   F_Z; "no defender pawn" means the defender's context pawns moving alone with the punisher's king and all Z-pawns
   deleted; the stalemate clause is along a guided strategy. The queen-safety clause of S12's (L1) is not needed in P.
   In form (a) the e.p. clause of (L2) is vacuous (Q's only possible right comes from r, on F_Z), so (C2) is stated without e.p.

4. **Theorem `thm:hss` (A.7): COMPLETE WITH A SHARPENED HYPOTHESIS.**
   - Added: X has no passed pawn; the race rule is local (depends only on the passed pawns, their and neighbouring files,
     and the mover; count, mover and opponent all are); and, under the e.p.-aware test, H >= 6. The last is needed for
     S(X) to be well defined: in a sum a player can move twice in a row in one component, and on a 5-rank board a pawn that
     double-steps to the rank before its last is not passed (it can be taken e.p.), so it could promote in S. All boards
     of the main text have at least six ranks, so no main-text change is needed.
   - Weakened (in the reader's favour): HSS and (E) are needed only at positions reachable by alternating play (Reach(X)),
     not "in any order"; threats are read as "reachable before the first passed pawn", the weakest reading. So the main
     text's statement follows under either reading of its threat definition.
   - The move bound is B > N(X), N(X) the largest number of moves of one side in any sequence of pawn moves from X; N(X) <=
     max(Phi_W, Phi_B) <= n(H-1)(H-2)/2 = 168 on boards up to 8x8 (Remark A.9: a hand proof of the main text's "with B = 256
     the move bound always holds on boards up to 8x8").

## Gaps found in the S12 proof and how the appendix repairs them

- **Theorem 1.11(c), frontier step: "every integer frozen later is +B, because a -B would need a - threat".** This uses
  monotonicity of threats under re-splitting (Definition 1.10, "tau(y') is a subset of tau(y)"). With the e.p.-aware test and
  "reachable without passing a terminal", monotonicity is not immediate: a pawn that just double-stepped and can be taken
  e.p. is not passed, and after a move in another part of the component it is, so a sequence through a split can pass a
  passed pawn early. Repaired by Lemma A.5 (an induction that builds the witness sequence move by move: a double step does
  not split a component, and a non-double-step leaves no right behind).
- **Theorem 1.11(c) compares S with a decisive-event game whose e.p. rights stay with their component**, not with the
  whole-board W(X) of the main text. The step S <-> W is where (E) is used. S12 mentions this only in Proposition 1.15(a).
  Made explicit by Lemma A.4 (under (E) a stale right allows no move, and a move elsewhere makes no pawn passed) and by its
  use in Lemma A.6 (the opponent never captures e.p. after the frontier, so its moves form a legal sequence and are
  bounded by N(X)).
- **S(X) with promotions** (H = 5, e.p.-aware): not addressed in S12; handled by the hypothesis H >= 6 (Lemma A.2(c)).
- No gap was found in the proof of Theorem 2.7(a); the appendix re-derives it in four steps (A.16) and drops the parts
  only needed for the window form (b).

## Assumptions marked as computer-checked

- None of the four results rests on a computation or on an assumed lemma.
- Proposition A.14(c) (prop:sumcounter: S(X) a black win whoever starts, W(X) a first-player win) is marked "checked by
  computer only, not proved here and not used here". Parts (a) and (b) of A.14, including that X is not HSS, now have a hand
  proof (h5-h6, a7xh6 splits X into {f,g,h} with a black threat and {b,c,d} with a white threat).

## Suggested main-text changes (optional; each replacement is no longer than the text it replaces)

1. `dist/tog/sections/04_kings.tex:59` (end of Theorem `thm:validity`)
   - current: `without draws, where $X$ is the position with $Z$ and its pawns deleted.`
   - replacement: `without draws, where $X$, the position without $Z$, has no passed pawn.`
   - reason: states the implicit hypothesis that X has no passed pawn (72 -> 71 characters).
2. `dist/tog/sections/04_kings.tex:83-84` (certificate sentence)
   - current: `if the punisher promotes within $h$ of its own moves against any defence, no defender pawn promotes that fast and the defender is not stalemated`
   - replacement: `if after a reply in $Z$ the punisher promotes in $h$ moves with the context removed, no defender context pawn is as fast and no stalemate occurs`
   - reason: the precise certificate counts after a reply in Z, deletes the context in clause (i), and counts only the
     defender's context pawns in clause (ii); the current wording reads as a statement about the real game, where it would
     be close to circular (144 -> 144 characters).
3. No change is needed in `05_sums.tex`. If wanted, the proof sketch of `thm:hss` (`05_sums.tex:65`, "The full proof, by
   induction with (E), is in Section~S12.") is accurate for the new subsection, which is the first part of S12.
