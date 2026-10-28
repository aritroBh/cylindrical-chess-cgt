# Integrator runs (2026-10-27): the two 4-pawn children c4-c3 at (b2, a4) and a3-a4 at (c3, b5)

- `c1.in` = `Kb2 Pa3 Pb4 ka4 pb3 pc3 w -` (after c4-c3 from Kb2/ka4, Black having moved).
- `c2.in` = `Kc3 Pa4 Pb4 kb5 pb3 pc4 b -` (after a3-a4 from Kc3/kb5, White having moved).
- kpsolve (`kings/kpsolve.c`, built privately): `kp --board flat:7x6 --cap 1 --threads 2`, giving bounds A B.
- ownchess (`kings/delegate/out/K27/verify/ownchess.cpp`, the K27 referee's chess solver, built privately):
  `ownchess 7 6 0` gives bound A and `ownchess 7 6 1` gives bound B.
- Each run went through `kings/delegate/heavy.sh` and `scripts/watch2.sh` (3 GB RSS cap, 20-minute wall cap), at nice 15.

| child | kpsolve A B | ownchess A | ownchess B |
|---|---|---|---|
| c1 | W L | W | L |
| c2 | W L | W | L |

Both children have bounds (W, L) at cap 1 in both solvers, so cap 1 does not settle these two deviations.
