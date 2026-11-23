# ScholarOne fields (paste-ready)

Everything below is copied from the paper sources in `dist/tog/`. Items marked "not verified" are not in the ToG audit (`delegate/out/ieee_audit/AUDIT.md`).

## Title

Chess Endgames on a Cylindrical Chessboard: Exact Combinatorial Game Values, Real-Chess Checks, and Tablebases

## Abstract (plain text, 199 words)

Word count: 199, computed with a script on `dist/tog/sections/00_abstract.tex` (LaTeX removed, hyphenated words such as "a-file" and "tablebase-backed" counted as one word). ToG asks for 150-200 words (AUDIT.md), so there are 3 words of headroom. The review PDF carries the same text.

Cylinder chess joins the a-file to the h-file, leaving no side edges or corners. We study king-and-pawn endgames with combinatorial game theory after Elkies: a passed pawn wins, and the kings are frozen in a mutual zugzwang worth zero. We make the passed-pawn test respect en passant, and state when frozen kings give the chess result. Under this test and the count rule, no position of at most six pawns on an ordinary board of any width has a nimber above star; with seven, star two appears once, plus its color-reversed twin, confirmed by three programs; its real-chess value is open. In pawn-only whole-board rings, star two needs six pawns on three files and, from ten files on, one per file (proof sketched); on seven files ten-pawn rings reach star three. We find positions with a legal pawn history worth one-eighth, up-second star and Tiny 1; with frozen kings and queen promotions only, the one-eighth position's tablebase-backed oracle value is one-eighth. On the cylinder king and rook rarely force mate, but opposite-colored bishops can. We correct earlier work on cylinder Dawson's chess: the ring is a first-player win exactly when the strip three files shorter has Grundy value zero.

## Index terms (keywords)

Chess, combinatorial game theory, endgame tablebases, game solving, nimbers

(5 terms; ToG allows 2 to 5. Whether the IEEE Thesaurus accepts them: not verified. Swapping "game solving" for "Game theory" is an option noted in the audit.)

## Manuscript type

Full paper (regular paper). The exact name of the option in ScholarOne: not verified.

## Counts (review PDF `tog_review.pdf`)

| Item | Count | Source |
|---|---|---|
| Pages | 10, including references (limit 10) | `pdfinfo`, US Letter |
| Figures | 7 (Fig. 1 to Fig. 7, several with sub-panels) | caption lines in `pdftotext` of the review PDF; `\begin{figure}` blocks in `sections/*.tex` |
| Tables | 5 (Table I to Table V) | same |
| References | 20 | `build/tog_review.bbl` has 20 `\bibitem`; the PDF list ends at [20] |
| Supplement pages | 99 (not counted toward the limit, per AUDIT.md) | `pdfinfo supplement_review.pdf` |

## AI-use statement (plain text)

This is the paper's own statement, from its Acknowledgment (named version, which says "the author"; the review version says "the authors"). Copy the review version into ScholarOne if a separate field asks for it.

Named version: AI coding assistants (Claude, Anthropic; Codex, OpenAI; and open models run through the OpenCode and Kilo tools) wrote and ran, under the author's direction, the software for the simulations, endgame searches, tablebases and cross-checks of Sections II-XIII and the scripts that draw the figures, wrote the full proofs of Sections S12-S15, and helped draft and edit the text of all sections. The author chose the research questions, directed the work and is responsible for all content.

Review version: AI coding assistants (Claude, Anthropic; Codex, OpenAI; and open models run through the OpenCode and Kilo tools) wrote and ran, under the authors' direction, the software for the simulations, endgame searches, tablebases and cross-checks of Sections II-XIII and the scripts that draw the figures, wrote the full proofs of Sections S12-S15, and helped draft and edit the text of all sections. The authors chose the research questions, directed the work and are responsible for all content.

Note: AUDIT.md section 3.6 says IEEE's AI policy asks for the system, the sections and the level of use, and judged an earlier wording incomplete. The current wording names the systems and sections. Whether it now meets the policy is Author must confirm. Also Author must confirm that the open models run through OpenCode and Kilo are named well enough (model names are not given).

## Data and code availability statement (plain text)

Review version (Section XIII of the review PDF, and the supplement): "The code and data are available at <anonymous link>." The supplementary material gives the full proofs of the [S] results (Sections S12-S15) and the FEN of every position with kings (Section S11).

Suggested ScholarOne text: The code and data for review are at https://anonymous.4open.science/r/<id> [Author must insert]. The engine is Python 3 (standard library only); the fast solvers are in C. The supplementary PDF holds the full proofs and the FEN of every position with kings.

After acceptance (named version): github.com/aritroBh/cylindrical-chess-cgt. Author must confirm that this repository is public and matches the submitted version at the time of the final upload (the audit found it private on 2026-11-22, in `paper/SUBMISSION.md`; its present state is not verified).

## Supplementary files

| File | One-line description |
|---|---|
| `supplement_review.pdf` | Anonymous supplement, 99 pages: material moved out of the 10-page paper (S1-S11), full proofs of the [S] results (S12-S15), and the square-rule passer test with a counterexample (S16). |

(Code and data are not uploaded as a file; they are reached through the anonymous link. A zip of sources for the "sources" slot: Author must confirm whether ScholarOne asks for it. Not verified.)

## Other fields that need author input

- Author name, affiliation, e-mail, ORCID: Author must confirm. Affiliation per the paper: University of Illinois Urbana-Champaign, Urbana, IL 61801 USA; e-mail given in the named paper. ORCID: not in the paper.
- Funding: the paper states none. Author must confirm that there is none.
- Prior or related submissions, conference or preprint versions: the paper says only that it extends an unpublished 2025 study. Author must confirm there is no preprint or conference version.
- Suggested or opposed reviewers: none suggested (as instructed).
