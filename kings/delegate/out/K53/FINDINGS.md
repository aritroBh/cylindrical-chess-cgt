# K53 comparison with Proposition 2.10(a)

## Five-line summary

- **PROVED.** Retain **PROVED after repair** for the side to move, in a chess-legal non-terminal context on H ≥ 5.
- **PROVED.** A penultimate pawn of the mover is passed under both tests, even on five ranks.
- **PROVED.** The bound is sharp. On four ranks White a2 can double-push to promotion past Black b3.
- **COMPUTED-1.** Across 145,444,720 context states on five through eight ranks, both tests had zero failures. On four ranks both had the same 1,492 failures.
- **COMPUTED-1.** For LOOPY's stronger-claim search on five ranks, requiring an empty double-push origin reduces 156 pairs to 120.

## Comparison of the arguments

**PROVED.** The blind argument starts with an alleged promotion in Q°, the position in which (L2) measures time. Its source pawn occupies the same square in Q, where the non-terminal hypothesis applies. LOOPY starts with the source pawn in the context and then discusses the king's help and e.p. separately. The direct Q° argument explains why deleting pieces cannot produce an exception. Both arguments use the global turn to settle the five-rank case.

| Step in LOOPY, in order | Finding |
|---|---|
| One move from promotion implies penultimate rank. | **SOUND · PROVED.** A two-rank push always ends on relative rank 4. H ≥ 5 excludes promotion by that push. Every remaining pawn move gains one rank. |
| No enemy pawn stands ahead, including on adjacent files. | **SOUND · PROVED.** All three possible files ahead lead to the last rank, where no unpromoted pawn may stand. Wrapping changes the file only. |
| The mover's pawn cannot have just double-stepped. | **SOUND · PROVED.** Before Y, a live right must come from the opponent's move. At ordinary Q the last move is the opponent's Z-reply r. At window Q it is the opponent's preceding move, possibly in the context. If there is no preceding move, there is no right. The identity of a particular application of Y and Q is unnecessary. |
| Passed under both tests, so the context would be terminal. Component-local rights can be stale. | **SOUND · PROVED.** No pawn ahead establishes the textbook result. The turn excludes vulnerability of this particular pawn under the e.p.-aware test. The invalid five-rank state in the blind proof shows exactly what breaks when a right survives a move elsewhere. |
| The king cannot accelerate this into a first-turn promotion. | **SOUND · PROVED.** A king capture and a pawn promotion are different moves. Relaxing the board in Q° still preserves the source pawn's rank. |
| Only context pawns enter (L2). | **SOUND · PROVED.** Definition 2.6 counts these explicitly. A legal promotion by an s Z-pawn is a defender win in the local game, so (L1) handles that possibility. The case references concerning individual Z-pawns are illustrations and play no role in this deduction. |
| An off-group e.p. right in Q° cannot promote on this turn. | **SOUND · PROVED.** For s the skipped square is on relative rank H−2, strictly short of promotion. A later promotion after using this right would be at least the second move. |
| Stronger statement about either colour fails on five ranks. | **SOUND · PROVED.** In White a2 / Black a3 b2 after ...b4–b2, a2 and a3 obstruct each other, and a2 can take b2 e.p. The b2 pawn would queen by a single push on a Black turn. White has the actual turn. This refutes the geometric either-colour claim for the e.p.-aware test. |
| Numerical evidence of 156 versus 120 such pairs. | **SOUND as two different searches · COMPUTED-1.** On flat four-file boards with at most two pawns per side, an empty skipped square and both turns, five ranks give 156 with the origin unchecked, 120 with the origin empty. The 36 extra pairs cannot follow the alleged double push. Both searches give zero on six, seven and eight ranks. |
| Six ranks suffice for the stronger statement. | **SOUND · PROVED.** A just-double-stepped pawn stands on relative rank 4, at least two single steps short. Any penultimate pawn of either colour is therefore textbook-passed and immune to e.p. |
| Four ranks allow a non-passed one-move promotion. | **SOUND · PROVED.** White a2 / Black b3, White to move, is a minimal two-pawn witness for both tests. |
| Decisive punishment in P follows under (L1) and (L3). | **SOUND as an application of Theorem 2.7 · PROVED conditional on that theorem.** The argument supplies its missing hypothesis (L2). At T = 1 only s's turn at Q needs the stalemate check. This audit addresses the application and takes Theorem 2.7 as cited. |

## Test counts and recommendation

| Ranks | E.p. field | Context states | No passer, textbook | No passer, e.p.-aware | Failed implication, textbook / aware |
|---|---|---:|---:|---:|---:|
| 5–8 | none | 109,239,448 | 8,690,872 | 8,690,872 | 0 / 0 |
| 5–8 | fresh target | 36,205,272 | 3,558,028 | 3,736,860 | 0 / 0 |
| 4 | none | 68,644 | 1,956 | 1,956 | 1,492 / 1,492 |
| 4 | fresh target | 0 | 0 | 0 | 0 / 0 |

**COMPUTED-1.** Counts include both turns, both topologies and widths three through five. Every failed implication is in [failures.csv](failures.csv). **CHECKED-2.** The tests classify 178,832 states differently as terminal or non-terminal. Each becomes non-terminal under the e.p.-aware test and none admits a one-move promotion by the mover. The independent difference enumeration agrees with the main enumeration's difference counts in every size, topology and e.p. stratum. All such states are in [test_differences.csv](test_differences.csv).

**PROVED.** Recommended label for Proposition 2.10(a) is **PROVED after repair**. Keep “side to move,” “chess-legal,” and “H ≥ 5” explicit. For the stronger example count, quote 120 as the legal count and identify 156 as the relaxed-origin diagnostic. Exact commands for the table, witnesses and comparison search are in [REPORT.md](REPORT.md#reproduction).
