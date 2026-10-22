# T18: style, flow and IEEE-compliance review of `paper/ieee/`

## 5-line summary

The paper builds and is internally consistent, but it is not yet IEEE Transactions on Games material: the
Acknowledgment and author block identify the author (double-anonymous failure), the AI disclosure is
incomplete and contradicts Section XIII, and the byline has no affiliation, city or country. The prose is
readable but repeats definitions (nine settings, temperature, the trébuchet, the default setting) and
slips into lab-notebook phrasing in Sections VI, VIII and IX. One figure label (`fig:kings`) is never
cited as a whole, the only numbered equation is fine, and the last page is over-packed (conclusion,
appendix, references and acknowledgment on one page). No TODO/VERIFY/placeholders or code listings remain.

## Scope

Reviewed `paper/ieee/main.tex`, `sections/*.tex`, `macros.tex`, `refs.bib`, `figures/INDEX.md`, the built
`main.pdf` (13 pages, tectonic/xelatex), and `prior_work/main.tex` for voice. Compared against
`paper/ieee/SPEC.md`, `paper/STYLE.md`, `paper/ieee/GUIDELINES.md`, `RESULTS.md` and the earlier
`paper/ieee/REVIEW_FINDINGS.md` / `REVIEW_LOG.md`. No paper files were edited.

## 1. Critical / IEEE compliance

1. `main.tex:156-170` — **Acknowledgment identifies the author and is incomplete.** The named build prints
   the Morley thanks and the GitHub URL, and the AI disclosure ("Claude (Opus 5.5, Anthropic) ... and
   others") disagrees with `sections/13_verify.tex:13` ("Claude by Anthropic, Codex by OpenAI, and others").
   IEEE requires the AI statement in the Acknowledgment to name every system and what it did.
   Replacement: keep the Acknowledgment as the single disclosure, listing Claude, Codex, Nemotron 3 Ultra and
   MiniMax M3.1 Flash (and any router-selected models), state that AI drafted the manuscript text and
   figures, and drop the model list from Section XIII-D.

2. `main.tex:108-111` — **Author block has no affiliation, city or country; `\markboth` repeats the
   author/title on both sides.** IEEE wants the journal name on the left and `Bhattacharjee: Short Title`
   on the right.
   Replacement: `\thanks{A.~Bhattacharjee is with <affiliation>, <city>, <country> (e-mail: ...)}` and
   `\markboth{IEEE Transactions on Games}{Bhattacharjee: Chess Endgames on a Cylindrical Chessboard}`.

3. `main.tex:2` / `main.tex:3` (`\usepackage[T1]{fontenc}`) — **Font encoding mismatch.** Under tectonic
   (xelatex) the log shows `Font shape TU/ptm/... undefined` and falls back to Latin Modern, so the PDF is
   not in IEEE Times. The build is clean otherwise.
   Replacement: remove `\usepackage[T1]{fontenc}` (or switch to a Times setup that tectonic resolves), and
   re-check the PDF font list.

4. `main.tex:156` — **Double-anonymous.** The byline, e-mail footnote, Morley thanks, GitHub URL
   (`aritroBh`) and the first-person self-citation `by the author` all identify the author; the review
   build already switches some of these, but `main.tex:95`/`main.tex:112` still carry the author name.
   Replacement: confirm the `\anonbuild` path blanks all of them (author, `\thanks`, `\markboth`,
   `\codeurl`, `\bytheauthor`, `pdfauthor`).

5. `main.tex:103-105` — **`\submittedtrue` notice.** The preprint notice macro is defined but the switch is
   off; fine for a draft, but it must be on only after submission. No edit needed now; flag for the
   submission checklist.

## 2. Flow (repetition, jumps, undefined terms)

6. `sections/01_intro.tex:37-38` — **"Nine settings" used before it is defined.** It appears in the
   Introduction bullet and in Section V; the definition is buried in Section VII.
   Replacement: close Section II-C with "The three race rules and three treatments of en passant (the
   textbook test, the e.p.-aware test, and e.p. off) give nine *settings*; our default is the count rule
   with the e.p.-aware test," and shorten the Theorem in Section VII to "in all nine settings."

7. `sections/02_rules.tex:38` and `sections/05_sums.tex:166` — **Temperature defined twice.** The
   thermograph/mean sentence in II-B and Principle 2 in V-A repeat the temperature of ±x.
   Replacement: Principle 2 becomes "Move in the component with the highest temperature (Section II-B)."

8. `sections/02_rules.tex:44` end and `sections/05_sums.tex:87` — **The "first passed pawn ends the game"
   point is made twice.** Section II-D already says it; V-C repeats it almost verbatim.
   Replacement: shorten II-D to "Hence values that only a cylinder can make must come from rings
   (Section VI); Section V-C gives the condition under which a sum of components still names the right
   winner."

9. `sections/02_rules.tex:10` and `sections/10_tablebases.tex:6` — **The slider rule is stated twice.**
   Replacement: in Section X write "Pieces move as in Section II-A and wrap around each glued edge," and
   delete the rook sentence.

10. `sections/08_star2.tex:3` — **`\nim{2}` defined a third time** (Introduction and II-B already define
    it) and "artifact of en passant" is imprecise.
    Replacement: open with "The $\nim{2}$ question of Section I asks whether a king-and-pawn position on a
    board with eight ranks can have this value."

11. `sections/06_atlas.tex:83` — **Internal project history in the paper.** "One honest correction. Our
    first atlas report said ..." does not belong in the published text.
    Replacement: rename the subsection "Dependence on the Race Rule" and delete the first sentence.

12. `sections/06_atlas.tex:46` (last paragraph) — **Tells the candidate's e.p. story ahead of
    Section VIII.**
    Replacement: "On $\cyl{4}$, white a2, c2 against black b7, d7 (the $\nim{2}$ candidate of
    Section VIII) is worth $\game{3/2\pm1/2}{-3/2\pm1/2}$ under the textbook test; under the e.p.-aware
    test it is $\game{2\pm1}{-2\pm1}$ on the ring and on the flat board alike, so it is no longer
    cylinder-only."

13. `sections/08_star2.tex:139-146` — **Underfull box (badness 2318)** from three long `\pos{...}` lists.
    Replacement: put the three positions in a short `itemize` or table, or split each `\pos` into two
    units.

14. `sections/09_real.tex:60-80` — **Lab-notebook bullets** ("A greedy search ... then left", "After these
    results the bounds were"). Reads as a work log, not a result.
    Replacement: rewrite as prose: "All 306 end-position sides with at most seven men are resolved by the
    tablebase: 283 agree with the model, 5 disagree and 2 are draws. A greedy search for a smallest
    decisive set leaves eight larger end positions, five with eight men and three with nine. Resolving the
    eight-man sides gives seven agreements and one disagreement: with black to move in
    \pos{W a3 a5 / B b4 b5}, black wins where the model scores a white win. Our king-and-pawn solver shows
    that all six sides of the three nine-man positions agree with the model, and that white to move in
    \pos{W b2 b5 / B a5 b4} is a white win. Only black to move there is still open, and on its own it
    decides the value."

15. `sections/09_real.tex:82` — **"conditional only on the king freeze" contradicts the previous
    sentence** (under-promotions still unchecked).
    Replacement: "conditional on the king freeze and on an under-promotion rerun."

16. `sections/13_verify.tex:13-16` — **Evidence labels defined twice** (Section I already defines them).
    Replacement: replace XIII-A with one sentence: "In the labels of Section I, a program is independent
    when it was written from the rules alone, without reading the code of the first, and a claim with both
    a proof and a computer check carries both labels."

17. `sections/13_verify.tex:17-22` — **Real-chess tools subsection repeats Sections IV and IX.**
    Replacement: delete the subsection and add to the move-generator row of the table: "covers en passant,
    promotions, pins, checks, mates and stalemates; tablebase responses were cached."

18. `sections/04_kings.tex:152` and `sections/05_sums.tex:155` — **"6×6 cylinder" clashes with the
    $\cyl{n}$ notation** (which assumes eight ranks) and does not say files vs ranks.
    Replacement: "cylinders with six and seven files and six ranks, and an ordinary board with five files
    and six ranks."

## 3. Voice

19. `sections/03_basic.tex:13` — already "Let us begin"; fine. But `sections/07_targets.tex:67` and
    `sections/03_basic.tex:56` use "To see why" and "Let's"-style phrasing flagged by the earlier review.
    Replacement: "To see why, look at Fig.~\ref{fig:eighth}(a)."

20. `sections/02_rules.tex:19` — "you must play on your turn" is too informal.
    Replacement: "There are no null moves: a player must move on every turn."

21. `sections/12_engines.tex:24` and `:80` — "The interesting part is" and "There is an important
    caveat."
    Replacement: "The classes separate at a small fixed depth (Table VI)." and delete the caveat sentence,
    opening the paragraph with "The ground truth here is the CGT model with frozen kings, not real chess."

22. Paragraph openings with "So" in `sections/02_rules.tex` (cut lemma), `sections/04_kings.tex`
    (IV-C, IV-E), `sections/09_real.tex`, `sections/11_dawson.tex`, `sections/12_engines.tex`.
    Replacement: vary or drop them: "Hence values that only a cylinder can make ...", "In short, a white
    shuttle ...", "The group is therefore frozen for black only ...", "Real chess thus agrees with
    $\nim{2}$ on the outcome ...", "The suite is therefore too easy ...", "These numbers therefore
    measure ...", "The ring formula of [9] ... is therefore right once ...".

23. `sections/00_abstract.tex:4,7,10` — "We first make this model exact" overclaims (Section IV shows the
    kings are exact only under (V1)-(V4); "\*2 returns" implies it existed before; "We correct Dawson's
    chess" reads as correcting the game.
    Replacement: "We first repair this model." / "but star two appears with seven pawns, in two positions
    confirmed by three independent programs." / "We correct the earlier analysis of Dawson's chess on the
    cylinder and prove ..."

24. `sections/01_intro.tex` end of paragraph 2 — "But a position with a pawn on every file ..." mixes
    three cylinder differences into a paragraph about prior work.
    Replacement: start a new paragraph: "The cylinder changes this picture in three ways. There are no rook
    pawns, and a position can be shifted sideways by any number of files without changing its value. A
    position with a pawn on every file, a *ring*, has no edge at which to cut it. And the corners that
    decide mates and fortresses on the ordinary board are gone."

25. `sections/07_targets.tex:32` vs the Table II note — the `G - T = 0` check is described twice.
    Replacement: delete "For every counted position G and target T, an independent C solver checked that
    G-T=0." from the text and keep the note.

26. `sections/03_basic.tex:38` and `sections/05_sums.tex` — "black answers it back to 0" / "black answers
    to -3" are clumsy.
    Replacement: "The quieter a2--a3 reaches only *, from which black can return to 0, so it is
    reversible. The move b3--b4 is bad, since black's reply leaves -3."

27. `sections/10_tablebases.tex:13` — "KRK and KBNK are draws on the cylinder" overclaims (2.80% of KRK
    positions are wins).
    Replacement: "*KRK and KBNK cannot force mate on the cylinder.*"

28. `sections/10_tablebases.tex:120` — "On a cylinder every file is a center file, so there are no rook
    pawns" is the third time this point is made.
    Replacement: delete the sentence and start with "Fig.~\ref{fig:kpk_rookpawn} shows the classic
    rook-pawn draw."

## 4. IEEE compliance (beyond the critical items)

29. `sections/00_abstract.tex` — abstract is 195 words (within 150-250) and has no citations, but it uses
    `\pm\BIG` without defining B. IEEE forbids undefined abbreviations.
    Replacement: spell out "a large number $\pm\BIG$ (our programs use $\BIG=256$)" or drop the symbol.

30. `sections/00_abstract.tex` Index Terms — "nimbers" and "game solving" may not be IEEE Thesaurus terms.
    Replacement: check against the IEEE Thesaurus; "game theory" is a Thesaurus term. Keep five terms in
    alphabetical order.

31. `sections/07_targets.tex` Table II caption — "Table II counts them under both passed-pawn tests" plus
    the note; fine. But the earlier review noted the Table I caption starts with "The" (not allowed in
    IEEE captions). Check `sections/05_sums.tex:52` caption "Puzzles of Fig. 5: Claimed and Exact Values".
    It does not start with "The", so OK. Table V caption has lower-case "white Wins".
    Replacement: `sections/10_tablebases.tex:87` caption: "Legal Positions and White Wins on the 8×8
    Ordinary Board and Cylinder."

32. `sections/04_kings.tex:1` — heading "Kings: The Trébuchet and When It Is Exact" is already in Title
    Case; OK. (Earlier draft had lowercase "the"; current file is fixed.)

33. `sections/11_dawson.tex:51` equation — `\label{eq:dawson}` is referenced twice via `\eqref`; good.
    No unused numbered equations remain.

34. `sections/04_kings.tex:45` — `fig:kings` label is defined but never cited as a whole (only its
    subfigures are). A strict referee may ask for a citation.
    Replacement: either cite "Fig.~\ref{fig:kings}" in the text or drop the top-level label.

35. `refs.bib` `PyTorch` — lists six authors plus "et al."; IEEE wants first author plus "et al."
    Replacement: `author = {Adam Paszke and others}` (already done in current file; verify).

36. `refs.bib` `WuYuLandry2010` — key says 2010, entry says 2010; URL is a 2019 course page. Confirm
    year and spelling "Yü" against the PDF.

37. `refs.bib` `DrummondCole2005` — title prints a literal "*2"; ensure it renders as `$\star 2$` (current
    file uses `{$\star2$}`; OK).

38. `refs.bib` `Maeser2002` — present but never cited; arXiv submission rules frown on unused files.
    Replacement: remove from the arXiv tarball or delete the entry.

39. `main.tex:163-169` — AI disclosure names "Claude (Opus 5.5, Anthropic)" and "Further models, chosen
    automatically ... not recorded by name." IEEE asks for every system to be named.
    Replacement: name the router-selected models or drop "not recorded by name" and state that the list is
    complete.

40. `main.tex:156` — "Prof. T. Morley" thanks is fine, but STYLE.md says do not add "Mentored Under
    Thomas Morley" to the author line; current file complies. Keep as is.

## 5. Layout (PDF)

41. `main.pdf` p.13 — **Over-packed last page.** Conclusion, Appendix, References and Acknowledgment all
    land on page 13, with the references in a narrow column and the acknowledgment dangling after them.
    Replacement: move the Acknowledgment before the references (IEEE order: Acknowledgment, then
    References) or add `\IEEEtriggeratref{N}` to balance columns; consider moving the Appendix FEN table to
    supplementary material.

42. `main.pdf` p.1 — The table of contents (named build only) adds a half-page. Acceptable for arXiv, but
    it pushes Section I down; IEEE submissions do not usually include a TOC.
    Replacement: keep it only in the arXiv build (already gated by `\anonbuild`).

43. `figures/INDEX.md` lists `superseded/` and unused figures (`eighth_open.pdf`,
    `star2_eight_five.pdf`, `src/`). arXiv asks for no unused files.
    Replacement: leave them out of the arXiv tarball.

44. Font fallback (item 3) makes the PDF look like a draft; fix before submission.

45. `sections/08_star2.tex:139-146` — underfull box (item 13) produces visibly stretched lines in the PDF.

46. `sections/11_dawson.tex` — `dawson_grundy.pdf` is a full-width `figure*`; check that it does not
    leave a large gap. In the PDF it sits at the top of page 10, which is fine.

## 6. Placeholders / TODOs / code listings

47. Grep of `paper/ieee/` for `TODO`, `VERIFY`, `to appear`, `XXX`, `FIXME` returns only the SPEC, the
    review logs and this report; the paper itself is clean. No code listings appear; code is mentioned
    only in the Code Availability paragraph (`sections/13_verify.tex:23-28`), as SPEC requires.

48. `sections/13_verify.tex:23` — Code Availability paragraph is present and uses `\codeavail`. Good. Ensure
    `\repourl` is defined once in `main.tex` (it is, via `macros.tex`).

## 7. What still keeps it from looking professional (verdict)

Even after the edits above, four things remain that a Transactions on Games referee will notice:

- **The AI disclosure is not yet submission-ready.** It still says that a human check of the proofs is
  pending, while the paper labels statements `[P]`. Either complete the human check or downgrade the
  affected labels. The two versions of the disclosure (Acknowledgment vs. Section XIII-D) must be
  reconciled first.
- **The paper is 13 pages with a cramped last page.** The SPEC target was 12-14, so length is acceptable,
  but the reference list and the acknowledgment need rebalancing, and the Appendix FEN table could move to
  supplementary material.
- **The font fallback** (Latin Modern instead of Times) makes the PDF look like a preprint; fix the
  encoding before any external submission.
- **The double-anonymous build must be verified end-to-end** (no author, e-mail, Morley thanks, GitHub
  URL, or self-citation). The named build is fine for arXiv.

Until those four are resolved, the paper reads as a strong, well-checked draft rather than a finished
journal article. The scientific content, the move-by-move walk-throughs and the table/figure hygiene are
already at the right level.
