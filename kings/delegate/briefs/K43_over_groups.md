# K43: over groups (LOOPY §8 item 2, second half of Conjecture 4.7)

K15 and K26 found dud groups (both sides can shuttle forever) but no over group. Read LOOPY §4 (Conjecture 4.7,
Definition 4.8, Lemma 4.9), §5.7 and §8 item 2, and K15/K26 reports.

1. Write down exactly what an over group is in P (value over = {0 | pass}: one side has a spare tempo forever, the
   other does not), and a computable test for it from the K15/K26 two-shuttle tests.
2. Exhaustive search on cyl:6×6 … cyl:9×6 and flat 7×6, 8×6: groups on |F_Z| ≤ 4 files with up to 3 + 3 pawns,
   all king placements, with your own solver from SPEC.md; a second implementation (or kp_p --pmodel / ref3m with
   board names like `cyl:7x6`) must confirm every hit.
3. If none exists, try to prove why (a parity or king-opposition argument) or state the search bound as the result.
4. Output findings.txt, EDITS.md for LOOPY (§4 Conjecture 4.7 status, §8 item 2, status row).
