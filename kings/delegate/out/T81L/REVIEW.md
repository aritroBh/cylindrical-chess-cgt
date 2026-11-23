# Foundations check after Codex T81 (integrated 2026-11-23)

Source: a Codex referee report on the paper's proofs appendix (`delegate/out/T81/REPORT.md`) raised four points that
also concern this note. One agent checked LOOPY against each and drafted 9 edits; an independent referee re-derived
them, fixed five and added seven for later places that cite the edited items. `verify/EDITS.md` applied: 16 applied,
0 rejected, table cell counts unchanged.

- **Promotion convention (§1.1), now stated:** a pawn on its last rank stays a pawn and is passed under every test, as
  in `cylcgt`. No theorem needs a height bound. One statement does (PROVED by hand): for H ≥ 5, at a passer-free
  position whose e.p. right was made by the opponent, the side to move has no promoting move; false for H = 4
  (`W a2 / B b3`).
- **Order of operations in S, now stated:** test the whole moved component for passed pawns, score a race, split only
  if nobody is passed. Split-first is a different model (flat 8×8 `W b2 d6 / B c7`: after c7×d6, split-first gives 0
  where the engine and the whole-board game give a White win).
- **Theorem 1.11(c):** the root has no passed pawn (with passers of both colours in different components the engine
  gives 0 and (HSS) is vacuous).
- **Threats (Definition 1.10):** moves of either player in any order, in that definition and in Theorem 1.11.
- **Theorem 1.14:** restated per side to move. (V1)–(V3) can hold for one starter only (`Kb6 Pc7 / Ka8 Pa5`, empty
  context: hold with Black to move, fail with White to move). (ii) assumes (V4) and (E) on the any-order reach and a
  passer-free pawn part. The sharp form, the bridges and Theorem 3.2‴ were already per side.
- **Knock-ons:** status rows T1.11(c), T1.14(ii), the summary row T1.14, P11 (restricted to passer-free roots), §7 item 4.

Computed support (COMPUTED-1, one engine): 1,306 small roots on 4- and 5-rank boards, o(S) = o(W) at all.
