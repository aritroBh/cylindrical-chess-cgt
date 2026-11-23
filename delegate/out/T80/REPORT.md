## Independent check of pawn endgames by board height

1. **RUN · CHECKED-2** — All eight named positions agree: seven are `*2` and the six-pawn flat four-file example at R=7 is `*3`.
2. **RUN · CHECKED-2** — All five R=5 boards lack `*2` and `*3`. At R=6 the reported `*2` minima and absence of `*3` also hold.
3. **RUN · CHECKED-2** — The R=6 five-file cylinder has **1,786,371** valid roots and **340** zeros. Two impossible material splits account for the earlier excess of 280 roots and five zeros.
4. **RUN · CHECKED-2** — At R=7 the three-file strip has eight `*2` roots and the three-file cylinder has six. Neither has a `*3`.
5. **RUN · CHECKED-2** — None of the 2,381,595 roots in the twelve complete censuses has value `*4` through `*7`. A separate tail check also excludes every larger nimber on these roots (**RUN · COMPUTED-1**).

## Task 1. Named positions

**READ · CHECKED-2** — F denotes a flat strip and C a cylinder. The digit is the file count. Each signature runs from heap size 0 on the left to 7 on the right. N and P mean first- and second-player wins. L and R mean White and Black win, respectively, whichever player starts.

| Evidence | R | Board | White pawns | Black pawns | Signature | Value |
|---|---:|---|---|---|---|---|
| RUN · CHECKED-2 | 6 | F4 | a2 b2 d2 | a5 c5 d5 | NNPNNNNN | `*2` |
| RUN · CHECKED-2 | 6 | F4 | a2 d2 b3 | c4 a5 d5 | NNPNNNNN | `*2` |
| RUN · CHECKED-2 | 6 | C4 | c2 d2 a3 | b4 c5 d5 | NNPNNNNN | `*2` |
| RUN · CHECKED-2 | 7 | F3 | a2 c2 | c3 b6 | NNPNNNNN | `*2` |
| RUN · CHECKED-2 | 7 | C3 | c2 a3 | b5 c5 | NNPNNNNN | `*2` |
| RUN · CHECKED-2 | 7 | F4 | a2 c2 | d4 b6 | NNPNNNNN | `*2` |
| RUN · CHECKED-2 | 7 | F4 | a2 c2 d3 | c3 b6 c6 | NNNPNNNN | `*3` |
| RUN · CHECKED-2 | 9 | C3 | a2 b2 c2 | a8 b8 c8 | NNPNNNNN | `*2` |

## Task 2. Complete census

**RUN · CHECKED-2** — Counts are symmetry classes over all pawn counts. A dash means the census found no such value. “Earlier” gives the published root total. Evidence refers to agreement of board aggregates, including agreement with the archived valid material splits for the corrected row.

| Evidence | R | Board | Roots | Earlier | `*0` | `*1` | `*2` | `*3` | `*4` | `*5` | `*6` | `*7` | Min pawns `*2` | Min pawns `*3` |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RUN · CHECKED-2 | 5 | F3 | 236 | 236 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| RUN · CHECKED-2 | 5 | F4 | 2,196 | 2,196 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| RUN · CHECKED-2 | 5 | C3 | 121 | 121 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| RUN · CHECKED-2 | 5 | C4 | 826 | 826 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| RUN · CHECKED-2 | 5 | C5 | 5,847 | 5,847 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| RUN · CHECKED-2 | 6 | F3 | 7,093 | 7,093 | 102 | 14 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | — |
| RUN · CHECKED-2 | 6 | F4 | 219,491 | 219,491 | 460 | 99 | 7 | 0 | 0 | 0 | 0 | 0 | 6 | — |
| RUN · CHECKED-2 | 6 | C3 | 3,259 | 3,259 | 18 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| RUN · CHECKED-2 | 6 | C4 | 72,435 | 72,435 | 149 | 20 | 1 | 0 | 0 | 0 | 0 | 0 | 6 | — |
| RUN · CHECKED-2 | 6 | C5 | **1,786,371** | **1,786,651** | **340** | 48 | 6 | 0 | 0 | 0 | 0 | 0 | 8 | — |
| RUN · CHECKED-2 | 7 | F3 | 196,918 | 196,918 | 1,123 | 343 | 8 | 0 | 0 | 0 | 0 | 0 | 4 | — |
| RUN · CHECKED-2 | 7 | C3 | 86,802 | 86,802 | 133 | 40 | 6 | 0 | 0 | 0 | 0 | 0 | 4 | — |

**RUN · CHECKED-2** — The discrepancy is in class membership. Every valid C5/R=6 material split agrees on its root count and all eight nimber counts under the stated symmetry reduction. The first and only discrepancies occur at 20 pawns. The archived 1 White + 19 Black split contributes 112 extra roots, including two zeros. The 2 White + 18 Black split contributes 168, including three zeros. Removing them takes the published zero count from 345 to 340.

**READ · PROVED** — Each colour has only 15 eligible squares on this board (three ranks of five files). At full occupancy, rank 2 must be all White and rank 5 all Black, so each side must actually have at least five pawns. Neither disputed split can contain a single root.

**RUN · CHECKED-2** — As a separate check at 20 pawns, `compare.py` tries both colours on each of the ten middle squares. Every pawn has an opposing home-rank pawn ahead on its own file. Reducing these assignments by rotation, reflection and colour reversal gives 78 orbits, equal to the independent C census at this level.

## Task 3. Verdicts

| Claim | Verdict | Evidence |
|---|---|---|
| 1. R=5 | Agree | RUN · CHECKED-2. All five root totals agree and every count for `*2` or `*3` is zero. |
| 2. R=6 | Agree on minima and nimbers. Disagree on one root total. | RUN · CHECKED-2. The `*2` minima are 8, 6, absent, 6, 8 in the order given. No `*3` occurs. The first false count is the C5 split with 1 White and 19 Black, detailed above. |
| 3. R=7 | Agree | RUN · CHECKED-2. The four named witnesses have the stated values. Both complete three-file censuses agree. |
| 4. R=9 | Agree | RUN · CHECKED-2. The three-file cylindrical home position has signature NNPNNNNN. |
| 5. No higher nimber | Agree within the enumerated class | RUN · CHECKED-2 for `*4` through `*7`. RUN · COMPUTED-1 for the tail beyond seven. The unrestricted claim remains open. |

## Method and reproduction

**READ · CHECKED-2 (shared game convention)** — Following “The game” in the earlier report, the winner of a two-sided race is the player with the smaller promotion count. A tie goes to the opponent of the player who just made the pawn move. For a passed pawn on rank r, White counts R−r minus one at rank 2, and Black counts r−1 minus one at rank R−1. Each side uses its smallest count. The home-rank discount is unconditional. A sole passer wins immediately for its owner. [Earlier report](../../../research/tall_boards/REPORT.md#the-game-my-reading-of-cylcgtpawnspy-and-cylcgtcgtpy)

**RUN · COMPUTED-1 (implementation)** — I wrote `check.c` from the game description, using the report to clarify race and heap semantics. The only input to the solver is the geometry or the named example. It plays the whole board, including after a file empties. It uses the adopted e.p.-aware test: a pawn vulnerable to immediate en passant is excluded from both passer lists. A pawn move replaces the previous right. A heap move preserves the board and the right.

**RUN · COMPUTED-1 (enumeration)** — Each nonempty file is a string of empty/White/Black interior squares, with the colour restrictions on the two end ranks. The program enumerates file strings, rejects roots with a passer, and retains the lexicographically least encoding under reflection and colour reversal, plus rotations on cylinders. Every root starts without an en passant right. For each heap and starting side it tests pawn moves and moves to every smaller heap. A signature with a P must have N everywhere else, which the run asserts.

**RUN · COMPUTED-1 (tail check)** — The solver additionally evaluates heap size 8 and asserts that each player's win bit is identical at 7 and 8 at every evaluated nonterminal. Terminal winners are fixed for every heap size.

**READ · PROVED (why the tail check suffices)** — Induct on the finite pawn tree. If each pawn child's outcomes are constant from heap 7 onward, each pawn move has the same result at heap 8 and at every larger heap. Once heap 8 repeats heap 7 for both players, adding 8 as a smaller-heap option supplies no new losing reply. Induction on heap size now repeats that outcome forever. A side whose pawn search stops early already has a winning pawn move for each tested heap, including one that wins throughout the tail. Thus a further P cannot first appear above the tested range.

**RUN · COMPUTED-1 (reproduce)** — From the project root, the following commands produce every number in the tables and the split audit. In `census.txt` the fields are ranks, board, roots, counts for `*0` through `*7`, and minimum pawn counts for `*2` and `*3` (zero means absent). The sandbox declined the priority change, and scans ran serially.

```sh
set -e
out=delegate/out/T80
cc -std=c11 -O2 -Wall -Wextra -pedantic "$out/check.c" -o "$out/check"
nice -n 15 "$out/check" examples
{
  for r in 5 6; do
    for b in F3 F4 C3 C4 C5; do nice -n 15 "$out/check" "$b" "$r"; done
  done
  for b in F3 C3; do nice -n 15 "$out/check" "$b" 7; done
} > "$out/census.txt"
nice -n 15 "$out/check" splits > "$out/splits.txt"
PYTHONPATH=. .venv/bin/python "$out/compare.py"
```
