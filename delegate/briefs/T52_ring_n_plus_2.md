# T52: rings worth *2 with n+2 pawns on C_n for n ≥ 8

Output directory: `research/ring_n_plus_2/`. Create it and write nothing anywhere else.

## Background

We work in the default setting: count rule, e.p. on, e.p.-aware passed test. A *ring* on the cylinder C_n has a
pawn on every one of its n files. The first ring worth *2 has n+3 pawns for n = 3..7; this is checked by two
programs.

Earlier work built a *wall family* with n+3 pawns, *2 on every C_n with n ≥ 5. It is proved in the whole-board
game in `research/ring_family_proof/`. The wall is single pawns of alternating colors on consecutive files:
- W3/B5, as in the odd family `W23B4, B5, W2B5, (W3, B5)^k`;
- W2/B4, as in the even family `B5, W2B5, W35B6, W2, (B4, W2)^(m+1)`.

If a wall pawn moves, its neighbor captures it and gets a passed pawn.

New result: the C8 scan finds no nine-pawn ring worth *2, but in the 5+5 split of the ten-pawn rings it finds 18
classes worth *2 and 2 worth *3. Ten is n+2. They are in `research/star26_rings/c8/p10_5_5_hits.tsv`, one
position per line, a tab, then `8 10 N,k` (k is the nimber). cylcgt confirms them
(`research/star26_rings/c8/cylcgt_p10_5_5.txt`). Example: `W: a3 b3 c3 d2 f2 / B: b6 d5 e5 g4 h5`, whose files
f, g and h look like a wall.

**Question: is there a ring worth \*2 with n+2 pawns on every C_n, n ≥ 8?** And on C_9, is there one with n+1 = 10?

## What to do

1. **Structure.** For each of the 18 *2 classes, find the longest run of wall files: a single pawn per file,
   colors alternating, W2/B4 or W3/B5 phase, the black pawn two ranks above the white one on adjacent files.
   Report the "core" window (the files that are not wall) and its pawn count.
2. **Grow by wall insertion.** For each class, insert one wall file (n+1, one more pawn) and two wall files
   (n+2, two more pawns) at every position inside or next to the wall, in both phases. Try both colors and
   ranks 2–6 for a single new pawn. Evaluate every result on C_9 and C_10 with the existing C solver
   `research/star4_hunt/ring4`. Build it from `ring4.c` into YOUR directory with
   `cc -O2 -DSTRIDE=10 -o research/ring_n_plus_2/ring4 research/star4_hunt/ring4.c -lm`, and use `--eval FILE`
   (see the header of `ring4.c`; widths up to 10 only). Do not edit `research/star4_hunt/`.
   Report every *2 ring with n+2 pawns on C_9 and C_10.
3. **Family.** If one pattern gives n+2 pawn rings on C_8, C_9 and C_10 by repeating wall files, write it as a
   formula, like the families above. Then test it for n = 11..26 in the whole-board game with cylcgt
   (`pawns.components = lambda b, p: [p]`), one ring at a time, under `nice -n 15`, with a 30-minute cap per
   ring. Also give the sum-model value (`pawns.value`) where it finishes. If the T50 proof engine
   `research/ring_family_proof/rg.c` can be pointed at the new family by copying it into your directory and
   changing only the family builder, run its reduced-graph and pumping checks too (`run_all.sh` shows how). Do
   NOT edit T50's files.
4. **C_9 with 10 pawns (n+1).** Only a pilot. Time 4 chunks of the 5+5 split with the scanner,
   `research/star26_rings/frontier_split1_fixed2 --cylinder --width 9 --min 10 --max 10 --nw 5 --nb 5
   --only-setting 2 --chunk I 4096 --max-entries 67108864`, with I = 0, 1000, 2000, 3000. Run from
   `research/star26_rings/`; output into your directory. Estimate the cost of the full scan. Report any hit.

## Rules

- Follow delegate/COMMON.md.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start
  and stop only those, by PID. Other projects share this machine.
- At most 2 processes at a time, each under `nice -n 15` and under 4 GB RSS.
- No git. Do not edit `paper/` or any other task's directory. No file over 50 MB.
- Python: use `.venv/bin/python` from the project root, with `PYTHONPATH=.`.
- Write `REPORT.md` in your output directory.
  - Begin it with a 5-line summary.
  - List every ring you claim with its value, the program that computed it and the time it took.
  - Label each claim: COMPUTED-1 (one program) or CHECKED-2 (two programs: ring4 and cylcgt).
  - Give the exact commands to reproduce.
- When done, compress raw outputs over 1 MB with `zstd`, test the archive (`zstd -t`), then remove the original.
