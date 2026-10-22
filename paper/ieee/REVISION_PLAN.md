# Revision plan for paper/ieee (one plan, seven revisers)

Written 2026-10-21 by the orchestrator after reading every file in `sections/`, `main.tex`, `macros.tex`,
`refs.bib`, the 19-page `main.pdf` (built 20:36, before the 21:06 edits), SPEC.md, GUIDELINES.md,
REVIEW_FINDINGS.md (67 findings) and ORCH_FIXES.md (9 fixes). This file overrides SPEC.md wherever they
disagree. ORCH_FIXES.md and RESULTS.md override the SPEC fact sheet.

Finding ids used below: **P1–P19** = "Review: IEEE production", **V1–V33** = "Review: flow + voice",
**F1–F15** = "Review: facts", **O1–O9** = ORCH_FIXES.md.

## 0. Rules for every reviser

- Edit only the files of your group (Section 4). Read files outside it, never write them. Do not edit anything
  outside `paper/ieee`. Do not git commit or push. Do not contact anyone.
- Read the current file first. 00_abstract, 01_intro and 02_rules already hold part of the revision
  (21:06); keep what is already done and listed as "done" below.
- No placeholders, TODO, VERIFY, "to appear", empty boxes or code listings. Program names (`cylcgt`,
  `kpsolve`, ...) appear only in Code Availability (13_verify). In the body write "our CGT engine", "our
  king-and-pawn solver", "the independent whole-board solver", "the census scanner".
- Every number you keep must trace to RESULTS.md, delegate/REVIEW.md, delegate/checks/*.out, kings/REPORT.md,
  atlas/*/REPORT.md, realchess/targets18/*, engine/runs/*/analysis.md or the SPEC fact sheet as corrected by
  ORCH_FIXES.md. If you cannot trace a number, delete it. Add no new numbers except where this plan names
  the source.
- Do not rename or delete a `\label` listed under "labels to keep" for your group. New labels named in this
  plan must be added exactly as spelled, because other groups will `\ref` them.
- Build check before you stop: `cd paper/ieee && tectonic -X compile main.tex` must give no errors and no
  undefined references in your files (other groups' work in progress may cause warnings elsewhere).
- Measure your words with this command (prose outside figures and tables; captions are budgeted separately):

```
f=sections/XX.tex; sed -e 's/%.*$//' "$f" | perl -0pe 's/\\begin\{(figure\*?|table\*?)\}.*?\\end\{\1\}//gs' \
 | sed -E 's/\\[a-zA-Z@]+\*?(\[[^]]*\])?//g; s/[{}$\\]/ /g' | wc -w
```

  Budgets are hard ceilings. Captions: at most 40 words per figure caption (50 for a figure with four or more
  panels), 25 per table caption, 30 per table note.

### Evidence-label policy (applies to every group; supersedes SPEC "Evidence labels")

The hard rule is that a proof checked only by AI models is never [P]. Every proof in this project was drafted
and checked by AI models (kings/theory/LOOPY.md: "All checkers are AI models; no human has re-derived these
proofs"). So the labels mean:

- `\lab{P}`: the complete proof is printed in this paper (cut lemma, the B-cancellation example, the
  T = 1 counter-promotion proposition, sandwich lemma, ring rule). The reader can check it on the page.
- `\lab{AI}` (new): proof only sketched here; the full proof is in the repository and has been checked by AI
  models, human check pending. Use it for the validity theorem (V1)–(V4), the loopy theorem and the
  sum-safety (HSS) theorem. This settles P19, F1, F2, O3 and O9.
- `\lab{C2}`, `\lab{C1}`, `\lab{Conj}` as before. A statement whose proof has a known gap (the certificate
  theorem, kings T2.7; the sharp form of T1.14) is `\lab{Conj}` or is described as "proof incomplete";
  never [P] or [AI].
- Never put a label directly beside a citation (P10).

## 1. Length

The PDF is 19 pages. Target: **at most 14 pages for the review (ToG) build, including references and the
appendix**; the arXiv build adds the table of contents (about 0.3 page). Estimate after this plan: about
13 pages (review build), so there is roughly one page of margin for float placement.

Measured now (prose words outside floats; current files):

| File | Now | Budget | Cut | Main cuts |
|---|---:|---:|---:|---|
| 00_abstract | 212 | 195 | 8% | ToG limit 200 |
| 01_intro | 745 | 580 | 22% | Fig. 1 photo, label paragraph, shorter Elkies paragraph |
| 02_rules | 1272 | 950 | 25% | value definitions move to first use, race-rule and board trims |
| 03_basic | 803 | 620 | 23% | two boards out of the figure, opening paragraph |
| 04_kings | 1515 | 950 | 37% | loopy subsection to theorem + 1 sentence, certificate, proof sketch |
| 05_sums | 1392 | 900 | 35% | puzzle walk-throughs, principles, Fig. 6 |
| 06_atlas | 710 | 420 | 41% | VI-D "correction", C4 ring story, value list |
| 07_targets | 621 | 480 | 23% | duplicated G−T sentence, theorem wording, textbook results |
| 08_star2 | 1316 | 920 | 30% | "What this answers", census paragraph, Fig. 11, scope |
| 09_real | 1101 | 700 | 36% | IX-B bullets to prose, stops, closing paragraph |
| 10_tablebases | 849 | 640 | 25% | rules repeat, Figs. 12–13, rook-pawn repeat |
| 11_dawson | 1023 | 700 | 32% | "What was wrong", misère, sums warning |
| 12_engines | 894 | 600 | 33% | intro, Lc0 paragraph, ChessSums, learning |
| 13_verify | 438 | 200 | 54% | XIII-A, Table VII, XIII-C, XIII-D |
| 14_conclusion | 559 | 350 | 37% | opening paragraph, each problem ≤ 2 sentences |
| **Total** | **13,450** | **9,205** | **32%** | |
| appendix text | 139 | 90 | | table from 38 rows to 18 |

Floats (16 figures, 8 tables now; 10 figures, 7 tables after):

| Float now | Decision | Owner |
|---|---|---|
| Fig. 1 cover photo (CoverPic.png) | **drop**, with refs.bib `CoverImage` (P4: CC BY-SA ShareAlike, 40% of a column) | A |
| Fig. 2 basic positions (figure*, 8 boards, 2 rows) | **one row of six boards**, each `0.16\textwidth`; drop (a) e4/e5 and (h) a2/a6 (both stay as text) | B |
| Fig. 3 e.p. test | keep, `0.36\columnwidth` | B |
| Fig. 4 king groups (2 rows) | keep, **one row of three** at `0.32\columnwidth` | C |
| Fig. 5 puzzles (figure*) | keep | C |
| Fig. 6 sum counterexample | **drop**; the position stays in Prop. sumcounter and the appendix is not needed (pawns only) | C |
| Fig. 7 hot / ring values | keep | D |
| Fig. 8 small values (figure*) | **single column**, three subfloats at `0.32\columnwidth` | D |
| Figs. 9 + 10 (candidate; positions A, B) | **merge** into one column figure `fig:star2`, three subfloats at `0.32\columnwidth` | E (G regenerates the candidate board at small size) |
| Fig. 11 \*2 count bar chart (0,0,0,2,4) | **drop**; the five counts stay in the text | E |
| Fig. 12 tablebase bars | **drop** (P14; repeats Table IV) | F |
| Fig. 13 KPK bars | **drop** (P14; repeats Table V) | F |
| Fig. 14 KPK rook pawn | keep, `0.4\columnwidth` | F |
| Figs. 15, 16 Dawson boards, Grundy plot | keep (Grundy is first in the fallback list) | F |
| Tables I–VI | keep (captions fixed) | C, D, E, F, F, G |
| Table VII cross-checks | **delete**; one paragraph in 13 | G |
| Table VIII positions (full page) | **compress** to the 18 rows with kings or with no pawn list elsewhere, about 0.4 page | G |

What moves where: the specific value definitions (nimbers, ups, up-second, tinies) leave the notation
paragraph of II and are defined at first use (III and VII), as Elkies does (GUIDELINES G.1). Program
cross-checks that a section already states stay in that section only; 13 keeps only the checks no section
states. Nothing moves to supplementary material in this round.

Fallback if the review build still exceeds 14 pages after integration (A decides, in this order): drop the
Grundy figure (F); fold Table III into one sentence (E); drop Fig. 3 (B); move the appendix table to the
supplement (G).

## 2. Decisions on every finding

Status: **A** = accept, **M** = modify (instruction in the group list), **R** = reject, **done** = already in
the 21:06 files (owner only re-checks). Each change has exactly one owner; a finding that touches files of
two groups is split by file (owner shown as "X: part").

### Production (P1–P19)

| Id | Decision | Owner |
|---|---|---|
| P1 | M: target 14 pages, not 10–12 (orchestrator decision); budgets of Section 1; appendix compressed, not moved | A (integration and page check) |
| P2 | M: build switch as in Section 3; the review build prints "anonymized for review" instead of an anonymous.4open.science link | A |
| P3 | A: full AI disclosure in the Acknowledgment (text model in group A) | A |
| P4 | M: drop the photo and `CoverImage` | A |
| P5 | M: no affiliation exists in the repo (part1_2025.tex has none), so the `\thanks` keeps the e-mail only; running heads as in Section 3 | A |
| P6 | A: `\appendix[Positions]` | A: main.tex line; G: delete `\section{Positions}` |
| P7 | A | C: Table I caption; F: Table V caption |
| P8 | A | C |
| P9 | A | E: eq. (1) unnumbered; F: cite eq:dawson in the text |
| P10 | M: `\lab` typeset in sans serif (one line in macros.tex); no label beside a citation | A |
| P11 | M: fix the entries; keep the key `WuYuLandry2020` (renaming it would touch three groups' files for an invisible change) | A |
| P12 | A | B: 03; D: 07 |
| P13 | A: `\IEEEtriggeratref` chosen after the final build | A |
| P14 | A | F |
| P15 | A | E |
| P16 | A | A |
| P17 | R: packaging, not source; the arXiv tarball will include only the files `\includegraphics` uses. No files are deleted in this round | — |
| P18 | M: replace "game solving" with "game theory"; keep "nimbers" (author keyword, no Thesaurus equivalent) | A |
| P19 | A via the label policy ([AI] for sketched proofs) | C |

### Flow and voice (V1–V33)

| Id | Decision | Owner |
|---|---|---|
| V1 | A as the budgets of Section 1 | A (page check) |
| V2 | done; A changes the bullet labels to the new policy | A |
| V3 | A | A |
| V4 | M: Table VII is deleted; the new 13 paragraph makes no "every row agrees" claim (the KPK difference stays in 10) | G |
| V5 | A | E |
| V6 | A | E: sentence in IX-B; A: item 1 of 14 points to it |
| V7 | A | G (13 keeps one sentence; the Acknowledgment is P3) |
| V8 | done in 02 | D: shorten Theorem thm:eighth, delete the sentence after it |
| V9 | M: prose as proposed, with the corrected counts of F6 and the status of O7 | E |
| V10 | done | B |
| V11 | M: 02 keeps the birthday definition (done); 08 deletes its parenthesis and points to Section II | E |
| V12 | done in 02 | E: delete the stops sentence in 09 |
| V13 | A | C |
| V14 | done in 02; V-C keeps the full explanation | C |
| V15 | A | F |
| V16 | A | E |
| V17 | A | E |
| V18 | A, merged into the end of VI-C (no own subsection) | D |
| V19 | A | D |
| V20 | M: XIII-A is deleted; the "independent" clause moves into the label sentence of I | A: 01; G: delete |
| V21 | A | G |
| V22 | done | A |
| V23 | done | A |
| V24 | A | B: 03; D: 07; G: 12 (02 done) |
| V25 | A, as a style rule | every group, own files |
| V26 | A | C |
| V27 | A: 04 names the f–h group T; everyone writes "beside T" and "in the default setting" | C defines; every group applies |
| V28 | A, as a style rule | every group |
| V29 | A | D |
| V30 | A | D |
| V31 | A | F |
| V32 | A | G |
| V33 | A | C |

### Facts (F1–F15)

| Id | Decision | Owner |
|---|---|---|
| F1 | A: the certificate implication is "proof incomplete" [Conj]; the proposition is restated to the counter-promotion part [P] | C |
| F2 | M: the label policy replaces the "8 of 9" sentence; the Acknowledgment says which systems checked proofs | A |
| F3 | done | A |
| F4 | A: "conditional on the king freeze and on a rerun with underpromotions"; "one side of one end position" | E: 09; A: 01 bullet wording |
| F5 | A | C |
| F6 | M: the breakdown that traces to `realchess/targets18/bounds_after_le7.json` is **302** resolved sides with at most seven men: 290 one-sided sides (283 agree, 5 disagree, 2 draws) and 12 race sides. RESULTS.md's "306" does not trace to any file, so do not use it | E |
| F7 | A: the 1/8 end-position results are [C1] | E |
| F8 | A | C |
| F9 | done (02 text and Fig. 3 caption) | B |
| F10 | A | D |
| F11 | A | D |
| F12 | A | D |
| F13 | A: 06 states the census scope once; 08 adds "in the default setting" to the minimality sentence | D: scope; E: qualifier |
| F14 | A: drop the "!" | F |
| F15 | M: Drummond-Cole needs pieces (notes/lit_cgt_chess.md, full text read); Wu–Yü–Landry is a Stanford Math 191 paper dated December 2010 (same note); Elkies 2002 pp. 61–78 stays (refs.bib header: checked against the SLMath volume contents); CoverImage is dropped | A |

### Orchestrator fixes (O1–O9, all mandatory)

| Id | Change | Owner |
|---|---|---|
| O1 | 08: "dominated" is wrong for A (a7–a6, b7–b5) and B (d2–d3, c2–c4); they are reversible (wording in group E) | E |
| O2 | 12: Lc0 perfect at all four budgets, 10^3 to 10^6 nodes; all 17 draws called from 10^3 nodes on | G |
| O3 | 04: cite only plain-PROVED items and computed results; with the label policy they are [AI] | C |
| O4 | 08: five-file witnesses [C2]: no change | E (check) |
| O5 | 01: Drummond-Cole "needs officers": reword as in F15 | A |
| O6 | "exactly two" seven-pawn \*2 stays [C1]: no change | E (check) |
| O7 | 09: 0 ≤ O ≤ 1/8, one open side; abstract already updated | E (09); A (abstract: done) |
| O8 | 09: only witness `W a3 b3 c2 e2 / B a6 c5 d5 e3` embeds cleanly beside T (12 men); 08 must not claim all five-file witnesses embed | E |
| O9 | 04/13: the 17 "PROVED after repair" items are AI-checked; K2 recomputed every kings number; the 1.4M cross-check validates the solver, the theory predictions are [C1] | C (04); A (Acknowledgment names K2/K3 systems) |

### Cross-section repetition: who keeps it

| Item | Kept in | Replaced by a pointer (or deleted) in |
|---|---|---|
| Evidence labels and "independent program" | 01 (one sentence) | 13 (deleted) |
| AI-use disclosure | Acknowledgment (main.tex) | 13 (one sentence), 01 (none) |
| Board rules, slider rule, seam adjacency | 02 II-A | 10 ("Pieces move as in Section~\ref{sec:rules} and wrap round each glued edge.") |
| "No rook pawns, all files alike" | 01 | 02 (delete "there are no edge pawns"), 10 (delete line-120 sentence), 11 (keep only "every file is alike" as the premise) |
| Passed-pawn convention, race rules, nine settings, default setting | 02 II-B, II-C (`\label{sec:ep}`) | every other section writes "in the default setting" / "in all nine settings (Section~\ref{sec:ep})" |
| CGT notation, mean, temperature, stops, birthday | 02 II-E (`\label{sec:notation}`) | 05 Principle 2, 08 birthday, 09 stops |
| \*, ↑, ↓, ⇑, ⇑\*, Tiny 1 definitions | 03 at first use | 02 notation (delete the specific values) |
| \*2 | 01 (informal: either player may move to 0 or \*); 02 lists `\nim{2}=\game{0,\star}{0,\star}` in one clause | 08 (opens with the pointer of V16) |
| ↑², ↑²\*, tiny(x) | 07 | 02 (delete) |
| Trébuchet, the group T, frozen kings | 02 (one bullet), 04 IV-A (full; defines T) | 07, 08, 09, 12 captions and text: "beside T (Fig.~\ref{fig:trebuchet})" |
| King-and-pawn solver and its 1,418,480-position check | 04 | 09 (pointer), 13 (deleted) |
| Puzzle 2 king group | 04 IV-D | 05 (one clause + `\ref{fig:kinggroup72}`) |
| +B / −B cancellation, HSS, sum vs whole board | 05 V-C | 02 (done), 08 (pointer), 13 (pointer) |
| Census definition and scope | 06 (opening) | 02 (pointer, done), 08 Theorem census ("the census of Section~\ref{sec:atlas}") |
| Atlas and its minimax check | 06 | 13 (deleted) |
| ⇑\* on a single file (W a2 / B a6) | 03 (text walk-through) | 06 (pointer to `\ref{sec:basic-inf}`) |
| C4 ring and candidate e.p. story | 08 | 06 (V19 text) |
| G − T = 0 check | 07 table note | 07 text (deleted), 13 (deleted) |
| 1/8 walk-through and reachability | 07 | 09 (pointer) |
| Census three-program check, seven-pawn three programs | 08 | 13 (deleted) |
| Tablebase solver agreement, KPK 6-position difference | 10 | 13 (deleted) |
| Dawson two-program check, misère quotient check | 11 | 13 (deleted) |
| Move generator 160/160, brute-force sum solver, whole-board minimax 1,070 | 13 (only home) | — |
| Kings sweep (159/500) | 04 | 12 (pointer) |

## 3. Builds (owner A, in main.tex)

1. **Default = named arXiv build.** After `\input{sections/00_abstract}` (abstract and Index Terms) add a
   compact table of contents: `{\setcounter{tocdepth}{1}\tableofcontents}` (sections only), guarded by
   `\ifdefined\anonbuild\else ... \fi`. Check that IEEEtran's `\tableofcontents` builds in journal mode and
   that the drop cap of the Introduction still works after it. Running heads in this build:
   `\markboth{Bhattacharjee: Chess Endgames on a Cylindrical Chessboard}{Bhattacharjee: Chess Endgames on a
   Cylindrical Chessboard}` (do not print "IEEE Transactions on Games" on a preprint that is not yet
   submitted; the IEEE preprint notice of GUIDELINES F is added only at submission).
2. **Review build.** New file `main_review.tex`, exactly:
   ```
   \def\anonbuild{}
   \input{main}
   ```
   Build with `tectonic -X compile main_review.tex`. Under `\ifdefined\anonbuild` the paper:
   - prints `\author{Anonymized for review}` with no `\thanks`;
   - uses `\markboth{IEEE Transactions on Games}{Chess Endgames on a Cylindrical Chessboard}`;
   - sets `pdfauthor={}` (named build: `pdfauthor={Aritro Bhattacharjee}`; both: `pdftitle`);
   - drops the Morley sentence from the Acknowledgment and keeps the tool maintainers and the AI disclosure;
   - prints "anonymized for review" for the repository: define in main.tex
     `\newcommand{\codeurl}{\url{https://github.com/aritroBh/cylindrical-chess-cgt}}` (named) or
     `\newcommand{\codeurl}{(anonymized for review)}` (review). G uses `\codeurl` in Code Availability.
     `\repourl` in macros.tex stays as it is;
   - omits the table of contents.
3. **Self-citation.** 01 already contains `\bytheauthor` (currently undefined, so the build breaks). Define
   it in main.tex: named build `\newcommand{\bytheauthor}{ by the author}`, review build empty. In refs.bib
   give `Bhattacharjee2025` the field `author = {{\studyauthor}}` and define `\studyauthor` in main.tex as
   `A.~Bhattacharjee` (named) or `Anonymous` (review); check that both .bbl files typeset it. The other
   citations of the 2025 study (05, 11) already read in the third person and need no change.
4. **AI disclosure** in `\section*{Acknowledgment}` (GUIDELINES E): name each system and what it did; 13 keeps
   one sentence. Take the systems from `delegate/run.sh` (TOOLS, MODELS), `delegate/REVIEW.md`,
   `kings/delegate/run.sh`, `kings/REPORT.md` and `kings/theory/LOOPY.md`, and check `delegate/briefs/T16*`
   for any text drafted by Codex. Model text (correct it against those files; name nothing they do not
   record):
   > The author thanks T.~Morley for mentoring the 2025 study on which this work builds [named build only],
   > and the maintainers of the Lichess tablebase, Stockfish and Lc0. AI systems were used throughout, under
   > the author's direction; the author is responsible for the content. Claude (Opus 5.5, Anthropic), run in
   > Claude Code, wrote most of the software, ran the searches, drafted the proofs and the figures, and
   > drafted the text of every section from the author's 2025 study and the project notes. Codex (OpenAI)
   > wrote the independent whole-board solver and the census scanner that found the seven-pawn positions.
   > Nemotron 3 Ultra (NVIDIA) and MiniMax M3.1 Flash (MiniMax), run through the Kilo and OpenCode tools,
   > re-derived and repaired proofs and recomputed the reported king-and-pawn numbers; further free models,
   > chosen automatically by the OpenCode and OmniRoute routers and not recorded by name, carried out
   > delegated checks. Statements labeled [AI] have been checked only by these systems.
5. **Other main.tex items.** `\appendix[Positions]` replaces `\appendices` (P6); `\hypersetup{pdftitle=...}`
   (P16); `\IEEEtriggeratref{N}` before `\bibliography` once the final reference list is known (P13); the
   Acknowledgment must not `\ref{sec:ai}` (G deletes that subsection). Keep the subfigure shim and theorem
   styles.
6. **Integration (A, last).** Build both `main.tex` and `main_review.tex`; check no errors, no undefined
   references, no overfull box wider than 5 pt; `pdfinfo main_review.pdf` must report ≤ 14 pages; grep
   both PDFs' text (`pdftotext`) for TODO and VERIFY (none allowed), and the review PDF for "aritroBh",
   "Bhattacharjee" and "Morley" (none allowed); apply the fallback list of Section 1 if needed.

## 4. Owner groups

### Group A: main.tex, main_review.tex (new), macros.tex, refs.bib, 00_abstract, 01_intro, 14_conclusion

Budgets: 00 ≤ 195 words; 01 ≤ 580; 14 ≤ 350.

Changes:
- **Section 3 items 1–6** (P1, P2, P3, P5, P6 main.tex line, P13, P16, F2, O9 Acknowledgment part).
- **macros.tex (P10):** `\newcommand{\lab}[1]{\textsf{\footnotesize[#1]}}`; nothing else changes there.
- **refs.bib (P11, F15, P4):** delete `CoverImage`; `PyTorch` author = `{Adam Paszke and others}`;
  `WuYuLandry2020`: year 2010, `howpublished = {Math 191 paper, Stanford Univ.}`, keep the URL and the
  "Accessed" note (key unchanged); `DrummondCole2005` title `Positions of value {$\star2$} in generalized
  {D}omineering and chess`; `Bhattacharjee2025` author `{{\studyauthor}}` (Section 3.3).
- **00 (P18, V22 done, O7 done):** trim to ≤ 195 words; Index Terms: *Chess, combinatorial game theory,
  endgame tablebases, game theory, nimbers*. Keep: no symbols, no numbers in digits beyond what is there,
  "star two", "one-eighth", "up-second star", "Tiny 1".
- **01:**
  - delete the Fig. 1 float and every reference to `fig:cover` (P4); the first paragraph then ends "...no
    edges and no corners." without "(Fig. 1)";
  - Drummond-Cole (F15, O5): "...and Drummond-Cole built positions of value $\nim{2}$ in chess with the help
    of pieces other than kings and pawns~\cite{DrummondCole2005}";
  - label sentence (V20 and the policy): "Each theorem and headline number carries a label: \lab{P}, the
    complete proof is in this paper; \lab{AI}, the proof is sketched here and the full proof, in the
    repository, has been checked by AI models but not yet by a human; \lab{C2}, two independently written
    programs agree, where the second was written from the rules alone; \lab{C1}, one program; and
    \lab{Conj}, a conjecture.";
  - bullets: "prove a cut lemma \lab{P} and a sum-safety theorem \lab{AI}"; Kings bullet "\lab{AI}";
    real-chess bullet: "...and the $1/8$ hinges on one side of one end position, which a search with queen
    promotions only leaves open \lab{C1}" (F4); keep the ring bullet at \lab{P} (it follows from the cut
    lemma) with $1/8$, $\upsec\star$ and Tiny~1 at \lab{C2};
  - roadmap (done) gets one clause: "and the Appendix gives the FEN of each position with kings";
  - cut to budget: shorten the Elkies paragraph (keep the two conventions as bullets), keep the
    three-way cylinder paragraph (V23 done). "Tiny 1" in prose (V28).
- **14 (V3, V6, F1, ≤ 350 words):** opening paragraph ≤ 90 words, no numbers beyond those in the problems;
  item 1: "...exactly $1/8$. The same pipeline then applies to $\upsec\star$ and Tiny~1
  (Section~\ref{sec:real-eighth})." and "with underpromotions allowed"; item 2: no new counts beyond
  "one program \lab{C1}" and the five-file search; item 3: "For $T=1$ the counter-promotion condition of
  the certificate holds in every context \lab{P}; that a certificate implies a decisive punishment is still
  unproved, and real tr\'ebuchets have $T$ of about 5 to 7. Conjecture~\ref{conj:horizon2} ..."; item 5:
  replace the last sentence by V3's text; every item ≤ 2 sentences (item 1 may have 3).

Labels to keep: `sec:intro`, `sec:conclusion`. Removed: `fig:cover`.
Coordinate: G uses `\codeurl`; nobody may `\ref{sec:ai}`; E adds `\label{sec:real-eighth}` (your item 1
points to it); C keeps `conj:horizon2`.

### Group B: 02_rules, 03_basic

Budgets: 02 ≤ 950 words; 03 ≤ 620.

02 (done: V8, V10, V12 stops, V14, V24, F9, birthday; keep them):
- add `\label{sec:ep}` to subsection C (En Passant and the Passed-Pawn Test) and `\label{sec:notation}` to
  subsection E (Notation); others will `\ref` both;
- II-A: delete "All files are now equivalent, and there are no edge pawns." (01 says it) and tighten the
  knight/king sentence (keep the corrected squares a3, b2 for the knight and a1, a2 for the king);
- II-B: delete "So a standard win is a checkmate, ..." (V25); one line per race rule;
- II-E (GUIDELINES G.1): keep game form, sums, canonical form and equality, outcome classes, numbers with
  the example $1/2=\game{0}{1}$, switches $\pm x$ and $a\pm x$, the "sum without plus sign" convention,
  $\nim{2}=\game{0,\star}{0,\star}$ in one clause, birthday, mean and temperature (one sentence), stops.
  Delete the definitions of $\star$, ${\uparrow}$, ${\Uparrow}$, ${\downarrow}$, $\upsec$ and $\tinyg{x}$
  and the infinitesimal sentence: 03 and 07 define them at first use;
- Fig. 3: `width=0.36\columnwidth`; caption ≤ 35 words, keeps "value $0$" (F9).

03:
- figure: one row of six subfloats at `0.16\textwidth` in this order: zero across the seam, 1, 2, $\star$,
  ${\uparrow}$, Tiny 1 (drop the e4/e5 board and the a2/a6 board); caption ≤ 50 words, says "(cylinder:
  files a and h adjacent)" and keeps the e.p. remark for the value 2 board;
- "Let us begin with the zero game" (P12, V24); describe W e4 / B e5 in one sentence without a board;
- define each value at first use: $\star=\game{0}{0}$, ${\uparrow}=\game{0}{\star}$ ("positive, yet smaller
  than every positive number"; an *infinitesimal*), ${\downarrow}=-{\uparrow}$ by switching colors,
  ${\Uparrow}={\uparrow}+{\uparrow}$, $\tinyg{1}=\ggame{0}{0\mid-1}$;
- keep the ⇑\* walk-through for W a2 / B a6 as text (≤ 70 words): this is its only home; add
  `\label{sec:basic-inf}` to subsection "The Infinitesimals" (D points to it);
- opening paragraph ≤ 90 words; keep the reversible-move remark (later sections rely on it);
- relabel every "Fig.~\ref{fig:basic}(x)" to the new letters.

Labels to keep: `sec:rules`, `def:epaware`, `thm:cut`, `fig:ep_test`, `sec:basic`, `fig:basic`. New:
`sec:ep`, `sec:notation`, `sec:basic-inf`.
Coordinate: D replaces its "Fig.~\ref{fig:basic}(h)" with "Section~\ref{sec:basic-inf}"; D defines
up-second; nobody else refers to subfigure letters of Fig. 2.

### Group C: 04_kings, 05_sums

Budgets: 04 ≤ 950 words; 05 ≤ 900.

04:
- heading "Kings: The Tr\'ebuchet and When It Is Exact" (P8);
- first paragraph (V26): "So far a player with no pawn move simply lost. In chess that player would move
  the king instead, or, with no king move either, be stalemated, which is a draw." Keep the solver sentence
  with $1{,}418{,}480$ \lab{C2} (its only home) and add, from O9: "this validates the solver; the
  predictions of the theory below are \lab{C1} computations";
- IV-A: merge the repeated sentence (V26); after the f–h group add "We call this group T and place it
  beside every ordinary-board pawn position in this paper" (V27);
- figure: one row, three subfloats at `0.32\columnwidth`, caption ≤ 40 words;
- Theorem thm:validity: label `\lab{AI}` (O3, O9, P19); proof sketch ≤ 70 words, ending "The full proof
  is in the repository." Keep the paragraph listing how each condition fails (≤ 60 words);
- certificate (F1): define the horizon-$T$ certificate in ≤ 2 sentences, then "That a certificate implies
  (V3) is plausible, but its proof is incomplete \lab{Conj}." Restate Prop. prop:horizon1: "For $T=1$, the
  counter-promotion condition of the certificate holds in every context without a passed pawn \lab{P}"
  with the existing one-line proof. Keep Conj. conj:horizon2 and the $T\approx5$--$7$ sentence;
- IV-C loopy: on/off/dud in one sentence, Theorem thm:loopy `\lab{AI}` with no proof sketch, then one
  sentence of consequence (V1);
- IV-D: ≤ 110 words; "The group is therefore frozen for black only" (V25);
- IV-E sweep (F5, V33): "We placed every small pawn component beside a trébuchet, on cylinders with six
  and seven files and six ranks and on an ordinary board with five files and six ranks, and solved each
  position with the kings played out. Under the textbook test, 159 of the 500 components ..." Then: "Under
  the e.p.-aware test the 18 failures through en passant disappear, and on the seven-file cylinder the
  mismatches fall from 143 to 138" (kings/REPORT.md line 182). Keep 94 / 449 / 41 / 7 (RESULTS.md line 37)
  at \lab{C1}.

05:
- Principle 1 one sentence; Principle 2 as V13;
- Table I caption "Puzzles of Fig.~\ref{fig:puzzles}: Claimed and Exact Values \lab{C2}" (P7);
- Puzzle 1 ≤ 160 words, with F8: "since every other move loses (h6--h5, for example, allows a5--a6)";
  Puzzle 2 ≤ 100 words, kings in one clause pointing to `fig:kinggroup72`; Puzzle 3 ≤ 120 words;
- V-C: keep the cancellation example \lab{P}, Def. def:hss, Theorem thm:hss with `\lab{AI}` (P19) and a
  ≤ 50-word sketch; label the random-sample sentence \lab{C1}; delete Fig. 6 and its `\ref`; keep
  Prop. prop:sumcounter (pawn list in the statement) and Prop. prop:condE with "the ordinary board with six
  files and six ranks" (V33); keep the two-models paragraph (≤ 110 words; its only home).

Labels to keep: `sec:kings`, `fig:kings`, `fig:trebuchet_2025`, `fig:trebuchet`, `fig:kinggroup72`,
`thm:validity`, `prop:horizon1`, `conj:horizon2`, `thm:loopy`, `sec:kings-sweep`, `sec:sums`,
`sec:sums-hss`, `fig:puzzles`, `fig:puzzle71`, `fig:puzzle72`, `fig:puzzle73`, `tab:puzzles`, `def:hss`,
`thm:hss`, `prop:sumcounter`, `prop:condE`. Removed: `fig:sum_counter`.
Coordinate: every group writes "beside T (Fig.~\ref{fig:trebuchet})"; 14 (A) states the horizon result in
your new wording.

### Group D: 06_atlas, 07_targets

Budgets: 06 ≤ 420 words; 07 ≤ 480.

06:
- opening: define *the atlas* and *the census* (one name each; drop "flat census"). Census scope, once
  (F13; atlas/flat8/rerun/REPORT.md line 20): "ordinary boards with eight ranks and one to four files, at
  most six pawns, all on ranks 2--7, at least one pawn per side and no passed pawn, counted up to translation
  and mirror image: $231{,}071$ records standing for $459{,}443$ positions". Atlas check (F12): "an
  independent minimax program confirms the winners of all $12{,}568$ rings and of $4{,}000$ random ordinary
  components";
- value families: one sentence; ⇑\* "on a single file (Section~\ref{sec:basic-inf})";
- hottest position: keep the walk-through, ≤ 90 words;
- cylinder-only: Prop. prop:cylonly, then V19's text for the C4 ring, then V18's text (no own subsection,
  no project history);
- Fig. hot3: keep; caption ≤ 50 words.

07:
- define up-second here: $\upsec=\game{0}{{\downarrow}\star}$ and $\upsec\star=\game{0,\star}{{\downarrow}}$;
  delete "were defined in Section II";
- delete the text sentence on $G-T=0$; the table note says "Each identity $G-T=0$ was confirmed by an
  independent C solver \lab{C2}." (V29);
- Theorem thm:eighth: "... has value exactly $1/8$ in all nine settings (Section~\ref{sec:ep}) and for
  every assignment of outcomes to its race positions." Delete the next sentence (V8). F10: "A third,
  separately written solver agrees in all nine settings; it was run on the mirror image, which has the same
  value by symmetry.";
- "To see why, look at Fig.~\ref{fig:eighth}(a)." (P12, V24); walk-through as V30;
- Tiny 1 (F11): "under every race rule with en passant on (count rule \lab{C2}, the others \lab{C1})";
- Fig. 8: single-column figure, three subfloats at `0.32\columnwidth`; caption "... beside T
  (Fig.~\ref{fig:trebuchet}), each a legal 10-man position (ordinary board)";
- the two textbook results: ≤ 80 words.

Labels to keep: `sec:atlas`, `fig:hot3`, `prop:cylonly`, `sec:targets`, `tab:targets`, `fig:eighth`,
`thm:eighth`.
Coordinate: B owns `sec:basic-inf`; E's Theorem census refers to your census definition; E's IX points to
your walk-through.

### Group E: 08_star2, 09_real

Budgets: 08 ≤ 920 words; 09 ≤ 700.

08:
- open with V16's text (no third definition of $\nim{2}$);
- one figure `\label{fig:star2}`, three subfloats at `0.32\columnwidth`: (a) candidate
  `\label{fig:star2_textbook}`, (b) A `\label{fig:star2_seven_a}`, (c) B `\label{fig:star2_seven_b}`,
  each beside T; caption ≤ 45 words with the values (candidate: $\nim{2}$ under the textbook test,
  $\game{2\pm1}{-2\pm1}$ under the e.p.-aware test). Use the small `star2_textbook.pdf` that G regenerates;
- candidate walk-through ≤ 200 words; the display becomes unnumbered `\[ G=\game{2\pm1}{-2\pm1} \]` with
  \lab{C2} in the sentence (P9);
- Theorem thm:census: "In the census of Section~\ref{sec:atlas}, in the default setting, no position has
  value $\nim{k}$ with $k\ge2$; it has $6{,}724$ zeros and $4{,}042$ stars." Programs paragraph ≤ 90
  words; V11: "Every position in scope has birthday (Section~\ref{sec:notation}) at most $292$, so no
  larger nimber can occur." Keep the textbook counts 6,470 / 3,891 (RESULTS.md line 46);
- Theorem thm:star2seven "in the default setting"; programs in one sentence;
- O1, position A: "Black's other moves are reversible: a7--a6 (worth $\game{2}{0}$) and b7--b5 allow white
  replies worth $2$ and $3$, both at least $\nim{2}$, and c5--c4 lets d3$\times$c4 free white's d2 pawn,
  which gives white $+\BIG$."
  Position B: "The moves d2--d3 and c2--c4 are reversible, since black's replies reach $-2$ and $-3$."
  Keep the existing a6--a5 sentence (reversible through b4$\times$a5, then c6--c5 to $\star$). If you state
  any intermediate value not in ORCH_FIXES item 1, recompute it first (read-only run of the CGT engine) or
  leave it out;
- Table III keep; delete Fig. 11 and give the counts in text ("none with four to six pawns, two with
  seven, four with eight"), with the existing [C2]/[C1] split; F13: "seven is the least number of pawns in
  a $\nim{2}$ on ordinary boards of width at most four, in the default setting \lab{C2}";
- five files (P15, O8): the three witnesses as a three-item list (or one per line); do not say that all
  three embed beside T;
- "What this answers": replace with V17's two sentences.

09:
- oracle definition: "beside T"; keep Lemma lem:sandwich with its proof;
- delete the stops sentence (V12; 02 defines stops);
- IX-A: replace the last two sentences of the paragraph after Theorem thm:oracle-cand with V5's text;
  "A few other positions" ≤ 60 words;
- IX-B, `\label{sec:real-eighth}`, as prose (V9), ≤ 230 words including Prop. prop:eighth-real:
  - F6: "All $302$ end-position sides with at most seven men are resolved by the tablebase: $290$
    one-sided sides, of which $283$ agree with the model, $5$ disagree and $2$ are draws, and $12$ race
    sides";
  - the decisive set in one sentence (greedy search; eight larger end positions, five with eight men and
    three with nine; the eight-man disagreement \pos{W a3 a5 / B b4 b5}, black to move, black wins);
  - O7: "Our king-and-pawn solver, with queen promotions only, shows that all six sides of the three
    nine-man positions agree with the model and that white to move in \pos{W b2 b5 / B a5 b4} is a white
    win. Only black to move there is open, and on its own it decides the value.";
  - keep Prop. prop:eighth-real (0 ≤ O ≤ 1/8) at \lab{C1}; F7: all 1/8 end-position results \lab{C1};
  - F4 closing: "...whose oracle value is $1/8$, conditional on the king freeze and on a rerun with
    underpromotions.";
  - V6: "The same method applies to $\upsec\star$ and Tiny~1: their lower bounds already equal the target
    values, with 11 and 13 end positions of 8 to 10 men still open \lab{C1}." (RESULTS.md lines 266–267);
- IX-C (O8), ≤ 60 words: "Positions A and B have 11 men beside T, and the five-file witness
  \pos{W a3 b3 c2 e2 / B a6 c5 d5 e3} has 12. Their oracle values are open; until they are computed, the
  $\nim{2}$ of Theorem~\ref{thm:star2seven} is a model value."

Labels to keep: `sec:star2`, `fig:star2_textbook`, `fig:star2_seven_a`, `fig:star2_seven_b`,
`thm:census`, `thm:star2seven`, `tab:star2_settings`, `sec:real`, `def:oracle`, `lem:sandwich`,
`thm:oracle-cand`, `prop:eighth-real`. New: `fig:star2`, `sec:real-eighth`. Removed: `fig:star2_seven`,
`fig:star2_by_pawns`.
Coordinate: G regenerates `star2_textbook.pdf` at the small board size; until then the build still works
with the column-size file. A's item 1 of 14 points to `sec:real-eighth`.

### Group F: 10_tablebases, 11_dawson

Budgets: 10 ≤ 640 words; 11 ≤ 700.

10:
- rules (V15): "Pieces move as in Section~\ref{sec:rules} and wrap round each glued edge." Keep castling,
  fifty-move, stalemate and legality; "Both dimensions of the board are even, so the coloring of the
  squares survives the gluing" (V31);
- "ordinary board" in prose and "Ordinary" as the Table IV column head (one name per concept);
- delete Figs. 12 and 13 and their `\ref`s (P14); the text does not repeat table numbers except 2.80\%;
- "\emph{KRK and KBNK cannot force mate on the cylinder.}" (V31);
- Table V caption "...Legal Positions and White Wins on the $8\times8$ Ordinary Board and Cylinder
  \lab{C2}" (P7);
- delete "On a cylinder every file is a center file, so there are no rook pawns." (V31); start with
  "Fig.~\ref{fig:kpk_rookpawn} shows the classic rook-pawn draw."; drop the "!" after 2.~Kh7 (F14);
- Fig. 14: `0.4\columnwidth`.

11:
- the Dawson recurrence keeps its number and the text cites it: "by~\eqref{eq:dawson}" (P9);
- rules paragraph and the one-move walk-through keep the 2025 voice (≤ 130 words for the walk-through);
- "What was wrong" ≤ 110 words; misère ≤ 90 words (keep the reduction, the quotient numbers, "did not
  converge"); "A warning about sums" ≤ 60 words;
- "The ring formula of~\cite{Bhattacharjee2025} ... is therefore right once ..." (V25);
- Theorem thm:ring keeps "\lab{P}, machine-checked for $n\le22$".

Labels to keep: `sec:tb`, `sec:kpk`, `tab:tb`, `tab:kpk`, `fig:kpk_rookpawn`, `sec:dawson`,
`fig:dawson_boards`, `fig:dawson_strip`, `fig:dawson_ring`, `fig:dawson_grundy`, `thm:ring`,
`eq:dawson`. Removed: `fig:tb_bars`, `fig:kpk_bars`.
Coordinate: the Grundy figure is first on A's fallback list; keep its caption ≤ 40 words so it can go
cleanly.

### Group G: 12_engines, 13_verify, appendix_positions, figures/

Budgets: 12 ≤ 600 words; 13 ≤ 200 (no table); appendix text ≤ 90 words.

12:
- intro ≤ 80 words; "The classes separate at a small fixed depth (Table~\ref{tab:sf})." (V24);
- Table VI caption "...by CGT Class (the Seven Decided Positions Are Omitted)" and delete the text
  sentence (V32);
- O2: "Lc0 ... is perfect at all four budgets, $10^3$ to $10^6$ nodes: every best move keeps the tablebase
  result and every evaluation matches it, and it calls all $17$ draws correctly from $10^3$ nodes on
  \lab{C1}" (engine/runs/lc0/analysis.md); "The suite is therefore too easy for both engines." (V25);
- ChessSums ≤ 110 words (4,887 traces to RESULTS.md line 311); engines on sums ≤ 120 words, "beside T or
  a shifted copy that our king-and-pawn solver confirms is a mutual zugzwang"; delete "There is an
  important caveat." and open with "The ground truth here is the CGT model with frozen kings, not real
  chess." "These numbers therefore measure ..."; "... the kind of certification that
  Section~\ref{sec:real} begins for $1/8$" (V32);
- learning ≤ 90 words.

13 (title may become "Reproducibility"; keep `\label{sec:verify}`):
- delete XIII-A (V20), Table VII (V1, V4), XIII-C (V21) and XIII-D with `\label{sec:ai}` (V7);
- one paragraph, run-in head `\emph{Cross-checks.}`, ≤ 120 words, with only the checks no section states:
  the brute-force sum solver ($55{,}195$ positions with at most two pawns a side on 3--5 files, three race
  rules, $15$ reference games: $4{,}967{,}550$ outcome predictions under the textbook test, e.p. on and off,
  plus $2{,}483{,}775$ under the e.p.-aware test), the whole-board minimax ($1{,}070$ single components),
  and the legal-move generator ($160$ of $160$ positions against Lichess, covering en passant, promotions,
  pins, checks, mates and stalemates; tablebase responses were cached). End: "Each section states its other
  cross-checks." One sentence on AI: "The AI systems used, and what each did, are listed in the
  Acknowledgment.";
- `\emph{Code availability.}` the SPEC paragraph with `\codeurl` (defined by A) instead of
  `\expandafter\url\expandafter{\repourl}`.

Appendix:
- delete the line `\section{Positions}\label{app:positions}`, and put `\label{app:positions}` alone on
  the first line (A writes `\appendix[Positions]` in main.tex);
- text ≤ 90 words: men lists, T, FEN placement only, default setting, and "Positions with pawns only are
  given by their pawn lists in the text; their FENs follow directly.";
- table: keep only these 18 rows, with a short Role column: the two trébuchets and the Puzzle 2 king group;
  Puzzle 2; Puzzle 3 as drawn; $1/8$; $\upsec\star$; Tiny 1; textbook $1/8$; textbook $\upsec$; the
  candidate; the second candidate; A; B; the five-file witness; the last decisive end position; the
  disagreeing end position; the KPK rook pawn. Delete the pawn-only rows (basic positions, e.p. examples,
  Puzzle 1, the two sum counterexamples, ⇑\*, ±3, the three rings). Run
  `PYTHONPATH=. .venv/bin/python paper/ieee/make_figures.py --check` from the repo root to confirm values
  and legality of anything you touch.

figures/ (and, for this one change, `make_figures.py` line 235): change the `star2_textbook` entry from
size `"column"` to `"small"`, regenerate that one PDF, and run `--check`. No other figure is wrong; do not
delete unused files (P17).

Labels to keep: `sec:engines`, `tab:sf`, `sec:verify`, `app:positions`, `tab:positions`. Removed:
`tab:checks`, `sec:ai`.
Coordinate: A defines `\codeurl` and `\appendix[Positions]`; E consumes the small `star2_textbook.pdf`.

## 5. Voice and style (every reviser)

- IEEE register in the author's plain 2025 voice: "we", short paragraphs, move-by-move walk-throughs that
  give the side to move and each side's main line, and dismiss a bad move in one clause ("b3--b4 is bad,
  since black's reply leaves $-3$"). Define a value the first time it is used. No hype ("novel",
  "comprehensive", "interesting", "important", "honest"), no project history ("our first report", "then
  left", "after these results"), no contractions ("Let us", never "Let's"), no "you".
- Do not open a paragraph with "So" (V25). Do not restate a definition or a result owned by another
  section; point to it with `Section~\ref{...}`, `Theorem~\ref{...}`, `Fig.~\ref{...}`. Section references
  print as "Section II-C" by themselves; never write "Subsection".
- One name per concept:

| Concept | Prose | Math / macro |
|---|---|---|
| board with a and h joined | cylinder | `\cyl{n}` |
| usual board | ordinary board (not "flat board", "plane") | `\flatb{n}` |
| the two passed-pawn tests | textbook test; e.p.-aware test (Definition~\ref{def:epaware}); e.p.\ off | — |
| race rules | count rule, mover rule, opponent rule | — |
| the nine combinations / ours | nine settings; default setting (count rule, e.p.-aware test) | — |
| king group in mutual zugzwang | tr\'ebuchet; the f–h group is T | — |
| kings held fixed | frozen kings (not "king freeze" except in "conditional on the king freeze") | — |
| pieces of a split position | component; ring; arc | — |
| data sets | the atlas; the census | — |
| real-chess value | oracle value | $O(X)$ |
| leaves of the model tree | end position; its two sides | — |
| sum model vs whole board | sum model; whole-board game | $S(X)$, $W(X)$ |
| programs | our CGT engine; our king-and-pawn solver; the independent whole-board solver; the census scanner | names only in Code Availability |
| values | star two (abstract only), Tiny~1, up-second star (abstract only), one-eighth (abstract only) | `\nim{2}`, `\tinyg{1}`, `\upsec\star`, $1/8$ |
| positions | position A, position B, the candidate, Puzzle 1–3 | — |
| colors | white, black (lower case; "Left"/"Right" once, in Section III) | — |

- American spelling: color, neighbor, favor (04 has "favour" twice), center, labeled, modeling,
  analyze; "underpromotion" (one word); "en passant" in roman; "e.p." only after it is introduced in II.
- Moves: en dash for moves, `a2--a4`; captures `b4$\times$a3`; numbered lines `1.~c4`, `1\ldots~b5`,
  check `+`, mate `\#`. No arrows in prose: a move "leaves", "reaches" or "gives" a value.
- Values only through the macros of macros.tex: `\nim{2}`, `$\star$`, `${\uparrow}$`, `${\Uparrow}$`,
  `${\downarrow}$`, `\upsec`, `\tinyg{1}`, `\game{..}{..}`, `\ggame{..}{..}`, `\BIG`, `\cyl{n}`,
  `\flatb{n}`; positions `\pos{W a2 c2 / B b7 d7}`; FENs `\fen{...}`; labels `\lab{P}`, `\lab{AI}`,
  `\lab{C2}`, `\lab{C1}`, `\lab{Conj}`. Write numbers with `{,}` separators, `2.80\%`, `$8\times8$`.
- Captions start with a noun (never A/An/The), make sense without the text, name each position and its
  value, and say "(cylinder: files a and h adjacent)" or "(ordinary board)". Tables: caption above, Title
  Case, no final period.
