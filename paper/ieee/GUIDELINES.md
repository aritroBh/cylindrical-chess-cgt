# Submission guidelines: IEEE Transactions on Games (ToG) and arXiv

Checked 2026-10-21. Tags such as [TG] point to the source list at the end. Where the SPEC and a source disagree, see "Conflicts with SPEC". Policy figures below come from the cited pages, not from our results.

## A. Target and review model (ToG)
- [ ] Full paper: 10 pages in the two-column format, counting references and biographies. Supplementary material does not count. Over 12 pages needs a written justification in the cover letter [TG].
- [ ] Over-length charge: $200 per page beyond 10 if the voluntary $110/page charge is not paid [TG].
- [ ] Double-anonymous review for submissions from 2025-01-01. Remove names, affiliations, biographies and funding acknowledgments [TG, TGH]. (The same page also says "single-blind"; the double-anonymous notice is newer, so follow it and ask the EiC if unsure.)
- [ ] Code and data during review: use anonymous.4open.science, linked in a footnote or the Acknowledgment. Put the real links in the final version [TG].
- [ ] An extension of prior work must state the relation and what is new in the paper itself, not only in the cover letter, while staying anonymous [TG]. Mention the 2025 study in the third person.
- [ ] Cover letter: say "full paper", say the work is unpublished and not under review elsewhere, and justify the length if over 12 pages [TG]. Submit at https://mc.manuscriptcentral.com/tg-ieee [TG].
- [ ] Scope is "all scientific, technical, and engineering aspects of games". CGT and chess are not named, so the cover letter should tie the paper to game solving, engines (Stockfish/Lc0 by CGT class) and learning [TGH].
- [ ] Final version: all source files, graphics as separate files, and the IEEE copyright form [TG]. Biographies are optional and count toward the limit, so use `IEEEbiographynophoto` or none [TG, HOW].

## B. IEEEtran setup
- [ ] `\documentclass[journal]{IEEEtran}`. The default is 10pt; letter paper also prints on A4 [HOW §II, TG]. Do not use `peerreview` (it adds a single-column cover page); ToG counts two-column pages [TG].
- [ ] Title in Title Case: capitalize nouns, verbs, adjectives and subordinating conjunctions [ESM]. Make it specific; no "new" or "novel", and no math symbols (so no \nim{2} in the title) [STR].
- [ ] Author: `\author{Aritro~Bhattacharjee\thanks{affiliation, city, country, e-mail}}`. The corresponding e-mail is required. Funding goes in this first footnote, not in the Acknowledgment [STR, ESM]. Use `\IEEEmembership` only for an IEEE member. Running head: `\markboth{IEEE Transactions on Games}{Bhattacharjee: Short Title}`. Leave names out of the heads in the anonymous version [HOW §IV].
- [ ] Abstract: one paragraph of 150–200 words (ToG; IEEE-wide 150–250). Self-contained: no abbreviations, references, footnotes, or displayed or numbered equations [TG, ESM]. Avoid symbols; write values in words where possible [STR, HOW]. Put `\begin{abstract}` and `\begin{IEEEkeywords}` before the first section [HOW].
- [ ] Index Terms: at most 5 (ToG allows 2–5, IEEE says 3–5). Alphabetical, only the first word capitalized, acronyms spelled out, no math [TG, ESM, STR]. Check them against the IEEE Thesaurus [STR]. Candidate: *Chess, combinatorial game theory, endgame tablebases, game solving, nimbers*.
- [ ] Order: Abstract, Index Terms, Introduction, body, Conclusion, Appendix, Acknowledgment, References, Biographies [ESM §II].
- [ ] Headings: `\section` gives "I.", `\subsection` gives "A.", `\subsubsection` gives a run-in "1)". Write "Introduction" and "Conclusion" in the singular. Cite sections as "Section II-A1" and never write "Subsection" [ESM]. Open with a drop cap: `\IEEEPARstart{C}{ylinder}` [HOW, ESM].
- [ ] One appendix: `\appendix[Positions]`, titled "Appendix" and unnumbered; its theorems get an "A" prefix. Use `\appendices` for more than one [HOW §XIII-A, ESM].

## C. Figures, tables, equations, theorems
- [ ] Floats go at the top (`[!t]`), never in the first column of page 1, and almost never `[h]`. Use `figure*` for full width [HOW §X]. Place each float near its first mention, preferably after it [ESM §F].
- [ ] Cite figures and tables in numerical order at first mention. Always write "Fig. 3", even at the start of a sentence. A caption reads "Fig. 3." followed by a capitalized first word, and does not start with A/An/The. Describe subparts "(a)", "(b)" in the main caption [ESM].
- [ ] Tables: caption above, "TABLE I" in Roman numerals, no final period [ESM, HOW §X-C]. No floating algorithm environments; IEEE uses only figures and tables [HOW §X-B].
- [ ] Captions must make sense without the text, and graph axes need descriptive labels [TG]. Board pictures should stay readable in grayscale [TG].
- [ ] Subfigures: the HOWTO says subcaption "can not be recommended" because it takes over IEEEtran's captions. Use `\usepackage[caption=false,font=footnotesize]{subfig}` with `\subfloat[]{...}` [HOW §X-A1].
- [ ] Third-party image (the Wikimedia cover picture): check its license and credit it at the end of the caption [ESM, reuse of graphics].
- [ ] Equations: use `equation` or amsmath `align`, with `\interdisplaylinepenalty=2500`, and never `eqnarray` [HOW §IX]. Everything must fit `\columnwidth`, so break long game expressions [HOW §VIII]. Number consecutively and refer as "(3)", not "Eq. (3)" [HOW §VIII, ESM]. An equation that ends a sentence takes a period [ESM].
- [ ] Theorems: `\newtheorem{theorem}{Theorem}`, plus `\newtheorem{lemma}[theorem]{Lemma}` and likewise for Proposition, Corollary, Definition and Conjecture, sharing one counter numbered through the paper, as most IEEE papers do. Proofs use `\begin{IEEEproof}[Proof of Theorem~\ref{..}]` [HOW §XII]. Put labels in the optional title: `\begin{theorem}[Cut lemma; \lab{P}]`.

## D. References (IEEEtran.bst)
- [ ] Use `\usepackage{cite}`, which sorts and compresses to [2]–[4]. Put several keys in one `\cite`. Then `\bibliographystyle{IEEEtran}` and `\bibliography{IEEEabrv,refs}` [HOW §VII, §XIII-C].
- [ ] One work per number. List all authors up to six; with more, write the first author plus "et al.". Every entry has a year. Point to parts as "[3, Ch. 2]" or "[1, Fig. 2]" [REF §I–II, ESM].
- [ ] Book (`@book`): "A. N. Siegel, *Combinatorial Game Theory*. Providence, RI, USA: AMS, 2013." [REF §B].
- [ ] Chapter (`@incollection`, with editor, series and pages): "N. D. Elkies, “On numbers and endgames…,” in *Games of No Chance* (MSRI Publ. 29), R. J. Nowakowski, Ed., Cambridge, U.K.: Cambridge Univ. Press, 1996, pp. 135–150." [REF §B, E96].
- [ ] arXiv-only work: "J. K. Author, “Title,” year, arXiv:NNNN." Use `@misc` with `howpublished`. For a published work, cite the published version [REF §S].
- [ ] Website (Lichess API, Wikimedia file): `@electronic` (alias `@online`) with `url`. IEEEtran.bst has no `urldate`, so put "Accessed: Oct. 21, 2026" in `note` [BST §V-M, REF §T].
- [ ] Software (cylcgt, Stockfish, Lc0): IEEE follows FORCE11. Give author, name, repository, version, release date and a persistent identifier: "Author. *Title*. (Date). Repository. (version). Accessed:… [Online]. DOI/URL." [REF §O]. Cite a manual if one exists, then `@electronic`, and `@misc` only as a last resort [BST §VI-B].
- [ ] Datasets: author, date, title, source, then a DOI or URL [REF §E].

## E. Data, code and AI disclosure
- [ ] IEEE encourages sharing. Code can go in a Code Ocean capsule, which appears under "Code & Datasets" in Xplore; data can go to figshare, Zenodo or Dryad [REP]. These pages do not require a data statement, so the SPEC's single Code Availability paragraph is enough. Archive a tagged release (e.g., a Zenodo DOI) and cite it in the references [REF §O].
- [ ] AI use must be disclosed in the Acknowledgment. Name each AI system, the sections where it was used, and how much it did. This covers text, figures, images and code. Disclosure is recommended even for editing-only use [AI, ESM, POL]. Take the system names from delegate/REVIEW.md. Section XIII can keep the methodology detail.
- [ ] Acknowledgment: `\section*{Acknowledgment}`, singular, no "e", not numbered, in the third person: "The author thanks Prof. T. Morley…". No Mr./Mrs. [ESM, HOW §XIII-B]. In the anonymous version, keep only the AI disclosure.

## F. Preprints and arXiv
- [ ] IEEE: once the paper is submitted, any posted preprint must carry "This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible." On acceptance, add the IEEE copyright notice and send IEEE the URL. After publication, post the accepted manuscript but never the IEEE PDF [POL].
- [ ] ToG says nothing about preprints under double-anonymous review, and some IEEE venues reject papers that already have an arXiv preprint [TG, COMSOC]. **Ask the EiC before posting.**
- [ ] Upload TeX source. arXiv rejects PDFs produced from TeX [XSUB]. With pdfLaTeX, figures must be PDF, PNG or JPG; arXiv does not convert them, so do not mix in EPS [XTEX, XMIS].
- [ ] Shell escape (`\write18`) is disabled [XMIS], so no pgfplots externalization and no minted.
- [ ] Bibliography: upload `main.bbl` named after `main.tex`. Get it with `tectonic -X compile -k main.tex`. Since Nov 2025 arXiv can also run BibTeX itself [XTEX, XBIB]. The HOWTO also suggests pasting the .bbl into the .tex [HOW §XIII-C].
- [ ] Files: relative paths only; names use only `a-z A-Z 0-9 _ + - . , =`; names are case-sensitive; no hidden files, no .aux/.log/.pdf, no unused figures; arXiv compiles from the upload root [XTEX, XSUB, XMIS]. `paper/ieee/figures` is a symlink, so build the tarball with `tar -h` to copy the real files (our own precaution).
- [ ] arXiv uses TeX Live 2025 by default; tectonic uses its own bundle. Check the PDF that arXiv builds page by page. Pass no hyperref driver options; if PDF bookmarks fail, use `bookmarks=false`. Do not use `\today` [XTEX, XMIS].
- [ ] Metadata: authors as "Aritro Bhattacharjee". Abstract at most 1920 characters, without the word "Abstract" and without `\emph` or `~`; MathJax math is allowed. Comments: page and figure counts, the code URL, and "submitted to IEEE Trans. Games". MSC-class 91A46 (combinatorial games) [XMETA].
- [ ] Categories: primary math.CO, cross-list cs.GT. Endorsement: since 2025-12-10 (math) and 2026-01-21 (all sections), an institutional e-mail alone no longer qualifies, so a first math.CO paper needs a personal endorser [XEND].
- [ ] License: the arXiv non-exclusive license 1.0 keeps copyright transferable to IEEE; CC0 does not [XLIC].
- [ ] AI rules: report significant use of generative AI; the authors are fully responsible for the content [XMOD]. News reports describe a one-year ban for clear evidence of unchecked AI output, such as invented references or leftover placeholders [XBAN, secondary source]. Before uploading, resolve every reference and grep for TODO/VERIFY. Reports also describe a cap of 2 new submissions per month from 2026-10-01 [XRATE, secondary source].
- [ ] Fix errors by replacing the arXiv version, never by a new submission [XSUB].

## G. How strong CGT and chess-endgame papers are built (to emulate)
1. Elkies 1996 [E96] goes small to large: one- and two-file subgames, then a real game (Schweda–Sika, 1929), then fractions, switches and tinies, then loopy king chunks, then open problems. Notation appears only when a diagram needs it, with Winning Ways cited for the details. We should keep §II's CGT paragraph short and define each value at first use.
2. [E96] says up front which moves the model counts (moves that neither lose a pawn nor free an enemy pawn) and where chess departs from CGT (draws, kings, zugzwang). Our §II conventions and the (V1)–(V4) theorem do the same job and belong early.
3. [E96] analyses are terse. Each gives the side to move and the main line for each side, and dismisses dominated moves in one clause ("b3–b4 is bad: black answers to −3"). This matches the 2025 voice; keep every walk-through to a few lines.
4. [E96] ends with labeled open problems that the next paper answered: Elkies 2002 [E02] built higher nimbers on larger boards from Dawson's pawn game. Section VIII must cite [E02] and say how our \nim{2} differs: an 8-rank board of width at most 4, the e.p.-aware test, 7 pawns. Section XIV should pose problems just as concretely.
5. Plambeck–Siegel [PS08] split theory from computation and moved the computation to a separate arXiv supplement (0705.2404). We should do the same: keep the main text within the page limit and put full listings and the FEN appendix in supplementary material, which does not count toward the limit [TG].

## Conflicts with SPEC (orchestrator to decide)
- Length: the SPEC targets 12–14 pp, while ToG allows 10 pp, needs a justification over 12, and charges $200 per page over 10. Cut to 10–12 pp and move tables and the appendix to the supplement.
- Abstract: the SPEC says 150–250 words, ToG says 150–200. Use 150–200.
- Figures: the SPEC asks for subcaption, but the IEEEtran HOWTO recommends subfig with `caption=false`.
- Order: the SPEC puts the Appendix after the References, but IEEE puts it before the Acknowledgment.
- Anonymity: the byline, the Morley thanks, `\repourl` (it contains the user name) and the 2025-study sentence all identify the author. Add an anonymous build switch in main.tex; macros.tex stays unchanged.
- AI statement: the SPEC puts it only in §XIII, but IEEE requires it in the Acknowledgment.

## Sources
- TG: https://www.transactions.games/submit/submission-guidelines · TGH: https://www.transactions.games/
- ESM (IEEE Editorial Style Manual for Authors, 29 Jul 2024): https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf
- STR: https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/
- HOW (IEEEtran HOWTO v1.8b): https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/IEEEtran_HOWTO.pdf
- BST (IEEEtran BibTeX HOWTO v1.14): https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/bibtex/IEEEtran_bst_HOWTO.pdf
- REF (IEEE Reference Guide, V 3.28.2025): https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf
- POL: https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/
- AI: https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/
- REP: https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/research-reproducibility/
- COMSOC: https://comsoc.org/publications/journals/ieee-comml/ieee-communications-letters-regular-double-anonymous-review-process
- XTEX: https://info.arxiv.org/help/submit_tex.html · XSUB: https://info.arxiv.org/help/submit/index.html
- XMIS: https://info.arxiv.org/help/faq/mistakes.html · XMETA: https://info.arxiv.org/help/prep.html
- XBIB: https://blog.arxiv.org/2025/11/05/attention-authors-updates-for-bib-file-processing-and-tex-in-arxiv-submissions
- XLIC: https://info.arxiv.org/help/license/index.html · XMOD: https://info.arxiv.org/help/moderation/index.html
- XEND: https://info.arxiv.org/help/endorsement.html and https://blog.arxiv.org/arxiv/2025/12/10/updated-endorsement-policy-for-arxiv-mathematics
- XBAN (secondary): https://casrai.org/news/arxiv-one-year-ban-unchecked-ai-content
- XRATE (secondary; official post of 2026-10-01 listed at https://blog.arxiv.org/2026): https://alternativeto.net/news/2026/10/arxiv-limits-researchers-submissions-at-two-papers-per-month-amid-ai-powered-paper-flood/
- E96: https://arxiv.org/abs/math/9905198 · E02: https://arxiv.org/abs/math/0011253 · PS08: https://arxiv.org/abs/math/0609825
