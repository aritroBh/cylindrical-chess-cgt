# W8: S12.2 cut and replaced (2026-11-23)

Rebuild: `sh dist/tog/rebuild.sh` OK. tog 10, tog_review 10, supplement 67 (was 109), supplement_review 67 pages.
Last lines: free in right column 0.36 in; RESULT: all numbers found; anon hits 0 / 0; overfull/undef-ref: 0 (tog) 2 (supplement).
The 2 supplement hits are Overfull hboxes of 2.4 pt (log lines ~915, 920); no undefined references (the font-shape warning is old). Full output: rebuild.out.
supplement.txt of the build: supp.txt here.

## Edits
build_supplement.py
- new helper REP(text, old, new) (assert count == 1).
- S12: removed `\subsection{The Longer Treatment}`, NOTE block and MD('kings/theory/LOOPY.md',225,2213,...); now
  `\subsection{Two Further Proofs for Section~S2}\label{S-kingslong}` + scrub(supp_src/s12b_extra.tex). S12 title kept. S-kingslong was only used in the build script; label kept (now also cited from S2).
- S2 (guarded REP on the slices of long/04_kings.tex): (V2) sentence replaced with the W7 wording plus "(Proposition~A.19 of Section~\ref{S-kingslong})";
  Theorem S4 proof sketch ends with "The full proof is Theorem~A.18a of Section~\ref{S-kingslong}."; locked pair sentence followed by an example
  (W Ka2 a3 d2 / B Kb4 a4 e3, cylinder 6 files x 6 ranks, black to move; pawn a3 checks the king, black has only its four king moves, each loses the promotion game, white wins; with kings and locked pair removed black wins moving first; computed, three separately written programs agree on the first result, two on the second, C2);
  edges sentence gets "(the counts are in kings/REPORT.md, task K4, in the code copy)".
- S5 lead-in: "To see why, look at Fig.~\ref{fig:eighth}(a)." deleted by REP on the L('07_targets',62,90) slice.
- S7.1: "no file between its pawns and T is free of pawns, so Theorem..." -> "file e holds pawns and file f the white king, so T has no empty buffer and Theorem... does not apply" (REP only; long paper unchanged). I judged it true: the five-file position W a3 b3 c2 e2 / B a6 c5 d5 e3 has pawns on e, T = W Kf5 g4 / B Kh4 g5 starts with the king on f.
supp_src/s12a_core.tex
- A.12(d): "Unlike (V1a) of Theorem~1.14 in the longer treatment, (V1) contains no condition (E):" -> "(V1) contains no condition (E):".
- "Where to find the longer treatment ..." paragraph -> "Further material. The working note kings/theory/LOOPY.md in the code copy has further results and the records of the computer checks; its numbering differs from the numbering used here."
- No other numbered item of the old note is cited in the file (grep for Theorem~1., 2., Definition, Proposition, Lemma 2). The lead-in "read without the rest of this section" kept.
supp_src/s17_provenance.tex
- old row "Longer treatment, S12.2: ..." -> row "S12.2, A.18--A.19b ...": written by a Claude Opus model, November 2026, as a condensation of Theorem 3.4 and Prop 2.11 with Cor 2.11a of the working note; Theorem 3.4 of the note by an open model via OpenCode; checks stated as checks of the note's results, not of the condensed text (Claude reviewers (no); Codex (yes) on Prop 2.11 sound, two passages tightened; Codex (yes) Theorem 3.4 holds, one false sentence replaced); programs: 22,522,464 comparisons on 763,440 games (Thm 3.4), several programs for Prop 2.11. A line `%%T91-RESULT%%` (LaTeX comment) is inside the checked-by cell, for the T91 result. Dropped facts about Theorems 1.11(c), 1.14, 2.7, 2.10(a) (they concern S12.1/the note, not A.18-A.19).
- "What the checks found": Theorem 3.4 sentence -> "Theorem A.18a ... (in the note's version, Theorem 3.4)"; Theorem 1.11(c) sentence -> "An earlier proof of the induction behind Theorem A.7 (Lemma A.6 and Theorem A.7) had a gap in its move-count step"; horizon-1 -> "The horizon-1 proposition of Section~\ref{S-kings}" (it is Proposition S2, proved inline in S2). Caption (line 14) unchanged (still true).
supplement.tex: line 85 -> "(S12 is a self-contained write-up; S13--S15 are typeset from the project's proof notes)"; label key extended with the \lab{P}/"hand proof"/AI sentence (references S-prov); line ~104 "typeset from the project's proof notes" now says Sections S13--S15 are typeset from the notes.
dist/anon/build.py: README row for Kings/Section III now lists kings/theory/LOOPY.md. Not run.
submission: pdf_checks.md ("supplement 106 pages" -> 67, page table 109 -> 67), cover_letter.md (109 -> 67), scholarone_fields.md (109 -> 67 twice; "3 words of headroom" -> "1 word"; the abstract is 199 words by my count of 00_abstract.tex, limit 200). files_to_upload.md rows and pdf_checks sizes refreshed by rebuild.sh.
paper/PROOF_READING_ORDER.md: pages updated (S12.1 17-23 unchanged; S12.2 23-27; S13 28-31; S14 32-35; Note 1 36-42; Note 2 42-44; Note 3 44-50; Note 4 50-54; Note 5 54-59; Note 6 60-63; S17 64-67), total 67, "about 43 pages", Part B 36 pages, "Not needed" section replaced by Part C with three read-slowest points from W7.

## Leftover grep (pdftotext of dist/tog/supplement.pdf)
- "longer treatment", "Theorem 1.1x", "Theorem 2.7", "Proposition 2.1x" in the old sense, "Lemma 2.2", "Definition 1./2.", "??": none.
- "Theorem 3.4" / "Proposition 2.11": only in the lead-in of S12.2 (p.23) and S17 (Table S9 row and "What the checks found", naming the note). Allowed.
- "S12.2" appears only as pointers from S2 (V2 sentence, Theorem S4 sketch), the heading and the S17 row. All sensible.

## Not done / unsure
- "Real trébuchets seem to need h ≈ 5-7 <Conj>": left unchanged. The only source is kings/REPORT.md:67 (also :528), stated without derivation; line ~433 says "The T of Definition 2.6 was not computed" for a different group. No evidence found, so no clause added. R19 suggested deleting the sentence from the Conclusion and S2.
- Locked pair example: the position is the one in the note's (V1a) row, and it does show a Z consisting of kings and a locked pair whose zero is broken in P. But the note says the cause is the check (a3 gives check to kb4); the twin with the king on b5 is fine. I wrote that the pawn checks the king, but the S2 sentence "a locked pawn pair can still break their zero" is therefore only as strong as "in a case where the pair gives check". The note's refp.py is not in the code copy (so "three programs" are partly not reproducible by a reviewer).
- Theorem S1's last sentence "Clause (ii) cannot be weakened to h-1 moves" (R18 C3) was not in my task list; untouched.
- The S2 intro and the main text (04_kings.tex:66, 85) still say "Section S12"; true. R18 optional "S12.1" not applied (sections/* not allowed).
- Remaining mention in s12_kings.md: file left in place and unused.
- The `%%T91-RESULT%%` marker sits inside a tabular cell line; fill it in as a plain sentence there (no %).
