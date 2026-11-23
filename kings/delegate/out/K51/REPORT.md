# K51 independent check of Theorem 3.4

## Five-line summary

- **PROVED.** All three outcome rules hold for short D-games under the stated normal-play and decisive-terminal conventions.
- **PROVED.** With both sides able to pass, neither suffers zugzwang. Every state is drawn when G has no decisive options.
- **PROVED.** With only one side able to pass, every play is finite and the side that can pass never suffers zugzwang.
- **CHECKED-2.** Two implementations agreed on all 22,522,464 position, turn, and reservoir comparisons across 763,440 labelled games.
- **PROVED.** Keep the theorem's label. LOOPY needs one sentence corrected because a pass can preserve a forced win.

## The correction

**PROVED.** In (a), replace “So Left's winning moves are always G-moves” with “Whenever Left wins on its turn, some winning G-move exists.” At the single position with L(x) = {⊕} and R(x) empty, White may pass, wait for Black's forced pass, and then win by taking ⊕. The first pass wins under optimal continuation. Passing forever would draw. LOOPY's preceding argument correctly shows that a pass cannot first bring a state into the winning attractor.

The [blind proof](PROOF.md) was saved before the computational run and before reading LOOPY's proof. The [step audit](FINDINGS.md) gives the verdict for each part of that proof.

## Scope and reproduction

**CHECKED-2.** The [checker](check.py) tests both turns of every ordinary position in each of the three sums, including positions unreachable from label 0 in the unrestricted family. One solver uses only Definition 1.2's finite-win attractors on the explicit sum graph. Its empty existential and universal implement normal play. The other solver uses only the theorem's predicates, evaluated in reverse label order. Each mismatch would print the full option lists, reservoir, position, turn, actual result, and predicted result. The [run output](counts.txt) records zero disagreements in every size and gives W/L/D counts for each reservoir.

**PROVED (enumeration scope).** For n = 1, 2, 3, include every pair of option sets at every position with edges to later labels or either decisive terminal. Every short D-game of these sizes admits such a labelling. This gives 2^(n(n+3)) labelled games because every admissible edge may be included independently for each mover. For n = 4, 5, 6, enumerate the family in which each vertex j > 0 has one earlier parent, and the edge is available to Left, Right, or both. Only the final vertex may have terminal options, with an arbitrary subset of {⊕, ⊖} for each side. The number in this family is (n−1)! × 3^(n−1) × 16. These larger runs cover branching trees within this family. The universal result follows from the proof.

**CHECKED-2.** Per-size counts are in [FINDINGS.md](FINDINGS.md). From the project root the first command recomputes the per-size outcome and disagreement counts, and the second totals the games, comparisons, and disagreements in the saved run.

~~~sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K51/check.py
awk '{g+=$2; c+=$3; m+=$4} END {print g,c,m}' kings/delegate/out/K51/counts.txt
~~~
