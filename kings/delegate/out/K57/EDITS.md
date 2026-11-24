### EDIT new Proposition 4.14, Lemma 4.15 and Corollary 4.16 before the K43 computable test (K57, 2026-11-23)
<<<<<<< OLD
*Computable test (K43).*
=======
**Proposition 4.14 (over ≥ 0 in D-sums). PROVED** (new, K57, 2026-11-23; `kings/delegate/out/K57/PROOF.md` §2). For every finite D-game T, position t and side s, White does at least as well in ω ⊞ t as in 0_D ⊞ t (over_D of Proposition 4.6). *Proof.* White plays its 0_D ⊞ T strategy in T and answers Black's first ω → ω by ω → 0_D; deleting that pair gives a play of 0_D ⊞ T. ∎ So Black, when winning (or not losing) beside ω, may give over's passes up and still win (not lose) beside 0_D.

**Lemma 4.15 (one Black token suffices). PROVED** (new, K57, 2026-11-23; `kings/delegate/out/K57/PROOF.md` §3; one AI proof, not refereed). Let G be an exact over group of Definition 4.8, as the P game of its own pieces in a D-sum (Definition 1.3 with K40's convention), and suppose (B1): for every non-shuttle Black move m at a root, the position after m (White to move, with White's e.p. right if m is a double step) is a White win beside −1 (White wins although Black may once move elsewhere). Then for every finite D-game T, loopy or short, with or without terminals, both roots have the results of ω and every q the results of 0_D, with either side to move. *Proof idea.* The side Y that wins (or does not lose) beside over copies its strategy while the group stays at the roots and the q's (shuttle = ω → ω, freeze = ω → 0_D). After any other move of the opponent, which loses at once by Definition 4.8, Y answers it on the board and from then on answers board moves on the board and moves elsewhere elsewhere. If the opponent is White, Black also replaces ω by 0_D (Proposition 4.14), so Black never has to make an unforced board move; if the opponent is Black at a root, White may still be asked once for over's move ω → 0_D, and (B1) pays for it. Draws transfer with non-losing strategies. Nothing beyond Definition 4.8 is needed on White's side or at the q's: condition (T3) of Definition 4.12 is not needed, and (B1) is condition (N1) of (T2) read with the sum's rule that a side with no move loses.

**Corollary 4.16 (an over group). PROVED, given CHECKED-2 computations** (new, K57, 2026-11-23). The 2 + 3 group `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` of cyl:10×6 has the results of over beside every finite D-game: Definition 4.8 holds (K45, CHECKED-2), and (B1) holds for all ten non-shuttle Black root moves (K55's za and rz and K57's own solver agree; the two double steps …a5–a3 were checked by za and rz through White's e.p. reply b3xa4). So over is realised in D-sums by a king-and-pawn group of P. The four exact groups of cyl:8×7 (K48) satisfy (B1) by one program (COMPUTED-1), so for them the same conclusion is conditional. Z_O and its flat translates fail (B1) exactly at 1…e5–e4 (and its translates), which one Black token saves; this is the K47 difference, which always favours Black.

*Computable test (K43).*
>>>>>>> NEW

### EDIT "To settle": the 2 + 3 group is settled (K57, 2026-11-23)
<<<<<<< OLD
whether the 2 + 3 group of cyl:10×6, which has the results of over against all 752 test games tried (K55), is over, which needs an argument beyond a finite battery (it is not a stopper);
=======
the 2 + 3 group of cyl:10×6 has the results of over beside every finite D-game (K57, Corollary 4.16: PROVED given CHECKED-2 computations; not yet refereed); a referee check of Lemma 4.15 and a second program for (B1) on the cyl:8×7 groups;
>>>>>>> NEW

### EDIT summary of Conjecture 4.7 in §8: an over group exists in D-sums (K57, 2026-11-23)
<<<<<<< OLD
so "an over-group" in the sense of a group with the value over is still not known;
=======
so "an over-group" in the sense of a group with the value over was still not known after K47 (K57, 2026-11-23: the 2 + 3 group of cyl:10×6 has the results of over beside every finite D-game, Corollary 4.16, PROVED given CHECKED-2 computations, not yet refereed);
>>>>>>> NEW
