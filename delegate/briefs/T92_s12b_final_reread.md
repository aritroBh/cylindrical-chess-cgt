# T92 — Re-read of the two condensed proofs after your report T91 was applied

Output directory: `delegate/out/T92/` (create it). Write `REPORT.md` there. Do not edit anything else. Never run
git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs you started and recorded
yourself. At most 1 process at a time, under 3 GB RSS; total compute budget about 10 minutes. Other people's jobs
run on this machine: leave them alone. Do not copy raw terminal transcripts into your report, and do not write
anything from your own memory of other projects or any personal identifier into it.

## Text
`dist/tog/supp_src/s12b_extra.tex` (285 lines) is the text after your report `delegate/out/T91/REPORT.md` was
applied by a model of another vendor, mostly in its own wording (its account: `delegate/out/W10_t91_fixes/REPORT.md`).
Judge the text as printed now. It cites items A.1-A.17 of `dist/tog/supp_src/s12a_core.tex`.

## What to decide
1. For each of your findings 1-14: resolved in the new text? Quote the new sentence. If the other model's wording
   differs from your replacement, is it still correct?
2. Read A.18 (a),(b),(c) and the three cases of A.18a once more line by line: is every use of a blocking strategy
   made where the blocker can wait in the actual game, and is each case fully proved by what is printed, with the
   acyclic definition and the stated move bounds?
3. Read A.19 Steps 0-5 and A.19a once more: Step 4 and Step 5 as now worded; the e.p. sentences; the definition of
   king distance.
4. This sentence of Section S2 now cites A.19. Does A.19 with A.19a imply it exactly?
   "For (V2) we give a sufficient test in the frozen-king game \lab{S} (Proposition~A.19 of Section S12.2): ..."
   The exact sentence is the last string argument of the first `REP(` call that mentions `S-kingslong` in
   `dist/tog/tools/build_supplement.py` (search for "sufficient test"). Quote it in your report.
5. Anything new that the edits broke: a symbol now undefined, a statement changed in strength, a dangling reference.

## Report
`delegate/out/T92/REPORT.md`: one-line verdict per item A.18, A.18a, A.18b, A.19, A.19a, A.19b (sound as printed /
sound with wording fixes / mathematical error), then numbered findings with line, quoted sentence and exact
replacement. Keep it short: list only what still needs a change, plus a table for point 1.
