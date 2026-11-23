# K45: is K44's over root an exact over group in P? (Conjecture 4.7)

K44 found roots of the king-fight game LK equal to over and under on cyl:10×6 and wider, with three blocked pairs
(files a, c, f: `Kc3 ka4 Pa2 pa3 Pc4 pc5 Pf2 pf3`; mirror a, c, h gives under). K43 found no exact over group of
Definition 4.8 in P, but searched only four files. Read LOOPY Definition 4.8, Conjecture 4.7, Lemmas 4.9–4.11, §8 items
2 and 3, and the K43 and K44 reports.

1. Run Definition 4.8's exact over/under test in P on the K44 battery configurations (three pairs within six files),
   cyl:10×6 to 12×6, every king placement. Use K43's test code as one implementation and your own (from SPEC.md and
   Definition 4.8) as the second.
2. If an exact over group exists in P, Conjecture 4.7's over half is realised: give the smallest one, its roots, and its
   values beside a sample of contexts (kp_p --pmodel and ref3m, board names with a colon, e.g. `cyl:10x6`).
3. If not, say exactly which clause of Definition 4.8 fails at K44's roots and why the LK value does not transfer.
4. Output findings.txt, EDITS.md for LOOPY (Conjecture 4.7, its status row, §8 items 2 and 3).
