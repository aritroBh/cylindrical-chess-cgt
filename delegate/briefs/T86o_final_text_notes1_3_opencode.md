# T86 — Hostile referee read of two FINAL proof notes (supplement S15, Notes 1 and 3)

Output directory: `delegate/out/T86_opencode/` (create it). Write `REPORT.md` there and any programs. Do not edit
anything else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs
you started and recorded yourself. At most 1 process at a time, under 3 GB, `nice -n 15`; total compute budget
about 20 minutes. Other people's jobs run on this machine: leave them alone. Do not copy raw terminal
transcripts into your report, and do not write anything from your own memory of other projects or any personal
identifier (names, email addresses, home paths outside this repository) into it. Do not read or quote the
author block of any paper file.

## Texts
1. `dist/tog/supp_src/s15_note1.md` (Note 1; section 2b is the written-out proof of Lemma 3).
2. `dist/tog/supp_src/s15_note3.md` (Note 3).
They build on `dist/tog/supp/s13.tex` (setting, move classes, the reduced game, Lemmas 1 to 3). Rules:
`dist/tog/sections/02_rules.tex`. Claims in the paper: `dist/tog/sections/08_star2.tex`.

## Do
1. For each note: is every statement precise, and does each step of each proof follow? Quote the exact step that
   fails if one does. Are all hypotheses of the lemmas of S13 verified where they are used?
2. List every computed fact each note depends on, with its label and the number of independent programs it
   claims. Is each label honest?
3. With your own short program (do not import the repository's code) recompute one small computed fact of each
   note, if one fits in 10 minutes; report agreement or say that none fits.
4. Any sentence that states more than is proved, any reference to a program, table or section that does not
   exist in `dist/tog/supp/` or `dist/tog/supp_src/`, any undefined symbol.

## Report
`REPORT.md`: first line a verdict per note (FINAL TEXT SOUND / SOUND WITH FIXES / GAP). Then findings as
`file:line`, severity (BLOCKER, MAJOR, MINOR), exact replacement text, and what you did not check.
