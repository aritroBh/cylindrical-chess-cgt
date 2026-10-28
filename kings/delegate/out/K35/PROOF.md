# Independent proof of Theorem 2.11K

**Status: PROVED (conditional on the stated hypotheses).** This proof uses the frozen definitions in `blind_packet.md`, the adopted en-passant-aware meaning of “passed,” and ordinary legal chess moves for the real kings in P. It does not use the proof in LOOPY.

Let β be the side whose pawn is p, and measure ranks by ρ from β's side. Write q_j for p's square after its j-th push, with q_0 its initial square. The number of ω moves made by the time p is at q_j is n_j. In particular, an ω turn at which p is already at q_j occurs after n_j such moves, and before that turn ω's king has made at most n_j king moves. The prescribed line Π pushes p at each β turn, using its initial double step exactly when ρ(p)=2.

## 1. Pawns cannot capture or obstruct p

The e.p.-aware passed-pawn condition says that initially no ω pawn lies on p's file or either neighboring file strictly ahead of p, and that p is not presently vulnerable to en passant. Consider any later attempted ordinary pawn capture of p. Immediately before the capture, the capturing ω pawn would have to be on one of p's neighboring files at rank-coordinate ρ(p)+1: ω pawns capture one step toward smaller ρ. Such a pawn cannot arise from an initially behind pawn, whose ρ only decreases. Nor can a pawn initially ahead make the capture: the passed condition excludes one in these files, and ω pawns cannot move toward larger ρ. Thus no ω pawn can capture p.

An ω pawn can change files only by capturing a β pawn. For it to end up on p's file strictly ahead of p, its last such capture must be of a β pawn on a neighboring file at coordinate at least ρ(p)+2: the capture lands one rank nearer ω, hence still strictly ahead of p. H4 bounds every β pawn on either neighboring file by ρ(p)+1. No such last capture exists. A pawn on p's file at the same or a lower coordinate cannot block a forward push to a higher coordinate. Also, pawns cannot capture onto p's file by capturing p itself, as already shown. Therefore no ω pawn can occupy a future square of p's file or otherwise block a prescribed push.

For the initial double push, the skipped square and landing square are empty by H1. En passant against that double push would require an ω pawn on a neighboring file at the landing coordinate. H1's passed condition excludes any such pawn, since the landing coordinate is strictly ahead of p's initial coordinate. Later pushes are single steps and create no en-passant right. The separate e.p.-aware clause in H1 also rules out an en-passant capture of p already offered at y. Hence en passant never defeats Π.

## 2. ω's king cannot capture p or stop a push

Fix an ω turn with p at q_j. Before ω moves, its king has made n_j one-square moves from k_ω. The triangle inequality for king distance and (SQ) give

\[
d(k_\omega^{\rm current},q_j)\ \geq\ d(k_\omega,q_j)-n_j\ \geq 2.
\]

If s=β, the initial turn is not an ω turn with p at q_0 and (SQ) is not needed for j=0. For every later reply the displayed bound applies; if s=ω, it applies also at q_0. At the start of each ω turn the king is at least distance two from p, so its one move cannot capture p. After that move it has made n_{j+1} moves, and (SQ) at q_{j+1} gives distance at least two from the next landing square. Thus the β push that follows cannot be blocked by the king. The double-push case is covered by the separate skipped-square argument below.

More explicitly for a double push, the skipped square is empty initially by H1. If ω moves its king to that square after p has landed beyond it, the skipped square is behind p and is not on any later push path. If ω is to move before the double push, (SQ) at q_0 puts its king at distance at least two, so it cannot stand on the skipped square and invalidate the double move. For every later single push, (SQ) at the next landing square, applied after ω's reply (when the king has made n_{j+1} moves), gives distance at least two from q_{j+1}. Thus the king cannot capture p or occupy a landing square. The pawn argument in section 1 excludes pawn occupation of those squares.

## 3. β remains safe and its pushes are legal

The kings are not adjacent initially. In P every legal ω king move must leave the kings nonadjacent, so it cannot put β in check. A pawn checks a king only from an adjacent file. H2 says that no pawn of either colour is on a file adjacent to β's king's file; in particular no ω pawn attacks the stationary β king. This remains true: a pawn can change files only by capturing onto the square of a β pawn, and all β pawns on those adjacent files are absent at y and stay fixed (or are removed). Thus no ω pawn can enter one of those files. The king remains stationary, and no legal ω king move makes the kings adjacent. Consequently β is never in check.

Every push in Π is a legal pawn move. Its destination is on the board; for the first push, H1 clears the whole forward path, including both the skipped and landing squares if it is a double step. Later, section 1 and the king-distance bound keep the next square empty. A pawn push does not expose β's king to a king attack because ω's king cannot move adjacent to it in a legal position, nor to a pawn attack by H2. Thus the side-to-move king-safety condition is maintained after each push.

## 4. ω cannot promote first

Consider any play against Π before p promotes. A ω king move may capture any of β's other pawns, and that possibility must not be ignored: it is explicitly included in G^K_\omega. In that game ω may make a king step on each turn, subject to the specified king-square restrictions, as well as make its pawn moves and captures. It therefore allows at least the pawn routes and captures available to any actual play in which ω's king has not captured p. The variant that also excludes squares attacked by remaining β pawns is no more permissive and is expressly covered by the hypothesis.

If p's start coordinate is 2 and s=ω, the first move in G^K_\omega can include only the en-passant right offered at y, exactly as in P. H1 ensures this right cannot take p; after that first turn the right expires. In every other case, the initial pawn options agree with the stated game. Thus, if an actual ω pawn could promote within e of ω moves, its pawn sequence, including any captures of β's other pawns, would be a permitted sequence in G^K_\omega and would imply \(\mu^K_\omega(y;p)\le e\). This contradicts H5K. Therefore no ω pawn promotes before β's scheduled promotion. This reasoning allows ω's king to capture β's other pawns; the king is not assumed frozen.

The timing convention makes the count exact: if s=ω, there are d=e ω moves before p's d-th (promoting) push; if s=β, there are d-1=e ω moves before that push. H5K rules out promotion in those moves. On the final β turn, p's path remains clear by sections 1–3 and its promotion is immediate and wins P by definition.

## 5. ω always has a legal move or is mated

This is needed to exclude a stalemate draw along Π. If an ω turn before p promotes exists, then e≥1. On that turn let x be ω's king square. At most e-1 ω king moves have occurred: the last ω turn precedes the final promoting push, and the counts above are e (when ω starts) or e moves in total (when β starts), leaving at most e-1 moves before the last reply. Hence \(d(x,k_\omega)\le e-1\). By (H3K), there is a king-neighbor t of x that is at distance at least 2 from k_β, and with no pawn on t's file or either neighboring file. The square t is not occupied by a pawn, and it is not occupied by β's king. It is a legal king destination: it is not adjacent to β's king and no β pawn attacks it, since any pawn attack would have to come from a neighboring file. It may be occupied by ω's own piece only if that piece were the king at x; since t is a distinct neighbor, it is not. Therefore ω has a legal king move. In particular, ω is not stalemated. If e=0, there is no ω turn before the immediate promotion. (If instead ω has no legal move because it is in check, it is checkmated and P is already a β win.)

This proves (NS) from (H3K). Equivalently, the explicit NS hypothesis in the theorem is guaranteed on every ω turn of Π by H3K. The argument uses only the pawn-free file neighborhood, king distance, and the fact that the king's distance from its start grows by at most one per move.

## 6. Conclusion

Against every legal response to Π, β is never in check, p cannot be captured or blocked, ω cannot promote first, and ω is never stalemated. A checkmated ω loses immediately; otherwise play reaches p's clear promotion square, where β wins at once. Thus β wins P from (y,s) by Π.
