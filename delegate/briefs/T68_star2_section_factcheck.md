# T68: fact-check of the ring and nimber claims in the paper (Sections I, VIII and XIV)

Output: `delegate/out/T68/REPORT.md` (create the directory). Write nothing anywhere else. Keep the report under about
150 lines and write it in one go at the end.

## What to check

Read `paper/ieee/sections/01_intro.tex`, `paper/ieee/sections/08_star2.tex` and `paper/ieee/sections/14_conclusion.tex`.
For every number, position and label (\lab{P}, \lab{AI}, \lab{C2}, \lab{C1}, \lab{Conj}) in the passages about rings,
the least number of pawns, $\nim{3}$ and $\nim{4}$, find the source in the repository and check that it says the
same thing. Sources to start from:

- `research/c9_rings/REPORT.md` (C9, C10, C11 rings, the M_n and O_n families);
- `RESULTS.md` (sections 6c and 6d);
- `research/star4_rings/*/REPORT.md` (the search for a $\nim{4}$);
- `research/ring_family_proof/`, `research/ring_n_plus_2_proof/`, `research/ring_n_plus_2_check/` (the wall-family
  proofs and their referee reports);
- `research/ring_n_proof/PROOF_N.md` and `research/ring_n_check_logic/REPORT.md` (the n-pawn families).

The paper writes positions as \pos{W ... / B ...} with files a, b, c, ... (file a = file 0) and ranks 1-8; the reports
write rings as one token per file, e.g. `B4 W2 B6` = black pawn on a4, white on b2, black on c6. Convert and check
that each printed position is the ring the source names.

The labels mean: P proved here; AI proof checked by AI models; C2 two independently written programs agree; C1 one
program. A claim may not carry a stronger label than its source supports.

## Report format

A table with one row per claim: the paper's text (short), the file and line, the source, and OK / WRONG / UNSUPPORTED /
LABEL TOO STRONG / LABEL TOO WEAK, with the correct text when it is not OK. Then a list of anything else that reads
wrong.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. You should not need to start any process; if you
  do, record its PID and stop only that PID. Other projects share this machine.
- Read only. No git. Do not edit `paper/` or any other file except your output.
