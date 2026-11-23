# T81 — Referee: self-contained proofs of the four S-labelled king and sum results

Output directory: `delegate/out/T81/` (create it). Write `REPORT.md` there and any programs. Do not edit
anything else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs
you started and recorded yourself. At most 2 processes at once, each under 3 GB, `nice -n 15` if your sandbox
allows it; total compute budget about 60 minutes. Other people's jobs run on this machine: leave them alone.
Do not copy raw terminal transcripts into your report, and do not write anything from your own memory of other
projects or any personal identifier (names, email addresses, home paths outside this repository) into it.

## What to referee

`dist/tog/supp_src/s12a_core.tex` (LaTeX, items A.1 to A.17; written by one AI model). It is the first
subsection of Section S12 of the supplement of a paper on pawn endgames as combinatorial games. It claims complete
hand proofs, using only its own definitions, of four results that the 10-page paper states with the label S
("proof sketched here, full proof in the supplement"):

- Theorem `thm:validity` and Corollary `cor:v4`: `dist/tog/sections/04_kings.tex`, lines 44 to 79;
- the certificate statement: same file, lines 81 to 86;
- Definition `def:hss` and Theorem `thm:hss` (sum safety): `dist/tog/sections/05_sums.tex`, lines 45 to 70.

The rules of the model are in `dist/tog/sections/02_rules.tex` (passed-pawn tests, race rules, BIG).
The author's notes are in `delegate/out/core_proofs/NOTES.md`. Do not rely on `kings/theory/LOOPY.md` or on the
rest of S12: the point of the subsection is that it stands alone.

## Tasks

A. **Referee every proof as a hostile reader.** For each of A.1, A.2, A.4, A.5, A.6, A.7, A.8, A.9, A.10, A.11,
   A.13, A.14(a)(b), A.16 say CORRECT, CORRECT WITH A FIX (exact replacement text), or GAP / WRONG (smallest
   counterexample or the missing case). Look hardest at:
   1. A.7 and A.6: the induction that S(X) and W(X) have the same winner. Is every option of the sum matched
      with a move of the whole-board game and back? Are en passant rights handled (a right stays with its
      component in a sum but lapses after one move on the whole board; a pawn that has just double-stepped is
      not passed under the e.p.-aware test and may become passed after a move elsewhere)? Is the move bound
      BIG > N(X) used correctly in A.6 (count White's and Black's moves exactly, including who starts)? Is
      "every integer that appears is +BIG" justified by A.5? Does HSS as defined (over Reach(X) only) suffice?
   2. A.2(c) and the hypothesis H >= 6: is it needed, and is it enough for S(X) to be well defined?
   3. A.11: is the chess strategy well defined at every turn (side to move has a move; the opponent's legal
      moves are covered: context moves, Z-moves, moves when it has no move in W)? Is termination shown? Is
      anything used that (V1) to (V3) as stated in the subsection do not give?
   4. A.16: the four steps. Are real moves of the defender always local moves or passes (including a king
      capture of a context pawn, a king off the group files, a move while in check)? Are the punisher's
      prescribed moves always legal in the real position? Does (C2) really exclude a defender promotion first,
      including promotions by capture and en passant? Is the mate claim in Step 4 right? Is anything missing
      that could let the defender win, draw or stall in the promotion game (for example the punisher's king
      being attacked from outside the group files, or the defender's king capturing the promoting pawn before
      it promotes; note the game ends at promotion)?
B. **Does the precise form imply the main text's statement?** For each of the four results compare the precise
   form with the paper's wording at the lines given. List every hypothesis the subsection adds (for example "X
   has no passed pawn", "local race rule", "H >= 6") and say whether the paper's sentence is still true as
   printed, true only with the added hypothesis, or false. Remark A.15 says the paper's one-sentence certificate
   definition is a loose summary of (C1) to (C3): is the paper's sentence misleading enough to need a change?
   If so give replacement text of at most 150 characters.
C. **Small machine checks, your own code.** (1) A.9: confirm max over positions of Phi_t is n(H-1)(H-2)/2 and
   that it is 168 for n = H = 8. (2) A.14(b): replay the two move sequences on the cylinder of 8 files and
   confirm no pawn is passed before the stated moment and one is after it. (3) If cheap: on boards of 3 or 4
   files and 6 ranks, enumerate small pawn positions with no passed pawn, test HSS, (E) and compare the winner
   of S(X) with BIG = 256 against W(X) for both sides to move; report the number tested and any counterexample
   to A.7. Use the e.p.-aware test and the count rule as in `02_rules.tex`; write the solver yourself.

## Report

`delegate/out/T81/REPORT.md`: a verdict line first (ALL FOUR PROVED / PROVED WITH FIXES / GAP), then A, B, C
in order, each finding as `s12a_core.tex:line` with the exact replacement text, then the commands to rerun
your programs. Say plainly what you did not check.
