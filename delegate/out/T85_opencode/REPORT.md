SOUND WITH FIXES

Summary: The final text of s12a_core.tex (A.1-A.9) was read line by line as a hostile referee. No proof step in A.1, A.2, A.4, A.5, A.6, A.7 or A.8 was found to fail under the stated hypotheses, and an independent reimplementation of W and S on cylinders with 3-5 files, 5-6 ranks and at most 4 pawns (adopted e.p.-aware setting, 11,577 HSS/(E)-satisfying positions across six board sizes) found zero outcome mismatches. The main remaining issue is that the proof treats each position as having one en passant right, while the supplement's own sum model lets rights persist in components; condition (E) as stated may not control those persisted rights. A.7 implies the main-text theorem modulo this clarification and the sharper move bound N(X).

Findings:

1. dist/tog/supp_src/s12a_core.tex:124, :164, :170 — MAJOR — The proof assumes a single right of Y. The sum model stated earlier lets a right persist in a component while play moves elsewhere, so a later multi-component position can carry older rights in components other than the last-moved one. Condition (E) is stated over Reach(X) and is applied to "the right of Y" only; it does not obviously control those persisted rights. Proposed replacement for Lemma A.4: "For every right carried by a component D of Y (including rights persisted from earlier moves), S(D) with and without that right has the same options..." and for Theorem A.7/A.6 replace "the right of Y" by "every right carried by a component of Y", with (E) correspondingly strengthened (e.g. to positions reachable in the sum model, or by adding the invariant that all persisted rights are unusable).

2. dist/tog/supp_src/s12a_core.tex:62 — MINOR — The parenthetical justification of the e.p. clause in A.2(a) is too terse for the 4-rank case. Proposed replacement: "It fails the e.p. clause only if it has just double stepped with an enemy pawn beside it; on a 4-rank board that enemy pawn would stand on its own first rank, and on more ranks a double step cannot end on the last rank, so neither case occurs."

3. dist/tog/supp_src/s12a_core.tex:117 — MINOR — The claim that Reach(X) is smaller than the main text's set of positions is stated without the reason. Proposed replacement: "Definition ... and Theorem ... quantify over positions reachable by moves of either side in any order; Reach(X) is the subset reachable in alternating play, so our HSS and (E) are implied by, and no stronger than, the main text's."

4. dist/tog/supp_src/s12a_core.tex:186 — MINOR — The sentence "If Y has two or more components, Lemma A.4(a) lets us drop the right of Y from the summands S(D) without changing them" should also state the one-component case: when Y has one component there is no other summand and no persisted right to drop.

5. dist/tog/supp_src/s12a_core.tex:209 — MINOR — The move-bound formula is correct; no change required. (Recorded as checked.)

A.7 vs. main text, hypothesis by hypothesis: no passed pawn (same); HSS (main text quantifies over a larger set of positions, so its hypothesis implies the supplement's); condition (E) (same, modulo the persisted-right clarification above); BIG exceeds the number of moves (main text's "any sequence of pawn moves" is the looser phrasing; the supplement's N(X) counts sequences that continue past passed pawns, so BIG>N(X) is the sharper sufficient condition). The precise form's "for each side to move first" and "local race rule" are the only additions, and both are licensed by the main text.

Commands to rerun the independent check (from the project root, with PYTHONPATH=. not needed; use the venv python):

  for n in 3 4 5; do for H in 5 6; do nice -n 15 .venv/bin/python delegate/out/T85_opencode/solver.py --n $n --H $H --ep 1 --maxpawns 4 --out delegate/out/T85_opencode/res_${n}_${H}.json; done; done

  nice -n 15 .venv/bin/python delegate/out/T85_opencode/solver.py --n 5 --H 6 --ep 1 --race opponent --maxpawns 4 --out delegate/out/T85_opencode/res_5_6_ep1_opp.json

Observed: 11,577 positions satisfying HSS and (E) across the six board sizes, zero mismatches; 4,641 positions for the opponent race rule, zero mismatches. Result files: res_3_5_ep1.json, res_3_6_ep1.json, res_4_5_ep1.json, res_4_6_ep1.json, res_5_5_ep1.json, res_5_6_ep1.json, res_5_6_ep1_opp.json.

Not checked: A.10-A.17 and the king-group validity material; the count race rule (only mover and opponent rules were implemented); positions with more than four pawns or outside 3-5 files and 5-6 ranks; rings were included but not separately reported; arbitrary-order reachability beyond alternating play; accumulated/persisted rights in the sum model (the solver persists rights, but the (E) filter follows the proof's single-right reading); and any use of the tablebase. The solver is in delegate/out/T85_opencode/solver.py.