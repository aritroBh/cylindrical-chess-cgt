# R2 cross-reference audit

Scope: `dist/tog/sections/*.tex`, `dist/tog/tog.tex`, `dist/tog/supp/*.tex`, `dist/tog/supp_src/*`, `dist/tog/submission/*.md`, `paper/ieee/sections/`, `README.md`, `RESULTS.md`. Read-only. The built PDFs are newer than every source file (`find -newer` returns nothing), so the PDFs show the text audited here. Supplement section numbers below are the ones printed in the supplement PDF (S6.4 = Mobius subsection, S12.1 = self-contained proofs, and so on).

Findings per task: T1 = 7 (2 wrong, 5 vague), T2 = 4, T3 = 1, T4 = 6 (a: 3, b: 1 low, c: 1 low, d: 1), T5 = 5, T6 = 0.

## Task 1. Supplement pointers

### 1a. Every hard-coded pointer from the paper (sections/*.tex, tog.tex)

| file:line | claim | actual title of target | content there? |
|---|---|---|---|
| 02_rules:66 S1 | positions of value 1, 2, star, up are in the supplement | S1 Basic Positions and the E.p.-Aware Test | yes, Fig. basicS (a)-(f), "Thus $G=\game{0,1}{}=2$" |
| 02_rules:79 S1 | 18,137 of 231,071 values change, 4,070 in outcome | S1 | yes, s01:48 same numbers |
| 02_rules:108 S1 | derivations of 1, 2, star, up, double-up-star | S1 | yes ("double-up star") |
| 04_kings:66 S12 | full proof of validity theorem | S12 Full Proofs ... | yes, S12.1 A.11 (S12.2 Thm 1.14). Fine, but S12.1 is more exact |
| 04_kings:85 S12 | exact clauses of certificate | S12 | yes, S12.1 A.14 (C1)-(C3), A.16 |
| 04_kings:86 S2 | local test for (V2), loopy games | S2 Kings: Certificates, Loopy Games, Failure Sweep | yes, s02:21 "For (V2) a local test is known only if king moves also lose", S2.2 "Spare King Moves Are Loopy" |
| 04_kings:99 S16 | square rule not sound on every board | S16 Square-Rule Passer Test ... Counterexample | yes, "3. S is not sound in general" |
| 04_kings:101 S2 | 2,154 positions, 105 draws, 92.5% | S2 (S2.3) | yes, same numbers |
| 05_sums:17 S3 | puzzles shown | S3 Sums: The Puzzles and Condition (E) | yes, Figs puzzle72/73, text on Puzzle 3 and legal copy |
| 05_sums:66 S12 | full proof of sum safety, induction with (E) | S12 | yes, S12.1 A.4-A.7 |
| 05_sums:74 S3 | (E) cannot be dropped, pure pawn game, C1 | S3 (S3.2 Condition (E)) | yes, Prop condE C1 |
| 05_sums:85 S3 | models differ, even in outcome | S3 (S3.3 Two Models) | yes, "${\Uparrow}$ as a sum but $\nim{2}$ on the whole board" |
| 06_atlas:14 S4 | highest temperature 3 | S4 The Atlas: Details | yes, "The Hottest Position" |
| 06_atlas:24 S4 | "shows these positions" (six-setting comparison) | S4 | NO, see T1 finding 1 |
| 07_targets:62 S5 | checks ran on mirror image | S5 Elkies' Small Values: Details | yes, "The independent checks were run on the mirror" |
| 07_targets:70 S5 | textbook 1/8 and up-second fail under e.p.-aware | S5 | yes, "Two Textbook Values That Fail" |
| 08_star2:31, 52, 58, 89, 90, 104, 130 S6 | details of candidate, A/B legal history, move-for-move B, nine-file scan, five-file counts, ring listings, heights | S6 The *2 Question: Details and Ring Listings | all yes (S6.1 "Thus $G=\game{0,\star}{0,\star}$", S6.2 "A by a2--a4 ...", S6.3 "21 of value *2", S6.5 heights) |
| 08_star2:136 S15 | Mobius one pawn per file, every strip of ten or more files | S15 (Note 5, S15.5) | yes, Theorem F1/F2/F3, "for every $m\ge1$". Could say "Note 5" |
| 09_real:46, 55 S7 | other non-default *2 open; 6.1e10 states in 15.6 h | S7 From the Model to Real Chess: Details | yes both |
| 10_tablebases:69 S8 | counts, widths 3 to 10, KPKP | S8 Tablebases: Rules and KPK | yes (table n=3..8 C2, n=9,10 C1, "A pawn each") |
| 11_dawson:10, 60 S9 | boards; next quotient did not finish | S9 Dawson's Chess: Details and Learning | yes (Fig. dawson_boards; "the next quotient did not finish") |
| 12_engines:63 S9 | learning experiment | S9 (S9.1 Learning Dawson's Chess) | yes |
| 13_verify:15 S12-S15, S11 | full proofs of the S results; FEN of every position with kings | S12-S15; S11 Positions with Kings in FEN | yes (see T1 finding 6 for one nuance) |
| 14_conclusion:5 S10 | "lists more problems than these four" | S10 Further Open Problems | yes, six problems |
| 14_conclusion:14 S2 | h about 5-7 (Conj) | S2 | yes, s02:42 |
| tog.tex:143, 152 S12-S15 | AI wrote the full proofs | S12-S15 | yes |

### 1b. Hard-coded pointers inside the supplement

All "Section S13 / S14 / S15" pointers in `supp/s14.tex`, `supp/s15.tex`, `supp_src/s14_ringn.md`, `supp_src/s15_note1..5.md` point at the right section (S13 = wall proof and Lemmas 1-3, S14 = one pawn per file with check C1M, S15 = Notes 1-5 with Lemma 3 in Note 1 section 2b). `supp_src/s12a_core.tex` has one hard-coded text pointer (line 1-2, a comment: "Sections 4 and 5 of the main text", correct); everything else in it uses `\ref`. `supp/s06.tex:220` "Sections S6.2 and S6.3" is correct. `supp/s10.tex:17` "Section S6.4" is the right subsection.

### 1c. Findings

| # | file:line | problem | proposed replacement |
|---|---|---|---|
| 1 | `sections/06_atlas.tex:23-24` and `supp/s04.tex:53-54` | Main text says six settings (three race rules, e.p. on or off) and "all six"; S4 says "all nine settings ... all nine". RESULTS.md:218 says six, so S4 is wrong. Also main "Section S4 shows these positions" is not true: S4 shows the cylinder-only examples, not the compared positions. | main: "...in all six \lab{C1} (Section~S4 shows examples)." (drop "these positions"). S4 lines 53-54: "We compared six settings (three race rules, e.p.\ on or off) only for positions with at most four pawns; among them no value is cylinder-only in all six \lab{C1}." |
| 2 | `supp/s10.tex:16-17` | Stale after the Mobius proof: "a proof for the families, and the kings, remain open". Note 5 of S15 proves the three families (S). | "On the Mobius strip the least ring $\nim{2}$ is known for $n\le11$ (Section~S6.4) and one pawn per file suffices for $n\ge10$ (Section~S15); the least for $n\ge12$ and the kings remain open." |
| 3 | `sections/04_kings.tex:85-86` | The sentence carrying `\lab{S}` (certificate in the promotion game) has no reason in the paper, and the pointer says "exact clauses", not "proof". | "The exact clauses and the proof are in Section~S12.1;" (replace "The exact clauses are in Section~S12;") |
| 4 | `sections/08_star2.tex:116, 118, 126` | Three `\lab{S}` claims (n+3 wall rings, n-pawn families, *3 families) give a clause ("the same argument") but no pointer to which supplement section proves them; only 13_verify:15 says S12-S15 as a block. | add "(S13)" after the S at line 116, "(S14)" at line 118, "(S15)" at line 126, in the form `\lab{S} (Section~S13)` etc. (about 3 tokens each) |
| 5 | `sections/14_conclusion.tex:5` | "lists more problems than these four" is vague. | "Section~S10 lists two more." |
| 6 | `sections/13_verify.tex:15`, `tog.tex:143,152` | "full proofs of the S results (Sections S12-S15)": the S-labelled proofs of Prop. horizon1 and the (V2) test are in S2, not S12-S15. Minor. | "(mostly Sections~S12--S15)" or leave. |
| 7 | `supp/s14.tex:15`, `supp/s15.tex:14,19`, `supp_src/s15_note2.md:27` | "program A is the C program of Section S13 (rg.c ...)": S13 never names rg.c, it only says "Two independent programs build the same graph" (s13:68-70). Also `supp/s15.tex:367,379` / `supp_src/s15_note5.md:5,17` "Section S6" should be "Section S6.4" (rules) and "S6.3-S6.4" (scans). Table row labels S1..S6 in Notes 1-2 are easy to confuse with Sections S1..S6. | cosmetic: "the C program rg.c of Section S13" -> "the C program rg.c of the repository, used for Section S13"; "Section S6" -> "Section S6.4" |

## Task 2. Evidence labels

### 2a. Every `\lab{S}` in the paper

| file:line | claim | reason in main text? | full proof in supplement |
|---|---|---|---|
| 01_intro:43 | (V1)-(V3) give whole-board result; (V4) gives +-BIG value | sketch at 04_kings:62-67 | S12.1 A.11, A.13; S12.2 Thm 1.14 |
| 01_intro:44 | sum-safety theorem | sketch at 05_sums:63-67 | S12.1 A.4-A.7 |
| 04_kings:48 Thm validity | yes, proof sketch | yes | S12.1 A.11 |
| 04_kings:69 Cor v4 | two-line proof from two theorems | yes | S12.1 A.13 |
| 04_kings:85 certificate, promotion game | no | NO (finding T1.3) | S12.1 A.14-A.16, S2.1 Thm cert |
| 05_sums:57 Thm hss | sketch | yes | S12.1 A.7 |
| 08_star2:99 (Fig. 6 caption), 01_intro:51-52, 00_abstract "proof sketched" | n pawns, n>=10 | the walls paragraph 08_star2:112-119 gives the reason | S14 (induction n>=18/19, finite checks C2 for n=10..17) |
| 08_star2:116 | n+3 wall rings, n>=5 | wall paragraph | S13 (n0=17/16, C2 below) |
| 08_star2:118 | two n-pawn families, n>=10 | "the same argument" | S14 |
| 08_star2:126, 01_intro:52 | *3 with n+2 pawns (even n>=8, odd n>=11), n+1 pawns (n>=12) | "wall insertion" | S15.2 (even n+2), S15.3 (odd), S15.4 (n+1, even n>=12, odd n>=13) |
| 08_star2:136 | Mobius one pawn per file, strips of ten or more files | one clause ("cylinder's insertion proof away from the seam") + pointer S15 | S15.5 (m>=5 by insertion, m<5 finite) |

All `\lab{S}` results have a full write-up in S12-S15. Only 04_kings:85 lacks any reason in the main text.

### 2b. Label disagreements for the same claim

| # | places | disagreement | proposed fix |
|---|---|---|---|
| 1 | `sections/05_sums.tex:16` (C2 on the cylinder) vs `supp/s03.tex:51` (C1); `paper/ieee/sections/05_sums.tex:77` says C2 | Puzzle 2 king group "zugzwang for black only" on the cylinder: main C2, supplement C1. S3 says "(a C++ solver, a Python solver, and a third ...)" elsewhere; decide which is right | If C2 is right: `supp/s03.tex:51` "and on the cylinder \lab{C2}". |
| 2 | `sections/06_atlas.tex:23` (six settings) vs `supp/s04.tex:53-54` (nine) | see T1.1 | see T1.1 |
| 3 | `sections/01_intro.tex:52` ("n+1 pawns give a *3 on C11 (C2)") vs body | body (08_star2:124-126) states only n>=12 for n+1 pawns; C11 appears only in S6 and S10 | see T3 |
| 4 | `supp/s10.tex:10-11` vs main | S10 labels the minima "n+2 on C10, n+1 on C11 and C12 (C1)"; Fig. 6 caption says computed *3 minima are C1; intro labels existence on C11 C2. Consistent, but S10 should say "least ... C1" explicitly | optional |

## Task 3. Numbers repeated in abstract, introduction, conclusion

37 numbers/claims compared (abstract: six/seven pawns, twin, three programs, six pawns on three files, ten files, seven files/ten pawns/*3, 1/8, mate rates; intro: 8 ranks, 10-man, 233, 2.80%, eight endings, six pawns C3, ten pawns C7 to C10, n>=10, n>=12, C11, ten-pawn *3 on C7, 160 Lichess, Dawson n-3 and Grundy 0; conclusion: seven pawns four files, no six, nine make *3, 92.5% of 2,049, six ranks, 9 to 11 men, h about 5-7, "four problems"). All agree in value and wording except:

| # | file:line | what is wrong | proposed replacement |
|---|---|---|---|
| 1 | `sections/01_intro.tex:52` vs `sections/08_star2.tex:124-126` | Intro: "n+1 pawns give a *3 on C11 (C2)". Body gives n+1 pawns only "on every C_n with n>=12"; the C11 case (twelve-pawn ring, `supp/s06.tex`, C2) is not in the body. | in 08_star2:125-126: "and with $n+1$ pawns on $\cyl{11}$ \lab{C2} and on every $\cyl{n}$ with $n\ge12$ \lab{S}" (+5 tokens; or drop "on C11 (C2)" from the intro) |

## Task 4. Statements changed today

### 4a. Mobius rings

Main text is clean: `sections/08_star2.tex:132-136` has the new wording (S, "strip of ten or more files"); `paper/ieee/sections/08_star2.tex:188-203` and `paper/ieee/sections/14_conclusion.tex:19-21` are current ("least for n>=12 ... remain open" is correct, the least is unknown). No "up to 32 files" in `dist/tog/sections`, `paper/ieee/sections` or `submission/`. Leftovers:

| # | file:line | leftover | proposed replacement |
|---|---|---|---|
| 1 | `supp/s10.tex:16-17` | "a proof for the families ... remain open" (open question) | see T1.2 |
| 2 | `RESULTS.md:486-490` (outside the last-80-lines window, in the 2026-11-22 entry) | "two for n <= 32 (COMPUTED-1) ... a pumping proof looks feasible (CONJECTURE for all n)" and "from 10 to 32" | append: "Superseded: proved for every n >= 10 (entry 2026-11-23 below)." |
| 3 | `README.md:26-29` | cylinder ring claims are stale: "n, one pawn per file, for 10 <= n <= 60 (C1)" and "*3 with n+1 pawns on every C_n with 11 <= n <= 59 (C1)". The paper now says whole-board proofs (S) for n>=10 and n+1 pawns for n>=12 (S), C11 by C2. Also no Mobius line. | line 27: "It is n, one pawn per file, for every n >= 10 as a whole-board game (S); computed for n <= 60 (C1)." line 29: "Rings *3 with n+1 pawns exist on C11 (C2) and on every C_n with n >= 12 (S); on C11 n+1 is the least." |

### 4b. Order in S(X)

All statements describe test-before-split. `sections/05_sums.tex:45-47` ("a component in which a side has a passed pawn becomes +-BIG; otherwise it is re-split") is right but ambiguous about which component; `paper/ieee/sections/05_sums.tex:93-94` adds "The test comes before the split."; the 10-page text dropped that sentence. `supp/s12.tex` (core line 99 and long note 1.2) states the order; `supp/s03.tex` has no sentence describing S. Finding (low):

| # | file:line | proposed replacement |
|---|---|---|
| 1 | `sections/05_sums.tex:45-47` | "after a move, the moved component becomes $\pm\BIG$ if a side has a passed pawn in it (by the race rule if both have one); otherwise it is re-split along empty files (one ring if no file is empty); and the components add up" (same length) |

### 4c. Theorems need X without a passed pawn

Both main-text theorems (04_kings:49, 05_sums:58) and the ieee copies contain "X has no passed pawn". No conflicting statement in abstract, intro, S2, S3, submission files (none of them states the theorems). One omission (low): the main Theorem validity does not say the board needs at least five ranks, which `supp_src/s12a_core.tex:215` assumes ("In this part H >= 5"; A.2(c)); A.3 also notes the race rule is assumed local.

| # | file:line | proposed replacement |
|---|---|---|
| 1 | `sections/04_kings.tex:49` | "let $X$, the position without $Z$, have no passed pawn, on a board of at least five ranks, and suppose" (+7 words; only if space allows, all boards in the paper have at least six ranks) |

### 4d. Engines on sums

| # | file:line | leftover | proposed replacement |
|---|---|---|---|
| 1 | `README.md:35-36` | "On sums of components, engines often miss the model's winning moves (C1)." (withdrawn, RESULTS.md:20-28 and Section XII) | delete the sentence; or "A test of engines on sums was withdrawn and is future work." |

`sections/12_engines.tex:59-63`, `sections/01_intro.tex` (engine bullet), `paper/ieee/sections/12_engines.tex:63-73`, `supp/s09.tex`, `dist/tog/submission/*` are clean.

## Task 5. Submission files against the PDFs

Verified true against the current PDFs: 10 pages (tog, tog_review), 95 pages (both supplements), 20 references (`build/*.bbl` 20 `\bibitem`, PDF list ends at [20]), 7 figures, 5 tables (TABLE I-V), abstract 199 words and `scholarone_fields.md` abstract is identical to `sections/00_abstract.tex`, AI-use statement identical to `tog.tex:140-152`, title identical, Sections II-XIII and S12-S15, S1-S11, S16 as described, cover-letter results 1-4 match the abstract/body, anonymity text search of both review PDFs: 0 hits for aritro, bhattach, illinois, morley, uiuc, urbana (re-run today). `tog.tex:26` and `supplement.tex:27` still hold the `\anoncodeurl` placeholder as SUBMIT_STEPS says.

| # | file:line | what is wrong | proposed replacement |
|---|---|---|---|
| 1 | `submission/scholarone_fields.md:47` | Quotes the paper's availability paragraph and adds "Our CGT engine is in Python 3 (standard library only) and the fast solvers are in C." That sentence is no longer in Section XIII or in the supplement. | delete that sentence; keep "The supplementary material gives the full proofs of the [S] results (Sections S12-S15) and the FEN of every position with kings (Section S11)." |
| 2 | `submission/pdf_checks.md:87` | quotes B line "at anonymized repository link. Our CGT engine is in Python 3" (old text); current line: "at anonymized repository link. The supplementary material" | "B line "at anonymized repository link. The supplementary material gives the full proofs" (Section XIII)" |
| 3 | `submission/pdf_checks.md` table row "File size (bytes)" | 260053 / 259629 / 652138 / 651948 are from the 17:58 build; current sizes are 260856 / 260294 / 759840 / 759580 (matches `files_to_upload.md`). Sizes only, hashes not recomputed here. | update the row to the current sizes; add "text search re-run 2026-11-23, 0 hits"; the fonts and URI rows were not re-run in this audit |
| 4 | `submission/cover_letter.md:3` | Date "22 November 2026" (today is 23 November); flagged by the file as author-confirm | author sets the date on the day |
| 5 | `submission/pdf_checks.md:3` | "Run on 2026-11-22 on the PDFs built at 17:58"; PDFs were rebuilt 2026-11-23 10:05 (page-count row says refreshed, other rows not) | state that rows 2, 3, 5 were not re-run |

## Task 6. LaTeX hygiene (`dist/tog/sections/*.tex`, `tog.tex`, `macros.tex`)

0 findings. 60 labels, 71 `\ref` uses: no `\ref` to a missing label, no duplicate label (also none among supplement labels, and every `\ref` in `supp/s*.tex` resolves). 0 occurrences of `??` in `pdftotext` of `tog.pdf`, `tog_review.pdf`, `supplement.pdf`, `supplement_review.pdf`. Build logs: no undefined reference or citation, no multiply defined label, 0 Overfull boxes. All 20 `\cite` keys exist in `refs.bib` (one extra bib entry, PyTorch, is cited only in the 15-page version). Labels defined but never referenced (fine): cor:v4, eq:dawson, fig:kings, fig:star2, fig:star2_seven_b, lem:sandwich, prop:cylonly, prop:eighth-real, sec:conclusion, sec:intro, sec:kings-sweep, sec:kpk, sec:real-cand, sec:real-eighth, sec:star2-five, sec:verify, thm:eighth, thm:oracle-cand, thm:star2seven.

## Checked and fine

- All 26 pointer groups of Task 1a, including S1 (4,070 numbers), S2 (92.5%, 2,154, h 5-7), S3 (19.3%, 540,503 HSS, real-king 19 sums / 38 sides), S5, S6 (every ring family, Mobius table 6,8,6,8,8,8 / 6,7,8,9,10,10 / 10,10,11 equal in main and S6.4), S7 (302 end-position sides, 283+5+2=290), S8 (216 vs 160, widths), S9 (31 of 301, 56 wrong, order 638, 109 P), S16.
- Supplement internal pointers S6.2/S6.3/S6.4, S13/S14/S15 in notes, Note 5 pointers to S6, S14 (C1M exists), S15 section 2b.
- Theorem statements in S12.1 match the main text (V1-V3, V4, (E), HSS, "either side in any order", test-before-split, no passed pawn in X); `supp/s12.tex` is a line-for-line copy of `supp_src/s12a_core.tex` after its \section line.
- S labels agree between abstract, intro, body and conclusion for: one pawn per file n>=10 (S), n+3 wall (S), *3 families (S), Mobius (S), validity/HSS (S), 1/8 (C2), Tiny 1 (C1), real-chess 1/8 (C1), tablebases (C2), Dawson (P).
- Arithmetic inside the body: 159 = 107+18+34, 52 = 18+34, 159-31 = 128, 55,195 x 15 x 3 = 2,483,775 (x2 = 4,967,550), 233 = 181+52, Table V class sizes + 7 decided = 233, 53 = 40+13, 24 tables = 8 x 3.
- Table II default row: 11,300/58,595 = 19.3%; 540,503 HSS.
- 4a in `sections/`, `paper/ieee/sections/`, `supp/s06.tex`; 4b in all of them plus `supp/s12.tex`; 4c in `sections/`, `paper/ieee/sections/`, `supp_src/s12a_core.tex`, `submission/*.md`; 4d in `sections/`, `paper/ieee/sections/`, `submission/*.md`, `supp/s09.tex`, last 80 lines of RESULTS.md (they say the test was withdrawn).
- Not verified (outside scope): hashes, fonts, URI scan, page-image checks, whether any external numbers (e.g. 18,137) recompute.
