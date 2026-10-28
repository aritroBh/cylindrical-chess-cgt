# K20 review: king-vs-king fights inside a group (integrated 2026-10-27)

**Outcome: accepted with fixes.** `EDITS_FINAL.md` applies the referee's section 7. The integrator added three
scope fixes.

- **Finite king tempo exists.** flat:6x6 `Kc3 ka4 Pa2 pa3 Pc4 pc5` is +1 and its mirror is −1; `Kd3 ka4 …` is
  {1|0}. These are CHECKED-2 on battery values, from K20's solver, its Python implementation and the referee's
  `lk.cpp`. The value depends on the room the kings have: 0 in box(0), tis in box(1), +1 in box(2).
- **Proposition 4.3 is correctly scoped but its title misled.** It excludes finite tempo only against a frozen
  opponent. The title, the status row, the "n safe spare moves" paragraph and open question 3 now say so.
- **Labels.**
  - Counts the referee reproduced are CHECKED-2.
  - The B4553 separation counts for on and off (40 of 3,883; 6 of 130) and the claim "no pawn-bearing `*` root"
    outside flat:6x6 rest on K20 alone and are COMPUTED-1.
  - The kpsolve chess rows were not re-run and are COMPUTED-1.
- **Accepted judgment call.** The §4 sentence ("no other number in the searched games") is CHECKED-2. It is a
  statement about class counts, and the referee reproduced those exactly.
