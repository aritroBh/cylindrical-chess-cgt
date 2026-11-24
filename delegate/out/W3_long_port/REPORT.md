# W3 long-version port report

Pairs paper/ieee/sections vs dist/tog/long BEFORE edits: identical = 03_basic, 04_kings, 06_atlas, 07_targets, 09_real, 11_dawson, appendix_positions, appendix_table; different = 00_abstract, 01_intro, 02_rules, 05_sums, 08_star2, 10_tablebases, 12_engines, 13_verify, 14_conclusion. After: 04_kings cmp OK, 09_real still identical.

Line counts of every dist/tog/long file unchanged (wc_before.txt / wc_after.txt; the diff is only the path prefix).

## Edits (file:line is the line of the old text; before/after are the replaced strings)

### 1 Cor V4
paper/ieee/sections/04_kings.tex:75
BEFORE: "If also (V4) $X$ is hereditarily sum-safe (Definition~\\ref{def:hss}) and satisfies condition (E) of\nTheorem~\\ref{thm:hss}, and $\\BIG$ exceeds the number of moves either side can make, the chess result is\nthe outcome class of the components' $\\pm\\BIG$ value."
AFTER:  "If also (V4) holds, that is, $X$ is hereditarily sum-safe (Definition~\\ref{def:hss}), satisfies condition (E) of\nTheorem~\\ref{thm:hss}, and $\\BIG$ exceeds the number of moves either side can make, then for that side to move\nthe chess result is the one given by the components' $\\pm\\BIG$ value."

### 1 Cor V4
dist/tog/long/04_kings.tex:75
BEFORE: "If also (V4) $X$ is hereditarily sum-safe (Definition~\\ref{def:hss}) and satisfies condition (E) of\nTheorem~\\ref{thm:hss}, and $\\BIG$ exceeds the number of moves either side can make, the chess result is\nthe outcome class of the components' $\\pm\\BIG$ value."
AFTER:  "If also (V4) holds, that is, $X$ is hereditarily sum-safe (Definition~\\ref{def:hss}), satisfies condition (E) of\nTheorem~\\ref{thm:hss}, and $\\BIG$ exceeds the number of moves either side can make, then for that side to move\nthe chess result is the one given by the components' $\\pm\\BIG$ value."

### 2 C2 label
paper/ieee/sections/01_intro.tex:31
BEFORE: '\\lab{C2}, two independently written programs agree,\nthe second written from the rules alone;'
AFTER:  '\\lab{C2}, two separately written programs agree,\nthe second from the rules alone (both AI-written; Section~\\ref{sec:verify}, Acknowledgment);'

### 2 C2 label
dist/tog/long/01_intro.tex:31
BEFORE: '\\lab{C2}, two independently written programs agree,\nthe second written from the rules alone;'
AFTER:  '\\lab{C2}, two separately written programs agree,\nthe second from the rules alone (both AI-written; Section~S17);'

### 3 real kings
paper/ieee/sections/05_sums.tex:150
BEFORE: 'Of the $38$ positions, $19$ are solved exactly\nand all agree with the outcome of the model sum; they include sums of two live components such as\n$\\{1\\mid0\\}+\\{1\\mid0\\}$ and $-1+\\{0\\mid-1\\}$. The other $19$ positions, among them every sum that is a\nsecond-player win, are only bounded, and no bound contradicts the model \\lab{C1}. So this test supports the sum\nmodel where one side wins outright and leaves the zero sums open.'
AFTER:  'Of the $38$ sides to move, $19$ are solved exactly\nand all agree with the outcome of the model sum; they include sums of two live components such as\n$\\{1\\mid0\\}+\\{1\\mid0\\}$ and $-1+\\{0\\mid-1\\}$. The other $19$ have only bounds, each consistent with the\nsum; all $19$ sums share one king placement \\lab{C1}. So this test supports the sum\nmodel where the solver is exact and does not contradict it elsewhere.'

### 4 oracle def
paper/ieee/sections/09_real.tex:13
BEFORE: "for white, or as worth $0$; in the last case the end position is $\\game{\\BIG r_W}{\\BIG r_B}$, where\n$r_W,r_B\\in\\{-1,0,1\\}$ are white's results with white and with black to move."
AFTER:  "for white, or as worth $0$, scoring the end position $\\game{\\BIG r_W}{\\BIG r_B}$ ($r_W,r_B\\in\\{-1,0,1\\}$ are\nwhite's results with white and with black to move; a dead draw is scored $\\star$)."

### 4 oracle def
dist/tog/long/09_real.tex:13
BEFORE: "for white, or as worth $0$; in the last case the end position is $\\game{\\BIG r_W}{\\BIG r_B}$, where\n$r_W,r_B\\in\\{-1,0,1\\}$ are white's results with white and with black to move."
AFTER:  "for white, or as worth $0$, scoring the end position $\\game{\\BIG r_W}{\\BIG r_B}$ ($r_W,r_B\\in\\{-1,0,1\\}$ are\nwhite's results with white and with black to move; a dead draw is scored $\\star$)."

### 5 engines class label
paper/ieee/sections/12_engines.tex:9
BEFORE: 'each labeled by its CGT class\n(Table'
AFTER:  'each labeled by its CGT class in the model\n(Table'

### 5 engines class label
dist/tog/long/12_engines.tex:9
BEFORE: 'each labeled by its CGT class\n(Table'
AFTER:  'each labeled by its CGT class in the model\n(Table'

### 5 engines text
paper/ieee/sections/12_engines.tex:17
BEFORE: '\\lab{C1}. The classes separate at a small fixed depth\n(Table~\\ref{tab:sf}). At depth~1 the engine reads hot positions, numbers and switches correctly\n$73$--$81\\%$ of the time, but infinitesimals only $30\\%$ ($26\\%$ at depth~2) and nimbers $53\\%$\n\\lab{C1}, consistent with tempo and parity fights, though nimbers and the class \\emph{other} are not clearly\nseparated at this sample size. Both classes reach $100\\%$ by depth~8.'
AFTER:  "\\lab{C1}. A verdict (win, draw or loss at $\\pm150$\\,cp) matches if it agrees with the tablebase.\nAt depth~1 (Table~\\ref{tab:sf}) the engine matches on hot positions, numbers and switches $73$--$81\\%$ of the time,\non infinitesimals $30\\%$ ($8$ of $27$) and on nimbers $53\\%$ \\lab{C1}. Infinitesimals trail the first three classes\n(Fisher's exact test, $p<0.001$ each) but not nimbers or the class \\emph{other}. Infinitesimals and nimbers reach\n$100\\%$ by depth~8."

### 5 engines text
dist/tog/long/12_engines.tex:17
BEFORE: '\\lab{C1}. The classes separate at a small fixed depth\n(Table~\\ref{tab:sf}). At depth~1 the engine reads hot positions, numbers and switches correctly\n$73$--$81\\%$ of the time, but infinitesimals only $30\\%$ ($26\\%$ at depth~2) and nimbers $53\\%$\n\\lab{C1}, consistent with tempo and parity fights, though nimbers and the class \\emph{other} are not clearly\nseparated at this sample size. Both classes reach $100\\%$ by depth~8.'
AFTER:  "\\lab{C1}. A verdict (win, draw or loss at $\\pm150$\\,cp) matches if it agrees with the tablebase.\nAt depth~1 (Table~\\ref{tab:sf}) the engine matches on hot positions, numbers and switches $73$--$81\\%$ of the time,\non infinitesimals $30\\%$ ($8$ of $27$) and on nimbers $53\\%$ \\lab{C1}. Infinitesimals trail the first three classes\n(Fisher's exact test, $p<0.001$ each) but not nimbers or the class \\emph{other}. Infinitesimals and nimbers reach\n$100\\%$ by depth~8."

### 5 intro engines bullet
paper/ieee/sections/01_intro.tex:56
BEFORE: 'Stockfish at low depth is weakest on infinitesimals \\lab{C1}.'
AFTER:  'Stockfish at low depth matches the tablebase least often on infinitesimals, significantly less than on hot positions, numbers and switches \\lab{C1}.'

### 5 intro engines bullet
dist/tog/long/01_intro.tex:56
BEFORE: 'Stockfish at low depth is weakest on infinitesimals, and on sums'
AFTER:  'Stockfish at low depth matches the tablebase least often on infinitesimals, significantly less than on hot positions, numbers and switches, and on sums'

### 6 2154
paper/ieee/sections/04_kings.tex:166
BEFORE: "Of the $2{,}154$ $8\\times8$ positions beside a tr\\'ebuchet whose real results we know, $105$ are"
AFTER:  "Of the $2{,}154$ $8\\times8$ positions beside a tr\\'ebuchet whose real results we could compute (not a random sample), $105$ are"

### 6 2154
dist/tog/long/04_kings.tex:166
BEFORE: "Of the $2{,}154$ $8\\times8$ positions beside a tr\\'ebuchet whose real results we know, $105$ are"
AFTER:  "Of the $2{,}154$ $8\\times8$ positions beside a tr\\'ebuchet whose real results we could compute (not a random sample), $105$ are"

### 6 92.5 conclusion
paper/ieee/sections/14_conclusion.tex:4
BEFORE: 'The model names the real winner in $92.5\\%$ of $2{,}049$ decisive $8\\times8$ positions; on six ranks a'
AFTER:  'On $2{,}049$ decisive $8\\times8$ positions that we could solve (not a random sample) the model names the real winner in $92.5\\%$; on six ranks a'

### 6 92.5 conclusion
dist/tog/long/14_conclusion.tex:3
BEFORE: 'Against real chess the model is right in $92.5\\%$ of the decisive $8\\times8$ positions we can check; on six ranks a'
AFTER:  'Against real chess the model is right in $92.5\\%$ of the decisive $8\\times8$ positions we could solve (not a random sample); on six ranks a'

### 7 threat
paper/ieee/sections/05_sums.tex:99
BEFORE: '\\emph{threat} for a side if a position reachable from it gives that side a passed pawn.'
AFTER:  '\\emph{threat} for a side if play on its own files can reach a position, with no passed pawn earlier, that gives that side a passed pawn (a race gives both sides one).'

### 7 threat
dist/tog/long/05_sums.tex:99
BEFORE: '\\emph{threat} for a side if a position reachable from it gives that side a passed pawn.'
AFTER:  '\\emph{threat} for a side if play on its own files can reach a position, with no passed pawn earlier, that gives that side a passed pawn (a race gives both sides one).'

### 8 E in our model
paper/ieee/sections/05_sums.tex:120
BEFORE: 'without (E) the decomposition already fails in the pure pawn game (Proposition~\\ref{prop:condE}).'
AFTER:  'without (E) the decomposition already fails in the pure pawn game (Proposition~\\ref{prop:condE}), and in our model \\lab{P} (the position is in the repository).'

### 8 E in our model
dist/tog/long/05_sums.tex:117
BEFORE: 'without (E) the decomposition already fails in the pure pawn game (Proposition~\\ref{prop:condE}).'
AFTER:  'without (E) the decomposition already fails in the pure pawn game (Proposition~\\ref{prop:condE}), and in our model \\lab{P} (Section~S12).'

### 8 count rule
paper/ieee/sections/05_sums.tex:123
BEFORE: 'on $\\cyl{8}$ with en passant off, $X=$'
AFTER:  'on $\\cyl{8}$ with en passant off and the count rule, $X=$'

### 8 count rule
dist/tog/long/05_sums.tex:120
BEFORE: 'on $\\cyl{8}$ with en passant off, $X=$'
AFTER:  'on $\\cyl{8}$ with en passant off and the count rule, $X=$'

### 8 C1 on real bullet
paper/ieee/sections/01_intro.tex:50
BEFORE: 'however draws are treated;'
AFTER:  'however draws are treated \\lab{C1};'

### 8 C1 on real bullet
dist/tog/long/01_intro.tex:50
BEFORE: 'however draws are treated;'
AFTER:  'however draws are treated \\lab{C1};'

### 8 two queens
paper/ieee/sections/04_kings.tex:160
BEFORE: '(queen promotions only, at most two). Of these'
AFTER:  '(queen promotions only, at most two queens at a time). Of these'

### 8 two queens
dist/tog/long/04_kings.tex:160
BEFORE: '(queen promotions only, at most two). Of these'
AFTER:  '(queen promotions only, at most two queens at a time). Of these'

### 8 eight ranks
paper/ieee/sections/02_rules.tex:9
BEFORE: 'with $n$ files and eight ranks.'
AFTER:  'with $n$ files and, unless we say otherwise, eight ranks.'

### 8 eight ranks
dist/tog/long/02_rules.tex:9
BEFORE: 'with $n$ files and eight ranks.'
AFTER:  'with $n$ files and, unless we say otherwise, eight ranks.'

### 8 R
paper/ieee/sections/13_verify.tex:8
BEFORE: '$15$ reference games $X$: all\n$4{,}967{,}550$ outcomes of $G+X$ match'
AFTER:  '$15$ reference games $R$: all\n$4{,}967{,}550$ outcomes of $G+R$ match'

### 8 R
dist/tog/long/13_verify.tex:8
BEFORE: '$15$ reference games $X$: all\n$4{,}967{,}550$ outcomes of $G+X$ match'
AFTER:  '$15$ reference games $R$: all\n$4{,}967{,}550$ outcomes of $G+R$ match'

### 8 n<=61
paper/ieee/sections/08_star2.tex:154
BEFORE: 'two programs check $n<17$ \\lab{C2}'
AFTER:  'two programs check $n\\le61$ \\lab{C2}'

### 8 n<=61
dist/tog/long/08_star2.tex:154
BEFORE: 'two programs check $n<17$ \\lab{C2}'
AFTER:  'two programs check $n\\le61$ \\lab{C2}'

### 9 five-file
paper/ieee/sections/09_real.tex:72
BEFORE: 'beside T, has $12$, with only file f free of pawns between them. Their oracle'
AFTER:  'beside T, has $12$; no file between its pawns and T is free of pawns, so Theorem~\\ref{thm:validity} does not apply. Their oracle'

### 9 five-file
dist/tog/long/09_real.tex:72
BEFORE: 'beside T, has $12$, with only file f free of pawns between them. Their oracle'
AFTER:  'beside T, has $12$; no file between its pawns and T is free of pawns, so Theorem~\\ref{thm:validity} does not apply. Their oracle'

### 10 Muller
paper/ieee/sections/../refs.bib:198
BEFORE: '  organization = {{XBoard} variant rules},\n'
AFTER:  '  organization = {{XBoard} variant rules},\n  year         = {n.d.},\n'

### 10 WuYuLandry
paper/ieee/sections/../refs.bib:136
BEFORE: 'howpublished = {Undergraduate course paper (Math 191)},'
AFTER:  'howpublished = {Undergraduate course paper (Math 191), Stanford Univ., Stanford, CA, USA},'

## No counterpart / not done
- 3 (real-king test): the long dist copy has no real-kings paragraph (only paper/ieee); no "second-player"/"38" claim in dist/tog/long. The paper/ieee closing sentence was changed from "supports the sum model where one side wins outright and leaves the zero sums open" to "where the solver is exact and does not contradict it elsewhere", because the old one implied bounded = zero sums.
- 8 "other 12 are races" (302 sentence): already present in 09_real.tex (both copies); no edit.
- 8 "At most two queens": only in 04_kings.tex (both copies, identical).
- 6: 04_kings already says (line 168) "These positions are the ones our other runs solved, not a sample of a defined class"; I only changed "we know" to "we could compute (not a random sample)", so the two statements now sit together.
- 2: paper/ieee does not cite the supplement; it points to Section~\ref{sec:verify} and the Acknowledgment (13_verify says who wrote and checked the proofs; main.tex Acknowledgment says AI assistants wrote the programs). dist/tog/long has no such statement in 13_verify; it already cites the supplement as Section~S6.4 (14_conclusion), so it points to Section~S17.
- 8 (E) "in our model P": paper/ieee has no S references, so it says "(the position is in the repository)"; dist long says Section~S12 (Remark "(E) cannot be dropped", flat board 5 files, 7 ranks, a4 b3 e2 / a5 b4 e4).
- Not ported (not listed): abstract wording change ("give conditions for frozen kings to match chess"; paper/ieee abstract still says "state when frozen kings give the chess result"); 01_intro "(Sections sums and dawson)" instead of the puzzles table (Table I stays); Section~S3 pointers.
- Item 5 "($26\%$ at depth 2)" dropped as in the 10-page version.
## Item 9: checks of the position
T = W Kf5 g4 / B Kh4 g5 occupies files f-h; its king group's buffer is file e. The five-file nim2 W a3 b3 c2 e2 / B a6 c5 d5 e3 uses files a-e, and e holds pawns (e2, e3): no pawn-free buffer, Theorem validity does not apply; old text "only file f free" was wrong (f holds the white king). Positions A (W a4 b3 d2 d3 / B a7 b7 c5) and B (W b4 c2 d2 / B a6 a7 c6 d5) use files a-d only, so file e is free of pawns and is a buffer: the validity theorem's buffer condition holds for both; what the text says about A and B ("11 men beside T", oracle values open) is not false, no change made.
## Builds
Long version (paper/ieee/build_w3): main 16 pages, main_review 16 pages (the brief said 15 anonymous: +1). No undefined references or citations (only 4 TU/ptm font-shape warnings each), 0 Overfull boxes. No PDFs copied; no aux/bbl needed beside sources.
Supplement: build_supplement.py ran ("ok"). diff of dist/tog/supp vs saved copy (supp_before): only s02.tex (two sentences: "at most two queens at a time", "we could compute (not a random sample)"), s06.tex (n<17 -> n<=61), s07.tex (five-file line). supplement.pdf and supplement_review.pdf (dist/tog/build): 106 pages each, no undefined references (only font warnings).
