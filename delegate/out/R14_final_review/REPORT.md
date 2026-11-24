# R14 referee report: "Chess Endgames on a Cylindrical Chessboard" (IEEE ToG, double-anonymous)

Read: anonymous main PDF (10 pp), dist/tog/tog.tex + sections/*.tex (anonymous branch via tog_review.tex), supplement PDF
(S12.1 pp. 17-23, S13 pp. 70-72, S16-S17 pp. 103-106 in full; S1-S11, S12.2, S14, S15 sampled). Character counts below are
of the rendered text (LaTeX markup removed); "src" counts are given where they differ much.

## 1. Recommendation: MAJOR REVISION

1. The results are many and largely computational; the theory under them (Thm 3, Cor 4, Thm 6, all ring families) is AI-proved,
   and the "independent" programs behind the C2 label were also AI-written, often from one rules text (S14, S17 "Limits"); the
   main text's C2 definition does not say so.
2. Some main-text statements are wrong or stronger than the supplement: Corollary 4 (outcome class vs one side to move), the
   real-king sum sentence (Sec. V), Definition 5 (threat), the draw scoring of Definition 12, "weakest on infinitesimals".
3. Sixteen loosely linked results in 10 pages lean on a 106-page supplement, about 60 pages of which are raw working notes with
   their own numbering, label words, repository paths, dates and dangling references. Refereeing it is hard.
4. The game-AI content that makes this a ToG paper (Sec. XII) is a pilot: no defined metric in the paper, no intervals, labels that
   the model gets wrong for 52 of 233 positions, and a sums test that draws no conclusion.
5. The motivating question (does chess, not the model, have a *2) stays open, and the one real-chess value (1/8) needs frozen kings
   and queen-only promotions. That is acceptable if the claims say so plainly; most do.

## 2. Ranked problems (most damaging first)

Payment rule: the paper has 0.32 in spare. Items marked (+) lengthen the text; they are paid for by cut P1 (ChessSums paragraph,
about 840 characters, about 9 column lines) and, if Table I is kept, by cut P2. Every other replacement is no longer than the
text it replaces.

### 1. Corollary 4 claims the outcome class; the supplement proves only a per-side statement
Location: Sec. IV-A, 04_kings.tex:69-73. Supplement A.13 (p. 21) gives a precise form "for a side to move for which the
hypotheses hold" and a counterexample showing that they can hold for one side only (W Kb6 c7 / B Ka8 a5). S17 (p. 106) says
"The validity corollary was stated for both sides to move ... corrected". The main text still says "outcome class".
Replace (04_kings.tex:71-72)
  "the chess result is the outcome class of the components' $\pm\BIG$ value."   (63 chars)
with
  "the chess result, for that side to move, is that of the $\pm\BIG$ sum."   (62 chars)

### 2. The C2 label overstates independence
Location: Sec. I, 01_intro.tex:37-39 (label definitions). The definition says "two independently written programs agree, the
second written from the rules alone". The supplement says that the programs behind the ring base cases were "all written by
Claude models" (S17, Table S9), that "C and R were written by the same model family and share part of their move generation"
(S14), and that "the independent programs ... were written by models from one description of the rules, so a shared misreading
of the rules is not excluded" (S17, Limits). Every C2 in the paper inherits this. Point (a) on AI-written proofs is handled
adequately in Sec. I and XIII; this programs point is not.
Replace
  "\lab{C2}, two independently written programs agree, the second written from the rules alone; \lab{C1}, one program;"
  (107 chars)
with
  "\lab{C2}, two separately written programs agree (AI-written, often from one rules text); \lab{C1}, one program;"
  (103 chars)

### 3. Factual error in the real-king sum test
Location: Sec. V-B, 05_sums.tex:87-89: "Of the 38 positions, 19 are solved and agree with the sum; the other 19, all the
second-player wins, have only bounds". Table S2 (p. 7) contradicts this. P1 is class L and is bounded with white to move,
where white is the first player and wins. N3 is bounded with white to move (a first-player win in the model). P21 is exact with
black to move, a second-player win. So the bounded sides are not "all the second-player wins". Also, these are 38 sides, not
positions, and all 19 sums share one king and anchor placement (S3.4).
Replace
  "Of the $38$ positions, $19$ are solved and agree with the sum; the other $19$, all the second-player wins, have only bounds,
   each consistent with the sum \lab{C1}."   (153 chars)
with
  "Of the $38$ sides, $19$ are solved and agree with the sum; the other $19$ have only bounds, each consistent with it; all share
   one king placement \lab{C1}."   (145 chars)

### 4. Definition 12: "draws worth 0" is not 0, and the leaf encoding is not explained
Location: Sec. IX, 09_real.tex:11-13. With draws "worth 0" a leaf is {B r_W | B r_B}. A dead draw (0,0) becomes {0|0} = *, a
nimber, and that matters most in a paper about *2. The pair (-1,0) becomes {-B|0} = -1, a number, and (0,1) becomes +1. The
scoring is faithful to stops (and Thm 14(b) uses only stops, so (b) is safe). But "worth 0" is wrong as stated, and "undecided if
draws count 0" (09_real.tex:43-44) depends on these choices. Say what the encoding is and why. Ideally add a one-line check that
the textbook-tree verdict does not depend on the * leaves.
Replace (09_real.tex:11-13)
  "or as worth $0$; in the last case the end position is $\game{\BIG r_W}{\BIG r_B}$, where $r_W,r_B\in\{-1,0,1\}$ are white's
   results with white and with black to move."   (140 chars)
with
  "or as worth $0$, scoring the end position $\game{\BIG r_W}{\BIG r_B}$ ($r_W,r_B\in\{-1,0,1\}$: white's results with white,
   black to move; a dead draw is $\star$)."   (about 128 chars)

### 5. Engine statistics overstated and the metric undefined
Location: Sec. XII-B, 12_engines.tex:17-22; contribution bullet 01_intro.tex:60-61; Table V.
- The paper never says what "matching the tablebase" means. The project notes (engine/ENGINES.md:363) use a +-150 cp
  win/draw/loss verdict. State it. The author should confirm the threshold.
- "The classes separate at a small fixed depth" and "weakest on infinitesimals" go beyond the data. At depth 1, infinitesimals
  are 8/27 = 30% (Wilson 95% interval 16-48%). By Fisher's exact test they trail hot, number and switch positions (p <= 0.001),
  but not nimbers (9/17, p = 0.20) or "other" (12/20, p = 0.07). At depth 2, infinitesimals against "other": p = 0.13. At
  depth 4: p = 0.35. No multiplicity correction is applied.
- "Both classes reach 100% by depth 8" has no clear antecedent.
- 52 of the 233 class labels come from a model that the tablebase contradicts in that very position (12_engines.tex:10-12).
  Either report the 181 model-correct positions separately, or say that the class is the model's.
Replace (12_engines.tex:17-22, from "The classes separate" to "by depth~8.")   (385 chars)
with
  "A verdict (win, draw or loss at $\pm150$\,cp) matches if it agrees with the tablebase. At depth~1 (Table~\ref{tab:sf}) hot
   positions, numbers and switches match $73$--$81\%$ of the time, infinitesimals $30\%$ ($8/27$) and nimbers $53\%$ \lab{C1};
   infinitesimals trail the first three (Fisher $p<0.001$) but not nimbers or \emph{other}. Infinitesimals and nimbers reach
   $100\%$ by depth~8."   (about 343 chars)
Replace bullet (01_intro.tex:60-61)
  "in a $233$-position pilot, Stockfish at low depth is weakest on infinitesimals \lab{C1}."   (82 chars)
with
  "in a $233$-position pilot, low-depth Stockfish seems weakest on infinitesimals \lab{C1}."   (82 chars)

### 6. The 92.5% figure is a convenience sample but reads as representative
Location: Sec. IV-B, 04_kings.tex:99-101, and Conclusion, 14_conclusion.tex:4-5. S2.3 (p. 4) says these are "the ones our other
runs solved, not a sample of a defined class", with Wilson intervals called "optimistic". The main text and the Conclusion drop
that caveat.
Replace (04_kings.tex:99)
  "Of the $2{,}154$ $8\times8$ positions beside a tr\'ebuchet whose real results we know,"   (72 chars)
with
  "Of $2{,}154$ solved $8\times8$ positions beside a tr\'ebuchet (not a random sample),"   (70 chars)
Replace (14_conclusion.tex:4-5)
  "The model names the real winner in $92.5\%$ of $2{,}049$ decisive $8\times8$ positions; on six ranks a square-rule passer test
   removes its pawn errors with frozen kings \lab{C1}."   (160 chars)
with
  "On $2{,}049$ decisive $8\times8$ positions we could solve (not a random sample) the model names the real winner in $92.5\%$
   \lab{C1}."   (115 chars)

### 7. Definition 5 (threat) is looser than the theorem that uses it
Location: Sec. V-B, 05_sums.tex:52-53. The supplement's Remark A.3 (p. 18) says that the main text's threat "does not say
'before the first passed pawn'". "Reachable from it" also does not say "by moves on its files". As written, a component could
carry a "threat" through play that passes a first passed pawn, or that uses other components.
Replace
  "A component carries a \emph{threat} for a side if a position reachable from it gives that side a passed pawn."   (102 chars)
with
  "A component carries a \emph{threat} for a side if moves on its files can give that side the first passed pawn."   (103 chars, +1)

### 8. Notation: one letter, several meanings, and uses before definitions
- B is the big number (sans 𝖡), Black in every pawn list, "position B", and B4 in wall notation. Example (08_star2.tex:47-48):
  "position~B, \pos{W b4 c2 d2 / B a6 a7 c6 d5}". Fix: rename position B to A' (A with colors reversed). In 08_star2.tex:17, 21,
  47, 57, 68 (table header), 79-80 and 09_real.tex:63: "B" -> "A$'$" (+1 rendered char each, 8 places; (+), paid by P1).
- W is White in pawn lists and also W(X), the whole-board game. S is the evidence label <S>, the sum model S(X), the supplement
  prefix ("Section S12") and, in S16, the square-rule test. At least rename the sum model, S(X) -> Sigma(X), in 04_kings.tex:77
  and 05_sums.tex:45, 59-60, 79, 83. Same length.
- W(X), S(X), HSS and (E) are used in Sec. IV (Thm 3, Cor 4) and defined in Sec. V-B. There are forward pointers, which is
  acceptable, but (V4) is defined only inside Corollary 4, and its scope is ambiguous: does the bound "B exceeds" belong to
  (V4)? In the supplement it does ("(V4) is: X is HSS, satisfies (E), and B > N(X)").
- C_n is defined with eight ranks (02_rules.tex:8-9), yet 05_sums.tex:87 has "a six-rank C_8". Replace
  "with $n$ files and eight ranks." with "with $n$ files (eight ranks unless stated)." (+8, (+)).
- Tiny 1 vs tiny(1): both names for one value (02_rules.tex:65, 01_intro.tex:46, 07_targets.tex:9, 70). Use $\tinyg{1}$
  throughout (+1 each, (+)). The abstract can keep words.
- X is reused for the "15 reference games X" (13_verify.tex:8); it is the pawn position elsewhere. Replace "reference games
  $X$" with "reference games $R$" and "$G+X$" with "$G+R$" (same length).
- h is a nim heap (V-B) and a certificate horizon (IV-A); minor.
- Supplement only: N(X) (move bound) against the outcome class N and the "NNPN" signatures. In S13/S14 the finite checks are
  named "C1", "C2", so one reads "C1 <C2>" (p. 70). Certificate conditions are also (C1)-(C3) (p. 22). In S13 "player Z" and
  "player X" clash with the king group Z and the position X. Rename the checks F1/F2 and the players sigma/tau.
- No conflicts found for Reach (supplement only, defined at A.II) or for the star symbols (*, *k, up^2*), apart from Tiny 1.

### 9. Anonymity and working-note residue (filename, supplement)
- Both PDF filenames begin "Bhattacharjee_". Rename, for example to ToG_cylinder_chess_main.pdf and
  ToG_cylinder_chess_supplement.pdf.
- The supplement prints distinctive repository paths and tool names: "kings/theory/LOOPY.md" (p. 23),
  "research/ring_family_proof/proof.tex" (p. 70), "research/ring_n_proof/PROOF_N.md" (p. 72),
  "research/ring_n_plus_2_proof/PROOF.md", "research/star3_proof/PROOF_S3T3.md", "research/mobius_rings_proof/PROOF.md",
  "research/v2_mechanisms/cc.py", "pawngame.py" (p. 103), "cylcgt", "kpsolve", "kings/SPEC.md", "RESULTS.md §2",
  "notes/lemmas.md", "lemmas/common.py" (S12.2). The named repository (git origin github.com/aritroBh/cylindrical-chess-cgt)
  holds these files (131 matching tracked paths), so a reviewer who searches GitHub for "LOOPY.md cylinder" or "cylcgt" can
  find the author. Strip the paths, or keep the named repository private until the decision.
- Internal revision dates: "revised 2026-11-23", "the revisions of 2026-11-23" (p. 23), "Drafts ... in 2026-10", "In November"
  (Table S8), and "caught real errors in November 2026" (p. 106).
- Internal working notes: "an automatic choice after the intended tool failed", "Opus agent", "Sonnet verifier", "two
  adversarial Claude lenses", "the specific agent is not recorded" (Tables S8-S9); "References to §4–§8 and to Appendix A are to
  later parts of the source note, which are not reproduced here" (p. 24, dangling); label words PROVED/CHECKED-2/COMPUTED-1
  instead of <S>/<C2>/<C1> (S12.2, S14-S16).
- Main text, acknowledgment (tog.tex:139-140): naming the AI systems is required by IEEE policy, but the harness names are not.
  Replace
    "AI coding assistants (Claude, Anthropic; Codex, OpenAI; and open models run through the OpenCode and Kilo tools)"
    (112 chars)
  with
    "AI coding assistants (Claude, Anthropic; Codex, OpenAI; and open-weight models, Section S17)"   (92 chars)
- Supplement, S12.2 opening (p. 23). Replace "Source. kings/theory/LOOPY.md, Sections 1–3 (the theory note on frozen king groups). The
  note is typeset here without changes to its mathematics; it keeps its own numbering, labels (PROVED, CHECKED-2, COMPUTED-1,
  CONJECTURE) and file references, which are paths in the code repository." with "This subsection reproduces Sections 1–3 of
  the repository's theory note on frozen king groups, with its own numbering; its labels PROVED, CHECKED-2, COMPUTED-1 and
  CONJECTURE mean <S>, <C2>, <C1> and <Conj>." (shorter). Delete both "2026-11-23" parentheticals.
- Reference [9] ("Anonymous, Title withheld for review") and the third-person wording in Sec. I are adequate.

### 10. Table I does not stand on its own (check iv)
Location: Sec. V-A, 05_sums.tex:11-37. The puzzle positions are not in the main text (they are in Fig. S4). The rows ("1: c-file",
"2: kings", "3: total") mean nothing without them. The "Exact" column mixes values, verbal properties ("not mutual", "white wins
either way") and one illegal-as-drawn total ("+B before any move"). For a reader who cannot see [9], the table judges a document
the reader cannot check.
Preferred fix (cut P2, which saves about 1.8 in): delete Table I and replace the first two sentences of V-A with
  "Section~S3 re-solves three cylinder puzzles of~\cite{Study2025}: the winners claimed there are right, but four of the six
   component values are not."   (shorter than the deleted text)
Minimal fix if kept (+): retitle the caption
  "Puzzles of the 2025 Study: Claimed and Exact Values \lab{C2}"   (56 chars)
  -> "Cylinder Puzzles of~\cite{Study2025} (Fig.~S4): Claimed and Exact Values \lab{C2}"   (about 70 chars, +14, paid by P1)
and replace the first sentence (05_sums.tex:11-12, about 186 chars) with
  "Table~\ref{tab:puzzles} compares values claimed in~\cite{Study2025} for parts of three cylinder puzzles (Fig.~S4) with exact
   ones; the winners claimed are right."   (about 148 chars)

### 11. ChessSums paragraph: space with no result (cut P1)
Location: Sec. XII-C, 12_engines.tex:55-63 (about 990 src chars). The authors "draw no conclusion" from 187 of the 200
placements, and 13 positions remain. Replace the paragraph with
  "Engines on sums, where no tablebase applies, are future work; Section~S9 describes ChessSums, $26{,}000$ exactly valued
   pawn-endgame sums."   (about 135 chars)
and move the current text to S9. This frees about 9 lines, which pays for every (+) above.

### 12. Label and number mismatches (check ii, vii)
- 08_star2.tex:116-117: "checked by two programs for n < 17 <C2>". S13 check C2 (p. 71) says "unreduced search; whole-board
  cylcgt for n <= 10", and S17 says "whole-board solvers up to n = 10 and ... the verifier's engine up to n = 61". For
  11 <= n <= 16 it is not clear that two programs ran. Verify, or write "for n <= 10 <C2> and n < 62 <C1>".
- S13 is headed "typeset unchanged", but S15 Note 1 says that S13's "pattern file" definition was repaired. S17 says that the
  cross-vendor referee "did not read S13 itself". The n+3 ring family <S> and, through Lemmas 1-3, every other ring <S> rest on
  S13. State this in the main text, or have S13 refereed across vendors.
- 05_sums.tex:73-74: "(E): without it, sums fail even in the pawn game with no passed-pawn rule <C1>". S12.1 (p. 20) has a
  hand-proved <P> counterexample in the actual model (W a4 b3 e2 / B a5 b4 e4). Cite it as <P>.
- Prop 7 (05_sums.tex:77): the race rule (count, per A.14) is not stated. Add "count rule," (+11, (+)).
- Contribution bullet 01_intro.tex:53-54: "the textbook *2 candidate is not *2, however draws are treated" has no label. Use
  "... is not $\nim{2}$ for any draw treatment \lab{C1};" (+1, (+)).
- Sec. IX-B (09_real.tex:50-52): 302 end-position sides, 290 with one passer, and the other 12 (races, per S7.1) are not
  mentioned.
- Supplement S7 (p. 12): the five-file *2 "sits legally beside T ... with only file f free of pawns between them". File e holds
  pawns and file f holds the white king, so there is no buffer, and Theorem 3 does not apply. Say so.
- Numbers checked and consistent: 18,137/4,070; 159 = 107+18+34; 52 = 18+34; 128 = 159-31; 11,300/58,595 = 19.3%;
  4,967,550 = 55,195 x 3 x 15 x 2; 2,483,775 = half of it; KPK 160,656 + 165,984 = 326,640; Table V n's sum to 226 = 233-7, and
  its percentages match integer counts; Dawson's chess: last exception 51 and the cylinder first-player list 3, 7, ..., 57
  (recomputed); FENs in Table S7 match the pawn lists; the ring minima 6, 7, 8, 9, 10, 10, 10, 10, 11 agree across Fig. 6,
  Sec. VIII-E, the Möbius paragraph and Table S3.

### 13. Typos, grammar, figures (check vii)
- 13_verify.tex:12: "no human referee has yet." (25) -> "no human has read them." (23)
- 04_kings.tex:99: "$2{,}154$ $8\times8$" (two numerals in a row); fixed by item 6.
- 04_kings.tex:91-92: "(...; queen promotions only, at most two)": two what? Write "at most two promotions" if that is meant.
- 02_rules.tex:78: "changes at least 18,137": "at least" is explained only in S1 (values beyond the display range).
- 05_sums.tex:88: "38 positions" should be "38 sides" (fixed by item 3).
- Fig. 6 (08_star2.tex:97-100): the *3 series starts at n = 10 (12 pawns) and hides the lower 10-pawn *3 rings on C7 and C8. The
  plot suggests that the least *3 grows with n. Plot C7 and C8 too.
- Figs. 2-5: the rank and file labels of the 0.32-column boards are about 5 pt in print: readable, but at the limit. The Fig. 7
  markers (red dots) are small. The Fig. 6 legend is fine.
- Supplement S5 (p. 8) begins "To see why, look at Fig. 4(a)." (residue of moved text). In S13 Lemma 3 the typesetting reads
  "So μ is P in 𝑝 iff in 𝑝.̂" (hat on the period).

## 3. Required checks

(i) Abstract and contribution claims supported by labelled body statements: YES, with three exceptions.
- "state when frozen kings give the chess result": Thm 3 gives sufficient conditions, so "state when" overclaims. Replace
  "and state when frozen kings give the chess result." (50) with "and give conditions for frozen kings to be exact." (49).
- The candidate bullet has no label (item 12).
- The engine bullet overstates (item 5).
All others match: no *k (k >= 2) with at most 6 pawns at any width (VIII-D <C2>); A and A' "confirmed by three programs"
(Table III text); six-pawn ring on C3 and ten on C7-C10 <C2>; one pawn per file for n >= 10 <S>; ten-pawn *3 on C7 <C2>;
1/8, up^2*, tiny(1) with legal history (Thm 9, VII); oracle 1/8 (Prop 15 <C1>); KRK 2.80% and opposite bishops (Table IV <C2>);
Dawson ring rule (Thm 16 <P>).

(ii) Labels match the supplement: MOSTLY. Mismatches:
- Cor 4 is stronger than A.13.
- The C2 definition is stronger than S14/S17 (programs not independent in the stated sense).
- The "two programs for n < 17" claim (item 12).
- Def 5 is looser than A.3.
- (E) is cited as <C1> where a <P> exists.
- The certificate theorem <S>, the cut lemma <P>, Thm 6 <S> (A.7), Prop 7 (A.14: (a), (b) proved, (c) computed, so <C2> as
  computed), Thm 16 <P> and the Table III <C2> entries agree with the supplement.

(iii) Notation defined before use, one meaning each: NO. B has 4 meanings, W 2, S 4. W(X), S(X), HSS and (E) are used in
Sec. IV and defined in Sec. V. C_n is "eight ranks" but used for six ranks. Tiny 1 and tiny(1) are two names for one value. X
and h are reused. The supplement clashes: C1/C2 as check names, (C1)-(C3), N(X) against N, players X and Z. See item 8.

(iv) Table I is not understandable to a reader without [9]: positions absent, rows uninterpretable, the "Exact" column mixed.
Minimal wording: the caption and the first sentence in item 10. Better: delete it (cut P2).

(v) Engine section statistics:
- Sample sizes are given in Table V (n per class).
- No intervals or tests are given.
- The metric is undefined (+-150 cp per the project notes).
- "Classes separate" and "weakest on infinitesimals" are overstated (item 5).
- The Lc0 "perfect" result shows that the suite is too easy, which the text concedes.
- ChessSums: the sample sizes are stated (200, 163, 13). The conclusion for 13 positions is modest and correctly hedged, but
  the paragraph adds nothing (item 11).
- The 92.5% figure is a convenience sample, and the main text does not say so (item 6).

(vi) Identity and internal-note residue: YES, present.
- Author surname in both PDF filenames.
- Repository paths and engine names in the supplement that match the public named GitHub repo.
- Internal revision dates (2026-11-23, 2026-10, November 2026).
- Internal jargon ("Opus agent", "adversarial Claude lenses", "automatic choice after the intended tool failed").
- Dangling references to unreproduced note sections.
- Harness names (OpenCode, Kilo) in the main-text acknowledgment.
- No author name, institution or e-mail in the main PDF text or metadata (pdfauthor empty; title only).
- The code-link placeholder is known (b) and adequately marked as such.
- Point (c), no room for related work: the text handles it acceptably (Elkies, Wu-Yü-Landry, Mäser, Drummond-Cole and
  tablebase history are all cited briefly).

(vii) Typos, references, figures, numbers: see item 13. No broken \ref or \cite in the PDF. One factual number error: the real
kings "all the second-player wins" (item 3). Otherwise the numbers are consistent across the abstract, body, tables and
supplement (item 12, last bullet).

## 4. Three changes that would most raise the chance of acceptance

1. Make every main-text claim match what the supplement proves or computes. Fix Cor 4 per side (item 1), the real-king
   sentence (3), Def 5 (7) and Def 12 draw scoring (4). Restate C2 honestly (2), audit the "two programs" claims (12), and
   drop "weakest" and "92.5%" from the headline claims (5, 6). These edits are cheap and remove every error a referee can
   check from the supplement.
2. Make the supplement refereeable and anonymous:
   - Replace S12.2-S15 (raw notes) by self-contained proofs in the style of S12.1, or move the notes to the code repository.
   - Get a cross-vendor (ideally human) read of S13, on which all the ring <S> claims rest.
   - Strip the paths, tool names and dates, and rename the PDFs.
3. Refocus the 10 pages on the *2 question and the model-versus-chess validity:
   - Cut Table I and the puzzle paragraph, ChessSums, and the Möbius paragraph (move them to the supplement).
   - With the space, either run a real engine experiment, the natural ToG hook (a defined metric, intervals, king placements
     that satisfy the validity conditions, sums beyond seven men), or demote the engine content to one sentence and drop it
     from the contributions.
