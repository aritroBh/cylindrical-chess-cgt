# V1 pointer audit: 10-page paper vs 67-page supplement

Scope: `dist/tog/tog.pdf` (10 pages) against `dist/tog/supplement.pdf` (67 pages). Read-only; nothing under `paper/` or `dist/` was changed. Both PDFs are byte-identical to `dist/tog/build/tog.pdf` and `build/supplement.pdf`. The paper's numbering (Definition 1, Theorem 2, Theorem 3, Corollary 4, Definition 5, Theorem 6, Proposition 7, Proposition 8, Theorem 9, Theorem 10, Theorem 11, Definition 12, Lemma 13, Theorem 14, Proposition 15, Theorem 16; Tables I-IV; Figs 1-7) was read from `build/tog.aux` and confirmed in the PDF text. "p." is the printed page of the supplement, which equals the PDF page.

## Totals

| Group | Items | PASS | FAIL | UNSURE |
|---|---|---|---|---|
| 1 Pointers paper to supplement | 44 | 40 | 1 | 3 |
| 2 Evidence labels | 46 | 31 | 0 | 15 |
| 3 Abstract and conclusion numbers | 25 | 25 | 0 | 0 |
| 4 Figures 1-7, Tables I-IV | 11 | 10 | 0 | 1 |
| 5 Internal cross-references in the paper | 4 | 4 | 0 | 0 |
| 6 Inside the supplement | 10 | 7 | 2 | 1 |
| 7 Reference list | 3 | 3 | 0 | 0 |

## Group 1. Pointers from the paper to the supplement

| # | Paper (quote) | Target and page | Verdict |
|---|---|---|---|
| 1 | "(ours are AI-written; Section S17)" (Intro, label C2) | S17, pp. 64-67. S17 says who wrote and checked the S proofs and lists programs only for the ring/loopy proofs (Tables S9, S10). It names no program behind any C1/C2 claim of Sections II-XII. | UNSURE |
| 2 | "Positions of value 1, 2, star and up are in the supplementary material, Section S1." (Fig. 2 caption) | S1.2, S1.3, Fig. S2, pp. 2-3. Values 1, 2, star, up all there. | PASS |
| 3 | "changes at least 18,137 of the 231,071 values, 4,070 of them in outcome <C1> (Section S1)" | S1 p. 1: same numbers, same scope (at most six pawns, width at most four). | PASS |
| 4 | "derivations of 1, 2, star, up and double-up star are standard and are in Section S1" | S1.2-S1.3 p. 3 (double-up star at end of S1.3). | PASS |
| 5 | "the Forsyth-Edwards Notation (FEN) of every position with kings" (Intro); "the FEN of every position with kings (Section S11)" (XIII) | S11 p. 16 says "Table S8 gives the FEN of each main position with kings". Positions with kings that have no FEN there: S2.1 p. 4 (Kb4,Pe4 v Ka1,Pa2; Kb4-c5 and Kc5-d5 examples), S8 p. 13 (Ka3,Rb2 v Ka1; Ke6,Be1,Bf1 v Ke8), S8.1 pp. 13-14 (Ka4,Pb7 v Ka6; Ka3,Ph2 v Kg2,Ph3; Ka1,Pa7 v Ka3), A.13 p. 21, A.16 remark p. 23, S2.1 trebuchet beside locked pairs. The supplement's own p. 1 also says "every position with kings". | FAIL |
| 6 | "The full proof is in Section S12." (Theorem 3) | A.11 p. 21 (states "Theorem 3"; needs at least five ranks, A.12(c)). | PASS |
| 7 | "The exact clauses and the proof are in Section S12" (certificate of horizon h) | A.14 (C1)-(C3) p. 22, A.15, A.16 pp. 22-23. Clauses match S2.1 (i)-(iii). | PASS |
| 8 | "a local test for (V2) and the loopy games of kings with spare moves are in Section S2" | S2.1 p. 4 (Prop A.19, p. 26, Cor A.19a p. 27), S2.2 p. 4 (Theorem S4 = A.18a pp. 24-25). | PASS |
| 9 | "The rule is not sound on every board (Section S16)." | S16 p. 64: W a4 b6 / B c7, three files, 8 ranks. Agrees with S2.3 p. 4-5. | PASS |
| 10 | "Of 2,154 positions ... 105 are draws; in the other 2,049 the model names the winner in 92.5%, against 83% and 84% ... (Section S2)" | S2.3 pp. 4-5 and Fig. S3: 1896/2049, 1701/2049, 1714/2049 = 92.5, 83.0, 83.7. The same pages give 500, 159 = 107+18+34, 52, 31, 128. | PASS |
| 11 | "(Section S3 shows them and tabulates the claimed and the exact values)" | S3.1 Table S1, Fig. S4, pp. 5-6. Puzzle 1, 2, 3 statements match (hot h/a part, black-only zugzwang, tiny(1) and the legal copy W c2 c4 d4 / B c3 d5 d6 d7). | PASS |
| 12 | "The full proof, by induction with (E), is in Section S12." (Theorem 6) | A.7 p. 19 (induction on Phi_W + Phi_B). | PASS |
| 13 | Paper Theorem 6: "B exceeds the number of moves one side can make in any sequence of pawn moves from X" | A.7 p. 19 quotes the main text as "B exceeds the number of moves either side can make." Same meaning (B > N(X)); the quoted wording is not the printed wording. A.13 p. 21 also quotes Corollary 4 without "(Definition 5)". | UNSURE |
| 14 | "without it, sums fail even in the pawn game with no passed-pawn rule <C1> (Section S3)" | Proposition S5 <C1>, S3.2 p. 6 (W a4 f4 / B b4 e5, 6 files, 6 ranks). | PASS |
| 15 | "and in our model <S> (Section S12)" | Remark "(E) cannot be dropped", p. 20 (5 files, 7 ranks, W a4 b3 e2 / B a5 b4 e4; labelled <P> there). | PASS |
| 16 | "Elsewhere they can differ, even in outcome (Section S3)" | S3.3 p. 6. | PASS |
| 17 | Proposition 7: "on C8 with en passant off and the count rule, X = W b2 d4 g3 h5 / B a7 c7 f7 g4" | A.14 p. 21 (header says "Proposition 7"): same position and settings; (a),(b) hand-proved, (c) computed. | PASS |
| 18 | "the highest temperature is 3 <C1> (Section S4)" | S4.1 p. 8 (W a2 b4 / B a5 b7, +-3). | PASS |
| 19 | "Section S4 shows examples." | Fig. S5, Prop S6, pp. 7-8; numbers 53 = 40 + 13 agree. | PASS |
| 20 | "The checks ran on its mirror image (Section S5)." | S5 p. 8. | PASS |
| 21 | "A textbook-test 1/8 and up-second in the census fail under the e.p.-aware test (Section S5)" | S5.2 p. 9. | PASS |
| 22 | "(Section S6 gives the details)" (candidate, hot game) | S6.1 p. 9: {2+-1 | -2+-1}, mean 0, temperature 2. | PASS |
| 23 | "their pawns can arise in a game (Section S6)"; "its analysis matches move for move (Section S6)" | S6.2 p. 9 (A by a2-a4, b2-b3, c2xd3, c7-c5; B by mirror). | PASS |
| 24 | "(Section S6): it finds no *k with k>=2 with six pawns or fewer ... Section S6 gives the counts on five files" | S6.3 pp. 9-10 (scan of at most seven pawns on up to nine files; 21 eight-pawn *2 on five files). | PASS |
| 25 | "Section S6 lists example rings, counts and checks for every n." | S6.3 pp. 9-11 lists rings for n = 3..12 and families for all n (the n up to 20 in Fig. 6 rest on the family statements). | PASS |
| 26 | "none of the 134,920,191 ... about 24 million rings or of 1.8 billion positions ... (Section S6)" | pp. 10 and 12 (S6.3, S6.5). | PASS |
| 27 | "6, 8, 6, 8, 8, 8 pawns for n = 3..8 ... against 6, 7, 8, 9, 10, 10 ... 10, 10, 11 for n = 9, 10, 11 ... (Section S15)" | Table S4 p. 11 gives exactly these; Note 5 pp. 54-59. | PASS |
| 28 | "the other non-default *2 positions are open (Section S7)" | S7 p. 12. | PASS |
| 29 | "needed 6.1e10 states in 15.6 h (Section S7)" | S7.1 p. 12. | PASS |
| 30 | "Section S8 gives the counts, other widths C3 to C10 and KPKP." | Table S6 p. 13, Table S7 and text p. 14 (n = 9, 10 in text, 79.41%, 79.94%). | PASS |
| 31 | "(Section S9 shows the boards)" | Fig. S7 p. 14. | PASS |
| 32 | "the next quotient did not finish (Section S9)" | p. 15 (order 638, 109 P-positions, at most 32 files). | PASS |
| 33 | "A learning experiment on Dawson's chess is in Section S9." | S9.1 p. 15. | PASS |
| 34 | "full proofs of the <S> results (Sections S12-S15)" | S12 p. 17 to S15 p. 63. | PASS |
| 35 | "Section S10 lists two more problems." | S10 p. 15-16 lists six; main lists four. | PASS |
| 36 | "In the promotion game even a locked pair can break a trebuchet's zero <C2> (Section S2)" | S2.1 p. 4 (W e3 / B e4 versus W e2 / B e3, 1...Kd2). | PASS |
| 37 | "Theorem 16 (Ring rule; <P>, machine-checked for n <= 22)" | S9 p. 15 gives the argument but nowhere says a check for n <= 22 was run (grep for "machine", "22" finds nothing). The proof is in the paper, so the label P is not at risk; the "machine-checked" claim has no target. | UNSURE |
| 38 | Dawson facts: "period 34 with last exception n = 51 ... n<=300"; "31 of the 301 values ... 56 ... first at n = 4"; "n = 3,7,11,17,23,27,31,37,41,45,57" | p. 15 states the first three; I recomputed g(n) from recurrence (1): period 34, last exception 51, and g(n-3)=0 exactly for 3,7,11,17,23,27,31,37,41,45,57,61,65. | PASS |
| 39 | VIII-E numbers: n+3 for n = 3..7; ten on C8, C9; n<=61 two programs; n<=12 sums; nine-pawn *3 on four files; eight ten-pawn *3 rings on C7; C11 twelve-pawn *3 | S6.3 pp. 9-10: all match. | PASS |
| 40 | IX-B numbers: 302 / 290 / 283 / 5 / 2 / 12; one 8-man plus three 9-man positions; 10 and 12 open; five and seven 8-man end positions for A and B | S7.1 pp. 12-13: all match. | PASS |
| 41 | Table III and X-A numbers: 2.80%, 0.66%, 24 tables, 607 million, 326,640, 6 differing, 16,538, 15,930, 216 v 160 | S8 pp. 13-14: all match. | PASS |
| 42 | Theorem 14 (a)-(c) | Theorem S7 p. 12: identical statements. | PASS |
| 43 | Theorem 9 (1/8, all nine settings) | S5 p. 8 (C solver confirms both parts; third solver, nine settings). | PASS |
| 44 | Theorem 11, positions A and B, analysis | S6.2 p. 9: same moves, same values (2 and 3 replies, +B). FENs in Table S8 p. 16 match the paper's pawn lists (checked all 14 FENs against their men lists). | PASS |

## Group 2. Evidence labels

Counts of `\lab{}` in the paper sources: C2 51, C1 37, S 20, P 8, Conj 1 (the Conj instance is only the label definition; no claim carries it).

### S and P labels

| # | Paper claim (quote) | Proof / support in supplement | Verdict |
|---|---|---|---|
| 2.1 | Theorem 3 "Validity of the convention; <S>" | A.11 p. 21 | PASS |
| 2.2 | Corollary 4 "<S>" | A.13 p. 21 | PASS |
| 2.3 | "such a move loses for its mover <S>" (promotion game) | A.16 pp. 22-23 (Theorem S1 p. 3). | PASS |
| 2.4 | Theorem 6 "Sum safety; <S>" | A.7 p. 19 (Lemmas A.4-A.6 pp. 19-20). | PASS |
| 2.5 | "and in our model <S> (Section S12)" | Remark p. 20. | PASS |
| 2.6 | "this gives a ring *2 with n+3 pawns on every C_n with n>=5 <S>, checked by two programs for n<=61 <C2>" | S13 Theorem 1 p. 28. Proof covers n >= 17 (odd) and n >= 16 (even) given computed C1 base graph; for n = 5..15 (odd) and 6..14 (even) the supplement says "this is C2" (p. 30). The paper discloses the C2 check but still labels the n>=5 statement S. | UNSURE |
| 2.7 | "The same argument proves the two n-pawn families above *2 as whole-board games for every n>=10 <S>" (also Fig. 6 caption "open ones proved for all n ... <S>") | S14 pp. 32-35. Proved for n >= 18 (even), n >= 19 (odd) given Lemmas 1-3 and computed base graphs; p. 32 states "The sizes n < n0 are covered only by C2, not by the induction", i.e. n = 10..17. | UNSURE |
| 2.8 | "Wall insertion gives a whole-board *3 with n+2 pawns on every C_n with even n>=8 and odd n>=11 <S>" | Notes 2 and 3, pp. 42-49. Note 2: "insertion proof gives Q_n = *3 for even n >= 22" (p. 42); Note 3: "PROVED for odd n >= 19 ... CHECKED-2 for n = 11..17" (p. 44). Small n are computation only. | UNSURE |
| 2.9 | "and on every C_n with n>=12 <S>" (*3 with n+1 pawns) | Note 4 pp. 50-53: proved for n >= n0 (T: 20, S: 23); smaller n CHECKED-2 (p. 51). | UNSURE |
| 2.10 | "on every strip of ten or more files ... <S> (Section S15)" (Mobius, one per file) | Note 5 pp. 54-59: "PROVED for m >= 5 ... the cases m < 5 are finite computations" (p. 54), i.e. n = 10..17 by computation. | UNSURE |
| 2.11 | "and n+1 pawns on every strip of n>=11 files <S>" | Note 6 pp. 60-63: proved for m >= m0 (n = 20, 23); smaller m by C2 (p. 60). | UNSURE |
| 2.12 | Cut lemma <P>,<C2> | Proof in the paper; reused S4.2 p. 8, A.1 p. 17. | PASS |
| 2.13 | "<P>" cancelling +B and -B (V-B) | A.8 p. 20. | PASS |
| 2.14 | Lemma 13 Sandwich <P> | Proof in the paper. | PASS |
| 2.15 | Theorem 16 Ring rule <P> | Proof in the paper; S9 p. 15 repeats the argument. ("machine-checked" part: group 1 row 37.) | PASS |
| 2.16 | Conj | No claim in the paper carries it. | PASS |

### C1 and C2 labels (S17 names no programs for any of these; see row 2.17)

"Program named" below means what the supplement says about who computed it. The supplement describes programs only generically ("independent C solver", "whole-board solver", "third program written from the rules alone").

| # | Paper claim (quote) | Where in supplement | Verdict |
|---|---|---|---|
| 2.17 | S17 as the place where C1/C2 programs are named (Intro) | S17 pp. 64-67 lists models per proof and base-case programs for S12-S15 only. For the 88 C1/C2 label uses in Sections II-XII it names nothing. | UNSURE |
| 2.18 | "an independent reference solver ... agrees with it on all 1,418,480 positions of its test runs <C2>" | Not in supplement. | UNSURE |
| 2.19 | Trebuchet mutual zugzwang, Fig. 3(a),(b) <C2> | p. 14 (two independent solvers, 4<=n<=8; Lichess for T). | PASS |
| 2.20 | Kings sweep 500 / 159 / 107 / 18 / 34 / 31 / 128 <C1> | S2.3 p. 4; program `research/v2_mechanisms/cc.py` named p. 64. | PASS |
| 2.21 | 2,154 / 2,049 / 92.5% <C1> | pp. 4-5, Fig. S3. | PASS |
| 2.22 | Puzzle 2 king group <C2> (our solver and tablebase) | S3.1 p. 6. | PASS |
| 2.23 | 599,098 positions, 540,503 HSS, 19.3% <C1> | Table S2 p. 7 (11,300 / 58,595 = 19.3%). The example "smallest being W a5 d3 / B b6 e4" is not in the supplement. | PASS |
| 2.24 | Proposition 7 <C2> | A.14(c) p. 21: "Checked by computer only"; number of programs not stated. | UNSURE |
| 2.25 | Real kings, 19 sums <C1> | Table S3 p. 7 ("One run per position, no independent re-run"). | PASS |
| 2.26 | Atlas "1,223,689 positions <C1>"; "independent minimax program confirms ... all 12,568 rings and 4,000 random ordinary components" | Not in supplement (S4 gives values only). | UNSURE |
| 2.27 | Atlas values: temperature 3, 53 cylinder-only (40 + 13), six-setting check <C1> | S4 pp. 7-8. | PASS |
| 2.28 | Table I counts (footnote "an independent C solver confirmed each identity <C2>"; e.p.-aware column <C1>) | S5 pp. 8-9 name the example positions only; the 13/3/1/5/10/13 and 9/2/0/2/10/16 counts and the C-solver confirmation of each identity are not in the supplement. | UNSURE |
| 2.29 | Theorem 9, up-second star, Tiny 1 <C2>/<C1> | S5, S5.1 p. 8. | PASS |
| 2.30 | Candidate hot game <C2> | S6.1 p. 9. | PASS |
| 2.31 | Theorem 10 "Census; <C2>": "6,724 zeros and 4,042 stars" | S6.2 p. 9 states the engine, "an independent C solver" and the whole-board solver agree, and 793,299 placements, but prints only the textbook-test counts (6,470 zeros, 3,891 stars). 6,724 and 4,042 appear nowhere in the supplement. | UNSURE |
| 2.32 | Theorem 11 and Table II "every entry is <C2>; for A and B, three programs agree on each" (abstract: "confirmed by three programs") | S6.2 p. 9 gives the hand analysis but never says three programs agree on A and B, and Table II is not reproduced. | UNSURE |
| 2.33 | "5,503,282 root positions <C1> ... our engine re-checked every one <C2>"; nine-file scan <C2> | S6.3 p. 9. | PASS |
| 2.34 | Ring minima n = 3..9, M10, O11, n<=61 <C2>; sums to n=12 <C1> | S6.3 pp. 9-10. | PASS |
| 2.35 | *3 claims (nine-pawn four-file, eight-or-fewer none <C1>, C7 eight rings <C2>, C11 twelve-pawn <C2>) | S6.3 p. 10. | PASS |
| 2.36 | Height claims (7 ranks, 4 pawns; 7 ranks, 6 pawns *3; 6 ranks; 5 ranks none) <C2> | S6.5 pp. 11-12, Table S5; 48 least-count positions agree between two programs; 5, 6 ranks and 3 files at 7 ranks rescanned by a third program. | PASS |
| 2.37 | "none of the 134,920,191 ... 24 million rings ... 1.8 billion ... <C1>" | pp. 10, 12. | PASS |
| 2.38 | Mobius values, Table S4, *3 on five and six files <C2> | p. 11. | PASS |
| 2.39 | Fig. 6 caption: "Filled markers are computed minima (<C2> for *2, <C1> for *3)"; "No *3 ring is known for n<=6 or n=9; ten pawns are the least on C7 and C8" | The supplement shows no scan establishing the *3 minima 10 (C7, C8), 12 (C10), 13 (C12). S10 p. 15 states "n+2 on C10, n+1 on C11 and C12 <C1>" without a scan; S6.3 gives a minimality result only for C11 ("no eleven-pawn ring there is *3"). For C7, C8 the supplement shows no *3 with 8 pawns or fewer and some with 10, but is silent on nine-pawn rings. "No *3 known for n<=6, n=9" is not stated. | UNSURE |
| 2.40 | Theorem 14, Prop 15, second candidate, lower bounds, 8-man end positions <C1>/<C2> | S7, S7.1 pp. 12-13. | PASS |
| 2.41 | Tablebases: 24 tables <C2>, Table III, Mobius/Klein, KPK, zugzwang counts <C2> | pp. 13-14. | PASS |
| 2.42 | Dawson <C2> (three uses) | p. 15. | PASS |
| 2.43 | Engines (Section XII): 233 positions, 181 / 52, Stockfish, Lc0, Table IV, ChessSums 26,000 / 418 / 37, five alpha-beta timeouts, independent minimax 4,887, 13 positions <C1>/<C2> | None of these appears in the supplement (only the LSTM experiment, S9.1 p. 15). | UNSURE |
| 2.44 | Conclusion <C1> (92.5%, square-rule repair) and <C2> (locked pair) | pp. 4-5, 64; p. 4. | PASS |
| 2.45 | Section XIII cross-check numbers (55,195; 4,967,550; 2,483,775; 1,070; 160 positions; unlabelled) | Not in supplement; unlabelled, so not counted as a label failure. | PASS |
| 2.46 | Intro bullet labels (duplicates of the above claims) | Same targets as above. | PASS |

## Group 3. Numbers in abstract and conclusion (all PASS, 25 checked)

Abstract (12): at most six pawns (VIII-B, VIII-D); seven pawns, once plus twin (VIII-C: A and B); three programs (VIII-C, Table II sentence); six pawns on three files (VIII-E); from ten files on, one per file (VIII-E); seven files, ten-pawn rings, star three (VIII-E); one-eighth, up-second star, Tiny 1 (VII); queen promotions only, frozen kings, one-eighth (IX-B); opposite-colored bishops (X); strip three files shorter, Grundy zero (XI, Theorem 16). Conclusion (13): seven pawns on four files and no six (VIII-C, D); nine pawns *3 (VIII-E); 2,049 and 92.5% (IV-B); 8x8 (IV-B); six ranks, square-rule test (IV-B); "two more problems" in S10 (checked, S10 lists six against four); n pawns / Fig. 6 (VIII-E); 1/8 with queen promotions and frozen kings (IX-B); four promotions (IX-B); 8-man end positions agree, 9 to 11 men unsolved (IX-B); four listed problems.

## Group 4. Figures and tables

| Item | Cited where | Caption vs text | Verdict |
|---|---|---|---|
| Fig. 1 | Intro | M10 = W b2 d2 e3 h3 j5 / B a4 c6 f6 g7 i7 matches the VIII-E text; image shows 10 pawns in (b) and 7 visible in (a) as stated; value *2 matches. | PASS |
| Fig. 2 | II-D, III | (a) W a2 / B b4, (b) W a4 h3 / B a5 h6, (c) tiny(1) position match the texts citing them; "nine settings" matches S2 caption p. 2; S1 pointer correct. | PASS |
| Fig. 3 | IV, V | (a),(b),(c) each cited; positions match S11 FENs; (c) draws with white to move, black-only zugzwang, matches V. | PASS |
| Fig. 4 | VII | (a)-(c) positions match the theorem and the text; "10-man" correct (6 pawns + T). | PASS |
| Fig. 5 | VIII-A, VIII-C | (a) and (b) cited as Fig. 5(a), 5(b); panel (c) (position B) is never cited by label in the paper (only S6.2 cites it). Caption values match Table II and the text. | PASS (note) |
| Fig. 6 | VIII-E, XIV | "ten pawns are the least on C7 and C8" and "No *3 ring is known for n<=6 or n=9" are in the caption only; the citing text says only that eight ten-pawn rings on C7 are *3 (support gap in group 2, row 2.39). | UNSURE |
| Fig. 7 | XI | Dots at g(m)=0 and cylinder 3x(m+3) match Theorem 16; list recomputed. | PASS |
| Table I | VII | Rows and "1/32 disappears" match text; counts not in supplement (row 2.28). | PASS |
| Table II | VIII-C | Entries agree with Theorem 11 and the sentences after it (candidate survives e.p. off; A and B need e.p.). | PASS |
| Table III | X (line-broken "Table / III") | Values match text (2.80%, KBBK 14 v 19, torus). | PASS |
| Table IV | XII (twice) | 73-81%, 30% (8 of 27), 53%, 100% by depth 8 match; class sizes sum to 226 = 233 - 7. | PASS |

## Group 5. Internal cross-references in the paper (all PASS)

(a) No "??" and no "[?]" in the PDF text; `build/tog.log` has no undefined references (only font-shape warnings). (b) 70 `\ref` uses in the sources, 0 undefined labels. (c) Printed statement numbers cited in prose are 2, 3, 4, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16; all exist (maximum is 16). (d) Printed section numerals cited (II, II-B, II-D, IV, IV-A, V, V-B, VI, VII, VIII, VIII-E, IX, X, XI, XII, II-XIII) all exist.

## Group 6. Inside the supplement

| # | Supplement text | Check | Verdict |
|---|---|---|---|
| 6.1 | "??" anywhere | None. | PASS |
| 6.2 | Item numbers A.1 .. A.19b | Items A.1-A.17, A.18, A.18a, A.18b, A.19, A.19a, A.19b are all defined (pp. 17-27); nothing refers above A.19b; parts A.I-A.VI all exist. | PASS |
| 6.3 | "Section S12.3" and other S-section references | No S12.3. All of S1.1-S15.6, S16, S17 referenced exist. Contents page numbers match actual pages. | PASS |
| 6.4 | Theorem S1, S4, S7; Proposition S2, S5, S6, S8; Conjecture S3; Tables S1-S10; Figs S1-S7 | All referenced items are defined. | PASS |
| 6.5 | References to main-text numbers (Definition 1, Theorem 2, 3, 6, 7, 9, 10, 16, Corollary 4, Table III, Figs 1, 3(a-c), 4(a-c), 5(a-c), Sections II-B, II-D, IV, IV-A, V-B, VI, VII, VIII-D, VIII-E, IX-A, IX-B) | All match the paper's printed numbering. | PASS |
| 6.6 | S3.3 p. 6: "(the first five-file *2 of Section VIII-D)" | The main text's Section VIII-D never mentions a five-file *2 (it says only "Section S6 gives the counts on five files"). The name "five-file *2" is introduced in S6.3 p. 10. | FAIL |
| 6.7 | S7 p. 12: "A second candidate, W a3 b3 c2 / B b5 b7 c6 ..., is *2 under the opponent rule with en passant on (Section VIII)" | Section VIII of the main text does not contain this position; it first appears in Section IX-A. (S6.2 p. 9 points to IX-A correctly.) | FAIL |
| 6.8 | pp. 23, 65, 67: "Theorem 3.4", "Proposition 2.11", "Corollary 2.11a" of `kings/theory/LOOPY.md`; p. 4: `kings/REPORT.md`, task K4 | These numbers belong to working notes outside the supplement; p. 23 maps them to A.18a, A.19, A.19a, so nothing dangles inside the PDF, but the numbers cannot be checked from the supplement. | UNSURE |
| 6.9 | S10 p. 15: "The main text lists four open problems; this is the full list of six." | Main text has four. | PASS |
| 6.10 | S2 p. 3: "the parts of Section IV of the main text that were moved out" | IV-A pointer and S2.1-S2.3 content match; the old 47-page S12.2 is not referred to anywhere. | PASS |

## Group 7. Reference list (all PASS)

The paper prints 20 references, [1]-[20]; all 20 are cited in the text, and all 42 `\cite` keys resolve against `dist/tog/refs.bib`. `PyTorch` is in the bib but only cited by the supplement, so it is not in the paper's list.
