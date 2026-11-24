# W2 review fixes: report
Builds (dist/tog/build/ only): tog.pdf 10 pp, tog_review.pdf 10 pp; supplement.pdf and supplement_review.pdf 106 pp; no overfull box over 5 pt, no undefined reference (only font-shape warnings). freespace.sh: "pages 10 left col ends 748 pt, right col ends 722 pt, free in right column 0.36 in". check_numbers.py: "RESULT: all numbers found". Anonymity grep on tog_review.pdf and supplement_review.pdf: 0 and 0. Abstract: 199 words (pdftotext).

## A Corollary 4 (04_kings.tex ~69-73; s12a_core.tex A.13 quote)
Now: "If also (V4) holds, that is, X is hereditarily sum-safe (Definition), satisfies condition (E) of Theorem, and BIG exceeds the number of moves either side can make, then for that side to move the chess result is the one given by the components' +-BIG value." Used your target wording; A.13 needs no change. A.13's "Main text:" quote replaced to match. s12a_core had no remark saying the main text states it for both sides (only the A.13 parenthesis on inferring the full outcome class, which is true and kept). In s17_provenance.tex "What the checks found" I added "; it is now stated for the side to move."
## B 01_intro.tex ~36: C2 definition now "two separately written programs agree, the second from the rules alone (both AI-written; Section~S17);". Note: supplement.tex:87 (not editable) still says "two independently written programs agree".
## C 05_sums.tex ~88: replaced as specified. "all the second-player wins" occurs nowhere else except paper/IEEE_CHECKLIST.md:207 (a quote of the R14 report) and R14 REPORT.md. It is not in dist/tog/long/ or the supplement sources. (The supplement S3.4 text, build_supplement.py:157, already says "38 sides ... all 19 sums share the same anchors".)
## D Definition 12 (09_real.tex 11-13): now "or as worth 0, scoring the end position {BIG r_W | BIG r_B} (r_W,r_B in {-1,0,1}: white's results with white and with black to move; a dead draw is scored *)." Verified in code: realchess/oracle_value.py:635-645 (pair_game, kind "draw0"): returns make([BIG*rw],[BIG*rb]); comment line 636 "draw/draw -> *"; so (0,0) gives {0|0}=*. Matches; edit applied.
## E Engines
1. Threshold: engine/runs/analyze_sf.py:22 `return "win" if v >= 150 else "loss" if v <= -150 else "draw"`; mate scores are win/loss (lines 19-21); match test line 33. Also engine/ENGINES.md:363.
2. Script and output: delegate/out/W2_review_fixes/fisher_tablev.py, fisher_tablev.out (no scipy; exact hypergeometric sum, two-sided = sum of tables with prob <= observed). Counts reproduce Table V (hot 55/68, number 45/57, switch 27/37, other 12/20, nimber 9/17, infinitesimal 8/27 at depth 1). Infinitesimals vs hot p=1e-5, number 2e-5, switch 8.8e-4, other 0.072, nimber 0.203. Confirms the referee. (Depth 2: infinitesimal vs nimber p=0.015, so the "not nimbers" statement holds only at depth 1, which is what the text says.)
3. Text replaced as specified (no number differed). 4. Bullet replaced. 5. "labeled by its CGT class in the model".
## F 04_kings.tex ~99 and 14_conclusion.tex 4: replaced as specified. S2.3 source is long/04_kings.tex:168: "not a sample of a defined class" (so "not a random sample" is faithful).
## G Definition 5 (05_sums.tex ~52): A.3's exact conditions differ from your target: A.3 requires that no position before the last has a passed pawn, and a race gives both sides one. Written: "A component carries a threat for a side if play on its own files can reach a position, with no passed pawn earlier, that gives that side a passed pawn (a race gives both sides one)." Remark A.3 rewritten: the main text's threat is now the same notion; dropping the earlier-passed-pawn clause would be a stronger hypothesis and the theorem covers it.
## H Table I removed (05_sums.tex); opening sentence replaced; 01_intro.tex ~35 now "(Sections~\ref{sec:sums} and~\ref{sec:dawson})". No other \ref{tab:puzzles} in sections/. Supplement S3 did NOT print the table (build_supplement.py used long/05_sums.tex lines 18-41; table is lines 42-60). Changed to L('05_sums', 18, 60); built supplement now prints it as Table S1 (label no longer in the main text, so it is kept). Supplement refers to main-text items by \ref via xr (supp/mainlabels.tex, regenerated from tog_review.aux), so table numbers follow automatically; I found no hard-coded main-text table numbers in supp_src/, build_supplement.py, supplement.tex, long/, check_numbers.py. To change by the author: submission/scholarone_fields.md:31 "5 (Table I to Table V)" -> "4 (Table I to Table IV)"; figure count 7 unchanged. No "Table I..V" in other submission/*.md.
## I
1. 08_star2.tex ~116: "checked by two programs for $n<17$" -> "for $n\le61$ \lab{C2}". Evidence: research/ring_family_proof/logs/fullsweep.log (author's unreduced search rg.c, n=5..61, 113 rings, all *2); the verifier's independent engine eng.py agrees for O 5..61, E 6..60, F 5..61 (research/ring_family_proof/REPORT.md lines 14-16, "CHECKED-2"); cylcgt whole-board n<=10 (logs/cyl_whole_even.log, cyl_whole_odd.log: n=5..10). proof.tex:86 (C2) lists n<n0=17 plus n<=61. I also corrected the S17 table cell (s17_provenance.tex ~74) to say the same. Your example "two for n<=10, one for n<=61" is more cautious; I used the logs plus REPORT.md. Change it back if you do not accept the verifier's engine as a second program for n up to 61.
2. 05_sums.tex ~74: "... \lab{C1} (Section~S3), and in our model \lab{P} (Section~S12)." (remark in s12a_core says label P, holds with e.p. on.)
3. Prop 7: "on cyl8 with en passant off and the count rule," (A.14 hypotheses: e.p. off, count race rule, BIG=256; BIG=256 is stated in the preceding paragraph, not in the proposition).
4. Intro "Real chess" bullet: label \lab{C1} (09_real Theorem 14 is \lab{C1}; part (b) is the claim).
5. 09_real.tex ~51: "in $290$ only one side has a passed pawn (the other $12$ are races); $283$ of them agree ..." (long/09_real.tex:56 says "the other 12 are races").
6. 02_rules.tex: "with $n$ files and, unless we say otherwise, eight ranks."
7. 13_verify.tex: "reference games $R$", "$G+R$".
8. 04_kings.tex: "at most two promotions". CAUTION: the supplement never says what "at most two" counts. kings/SPEC.md:75-81 defines the solver cap as the maximum number of officers on the board (both colours together). I could not locate the 500-component sweep's settings. Author please confirm (could be "at most two promoted pieces on the board").
9. Abstract: "sufficient conditions for ..." would give 202 words; used the fallback "and give conditions for frozen kings to match chess." Count stays 199. scholarone_fields.md abstract updated (only that sentence; its "3 words of headroom" note is wrong, should be 1, untouched).
10. refs.bib: HGMCylinder gets year = {n.d.} (no year recorded in notes/lit_cylinder.md or the bib); prints "H. G. Muller. (n.d.) Cylinder chess. XBoard variant rules. Accessed: Oct. 22, 2026". WuYuLandry2010: notes/lit_cgt_chess.md:28 records "Stanford Math 191 paper", so howpublished = "Undergraduate course paper (Math 191), Stanford Univ., Stanford, CA, USA" (the city is my inference from Stanford).
## J
1. build_supplement.py NOTE template (S12.2 and S14) now adds the sentence "Its labels PROVED, CHECKED-2, COMPUTED-1 and CONJECTURE correspond to \lab{S}, \lab{C2}, \lab{C1} and \lab{Conj} of the main text." Same sentence added to the S15 intro. S13 has its own text (uses \lab already): "typeset unchanged" kept but now "...; one of its definitions (pattern file) is repaired in Note~1 of Section~\ref{S-star3}" (your wording would be false: S13 is proof.tex unchanged and Note 1 s15_note1.md items 2 and 22 do the repair). Not edited: supplement.tex lines 85-88 (cannot edit).
2. s17_provenance.tex before -> after: "an Opus agent" (x4, plus one "an Opus agent;") -> "a Claude Opus model"; "an agent; model not recorded" -> "a Claude model; version not recorded"; "the specific agent is not recorded" -> "the model version is not recorded"; "Two adversarial Claude lenses" (x2) -> "Two Claude reviewers instructed to look for errors"; "(an automatic choice after the intended tool failed)" -> "(chosen automatically by the tool)"; "in 2026-10" -> "in October 2026"; "Claude Sonnet verifier (no)" -> "A Claude Sonnet model (no)"; extra for consistency: "Sonnet agents" -> "Sonnet models", "a Claude Opus agent (no)" -> "a Claude Opus model (no)", "another Opus agent's search" -> "another Claude Opus model's search", "by the verifier from the rules ... verifier's engine" -> "by that Sonnet model ... that model's engine" (with the n<=61 fix above). Line 1 comment "2026-11-23" is a TeX comment, not printed.
3. S5: lead-in sentence added in build_supplement.py before L('07_targets',62,90): "Theorem~\ref{thm:eighth} of the main text states that the position of its Fig.~\ref{fig:eighth}(a) has value exactly $1/8$." Built text: "Theorem 9 of the main text states that the position of its Fig. 4(a) has value exactly 1/8. To see why, look at Fig. 4(a)."
4. S7: referee is right. T is \pos{W Kf5 g4 / B Kh4 g5} on files f-h (04_kings.tex:19-20), so file f holds the white king; the five-file *2 uses files a-e, file e has pawns (e2, e3) next to T, so T has no pawn-free buffer file and Theorem 3 does not apply. Source dist/tog/long/09_real.tex:71-72 (NOT edited). Replace the two lines
 "T, and the five-file $\nim{2}$ \pos{W a3 b3 c2 e2 / B a6 c5 d5 e3}, which sits legally" / "beside T, has $12$, with only file f free of pawns between them. Their oracle values are open: for A and B a"
by line 72 "beside T, has $12$; no file between its pawns and T is free of pawns, so Theorem~\ref{thm:validity} does not apply. Their oracle values are open: for A and B a". Same check should be done for A and B (not examined).
## K builds: see top. ## L Fig. 6 (research/figures_2026_11/f2_least_pawns.py, line 16-17; output dist/tog/figures/f2_least_pawns.pdf). Star-3 computed points (n, pawns): (10,12), (11,12), (12,13); proved upper bound n+1 for n=13..20. The ten-pawn star-3 rings on C7 and C8 are NOT plotted (the caption says only that they exist).
## Not done / notes
- No edits to long/, paper/, research/, kings/, tog.tex, supplement.tex; no commit. supp/*.tex are regenerated build outputs. supp_src/s12_kings.md, submission/{SUBMIT_STEPS,cover_letter,files_to_upload,pdf_checks}.md, rebuild.sh were already modified before this job. Not touched: R14 items 8 (notation renames), 9 (paths, PDF names, acknowledgment), 11 (ChessSums cut) - not in this brief.
- Also to change outside my scope: dist/tog/submission/scholarone_fields.md "Tables 5" count (above); pdf_checks.md and files_to_upload.md hashes and page data are now stale after the rebuild.
 M dist/tog/refs.bib
 M dist/tog/sections/00_abstract.tex
 M dist/tog/sections/01_intro.tex
 M dist/tog/sections/02_rules.tex
 M dist/tog/sections/04_kings.tex
 M dist/tog/sections/05_sums.tex
 M dist/tog/sections/08_star2.tex
 M dist/tog/sections/09_real.tex
 M dist/tog/sections/12_engines.tex
 M dist/tog/sections/13_verify.tex
 M dist/tog/sections/14_conclusion.tex
 M dist/tog/submission/SUBMIT_STEPS.md
 M dist/tog/submission/cover_letter.md
 M dist/tog/submission/files_to_upload.md
 M dist/tog/submission/pdf_checks.md
 M dist/tog/submission/scholarone_fields.md
 M dist/tog/supp/mainlabels.tex
 M dist/tog/supp/s03.tex
 M dist/tog/supp/s05.tex
 M dist/tog/supp/s12.tex
 M dist/tog/supp/s13.tex
 M dist/tog/supp/s14.tex
 M dist/tog/supp/s15.tex
 M dist/tog/supp/s16.tex
 M dist/tog/supp_src/s12_kings.md
 M dist/tog/supp_src/s12a_core.tex
 M dist/tog/supp_src/s17_provenance.tex
 M dist/tog/tools/build_supplement.py
?? dist/tog/rebuild.sh
?? dist/tog/set_anon_url.sh
