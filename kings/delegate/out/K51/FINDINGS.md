# Comparison with LOOPY, Theorem 3.4

## Five-line summary

- **PROVED.** Theorem 3.4(a–c) holds as stated under Definitions 1.1–1.3 and 3.1.
- **PROVED.** LOOPY correctly excludes a pass as the move that first establishes a win in the least fixed point.
- **PROVED.** Its claim that every winning move is a G-move is false under the usual meaning of a move after which the mover can still force a win.
- **CHECKED-2.** Direct attractors and the theorem recursions agreed on all 22,522,464 comparisons across 763,440 labelled games.
- **PROVED.** Retain the theorem label and replace the one overstatement with “Whenever Left wins on its turn, some winning G-move exists.”

## Difference in proof route

**PROVED.** The blind proof gives the opponent a strategy against an attempted pass-only win. Return each pass until the prospective winner makes a genuine move. If none of those genuine moves can force a win, the prospective winner can at best pass forever and draw. LOOPY instead considers the first attractor stage at which a state becomes winning. Both arguments justify omitting the pass from the existential in (a). For (b) the blind proof also supplies an explicit decreasing pair (height in G, turn bit). This makes the computation order and the exclusion of infinite play immediate.

## Step audit

The verdicts below are **PROVED** mathematical assessments. A winning move means a legal first move from whose successor the mover can force a finite win.

| LOOPY step | Verdict | Reason |
|---|---|---|
| (a) Use (x, s), switch turns on a pass, and take the least fixed point. | SOUND | The reservoir coordinate is constant. Least fixed points implement finite forced wins, with infinite play drawn. |
| A first-stage White win on its own turn cannot be discovered by passing. | SOUND | For the pass to certify the win, the opposite-turn state would already have to be winning. Since Right could pass back, the original state would have to have been winning earlier still. |
| “So Left's winning moves are always G-moves.” | FALSE | Take X = {x}, L(x) = {⊕}, R(x) = ∅. With dud_D, White can pass, Black must pass back, and White takes ⊕. White's first pass is a winning move. This is minimal in ordinary positions and in genuine options: a starting state requires a position, and with zero genuine options the players can only draw. The preceding rank argument proves that some winning genuine move exists whenever White wins on its turn. |
| White wins with Right to move iff every Right option, including a pass, leads to a White win. | SOUND | Right chooses the successor. Right always has the pass. A forced continuation can be chosen after seeing that choice. |
| These clauses give the recursion in reverse topological order. | SOUND | The weaker, established existential about genuine White moves suffices. At each height compute Λ_L first, then Λ_R. Interchanging colors gives Ρ_R first, then Ρ_L. |
| If G has no terminals, Λ_L fails at sinks and everywhere. | SOUND | At a sink the existential is empty, so both White predicates fail. The same induction applies at higher positions and for Black. Neither color can win. |
| Remaining (a) consequences, stated before the proof. | SOUND | Outside both winning sets the result is D by Definition 1.2. The conjunct Λ_R ⇒ Λ_L and its Black analogue rule out zugzwang in either direction. Both sides have a pass, so only a decisive event can end play. “Otherwise drawn” applies when neither side can force its own decisive event. |
| (b) Only a White pass can leave x unchanged. Finitely many Black moves and alternation imply finiteness and determinacy. | SOUND | Each ordinary Black successor strictly lowers the height, and there can be at most one final decisive move. Alternation then bounds the whole play. Backward induction applies. |
| Black needs some winning genuine move on its turn. Every White option, including its pass, must win for Black on White's turn. | SOUND | These are the existential and universal choices of the two movers. At each height compute Ρ′_R before Ρ′_L. |
| Black with no option loses. | SOUND | The empty existential is false, exactly the normal-play result. White always has an option, so a Black win requires ⊖. |
| White never suffers zugzwang in (b). | SOUND | White can pass to any win it has with Black to move. Equivalently Ρ′_L implies Ρ′_R and there are no draws. |
| (c) follows by reflection. | SOUND | Swap mover, terminal winner, and outcome color. The one-sided reservoir also swaps, carrying the entire proof of (b) to (c). |

## Computational comparison

**CHECKED-2.** The direct solver expands passes on the turn-labelled graph and iterates separate least fixed points for White and Black. The other solver evaluates the theorem's recursions on the ordinary DAG. Both were written for this check. The enumeration is exhaustive for forward-labelled DAGs on one through three ordinary positions, with arbitrary terminal options for either mover. For four through six ordinary positions it covers the increasing rooted trees specified in REPORT.md. All positions and both starting turns were compared under each reservoir. No disagreements occurred.

| Ordinary positions | Games | Comparisons | Disagreements |
|---:|---:|---:|---:|
| 1 | 16 | 96 | 0 |
| 2 | 1,024 | 12,288 | 0 |
| 3 | 262,144 | 4,718,592 | 0 |
| 4 | 2,592 | 62,208 | 0 |
| 5 | 31,104 | 933,120 | 0 |
| 6 | 466,560 | 16,796,160 | 0 |
| **Total** | **763,440** | **22,522,464** | **0** |

From the project root, reproduce the rows and total with the following commands. The checker also emits every disagreement individually if one occurs.

~~~sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K51/check.py
awk '{g+=$2; c+=$3; m+=$4} END {print g,c,m}' kings/delegate/out/K51/counts.txt
~~~
