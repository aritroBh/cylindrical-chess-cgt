# T84 re-read of final ring-proof texts

Text 1 (dist/tog/supp_src/s14_ringn.md): FINAL TEXT SOUND
Text 2 (dist/tog/supp_src/s15_note4.md): FINAL TEXT SOUND

## Findings

No BLOCKER or MAJOR found in either final text. Minor wording items only:

- dist/tog/supp_src/s14_ringn.md:8 (MINOR) -- "no smaller $n$-pawn ring of this family is $\star2$; $n<10$ is not in scope" conflates the two families' lower bounds. Exact replacement: "no smaller $n$-pawn ring of either family is $\star2$; $n<10$ ($M$) / $n<11$ ($O$) is not in scope".
- dist/tog/supp_src/s14_ringn.md:54 (MINOR) -- the parenthetical ranks in H2 are wall-specific and read as a general rule. Exact replacement: "With pattern neighbours the capture squares of $q$ are empty (rank 3 in the $M$ wall, rank 6 in the $O$ wall), and a $B4$ cannot take e.p. a $W2$ that has not moved (Note 1 of Section S15, H3)."

## Computed facts and labels

Text 1 (s14):
- C1M, CHECKED-2: independently rebuilt M_18 reduced graph: 441 nodes, 1128 K-moves, 428 T-moves, no flags, zone {10,11,12,13,14,15,17}, files 0..9 exact pattern. Our independent run: delegate/out/T84_opencode/solve.py graph M 18 -> nodes=441, K=1128, T=428, flagged=0, zone=[10,11,12,13,14,15,17].
- C1O, CHECKED-2: reported 2132 nodes, 6352 K-, 2680 T-moves, zone {0,12..18}; not recomputed by us in this budget.
- C2, CHECKED-2: full whole-board search (our code, keep and expire readings agree) for the smallest members: M_10 signature NNPN for heaps 0..3; O_11 signature NNPN. These are the first four characters of the reported NNPNN. Smaller members checked: M_8 is not *2 (NNNN); O_9 is not *2 (RRRR).
- C3, COMPUTED-1: reported pump stability; not recomputed by us beyond the base graph above.

Text 2 (s15):
- C1T, CHECKED-2: independently rebuilt T_20 reduced graph: 1305 nodes, 4018 K-moves, 1212 T-moves, no flags, zone {10,11,13..18}. Our run: delegate/out/T84_opencode/solve.py graph T 20 -> nodes=1305, K=4018, T=1212, flagged=0, zone=[10,11,13,14,15,16,17,18].
- C1S, CHECKED-2: reported 40445 nodes; not recomputed by us in this budget.
- C2, CHECKED-2: full whole-board search (our code, both readings agree): T_12 signature NNNPN for heaps 0..4; S_13 signature NNNPN. These are the first five characters of the reported NNNPNN. Smaller members checked: T_10 is not *3 (LLNLL); S_11 is not *3 (NNNRR).

Labels checked as honest: no computed fact was found overstated relative to our independent runs. The base-case labels (CHECKED-2) are supported by the reported multi-program agreement; we independently reproduced the two base reduced graphs and the four smallest full-search signatures.

## Reproduce our programs

From the project root:

    PYTHONPATH=. .venv/bin/python delegate/out/T84_opencode/solve.py
    PYTHONPATH=. .venv/bin/python delegate/out/T84_opencode/solve.py graph M 18
    PYTHONPATH=. .venv/bin/python delegate/out/T84_opencode/solve.py graph T 20

The first command prints the four smallest-member signatures; the graph commands print node/edge/zone counts. All use only the Python standard library and do not import cylcgt, rg.c, or myeng.py.

## Not checked

We did not recompute the O_19 (2132 nodes) or S_23 (40445 nodes) reduced graphs, the insertion isomorphisms beyond the reported counts, the Lemma 2/3 hypothesis counts, the race-rule sensitivity, the component-sum model, or any claim about arbitrary game addends. We did not run a human proof check. Our independent search covers the smallest member of each family and one reduced graph per text; it does not replace the cited multi-program finite checks for the larger base sizes.
