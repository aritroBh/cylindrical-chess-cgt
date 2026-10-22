# Review: IEEE production

Verdict: Production-wise the build is clean. tectonic compiles with no errors, no undefined references and no Overfull boxes. Every figure and table is cited, figure captions sit below and table captions above in "TABLE I" style, the abstract is 195 words with no abbreviations, citations or equations, and there are five alphabetical Index Terms. Theorems share one counter with IEEE run-in heads, and there are no TODO, VERIFY or code listings. As a checkpoint this is fine. It is not yet ToG-submittable, for three reasons. It is 19 pages against a 10-page limit (12 with a justification). The double-anonymous rules are not met. The AI disclosure in the Acknowledgment is incomplete and says "A human check of the proofs is still pending." The rest are minor style, reference and layout fixes listed below.

## 1. [critical] paper/ieee/main.pdf (whole paper)
- **problem:** The PDF is 19 pages (pdfinfo). The GUIDELINES say ToG full papers are 10 pages including references, anything over 12 needs a written justification, and pages beyond 10 cost $200 each. The SPEC's own target was 12-14 pages, which is also exceeded.
- **fix:** Cut to 10-12 pages. Move Table VIII (Appendix, a full page on p.18) and the FEN listing to supplementary material, as the GUIDELINES G.5 note on Plambeck-Siegel suggests. Drop the chart figures that repeat table data (Fig. 12 = Table IV, Fig. 13 = Table V). Consider dropping the Fig. 1 cover photo, which takes 40% of column 2 on page 1. Shorten Sections XII-XIII, and merge VI/VII if needed.

## 2. [major] main.tex author block, Acknowledgment, macros.tex \repourl, sections/01_intro.tex lines 37-38 ('an unpublished 2025 study by the author'), refs.bib Bhattacharjee2025
- **problem:** ToG uses double-anonymous review. The byline, the e-mail footnote, the Morley thanks, the GitHub URL (it contains the user name aritroBh) and the first-person self-citation all identify the author. There is no anonymous build switch.
- **fix:** Add an \ifanonymous switch in main.tex. In anonymous mode: no author or e-mail, the Acknowledgment keeps only the AI disclosure, \repourl points to an anonymous.4open.science link (overriding it in main.tex, not macros.tex), and the 2025 study is cited in the third person ('an unpublished 2025 study [11]'). This is the orchestrator decision already listed under 'Conflicts with SPEC'.

## 3. [major] main.tex Acknowledgment; sections/13_verify.tex lines 60-68 (Use of AI Tools)
- **problem:** The IEEE AI policy requires naming every AI system, the sections where it was used and how much it did, including for manuscript text. The disclosure says 'Claude ..., Codex ..., and others', so not all systems are named. It mentions only the software, the searches and the proof drafts, although the manuscript text itself was drafted by AI writers (SPEC: 'Writers: subagents'). It also states 'A human check of the proofs is still pending.' That is fine for a checkpoint, but it must not remain in a submitted version, especially next to [P] labels.
- **fix:** Name every system used, taking the names from delegate/REVIEW.md (e.g., Claude, Codex, Nemotron Ultra via kilo, plus any others actually used). Say that AI drafted the manuscript text and figures, and in which sections. Remove 'and others'. Before submission, either complete the human proof check or downgrade the affected [P] labels and drop the sentence.

## 4. [major] sections/01_intro.tex line 32 (Fig. 1 caption); refs.bib CoverImage
- **problem:** The photo is CC BY-SA 3.0. The caption credits only 'Wikimedia Commons [10]', without the photographer or the license, which the license requires. ShareAlike also may not fit an IEEE copyright transfer. In addition, the caption begins with 'A', which IEEE style forbids.
- **fix:** Rewrite the caption, e.g., 'Cylindrical chessboard with all pieces on their starting squares; files a and h are adjacent. Photograph by S. Clair, Wikimedia Commons, CC BY-SA 3.0 [10].' Check with the editor that CC BY-SA material is acceptable, or drop the photo (this also saves space).

## 5. [minor] main.tex lines 64-68 (\thanks, \markboth)
- **problem:** The author footnote has no affiliation, city or country. \markboth puts the same author/title string on both sides, but the GUIDELINES want the journal name on the left ('IEEE Transactions on Games') and 'Bhattacharjee: Short Title' on the right.
- **fix:** \thanks{A. Bhattacharjee is with <affiliation>, <city>, <country> (e-mail: ...)}. Use \markboth{IEEE Transactions on Games}{Bhattacharjee: Chess Endgames on a Cylindrical Chessboard}, and leave the name out of the anonymous build.

## 6. [minor] main.tex line 91 (\appendices) and sections/appendix_positions.tex line 1
- **problem:** With a single appendix, \appendices + \section prints 'Appendix A: Positions'. The GUIDELINES (HOWTO XIII-A) call for \appendix[Positions], which gives an unnumbered 'Appendix'.
- **fix:** Replace \appendices and \section{Positions} with \appendix[Positions], keeping \label{app:positions}.

## 7. [minor] sections/05_sums.tex line 52 (Table I caption), sections/10_tablebases.tex line 87 (Table V caption)
- **problem:** The Table I caption starts with 'The' (not allowed in IEEE captions). The Table V caption has a lowercase word in Title Case ('...Legal Positions and white Wins...'), which shows as a mismatched small-caps W.
- **fix:** Table I: 'Puzzles of Fig. 5: Claimed and Exact Values [C2]'. Table V: '...Legal Positions and White Wins on the 8×8 Plane and Cylinder [C2]'.

## 8. [minor] sections/04_kings.tex line 1
- **problem:** In the heading 'Kings: the Trébuchet and When It Is Exact', the first word after the colon is not capitalized (IEEE Title Case).
- **fix:** 'Kings: The Trébuchet and When It Is Exact'.

## 9. [minor] sections/08_star2.tex lines 33-35 (eq. 1); sections/11_dawson.tex line 55 (eq. 2)
- **problem:** Both numbered equations are never referenced. Equation (1) also puts the evidence label [C2] inside the display, where it reads like math or a citation.
- **fix:** Either cite them as (1) and (2) in the text, or make them unnumbered displays (\[ ... \]). Move [C2] into the sentence ('...hot game [C2] with mean 0...').

## 10. [minor] macros.tex \lab and every use (e.g., 'value of a flat board [P]', '[C1]' next to '[11]')
- **problem:** Evidence labels in square brackets ([P], [C2], [C1], [Conj]) look the same as IEEE numeric citations ([2], [11]). This is especially confusing in captions and theorem heads with citations nearby.
- **fix:** Keep macros.tex unchanged, as the task requires, but raise it with the orchestrator. The fix would be to typeset the labels without square brackets (e.g., small caps in parentheses or a superscript), or to explain the convention in one line in Section I, which is partly done already. For now, avoid putting a label directly beside a citation.

## 11. [minor] refs.bib entries PyTorch, WuYuLandry2020, DrummondCole2005
- **problem:** (a) PyTorch lists six authors plus 'et al.'; the IEEE rule for more than six authors is first author plus 'et al.' (A. Paszke et al.). (b) The WuYuLandry2020 key says 2020, the entry says 2010, and the URL is a 2019 course page (19CSCI4341F). No source in the repo confirms the year or the spelling 'Yü'. The note also renders as lowercase 'accessed:'. (c) The Drummond-Cole title prints a literal '*2' instead of the star symbol.
- **fix:** (a) author = {Adam Paszke and others}. (b) Check the year and author spelling against the PDF and make the key match. Put 'Accessed: Oct. 21, 2026' after the URL; using @electronic makes IEEEtran capitalize it. (c) title = {Positions of value $\ast 2$ in generalized {D}omineering and chess}.

## 12. [minor] sections/03_basic.tex line 56, sections/07_targets.tex line 67
- **problem:** 'Let's begin...' and 'Let's see why...' are contractions, which IEEE editorial style does not allow.
- **fix:** 'We begin with the zero game...' and 'To see why, consider Fig. 8(a).'

## 13. [minor] main.pdf page 19 (References)
- **problem:** The last page is unbalanced: the references fill about 60% of the left column and the right column is empty.
- **fix:** Add \IEEEtriggeratref{N} before \bibliography, with N chosen so the columns balance (about the 8th or 9th reference), or load the balance package.

## 14. [minor] sections/10_tablebases.tex Figs. 12-13 vs Tables IV-V
- **problem:** Fig. 12 repeats Table IV, and its own caption admits the KRBK bar is 'too small to see'; most bars are 0 or 100, so the chart adds little. Fig. 13 repeats Table V. IEEE discourages showing the same data twice, and the paper is over length.
- **fix:** Drop Fig. 12, or replace it with a compact log-scale or dot chart. Drop Fig. 13 and keep Table V (or the reverse).

## 15. [minor] sections/08_star2.tex lines 139-146 (Five files paragraph)
- **problem:** The only Underfull \hbox (badness 2318) in the build: three long \pos{...} typewriter lists make visibly stretched lines in the PDF on p.11.
- **fix:** Put the three positions in a short itemize or a small table, or allow breaks inside \pos (e.g., \pos{W a3 b3 c2 e2} / \pos{B a6 c5 d5 e3} as separate units).

## 16. [minor] main.tex hyperref setup
- **problem:** The PDF has no Title or Author metadata (pdfinfo shows only Creator and Producer).
- **fix:** Add \hypersetup{pdftitle={Chess Endgames on a Cylindrical Chessboard}, pdfauthor={Aritro Bhattacharjee}}, and leave pdfauthor empty in the anonymous build.

## 17. [minor] paper/ieee/figures/
- **problem:** For arXiv, the figures folder contains files the paper does not use: eighth_open.pdf, star2_eight_five.pdf, the src/ and superseded/ folders, and INDEX.md. arXiv asks for no unused files. Note also that figures/ is now a real directory, not a symlink as the GUIDELINES assume.
- **fix:** Leave them out of the arXiv tarball (only the PDFs/PNG referenced by \includegraphics), or move them out of paper/ieee/figures.

## 18. [minor] sections/00_abstract.tex Index Terms
- **problem:** 'nimbers' and 'game solving' are probably not IEEE Thesaurus terms; the GUIDELINES ask for a Thesaurus check.
- **fix:** Check them against the IEEE Thesaurus. 'Game theory' is a Thesaurus term. Keep five terms in alphabetical order.

## 19. [minor] sections/04_kings.tex, 05_sums.tex (Theorems 3, 6, 8 marked [P] with 'Proof sketch')
- **problem:** Three theorems labelled [P] (proved) are followed only by a 'Proof sketch'. A journal referee will read [P] as meaning a full proof is in the paper or its supplement.
- **fix:** Either give the full proofs (in the supplement if space is short) and cite them from the sketch ('full proof in the supplement'), or say in Section XIII that [P] covers results whose full proofs are in the supplementary material.

# Review: flow + voice

Verdict: The paper mostly reads as one paper in a steady, plain "we" voice. The move-by-move walk-throughs carry the author's 2025 style well in Sections III, IV-A, VII, VIII, X and XI, and there are no Part 1/Part 2 seams. It is not yet concise. The body runs to page 17 of 19 against a 12-14 page target. The excess comes mainly from repetition: an intro contributions list dense with numbers plus a second roadmap; evidence labels, the AI statement, *2, temperature, the trébuchet, the slider rule and the default setting each defined two or three times; and a cross-check table and tools subsection that repeat the sections. Three terms are used before they are defined: "nine settings" (used in I and V, defined only inside Theorem 9), "birthday" (never defined) and "stops" (defined mid-Section IX). There are four internal inconsistencies a referee will catch: the conclusion asks for the misère ring rule that Section XI already proves; Section XIII says "every row agrees" next to the KPK row that differs on 6 positions; Section IX's textbook-tree conclusion does not follow from the sentence before it; and the ↑²* and tiny(1) numbers appear only in the conclusion. The AI disclosure in the Acknowledgment and in XIII-D also disagree on which models were used. The voice slips in a few places: into a lab notebook in the IX-B bullets ("then left", "after these results") and VI-D ("One honest correction. Our first atlas report..."), and into informality in "Let's", "you must play", "The interesting part" and "There is an important caveat". Many paragraphs also open with "So". Each problem below comes with replacement text. All the replacements use only numbers already in the paper or in the SPEC fact sheet; the ↑²* and tiny(1) end-position counts are moved from the conclusion, not invented.

## 1. [major] Whole paper (main.pdf: 17 body pages + appendix + references = 19 pages)
- **problem:** The SPEC target is about 12-14 pages including references, and the body alone runs to page 17. The extra length comes from restating things, not from new content: an intro contributions list dense with numbers, a section roadmap that repeats the section pointers already given in the bullets, a cross-check table and a real-chess-tools subsection that repeat checks already stated in each section, and closing 'what this answers' paragraphs that restate the conclusion.
- **fix:** Make the cuts listed below: one-sentence contribution bullets; a 2-sentence roadmap; fold XIII.A and XIII.C into a single sentence each; cut Table VII to the rows not already stated in the body (brute-force sum solver, whole-board minimax, move generator 160/160), or turn it into one paragraph; delete VIII 'What this answers'; trim VI.C and VI.D; compress IV.C (loopy) to the theorem plus one sentence. Together these should save about 2.5-3.5 pages.

## 2. [major] 01_intro.tex, contributions list (7 bullets) and the final roadmap paragraph
- **problem:** Each bullet is 3-5 lines and repeats headline numbers that the abstract and the body state again (1,223,689; 231,071; 607 million; 2.80%; 16,538; 27.5-28.0%; 32.5-33.5%). The bullet on the exact model gives the cut lemma's full statement. 'Tablebases and Dawson's chess' joins two unrelated topics in one bullet. The roadmap paragraph then lists every section a second time.
- **fix:** Replace the bullets with: \item \emph{An exact model} (Sections~II, V). The textbook passed-pawn test ignores en passant; we replace it, prove a cut lemma and a sum-safety theorem \lab{P}, and show that the earlier sum-safety test fails \lab{C2}. \item \emph{Kings} (Section~IV). We give conditions (V1)--(V4) under which a frozen tr\'ebuchet gives the true chess result \lab{P}; on small boards the convention fails for 159 of 500 components \lab{C1}. \item \emph{Small values} (Sections~VI, VII). Every value that only the cylinder can make comes from a ring \lab{C1}, and $1/8$, $\upsec\star$ and $\tinyg{1}$ occur in legal 10-man positions \lab{C2}. \item \emph{The $\nim{2}$ question} (Section~VIII). No $\nim{2}$ exists with six pawns or fewer on boards of width at most four, but two exist with seven \lab{C2}. \item \emph{Real chess} (Section~IX). An oracle value shows that the textbook candidate is not $\nim{2}$ in chess, and that the $1/8$ hinges on one undecided end position \lab{C1}. \item \emph{Tablebases} (Section~X). On the cylinder king and rook win only 2.80\% of positions \lab{C2}. \item \emph{Dawson's chess} (Section~XI). The $3\times n$ cylinder is a first-player win iff $g(n-3)=0$ \lab{P}. \item \emph{Engines} (Section~XII). Stockfish is weakest on infinitesimals at low depth \lab{C1}. Replace the roadmap with: 'Sections~II--III set up the rules and the basic values, Sections~IV--V add kings and sums, Sections~VI--IX search for small values and test them against real chess, and Sections~X--XII turn to tablebases, Dawson's chess and engines. Section~XIII explains how each result was checked, and Section~XIV lists open problems.'

## 3. [major] 14_conclusion.tex item 5 vs 11_dawson.tex 'Misere play' paragraph
- **problem:** This is a contradiction. Section XI already states the misère form of the ring rule (the first player wins the misère cylinder iff the strip of n-3 files is a misère P-position), yet open problem 5 asks 'what is the misère form of the ring theorem?'
- **fix:** Change the last sentence of item 5 to: 'Is the misère quotient of Dawson's chess infinite? By the ring rule of Section~XI, any answer for strips is also an answer for the cylinder.'

## 4. [major] 13_verify.tex line 16 vs the KPK row of Table VII
- **problem:** The text says 'In every row the programs agree on every case tested', but the KPK row in the same table says the two solvers differ on 6 flat positions.
- **fix:** 'In every row the programs agree on every case tested, except the six flat KPK positions, where only a rook underpromotion avoids stalemate and the second solver promotes to a queen only.'

## 5. [major] 09_real.tex, paragraph after Theorem (Candidate in real chess)
- **problem:** The logic does not follow. The text says that in the textbook tree '$\nim{2}$ is excluded only when draws count as wins for one side', and then concludes 'The textbook $\nim{2}$ therefore does not survive real chess.' The conclusion actually rests on part (b), the e.p.-aware tree, which is the one that matches chess. As written, the reader thinks the claim is drawn from the weaker textbook statement.
- **fix:** Replace the last two sentences with: 'Real chess has en passant, so the e.p.-aware tree is the one that matches it, and there $O\ne\nim{2}$ under every treatment. The textbook tree excludes $\nim{2}$ only when draws count as wins for one side, which again shows that the textbook $\nim{2}$ came from the old test.'

## 6. [major] 14_conclusion.tex item 1 (line 16)
- **problem:** New results appear for the first time in the conclusion: for $\upsec\star$ and $\tinyg{1}$ the lower bounds already equal the targets, and 11 and 13 end positions with 8 to 10 men remain. The body never mentions them, so the conclusion is introducing data.
- **fix:** Add one sentence at the end of IX-B: 'The same method applies to $\upsec\star$ and $\tinyg{1}$: their lower bounds already equal the target values, with 11 and 13 end positions of 8 to 10 men still open \lab{C1}.' In item 1, write: 'The same pipeline then applies to $\upsec\star$ and $\tinyg{1}$ (Section~IX-B).'

## 7. [major] main.tex Acknowledgment (line 93) vs 13_verify.tex XIII-D
- **problem:** The AI disclosure is given twice, and the two versions disagree. The Acknowledgment names Claude, Codex and Nemotron Ultra (NVIDIA). XIII-D says 'Claude by Anthropic, Codex by OpenAI, and others' and 'a second model from a different developer'. A referee will ask which is accurate.
- **fix:** IEEE policy puts the disclosure in the Acknowledgment, so keep it there with the full list: 'The software, the searches and the first drafts of the proofs were produced with AI coding assistants, Claude (Anthropic) and Codex (OpenAI), under the author's direction; the proofs were re-derived by Nemotron Ultra (NVIDIA) (Section~XIII-D).' In XIII-D, drop the model list and keep only the process: 'Each proof was re-derived by a second model (see the Acknowledgment). Eight of the nine were confirmed, one after a repair, and one gap was found; that statement is now Conjecture~6. A human check is pending.' The orchestrator should confirm whether 'and others' should name more tools.

## 8. [major] 02_rules.tex II-C; 05_sums.tex line 166; 01_intro.tex bullet 3; 07_targets.tex Theorem (eighth)
- **problem:** 'Nine settings' is used in the Introduction and in Section V before it is defined. The only definition is buried in Theorem 9 of Section VII, and that wording is garbled: 'the three race rules, each with en passant off, with the textbook test and with the e.p.-aware test'.
- **fix:** Close II-C with: 'The three race rules and three treatments of en passant (the textbook test, the e.p.-aware test, and e.p.\ off) give nine \emph{settings}. Our default is the count rule with the e.p.-aware test.' Then shorten Theorem 9 to: '... has value exactly $1/8$ in all nine settings and for every assignment of outcomes to its race positions.' Delete the sentence after the theorem, 'So this $1/8$ does not depend on how races are settled at all.'

## 9. [major] 09_real.tex IX-B bullet list (lines 60-80) and the closing paragraph
- **problem:** The bullets read like a lab notebook ('A greedy search ... then left', 'After these results the bounds were', 'The solver then settled'), not like a result. 'The value 1/8 has survived every real-chess test so far, including one disagreement' is confusing. 'Conditional only on the king freeze' contradicts the previous sentence, which says that under-promotions are still unchecked.
- **fix:** Write it as prose: 'All 306 end-position sides with at most seven men are resolved by the tablebase: 283 agree with the model, 5 disagree and 2 are draws. A greedy search for a smallest decisive set leaves eight larger end positions that matter, five with eight men and three with nine. Resolving eight-man sides gives seven agreements and one disagreement: with black to move in \pos{W a3 a5 / B b4 b5}, black wins where the model scores a white win. Our king-and-pawn solver shows that all six sides of the three nine-man positions agree with the model, and that white to move in \pos{W b2 b5 / B a5 b4} is a white win. Only black to move there is still open, and on its own it decides the value.' End the paragraph with: 'The one decisive disagreement does not move the value. If the last side goes as the model says, this gives an $8\times8$ king-and-pawn position whose oracle value is $1/8$, conditional on the king freeze and on the under-promotions.'

## 10. [minor] 02_rules.tex line 66
- **problem:** 'Changes the value of thousands of the 231,071 records, and the outcome of more than four thousand [C1]' is vague when the exact figures (21,441 and 4,068) are in RESULTS.md. 'Thousands' also understates 21,441. The pointer goes to Section VIII, but the census is introduced in Section VI.
- **fix:** 'Across the flat census (Section~VI), every position with at most six pawns on boards of width at most four, the stricter test changes 21,441 of the 231,071 values, 4,068 of them in outcome.'

## 11. [minor] 08_star2.tex line 51
- **problem:** 'Birthday' is never defined, and the parenthesis '(at most 36 pawn moves before a decided position of birthday B=256)' is hard to follow.
- **fix:** 'A game's birthday is the depth of its game tree, and $\nim{k}$ has birthday $k$. A decided position, the integer $\BIG=256$, has birthday 256, and at most 36 pawn moves come before one, so every position in scope has birthday at most 292 and no larger nimber can occur.' Or move the one-clause definition of birthday into II-E.

## 12. [minor] 09_real.tex line 31 ('We also use the stops of a game')
- **problem:** Stops are a basic CGT notion, but they are defined in the middle of Section IX, after mean and temperature were introduced in II-E. The definition interrupts the oracle section.
- **fix:** Move it to II-E, after the thermograph sentence: 'The \emph{left} and \emph{right stops} of $G$ are the numbers reached when white or black moves first and both sides play until a number appears; both stops of $0$ and of $\nim{2}$ are $0$.' Then delete the sentence from IX.

## 13. [minor] 05_sums.tex V-A, Principle 2 vs 02_rules.tex II-E
- **problem:** Temperature and infinitesimals are explained twice in nearly the same words (the temperature of ±x; infinitesimals have temperature 0).
- **fix:** Principle 2: 'Move in the component with the highest temperature (Section~II-E). For a switch $\game{x}{y}$ between numbers $x>y$, the temperature $(x-y)/2$ is what each side gains by moving there first, and infinitesimals have temperature $0$. This principle is not universally true, but it holds in all our examples.'

## 14. [minor] 02_rules.tex end of II-D ('One caution: ...') vs 05_sums.tex start of V-C
- **problem:** The point that 'the first passed pawn ends the game, while in a sum +B and -B cancel' is made in II-D and then again, almost word for word, in V-C.
- **fix:** Shorten II-D to: 'Hence values that only a cylinder can make must come from rings (Section~VI). Section~V-C gives the condition under which a sum of components still names the right winner.'

## 15. [minor] 10_tablebases.tex 'Rules' paragraph vs 02_rules.tex II-A
- **problem:** The slider rule (a ray stops before it returns to its own square, so a piece cannot pass by circling a rank) is stated in full twice.
- **fix:** In X: 'Pieces move as in Section~II-A and wrap around each glued edge.' Delete the rook sentence.

## 16. [minor] 08_star2.tex line 3
- **problem:** $\nim{2}$ is defined a third time ('a nim heap of size two: whoever moves may go to 0 or to *'), after the Introduction and II-E. 'Artifact of en passant' is also imprecise: the artifact comes from a test that ignores en passant.
- **fix:** Open with: 'The $\nim{2}$ question of Section~I asks whether a king-and-pawn position on a board with eight ranks can have this value. In this section we show that the one $\nim{2}$ among small positions comes from the textbook test, that none exists with six pawns or fewer, and that $\nim{2}$ appears with seven.'

## 17. [minor] 08_star2.tex VIII-D 3) 'What this answers'
- **problem:** This paragraph restates the abstract, the Introduction and the Conclusion. It also uses chess jargon ('no officers').
- **fix:** Replace it with: 'Within the model, then, the $\nim{2}$ question has a positive answer on the ordinary $8\times8$ board: four files, seven pawns and a tr\'ebuchet suffice, while Elkies' higher nimbers need larger boards~\cite{Elkies2002}. Whether real chess agrees is the subject of Section~IX.'

## 18. [minor] 06_atlas.tex VI-D, line 83 ('One honest correction. Our first atlas report said ...')
- **problem:** This is internal project history and does not belong in the paper. The reader never saw a 'first atlas report'. The phrasing is also too informal for IEEE.
- **fix:** \subsection{Dependence on the Race Rule} 'The cylinder-only values are not robust. The 3-file ring values depend on the race rule: $3/4$ becomes $0$ under the mover rule. The 4-file ring values do not, but they change when en passant is switched off. So no value is cylinder-only in all nine settings.'

## 19. [minor] 06_atlas.tex VI-C, last paragraph (the C4 ring)
- **problem:** This paragraph tells the candidate's e.p. story ahead of Section VIII, which then tells it in full.
- **fix:** 'On $\cyl{4}$, white a2, c2 against black b7, d7 (the $\nim{2}$ candidate of Section~VIII) is worth $\game{3/2\pm1/2}{-3/2\pm1/2}$ under the textbook test. Under the e.p.-aware test it is $\game{2\pm1}{-2\pm1}$ on the ring and on the flat board alike, so it is no longer cylinder-only.'

## 20. [minor] 13_verify.tex XIII-A (Evidence Labels) vs 01_intro.tex
- **problem:** The labels are defined in full twice. The SPEC asks for a single sentence.
- **fix:** Replace XIII-A with one sentence: 'In the labels of Section~I, a program is independent when it was written from the rules alone, without reading the code of the first, and a claim with both a proof and a computer check carries both labels.'

## 21. [minor] 13_verify.tex XIII-C (Real-Chess Tools)
- **problem:** This subsection repeats what Sections IV and IX already say about the Lichess tablebase, the move generator and the king-and-pawn solver.
- **fix:** Delete the subsection and add to the move-generator row of Table VII: 'covers en passant, promotions, pins, checks, mates and stalemates; tablebase responses were cached'.

## 22. [minor] 00_abstract.tex lines 4, 7, 10
- **problem:** 'We first make this model exact' overclaims, since Section IV shows the kings are exact only under (V1)-(V4). 'Star two returns' implies it existed before, when it existed only as an artifact of the old test. 'We correct Dawson's chess' reads as if the game itself were being corrected.
- **fix:** 'We first repair this model.' / 'but star two appears with seven pawns, in two positions confirmed by three independent programs.' / 'We correct the earlier analysis of Dawson's chess on the cylinder and prove ...'

## 23. [minor] 01_intro.tex, end of paragraph 2 ('On the cylinder there are no rook pawns ... But a position with a pawn on every file ...')
- **problem:** The 'But' sets up a contrast that does not exist. The sentence lists three differences of the cylinder, and they are mixed into a paragraph about prior work.
- **fix:** Start a new paragraph: 'The cylinder changes this picture in three ways. There are no rook pawns, and a position can be shifted sideways by any number of files without changing its value. A position with a pawn on every file, a \emph{ring}, has no edge at which to cut it. And the corners that decide mates and fortresses on the ordinary board are gone.'

## 24. [minor] 03_basic.tex line 56; 07_targets.tex line 67; 02_rules.tex line 19; 12_engines.tex lines 24, 80
- **problem:** These phrases are too informal for IEEE: 'Let's begin', 'Let's see why', 'you must play on your turn', 'The interesting part is', 'There is an important caveat.'
- **fix:** Use 'Let us begin with the zero game', which keeps the 2025 voice and matches 'Let us see' in Section XI. Use 'To see why, look at Fig.~9(a).' Use 'There are no null moves: a player must move on every turn.' Use 'The classes separate at a small fixed depth (Table~VI).' Delete 'There is an important caveat.' and begin that paragraph with 'The ground truth here is the CGT model with frozen kings, not real chess.'

## 25. [minor] Paragraph openings in 02_rules (cut lemma), 04_kings (IV-C, IV-E), 09_real, 11_dawson, 12_engines
- **problem:** Too many paragraphs open with 'So', which sounds machine-written: 'So values that only ...', 'So a white shuttle ...', 'So the group is frozen ...', 'So real chess agrees ...', 'So the suite is too easy ...', 'So these numbers measure ...', 'So the ring formula ...'.
- **fix:** Vary them or drop them: 'Hence values that only a cylinder can make ...'; 'In short, a white shuttle ...'; 'The group is therefore frozen for black only ...'; 'Real chess thus agrees with $\nim{2}$ on the outcome ...'; 'The suite is therefore too easy ...'; 'These numbers therefore measure ...'; 'The ring formula of~\cite{Bhattacharjee2025} ... is therefore right once ...'.

## 26. [minor] 04_kings.tex lines 3-5 and 15-18
- **problem:** 'In chess that player would be stalemated' is not accurate: a player with no pawn move would normally move the king. In IV-A, the kept 2025 sentence 'Whichever player goes first will lose a pawn ...' repeats the two sentences just before it.
- **fix:** Line 3: 'So far a player with no pawn move simply lost. In chess that player would move the king instead, or, with no king move either, be stalemated, which is a draw.' IV-A: merge into 'If white (Left) moves first, every king move gives up a4, since h4 ... ; in the same way black (Right), moving first, loses a5. Whichever player goes first will lose a pawn and then the game, so this position is a zero game.'

## 27. [minor] Throughout (Theorems 12-13, Figs. 10-11 and 13 captions, VIII-D, Table II note, V-D)
- **problem:** II-C already declares the default setting, yet 'under the count rule with the e.p.-aware test and e.p. on' is repeated about ten times. 'Beside the trébuchet on files f-h (white Kf5 and g4, black Kh4 and g5)' is also repeated many times.
- **fix:** Write 'in the default setting' after II-C. In IV-A, add 'We call this group T and place it beside every ordinary-board pawn position in this paper', then write 'beside T' everywhere, as the appendix already does with '$\flatb{8}$+T'.

## 28. [minor] 03_basic.tex III-C heading and text; 07_targets.tex VII-B heading; abstract
- **problem:** The same value is named three ways: 'Tiny 1', '$\tinyg{1}$' and 'tiny-one'.
- **fix:** Use 'Tiny 1' in prose and headings (the 2025 usage), $\tinyg{1}$ in formulas, and 'Tiny 1' in the abstract.

## 29. [minor] 07_targets.tex line 32 vs the Table II note
- **problem:** The G - T = 0 check is described twice, once in the table note and once in the text.
- **fix:** Delete 'For every counted position $G$ and target $T$, an independent C solver checked that $G-T=0$.' from the text, and keep the note as 'Each identity $G-T=0$ was confirmed by an independent C solver \lab{C2}.'

## 30. [minor] 07_targets.tex VII-A walk-through
- **problem:** 'Black answers it back to 0' and 'black answers to -3' are clumsy and break the 2025 move-by-move rhythm.
- **fix:** 'The quieter a2--a3 reaches only $\star$, from which black can return to $0$, so it is reversible. The move b3--b4 is bad, since black's reply leaves $-3$.'

## 31. [minor] 10_tablebases.tex lines 13, 59, 87, 120
- **problem:** 'KRK and KBNK are draws on the cylinder' overclaims, since 2.80% of KRK positions are wins. 'Both sides of the board have even length' is unclear. The Table V caption has lower-case 'white Wins' in title case. 'On a cylinder every file is a center file, so there are no rook pawns' is the third time this point is made.
- **fix:** '\emph{KRK and KBNK cannot force mate on the cylinder.}' / 'Both dimensions of the board are even, so ...' / 'Legal Positions and White Wins ...' / delete the line-120 sentence and start with 'Fig.~15 shows the classic rook-pawn draw.'

## 32. [minor] 12_engines.tex lines 30-31 and 84
- **problem:** 'Table VI leaves out the seven positions whose result is already decided' is cut off from the table and placed after the 'pilot result' sentence. 'The kind of certification that we carried out for 1/8' overstates the status, since the 1/8 is not yet certified.
- **fix:** Move the first sentence into the Table VI caption: '... by CGT Class (the seven positions already decided are omitted)'. Replace the second with '... the kind of certification that Section~IX begins for $1/8$.'

## 33. [minor] 04_kings.tex line 152; 05_sums.tex line 155
- **problem:** '6×6 and 7×6 cylinders' and 'a 5×6 ordinary board' clash with the $\cyl{n}$/$\flatb{n}$ notation, which assumes eight ranks, and do not say which number is files and which is ranks.
- **fix:** State files and ranks explicitly, for example 'cylinders with six and seven files and six ranks, and an ordinary board with five files and six ranks', and in Proposition 8 write 'the flat board with six files and six ranks'.

# Review: facts

Verdict: Most of the paper checks out. Every number in it matches the SPEC fact sheet, RESULTS.md, delegate/REVIEW.md, delegate/checks/*.out or the underlying reports (kings/REPORT.md, tablebase/replica/REPORT.md, atlas/flat8, bench, ml/dawson). I recomputed with cylcgt and found no mismatch in any value or walk-through. That covers every basic position (all 9 settings), the puzzle components and options, ±3, 3/4, 1/4±1/4 and the C4 ring, and the 1/8 (all 9 settings) with its mirror. It also covers ↑²*, tiny(1), the two textbook results that fail, the candidate (all settings, every option, and W a2 c2 / B b4 d7 under both tests), and the move-by-move options of the seven-pawn positions A and B. The Dawson g(n), the 31 and 56 counts, the last exception 51 and the ring list match too. The 1/8 bounds 0..1/8 reproduce from apply_kpsolve.py. Every appendix FEN decodes to the stated men, make_figures.py --check passes (values and legality), and kpsolve confirms the KPK rook-pawn result. The problems are evidence labels and over-claims rather than wrong values. Two are serious: a proof-gap result is labelled [P] in Section IV, and the AI/proof statement understates the open gaps. Several real-chess sentences also drop the queen-promotion-only and e.p.-aware-tree qualifiers, the king-failure sweep (159/500) was run under the textbook test without saying so, and a few walk-through sentences are imprecise.

## 1. [major] sections/04_kings.tex: certificate paragraph ('The certificate implies (V3) for that move \lab{P}') and Proposition prop:horizon1
- **problem:** The final status table in kings/theory/LOOPY.md (line 44) labels Theorem 2.7 (local certificate implies decisive punishment) 'GAP (proof incomplete) ... Unresolved until a further check', after the K3 review. Proposition 2.10 (LOOPY line 148) proves only that, for T=1, the defender cannot counter-promote in any non-terminal context. The paper's proposition says more: that such a punishment 'is decisive in every context'. That needs Theorem 2.7, and its one-line proof shows only the counter-promotion part. Both statements are labelled [P].
- **fix:** Mark the certificate implication as having an incomplete proof (or as \lab{Conj}). Restate Prop. horizon1 as 'for T=1 the counter-promotion condition of the certificate holds in every non-terminal context \lab{P}', and say that decisiveness then follows from the certificate theorem, whose proof is still incomplete.

## 2. [major] sections/13_verify.tex, Use of AI Tools ('Each proof was then re-derived ... Eight of the nine were confirmed ... one gap was found'); main.tex Acknowledgment
- **problem:** This reflects only REVIEW T2 (Nemotron re-derivation of 9 proofs). The later K3 check in kings/REPORT.md and LOOPY.md downgraded Theorem 2.7 and the sharp form of Theorem 1.14 to GAP. Theorem 1.14(ii), the (V4) part of the paper's validity theorem, is 'PROVED after repair'. 'Each proof' is also too broad: the nine re-derived results are L1.6, L2.1, L2.3, L3.3, L5.1-5.3, Thm 1.14(i), Thm 3.4, Thm 2.7 and Prop 2.10(b). Other [P] items in the paper, such as the sandwich lemma and Prop. horizon1, are not among them.
- **fix:** Say which statements had the second-model re-derivation. State that the certificate theorem still has a gap after a later external check, and that the (V4) part of the validity theorem was proved only after a repair. Replace 'Each proof' with the actual list.

## 3. [major] sections/01_intro.tex, real-chess bullet ('The oracle value of the textbook candidate is never \nim{2}, however draws are treated \lab{C1}')
- **problem:** RESULTS.md §1 and the paper's own Section IX (Theorem oracle-cand (b) and the sentence after it) say this holds only in the e.p.-aware tree. In the textbook tree, \nim{2} is excluded only when draws count as wins for one side. As written, the intro overstates the result.
- **fix:** Write 'In the e.p.-aware pawn tree, the oracle value of the textbook candidate is never \nim{2} (or 0), however draws are treated'.

## 4. [major] sections/09_real.tex, last paragraph of the 1/8 subsection ('conditional only on the king freeze'); 00_abstract.tex ('exact search leaves a single undecided end position'); 01_intro.tex ('exact search on larger ones pins the oracle value between 0 and 1/8')
- **problem:** The 8- and 9-man results come from kpsolve runs with --promote Q only (kp_eighth_*.err; RESULTS §6b: 'queen promotions only, so not yet a full-chess certificate'). Section IX itself says a full certificate also needs the under-promotions. So the closing claim of a 1/8 'conditional only on the king freeze' is overstated, and the abstract and intro call these runs 'exact' with no qualifier. The open item is also one side (black to move) of one end position, not a whole end position.
- **fix:** Write 'conditional on the king freeze and on an under-promotion rerun'. In the abstract and intro, write 'queen-promotion search' or add the caveat, and 'a single undecided end position, with black to move'.

## 5. [major] sections/04_kings.tex, 'How Often Does the Convention Fail?' (159 of 500; 18 through en passant); 01_intro.tex Kings bullet
- **problem:** kings/REPORT.md says the sweep used the textbook passed-pawn test. 'Under the e.p.-aware passed test, the convention agrees with the frozen-king solver' for the 18 e.p. failures, and the 7x6 mismatch count 'drops from 143 to 138' under e.p.-aware. Section II says every value uses the e.p.-aware test unless 'textbook' is stated. The paper therefore presents textbook-test failures as failures of its own model, without the label.
- **fix:** Label the sweep '(textbook test)'. Note that under the e.p.-aware test the 18 e.p. failures disappear and the 7x6 count falls to 138. Alternatively, report the e.p.-aware total.

## 6. [minor] sections/09_real.tex, first 1/8 bullet ('All 306 ... 283 agree ..., 5 disagree and 2 are draws')
- **problem:** 283 + 5 + 2 = 290, not 306, so 16 sides are not accounted for. The same incomplete breakdown is in RESULTS.md §6b, and no log in realchess/targets18 gives the rest.
- **fix:** Give the full breakdown, e.g. the category of the remaining 16 sides (one-sided or race results?), or reword so the numbers add up.

## 7. [minor] sections/09_real.tex ('The tablebase and tablebase-backed results are \lab{C2}')
- **problem:** For the 1/8 position, the ≤7-man sides were probed in one external tablebase. The 8-man sides were resolved by tablebase-backed search with the project's own move generator. No second independent check of these 1/8 end positions is recorded; RESULTS 'checked two ways' refers to the candidate's end positions. The C2 label is not supported for this position.
- **fix:** Label the 1/8 end-position results \lab{C1}, or cite the second check if one exists.

## 8. [minor] sections/05_sums.tex, Puzzle 1 ('Black to move must take on a5 at once, since any other move allows a5--a6')
- **problem:** After black's a7-a6, a5-a6 is impossible because the square is occupied. cylcgt gives the a7-a6 option the value {{+W|...}|0}: it still loses in the total, but not for the stated reason. The claim is false as written for that move.
- **fix:** Write 'since every other move loses (h6-h5, for example, allows a5-a6)'.

## 9. [minor] sections/02_rules.tex, W a2 b3 / B b4 example and Fig. ep_test caption/text
- **problem:** After a2-a3 b4xa3 (or a2-a4 b4xa3 e.p.), white's b3 pawn is also passed, so the result is a promotion race. Black wins it only under the count rule; under the opponent rule cylcgt gives +W for W a2 b3 / B b4 (e.p.-aware). In Fig. ep_test (W a2 / B b4), after a2-a4 the b4 pawn is also passed under the textbook test, so it is a race too, not a white passed pawn alone. The caption gives no value, although the value is 0 under the default settings.
- **fix:** Write 'every white move lets black capture on a3 and win the resulting race (count rule)'. Add the value 0 to the Fig. ep_test caption.

## 10. [minor] sections/07_targets.tex, Theorem thm:eighth and the sentence 'A third, separately written solver agrees in all nine settings'
- **problem:** The C-solver check (atlas/flat8/rerun C5) and the Codex check (REVIEW T1) were run on the mirror W a2 a3 b2 / B a6 b5 b6, including the every-race-outcome claim, not on the position stated. The equivalence is a trivial file mirror, but the paper does not say so. My cylcgt rerun confirms 1/8 for both in all 9 settings.
- **fix:** Add 'checked on its mirror image, which has the same value by symmetry'.

## 11. [minor] sections/07_targets.tex, tiny(1) paragraph ('with en passant on, under every race rule \lab{C2}')
- **problem:** The independent G-T identity check in the sources covers the count rule only. tiny(1) is not among Codex's five headline values. My cylcgt rerun gives tiny(1) under count, mover and opponent (e.p. on, both tests), so the value is right, but the C2 label holds only for the count rule.
- **fix:** Write 'tiny(1) under every race rule with e.p. on (count rule \lab{C2}, the others \lab{C1})'.

## 12. [minor] sections/06_atlas.tex ('an independent minimax program confirms the textbook outcomes')
- **problem:** atlas/cylinder/REPORT.md C9 says the minimax checked the winner only, for all 12,568 rings and 4,000 random flat components, not all 1,223,689 atlas outcomes.
- **fix:** Write 'confirms the winners of all 12,568 rings and of 4,000 random flat components'.

## 13. [minor] sections/08_star2.tex Theorem thm:census, the 'Scope' paragraph, and 01_intro.tex ('231,071 flat positions, up to mirror image')
- **problem:** The census scope (atlas/flat8/rerun) is narrower than stated. It requires pawns on ranks 2-7, at least one pawn per side and no passed pawn at the root, and it is reduced by translation and mirror. Separately, 'seven is the least number of pawns in a \nim{2} on ordinary boards of width at most four \lab{C2}' holds only under the count rule with the e.p.-aware test; the textbook census has a 4-pawn \nim{2}.
- **fix:** State the scope conditions once, in Theorem census, and add 'under the count rule with the e.p.-aware test' to the minimality sentence.

## 14. [minor] sections/10_tablebases.tex, KPK rook-pawn line ('1...~Kb8 2.~Kh7! Kb7 3.~a6+')
- **problem:** kpsolve (cyl:8x8, QRBN) confirms that the line wins and that the flat position is a draw with either side to move. But 2.Kb6 and 2.Kh6 also win, so the '!' wrongly suggests Kh7 is the only winning move.
- **fix:** Drop the '!' or add '(2.Kb6 and 2.Kh6 also win)'.

## 15. [minor] sections/01_intro.tex (Drummond-Cole sentence) and refs.bib
- **problem:** Some bibliographic and literature claims are unverified. The intro says \nim{2} positions 'are known in related settings' [DrummondCole2005], yet calls the kings-and-pawns 8-rank case 'still open'. Drummond-Cole 2005 constructs chess positions of value *2, so it needs checking that his positions use other pieces. The bib key WuYuLandry2020 has year 2010. The CoverImage author and year (Serge Clair, 1990) are not checked. REVIEW still asks for the Elkies 2002 pages (61-78) to be re-checked.
- **fix:** Check Drummond-Cole's actual pieces and word the sentence to match. Confirm the Wu-Yü-Landry year and the Commons metadata, and re-check the Elkies 2002 pages.

