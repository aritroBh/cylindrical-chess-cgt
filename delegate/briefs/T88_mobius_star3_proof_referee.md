# T88 — Hostile referee of a new proof note: *3 rings with n+1 pawns on the Möbius strip, every n >= 11

Output directory: `delegate/out/T88/` (create it). Write `REPORT.md` there and any programs. Do not edit anything
else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs you started
and recorded yourself. At most 1 process at a time, under 3 GB RSS, `nice -n 15` if your sandbox allows it (if it
does not, run short checks anyway and say so); total compute budget about 20 minutes. Other people's jobs run on
this machine: leave them alone. Do not copy raw terminal transcripts into your report, and do not write anything
from your own memory of other projects or any personal identifier into it.

## Text
`research/mobius_star3_family/PROOF.md` (96 lines, written by an AI model of another vendor today). It claims that
TT(m) = `B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2 (B4 W2)^m` (n = 2m+10, m >= 1) and
SS(m) = `B6 W3 (W2 B4)^m W6B7 W3 B7 B6 W3 W2 B6 W2 B4` (n = 2m+11, m >= 0) have value *3 on the Möbius strip M_n
(outcome against every nim-heap as *3). It cites, and does not re-prove, statement V and Lemmas 1, 2, 3 of
`dist/tog/supp_src/s15_note5.md` (the note you refereed in T82 and T83, in its corrected final form).

## Finite inputs
- Your own checker `delegate/out/T87/check.py` was run to completion by the project (your sandbox had refused the
  priority change): its output is `delegate/out/T87/run_all.log` (JSON lines; if the file is still growing, use what
  is there and say which records were missing). Compare every number in the note's C1, C3 and seam facts with it.
- The note's own logs are in `research/mobius_star3_family/logs/`.

## Referee as a hostile reader
1. **The seam (the one new point).** For TT the ten-file arc 10..19 ends at the seam file n-1 = 19 at the base
   n = 20, and file 0, across the seam, is a zone file that changes in the reduced graph. In Note 5 the arc of
   F1/F2 starts at file 0 and the file across the seam does not change. Go through V1 to V3 and the proofs of
   Lemma 2 and Lemma 3 in `s15_note5.md` and decide yourself whether any step uses that the seam neighbour of the
   arc's end file is unchanged or is a pattern file. Is the note's section on the seam a proof or an appeal to the
   computation? If you doubt it, say whether the note's fallback (base m0 = 6 for TT, so that the arc is away from
   the seam, with TT(5) moved to the direct checks) removes the doubt, and whether the logs support that base
   (`logs/fverify_TT.log`, line m = 6).
2. Walls and phase: which wall type of Note 5 each family has, whether the stated cut copies the right two files so
   that ins_c(start_m) = start_{m+1}, and from which m on.
3. Invariant and step: zone disjoint from the arc from which m on; ins_c maps zone to zone (SS's zone moves with m);
   no flag at any node; isomorphism of reduced games with T-flags; induction closed without assuming unseen widths.
4. From the signature for heaps 0..3 to every heap; what "value *3" is claimed to mean.
5. The range: is any width between the direct checks and the base of the induction skipped (even and odd n
   separately)? Are the labels (PROVED, CHECKED-2, COMPUTED-1) honest, given `run_all.log`?
6. Any sentence that states more than is proved; any undefined symbol; any citation of an item of Note 5 that does
   not say what the note claims it says (quote the item).

## Report
`delegate/out/T88/REPORT.md`: first line the verdict (HOLDS / HOLDS WITH FIXES / GAP). Then findings as
`file:line`, severity (BLOCKER, MAJOR, MINOR) and exact replacement text; a table comparing the note's numbers with
`run_all.log`; and what you did not check.
