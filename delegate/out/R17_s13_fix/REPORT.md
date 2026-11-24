# R17: repair of Section S13 (wall rings G_n = *2)

Output: `delegate/out/R17_s13_fix/proof_new.tex` (complete replacement for `research/ring_family_proof/proof.tex`).
Compiles with tectonic (`build/proof_new.pdf`, 4 pages, the extracted part about 3.1 pages): no undefined references, no warnings.
A simulation of the supplement's extraction (`build/sim/`: wallproof body with theorem->wtheorem, lemma->wlemma, plus the
five-moves block, supplement macros) also compiles; its only warning is an overfull hbox from the five-moves table, which is
unchanged from the old file. The four markers occur once each. Macros used: \lab, \nim, \cyl, \ins only; environments theorem,
lemma, proof, itemize; no \label/\ref.

## 1. Findings 1-12

| # | decision | reason |
|---|---|---|
| 1 Lemma 1 domain/induction | correct, adopted (reworded) | Root must be non-terminal; "keep their values" replaced by induction on (remaining pawn steps + heap). Statement now matches Note 5's careful one. |
| 2 Lemma 2(a) | correct, adopted (reworded) | Proof was sound; now says explicitly why q cannot capture (also e.p.) and why the W2->4 pawn is not passed. |
| 3 Lemma 2(b) capture side | correct, adopted | Verified by hand and by block E: on 11 files, W3 B5 W3 B5 W3 B5 on 3..8, B5->4 on file 6 (window 3..7 only) is P; capture from file 5 wins for White, capture from file 7 (the printed j+1) releases B5 on 8, distances 4/4, Black wins the tie. The conclusion survives with s chosen from the window: capturer from j+s is passed (files j-1..j+1 hold no X pawn) and the only X pawn that could be released, on j+2s, is blocked by j+3s. Second example (E window 4..8, W2->4 on file 5 is L) also replayed; consistent with the lemma. |
| 4 ins_c on flagged positions | correct, adopted | Proof applied ins_c to children with a flag, but ins_c was defined only for flag-free p. New definition: c,c+1 pattern files, flagged pawn not on c,c+1, flag moves with its pawn; facts (V) and (C) proved. |
| 5 step (iii) gap | correct, adopted | (iii) cited (ii) (moves of X from a flag-free parent) for Y's replies from a flagged child; replies from c-2 / c+3 were not covered. New (iii): near replies (c-1..c+2, resp. c-1..c+4) cannot give Y a passer by Lemma 2(a) (flag protects X's stepper); far replies start on <=c-2 or >=c+3, never touch c,c+1 (e.p. replies come from beside the far stepper), so (C)+(V) give the same terminal winner. Checked that this closes the gap; it is Note 1 §2b / Note 5 §3 in substance. |
| 6 bases / no width skipped | correct (no gap), adopted | Arc 5..14 needs n-2>=14 (odd 17); arc 4..13 needs n-2>=13 (even 16); also 4<=c<=n-6. C2 covers odd 5..15, even 6..14. Induction now explicit: injectivity, lift, project, invariant I_n. |
| 7 meaning of =*2 | correct, adopted (shortened) | P at h=2 forces N at h=0,1 (heap options of a P-position) and N for h>=3; proof uses no bound on h. The ±256 integer reading gives a genuine CGT equality Ĝ_n=*2 (checked: ±256+*h is won by the favoured side; heap move keeps board+flag = disjunctive sum). Stated with what it does not cover. |
| 8 C1 attribution | correct, adopted | See section 4. |
| 9 C2 attribution | correct, adopted | Old "(unreduced search; whole-board cylcgt for n<=10)" suggested cylcgt was the second program; it is only for 5..10. The two programs at every width are rg.c and eng.py. |
| 10 model paragraph | correct, adopted | Rules, files mod n, e.p. flag and holder of the right, heap move keeps the flag (this is what rg.c, eng.py do), passed test, count race with tie to the side that did not move (from Note 1 §1), classes for pawn moves only. |
| 11 zone wording / radius remark | correct, adopted | "never move and are never captured" holds only in nodes of the reduced game; radius 5 is sufficient, not minimal. Log check: lemmaL_sensitivity.log rows rho=1,2,3 give 217, 1, 0 counterexamples; the 4th row (1968) is the MUTATE (wrong-phase) run per run_all.sh line 23. |
| 12 F family remark | partly correct, adopted as a hedged remark | F definition, bases, zones and cuts checked against pump_F*.log and fam.py; transfer stated as "not written out in full". Not part of the extracted text. |

## 2. Statements whose mathematical content changed (old -> new, why)

1. Model. Old: one-line pointer ("race rule count; e.p. on; ..."). New: full rules incl. e.p. holder, heap move keeps board and flag, count race with tie rule, classes for pawn moves only, R(g)+*h moves. Why: findings 10, 7; the proof uses all of these.
2. Rings. New: G_n := O_n / E_n; general "wall" (W3/B5 or W2/B4 alternating, any phase) and pattern file = exact content. Old pattern-file wording ("contains precisely its one starting wall pawn") is the same content.
3. Theorem. Old: "O_n=*2, E_n=*2". New: G_n+*h is P iff h=2, for 0<=h<256; meaning stated. Why: finding 7.
4. Lemma 1. Old: "A side wins G+*h moving first iff it wins the reduced game moving first." New: g non-terminal, h>=0, either side first. Proof by induction on remaining steps + heap. Why: finding 1.
5. Lemma 2. Statement: position renamed c -> p (clash with the cut c), "Z=X" dropped (vacuous), "pattern files of one wall" added. Proof of (b): capture from j+s with s chosen from the window (old: always j+1, false for the left window). Why: finding 3.
6. Insertion. New paragraph: ins_c defined for positions with a flag off files c,c+1; facts (V) and (C). Old: defined only for flag-free p, used on flagged children. Why: finding 4.
7. Lemma 3. Added hypotheses 4<=c<=n-6 and "of one wall"; added conclusion "p̂ has no passed pawn and no flag". Proof (iii) rewritten (near/far replies). Why: findings 4, 5. (Every cut used in S13-S15 satisfies 4<=c<=n-6, see section 3.)
8. C1. Adds K-edge counts 209/177 and exact programs per claim. C2: exact ranges (odd 5..61, even 6..60), the two programs, cylcgt whole-board value only for 5..10. Why: findings 8, 9.
9. Proof of Theorem. Adds: start_n has no passer (hand check, verified also by eng.py for n<40), explicit isomorphism argument, invariant I_n, heap argument for all h. Why: findings 6, 7.
10. New paragraph "What is and is not proved": Ĝ_n=*2 in normal-play CGT (±256 reading); not sums with other pawn boards under first-passer adjudication; not the component-sum model; only rule "count". Why: finding 7.
11. Details (not extracted): reduced-game wording for frozen files; table caption with s=+1 and the non-terminal branch; the 11-file example. Remarks: radius sentence and F family hedged.

## 3. Needed changes in later notes (not edited)

- `dist/tog/supp_src/s15_note1.md` line 5: "the proof of Lemma 3 (ii)-(iii), which Section S13 gives in two terse lines" -> S13 now gives it in full; say 2b is an equivalent longer write-up.
- s15_note1.md line 46: "The statements of Lemmas 1-3 below are quoted verbatim" and the history of the pattern-file definition -> no longer verbatim; replace lines 52-54 by the new statements (Lemma 1: non-terminal g, h>=0, either side; Lemma 2: p for c, no "Z=X", "of one wall"; Lemma 3: add 4<=c<=n-6, "of one wall", "p̂ has no passed pawn and no flag") or say "quoted from an earlier version; equivalent for the uses here".
- s15_note1.md line 57: "Section S13 proves Lemma 3 in six lines; its step (iii) cites (ii) ..." -> stale; S13's (iii) is now written out.
- s15_note1.md line 91 (H8): "Section S13 does not say whether a pending e.p. flag survives a heap move" -> S13 now says it survives ("keep"). The rest of H8 (immaterial for the proof) stays true.
- s15_note1.md line 110: "The race rule is not defined in Section S13; H4 states it." and "Lemma 3 (iii) was terse in Section S13; 2b replaces it." -> both stale.
- `dist/tog/tools/build_supplement.py` line 365: "typeset unchanged; one of its definitions (pattern file) is repaired in Note 1" -> stale (the definition is now in S13).
- Optional harmonisation, no error: Notes 1 (line 12), 3 (H7), 4 (H7), 6 (line 90) say equality "as a standard partizan game / against arbitrary addends" is not claimed for their families. S13 now proves Ĝ_n=*2 for the ±256 representation; the notes' statements about the operational game remain true.
- No change needed: s14_ringn.md line 37 (restatements compatible; cuts c=4, n>=18 and c=5, n>=19 satisfy 4<=c<=n-6); Note 2 (c=9, n>=22); Note 3 (c=6, n>=19; its H3 right-end capture "B4 on j-1" is the s=-1 case, correct); Note 4 (c=4, n>=20; c=7, n>=23); Notes 5, 6 use their own strip lemmas. Note 1 H2 (line 78, "or the mirror image") is correct.

## 4. Coverage of C1 and C2 from the logs

C1 (bases O_17, E_16):
- rg.c (via pump_verify.py/graph.py): logs/pump_odd_c9.log, pump_even_c8.log: 144/104 nodes, kept 209/177, T 246/97, ep=0, zone [0..4,16] / [0..3,15], reduced-graph signature NNPNNNNN (h=0..7), at every odd 9..61 / even 8..60.
- cylcgt-based builder reduced_cyl.py vs rg.c: logs/reduced_cyl_odd.log (odd 5..23) and _even.log (even 6..22): identical node sets and (src,side,target) sets (T collapsed per side), 144/308 and 104/231.
- eng.py (verify/red.py, verify/zonecmp.py): no archived log; rerun here: O 17: 144 nodes, K 209, T 246, flagged 0, touched {0..4,16}, NNPN; E 16: 104, 177, 97, 0, {0..3,15}, NNPN; zone-state sets equal to the stored lists (144/144, 104/104).
- cylcgt CGT arithmetic on the cylcgt-built reduced game: logs/reduced_value.log: *2 for odd 5..25, even 6..26.
C2:
- rg.c solve 3 via fullsweep.py: logs/fullsweep.log: odd 5..61 (29 widths), even 6..60 (28 widths), all NNPN (plus F 5,7..61).
- eng.py Solver: verify/sweep_O.txt (odd 5..61, 29 rows), verify/sweep_E.txt (even 6..60, 28 rows), all NNPN.
- whole-board canonical value with cylcgt: logs/cyl_whole_odd.log (5,7,9), cyl_whole_even.log (6,8,10): *2; also verify/cylwhole.txt.
- Both unreduced searches keep the flag across heap moves (checked in the code), as the model now states; both skip only L-moves (immediate losses), no poison deletion.
Extra (not cited in the text): delegate/out/T89/check.py (imports argparse, functools only) rerun here: NNPN for every width 5..17.

## 5. Not verified

- Did not rerun rg.c (reduce, solve, pump), reduced_cyl.py, reduced_value.py, cyl_whole.py, fullsweep.py or the eng.py sweeps; their results are taken from the archived logs above. Did not audit rg.c or cylcgt code beyond the heap/flag convention and solver structure.
- The F-family remark (finding 12) rests on logs only; no independent proof of its zones beyond reading pump_F*.log.
- The randomized radius experiment is cited from logs/lemmaL_sensitivity.log; not rerun.
- Commands run (all nice 15, PYTHONDONTWRITEBYTECODE=1, -B): block E, block A (5..17), verify/red.py O 17 / E 16, verify/zonecmp.py, a check that ins_c(start_n)=start_{n+2} and that start_n has no passer for n<40. Nothing was written under research/, dist/, paper/ or kings/.
