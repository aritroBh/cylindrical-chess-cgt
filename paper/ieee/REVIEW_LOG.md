# Review log (revision of 2026-10-21)

Status of every finding in REVIEW_FINDINGS.md (P = production, V = flow and voice, F = facts) and every
orchestrator fix in ORCH_FIXES.md (O1-O9), after the seven revisers (groups A-G) and the integration pass.
"Applied" means done as the review or REVISION_PLAN.md asked; "modified" means done with a different wording
or scope, for the reason given; "rejected" means not done.

Final builds (in place, `tectonic -X compile --keep-logs`): `main.tex` and `main_review.tex` both compile with
no errors, no undefined references or citations and no Overfull boxes; both are 13 pages. The only TeX
warnings are one Underfull \vbox (badness 4913, page 12, float stretch) and the `TU/ptm` font-shape
substitution notes that every build has had (the PDF uses Nimbus Roman, i.e. Times). The review PDF contains
no "aritro", "Bhattacharjee", "Morley" or GitHub link, and neither PDF contains TODO or VERIFY.

## Production (P1-P19)

| Id | Status | Reason / where |
|---|---|---|
| P1 | modified | Target 14 pages (orchestrator), not 10-12; both builds are 13 pages incl. references and appendix. |
| P2 | modified | `main_review.tex` + `\anonbuild` switch; review build prints "(anonymized for review)", no anonymous.4open.science link. |
| P3 | applied | Acknowledgment names Claude, Codex, Nemotron 3 Ultra, MiniMax M3.1 Flash and the router-picked models, with what each did. |
| P4 | modified | Cover photo and `CoverImage` dropped rather than re-credited. |
| P5 | modified | No affiliation exists in the repo, so `\thanks` keeps the e-mail only; running heads per build. |
| P6 | applied | `\appendix[Positions]`; `\section{Positions}` removed. |
| P7 | applied | Table I and Table V captions fixed (Table V now says "Ordinary Board"). |
| P8 | applied | "Kings: The Tr\'ebuchet and When It Is Exact". |
| P9 | applied | 08 display unnumbered with [C2] in the sentence; Dawson equation numbered (1) and cited twice. |
| P10 | modified | `\lab` set in small sans serif; no label sits beside a citation (checked by grep). |
| P11 | modified | PyTorch "Paszke and others"; Wu-Yu-Landry 2010 Stanford Math 191 paper (key kept); Drummond-Cole title prints the star. |
| P12 | applied | "Let us begin" (03); "To see why, look at Fig. 6(a)" (07). |
| P13 | applied | `\IEEEtriggeratref` set at integration: 2 in the named build, 5 in the review build (last page balanced). |
| P14 | applied | Figs. 12 and 13 (tablebase and KPK bars) deleted. |
| P15 | applied | Five-file positions set as an itemize; the Underfull \hbox is gone. |
| P16 | applied | pdftitle in both builds; pdfauthor named build only. |
| P17 | rejected | Packaging, not source: the arXiv tarball will include only files `\includegraphics` uses. |
| P18 | modified | "game solving" replaced by "game theory"; "nimbers" kept (author keyword). |
| P19 | modified | Settled by the label policy: sketched proofs carry [AI] (checked by AI models, human check pending), not [P]. |

## Flow and voice (V1-V33)

| Id | Status | Reason / where |
|---|---|---|
| V1 | applied | Cuts made per the plan's budgets; 13 pages. 04 (1071 words vs 950) and 05 (1064 vs 900) stay over budget, since the page target is met (see group C report). |
| V2 | modified | One-sentence bullets with section pointers; roadmap cut to one sentence. Kings bullet drops 159/500 (stays in IV-E). |
| V3 | applied | Conclusion item 5 now asks whether the misere quotient is infinite. |
| V4 | modified | Table VII (cross-checks) deleted; 13 makes no "every row agrees" claim; the KPK difference stays in X-A. |
| V5 | applied | 09 conclusion rests on the e.p.-aware tree ("this *2 came from the textbook test"). |
| V6 | applied | Up-second-star / Tiny 1 sentence moved into IX-B; conclusion item 1 points to it. |
| V7 | applied | AI disclosure only in the Acknowledgment; 13 keeps one pointer sentence. |
| V8 | applied | Nine settings and default setting defined in II-C (`sec:ep`); Theorem 12 shortened; "So this 1/8" sentence deleted. |
| V9 | modified | IX-B is prose, with the corrected counts of F6 and the one open side of O7. |
| V10 | modified | "Across the census of Section VI ... 21,441 of the 231,071 values, 4,068 in outcome"; scope stated in VI. |
| V11 | modified | Birthday defined in II-E; 08 points there. |
| V12 | applied | Stops defined in II-E; removed from IX. |
| V13 | applied | Principle 2 refers to II-E for temperature. |
| V14 | applied | II-D shortened to one sentence pointing to V-C. |
| V15 | applied | X: "Pieces move as in Section II and wrap round each glued edge." |
| V16 | applied | VIII opens with the pointer to Section I. |
| V17 | modified | "In the model, then, ... four files and seven pawns beside T suffice". |
| V18 | modified | Merged into VI-C; last sentence limited to "with at most four pawns" (the scope of the cross-setting comparison). |
| V19 | applied | C4 ring sentence in VI-C. |
| V20 | modified | XIII-A deleted; the independence clause is in the label sentence of Section I. |
| V21 | applied | XIII-C deleted. |
| V22 | applied | "repair this model"; "star two appears with seven"; "earlier analysis of Dawson's chess". |
| V23 | applied | Separate paragraph on the three ways the cylinder differs. |
| V24 | applied | No "Let's", "you must", "interesting part" or "important caveat" remain (grep). |
| V25 | applied | No paragraph opens with "So" (grep). |
| V26 | applied | 04 opening on king moves / stalemate; IV-A merged. |
| V27 | applied | Group T defined in IV-A; "beside T" and "in the default setting" used elsewhere. |
| V28 | applied | "Tiny 1" in prose and headings, `\tinyg{1}` in formulas. |
| V29 | modified | G-T sentence deleted from 07 text; table note gives [C2] to the textbook column and [C1] to the e.p.-aware column (RESULTS.md: computed once). |
| V30 | applied | VII-A walk-through reworded. |
| V31 | applied | "cannot force mate on the cylinder"; "Both dimensions"; "White Wins"; line-120 sentence deleted. |
| V32 | applied | Omitted positions named in the Table VI caption; "the kind of certification that Section IX begins for 1/8". |
| V33 | applied | Files and ranks stated explicitly (IV-E, Prop. 10). |

## Facts (F1-F15)

| Id | Status | Reason / where |
|---|---|---|
| F1 | applied | Certificate implication is [Conj] ("proof incomplete"); Prop. 4 restated to the counter-promotion part [P]. |
| F2 | modified | Label policy ([AI]) replaces the "8 of 9" sentence; the Acknowledgment names who checked proofs. |
| F3 | applied | Intro real-chess bullet qualified ("with the new test"). |
| F4 | applied | "conditional on the king freeze and on a rerun with underpromotions"; abstract and intro say queen-promotion search, one side of one end position. |
| F5 | modified | Sweep labelled "Under the textbook test"; under the e.p.-aware test the 18 e.p. failures go but the free kings still change most of them, 143 to 138. |
| F6 | modified | 302 sides = 290 one-sided (283 agree, 5 disagree, 2 draws) + 12 race (bounds_after_le7.json); "306" dropped (no file). |
| F7 | applied | 1/8 end-position results are [C1]. |
| F8 | modified | Puzzle 1: "does best to take on a5 at once, since every other move lets white force a passed pawn (after h6-h5, for example, a4xh5)"; cylcgt shows h6xa5 also loses. |
| F9 | applied | Count-rule qualifier kept in II-C; Fig. 1 caption gives value 0. |
| F10 | modified | Both independent checks were on the mirror image; the text says so. |
| F11 | modified | Tiny 1 in VII-B: textbook test [C2], e.p.-aware test [C1]. Integration: intro bullet now gives Tiny 1 [C1] (default setting), 1/8 and up-second star [C2]. |
| F12 | applied | Minimax confirms the textbook winners of all 12,568 rings and 4,000 random ordinary components. |
| F13 | applied | Census scope stated once in VI; "in the default setting" on the minimality sentence (08, intro). |
| F14 | applied | "!" after 2. Kh7 dropped. |
| F15 | modified | Drummond-Cole "with the help of pieces other than kings and pawns" (notes/lit_cgt_chess.md); Wu-Yu-Landry 2010; Elkies 2002 pp. 61-78 kept; CoverImage dropped. |

## Orchestrator fixes (ORCH_FIXES.md, O1-O9)

| Id | Status | Check |
|---|---|---|
| O1 | applied | 08: A's a7-a6 ({2\|0}) and b7-b5 (replies 2 and 3) and B's d2-d3 and c2-c4 (replies -2, -3) are "reversible"; a6-a5 "counts as a move to *"; candidate's a2-a4, d7-d5 "dominated or reversible". |
| O2 | applied | 12: Lc0 perfect at 10^3 to 10^6 nodes; all 17 draws from 10^3 nodes on. |
| O3 | applied | 04: validity (T1.14(i)+(ii)) and loopy (T3.4) theorems are [AI]; sum safety (L2.1) [AI]; no "PROVED after repair" item is labelled [P]. |
| O4 | applied | 08: the three five-file witnesses are [C2] in the default setting (no change needed). |
| O5 | applied | 01: Drummond-Cole needs pieces other than kings and pawns. |
| O6 | applied | 08: completeness of the seven/eight counts is [C1]; conclusion item 2 says it "rests on one program [C1]". |
| O7 | applied | 09 Prop. 18: 0 <= O <= 1/8, one open side (black to move in W b2 b5 / B a5 b4); abstract, intro and conclusion match. |
| O8 | applied | 09 names only W a3 b3 c2 e2 / B a6 c5 d5 e3 as the 12-man witness beside T; 08 makes no claim that every five-file witness embeds. |
| O9 | applied | 04: the 1,418,480-position check "validates the solver; its results below are [C1]"; the GAP items (sharp T1.14, T2.7, P11, P12) are not cited as proved; the Acknowledgment names the systems that re-derived proofs and recomputed the king numbers. |

## Integration changes (this pass)

- `sections/appendix_table.tex` (new): the Appendix table* moved out of `appendix_positions.tex` and input
  before Section XIII, so it prints at the top of page 12 instead of splitting the reference list.
- The puzzles figure* (Fig. 4) source moved from 05 to the end of IV-C, so it prints on page 5 with the
  puzzle text instead of page 6.
- Compact table of contents (`\compacttoc` in main.tex, named build only): from a full column to about half.
- `\IEEEtriggeratref` (P13): 2 (named build) and 5 (review build).
- Certificate horizon renamed from $T$ to $h$ in 04 and 14, so it no longer clashes with the king group T.
- Conclusion item 3: the counter-promotion result holds "in every context without a passed pawn", and
  Conjecture 5 is stated as an unpunished move inside the king group (group C note).
- 09: "only under one non-default race rule" (was "setting"; W a3 b3 c2 / B b5 b7 c6 is *2 under the
  opponent rule with both e.p. tests, i.e. two of the nine settings; group G note).
- 01: Tiny 1 now carries [C1] in the default setting (the recorded independent check covers the textbook
  test only; group D note).
- Grundy figure legend: "flat 3 x n board" -> "ordinary 3 x n board" (make_figures.py line 190; figure
  regenerated, `--check` passes).
- Conclusion trimmed to 350 words, intro to 580.

## Still open

- 04_kings (1071 words) and 05_sums (1064) remain over their word budgets; the 14-page limit is met, so
  nothing further was cut.
- Stockfish on sums: the paper says 26.5-28.0% (sf_stdout.txt: 53/200 at 10^4 nodes), but RESULTS.md,
  delegate/REVIEW.md (T13) and the SPEC fact sheet still say 27.5-28.0%; those files are outside paper/ieee.
- The board figures embed chess glyphs from AppleSymbols without a ToUnicode map (text extraction only;
  all fonts are embedded).
- The proofs labelled [AI] still need a human check before submission.

## Round 1 checks (2026-10-21, after the network drop)

The check findings came from three reviewers: facts (R1-R15), referee (R16-R48) and layout (R49-R63). They
are numbered here in the order they were given. I read the current files first: 00-02 already had the
corrected 18,137 / 4,070 census numbers, and nothing else from this round.

Builds (`tectonic -X compile --keep-intermediates --keep-logs`): `main.tex` and `main_review.tex` both compile
with no errors, no undefined references and no Overfull boxes. Both are **13 pages** (limit 14). The only
TeX warning left is one Underfull \hbox (badness 5475) in the head of Theorem 18 (09_real, first line). The
Underfull \vbox on page 12 (badness 4913) and the one on page 1 (badness 10000) are both gone. `main.bbl` and
`main_review.bbl` were regenerated, with 16 \bibitem entries each. A zlib scan of every stream in
`main_review.pdf` finds no "Bhattach", "aritro", "Morley" or GitHub link, and neither PDF contains TODO or
VERIFY. All board figures were regenerated with `make_figures.py`, and `--check` passes. I looked at every page
of both builds.

| Id | Finding | Status | Reason / where |
|---|---|---|---|
| R1 | Census changes 18,137 / 4,070 | applied | Already in 02 (II-C). RESULTS.md section 1 already has the corrected numbers; it is outside paper/ieee anyway. |
| R2 | Split Theorem 3 (validity) | applied | Theorem 3 is (V1)-(V3) [AI]. The (V4) sentence is now Conjecture 4 [Conj], followed by "Its proof in the repository ... has a known gap". Intro bullet as proposed. |
| R3 | Condition (E) holds only in the pure game | applied | Prop. 11 opens "In the pure pawn game, without the passed-pawn rule ..." (notes/lemmas.md L1.7). The sentence before it now separates HSS (Prop. 10) from (E) (Prop. 11). |
| R4 | Dawson probes no better than majority | applied | Proposed sentence. I recomputed it: 8 of the 50 lengths 31-80 have g=0 (0.84), 1-30 give 0.80, and the majority Grundy class is 12/50 = 0.24 (ml/dawson/REPORT.md). |
| R5 | Prop. 5 rank hypothesis; certificate wording | modified | "At least **six** ranks", not five. On five ranks a pawn that has just double-stepped stands on its last rank but one and can still be taken e.p. On six or more ranks it can only have got there by a single step or a capture, which the proof now says. Stalemate is separated from the counter-promotion condition. |
| R6 | Sweep scope; "most of them" | applied | "at most two pawns a side on one file (on two files, d and e, on the seven-file cylinder)" (kings/REPORT.md section 4). The inference was replaced by "these 18 are no longer convention failures, yet ... fall only from 143 to 138". |
| R7 | Open problem 1 caveat | applied | Proposed wording, including "(with the kings frozen inside the tree)". |
| R8 | "one non-default setting" | applied (merged with R39) | Candidate 6 is mover rule with e.p. off (realchess/certify/REPORT.md). VIII-B now says "In non-default settings a few other census positions are *2". |
| R9 | Mirror reachability reasoning | applied | "could only have come from a2 or b2, and both are still on their starting squares". |
| R10 | Legality of up-second-star / Tiny 1 | applied | VII-B gives the history c2xb3, b3-b4-b5-b6, a7-a6, c7-c5 (c7-c6 for Tiny 1), checked by hand. Fig. 6 caption: "a 10-man position with a legal pawn history". Intro: "occur in 10-man positions that can arise in a game". |
| R11 | A and B "embed legally" | applied | "both fit beside T, with the capture histories c2xd3 (A) and b7xa6 (B)". The histories were checked by hand; no repo file records more than the geometry. |
| R12 | Engines on sums: 45 positions with no winning move | applied | "(45 of the 200 ... excluding them, 34-36% and 42-43%)" (engine/runs/chesssums/REPORT.md: 34.2-36.1, 41.9-43.2). |
| R13 | Queen sentence vs torus | applied (with R20) | See R20. |
| R14 | C4 ring wording | applied | "... a value that also occurs on the ordinary board, so under that test it is no longer cylinder-only". |
| R15 | Abstract census scope | applied | "... on boards up to four files wide". |
| R16 | Define "frozen" | applied | Defined in II-B (third bullet, as proposed). IV-D and V-B now say "a zugzwang for black only", IX-B says "the frozen kings (Section IV)", and the abstract says "the kings are frozen in a mutual zugzwang ... the frozen kings give the exact chess result". |
| R17 | ChessSums training sentence | applied | First option: "We built ChessSums, a set of 26,000 ..."; the training sentence is deleted. No ML baseline was added. |
| R18 | IX-B rewrite | modified | Proposed structure. "Seven agree" was checked: it covers the 8 sides of the four eight-man end positions other than W b2 b5 / B a5 b4 (min_support.json, resolve_needed.log, RESULTS.md 6b). The text adds that the re-search then brought in one more eight-man position (W a2 b4 b5 / B a5, min_support_after.json), whose two sides agree (kp_eighth_8man.out). Without that, the reader could not follow the final decisive set (min_support_after2.json). |
| R19 | "treatment" | applied | II-C: "three e.p. options". Table III: "opponent, any e.p. option". Def. 16: "... one fixed game t ...; the choice of t is the draw treatment". Lemma 17, Thm. 18(b) and IX-A: "draw treatment". |
| R20 | Tablebase queen sentence | applied | Proposed wording. |
| R21 | Fig. 5 caption | applied | Proposed wording. |
| R22 | Define nimbers before use | applied | Intro and II-E, as proposed. |
| R23 | Model bullet | applied | Proposed wording. |
| R24 | Wu-Yu-Landry sentence | applied | Moved to the end of the 2025-study paragraph. |
| R25 | "default setting" / census before definition | applied | Both as proposed. In II-C the numbers are the corrected 18,137 / 4,070, not the 21,441 / 4,068 of the finding. |
| R26 | III first paragraph | applied | Proposed wording. |
| R27 | "holds more" | applied | "A single file can do more. In W a2 / B a6, ...". |
| R28 | Stalemate sentence | applied | Deleted after the proof sketch; IV's opening extended as proposed. |
| R29 | "plausible" | applied | "We conjecture that a certificate implies (V3); our proof of this is incomplete [Conj]". |
| R30 | 143 never introduced; 8x8 wording | applied (merged with R6) | "143 of the 159 lie on the seven-file cylinder", then the facts wording for the 18, then the ordinary 8x8 sentences as proposed. |
| R31 | on/off/dud | applied | "on = {on \| } if only white can wait, off = -on if only black can, and dud if both can". |
| R32 | Principle 2 | applied | Proposed wording. |
| R33 | Five-file witness link | applied | Both cross-references added (V-C to VIII-D, and VIII-D to V-C). |
| R34 | +-3/4; "only on en passant" | applied | Proposed wording. |
| R35 | VII-A passive | applied | Proposed wording. |
| R36 | VIII-A telegraphic | applied | Proposed wording. |
| R37 | "placements" | applied | "793,299 labeled placements on widths 1-4 (every placement on each width, without reduction by symmetry or translation)" (verify_ext/codex/REPORT.md). |
| R38 | VIII-D repetition | applied | Proposed shortened text. |
| R39 | Move IX-A census sentence | modified | Moved to VIII-B as "In non-default settings ..." (not "Under the opponent rule", per R8). IX-A keeps the W a3 b3 c2 / B b5 b7 c6 sentence. |
| R40 | IX-C padding | applied | Heading dropped; the text ends IX-B ("... is so far a model value"). |
| R41 | Cylinder coverage | modified | "C3 to C5" (not C2; the atlas starts at C3). Rings: research/star2_frontier scope (d) scans C5-C8 rings with at most 8 pawns, and at count/aware its only *2 hits are the 14 eight-pawn C5 rings (scope_d_c5..c8_candidates.txt). C3/C4 rings were scanned only under the textbook test (atlas), so the text says so and open problem 2 asks about them. |
| R42 | "8 x 8"; Table VI "other" | applied | "the ordinary 8x8 board" twice. A table note defines "infinitesimal" and "other" from engine/suite/build_suite.py value_class: "values free of B that fall in none of the other classes, such as tinies and games {a+-x \| b+-y}". |
| R43 | "too easy" | applied | Proposed wording. |
| R44 | "cached"; Acknowledgment | applied | Deleted; Acknowledgment as proposed. |
| R45 | Open problem 3 | applied | Proposed wording; it refers to Section IV-B (new label). |
| R46 | Abstract wording | applied | "the one-eighth then depends only on one end position with black to move, which our queen-promotion search leaves open". I avoided "confirmed except for", which would overstate Prop. 19 (0 <= O <= 1/8). |
| R47 | Fig. 4 caption | applied | Proposed wording. |
| R48 | Delete TOC | applied | The \compacttoc definition and the TOC are removed. Final intro sentence: "Section IX tests ..., Sections X-XII ..., Section XIII ..., Section XIV ..., and the Appendix ...". Without the TOC, page 1's right column was left with a 2-line stretched gap (Underfull \vbox 10000), so two intro bullets gained a short clause each: torus mate (Table IV) and engines on sums (XII-D). In the review build only, `\enlargethispage{-2\baselineskip}` is applied on page 1, because that build has no author footnote. |
| R49 | Bib key leaks the surname | applied | Key renamed to Study2025 in refs.bib, 04, 05 and 11. The review PDF has 0 "Bhattach" in any decompressed stream (link names are now cite.Study2025). |
| R50 | Anonymous code mirror | rejected (author action) | An anonymous.4open.science mirror has to be created by the author. I may not contact services. When it exists, set \codeurl in the \anonbuild branch of main.tex. |
| R51 | Acknowledgment names "the author's" study | applied | The review build says "from the 2025 study [9]". New macro \studytitle: in the review build [9] reads "Anonymous, 'Title withheld for review', 2025, unpublished manuscript". |
| R52 | Stale main.bbl | applied | Regenerated with --keep-intermediates: 16 entries; Wu-Yu-Landry entry correct; no CoverImage. |
| R53 | Affiliation in \thanks | rejected | No affiliation, city or country is recorded in the repo, and inventing one would be a placeholder. The author should supply it. |
| R54 | URLs break after "https:" | modified | xurl was tried, but it breaks inside "https". Instead, main.tex resets the url package's break classes: ":" can no longer take a break, and breaks fall after "/" or ".". Both URLs now start "https://" on one line. |
| R55 | Faint, tiny board labels | applied | Small-board labels are now 9 pt black!70 (6.5-8 pt at printed size); column boards use black!70 as well. Dawson boards are set at scale 0.8 (about 7 pt), so labels are about the same size everywhere. |
| R56 | Fig. 3 subcaptions | applied | \mbox{B~Kb4~a5} etc.; the lines now break after "/". |
| R57 | Fig. 9(b) seam arrow | applied | The arrow is replaced by thick dashed red lines on the two glued edges. Caption: "files a and f are adjacent, and the two dashed edges are glued". |
| R58 | Stretched vertical glue | applied | Fixed by the new page breaks (see R48). No Underfull \vbox remains in either build; the gaps that remain are normal subsection spacing. |
| R59 | Label-only theorem heads | applied | `\ieeethmnote` in main.tex: a head whose note starts with \lab prints "Proposition 5 [P]:", and named heads keep "(Cut lemma; [P], [C2])". |
| R60 | References [1], [13] | applied | [1]: address "Harpenden, U.K." (John Beasley's own imprint; from memory, not checked against the title page). [13]: "no. 4", checked on Crossref (DOI 10.1016/j.jcta.2007.07.008: vol. 115, no. 4, pp. 593-622, 2008). |
| R61 | Index terms | applied | "game theory" changed to "game solving", which reverses the P18 change, as GUIDELINES B suggests. |
| R62 | Last-page balance | applied | \IEEEtriggeratref{10} in both builds; both last pages are now balanced ([2]-[9] / [10]-[16]). The comment was corrected. |
| R63 | IEEE preprint notice | rejected (not yet applicable) | The paper is not submitted. GUIDELINES F says to ask the EiC before posting, and to add the notice only to a preprint posted after submission. This is the author's call at that point. |

Still open after this round: R50, R53 and R63 need the author. The [AI] proofs still need a human check.
RESULTS.md and delegate/REVIEW.md, which are outside paper/ieee, still give Stockfish on sums as 27.5-28.0%.
The paper uses 26.5-28.0% (sf_stdout.txt).

## Round 2 checks

Builds (`tectonic -X compile --keep-intermediates --keep-logs`): `main.tex` and `main_review.tex` both compile
with no errors, no undefined references or citations, and no Overfull or Underfull boxes (the Theorem 18 head
warning is gone). Both builds are **13 pages** (limit 14). `main.bbl` and `main_review.bbl` were regenerated (16
entries each). A zlib scan of every stream in `main_review.pdf` finds no "Bhattach", "aritro", "Morley", GitHub
link, "cylcgt" or "kpsolve", and neither PDF contains TODO or VERIFY. The abstract is 188 words. The puzzle
boards were regenerated at the "small" size (`make_figures.py`), and `--check` passes. I looked at every page of
the named build and at the pages of the review build that differ from it (1, 2, 12, 13). Pages 3-13 break at
the same places in both builds.

Facts checked against the repository for this round:
- 138 on the seven-file cylinder (kings/results/exp_cyl7x6_epon_Q_conv.jsonl): the e.p.-aware test creates
  **no** new mismatches. It turns 5 mismatches into matches. Of the 18 e.p. failures, 5 now match, and in the
  other 13 the free kings change the result again (real differs from frozen). The referee's "creates new
  mismatches" reading is wrong, and the text says this instead.
- The 1/8 decisive set (realchess/targets18/min_support*.json): the first search finds 5 eight-man and 3
  nine-man positions. Four of the eight-man positions resolved (7 of 8 sides agree; black to move in
  W a3 a5 / B b4 b5 disagrees). The second search adds W a2 b4 b5 / B a5, which agrees on both sides. The last
  eight-man position is W b2 b5 / B a5 b4. So the "4 + 1 + 1" grouping holds, but the first search found
  five eight-man positions, not six; the text says so.
- e.p.-aware atlas: atlas/cylinder/ep_aware/REPORT.md item 4, accepted in delegate/REVIEW.md T4.
- 1.a4: RESULTS.md section 1 (1.a3 and 1.c3 lose, 1.a4 unresolved).
- Queen-only sweeps and 42 of 42: kings/REPORT.md (sections 3 and 4).
- Dawson training range: ml/dawson/REPORT.md (train totals 1-30).
- 4,887: RESULTS.md (ChessSums data line).
- Display cap behind "at least 18,137": atlas/flat8/rerun/REPORT.md.
- Lemma 1.7 qualifier: notes/lemmas.md.
- Status of P2.10(a) and T1.14(ii): kings/theory/LOOPY.md.

| Id | Finding | Status | Reason / where |
|---|---|---|---|
| C1 | Prop. horizon h=1 is [P], but it is a repaired AI result | applied | Now Proposition 6 [AI]. The intro's [AI] definition now reads "proof given or sketched here (in full in the repository), checked by AI models, human check pending", so it also covers a proof given in full in the paper. The optional note on four ranks was not added: the paper's statement (six ranks) is stricter than LOOPY's H >= 5. |
| C2 | C3/C4 rings "not scanned" under the e.p.-aware test | applied | 08: "Rings on C3 and C4 have been scanned under the e.p.-aware test only up to five pawns (the atlas), with no *k, k >= 2 [C1]". Open problem 3 asks about C3/C4 rings with six to eight pawns. |
| C3 | Stated reason that (V4) stays a conjecture | applied | Proposed wording. |
| C4 | Reversible moves are bypassed, not dropped | applied (merged with R15) | See R15. |
| C5 | Queen-only sweeps not stated | applied | The sweep paragraph has "(queen promotions only, at most two; on the six-file cylinder the all-promotion results agree in 42 of 42 cases)". The opening now says the solver supports "any of the four promotions". |
| C6 | [C2] rule omits a second program | applied | "... unless a second program or the Lichess tablebase confirms them". |
| C7 | Winning first moves not fully resolved | applied | "... on every winning first move resolved so far (1. a4 is still open)". |
| C8 | Abstract and intro overstate the 1/8 status | applied | Abstract: "with frozen kings and queen promotions only, the one-eighth hinges on one open end position". Intro bullet: "with queen promotions only and frozen kings, the 1/8 hinges on one side of one end position". |
| C9 | Five-file *2 has no e-file buffer | applied | 09: "the one of the three that sits legally beside T, has 12, with only file f free of pawns between them". |
| C10 | Prop. condE needs the side-to-move qualifier | applied | Added after the proposition: "The two differ with white to move, the case that arises inside larger sums; with black to move, as in the chess position, both say black wins." |
| R1 | Abstract "boards up to four files wide" | applied | Now "ordinary boards up to four files wide". |
| R2 | "Four-man tablebases" | applied | "Tablebases of up to four men". |
| R3 | "Puzzle 2" used before it is introduced | applied | IV-D deleted. Its text is in V-B after the Principle 2 sentence, with the proposed sentences, keeping "(our solver and the Lichess tablebase)" for the [C2]. Fig. 3(c) caption: "a king group from the 2025 study (cylinder; Section V), a draw with white to move". |
| R4 | Roadmap incomplete | applied | Proposed paragraph. The review-only `\enlargethispage` is gone, and page 1 of both builds is full with no stretched gap. |
| R5 | Atlas *2 needs a comment | applied | Proposed wording. |
| R6 | 1/8 paragraph reads like a run log | modified | Restructured as proposed, but checked against min_support*.json (see above). The first search finds five eight-man and three nine-man positions, and the second search adds the sixth eight-man position, so the text says that rather than "six eight-man". "The remaining sides have eight or nine men" became "The remaining end positions have more men", because the files do not bound the men at nine. The repeated definition of "side" and "These results are [C1];" are deleted. |
| R7 | Sweep paragraph hard to parse | modified | Proposed structure. The last sentence was corrected from the data: the e.p.-aware test fixes all 18 e.p. failures as convention failures, but in 13 the free kings change the result again, so the count falls only from 143 to 138. |
| R8 | "Five-file witness" undefined | applied | 08 names it after the list: "We call the first the five-file *2 (Section V-C)". It is not named inside the list item, where the long \pos broke the line (Underfull box). 05: "the first five-file *2 of Section VIII-D". 09 and Table VI as proposed. |
| R9 | "One census position ... non-default setting" | applied | Proposed wording. "Opponent rule with en passant on" was checked in realchess/certify/REPORT.md (candidate 2: opponent gives *2 under both tests). |
| R10 | "Elkies' Targets" | applied | Table II caption "Elkies' Small Values in the Census", header "Value", Table VI group "Elkies' small values". |
| R11 | "the old test" | applied | Proposed wording. |
| R12 | Conclusion omits Dawson and engines | applied | Proposed sentence. |
| R13 | Open problem 2 mixes two questions | applied | Split into items 2 and 3, with C2's "six to eight pawns" in item 3. "Seven problems are open." |
| R14 | "did not converge" | applied | Both proposed wordings (11 and 14). |
| R15 | Reversibility sentence | applied (merged with C4) | "A move that the opponent can answer with a passed pawn is a losing move, and it drops out, since having only losing moves is the same as having no moves at all [10]. A move that the opponent can answer by reaching a position at least as good for him as the one we started from is reversible: in the canonical form [3] it is replaced by the player's moves from that reply, and so drops out when there are none." |
| R16 | Nimbers defined twice | applied | Proposed. |
| R17 | Notation placed last | applied | Notation is now II-B, and its last sentence introduces the infinitesimals as proposed. |
| R18 | Double-up star used before definition | applied | Proposed. |
| R19 | Fig. 5 caption repeats the text | applied | Proposed caption. The numbers stay in VI-B. |
| R20 | Dangling sentence ending VII | applied | Proposed. |
| R21 | Unnumbered conjecture | applied | Now Conjecture 5 (conj:cert), followed by "Our proof of this has a gap." Open problem 4 cites it. |
| R22 | "small positions" vague | applied | Proposed. |
| R23 | Position A parenthesis | applied | Proposed. |
| R24 | "textbook tree" used undefined; compressed reasoning | modified | The definition sentence is added before Theorem 19. The replacement sentence is not used as proposed: realchess/REPORT.md says the textbook tree rules out *2 when draws count as wins for **either** side, not only under (c). Text: "In the textbook tree *2 is ruled out only when draws count as wins for one side, as in (c), so the candidate's *2 depends on the textbook test." |
| R25 | "every disagreeing case tested" | applied | Proposed. |
| R26 | Double negative | applied | Proposed. |
| R27 | "trained on shorter positions" | applied | "trained on total lengths up to 30" (ml/dawson/REPORT.md). |
| R28 | Scope of the C2 label on ChessSums | applied | Proposed. |
| R29 | "Seven Decided Positions" | modified | Caption: "... Seven Positions Already Decided (Value +B or -B) Are Omitted". engine/suite/build_suite.py's "decided" class is a value containing B that is not a switch, which is not always a passed pawn on the board, so "by a passed pawn" was not used. |
| R30 | Dawson "should open" | applied | Proposed. |
| R31 | Why only a lower bound on 18,137 | applied | Proposed parenthesis. |
| R32 | Acknowledgment "at no cost" | applied | Proposed. |
| R33 | Why the mirror was checked | applied | Proposed. |
| L1 | Broken anonymized code sentence | partly applied | New macro \codeavail. Review build: "The code and data are available in an anonymized repository supplied to the editor." The anonymous.4open.science mirror needs the author's account, so the author has to create it. Then set \codeavail in the \anonbuild branch of main.tex to point to it. |
| L2 | IEEE preprint notice | applied as a switch, off | main.tex has `\newif\ifsubmitted` with `\submittedfalse`. `\submittedtrue` adds the exact notice as the first \thanks of the named build; a test build confirmed it prints. It stays off because the paper has not been submitted, and the notice would be false now. GUIDELINES F: the author confirms with the EiC first. |
| L3 | References split around Table VII (review build) | applied (differently) | Fixed by L6. The table now prints on page 12, and the whole reference list sits in the right column of page 13 in both builds. \IEEEtriggeratref{10} would now push [10]-[16] onto a 14th page, so it was removed. With nothing left to move into the right column, the last page cannot be balanced. A `\raggedbottom` before the Appendix keeps the short left column of the review build from being stretched. |
| L4 | Stretched Theorem 18 head | applied | `[Candidate in real chess; [C1]]`, with [C2] at the end of (a), the root-move table checked two ways (realchess C6). The box warning is gone. |
| L5 | Affiliation, city and country | rejected (author action) | Not recorded anywhere in the repository; inventing them would be a placeholder. The author must supply them. |
| L6 | Table VII after the Acknowledgment | applied | `\input{sections/appendix_table}` moved before Section XII. The table is now Table VI, at the top of page 12, before the Appendix text; the Stockfish table is Table VII. Still 13 pages. |
| L7 | Inconsistent board scales | applied | Fig. 4 is now a single-column figure with three boards at 0.32\columnwidth, the same as Figs. 3, 6 and 7. The boards were regenerated at the "small" size, so the labels print at about 6 pt. Details moved from the subcaptions into the caption. Fig. 8 is now 0.32\columnwidth. |
| L8 | Bib entries [10], [16] | applied | [10] is a @techreport (Stanford Univ., Stanford, CA, USA, Math 191 paper), and the key was renamed WuYuLandry2010 in 01 and 03. [16]: "Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)", vol. 32. |
| L9 | Abstract at the 200-word cap | applied | 188 words: "with at most six pawns", "We repair", "the frozen kings are exact", "earlier work on". The four-man wording is fixed as in R2. |
| L10 | Tool names in the review build | applied | Section XIII names no tools in either build ("Our CGT engine", "the king-and-pawn solver"). |

Still open after this round: L1 (anonymous mirror), L2 (turn the notice on after submission) and L5
(affiliation) need the author. The [AI] proofs, now including Proposition 6, still need a human check.

## Orchestrator final pass (2026-10-21, 23:55)

- **Table of contents restored** in the named build (sections only, footnotesize, about a third of a column). The
  author asked for one. The review build has none.
- **Census numbers:** "at least 18,137 of the 231,071 values, 4,070 in outcome" (atlas/flat8/rerun/REPORT.md).
  The old 21,441 / 4,068 came from a raw-string comparison.
- **New result in VIII-D, intro, abstract and open problem 3:** the first ring \*2 on Cn has n+3 pawns for
  n = 3, 4, 5.
  - C3: `W a2 a3 b2 / B b7 c6 c7` (6 pawns).
  - C4: `W a4 b2 c2 / B b6 c5 d6 d7` and its color-reversed twin (7 pawns).
  - Values: cylcgt and the C scanner (`research/star3_hunt`, `research/star3_hunt_extra`) agree, so [C2].
  - Minimality: the atlas covers up to 5 pawns, and the C scan covers every 6- and 7-pawn split. That is
    [C1].
- Both builds: 13 pages, no errors, no overfull boxes, no undefined references.

## Orchestrator, 2026-10-22 01:00

- **VIII-D:** 21 five-file \*2 positions as whole-board games (C scanner, whole-board solver, and cylcgt with
  splitting off), 15 of them as sums. Replaces "three".
- **X-A:** new "Other widths" paragraph and Table VI, KPK on Cn for n = 3–10.
  - Drafted by T31 from T25's verified data.
  - Numbers checked by the orchestrator against `research/odd_cylinders_verify/summary.txt`.
  - "Odd-width cylinders" removed from open problem 5.
- **Layout:** both builds are now 14 pages (the review build's limit). `\IEEEtriggeratref{11}` balances the
  reference columns on page 14.
