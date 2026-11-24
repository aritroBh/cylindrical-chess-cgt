# T90 — Re-read of the repaired wall-ring proof (supplement Section S13), final text

Output directory: `delegate/out/T90/` (create it). Write `REPORT.md` there. Do not edit anything else. Never run
git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs you started and recorded
yourself. At most 1 process at a time, under 3 GB RSS, `nice -n 15` if your sandbox allows it; total compute
budget about 10 minutes. Other people's jobs run on this machine: leave them alone. Do not copy raw terminal
transcripts into your report, and do not write anything from your own memory of other projects or any personal
identifier into it.

## Text
`research/ring_family_proof/proof.tex` (222 lines) is the text after your report `delegate/out/T89/REPORT.md` was
applied by a model of another vendor. The earlier text is not needed; judge this one as printed. It will be read
by journal referees.

## What to decide
1. For each of your findings 1-12 of T89: is it resolved in the new text? Quote the new sentence.
2. Read the new proofs of Lemma 1, Lemma 2 (both parts) and Lemma 3 (statement (V), steps (i)-(iii)) and the
   induction line by line as a hostile referee. For each step: sound / gap / false, with the missing argument or
   a counterexample. Check in particular the new material: the definition of insertion for positions with an
   e.p. flag and the two facts proved about it; the choice of the side s in Lemma 2(b); step (iii); the hypothesis
   4 <= c <= n-6 and whether the cuts used (odd: c = 9 from n = 17; even: c = 8 from n = 16) satisfy it; the
   model paragraph (flag across a heap move, the count rule and its tie break) against what the programs do.
3. The theorem as now stated (outcome for 0 <= h < 256; the sense of G_n = *2 with terminal positions replaced by
   +-256): is exactly this proved, and is anything claimed beyond it?
4. C1 and C2 as now worded: do they match the logs (which programs, which widths)?
5. Consistency with the notes that cite these lemmas: `dist/tog/supp_src/s15_note1.md` (its section 2 restates
   Lemmas 1-3 and section 2b proves steps (ii)-(iii) for its family), `s14_ringn.md` and `s15_note2.md` to
   `s15_note4.md` (restatements). Does any note use a lemma under hypotheses that the new statement does not
   cover (for example the new hypothesis "pattern files of one wall" or 4 <= c <= n-6, or Lemma 1 for
   non-terminal g)? List note, line, and the needed change.
6. Wording: any sentence that is ambiguous, any symbol used before it is defined, any leftover that reads like a
   working note.

## Report
`delegate/out/T90/REPORT.md`: a verdict (sound as printed / sound with wording fixes / mathematical error), then
numbered findings with the line of proof.tex, the quoted sentence and an exact replacement. Separate mathematical
points from wording. Say what you did not check.
