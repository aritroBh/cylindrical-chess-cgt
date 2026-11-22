# ToG 10-page version: meaning-change check (2026-11-22)

Checker: independent Sonnet agent, read-only. L = `paper/ieee/sections`, S = `dist/tog/sections`, supp = `dist/tog/supp`.
Counts: BLOCKER 4, SHOULD FIX 9, MINOR 9. Clean: every number and position string, theorem labels, cross-references,
headline results, anonymity of names/paths/metadata.

## BLOCKER
- B1. S `01_intro.tex:52` lost "with the new test": write `with the e.p.-aware test the textbook $\nim{2}$ candidate is
  not $\nim{2}$, however draws are treated;`. S `09_real.tex:41-42` lost the caveat: end the sentence with
  `\lab{C1}; with draws worth $0$ the textbook tree is not decided.`
- B2. S `01_intro.tex:51` "from $\cyl{11}$ on $n+1$ pawns give a $\nim{3}$ \lab{S}" is wrong (the proof starts at
  n = 12; C11 is computed). Use the corrected long-version sentence: `$n+1$ pawns give a $\nim{3}$ on $\cyl{11}$
  \lab{C2} and on every $\cyl{n}$ with $n\ge12$ \lab{S}.` (fixed in L on 2026-11-22).
- B3. S `05_sums.tex:71-72`: restore the label and hedge: `without (E) the decomposition already fails in the pure
  pawn game, without the passed-pawn rule \lab{C1} (Section~S3).`
- B4. S `14_conclusion.tex:16-17`: restore the label: `The certificate theory settles the promotion game, not chess;
  real tr\'ebuchets seem to need $h\approx5$--$7$ \lab{Conj} (Section~S2), so we trust a frozen tr\'ebuchet only
  beside slow or locked components.`

## SHOULD FIX
- S1. Intro "Model and kings" bullet: `a passed-pawn test that respects en passant, a cut lemma \lab{P}; conditions
  (V1)--(V3) under which a frozen tr\'ebuchet gives the result of the whole-board pawn game \lab{S}, and (V4) for the
  $\pm\BIG$ value \lab{S}; a sum-safety theorem \lab{S}; and a position showing that checking only the top-level
  components is not enough \lab{C2}.`
- S2. Intro "Small values" bullet: sections are `\ref{sec:basic}, \ref{sec:atlas} and~\ref{sec:targets}`, not a range.
- S3. Intro: define the default setting at first use: `(count rule, e.p.-aware test; Section~\ref{sec:ep})`.
- S4. S `09_real.tex:13`: add `The tree is built under either passed-pawn test: the \emph{textbook tree} or the
  \emph{e.p.-aware tree}.`
- S5. S `04_kings.tex:82-84`: define the certificate: `For (V3) there is a local test: a move in $Z$ has a
  \emph{certificate of horizon $h$} if the punisher promotes within $h$ of its own moves against any defence and no
  defender pawn promotes that fast. In the \emph{promotion game}, where the first promotion wins, a move with a
  certificate loses for its mover \lab{S}; in chess, margins this small can fail (Section~S2).`
- S6. Supplement S12-S16 read as working notes: task IDs (K13, T50, ...), shell lines, `.venv` paths, "Human check
  pending". Strip the IDs, commands and paths; keep the status honest with one sentence at the head of the proofs part
  and in S `13_verify.tex`.
- S7. Anonymous supplement: "a model other than the author" (`supp/s15.tex:88`), first person "My own re-check",
  "I rebuilt" (`s15.tex:106, 274`). Rephrase impersonally.
- S8. Fig. 7 (Grundy values) floats a page before its first citation; move it after the citing paragraph.
- S9. Last page unbalanced; balance after the two slots are filled.

## MINOR
- M1. II-D: add the census scope `(at most six pawns, widths 1--4)`.
- M2. Fig. 6 caption: `$\nim{3}$ is plotted from $n=10$; ten-pawn $\nim{3}$ rings also exist on $\cyl{7}$ and $\cyl{8}$.`
- M3. S `08_star2.tex:121`: "the two families with n pawns above" is ambiguous; write "the two $n$-pawn families above".
- M4. S `09_real.tex:42-43`: add "(Section~S7)" for the other non-default positions.
- M5. S `11_dawson.tex:56`: add "(the first player wins exactly when the $(n-3)$-file strip is a mis\`ere P-position)".
- M6. S `06_atlas.tex:13-14`: add `\lab{C1}` after the temperature 3.
- M8. Corollary 4 proof uses $S(X)$ before V-B: add "(Section~\ref{sec:sums-hss})".
- M9. Supplement says "the long version" (`s01.tex:2`, `s06.tex:46`, `s10.tex:2`): write "the main text".
