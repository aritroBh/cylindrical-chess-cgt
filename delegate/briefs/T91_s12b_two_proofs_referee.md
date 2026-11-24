# T91 — Referee of two condensed proofs (new supplement Section S12.2, items A.18 and A.19)

Output directory: `delegate/out/T91/` (create it). Write `REPORT.md` there. Do not edit anything else. Never run
git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs you started and recorded
yourself. At most 1 process at a time, under 3 GB RSS, `nice -n 15` if your sandbox allows it; total compute
budget about 15 minutes. Other people's jobs run on this machine: leave them alone. Do not copy raw terminal
transcripts into your report, and do not write anything from your own memory of other projects or any personal
identifier into it.

## Text
`dist/tog/supp_src/s12b_extra.tex` (261 lines; a typeset copy is `delegate/out/W7_two_proofs/build/test_s12b.pdf`).
It was written by a model of another vendor as a condensation of two results of the working note
`dist/tog/supp_src/s12_kings.md`: Theorem 3.4 (line 1636 on, with Definitions 1.1-1.3 at lines 42-70 and
Definition 3.1 at line 1564) and Proposition 2.11 with Corollary 2.11a (lines 1306-1420). The 47-page note is
being removed from the journal supplement; the new text must stand alone, together with
`dist/tog/supp_src/s12a_core.tex` (items A.1-A.17, which it may cite). It will be read by journal referees.
The writer's own account of what it changed is `delegate/out/W7_two_proofs/REPORT.md`.

## What to decide
1. Read A.18, A.18a, A.18b, A.19, A.19a, A.19b line by line as a hostile referee. For each definition: is it
   complete and unambiguous? For each proof step: sound / gap / false, with the missing argument or a
   counterexample. Small counterexamples by a short program of your own are welcome (say what it computes).
2. Theorem A.18a (outcomes with waiting moves). Check in particular: what exactly a pass is and who may pass
   when; whether "every other move in Z loses" is used correctly; finiteness and the explicit move bound when
   only one side can wait; the draw case when both can wait (does each side really have a strategy that never
   loses?); the case where the side to move has no move except a pass; whether en passant rights or any other
   hidden state are affected by a pass and whether the text says what it assumes.
3. Proposition A.19 (frozen-king passer test) with hypotheses (H1)-(H5). Check in particular: en passant; a
   capture by an enemy pawn onto the passer's file or path, or a capture that creates a faster enemy passer;
   checks and stalemate with frozen kings; the move count and who moves first (off-by-one); promotion to pieces
   other than a queen; the cylinder wrap and the statement for flat boards (the note proves the cylinder case and
   says the flat case is the same: is it?).
4. Does A.18a imply this statement, as A.18b claims? "Let the components form a short game in which every
   decisive event ends the game, let a side that can wait pass at any time, and let every other move in Z lose.
   If only white can wait, black wins exactly when it can force a decisive event in its favor against a passing
   white, and white wins otherwise. If both can wait, a side wins exactly when it can do so against a passing
   opponent, and otherwise the game is drawn."
5. Does A.19 with A.19a imply this sentence? "For (V2) we prove a local test only with frozen kings: a passed
   pawn then wins the frozen-king game if, besides conditions on checks, stalemates and its own nearby pawns, its
   path is empty and no enemy pawn, passed or not, can promote first."
6. Is every item the text cites from s12a_core.tex (A.n) used as that item is actually stated there?
7. Compare with the note: did the condensation drop a hypothesis, strengthen a conclusion, or present as proved
   something the note marks as computed or conjectured?
8. Wording: any sentence that is ambiguous, any symbol used before it is defined, anything that reads like a
   working note.

## Report
`delegate/out/T91/REPORT.md`: a verdict for each of A.18-A.18b and A.19-A.19b (sound as printed / sound with
wording fixes / mathematical error), then numbered findings with the line of s12b_extra.tex, the quoted sentence
and an exact replacement. Separate mathematical points from wording. Say what you did not check.
