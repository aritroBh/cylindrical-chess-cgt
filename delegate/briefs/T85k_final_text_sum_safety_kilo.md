# T85 — Hostile referee read of the FINAL text of the sum-safety proofs (supplement S12.1, items A.1 to A.9)

Output directory: `delegate/out/T85_kilo/` (create it). Write `REPORT.md` there and any programs. Do not edit
anything else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs
you started and recorded yourself. At most 1 process at a time, under 3 GB, `nice -n 15`; total compute budget
about 20 minutes. Other people's jobs run on this machine: leave them alone. Do not copy raw terminal
transcripts into your report, and do not write anything from your own memory of other projects or any personal
identifier (names, email addresses, home paths outside this repository) into it. Do not read or quote the
author block of any paper file.

## Why
The text was written by one AI model and refereed by models that then saw it edited again. Read the final
wording as a hostile referee who wants to find an error. Form your own verdict; do not look for earlier reports.

## Text
`dist/tog/supp_src/s12a_core.tex`, lines 1 to 226: setting and conventions, Lemmas A.1, A.2, Remark A.3,
Lemmas A.4, A.5, A.6, Theorem A.7 (sum safety), Proposition A.8, Remark A.9. The statements they prove are in
`dist/tog/sections/05_sums.tex` (definition of HSS, condition (E), the sum-safety theorem) and the rules in
`dist/tog/sections/02_rules.tex`.

## Do
1. For each of A.1, A.2, A.4, A.5, A.6, A.7, A.8: is the statement precise, and does every step of the proof
   follow? Quote the exact step that fails if one does. Check in particular: the last-rank convention (a pawn on
   its last rank is passed), the order "test the moved component for a passed pawn first, re-split only
   otherwise", "reachable by moves of either side in any order", and where BIG > N(X) is used.
2. Does Theorem A.7 as proved imply the main-text theorem word for word (compare hypotheses one by one)?
3. Try to break A.7 with your own small program: write your own solver for the whole-board pawn game W and for
   the sum model S on a cylinder of 3 to 5 files and 5 or 6 ranks (do not import the repository's code), sample
   or enumerate positions with at most 4 pawns that satisfy the hypotheses, and compare the outcome classes of
   W(X) and S(X). Report counts and any counterexample with the full position.
4. Any undefined symbol, circular reference, or sentence that states more than is proved.

## Report
`REPORT.md`: first line a verdict (FINAL TEXT SOUND / SOUND WITH FIXES / GAP). Then findings as `file:line`,
severity (BLOCKER, MAJOR, MINOR), exact replacement text; the commands to rerun your program; and what you did
not check.
