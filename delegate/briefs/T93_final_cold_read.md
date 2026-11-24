# T93: final cold read of the 10-page paper (other-vendor referee)

Read-only task. Do not edit anything outside `delegate/out/T93/`. Do not commit.

Input: `delegate/out/T93/paper.txt` (text of the anonymous 10-page paper, `dist/tog/tog_review.pdf`); the LaTeX
sources are `dist/tog/sections/*.tex` if a formula is unclear in the text dump. The supplement is
`dist/tog/supplement_review.pdf` (67 pages; use `pdftotext -layout` if you need it).

You are a referee for IEEE Transactions on Games reading the final version once, cold. Report only things that are
wrong or that a referee would mark, not style preferences:

1. Mathematics: any statement, proof sketch or worked line of play that is wrong. Replay every line of play given in
   the text on the stated board (cylinder: the a-file is next to the last file; pawns capture across the seam;
   en passant allowed) and check the game values claimed for the small positions of Sections II, III, VII and VIII
   by hand or with a short program of your own written from the rules in Section II (state which).
2. Recompute independently: the Grundy values of the octal game 0.137 for n <= 80, the period 34, the last exception
   n = 51, the list n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57 of Theorem 16, and recurrence (1).
3. Internal consistency: a number, board size, range or label that differs between abstract, introduction, body,
   captions, tables and conclusion.
4. Any sentence that claims more than its evidence label allows (labels: P proved in the paper, S proof in the
   supplement, C2 two separately written programs, C1 one program, Conj conjecture).
5. Typos, broken sentences, undefined symbols or terms used before they are defined.

Output: `delegate/out/T93/REPORT.md` with a table: # | severity (error / should fix / minor) | location (section,
quote) | what is wrong | suggested exact replacement text. Then a list of what you recomputed and the result.
If you find nothing in a group, say so in one line. End with one sentence: accept as is / minor / major.
