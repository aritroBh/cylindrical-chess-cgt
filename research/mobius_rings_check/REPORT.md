# T77 · Independent check of Möbius pawn rings

## Five-line summary

1. **COMPUTED-1** · The first six Möbius witnesses have signature NNPN (star 2).
2. **COMPUTED-1** · The last two witnesses have signature NNNP (star 3).
3. **CHECKED-2** · Both cylinder controls have signature NNPN, matching the supplied benchmarks.
4. **COMPUTED-1** · The signatures use the e.p.-aware passed test and the count race rule.
5. **PROVED** · The three-file, three-pawn row has 190 labelled roots and 110 mirror classes.

## Witnesses recorded before opening the original report

**COMPUTED-1** for each Möbius row. The seam joins the last file to the first. Read each signature left to right at heap sizes 0, 1, 2 and 3.

| Files | Ring | Signature |
|---:|---|:---:|
| 3 | `W3B6 W2B7 W4B5` | NNPN |
| 5 | `B6 W3 B5 W2 W3B7` | NNPN |
| 4 | `B5 W23 W2B67 W4B7` | NNPN |
| 6 | `B4 W2 W2 W2B6 B5 W3B7` | NNPN |
| 7 | `B6 W2 W3 B6 B7 W3 W6B7` | NNPN |
| 8 | `B7 W3 W3 B6 W3 B6 B6 W2` | NNPN |
| 5 | `B67 W4 W2B6 W2B5 W5B7` | NNNP |
| 6 | `B7 W4 W23 B5 W3B7 W4B7` | NNNP |

## Exhaustive root counts recorded before comparison

| Files | Pawns | Labelled roots | Mirror classes | Labelled star 2 | Mirror star 2 | Labelled star 3 | Mirror star 3 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 3 | 190 | 110 | pending | pending | pending | pending |

**PROVED** for the two root counts by the hand count below. The two cylinder controls and eight named Möbius rings finished before the priority warning was inspected. Although invoked under `nice -n 10`, the solver inherited nice 5. Direct checks of the current process confirmed that macOS denies `setpriority` here. The exhaustive solver and the 300-position validation have not run. The original Möbius report remains unopened pending a complete blind table.

## Rules and reproduction

**PROVED** · Ranks 2 through 7 suffice throughout the search from these roots. Before the first pawn reaches an edge, a pawn on rank 7 heading up or rank 2 heading down has no possible enemy strictly ahead, including across the seam. Such a pawn cannot be the victim of a double step. The game therefore already ended. This also covers captures onto an edge because the seam reflects advancement and direction together.

**PROVED** · The recursion terminates. A pawn move strictly decreases the sum of all pawns' remaining rank distances, including a seam capture because it flips both coordinates and direction. A heap move preserves that sum and reduces the heap.

**COMPUTED-1** · The two cylinder control signatures in `signatures.txt` reproduce as the first two lines of the loop below. The ten-file control also matches the M₁₀ result in `research/c9_rings/REPORT.md`.

Each move acts on the whole board. The e.p. field records the square of the victim only when an enemy attacks the skipped square. Heap moves preserve this field. In a race the program considers the fastest passed pawn of each colour with a clear file ahead. Home-rank double steps save a move. The player who moves next wins ties, including when both distances are infinite. The position cache checks the complete state before reusing an answer.

Run the following from the project root. The loop reproduces both controls and the entire witness table, in order.

```sh
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
D=research/mobius_rings_check
TMPDIR="$PWD/$D" cc -O2 -std=c11 -Wall -Wextra -pedantic "$D/check.c" -o "$D/check"
while read -r shape n ring; do
  printf '%s\n' "$ring" | nice -n 10 "$D/check" "$shape" "$n" solve
done < "$D/examples.tsv"
```

## Hand count for three files and three pawns

**PROVED** · There are 190 labelled roots and 110 mirror classes in this row. Both colours must occur. With the minority pawn on the middle file, the two end pawns must each block it on an ordinary edge. For a white minority pawn on successive ranks, the numbers of choices for each black pawn are 5, 4, 3, 2, 1, 0. This gives 55 arrangements per minority colour. With a white minority pawn of rank r on an end file, the middle black pawn must stand above r. The far black pawn must see the white pawn strictly ahead across the seam, so its rank exceeds 9−r. The middle pawn already prevents White from being passed. This gives 20 arrangements for each end and minority colour. Colour reversal together with rank reflection gives the same counts for Black. Reflection fixes only middle-minority placements with identical end pawns, giving 30 fixed roots. The commands reproduce all the arithmetic.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python - <<'PY'
middle = sum(k*k for k in range(6))
end = sum((7-r)*(r-2) for r in range(2, 8))
raw = 2*middle + 4*end
fixed = 2*sum(range(6))
print(middle, end, raw, fixed, (raw+fixed)//2)
PY
```

## Census and cylinder validation commands

From the project root, after building the checker as above:

```sh
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
D=research/mobius_rings_check
nice -n 10 .venv/bin/python "$D/census.py"
nice -n 10 .venv/bin/python "$D/validate.py"
```

The census emits one row per completed material class in the requested order. Each solver invocation enforces its own 44-minute wall limit. Every file receives a nonempty subset of distinctly occupied ranks in increasing rank order, with both colours tried for each square. A file is rejected when both neighbours are known and it contains a passer. Every surviving labelled root contributes to the denominator. To classify hits, the solver evaluates one representative per left-right reflection and weights it by its orbit size for the labelled count. A side with an immediate terminal win wins for every heap size, excluding both target signatures. All other candidates are tested by exact minimax. The random cylinder check uses a three-file board, where every pair of files is adjacent and `cylcgt` cannot split the board into multiple components.

## Census and comparison (added by the main session, 2026-11-22)

Codex did not run the census (its sandbox could not lower the priority). The main session rebuilt `check` from
`check.c` and ran `nice -n 15 python3 census.py > census.out` outside the sandbox. Output: `census.out`.

| files | pawns | mirror classes | *2 (mirror classes) | `research/mobius_rings` orbits (mirror x colour swap) | its *2 orbits / colour-distinct |
|---|---|---|---|---|---|
| 3 | 3, 4, 5 | 110, 1557, 11530 | 0, 0, 0 | 55, 786, 5765 | 0 |
| 3 | 6 | 55455 | 1 | 27787 | 1 / 1 |
| 5 | 5 | 3326 | 0 | 1663 | 0 |
| 5 | 6 | 93979 | 2 | 47019 | 1 / 2 |
| 4 | 4, 5, 6, 7 | 487, 11284, 120964, 816444 | 0, 0, 0, 0 | 251, 5642, 60566, 408222 | 0 |
| 4 | 8 | 3956868 | 10 | 1978925 | 6 / 10 |
| 6 | 6, 7 | 22210, 710524 | 0, 0 | 11157, 355262 | 0 |
| 7 | 7 | 131226 | 0 | 65613 | 0 |
| 8 | 8 | 853722 | 1 | 427178 | 1 / 1 |

- Ring counts are consistent: with an odd number of pawns the mirror classes are exactly twice the orbits (the
  colour swap has no fixed class); with an even number they are slightly less than twice.
- *2 counts agree in every row (mirror classes = colour-distinct orbits). No *3 in any of these rows, in both.
- So the least number of pawns in a root ring *2 on the Moebius strip, 6, 8, 6, 8, 8, 8 for n = 3..8, is CHECKED-2:
  the upper bounds by the eight witnesses (both programs, plus `research/mobius/mob_pawns.py`), the lower bounds
  by both exhaustive scans. Not re-checked here: the counts above the least (n = 3 with 7..10 pawns, n = 4 with 9,
  n = 5 with 7..9, n = 6 with 8, 9, n = 7 with 8).
