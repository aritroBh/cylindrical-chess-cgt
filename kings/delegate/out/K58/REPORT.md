## Five-line summary

- **PROVED.** Proposition 4.14 holds for all finite D-games. White can answer Black's first pass by freezing and return the same T turn to Black.
- **PROVED.** Lemma 4.15 holds under (B1) at both roots and every q, for either starter and all three results.
- **PROVED in an abstract model.** Without (B1), an exact shuttle graph beside star gives L where over gives W. Realizability of this witness in chess is open.
- **PROVED.** White's non-freezes and the moves of either side at q need only the stated P-alone loss certificates.
- **PROVED** is the recommended label for both statements as written under R1–R10.

## Readings

**PROVED under these readings.** R1 uses rank reflection and colour exchange, preserving pawn attacks and king distances. R2 uses two unchecked, flag-free placements, each with both starters. R3 uses finite forced wins in P alone, with stalemate drawn. R4 compares q and 0 by their results in every context, and uses the freeze flag only for Black. R5 forbids every outside move while in check. R6 clears the holder's e.p. right on an outside move. R7 gives Black one optional, check-restricted outside move. R8 permits every finite T and every start, including loops, empties, and suicide terminals. R9 allows all board sizes in the brief on either topology. R10 includes both q starts independently of reachability from a root.

## Chess rules and results

- **PROVED.** K1 and K2 keep the roots unchecked. Legality with both starters keeps q unchecked. After a departure the board strategy answers checks. Checkmate closes every outside option.
- **PROVED.** After a double step the responder receives the actual flag, including at q and at the start of (B1). Intervening outside replies can erase a waiting opponent's e.p. capture. Each remaining board move still has its recorded successor.
- **PROVED.** Solo winning certificates cannot end in stalemate, which draws in P. In the sum, play may continue outside a locally stuck board. A player with no legal move anywhere loses.
- **PROVED.** Promotion ends the sum for the promoter. Each T terminal ends it for the indicated side, including a suicide by its mover.
- **PROVED.** After a departure every opposing move advances a recorded play. A winning record cannot advance infinitely often. A draw is preserved by transferring a nonlosing strategy for each side.

## Weakest step

**PROVED.** After a Black non-shuttle, White tracks both the winning (B1) board play and the model play in ω ⊞ T. If Black moves in T and White's model reply is the freeze, White must make a real board move. That Black move can be charged to −1 exactly then. The model still has its freeze, so the reservoir is unspent. The actual outside move certifies Black was free of check. Charging it clears any old Black flag and supplies the correct White board turn.

## Assessment of the hypotheses

- **(a) PROVED in the abstract model.** At the witness's bad departure x, White wins alone by moving to the mutual zugzwang q. With −1 Black can pass at q and win. With Black starting beside star the departure wins for Black at either root, whereas White wins beside the model ω. This settles the abstract version permitted in the brief. The example supplies no board placement.
- **(b) PROVED.** After a White non-freeze Black has a solo board win. Proposition 4.14 transfers Black's outside guarantee from ω ⊞ T to T with White on turn. Black can now answer in whichever component White plays.
- **(c) PROVED.** At q the outside strategy already belongs to T. It combines directly with the responder's solo board win after either player's deviation, including when an optional Black e.p. capture has expired.
- **(d) PROVED.** Substituting the empty component for −1 fails in (a). Literal identity with 0 also fails, since q has legal moves for both players. Removing both Black non-shuttle options from the example makes (B1) vacuous and preserves this distinction. The stated single-tempo test and contextual interpretation give the proved conclusions.

**PROVED.** Full strategies, move lists, and terminal lines are in [PROOF.md](PROOF.md). **COMPUTED-1.** The finite witness's result pairs can be reproduced from the project root with the following command.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python kings/delegate/out/K58/check.py
```
