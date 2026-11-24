# T89 — Hostile referee of the wall-ring proof itself (supplement Section S13)

Output directory: `delegate/out/T89/` (create it). Write `REPORT.md` there and any programs. Do not edit anything
else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs you started
and recorded yourself. At most 1 process at a time, under 3 GB RSS, `nice -n 15` if your sandbox allows it (if it
does not, run short checks anyway and say so); total compute budget about 20 minutes. Other people's jobs run on
this machine: leave them alone. Do not copy raw terminal transcripts into your report, and do not write anything
from your own memory of other projects or any personal identifier into it.

## Why
A mock journal referee pointed out that every ring result of the paper rests on Lemmas 1-3 of this text, and that
the text itself has been read only by models of the vendor that wrote it. You have refereed the written-out
Lemma 3 (`dist/tog/supp_src/s15_note1.md`, section 2b) and the transfer of Lemmas 1-3 to other families, but not
this text. Referee it now as a hostile reader, line by line.

## Text
`research/ring_family_proof/proof.tex` (126 lines; it is typeset as Section S13 of the supplement). It claims: the
wall rings G_n with n+3 pawns on the cylinder C_n have value *2 as whole-board games for every n >= 5 (outcome
against nim-heaps as *2), by Lemma 1 (reduction), Lemma 2 (wall pawns), Lemma 3 (insertion) and finite checks C1,
C2. The rules of the pawn game are in the text; the programs it cites are in the same directory, with logs in
`research/ring_family_proof/logs/`.

## What to decide
1. Definitions: is every object defined before use and unambiguous (the family G_n for each n and each parity, the
   pattern, "pattern file", "wall pawn", the reduced game, move classes, the cut c and ins_c, the zone, n_0)? Does
   the definition "a pattern file contains precisely its one starting wall pawn" make every later use correct?
2. Lemma 1, Lemma 2, Lemma 3: check each proof step. For each step say sound / gap / false, and for a gap give the
   missing argument or a counterexample. Pay attention to: en passant (flags, e.p. across the inserted files, a
   double step next to the cut), the passed-pawn test used (e.p.-aware), the race rule ("count"), which player a
   lemma is stated for, the case n small where the windows overlap or wrap around the cylinder, and both parities.
3. The induction: from the finite checks and Lemmas 1-3 to "every n >= 5". Is any width skipped? Is the base n_0
   justified? Does the step need a fact about a width that was not checked?
4. From the signature against heaps 0..3 to "value *2": what exactly is proved, and does the text claim more?
5. The finite checks C1 and C2: state exactly which programs computed what and for which n, from the logs. A
   sentence of the paper says the family is "checked by two programs for n < 17". Is that true for every n from 5
   to 16, and which two programs? If you can, recompute G_n + *h, h = 0..3, for n = 5..12 with a program of your
   own written from the rules in the text (not from the project's code) and compare.
6. Compare with `dist/tog/supp_src/s15_note1.md` section 2b (the long proof of Lemma 3): does the short proof here
   claim anything the long proof does not establish, or use a different hypothesis?

## Report
`delegate/out/T89/REPORT.md`: a verdict (holds / holds with fixes / does not hold), then numbered findings, each
with the line of proof.tex, the quoted sentence, what is wrong and an exact replacement text. Separate
mathematical errors from wording. Say plainly what you did not check.
