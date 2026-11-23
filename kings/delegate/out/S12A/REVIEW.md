# Theorem 1.11(c): two proof gaps repaired (integrated 2026-11-23)

Source: the paper's self-contained proofs appendix (`dist/tog/supp_src/s12a_core.tex`, Lemmas A.4 and A.5) and two
independent referees of it. Both gaps were found by the appendix author and confirmed by a referee who re-derived
A.1–A.7; a second referee confirmed gap (i) while checking A.11–A.17.

- **(i) Frontier step.** "Every integer frozen later is +B" used that re-split components inherit "no − threat".
  Definition 1.10's monotonicity is about one fixed D-game and does not cover it. It holds because a split is
  always made by a capture, which leaves no e.p. right. Now proved in place.
- **(ii) Condition (E).** The step "both models give the child", and the opponent's move count after the frontier, use
  (E): the sum model keeps an e.p. right with its component, the whole-board game drops it after one move. (E) is now
  a hypothesis of Theorem 1.11(c). Every use goes through Theorem 1.14, whose (V1a) already contains (E). Whether (c)
  holds without (E) is OPEN (no counterexample among 137 sampled roots that fail (E); COMPUTED-1, one run).

`EDITS.md` (7 edits): 7 applied, 0 rejected, table cell counts unchanged. The repair is one AI derivation, agreeing
with the appendix's Lemmas A.4 and A.5; a referee outside the Claude family is planned for the appendix.
