# K53 — One-move context promotions

## Five-line summary

- **PROVED.** Proposition 2.10(a) holds on flat and cylindrical boards for H ≥ 5 under both passed-pawn tests. Retain **PROVED after repair**.
- **PROVED.** On five ranks a double push can reach the penultimate rank, but only the opponent of the side to move can own the vulnerable pawn.
- **PROVED.** On four ranks White a2 / Black b3 has no passer, yet White promotes by a2–a4. Two pawns suffice and one cannot.
- **COMPUTED-1.** The exhaustive check found zero failures in 145,444,720 states on five through eight ranks, and 1,492 failures in 68,644 four-rank states under each test.
- **CHECKED-2.** The two enumerators agree on the 178,832 additional non-terminal states admitted by the e.p.-aware test, including the count for each board and e.p. status.

## Proof and audit

**PROVED.** A promotion on the first move in Q° would require a context pawn on its penultimate rank in Q. Every square ahead is on the last rank, where no enemy pawn can stand. Nor can the mover's pawn be taken e.p. under a valid global right. An e.p. capture by the mover lands short of promotion. Thus a non-terminal context has μ_s ≥ 2, exactly (L2) for T = 1. The decisive-punishment application in P also requires (L1) and (L3). The [blind proof](PROOF.md) was written before consulting LOOPY. The [step-by-step comparison](FINDINGS.md) found the proof of (a) sound.

## Enumeration

**COMPUTED-1.** Each state specifies the dimensions, topology, disjoint white and black pawn sets on interior ranks, side to move and e.p. target or absence. Each colour has zero through three pawns. A target requires an opponent pawn at the double-push destination and empty origin and skipped squares. Recording an inert target is allowed. A double push that promotes leaves no target. A state with no target is counted once, whether e.p. was disabled or no right was carried. A state with several possible last pushes is counted once per distinct target.

**PROVED (coverage).** These are pawn contexts. The count omits kings, Z, and full game histories. It covers every projection of a legal position, allowing all locally consistent pawn placements without requiring an embedding or reachability from a starting array. Removing kings for this one-move test can permit extra pushes through an otherwise occupied square. Before promotion there are no officers to capture and kings are never capturable. Thus every legal context promotion is included. The four-rank minimal witness also has a legal king-group embedding in the blind proof.

**COMPUTED-1.** For each White subset, [check.py](check.py) evaluates all Black subsets in parallel, one bit per subset. It tests passedness and one-move promotion separately. Rank reflection with colour exchange is a bijection to Black-to-move states preserving both predicates and the target. Counts include both turns, and witness files expand the bijection explicitly. Combinatorial assertions independently check the total number of assignments with and without a target for each board.

| Ranks | States | States with mover promotion | Non-terminal, textbook | Non-terminal, e.p.-aware | Failures under each test |
|---|---:|---:|---:|---:|---:|
| 5–8 | 145,444,720 | 62,973,384 | 12,248,900 | 12,427,732 | 0 |
| 4 | 68,644 | 65,680 | 1,956 | 1,956 | 1,492 |

**COMPUTED-1.** [counts.csv](counts.csv) gives every stratum and separate failure counts for the two tests. [failures.csv](failures.csv) gives every state satisfying “no pawn is passed” and “the mover can promote,” with both test flags. **CHECKED-2.** [test_differences.csv](test_differences.csv) lists every disagreement on non-terminality. Each has a fresh target and exactly one textbook passer, the opponent pawn that can be taken e.p. [compare.py](compare.py) enumerates these directly from the vulnerable pawn and checks the count against the difference of the main totals in each stratum.

**COMPUTED-1.** The separate either-colour search in LOOPY used a smaller domain, flat four-file boards with at most two pawns per side. On five ranks the reproduced count is 120 with a legal double-push origin, or 156 if the origin is allowed to be occupied. Both versions give zero on six through eight ranks. This five-rank exception concerns the pawn of the player who just moved.

## Reproduction

Run from the project root. The first command regenerates the complete stratified counts. The second prints the two totals rows above and the stronger-claim comparison. The third groups the counts by height range and target presence for the table in FINDINGS.

```sh
d=kings/delegate/out/K53
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
.venv/bin/python "$d/check.py" | diff "$d/counts.csv" -
.venv/bin/python "$d/compare.py"
awk -F, 'NR>1 {k=($2==4?"4":"5-8")" "$4; groups[k]=1; for(i=5;i<=10;i++) a[k,i]+=$i} END {for(k in groups) print k,a[k,5],a[k,6],a[k,7],a[k,8],a[k,9],a[k,10]}' "$d/counts.csv" | sort
```

To regenerate and compare every witness without overwriting the recorded files, run in the same shell. The two row counts exclude the CSV headers.

```sh
t=$(mktemp -d "$d/replay.XXXXXX")
.venv/bin/python "$d/check.py" --witnesses "$t/failures.csv" > "$t/counts.csv"
.venv/bin/python "$d/compare.py" --differences "$t/test_differences.csv"
for f in counts.csv failures.csv test_differences.csv; do cmp "$d/$f" "$t/$f" || exit 1; done
awk 'END {print NR-1}' "$t/failures.csv"
awk 'END {print NR-1}' "$t/test_differences.csv"
rm "$t/counts.csv" "$t/failures.csv" "$t/test_differences.csv"
rmdir "$t"
```
