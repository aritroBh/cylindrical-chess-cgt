## 5. How to read the certificates (what has to be checked by hand)

A *certificate* for "X wins at position x with X to move" is a list of entries. Each entry is a position with the side to
move (the winner X), the move X plays (**bold**), and the complete list of the replies of the opponent, each followed by
`->` another entry, or "X wins by <promotion>". There are three kinds of entry: N (replies lead to further entries), R (every
reply is answered by an immediate promotion), and leaves "X wins by p-p=Q". To check an entry by hand:
1. the position is the one reached by the entry that points to it;
2. X's move is legal (mover's king is not attacked afterwards);
3. the list of replies is complete (the bracket after each entry says why the other king moves and pawn moves are illegal:
   squares attacked by a named pawn, squares next to the other king, own pawn, a pawn blocked by a piece, a king in check);
4. each leaf is a legal promotion: the pawn is on its last-but-one rank, its square ahead is empty (or an enemy pawn stands diagonally
   ahead), and X's king is not attacked after the reply (no reply of the opponent attacks it, the only possible checks being those
   noted with `+` and answered in the entry).
The number `d` on an entry is the number of plies, counted from the entry and including X's move, after which X has promoted
(or mated) if the entry is played. Along every arrow `d` decreases by at least 2, so the entries form a finite acyclic
structure and the induction on `d` proves: **X, playing the listed moves, promotes first.** (Mate does not occur in any
certificate; stalemate cannot occur, because every list of replies is non-empty.)

