# T64: non-Claude check of the least ring *2 on C9 (is it 10 = n+1 pawns?)

Output directory: `research/c9_rings/codex/`. Create it and write nothing anywhere else.

## Background

We study the whole-board pawn game on the n-file cylinder C_n:
- 8 ranks; files wrap;
- race rule "count"; e.p. on;
- a pawn that can still be taken e.p. is not passed;
- the game ends at the first passed pawn.

A ring has a pawn on every file. A root ring has no passed pawn.

You already wrote a solver for this game (`research/ring_n_plus_2_check/independent.py` and
`research/ring_n_plus_2_check/odd/independent.py`).

What is known:
- the least number of pawns in a ring *2 is n+3 on C3..C7;
- it is n+2 on C8 (no nine-pawn ring there is *2).

A Claude-written enumerator (`research/c9_rings/enum_rings.c`) plus the `rg` engine scanned every root ring on C9 with
10 pawns. They found exactly 7 rings with signature NNPN (*2), all with 5 white and 5 black pawns, and no *3:

    B4 B7 W3 W2B5 B7 W3 W2 B7 W2
    B6 B7 W2B7 W4 B6 W2 W5 B7 W2
    B4 W2 B6 W2 W3 B6 B7 W3 W6B7
    B6 B7 W3 B7 W5 W2B3 B6 W2 W3
    B6 B7 W3 B7 W5B4 W2 B6 W2 W3
    B4 B7 W3 B5 W2B7 W2 W3 B7 W2
    B6 B7 W2 B7 W5 W2 B6 W4B7 W2

Tokens are per file, file a first; `W4B7` = a white pawn on rank 4 and a black pawn on rank 7.

If this is right, C9 needs only n+1 pawns, fewer than C8.

## What to do (use only your own code and the rules above; do NOT read rg.c, enum_rings.c or cylcgt's value code)

1. **Hits.** With your solver, compute the signature of G+*h, h = 0..3, for each of the 7 rings and for their colour
   reversals (swap colours, rank r -> 9-r). Also do one control ring that is not *2.
2. **Nine pawns.**
   - Write your own enumerator of all root rings on C9 with exactly 9 pawns (one per file), every colour split, up
     to rotation and reflection.
   - Report the counts per split.
   - Solve every one with your solver, if that fits in about 4 hours; otherwise solve all of the 4+5 and 5+4 splits
     and a stated random sample of the others.
   - Report every *2 or *3. We expect none if the minimum is 10.
3. **REPORT.md.**
   - Begin with a 5-line summary.
   - Give exact counts, every signature, the run times and the commands.
   - Label claims COMPUTED-1 (your program alone) or "agrees with the Claude result".

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under 4 GB RSS. Use `nice -n 15`; if the sandbox refuses it ("setpriority: Operation not
  permitted"), run one process at a time without it.
- No git. Do not edit `paper/` or any other directory.
