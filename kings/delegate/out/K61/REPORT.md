# K61 — Blind proof report

## Five-line summary

- **A0 — PROVED.** Every specified q-state equals zero in results, and each root is bounded above by ω for either side to move.
- **A — PROVED.** The reverse root bound holds exactly when every bad Black move satisfies (C).
- **B — PROVED.** For each bad move, (C), winning Aux, winning every ladder, and winning one ladder of length N ≥ K are equivalent.
- **B3 — PROVED.** White winning T_K from both Black-turn roots is necessary and sufficient for universal agreement.
- **Recommended labels — PROVED for all four** with the ordinary e.p. permission rule. If absence of a right may enable moves, all four statements have **PROVED counterexamples**.

## Readings

R1 compares the White-turn bad-move successor with the Black-turn reference. R2 uses P stalemate only to classify the internal moves. All sums use no-move-loses. R3 forbids every elsewhere move while in check. R4 consumes the mover's right, grants a new one only on an internal double step, and treats the right as adding legal moves with ordinary moves retaining their effects. R5 orders the three ordinary outcomes L < D < W and uses the stipulated pass objective in Aux. R6 includes all finite D-games and every start. R7 uses abstract boards, both roots and all specified q-states.

## Rule audit

- **PROVED.** In a strategy transfer, the side replying elsewhere is out of check. A copied T-terminal ends the sum with its signed winner, and a promotion ends it for its maker.
- **PROVED.** A P winning strategy also wins beside an inert component. This implication uses the fact that a P win cannot end in stalemate. Removing an e.p. right at q can leave Black with no internal option.
- **PROVED.** After a pair of T moves the opponent may have lost a right that the simulated history still grants. Move inclusion makes every actual internal response legal in that history.
- **PROVED.** Finite rank descent handles internal delays. Infinite shadow play preserves avoidance, and an infinite play invisible from some point on to the ω shadow would give only finitely many Aux passes. These arguments cover loopy T and draws.
- **PROVED.** The ladder finite-win regions form a descending sequence on the K group states. At its fixed point, each simulated layer must finish or yield another White pass in finite time.

## Weakest step

**PROVED.** The delicate case is a Black move in T during the transfer from Aux. A White T reply leaves the Aux history at its old Black turn, possibly with an extra Black e.p. right. A shadow deletion of ω instead uses that Black move as the Aux freeze, supplying a finite internal win with White to move. The explicit examples show why the ordinary move-inclusion rule belongs in a formal statement of the abstract model.

The complete arguments and counterexamples are in [PROOF.md](PROOF.md). All results are deductive.
