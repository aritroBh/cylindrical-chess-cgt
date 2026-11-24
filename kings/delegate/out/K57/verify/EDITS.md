### EDIT new Proposition 4.14, Lemma 4.15 and Corollary 4.16 before the K43 computable test (K57 and its referee, 2026-11-23)
<<<<<<< OLD
*Computable test (K43).*
=======
**Proposition 4.14 (over ≥ 0 in D-sums). PROVED** (new, K57, 2026-11-23; `kings/delegate/out/K57/PROOF.md` §2; one AI proof, re-derived step by step by the K57 referee, `kings/delegate/out/K57/VERIFY.md`; no human re-derivation). For every finite D-game T (Definition 1.1, loopy or short, with or without terminals), position t and side s to move, White does at least as well in ω ⊞ t as in 0_D ⊞ t (over_D of Proposition 4.6): a winning (non-losing) White strategy beside 0_D gives one beside ω, so a Black win (non-loss) beside ω gives one beside 0_D. *Proof.* White plays its 0_D ⊞ T strategy in T and answers Black's first ω → ω by ω → 0_D; deleting that pair from a play gives a play of 0_D ⊞ T with the same T-moves, the same end and at most two moves fewer. ∎ So Black, winning (or not losing) beside ω, may give over's passes up at any moment.

**Lemma 4.15 (exact over groups with one Black token have the results of over). PROVED** (new, K57, 2026-11-23; `kings/delegate/out/K57/PROOF.md` §3; one AI proof, re-derived step by step by the K57 referee, `kings/delegate/out/K57/VERIFY.md`; no human re-derivation). Let G be an exact over group of Definition 4.8 (so, with K1 and K2, no king is in check at the roots and at the q's), taken as the P game of its own pieces in a D-sum (Definition 1.3 with K40's convention, as in the K47 bullet of Conjecture 4.7), and suppose (B1): for every non-shuttle Black move m at a root, the position after m (White to move, with White's e.p. right if m is a double step) is a White win beside −1, under the sum's rule (Black may once move elsewhere, not while in check, which clears the right; a side with no move loses). Then for every finite D-game T, loopy or short, with or without terminals, every position t and either side to move: both roots have the results of ω, and every q (Black to move with or without the right of a double-step freeze, and White to move) has the results of 0_D, i.e. of t alone. *Proof idea.* The side Y that wins (or does not lose) beside over copies its strategy S while the group stays at the roots and the q's (shuttle = ω → ω, freeze = ω → 0_D). Any other move of the opponent X loses at once in P by Definition 4.8; Y answers it on the board and from then on answers board moves on the board (attractor strategy) and moves elsewhere by S elsewhere. If X is White, Black also replaces ω by 0_D (Proposition 4.14), so Black is never asked for an unforced board move; at a q nobody is. If X is Black at a root, S may still ask White once for ω → 0_D; White then makes one unforced board move, which is the one Black token of (B1). Phase 2 has finitely many board moves (attractor ranks, and the token is spent at most once), so an infinite play is an infinite play of over_D ⊞ T; terminals of T are reached in both plays alike; draws transfer with non-losing strategies. Nothing beyond Definition 4.8 is needed on White's side or at the q's: condition (T3) of Definition 4.12 is not needed, and (N1) of (T2) implies (B1) (a stalemate draw becomes a loss for the stalemated side, which only adds White wins when Black is stalemated, and a White winning strategy never reaches a stalemate of White). (B1) is sufficient, not necessary. *Sanity check (K57 referee, COMPUTED-1, own code `kings/delegate/out/K57/verify/src/toyref.py`):* abstract toy groups that model checks (no move elsewhere in check, no move into one's own check, checkmate a loss and stalemate a draw in P) and e.p. rights (double steps, extra moves for one turn, cleared by a move elsewhere): 12,000 exact groups with (B1) (8,000 random, 4,000 from an adversarial family whose bad White moves are saved by one, several or unlimited White passes and whose bad Black moves are saved by two or more Black tokens) beside 224 finite D-games each (24 hand-made, among them games with terminals for either side and games with unlimited spare White moves, and 200 random, loopy, with terminals) have the results of over at all 63,349,928 results; 5,584 of them fail K56's (T3), 6,124 of the 10,000 where it was recorded have different freezes at the two roots, 1,649 of these 10,000 are not won by White with two Black tokens after some bad Black root move, and 7,161 have a check somewhere; without (B1), 1,225 of 12,000 exact groups differ from over somewhere. Proposition 4.14 holds at all 150,796 comparisons tried.

**Corollary 4.16 (a group with the results of over). PROVED, given CHECKED-2 computations** (new, K57, 2026-11-23; refereed, `kings/delegate/out/K57/VERIFY.md`). The 2 + 3 group H10 = `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` of cyl:10×6, as the P game of its own pieces in a D-sum, has the results of over beside every finite D-game (both roots, either side to move; each q has the results of 0_D). The hand proof is Lemma 4.15; it rests on two computed facts. (i) Definition 4.8 for H10 (K45, CHECKED-2). (ii) (B1) for H10: Black has ten non-shuttle root moves (…Kf6–e6, …a4, …a5–a3, …e4, …e5–e3 at the f6 root; …Kg6–h6, …a4, …a5–a3, …e4, …e5–e3 at the g6 root; the same lists from `kp_p --moves` and from the K56 referee's move generator), and after each the position with White to move is a White win beside −1 (CHECKED-2: the K57 referee's `verify/src/vgsum.cpp` on the K56 referee's generator, with the e.p. right kept, under the sum's rule both as a one-token game and as the product with −1; the K56 referee's `vg` and K57's `pr57` in the pass game, which implies it; K55's za and rz, refereed for cyl:10×6, for the eight moves without a right and, for the two double steps …a5–a3, through White's reply b3×a4 e.p.). A direct check agrees: beside 63 further finite D-games (at most 4 positions, 34 with terminals), H10 has the results of over at all 1,215 results (COMPUTED-1, `vgsum`). "Has the results of over beside every finite D-game" is the statement proved; the note defines no equality of loopy D-games beyond it, and it says nothing about P contexts (which do not behave as D-sums, K47 bullet) or chess. The four exact groups of cyl:8×7 (K48) satisfy (B1) by one program (pr56/pr57, COMPUTED-1), so for them the same conclusion is conditional on a COMPUTED-1 fact. Z_O (cyl:8×6 and flat 8×6) and its two flat translates fail (B1) exactly at 1…e5–e4 (and its translates): every other non-shuttle Black root move satisfies it (K57 referee's `vgsum`, sum's rule; for Z_O on cyl:8×6 the failure agrees with the K55 referee's solver, CHECKED-2; for the others COMPUTED-1), and for Z_O this is where it differs from over (K47).

*Computable test (K43).*
>>>>>>> NEW

### EDIT Lemma 4.13: the 2 + 3 group is decided by Lemma 4.15 (K57 referee, 2026-11-23)
<<<<<<< OLD
So the lemma does not decide the 2 + 3 group, and **whether the 2 + 3 group is over stays OPEN**;
=======
So Lemma 4.13 does not decide the 2 + 3 group; Lemma 4.15 (K57), which drops (T3), does: **the 2 + 3 group has the results of over beside every finite D-game** (Corollary 4.16, PROVED given CHECKED-2 computations);
>>>>>>> NEW

### EDIT K47 bullet: the K56 sentence (K57 referee, 2026-11-23)
<<<<<<< OLD
None of the nine exact groups tested satisfies it, so no known group does, and whether the 2 + 3 group of cyl:10×6 is over stays open.)
=======
None of the nine exact groups tested satisfies it, so no known group does. K57, 2026-11-23: Lemma 4.15 needs only one Black token after a bad Black root move (B1) and nothing beyond Definition 4.8 on White's side; the 2 + 3 group of cyl:10×6 meets it, so it has the results of over beside every finite D-game (Corollary 4.16, PROVED given CHECKED-2 computations), while Z_O fails (B1) at 1…e5–e4.)
>>>>>>> NEW

### EDIT K55 bullet: the finite battery is now backed by a proof (K57 referee, 2026-11-23)
<<<<<<< OLD
This is a finite battery, not a proof that the group is over;
=======
This is a finite battery, not a proof (K57, 2026-11-23: Corollary 4.16 proves that the group has the results of over beside every finite D-game, given CHECKED-2 computations);
>>>>>>> NEW

### EDIT C4.7 status row: the 2 + 3 group (K57 referee, 2026-11-23)
<<<<<<< OLD
while the 2 + 3 group of cyl:10×6 has the results of over against all 752 test games tried, a finite battery, not a proof of equality; see the K55 bullet)
=======
while the 2 + 3 group of cyl:10×6 has the results of over against all 752 test games tried; see the K55 bullet; K57, 2026-11-23: **the 2 + 3 group has the results of over beside every finite D-game**, Corollary 4.16, PROVED given CHECKED-2 computations (Definition 4.8 and one Black token after each non-shuttle Black root move, (B1)), by Lemma 4.15, PROVED and refereed)
>>>>>>> NEW

### EDIT Conjecture 4.7, opening: which group is not over (K57 referee, 2026-11-23)
<<<<<<< OLD
but the one tested in sums is not equal to over (K47, 2026-11-23, CHECKED-2; see the K47 bullet below): Definition 4.8 does not force the value over.
=======
but the cyl:8×6 group is not equal to over in D-sums (K47, 2026-11-23, CHECKED-2; see the K47 bullet below): Definition 4.8 does not force the value over. With one Black token after each non-shuttle Black root move it does force the results of over (Lemma 4.15, K57), and the 2 + 3 group of cyl:10×6 has the results of over beside every finite D-game (Corollary 4.16, PROVED given CHECKED-2 computations).
>>>>>>> NEW

### EDIT Conjecture 4.7, second half: over is realised in D-sums by results (K57 referee, 2026-11-23)
<<<<<<< OLD
so over itself is still not realised as a sum value):*
=======
over itself is realised in D-sums in the sense of results by the 2 + 3 group of cyl:10×6, Corollary 4.16, K57, PROVED given CHECKED-2 computations):*
>>>>>>> NEW

### EDIT "To settle": the 2 + 3 group is settled in D-sums (K57 referee, 2026-11-23)
<<<<<<< OLD
whether the 2 + 3 group of cyl:10×6, which has the results of over against all 752 test games tried (K55), is over, which needs an argument beyond a finite battery (it is not a stopper);
=======
the 2 + 3 group of cyl:10×6 beside P contexts and in chess (in D-sums it has the results of over beside every finite D-game, Corollary 4.16, K57, PROVED given CHECKED-2 computations); a second program for (B1) on the four cyl:8×7 groups;
>>>>>>> NEW

### EDIT §8 item 2: a group with the results of over exists (K57 referee, 2026-11-23)
<<<<<<< OLD
so "an over-group" in the sense of a group with the value over is still not known;
=======
so "an over-group" in the sense of a group with the value over was still not known after K47; K57 (2026-11-23) proved that the 2 + 3 group `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` of cyl:10×6, as the P game of its own pieces, has the results of over beside every finite D-game (Lemma 4.15 and Corollary 4.16, PROVED given CHECKED-2 computations, refereed);
>>>>>>> NEW
