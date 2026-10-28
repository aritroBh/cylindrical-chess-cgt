# Blind proof of Proposition 2.11

## Claim and model

**PROVED.** Assume (H1)–(H5), with White as Left and Black as Right, in the frozen promotion model (F). Let (p) be the beneficiary β's pawn from the statement, and let ω be the other side. I show that β has a strategy that pushes (p) on every turn and wins. A legal king move loses immediately for its maker; a promotion wins immediately for its maker; a side with no legal move draws unless it is in check, when it loses; and infinite play draws.

Passed status uses H1's en-passant-aware definition (`PASSED_RESPECTS_EP = True`); the older textbook test is not used.

Write (r=ρ(p)) for the current rank of (p) measured from β's side, and (r_0) for its rank in (y). A pawn of ω advances toward smaller ρ. A pawn of β advances toward larger ρ.

## Lemma: the pushing pawn cannot be stopped

Suppose β pushes only (p). First consider an ordinary capture of (p). At (y), (H1)'s passed-pawn condition excludes every ω pawn on an adjacent file strictly ahead of (p), which is the only square from which it can capture (p). After β has made its first push, (p)'s rank is at least (r_0+1). On each later ω turn, a pawn already on an adjacent file can only move toward smaller ρ; a pawn newly arriving on an adjacent file by an ordinary capture of a different β pawn lands on that stationary pawn's square, whose rank is at most (r_0+1) by (H4), hence not ahead of (p). It cannot arrive on an adjacent file by a non-capturing move from another file. The only pre-push exception is (s=ω): on its first move ω could capture a β pawn on an adjacent file at rank (r_0+1), but cannot capture (p) on that same move because (H1) says no capturer is there at (y). β then pushes (p) to rank at least (r_0+1) before ω can move again. If (s=β), the first push is already made before ω moves. Thus (p) is never capturable by an ordinary pawn capture.

For en passant against (p), (H1) explicitly rules out a capture at (y). Later, (p) can create an en-passant right only on its first push, if it double-steps from β's start rank. To capture that double-step en passant, an ω pawn would have to be beside the destination square at the same rank (r_0+2). Existing adjacent-file ω pawns at that rank are excluded by the passed-pawn clause of (H1); any pawn newly arriving there by a normal capture lands at rank at most (r_0+1) by (H4), and an en-passant arrival lands still lower. So there is no en-passant capturer. A single push creates no en-passant right. Any right already offered at (y) expires after the first move, and (H1) rules out taking (p) with it. An en-passant capture of a different β pawn can only be offered to ω on its first move when (s=ω). If its victim is on an adjacent file, (H4) puts that pawn at rank at most (r_0+1), and the en-passant landing square is one rank lower; if the victim is on (p)'s file, it is behind (p) by (H1), and the landing square is lower still. Thus this exceptional capture cannot stage an ω pawn ahead of (p) either.

Now the path. Initially every square of (p)'s forward file is empty by (H1). An ω pawn cannot enter a square ahead of (p) on that file by a straight push: a push does not change files, and on (p)'s file ω moves toward smaller ρ. A normal capture onto that file must land on a pawn there; there is no β pawn on any forward square by (H1), and the only β pawn that later occupies the file ahead is (p), which has just been shown uncapturable. For en passant to land on (p)'s file, its victim must be a β pawn on that file. The only such available victim other than (p) is behind (p), by (H1), and en passant lands one rank lower still; (p) itself cannot be taken en passant by the preceding argument. An initial en-passant right is available only on ω's first move when (s=ω); later rights created by an ω double-step expire on β's intervening push, and a β double-step creates only a right to capture (p), already excluded. Thus no ω pawn can put a blocker on the path. The kings never occupy new squares on a play in which ω avoids its losing king move.

Consequently (p)'s next square is always empty on β's turn, so its prescribed push is available. This also proves that (p) reaches its promotion square after exactly

\[
d=H-r_0-[r_0=2]
\]

pushes: it moves two ranks on the first push exactly when (r_0=2), and one rank on every other push.

## Lemma: β's prescribed moves are legal

There are only kings and pawns, so a king can be in check only from an opposing pawn (the kings are nonadjacent in the legal initial position and do not move). By (H2), no pawn initially occupies a file adjacent to β's king. This remains true: (p)'s file is not adjacent to that king; the other β pawns do not move; and an ω pawn cannot move or capture into one of the empty adjacent files without landing on a β pawn there. It follows that β's king is never in check. Its pawn push does not move the king and is not otherwise prohibited by check. Together with the previous lemma, every prescribed push is a legal move.

## Lemma: ω cannot be stalemated

By (H3), the ω king has a neighboring square (t) at least king-distance two from β's king, with no pawn on (t)'s file or an adjacent file. That whole three-file neighborhood stays empty. No β pawn starts there; (p)'s file is outside it and (p) only moves on that file; other β pawns are stationary. An ω pawn cannot enter the neighborhood by pushing, and cannot capture onto one of its files because that would require a β pawn on the destination file. Thus (t) remains empty and unattacked by pawns. The kings stay fixed on every play where ω avoids moving its king, so moving its king to (t) is always legal. This holds even if ω is in check, since (t) is not attacked and is not adjacent to β's king.

In (F), that legal king move loses immediately for ω. It is therefore a legal move that prevents a no-move terminal (including stalemate) from being reached; if ω chooses it, β wins. This is the only use of (H3).

## Lemma: promotion timing defeats every pawn line

The (d) pushes promote (p). If β is to move at (y), ω gets (e=d-1) moves before the promoting push. If ω is to move, it gets (e=d) moves before that push. These are exactly the two cases in the definition of (e).

Consider any play in which ω does not move its king. Its pawn moves are also available in the ω-only game G_\omega(y;p): deleting p can only remove a blocker, while the other β pawns and both kings stay in the same places. An initial en-passant move is available only if it is offered at y and ω moves first, exactly as specified in G_\omega. A right created by an ω double-step expires on β's intervening push. A right created by β's double-step can only capture p, which the preceding lemma rules out. Thus every en-passant move that ω can actually use is represented in G_\omega. Legal-check restrictions in the real game can only remove ω pawn moves; they cannot create an earlier promotion than in this more permissive pawn-only comparison.

By definition, μω is the earliest promotion by any ω pawn along any such line, with captures allowed. (H5) gives μω ≥ (e+1), so no ω pawn can promote in the (e) moves available before (p)'s promotion. If ω instead moves its king, β wins immediately. Once β's (d)-th push promotes (p), β wins immediately. Thus no play against the stated strategy can reach an ω win or a draw first.

## Conclusion and hypothesis use

The invariant gives β a legal push on each of its turns; (H3) prevents stalemate while guaranteeing that a king move by ω is available but losing; and (H5) ensures ω cannot promote before (p). Therefore β wins by pushing (p) on every turn.

Each hypothesis has a distinct role in this proof: (H1) supplies the initially clear path, the initial passed-pawn condition, and the initial en-passant exclusion; (H2) keeps β out of check; (H3) supplies ω's legal king move; (H4) prevents a capture of another β pawn from staging an ω pawn ahead of (p); and (H5) supplies the promotion-time bound. I do not claim any of these hypotheses is unnecessary.
