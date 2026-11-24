# K62 review

2026-11-24. Investigator and referee were separate Opus agents. The referee wrote its own program before reading
the investigator's code. AI work, no human re-derivation.

## Result

- **Theorem 4.20: PROVED.** For an exact over group with b boards, the ladder T_b decides whether it has the results
  of over (T_{b−1} in chess). The bound counts the boards on which a White pass can leave Black to move, not the
  states. It is attained.
- **Proposition 4.21: PROVED.** Every ladder length N occurs for some abstract exact over group.
- **Theorem 4.22: PROVED.** No finite set of finite D-games decides for every abstract exact over group: the group
  Λ_N passes every D-game with at most N positions and fails one with N + 1. So no single D-game, loopy or short,
  is a universal test.
- **Corollary 4.23: PROVED.** On one board size one ladder decides every king-and-pawn group.

This answers the open item "a test family that does not depend on the group": there is none that is finite, in the
abstract model; the countable family of ladders works.

## What the referee changed

- Scope of Theorem 4.22: it is about abstract groups. For king-and-pawn groups the question is open, and on one
  board size one ladder decides. The investigator's wording said "some exact over group".
- Definition 4.8 constrains promotions only at the states it names. Under that reading three boards already give
  N\* = 3 with e.p. rights (referee's example Λ³). The investigator's count max(4, N) holds under a stricter reading.
  The two readings differ only by e.p. promotions, which chess does not have.
- The case the investigator left open (four boards, every move changes the board, with e.p.) is settled by the
  referee's example Δ4, which uses two moves of one state to the same board; without that, it stays open.
- Wording of the chess remark and of one counting step in Theorem 4.22.

## Checked by program

Both programs agree on every construction and on the counts of small D-games that separate Λ_1 and Λ_2 (CHECKED-2).
Each ran 4,500 random exact toy groups against Theorem 4.20: 0 violations.

## Not done

- No exhaustive list of all four-position D-games against Λ_4 (random and restricted lists only).
- Two small board-count cases stay open (see `verify/VERIFY.md`).
- Nothing on real boards. Whether a real group needs a ladder longer than 2 is open; the 3 + 3 group of cyl:8×6
  needs exactly 2.
