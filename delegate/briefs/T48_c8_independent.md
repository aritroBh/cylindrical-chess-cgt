# T48: independent check of the C8 ring minimum (heavy compute, chunked; your own code)

**Output directory:** `research/c8_independent/`. Write everything there; write `REPORT.md` there at the end.

**Background.** On the cylinder Cn (n files that wrap, 8 ranks, pawns only, default setting = count race rule,
e.p. on, e.p.-aware passed test) the first ring \*2 (a ring has every file occupied) has n+3 pawns for n = 3..7.
For C8, rings with at most 8 pawns are not \*2 (earlier scan), and an 11-pawn ring \*2 exists:
`W: b2 c3 c5 d2 f2 h2 / B: a5 b5 c6 e4 g4`. Our C scanner is now scanning all C8 rings with 9 and 10 pawns
(`research/star26_rings/c8/`; read-only for you, and do not touch its processes).

**Task.** Answer independently: is any C8 ring with 9 or with 10 pawns a \*2 (or a \*3)?
- Start from `research/c7_independent/c7check.c`, which you (Codex) wrote earlier for C7, and the variant
  `delegate/checks/c7_epconv/c7check_persist_ds.c`. That variant matches the model's conventions: an e.p. right
  persists across moves in the nim heap, and a pawn on its start rank counts one move closer in the race rule.
  Generalise it to 8 files and to 9 and 10 pawns (the enumeration currently hard-codes 7 columns and 9 pawns).
  Do not read `research/star26_rings/*.c` or `cylcgt/`.
- Self-check first:
  - your C7 nine-pawn count must reproduce `delegate/checks/c7_epconv/enum9/` (19,961,100 classes, no \*2);
  - the C8 wall ring above must come out \*2;
  - `W: a2 a3 c3 e3 f2 / B: a4 b5 d5 f5 g5` on C7 must come out \*2.
- Enumerate every C8 ring with 9 pawns, then with 10 (up to rotation and reflection of the files; pawns on ranks
  2–7; at least one pawn per side; no passed pawn at the root). Test G + \*k for k = 0..3, and report counts of
  classes, of \*2 and of \*3, with examples.
- Limits: at most 2 processes at a time, `nice -n 15`, under 4 GB each; split into chunks and run them
  sequentially. Never use pkill or killall: record PIDs and kill only those (COMMON.md rule 7). Compress any
  output over 50 MB with zstd.

**REPORT.md:** a 5-line summary first; counts by pawn number; the hit lists; labels (CHECKED-2 where they agree
with the scanner's `c8/progress.txt` totals once those exist, otherwise COMPUTED-1); runtimes; reproduce commands.
