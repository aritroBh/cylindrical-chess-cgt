# IEEE Transactions on Games: pre-submission audit

Audited 2026-11-22, read-only. Sources: `paper/ieee/main.tex`, `main_review.tex`, `macros.tex`, `refs.bib`,
`sections/*.tex`, `figures/`. The PDFs were rebuilt from a copy in `delegate/out/ieee_audit/build/`
(`tectonic -X compile --only-cached`). The fresh builds have the same page counts as the shipped PDFs: named 15 pp,
review 14 pp, US Letter.

Web pages fetched (3 of the 6 allowed, all succeeded):
- ToG submission guidelines: https://www.transactions.games/submit/submission-guidelines
- IEEE AI-generated text policy: https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/
- IEEE Author Center, "Structure your article":
  https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/

Key venue facts (ToG page, quoted):
- Full papers: "limited to 10 pages in the journal's two column format", references and biographies included,
  supplementary material excluded.
- "Papers longer than 12 pages … will be considered only if" the cover letter justifies the length.
- Mandatory over-length charge: "$200 USD per page" (or a voluntary $110/page).
- Review is double-anonymous since 2025-01-01: "Author names, affiliations, biographies and even acknowledgments of
  funding must not appear". Code and data go through http://anonymous.4open.science/ during review.
- The abstract "must be between 150-200 words", self-contained, "without abbreviations, footnotes, or references".
  Keywords: 2–5.
- The relation to prior work must be "made explicitly clear to the reader within the manuscript text".
- ToG says nothing about AI use, ethics or conflict-of-interest statements. IEEE-wide AI policy: disclose in the
  Acknowledgment, identify the AI system, "specific sections", and "the level at which the AI system was used",
  for text, figures, images and code alike.

Legend: **PASS** / **FAIL** / **UNKNOWN** (could not be decided from the files). A "fix" is the exact change to make.

---

## 0. FAIL items ranked by risk of desk rejection or a returned manuscript

| # | Item | Why it matters | Fix (short) |
|---|------|----------------|-------------|
| 1 | Length: the review build is 14 full pages (§1.1) | Over 12 pages needs a written justification or the EiC may return the paper unreviewed; even at 11–12 pages the charge is mandatory ($800 at 14 pages) | Cut to 10 (see `PLAN_10_PAGES.md`), or to 12 at most with a justification in the cover letter |
| 2 | Reviewers cannot reach the code, data or full proofs (§7.1, §7.2) | The review build says the code is "available in an anonymized repository supplied to the editor", and every [S] proof is "in the repository". ToG asks for an anonymous.4open.science link. Unverifiable [S] theorems invite a reject-and-resubmit | Put an anonymous.4open.science link in Section XIII; put the full [S] proofs in a supplementary PDF |
| 3 | AI disclosure is incomplete (§3.6) | IEEE requires the systems used, the sections, and the level of use per section. The text says "chiefly Claude … and Codex", so some systems are unnamed, and "all sections" gives no level | Name every system and give the level of use per section group (wording in §3.6) |
| 4 | Anonymity residue (§6) | "The author" (singular) and "the 2025 study on which this work builds" narrow the field. An arXiv preprint under the author's name, or a public 2025 study, would de-anonymize the paper | Write "the authors" in the review build; ask the EiC before posting to arXiv; keep the 2025-study sentence in the third person |
| 5 | Figure text below 8 pt at print size (§4.2) | Board coordinates print at about 5–6.3 pt. Production returns figures that fail legibility | Regenerate the boards with 11–12 pt labels in the source, or drop the coordinates and say "files a–h" in the caption |
| 6 | Tables cited out of order (§4.5) | Table VII (positions) is first cited in the Appendix, after Table VIII. IEEE copy-editing will query this | Move the table to the supplement (plan), or input it after Section XII and cite it in Section I |
| 7 | Evidence labels [P] [S] [C1] [C2] [Conj] look like IEEE citations (§5.3) | "[C2]" next to "[2]" reads as a reference. Reviewers may also object to "[S] … independent check pending" | Change the delimiters (e.g., a sans-serif tag without brackets, or ⟨C2⟩); define them in a footnote-free sentence in Section I, as now |
| 8 | Named build author block has no affiliation or country (§2.3) | IEEE requires affiliation and country in the first footnote of the final version | Add the affiliation (or "Independent researcher"), city, country and e-mail to `\thanks` |
| 9 | References: no DOIs, a Wikipedia source, an undated web page (§8) | Copy editors query these; reviewers dislike Wikipedia as a source | Add DOIs where they exist; replace or drop the Wikipedia citation; date the XBoard page |
| 10 | Undefined acronyms (§5.4) | FEN, KPK/KRK/KQK/KBNK…, LSTM, Syzygy, MB are never spelled out | Define each at first use (list in §5.4) |
| 11 | Last page unbalanced in the named build (§9.3) | Page 15 has about 2.8 in of references in the left column and an empty right column; the comment at `main.tex:168` claims it balances | Add `\IEEEtriggeratref{N}` or reflow; resolved by the cut plan anyway |
| 12 | Table of contents in the named build (§3.2) | IEEE journals never have one; harmless on arXiv, wrong for any IEEE file | Drop it from anything sent to IEEE (the review build already omits it) |
| 13 | Caption beginning with "The" (§4.4) | Style query only | "Three puzzles of [9] …" |
| 14 | Stale build files in `paper/ieee/` (§9.5) | `main.bbl`/`main.log`/`main.aux` date from Oct 21–22 and do not match `refs.bib` (no Mäser, Wikipedia or XBoard entries; old Wu–Yü–Landry URL). If they are uploaded with the final source, the wrong bibliography may be typeset | Rebuild the bibliography before packaging the final source |

Items 1–3 are the realistic return-without-review risks. Items 4–7 are likely first-round reviewer or editor
queries. The rest are copy-editing.

---

## 1. Length and format

### 1.1 Page count — **FAIL**
- Review build: 14 pages, both columns full on page 14 (left column to y = 749 pt, right to 733 pt).
- Named build: 15 pages (page 15 holds only the reference tail).
- The ToG limit is 10 pages. Over 12 pages needs a cover-letter justification. Pages 11–14 cost $200 each
  (mandatory) = $800.
- Fix: `PLAN_10_PAGES.md`.

### 1.2 Class and template — **PASS**
- `main.tex:1` uses `\documentclass[journal]{IEEEtran}`. The log shows `IEEEtran 2015/08/26 V1.8b`, the current CTAN
  release. Paper: Letter, 612×792 pt (prints on A4, as ToG asks).
- No `peerreview` or `draftcls`; two-column pages, which is what ToG counts. Correct.

### 1.3 Engine — **PASS (note)**
- Built with tectonic (XeTeX engine). The "Font shape `TU/ptm/...` undefined" warnings (build `main.log:19–38`) are
  harmless: body text comes out in NimbusRomNo9L (Times), as with pdfLaTeX. For the final source upload, check
  that IEEE's pdfLaTeX build matches page for page.

---

## 2. Front matter

### 2.1 Title — **PASS (with advice)**
- `main.tex:95–96`: "Chess Endgames on a Cylindrical Chessboard: Exact Combinatorial Game Values, Real-Chess Checks,
  and Tablebases". Title Case is correct and there is no math.
- It is 15 words and three lines. IEEE asks for "specific, concise". "Real-Chess Checks" is vague.
- Suggested (also saves a line): "Combinatorial Game Values and Tablebases for Chess Endgames on a Cylindrical
  Board".

### 2.2 Running heads — **PASS (review) / minor FAIL (named)**
- Review build, `main.tex:100`: `\markboth{IEEE Transactions on Games}{Chess Endgames on a Cylindrical Chessboard}`.
  Correct, and anonymous.
- Named build, `main.tex:111–112`: both heads are "Bhattacharjee: …". IEEE's left head is the journal line, as in
  the review build. Fix: `\markboth{IEEE Transactions on Games}{Bhattacharjee: Chess Endgames on a Cylindrical
  Chessboard}` (IEEE replaces it in production anyway).

### 2.3 Author block and first footnote — **FAIL (named build) / PASS (review build)**
- Named build, `main.tex:108–110`: `\thanks{A.~Bhattacharjee, e-mail: aritro.sonu@gmail.com.}`. There is no
  affiliation, city or country, and IEEE requires country and e-mail. Fix:
  `\thanks{A.~Bhattacharjee is with <Department>, <Institution>, <City>, <State> <ZIP>, USA (e-mail: …).}`
  If unaffiliated, write "is an independent researcher, <City>, <Country>".
- `\IEEEmembership`: none used. Correct unless the author is an IEEE member.
- ORCID: not in the PDF. IEEE collects it in ScholarOne and adds it in production. **UNKNOWN**: make sure the
  ScholarOne profile has one.
- "Manuscript received …" paragraph: absent. IEEE inserts the dates in production. Optional: start the first
  `\thanks` with "Manuscript received <date>; revised <date>." for the final version.
- Review build, `main.tex:99`: "Anonymized for review". Correct.

### 2.4 Abstract — **PASS (tight)**
- `sections/00_abstract.tex:1–13`. About 194 words (pdftotext count, minus the "Abstract—" head). ToG allows
  150–200, so there is almost no headroom: any edit that adds words breaks the limit.
- One paragraph, no citations, footnotes or display math. Values are written in words ("star two",
  "one-eighth"). Good.
- Proper names ("Elkies", "Grundy") are not citations. Acceptable.
- No undefined abbreviations. "a-file" and "h-file" are chess terms.

### 2.5 Index Terms — **PASS / UNKNOWN (taxonomy)**
- `00_abstract.tex:15–17`: "Chess, combinatorial game theory, endgame tablebases, game solving, nimbers." Five terms
  (the ToG maximum), alphabetical, only the first word capitalized.
- IEEE Thesaurus: "Game theory" and "Games" are thesaurus terms; "nimbers" and probably "endgame tablebases" are
  not. Not checked (it would have needed another fetch). Optional swap: "Game theory" in place of "game solving",
  if the thesaurus lacks the latter.

---

## 3. Structure

### 3.1 Section numbering — **PASS**
- Roman numerals I–XIV with subsections A, B, … (IEEEtran default). "Introduction" and "Conclusion" are singular.
- Fourteen sections is a lot for a 10-page paper. The plan merges several.

### 3.2 Table of contents — **FAIL for any IEEE file (named build only)**
- `main.tex:119–133` prints a table of contents on page 1 of the named build (about 2.45 column-inches). IEEE
  journals do not have one. The review build already omits it (`\ifdefined\anonbuild\else`).
- Fix: keep it for arXiv if wanted, but never send a build with it to IEEE. Ideally switch it off by default.

### 3.3 Appendix — **PASS (form) / FAIL (table order, §4.5)**
- `main.tex:153` `\appendix[Positions]`, a single unnumbered appendix before the Acknowledgment. Correct IEEE form.
- Its table (Table VII, `sections/appendix_table.tex`) floats onto page 13, inside Section XII. See §4.5.

### 3.4 Order of parts — **PASS**
- Abstract, Index Terms, I–XIV, Appendix, Acknowledgment, References. IEEE order.

### 3.5 Acknowledgment — **PASS (form)**
- `main.tex:156`: `\section*{Acknowledgment}`, singular, unnumbered, third person ("The author thanks
  Prof.~T.~Morley"). No funding is mentioned, so nothing needs to move to the first footnote.

### 3.6 AI-use disclosure — **FAIL (incomplete)**
- `main.tex:161–165`: "AI coding assistants, chiefly Claude (Anthropic) and Codex (OpenAI), were used … to write and
  run the software … of all sections, and to help draft and edit the text."
- The IEEE policy requires (a) the AI system to be identified, (b) the specific sections, and (c) the level of use
  for each.
  - "chiefly" admits unnamed systems. Project memory names other CLIs (agy, muse, qwen, opencode, Kilo).
  - "help draft and edit the text" gives no sections and no level.
- Fix: replace the two sentences with something like:
  > "Generative AI was used as follows. Software: AI coding assistants (Claude, Anthropic; Codex, OpenAI; <list
  > every other system used>) wrote, under the author's direction, the solvers, tablebase generators and
  > cross-checks behind all computational results in Sections II–XIII; every result was checked by at least two
  > independently written programs as labeled. Text: the same assistants drafted and edited prose in Sections
  > I–XIV and the Appendix, which the author revised. Figures were generated by AI-written scripts from the
  > computed data. The author chose the research questions, verified the results and is responsible for all
  > content."
- Keep the disclosure in the review build too (it is, and correctly so).

### 3.7 Biographies — **PASS (none) / UNKNOWN for the final version**
- None. ToG counts biographies toward the 10 pages and treats them as optional. If production asks for one, use
  `\begin{IEEEbiographynophoto}` (about 1 column-inch). Leave them out of the review build.

---

## 4. Figures and tables

### 4.1 Vector graphics and embedded fonts — **PASS**
- All 35 figure PDFs are vector (`pdfimages -list` finds no raster images). The only raster file, `CoverPic.png`,
  is not used.
- `pdffonts main.pdf`: every font is embedded and subset (Type 1C, CID Type 0C, plus AppleSymbols CID TrueType for
  the chess glyphs).
- Note: AppleSymbols is a macOS system font, embedded with no ToUnicode map ("uni no"). PDF eXpress normally
  accepts this. **UNKNOWN** until the PDF has been run through IEEE PDF eXpress.

### 4.2 Font size at print size — **FAIL**
- The board figures are drawn 118 pt wide with 9 pt coordinate labels (`make_figures.py:54`) and then scaled down:

  | Figure | Inclusion | Scale | Label size at print |
  |---|---|---|---|
  | Fig. 1 (`02_rules.tex:54`) | 0.30\columnwidth | 0.64 | ≈ 5.8 pt |
  | Fig. 2 (`02_rules.tex:63–85`) | 0.16\textwidth | 0.70 | ≈ 6.3 pt |
  | Figs. 3, 4, 6, 7 | 0.32\columnwidth | 0.68 | ≈ 6.1 pt |
  | Fig. 5 (`06_atlas.tex:19–31`) | height 1.05 in | 0.65 | ≈ 5.8 pt |
  | Fig. 8 (`10_tablebases.tex:99`) | 0.26\columnwidth | 0.55 | ≈ 5.0 pt |
  | Fig. 9 (`11_dawson.tex:11,17`) | scale 0.8 | 0.80 | ≈ 7.2 pt |
  | Fig. 10 (`11_dawson.tex:28`) | \textwidth | ≈ 1.06 | ≥ 8.5 pt (**PASS**) |

- IEEE asks for at least 8 pt type in figures at final size.
- Fix: in `make_figures.py`, set the "small" preset label size so that label × scale ≥ 8 pt. For example,
  12.5 pt labels at 0.64 scale, or draw the boards directly at 80 pt width with 8 pt labels. Alternatively, drop
  the rank and file labels from the small boards and add "files a–h left to right" to the captions.

### 4.3 Colour, greyscale and colour-blind safety — **PASS (checked visually)**
- The boards are light grey and steel blue; in greyscale the two square shades stay distinct, and the pieces are
  black and white glyphs.
- In Fig. 10, blue bars and red dots differ in shape as well as colour, so the figure survives greyscale and
  red–green colour blindness.
- The legend and axes are labeled in words ("strip length n", "Grundy value g(n)"), as ToG asks.

### 4.4 Caption style — **PASS, one FAIL**
- Captions read "Fig. N." followed by a sentence-case sentence (IEEEtran). The subfigure letters (a)–(f) are
  described in the main captions.
- FAIL, `05_sums.tex:32`: the caption begins "The three puzzles of~\cite{Study2025} …". The IEEE ESM says a caption
  does not start with "The". Fix: "Three puzzles of [9] …"
- Inconsistency, `02_rules.tex:85`: subcaption (f) says "tiny(1)" (via `\tinyg{1}`), while the text says "Tiny 1".
  Pick one form.
- The table captions use Title Case, sit above the table ("TABLE I"), and have no final period. **PASS**
- Table and caption titles contain evidence labels (`\lab{C2}` in the captions at `05_sums.tex:44` and
  `10_tablebases.tex:21`). Allowed, but see §5.3.

### 4.5 Every figure and table cited, in order — **FAIL (tables)**
- Figures 1–10: each is cited, in numerical order of first citation. **PASS**
- Tables I–VI and VIII: cited in order. **PASS**
- Table VII (`appendix_table.tex`, label `tab:positions`) is input before Section XII (`main.tex:146`) and floats to
  page 13, but its first citation is in the Appendix (`appendix_positions.tex:3`). That comes after Table VIII
  (`12_engines.tex:10`). **FAIL**
- Fix: move it to the supplement (plan). If it stays, cite it in Section I ("Table VII gives the FEN…", replacing
  `01_intro.tex:60`). Citing it there makes it the first table cited, though, so also move the `\input` so that
  it is numbered Table I or placed last.

### 4.6 Table style — **PASS**
- booktabs throughout, with no vertical rules. Table notes sit in a `\parbox` under the table, which is acceptable.
  IEEE's own style uses table footnotes (a, b) but does not require them.

### 4.7 Float placement — **PASS**
- All floats use `[!t]`. None lands in the first column of page 1.

---

## 5. Equations, notation, acronyms, evidence labels

### 5.1 Equation numbering and punctuation — **PASS**
- One numbered equation, (1) at `11_dawson.tex:53–55`, cited as "(1)" via `\eqref`. It ends with a comma before
  "where". Correct.
- One unnumbered display, at `08_star2.tex:41–43`, ends with a comma. Correct.
- amsmath is used with `\interdisplaylinepenalty=2500` (`main.tex:7`), as the HOWTO advises.

### 5.2 Units and numbers — **minor FAIL**
- `09_real.tex:62` "$15.6$ hours": IEEE style is "15.6 h".
- `12_engines.tex:16` "64 MB" is acceptable (IEEE writes "MB" for megabytes).
- Thousands separators: commas are used consistently (`1{,}418{,}480`). **PASS**

### 5.3 Evidence labels [P] [S] [C1] [C2] [Conj]
- **Defined before first use: PASS.** They are defined in `01_intro.tex:29–32`, and the first use is in the
  contribution list that follows (`01_intro.tex:36`). The abstract does not use them.
- **Used consistently: PASS (spot-checked).** Every theorem-like head carries one (`main.tex:67–78` prints them),
  and the conclusion repeats them.
- **Acceptable in IEEE: FAIL (risk).** IEEE has no rule against them, but:
  - In the IEEE numeric citation style, "[C2]", "[S]" and "[P]" are visually citations. The sans-serif
    `\footnotesize` (`macros.tex:5`) helps little in print.
  - "[S]: proof sketched here and given in full in the repository, independent check pending"
    (`01_intro.tex:30–31`) tells the reviewer that results are unrefereed and not in the paper. Four theorems
    rest on [S]: Validity (Thm 3), Cor 4, Thm 5, Sum safety (Thm 10), plus the wall arguments in Section VIII.
- Fix:
  1. Change the delimiter: `\newcommand{\lab}[1]{\textsf{\footnotesize\textlangle#1\textrangle}}`, or a
     superscript tag. Do not use bare brackets.
  2. Drop "independent check pending" from the definition. Put the full [S] proofs in the supplementary PDF and
     say "full proof in the supplementary material".
  3. Mention the system once in the cover letter, as a feature.

### 5.4 Acronyms defined at first use — **FAIL**
- Defined: CGT (`01_intro.tex:5`), e.p. (`02_rules.tex:8`), HSS (`05_sums.tex:99`).
- Not defined:
  - FEN (`01_intro.tex:60`, Appendix): "Forsyth–Edwards Notation (FEN)".
  - KQK, KRK, KBBK, KBNK, KNNK, KRBK, KRRK, KQRK (`10_tablebases.tex:32–39`, first in the text at `:48`): add "We
    name endings by their men, K for king, Q queen, R rook, B bishop, N knight, P pawn; KRK is king and rook
    against king."
  - KPK (`10_tablebases.tex:72`): covered by the same sentence. KPKP likewise.
  - LSTM (`12_engines.tex:76`): "long short-term memory (LSTM)".
  - Syzygy (`09_real.tex:4`): a proper name; add "the Syzygy endgame tablebases".
  - MB: standard, acceptable.

### 5.5 Notation consistency — **PASS (spot-checked)**
- `macros.tex` centralizes the notation (B, `\nim`, `\cyl`, `\flatb`, `\game`).
- Minor: "W a2 / B b4" pawn lists (monospace) appear inside running text. Acceptable.

---

## 6. Double-anonymous review build

| Check | Result | Evidence and fix |
|---|---|---|
| Author name and affiliation | PASS | `main.tex:99` |
| Running head | PASS | `main.tex:100` |
| Repository link | PASS (absent) | `main.tex:31–32` (`\codeurl` empty). But see §7.1: reviewers get no link at all |
| PDF metadata | PASS | `pdfinfo main_review.pdf`: Author empty; Title only; no XMP stream. `strings` shows no name or paths |
| Acknowledgment | PASS | The Morley thanks is removed (`main.tex:158–160`); only tool maintainers and the AI statement remain (ToG bans funding acknowledgments, not these) |
| Self-citation | PASS (borderline) | `refs.bib:171–176` prints "Anonymous, 'Title withheld for review,' 2025, unpublished manuscript". Acceptable. Because it is unpublished, consider giving the EiC an anonymized copy as review-only material |
| Singular "The author" | FAIL (minor) | `main.tex:157,164`: "The author thanks…", "under the author's direction". This reveals a single author. In the review build write "the authors" (ToG reviewers expect this neutral form) |
| "an unpublished 2025 study … that this paper extends" | PASS | `01_intro.tex:27`. ToG requires the relation to be stated in the text. Fine as long as the study is not public. **UNKNOWN**: if the 2025 study is on the web (course page, GitHub), a reviewer can find it |
| arXiv preprint | UNKNOWN | `paper/SUBMISSION.md` plans arXiv posting under the author's name. ToG is silent; ask the EiC first (already noted in `GUIDELINES.md` §F) |
| Underfull vbox | PASS | Review log: one `Underfull \vbox (badness 4940)` during output. Invisible |

---

## 7. Data, code and supplementary material

### 7.1 Code and data statement — **FAIL (review) / FAIL (named, until pushed)**
- `sections/13_verify.tex:14`: "The code and data are \codeavail."
  - Review build: "available in an anonymized repository supplied to the editor". ToG explicitly asks for
    http://anonymous.4open.science/ links in the manuscript.
  - Fix: create an anonymous.4open.science mirror of the repository and set
    `\newcommand{\codeavail}{available at \url{https://anonymous.4open.science/r/<id>}}` at `main.tex:32`.
- Named build: `github.com/aritroBh/cylindrical-chess-cgt` is private and the local commits are not pushed
  (`paper/SUBMISSION.md`, "Before sending to anyone" item 1). Fix: make it public, tag a release and archive it on
  Zenodo with a DOI; cite the DOI.

### 7.2 Proofs held only in the repository — **FAIL**
- `05_sums.tex:111–112` ("The proof, by induction with (E), is in the repository") and the [S] definition at
  `01_intro.tex:30–31`. Reviewers must be able to check the claims from the submission.
- Fix: supplementary PDF "Full proofs and listings", uploaded to ScholarOne as "Supplementary Material for Review",
  holding the full proofs of Thms 3, 5, 8, 10 and the wall arguments.

### 7.3 Supplementary material rules — **PASS (allowed)**
- ToG excludes supplementary material from the page count but gives no format rules. IEEE Xplore hosts
  supplementary files (PDF, zip) as "Supplemental Items". The plan in `PLAN_10_PAGES.md` uses one supplementary
  PDF plus the archived repository.

### 7.4 Ethics and conflict-of-interest statements — **PASS (not required)**
- ToG asks for neither, and there are no human or animal subjects. Nothing to add.

---

## 8. References (IEEEtran.bst, 19 entries)

| Check | Result | Evidence and fix |
|---|---|---|
| IEEE style via IEEEtran.bst, `cite` package | PASS | `main.tex:5,169` |
| Numbered in order of first citation | PASS | Fresh `main.bbl` order [1] Pritchard … [19] PyTorch matches the text order |
| All entries cited | PASS | BibTeX gives no warnings; Mäser is now cited (`02_rules.tex:32`) |
| "et al." in the list | PASS (rule-conforming) | Only `PyTorch` (`refs.bib:163` "and others"). IEEE allows "et al." for more than six authors, and PyTorch has 21. If a "no et al." house rule is wanted, list all 21 |
| DOIs | FAIL | None given. Add DOIs at least for: Siegel 2013 (AMS GSM 146), Plambeck–Siegel 2008 (J. Combin. Theory A), Guy–Smith 1956 (Proc. Cambridge Philos. Soc.), PyTorch (NeurIPS has none; leave it). The MSRI volumes have no chapter DOIs; keep the arXiv ids. (DOIs not looked up here; check them on Crossref) |
| URLs with access dates | PASS | Every `@electronic` entry has "Accessed: …" (`refs.bib:131,141,151,159,184,191`) |
| Complete fields | FAIL (minor) | `HGMCylinder` (`refs.bib:187–192`) has no author and no year. Write "H. G. Muller, 'Cylinder chess,' XBoard variant rules, <year>." `Dawson1935`: give the editor of *Five Classics of Fairy Chess* if listed, and "pp." `DrummondCole2005` (`refs.bib:62–70`): add the URL of the Integers article. `Study2025`: fine |
| Source quality | FAIL (minor) | `WikiCylinder` (`refs.bib:178–185`): IEEE reviewers discourage Wikipedia. Keep only the XBoard page, or cite Pritchard for the rule claims |
| Software citations | PASS | Stockfish and Lc0 give version, date, URL and access date |
| Stale `paper/ieee/main.bbl` | FAIL (packaging) | See §9.5 |

---

## 9. LaTeX hygiene

### 9.1 Overfull and underfull boxes over 2 pt — **PASS**
- Fresh named build: no Overfull or Underfull `\hbox` warnings.
- Fresh review build: one `Underfull \vbox (badness 4940) has occurred while \output is active`. Invisible.

### 9.2 Undefined references and citations — **PASS**
- No "undefined" or "multiply defined" warnings. BibTeX log is clean.

### 9.3 Last-page column balance — **FAIL (named) / PASS (review)**
- Named build, page 15: the left column runs from y = 26 to 228 pt (about 2.8 in of references); the right column
  is empty.
- The comment at `main.tex:168` ("both builds balance the last page without one") is wrong for the named build.
- Fix: `\IEEEtriggeratref{14}` before `\bibliography` in the named build only, or rely on the cuts.
- Review build: page 14 is balanced.

### 9.4 Widows and orphans — **UNKNOWN (not checked line by line)**
- The contact-sheet inspection found no section heading stranded at a column foot. A line-level widow check was not
  done.

### 9.5 Source package hygiene — **FAIL**
- `paper/ieee/main.bbl`, `main.aux`, `main.log` and `main.toc` date from 2026-10-21/22, while `refs.bib` changed on
  10-27 and the PDFs on 10-29. The stale `main.bbl` lacks Mäser, WikiCylinder and HGMCylinder and has the old
  Wu–Yü–Landry URL.
- Fix: before any source upload (IEEE final files, arXiv), rebuild with `tectonic -X compile -k main.tex` and ship
  the fresh `.bbl`. Remove the unused figures (`CoverPic.png`, `elkies_dup`, `eighth_open`, `kpk_bars`,
  `sum_counter`, `star2_by_pawns`, `star2_eight_five`, `tb_bars`, `superseded/`).

### 9.6 hyperref — **PASS**
- `main.tex:15` `[hidelinks]`; pdftitle and pdfauthor are set per build (`main.tex:36–45`). The `\texorpdfstring`
  wrappers in the headings give clean bookmarks. IEEE production strips hyperref anyway.

### 9.7 Fonts embedded — **PASS**
- See §4.1. `pdffonts` reports emb = yes for every font in both PDFs.

---

## 10. Other observations (not FAILs)

- **Scope.** ToG's scope is "all scientific, technical, and engineering aspects of games". The CGT-heavy core
  (Sections II–IX, XI) needs the cover letter to stress the game-solving, tablebase and engine angle (Sections X
  and XII).
- **Cover letter.** It must say "full paper", that the work is unpublished and not under review elsewhere, and
  justify the length if over 12 pages.
- **The 10–14 page wording.** The ToG page's article list says full papers are "10-14 pages", which conflicts with
  the 10-page limit. Treat 10 as binding for the charges and 12 as the justification threshold.
