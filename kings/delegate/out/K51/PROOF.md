# Blind proof of Theorem 3.4

## Result

**PROVED.** All three rules hold for every finite short D-game in the packet. A pass can preserve a forced win. With both players able to pass in the shared dud_D coordinate, a player who can force a win always has a winning genuine move on their own turn. With a one-sided reservoir, its owner can sometimes win only by passing.

## States and finite wins

Write L for White to move and R for Black to move. An ordinary sum state is ((x, ω), s), abbreviated (x, s). A genuine move follows an option of s at x. An ordinary successor y gives (y, other s), while either decisive symbol immediately ends the entire sum with its specified winner, regardless of who moved. A permitted pass is the move to (x, other s). If the combined move list is empty, the mover loses immediately. An infinite play is drawn. These are chess-sum semantics throughout, with no BIG translation.

For a fixed player P, call a state winning for P if P can force a finite win. Equivalently, start with terminal wins for P and no-move losses of the opponent, then repeatedly add P-turn states with some winning successor and opponent-turn states with every successor winning. A no-move P-turn state stays out. Each newly included state has a finite rank. P can decrease that rank on every turn of play, and from outside the final set the opponent can keep play outside or reach an outcome other than a P win. Thus a cycle of passes alone cannot certify a finite win. White's and Black's winning sets are disjoint, since playing their purported winning strategies against each other would give incompatible results.

## (a) Both players may pass

**PROVED.** Fix a prospective winner P and write p(x) for P winning on P's turn and q(x) for P winning on the opponent's turn. Write A(x) for “some genuine P option wins for P” and B(x) for “every genuine opponent option wins for P.” Here a terminal option is tested by its winner and an ordinary option by the winning predicate on the successor with the turn switched. An empty existential is false and an empty universal is true.

On the opponent's turn all their options must win for P, including their pass, so q(x) holds exactly when p(x) and B(x) hold. On P's turn any genuine winning option suffices. For necessity, if A(x) is false, the opponent answers every pass by passing back. If P keeps passing, play is infinite and drawn. If P first makes a genuine move, its successor admits no forced P win and the opponent can prevent a P win from there. Thus p(x) holds exactly when A(x) holds. This argument removes the apparent circularity of using a pass as the sole justification for a win.

For P = White, p is Λ_L and q is Λ_R, giving precisely the two displayed recursions. For P = Black, p is Ρ_R and q is Ρ_L, with ⊖ as the favorable terminal. To evaluate either pair, induct on the maximum length of a genuine path from x in the ordinary DAG. Every ordinary follower has smaller height. At x compute p first from followers and terminal options, then q from p and followers. This works also at height zero. Neither sum player can run out of moves. Outside both finite-win sets each player can avoid losing, and when both do so the resulting play is infinite, hence drawn.

The implication q ⇒ p for each color says that being given the move cannot turn that player's win into a draw or loss. Applied also to the opponent, it rules out a draw becoming a loss when given the move. Hence there is no zugzwang for either color. With no decisive terminal options anywhere, no finite result is possible and all states are drawn. At an optionless x this gives an explicit draw. Draws are possible in this model, though a particular G need not have a drawn state. Only a decisive event can deliver a win, and the opposing strategy is free to pass at any turn.

A pass is a winning *first move* for P exactly when q(x) holds, since that is its successor. It can thus preserve a win, but p(x) then guarantees a genuine winning alternative. For example at a single x with L(x) = {⊕} and R(x) empty, White may pass once and win on its next turn. An instruction to pass forever would draw.

## (b) Only White may pass

**PROVED.** Every Black move is genuine. Each nonterminal Black move strictly decreases the height in G, and play alternates. Infinite play would require infinitely many such moves, which is impossible. Equivalently, order states lexicographically by (height, turn bit), with bit 1 on White's turn and 0 on Black's. A White pass strictly decreases the second entry, and every nonterminal genuine move decreases the first. Terminal moves stop immediately. Thus every play ends and ordinary backward induction gives exactly one winner at each state.

On a Black turn there is no pass, so Black wins exactly when some genuine Right option is ⊖ or is an ordinary White-turn successor winning for Black. An empty list is a normal-play loss for Black. This is Ρ′_R. On a White turn Black wins exactly when every White choice wins for Black, including the pass to (x, R). This gives Ρ′_L(x) exactly when Ρ′_R(x) and the displayed universal condition on genuine Left options both hold. White always has at least the pass. Compute Ρ′_R first at each height, then Ρ′_L, which proves well-foundedness. All states outside these predicates are White wins.

White cannot run out of options, so Black can win only by forcing ⊖, possibly through a move made by White. A White win can also result from Black running out of moves. If White wins with Black to move, White wins with White to move by passing, so White never suffers zugzwang. A White pass is a winning first move exactly when Ρ′_R(x) is false. It may be the only winning move, for instance when x has no genuine options for either side.

## (c) Only Black may pass

**PROVED.** Swap the colors, L and R, ⊕ and ⊖, and W and L as outcomes in (b). More explicitly, denote the White-win predicates by U_L and U_R. On White's turn U_L(x) requires some genuine Left option to be ⊕ or to lead to an ordinary y with U_R(y). On Black's turn U_R(x) requires U_L(x) and every genuine Right option to be ⊕ or to lead to an ordinary y with U_L(y). Compute U_L before U_R at each height. The decreasing turn bit is now 1 on Black's turn. Hence no play is infinite, and the complement of White's winning set consists of Black wins. White wins precisely by forcing ⊕. White loses on an empty move list. Black can pass to preserve any win it has with White to move, so Black never suffers zugzwang. The pass wins exactly when U_L(x) is false and can be the sole winning move at an optionless x.
