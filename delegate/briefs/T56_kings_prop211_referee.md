# T56: Independent non-Claude referee for Proposition 2.11 (kings)

Read delegate/COMMON.md first and obey it (no pattern kills, kill only your own PIDs, label claims COMPUTED-1 vs CHECKED-2, never claim a number your own run did not print, no git commit or push). You are the non-Claude referee this project queued for after the Codex quota reset.

## Background
kings/LOOPY.md proves Proposition 2.11 (the passer certificate). Two Sonnet reviewers already checked it and searched for counterexamples in 5,730,596 certified cylinder positions plus 434,429 flat ones. They found one real gap: statement P11 covered only terminal positions reached by a move, not a starting position that already has a passed pawn. P11 was fixed (commit 1f22f91) so such a root must itself satisfy Prop 2.11. No model outside the Claude family has re-derived the proof.

## Task
Work in a new folder kings/muse-referee/. Do not edit LOOPY.md, RESULTS.md, or any existing file.
1. Re-derive Proposition 2.11 independently: read the statement and Steps 0-5 plus Corollaries 2.11a/b in kings/LOOPY.md, and check each step against the solver code it relies on (kings/ kpsolve sources, cylcgt/, sumtest/ as needed). Note any step you cannot justify from first principles.
2. Check the P11 fix specifically: does the amended statement actually close the passer-root gap, and does the end-to-end checker code enforce it?
3. If compute allows within COMMON.md limits, run your own targeted counterexample search on passer-root starting positions (a different sample than the Sonnet sweep if you can construct one); report exact counts of anything you run.
4. Write kings/muse-referee/REPORT.md: verdict SOUND / SOUND WITH RESERVATIONS / GAP FOUND, section by section, with every number traceable to your own runs (include scripts in the folder).