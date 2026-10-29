# K40: hand proofs (K+P vs K in sums, cylinder boards)

Setting. x is a K+P vs K position on cyl:W×H (White king wk, White pawn p on ranks 2..H−1, Black king bk). In the P model of
LOOPY Definition 1.5, the first promotion ends the game as a White win (⊕). Kxp leaves K v K. T is a terminal-free test game,
with Left = White and Right = Black. x ⊞ T is the sum of Definition 1.3, with the chess rule that a side in check may not
move in T. Only Black can be in check (by the pawn). Two conventions for a side with no move at all in x ⊞ T:
- **(N) normal play:** that side loses (the D-semantics of LOOPY).
- **(C) chess:** checkmate loses, stalemate draws. This is P itself.

Infinite play is a draw in both. Every statement below is labelled. PROVED means a hand proof given here, written by one
agent (K40) and not refereed.

## Lemma 1 (K v K is dead). PROVED.
On cyl:W×H with W ≥ 3 and H ≥ 2, a king in K v K always has a legal move. Hence after Kxp no decisive event can occur
and neither side is ever without a move, so every continuation of x ⊞ T is a draw, under (N) and under (C).

*Proof.* Let the king x stand on (f, r) and the other king y be non-adjacent to it. x has the neighbours
A = (f−1, r), B = (f+1, r) (distinct for W ≥ 3) and V = (f, r′) with r′ = r ± 1 (one exists, H ≥ 2). If y covers neither
A nor B, x moves there. A square on rank r is covered by y only if y's rank is within 1 of r, so y's rank is r ± 1 or r
and y's file must be at cyclic distance ≥ 2 from f (else y is adjacent to x).
- W = 3: every file is within 1 of f, so no such y exists; A is free.
- W ≥ 5: a file within 1 of both f−1 and f+1 is f itself (f ± 2 is at distance min(3, W−3) ≥ 2 from f ∓ 1), which is
  excluded; so y covers at most one of A, B and the other is free.
- W = 4: y on file f+2 ≡ f−2 covers A and B, but V is at file distance 2 from y: free.
A free neighbour is a legal move, since K v K has no other attacker. ∎ (Brute force agrees: no K v K stalemate on any
cyl:W×H, 3 ≤ W ≤ 8, 4 ≤ H ≤ 8, COMPUTED.)

## Lemma 2 (White is never stalemated in K+P vs K when W ≠ 4). PROVED.
On cyl:W×H with W = 3 or W ≥ 5, White to move in a legal K+P vs K position always has a legal move.

*Proof.* Let wk = (f, r). Let A = (f−1, r) and B = (f+1, r): distinct, and empty unless the pawn is on one of them.
- **W ≥ 5.** The files within distance 1 of both f−1 and f+1 are exactly {f}: the file f+2 is at distance min(3, W−3) ≥ 2
  from f−1, and symmetrically for f−2. A Black king on file f covers A or B only if its rank is within 1 of r. It is then
  adjacent to wk, which is illegal. So bk covers at most one of A, B.
  - If neither is occupied by the pawn, one of them is a legal king move.
  - Otherwise the pawn is on one of them, say B, and bk covers A. White is stalemated only if the pawn is also blocked.
    The square (f+1, r+1) then holds bk, since wk is on (f, r). But (f+1, r+1) is adjacent to (f, r): illegal. The case
    with the pawn on A is the mirror image.
- **W = 3.** Every file is within 1 of f, so a non-adjacent bk has rank distance ≥ 2 from r and covers neither A nor B.
  The pawn occupies at most one of them, so the other is a move. ∎

## Corollary 3 (Black never wins). PROVED.
For every terminal-free T, the result of x ⊞ T is W or D:
- under (C), on every cylinder;
- under (N), on cyl:W×H with W ≠ 4.

*Proof.* Black has no decisive event of its own in x (Lemma 1: Kxp leads to a draw). So Black can win only by leaving
White without a move. Under (C) that is a stalemate, which draws. Under (N), White always has a king move by Lemma 2. ∎
(On cyl:4×H under (N), White can be stalemated in front of its own pawn, e.g. `Ka8 Pa7 kc7`. K40 finds 28 Black wins on
cyl:4×6 and on cyl:4×8, COMPUTED.)

So no K+P vs K position equals a loopy game with a Right win in its signature: not {on | 0}, not a negative number, not
off (off ⊞ 0 is a Right win). This answers part of the Gafni comparison by hand.

## Proposition 4 (the dud test does not see stalemate; the sandwich). PROVED.
(a) Under both conventions, x ⊞ dud has the same result. (b) Under (N), White wins x ⊞ dud ⇒ White wins x ⊞ T for every
terminal-free T. So the decisive class "W against every test" is exactly P_L(x) = W(x ⊞ dud) = W(x ⊞ off) of LOOPY
Theorem 3.11.

*Proof.*
- (a) In x ⊞ dud, White always has the pass. Black has it unless Black is in check, and then a Black with no king move
  is checkmated. So no position of x ⊞ dud is without moves except checkmate, which both conventions score the same way.
- (b) This is Theorem 3.11 with K = x and S = T. Its proof needs one remark, because K40's sum forbids a T-move in check.
  - In step (1), Right's real options in x ⊞ T are mapped to virtual options in x ⊞ off. A real T-move by Right is
    possible only when Black is not in check, and then the virtual pass ω → ω is also legal. Real king moves are virtual
    king moves.
  - In step (2), Left (White) is never in check, so her S-moves can always be replaced by the pass in `on`.
  - In step (3), Right's pass back from (k, ω, R) is available, because Black is not in check at (k, R). Otherwise he was
    in check at (k, L) with White to move, which is not a legal position.
  So the proof goes through verbatim. ∎

Under (C), part (b) can fail, because a Black who has no test move may now be stalemated. On cyl:4×6, 52 Black-to-move and
40 White-to-move positions are W against dud but D against some other test (COMPUTED). On the cylinders with 3 and 5–8
files that K40 ran, it never fails (COMPUTED).

## Proposition 5 (a parity family in P: no CGT value). PROVED.
Let W ≥ 4 and H ≥ 4. Let x_f be Black to move with wk = (f, H−2), the pawn on (f, H−1) and bk = (f, H) (for example
`Ka6 Pa7 ka8` on cyl:8×8). Let n be an integer, where n > 0 gives White n spare moves and n = −k gives Black k spare moves.
Under (C), x_f ⊞ n is a White win iff n < 0 and n is odd.

*Proof.*

**Black's king moves.** Write a for file f and a± for f ± 1; a+ and a− are distinct and non-adjacent for W ≥ 4. Black's
king has five neighbours: (a±, H), (a±, H−1) and the pawn square (a, H−1). The pawn attacks (a±, H).

**Where White's king can stand.** The pawn is protected exactly when wk is adjacent to (a, H−1). The squares adjacent to
(a, H−1) and not adjacent to bk are (a, H−2), (a+, H−2) and (a−, H−2). Call them c, r+ and r−. Every other square leaves
the pawn unprotected, and then Kxp draws (Lemma 1). So White, who must move every turn (spares aside), keeps the pawn only
by moving among c, r+ and r−.
- c is adjacent to r+ and to r−.
- r+ and r− are not adjacent to each other, since their files are at distance 2 when W ≥ 4.

The graph c–r± is a path, hence bipartite: each White king move changes the side of the bipartition. The pawn cannot
move, because (a, H) is occupied.

**Black to move with wk on c.** c covers (a±, H−1), so bk has no move. With no spare, Black is stalemated: D. With a spare,
Black must play it.

**Black to move with wk on r+.** bk can go to (a−, H−1): it is not adjacent to r+, since the files a+ and a− are at
distance 2, and it is not attacked. That is bk's only move. After it the pawn promotes on (a, H): ⊕. (Under P a promotion
wins at once.) With a spare, Black plays the spare instead. The king move loses at once and the spare loses nothing.

**Case n ≥ 0.** Black is to move at c with no test-game move (an integer n ≥ 0 has no Right option). So Black is
stalemated: D.

**Case n = −k with k ≥ 1.**
- Black's optimal play: never move the king while a spare remains. A king move at r± loses at once, and at c none exists.
- White's options: White has no spare. A king move off {c, r+, r−} allows Kxp, a draw. So White's only non-drawing moves
  alternate between c and r±.
- After Black's j-th spare and White's j-th reply, wk is on r± iff j is odd.
- Black's spares run out after his k-th move. White's k-th reply then leaves wk on r± (Black must play bk to (a∓, H−1),
  then promotion: W) iff k is odd, and on c (stalemate: D) iff k is even.
- White cannot improve: every deviation draws by Kxp. Black cannot improve: a king move while spares remain loses at once.
∎

COMPUTED check: for every board K40 ran with W ≥ 4 (cyl:4–8×6 and cyl:4,6,7,8×8), the positions whose results against
−12…12 are exactly "W iff n < 0 and n is odd" are exactly the W translates of x_f.

**Consequence.** Under (C), x ⊞ n is not monotone in n. A loopy normal-play game G has G + n monotone in n (Lemma 1.6:
adding a Left move cannot hurt Left). So x_f is equal to no loopy CGT game, and the same holds for every position of the
parity classes in the K40 tables. The mechanism is the stalemate rule itself. A stalemated Black side must spend a spare
move it has, so Black's spare tempi help him or hurt him according to their parity. This is LOOPY Remark 1.8 seen from
the tempo side.
