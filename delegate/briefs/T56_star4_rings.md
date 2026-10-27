# T56: hunt for a ring *4 with the fast whole-board engine

Output directory: `research/star4_rings/`. Create it and write nothing anywhere else.

## Background

Whole-board pawn game on the n-file cylinder C_n (8 ranks, race rule "count", e.p. on, a pawn that can still be taken
e.p. is not passed, the game ends at the first passed pawn). A *ring* has a pawn on every file. No *4 is known.

**What is known about *3:**
- On C7 and C8, ten-pawn rings reach *3.
- The family Q_n = W4 B7 (B4 W2)^k W3B6 W3 W2B5 B5 W2 B4 is *3 for every even n.
- A search of 134.9M one-component flat ten-pawn positions found no nimber above *3.
- Every known flat *3 is a *2 core plus a *1 pair. Two C7 *3 rings are primitive. See `research/star4_hunt/REPORT.md`.

**Engine.** `research/ring_family_proof/rg.c` solves the whole-board game fast (milliseconds per ring).
- Copy it into your directory and build it with `cc -O2 -DMAXN=64 -o rg rg.c -lpthread`. Do not edit the original.
- Usage:
  - positions are one token per file, e.g. `W4B7 B6 W2`;
  - `rg solve 7` prints the signature of G+*h for h = 0..7;
  - a *k has N everywhere except P at position k (so *4 = NNNNPNNN).
- **Caution:** a long batch fills the memo table, and rg stops with "solver table full" on stderr after a few hundred
  positions. Batch at most 40 positions per run and check that the output line count equals the input count.

## What to do

1. **Seeds.** Collect seeds from:
   - the 20 C8 hits in `research/star26_rings/c8/p10_5_5_hits.tsv`;
   - the 43 C10 *2/*3 rings obtained by inserting a wall pair (W2 B4, B4 W2, W3 B5, B5 W3, W2 B5, B5 W2, W3 B4,
     B4 W3) at each of the 8 positions of each C8 hit;
   - the Q_n and P_n families for n ≤ 14.
2. **Local search.** From every *3 seed, try all ways to:
   - (a) add one pawn anywhere legal;
   - (b) add a pair (one W, one B) on two adjacent files;
   - (c) insert one or two new files holding one or two pawns;
   - (d) attach a whole *1 group on extra files. A single W r / B r+2 pair on one file is *1 alone on a flat board;
     check that on the ring.

   Evaluate with `rg solve 7` on C_n for n ≤ 14. Keep every *3 and *4 found and iterate (grow from new *3s) for at most
   3 rounds.
3. **Sums.** Rings are single components, but a *2 ring beside a separate *2 component would be *0. Instead, try
   placing the C8 *3 core and a *1 group in one ring with a buffer file between them, on C10 to C14.
4. **Report** every *4 (signature NNNNP...) with its pawn count, and confirm each with cylcgt whole-board
   (`pawns.components = lambda b, p: [p]`, from the project root, `PYTHONPATH=. .venv/bin/python`). Also report
   counts of all *2/*3 by n and pawn count, and the largest nimber seen.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS. Cap each run at 4 hours.
- No git. Do not edit `paper/` or any other task's directory.
- No file over 50 MB: compress with zstd, test the archive, then remove the original.
- Write `REPORT.md`:
  - begin with a 5-line summary;
  - give exact counts, every hit and the commands to reproduce;
  - label claims COMPUTED-1 or CHECKED-2.
