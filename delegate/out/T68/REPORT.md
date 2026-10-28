# T68: fact-check of ring and nimber claims

**Summary (5 lines).** Almost every ring/nimber claim in Sections I, VIII and XIV is supported by the repository (checked by running cylcgt on the C3 and C4 rings and by cross-checking the reports). The only hard error is the "about 24 million rings on up to 24 files" sentence, which conflates two different searches. A few labels are conservative (C1 where C2 would be justified) and one scope sentence is easy to misread.

| Paper claim (short) | Loc | Source | Verdict | Correct text if not OK |
|---|---|---|---|---|
| cylinder-only values come from rings [P] | 01:40 | RESULTS §6; atlas | OK | — |
| no *2 with <=6 pawns on ordinary boards of any width; *2 with 7 [C2] | 01:44 | RESULTS §1, §6b | OK | — |
| on C3 a six-pawn ring suffices [C2] | 01:45 | 08:133; cylcgt C3=*2 | OK | — |
| a ring needs ten on C7-C10 [C2] | 01:45 | c9_rings; RESULTS §6c | OK | — |
| only n, one per file, for 10<=n<=60 [C1] | 01:46 | c9_rings REPORT | OK (label weak: n=10-14 are CHECKED-2) | — |
| whole-board game has n+2 *2 for n=8 and n>=10 [AI] | 01:46 | RESULTS §6d | OK | — |
| on C7 some ten-pawn rings are *3 [C2] | 01:46 | RESULTS §6c | OK | — |
| textbook candidate W a2 c2 / B b7 d7: *2 textbook, {2+-1\|-2+-1} e.p.-aware [C2] | 08:30-44 | RESULTS §1; realchess | OK | — |
| census 6724 zeros, 4042 stars; textbook 6470 zeros, 3891 stars + candidate | 08:48-58 | RESULTS §1 | OK | — |
| A (W a4 b3 d2 d3 / B a7 b7 c5) and B (W b4 c2 d2 / B a6 a7 c6 d5) are *2 [C2] | 08:64 | RESULTS §6b | OK | — |
| widths 1-4: 5,503,282 roots; two *2 at 7 pawns, four at 8 [C1/C2] | 08:111 | star2_frontier | OK | — |
| five files: 14,680,983 eight-pawn positions, 21 *2 [C1] | 08:120 | T21b | OK | — |
| 14 eight-pawn *2 rings on C5 [C1] | 08:124 | star2_frontier | OK | — |
| C3 six-pawn ring W a2 a3 b2 / B b7 c6 c7 [C2] | 08:133 | cylcgt (verified *2) | OK | — |
| C4 seven-pawn rings W a4 b2 c2 / B b6 c5 d6 d7 and twin [C2] | 08:134 | cylcgt (verified *2) | OK | — |
| C6 first rings: nine pawns, six *2 [C1]; e.g. W a4 c4 d2 e2 / B b6 b7 d6 e5 f6; three + twins [C2] | 08:137 | RESULTS §6c | OK | — |
| C7: no nine-pawn *2 [C2]; 63 ten-pawn *2 [C1]; e.g. W a2 a3 c3 e3 f2 / B a4 b5 d5 f5 g5 [C2] | 08:140 | RESULTS §6c | OK | — |
| C8: no nine-pawn [C2]; 18 *2 and 2 *3 at 5+5 [C1]; e.g. W a3 b3 c3 d2 f2 / B b6 d5 e5 g4 h5 [C2] | 08:143 | RESULTS §6c | OK | — |
| C9: ten least; no nine-pawn *2; seven ten-pawn *2 [C2] | 08:146 | c9_rings | OK | — |
| C10/C11 n-pawn *2 examples and n<=60 family [C2/C1] | 08:147 | c9_rings | OK | — |
| wall family *2 for every n>=5 whole-board [AI]; rests on 144 and 104 nodes and n<17 [C2] | 08:152 | ring_family_proof | OK | — |
| n+2 pawns suffice for even n>=8 and odd n>=11 [AI] | 08:156 | ring_n_plus_2 | OK | — |
| C3 ring needs two e.p. captures; e.p. off gives 0 [C2] | 08:159 | T33, RESULTS §6c | OK | — |
| *3 single component, nine pawns, on four and five files [C2] | 08:161 | star3_single | OK | — |
| A beside a * group on six files is *3 [C2] | 08:163 | star3_hunt | OK | — |
| whole-board no *3 with <=8 pawns on up to 8 files [C1] | 08:165 | star3_hunt | OK | — |
| e.p. off eight pawns suffice (two examples) [C2] | 08:166 | RESULTS §6b | OK | — |
| C7 ten-pawn rings include 8 *3 [C2]; e.g. W a2 a5 c4 e2 f2 / B a7 b4 d7 e5 g7 | 08:169 | RESULTS §6c | OK | — |
| C8 ten-pawn *3 and n+2 family [AI] | 08:171 | ring_n_plus_2 | OK | — |
| no *4 in 134,920,191 ten-pawn one-component positions on five files [C1] | 08:174 | star4_hunt | OK | — |
| "about 24 million rings on up to 24 files" [C1] | 08:175 | core_wall (23.2M, n<=11); two_core (207,975, n<=24) | WRONG | Two separate searches: 23,235,751 core-in-wall rings (core width <=6, n<=11) and 207,975 two-core rings (up to 24 files); no *4 in either. Do not combine into one number. |
| two cores between walls: nimber => nim-sum [C1] | 08:176 | two_core | OK | — |
| open problem 3: n+3 (3<=n<=7), ten (7<=n<=10) [C2], n (10<=n<=60) [C1]; whole-board at most n+2 (n>=10) [AI] | 14:19 | RESULTS §6d | OK | — |
| "Is there a *4 on eight ranks?" | 14:22 | open problem | OK | — |

**Other things that read wrong.**
- 08:3-6 scopes the "no *2 with six pawns or fewer" claim to ordinary boards, which is correct, but the very next subsection exhibits the six-pawn C3 ring *2; a reader can miss the scope. (Pre-flagged in paper review r9; not a factual error.)
- The [C1] on the n-pawn family (10<=n<=60) is conservative: n=10..14 are CHECKED-2, so [C2] would be justified for that subrange.
- 14:4-6 summarizes *3 as "single-component *3 with nine pawns on ordinary boards and with ten on the seven-file cylinder"; this is true but omits that the ordinary-board *3 (nine pawns) is smaller than the cylinder one, which is the stronger result. (Flagged in review r8/r9.)
- No position printed in the three sections was found to be misconverted: the C10/C11 examples match M_10/O_11 (B4 W2 B6 W2 W3 B6 B7 W3 B7 W5 etc.) and the C3/C4 examples were re-run in cylcgt.