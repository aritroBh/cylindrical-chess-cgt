# Blind proof of Proposition 2.10(a)

**PROVED.** At the start of the window let s be the side to move. If H ≥ 5 and a context pawn of s can promote on that turn in the relaxed position Q° of (L2), that pawn already qualifies as passed in Q under either test. Thus a context with no passer has μ_s ≥ 2, including μ_s = ∞. The same implication holds for a promotion in Q itself.

## Where the pawn must be

**PROVED.** Give each side relative ranks 1 through H, increasing in its direction of travel. A single push, ordinary capture or e.p. capture gains one rank. The only two-rank move starts on relative rank 2 and ends on 4. When H ≥ 5, a pawn promoting this turn must therefore already stand on relative rank H−1. The only rank strictly ahead is the back rank H. No pawn of either colour may stand there before promotion. In particular no enemy pawn stands ahead on the same file or either neighbouring file, including a neighbour across the seam. This is exactly the textbook passed test. It does not require that a promotion square be free of attacks by a king. The argument even covers a penultimate pawn whose promotion move would be illegal.

## Which side owns the live e.p. right

**PROVED.** A pawn vulnerable to e.p. must itself have made the immediately preceding double push. In the plain form s played m in Z and then its opponent played r in Z. Any earlier right expired. If r creates a right, the vulnerable pawn belongs to the opponent and is in Z. In the window form only the second conclusion about location changes. The immediately preceding move was still the opponent's move, even if it was a context double push. A live right belongs to s as *capturer*. No pawn of s is its victim. This is also sufficient under the pawn-only e.p. test, which checks for an adjacent enemy pawn without testing a king pin. If Q has no recorded right the exception plainly does not apply.

**PROVED.** On five ranks a double push to relative rank 4 *does* put its mover on the penultimate rank. That pawn can be vulnerable on the other player's turn. When its own next turn arrives, it has either been captured or the right has expired. Thus H = 5 suffices for the assertion about s. For H ≥ 6 the double-push destination and the penultimate rank are distinct even without the turn argument.

## The relaxed position and the time bound

**PROVED.** Deletion in Q° neither changes the rank of an s context pawn nor adds one. Apply the rank argument to a hypothetical first-move promotion in Q°, and evaluate the passed tests on its source pawn back in Q. A first king move cannot also promote a pawn. An off-group e.p. right is retained for the first move only. Taking it gains one rank and lands on the opponent's skipped square, relative rank H−2 for s, so cannot itself promote. Clearing a path by that capture, or by the king, would cost a move before promotion. A target in Z is discarded as Definition 2.6 requires. The hypothesis precludes a first-move promotion under either test, hence (L2) holds for T = 1. This proves the context clause alone. The local win and stalemate conditions have their own hypotheses.

## Legality and sharpness

**PROVED.** The proof needs interior pawn ranks, the stated move rules and a globally turn-consistent e.p. right. With a right present, chess legality means a double push by the *opponent* on the immediately preceding ply, with the corresponding victim and skipped square. The right expires on the next move anywhere on the board. The proof does not require reconstructing an opening history or requiring an adjacent capturer before recording a target. A component cannot retain an independent e.p. clock. For example on five ranks take White a4 c2, Black b4, White to move. If one improperly retains Black's opportunity to take a4 after a previous a2–a4, the e.p.-aware test suppresses a4. The other two pawns obstruct each other in the passed test. Yet a4–a5 promotes. This describes an invalid turn/right pair, not a chess-legal counterexample.

**PROVED.** On four ranks take White a2, Black b3, White to move, no right. Each pawn has the other strictly ahead on a neighbouring file. Neither is passed by either test, but a2–a4 promotes by double push through the empty a3 and leaves no e.p. right. The example works on a flat board and across ordinary adjacent files of a cylinder. Two pawns are minimal because a lone pawn is passed. For a full plain flat embedding take files a–e, F_Z = {d,e}, kings initially White e1 and Black e4. The legal Z-moves Kd1 and ...Kd4 leave the displayed context and White's promotion intact. The embedding witnesses failure of the context implication at four ranks without any need to assume (L1).

Reproduce the examples by applying the relative-rank and e.p. rules above to the stated squares. The exhaustive numerical check is separate from this proof.
