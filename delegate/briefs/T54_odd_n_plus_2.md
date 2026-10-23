# T54: is there a ring *2 with n+2 pawns on an odd cylinder? (C9 with 11 pawns)

Output directory: `research/odd_n_plus_2/`. Create it and write nothing anywhere else.

## Background

We work in the whole-board pawn game on the n-file cylinder C_n:
- 8 ranks;
- race rule "count";
- e.p. on;
- a pawn that can still be taken e.p. is not passed;
- the game ends at the first passed pawn.

A *ring* has a pawn on every file.

What is known about the first ring \*2 on C_n:
- It has n+3 pawns for n = 3..7.
- It has n+2 = 10 pawns for n = 8.
- For every even n ≥ 8 a ring with n+2 pawns is \*2. The proof is in `research/ring_n_plus_2_proof/PROOF.md`, using the
  family `W5 B7 W4 W4B7 B6 W3B6 (W2 B4)^m`.
- For odd n we know only n+3, from T50's wall families.

All known small \*2 rings are a *core* on a few consecutive files plus a *wall*. The wall is single pawns, one per
file, alternating colours, in the W2/B4 or W3/B5 pattern.

So far, inserting one single-pawn file into any of the 20 ten-pawn C8 hits gave no \*2 on C9 (1,920 rings).

**Question:** is any ring on C9 with 11 pawns a \*2? If not in the search space below, say so precisely.

## Engine

Copy `research/ring_family_proof/rg.c` into your directory. Do not edit the original. It solves the whole-board game:
- Positions are one token per file, e.g. `W4B7 B6 W2`.
- `rg solve 3` prints the signature of G+*h, h = 0..3. NNPN means \*2 and NNNP means \*3.

Two cautions:
- A run that solves many positions fills the memo table. It then stops with "solver table full" on stderr after a few
  hundred positions, without printing the rest. Either call its solver in-process and clear the table per position,
  or batch at most 40 positions and check that the output count equals the input count.
- Validate any change against unchanged `rg` on 1,000 random rings before using it.

## Search space (structured; do as much as fits in about 6 hours of CPU at 2 processes)

Rings on C9 with 11 pawns of the form *core window + wall*:
- the core occupies w consecutive files, w = 4, 5, 6 or 7, with 11 − (9 − w) pawns;
- the wall occupies the other 9 − w files, one pawn per file, colours alternating along the wall;
- the white wall pawns all share one rank in 2..5, and the black wall pawns all stand two ranks above the white ones.
  Also try the other relative offsets (black one or three ranks above) as a secondary pass.

Enumerate:
- every core window with no passed pawn inside the full ring;
- every wall phase (which end starts white);
- both reflections.

Reduce by the dihedral symmetry and by colour reversal (swap colours and turn the ranks: rank r becomes 9 − r).

Report:
- the count of rings solved;
- every \*2 and every \*3 found;
- for each one, the same ring with the wall extended by two files on C11 (is it still \*2?).

Before the main run, check your enumerator on C8 with 10 pawns. The same core + wall search must find the C8 hits that
have a wall: all 20 rings listed in `research/star26_rings/c8/p10_5_5_hits.tsv`, except those whose wall does not fit
your pattern. Say which.

## Rules

- Follow delegate/COMMON.md.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git. Do not edit `paper/` or any other task's directory. No file over 50 MB; compress large outputs with zstd and
  test the archive before removing the original.
- Write `REPORT.md`:
  - begin with a 5-line summary;
  - give exact counts and every hit;
  - give the commands to reproduce;
  - label claims COMPUTED-1 (one program) or CHECKED-2 (confirmed by a second program, e.g. cylcgt whole-board with
    `pawns.components = lambda b, p: [p]`, for any hit).
