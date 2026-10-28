### Theorem 2.11K (real-king square rule with a no-stalemate clause)

**Setting.** P with real kings: the first promotion wins at once for the promoter; a king moves one step, may capture a
pawn, is never adjacent to the other king and is never left in check; checkmate loses for the side to move; stalemate
draws; infinite play draws. Board: cylinder or flat, W files, H ≥ 5 ranks. Notation as in Proposition 2.11: a legal
position y before any promotion, side s to move, β, ω, a pawn p of β on file f, ρ, d = H − ρ(p) − [ρ(p) = 2],
e = d (s = ω) or d − 1 (s = β); Π is the strategy "β pushes p at every turn (the double step first if ρ(p) = 2)".
q_0, …, q_d are the squares of p before its first push and after each push (q_d the promotion square),
n_j = j (s = ω) or j − 1 (s = β).

**Hypotheses.**
- (H1), (H4): as in Proposition 2.11 (H1 includes: no pawn and no king of either colour on p's file ahead of p).
- (H2) shelter: no pawn of either colour stands on a file adjacent to the file of β's king.
- (H5K) μ^K_ω(y; p) ≥ e + 1, where μ^K_ω is μ_ω of Proposition 2.11 computed in the game G^K_ω: p is deleted, only ω
  moves, ω's pawns move as in chess (e.p. only as the first move and only if s = ω, only the right offered by y), and
  ω's king may make a king step to a square that is not occupied by an ω pawn, not occupied by β's king and not adjacent
  to it; it may capture a remaining β pawn; a king move counts as one ω move. (Variant G^K1_ω, also covered by the proof:
  in addition the king may not step onto a square attacked by a remaining β pawn.)
- (SQ) d(k_ω, q_j) ≥ n_j + 2 for j = 0, …, d (j = 0 only if s = ω); d is the king distance of the board.
- (NS) no stalemate along Π: in every play in which β follows Π and ω moves in any legal way, ω is never stalemated (not in
  check and without a legal move) at one of its turns. This is a finite search over ω's replies (at most e of them).
  Sufficient and purely geometric: (H3K) for every square x with d(x, k_ω) ≤ e − 1 (if e ≥ 1) there is a king-neighbour t of x with
  d(t, k_β) ≥ 2 such that no pawn of either colour stands on the file of t or on a file adjacent to it.

**Statement.** Under (H1), (H2), (H4), (H5K), (SQ), (NS), β wins P from (y, s) by Π.

*Proof.* Facts: (F1) a pawn changes file only by a capture and lands on the square of the captured pawn (e.p.: on the
file of the captured pawn); a king capture removes a pawn and creates none; so a pawn enters a file only by capturing a pawn
that stands on it, and a file without pawns never gets one. (F2) the first promotion ends P with a win for the promoter.
(F3) under Π β's king and β's other pawns never move; only p moves, along file f.

*Step 1, β's king is never attacked.* By (H2) and (F1) no pawn ever stands on a file adjacent to β's king: no ω pawn attacks
it; ω's king is never adjacent to it. So β is never in check and a push of p never exposes β's king.

*Step 2, pawn invariants.* Exactly as Step 2 of Proposition 2.11: (J_β) at every node with β to move every ω pawn in the strip
f − 1, f, f + 1 has ρ ≤ ρ_p + 1; (J_ω) at every node with ω to move every ω pawn in the strip has ρ ≤ ρ_p and p cannot be taken
e.p.; (I1) every square of file f ahead of p is free of pawns. The proof there uses only pawn moves, (H1), (H4), and (F1)–(F3);
ω's king captures remove β pawns (never p, Step 3) and add no pawn, so the invariants and their proof are unchanged
(upper bounds on the landing ranks of captures can only get smaller when β pawns disappear). Hence no ω pawn ever captures p
or enters a square ahead of p on file f.

*Step 3, ω's king neither captures p nor blocks it.* Let ω have made m moves; its king has moved at most m times, so
d(k, k_ω) ≤ m. After β's j-th push p stands on q_j and ω has made n_j moves; to capture p ω's king needs d(k, q_j) ≤ 1,
hence d(k_ω, q_j) ≤ n_j + 1, contradicting (SQ) (for j = 0, s = ω, no move has been made and d(k_ω, q_0) ≥ 2). Before
β's (j + 1)-th push ω has made n_{j+1} moves; its king can stand on q_{j+1} only if d(k_ω, q_{j+1}) ≤ n_{j+1}, again
contradicting (SQ); the square skipped by the double step is adjacent to q_1, so d(k_ω, skipped) ≥ n_1 + 1 > n_1. β's king is not on
the path by (H1) and never moves. With Step 2 every push of Π is legal (target empty, β not left in check by Step 1).

*Step 4, β is never stalemated and ω is never stalemated.* β always has the push of Step 3. ω has a legal move or is
checkmated by (NS) (checkmate is a win for β).

*Step 5, timing.* Every move of ω up to β's promoting push is a legal move of G^K_ω from y: a pawn move is legal in G_ω
(squares that are empty in the play are empty in G_ω, where p is deleted; captured pawns are β pawns other than p by Steps 2
and 3; the only e.p. capture is the first move offered by y); a king move goes to a square that is not an ω pawn, not β's king, not adjacent to it,
and captures only a β pawn other than p (Step 3), which G^K_ω allows (and the variant G^K1_ω too, because a real king
move avoids attacked squares). Before β's d-th push ω has made exactly e moves; (H5K) says no sequence of e moves of G^K_ω puts an
ω pawn on its last rank. So ω does not promote first. β's d-th push is legal and promotes: by (F2) β wins. ∎

*(H3K) implies (NS).* At an ω turn with m − 1 earlier ω moves (m ≤ e) its king stands on a square x with d(x, k_ω) ≤ m − 1 ≤ e − 1.
Take t as in (H3K). The three files around t hold no pawn, so by (F1) they never do: t is never occupied by a pawn and never
attacked by a pawn; t ≠ k_β and t is not adjacent to it, and t ≠ x. So the king step x → t is legal even if ω is in check, and ω is never stalemated. ∎

**What is and is not proved.** Not claimed: that (H1), (H2), (H4), (H5K), (SQ) without (NS) win (false, see the counterexamples),
that the conditions are necessary, or the chess form (A_Q, §1.2).
