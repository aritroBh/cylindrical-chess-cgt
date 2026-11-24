# K64. Blind proof report

## Five-line summary

1. **PROVED** D1. Winning the ladder at N = |P(x) ∖ E(x)| is equivalent to (C) at the bad move.
2. **PROVED** D2–D3. The board bounds b and b − 1 are both attained under their respective hypotheses. Testing T_b with Black to move at both roots suffices.
3. **PROVED** E0–E1. Λ_N is exact over and agrees with ω beside every finite D-game with at most N positions.
4. **PROVED** E2. At root A with Black to move, Λ_N draws and ω wins for White beside C_N at N and T_{N+1} at u₀.
5. **PROVED** E3. Every finite family misses some failure of universal agreement, even when the family includes loopy games.

## Individual verdicts

| Statement | Recommended label | Basis |
|---|---|---|
| D1 | **PROVED** | The decreasing sets of useful pass boards stabilize after at most one strict removal per board outside E(x). |
| D2 | **PROVED** | A P win from x ends in a promotion or mate. Five-board examples attain 5 and 4, respectively. |
| D3 | **PROVED** | A Black-to-move root win covers every bad successor, and T_b is past every local cutoff or at it. |
| E0 | **PROVED** | q forces the mover to give the opponent a promotion. The sole bad move from A gives White a win via q. |
| E1 | **PROVED** | A forced win would need N + 1 distinct test positions to exhaust the chain. On a drawn line White can safely use e → p after the last chain move. |
| E2 | **PROVED** | In each witness Black can force the chain to e against continued test play, and White can secure a draw there. |
| E3 | **PROVED** | Choosing N at least the largest test size gives a failing group indistinguishable on the family from one with no bad moves. |

## Readings and weakest step

**PROVED under R1–R7 as stated.** Condition (C) uses White to move after the bad move and Black to move at ω. A pass hands Black a board with no right. Check forbids moving elsewhere. Rights add moves and lapse after use or play elsewhere. P-alone stalemate draws, while immobility in a sum loses. The result order is L < D < W. E1 covers every start and mover, cyclic tests and both terminal signs. The examples work even if all promotions on root and q boards are forbidden.

**PROVED.** The most delicate step is the draw at chain exhaustion in E1. The absence of a Black winning test terminal follows from the simulated Black turn immediately *before* the last pass. This makes e → p safe even against tests with decisive terminals.

**PROVED.** The complete derivations and exact move lists are in [PROOF.md](PROOF.md). All numbers follow symbolically. The reproduction command from the project root is `cat kings/delegate/out/K64/PROOF.md`.
