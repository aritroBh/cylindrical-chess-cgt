# K72 review (coordinator, 2026-11-26)

Question: do the five seven-man groups that are exact over groups in chess keep the results of ω, in the
promotion game P, beside real pawns on a separated file of the same 8×8 board?

Investigator: `findings.txt`. Referee (K74, independent, own solver p74 written from the rules):
`verify/VERIFY.md`. The note's paragraph after Proposition 4.25 is the referee's text (`verify/EDITS.md`).

| Statement | Label |
|---|---|
| The table of agree/fail counts for 11 (group, file) pairs, contexts of at most 2 + 2 pawns on one file (283 per pair, 8 positions each; 24,904 positions) | CHECKED-2 (three programs: pk, ref3m, p74; 0 disagreements) |
| The prediction r(ω ⊞ X) at the roots, r(X) at the q's | three predictors agree; it is what Lemma 4.15 and Corollary 4.17 give |
| C125_10 on file h agrees in all 283 contexts of at most 2 + 2 pawns | CHECKED-2 |
| C125_10 on file h, all 729 placements of pawns on h2–h7: 726 agree, 3 fail (smallest Ph3, Ph4, Ph5, Ph6, ph7) | the 3 failures CHECKED-2 (p74, pk); the 726 agreements COMPUTED-1 (p74) |
| The other four groups fail on every separated file, already with 1 + 1 pawns | CHECKED-2 |
| Every failing context of at most 2 + 2 pawns has pawns of both colours on the file | CHECKED-2 (recount) |
| Mechanisms (a king leaves and wins a context pawn; a context pawn takes a buffer square from a group king) | COMPUTED-1 labels read from single lines; the ten smallest cases replayed by the referee |

Corrections by the referee, all taken over: the investigator assigned each group to one failure kind, but two
pairs fail in both directions, and there is a third mechanism without a king raid (C125_05 beside Pf5, pf6:
the pawn f6 covers e5, the White king's road to b7). "Exactness in chess does not protect a group" is limited
to "in P, beside real pawns"; no chess was computed. The positive claim for C125_10 holds for contexts of at
most 2 + 2 pawns (by the referee's single program up to 3 + 3), not for every context on h.

No theorem is contradicted. Lemma 4.15 and Corollary 4.17 are about D-sums with an abstract D-game. The board
position is such a sum only while the kings stay on F_Z and nothing on the context file meets them; in every
failure that is what breaks ((V1)(a) of Theorem 1.14).

What it means for the paper. A real over group is a statement about the group's own files. Beside real pawns
it needs a separation hypothesis for the kings, not only for the pawns: distance ≥ 2 between files is not
enough. K75 screens all 48 groups for a rule in terms of king distances.

Process notes. Investigator: one input file copied outside its folder and deleted at once. Referee: one direct
run peaked at 1.27 GB for 20 s (it should have gone through the slot script; watchdog was on); it stopped its
own waiting chain (own recorded PIDs) after 1 h 40 min without a slot.
