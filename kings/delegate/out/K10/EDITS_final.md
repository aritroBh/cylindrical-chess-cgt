### EDIT 1
<<<<<<< OLD
**Remark 2.11 (the certificate is not special to kings). GAP.** A passer created in a component is a decisive
event too, and (V2) asks the same question about it. The certificate of Definition 2.6 **cannot apply as
written** to a passer (revised after review: R3 item 6):
- Q_Z deletes "every context pawn", which deletes the passer itself.
- The punishing reply r is not a king capture of a Z-pawn.
- The passer's owner may need its king off F_Z, where the legality step via Lemma 2.2 no longer covers it.
- The pawns of the passer's own component are not addressed.
The claim "which this certificate rules out" is therefore unproved. P11 in §6 relies on this remark under a
PROVED label; that label must be revised when the certificate is extended.
=======
**Proposition 2.11 (frozen-king passer certificate). PROVED in P (frozen), as a sufficient condition (revised after
K10, 2026-10-22).** *Caveat.* K10's first draft (a free model) was FALSE: it said that a passed pawn stays passed, and
that fails when an ω pawn captures a β pawn on a neighbouring file. Two AI reviewers found that error and five more
(checks, kings on the path, one move order only, races, en passant). The statement and proof below were rebuilt by
a Sonnet agent (the K10 fixer), which also ran the enumerations listed after the proof. The integrator read the
proof step by step, re-ran every example on a separate kpsolve build, and corrected one example (P1a, which also
fails (H1)). It is one AI proof. No human and no second model has re-derived it.

*Setting.* F is the frozen promotion model, `kpsolve --frozen`: a promotion wins at once for the promoter; a legal
king move ends the play at once in favour of the opponent of its maker; a side with no legal move at all (king
moves count as moves) that is not in check draws, and one in check loses; infinite play is a draw. The board is
a cylinder with W files and H ≥ 5 ranks (files mod W). On a flat board the same proof works with the neighbouring
files that exist; that case was not run.

*Notation.* Fix a position y before any promotion, the side s to move, a side β (the beneficiary) and ω, the
other side. For a pawn q of either colour let ρ(q) be its rank counted from β's side (ρ = rank for White,
H + 1 − rank for Black). β's pawns advance towards larger ρ, ω's towards smaller ρ; "ahead of p" means larger ρ.
β's start rank is ρ = 2 and ω's is ρ = H − 1. For a pawn p of β put d = H − ρ(p) − [ρ(p) = 2] (the number of β
moves p needs to promote; this is cylcgt's `promote_distance`), and
- e = d if s = ω (ω makes e moves before β's promoting push),
- e = d − 1 if s = β.

*The ω-only game G_ω(y; p).* Delete p. Only ω moves, one move after another. β's other pawns stay where they are
and can be captured. Both kings stay and block squares; nobody captures a king. ω's pawns move as in chess:
push, double step from the start rank over an empty square, capture, and the e.p. capture that y offers (only
as the first move, and only if s = ω). μ_ω(y; p) is the least number of moves after which some ω pawn stands on
its last rank (the promoting move included), or ∞. It is a minimum over **all** ω pawns, passers or not,
with captures allowed. An ω king move ends F at once, so it never occurs in G_ω.

*Hypotheses.*
- **(H1) clear path.** p is a pawn of β that is passed at y in cylcgt's e.p.-aware sense (`passed` with
  `PASSED_RESPECTS_EP = True`: no ω pawn on files f − 1, f, f + 1 with ρ > ρ(p), and p cannot be taken en passant at
  y), and every square of p's file ahead of p, the promotion square included, is empty. So p is the front pawn
  of its file, and **no pawn and no king of either colour** stands on the path.
- **(H2) no check.** No pawn of either colour stands on a file adjacent to the file of β's king.
- **(H3) no stalemate.** ω's king has a neighbouring square t that is not adjacent to β's king, such that no
  pawn of either colour stands on the file of t or on a file adjacent to it. "Not adjacent" means king distance ≥ 2.
- **(H4) no interference.** Every pawn of β other than p that stands on a file adjacent to p's file has
  ρ ≤ ρ(p) + 1.
- **(H5) timing.** μ_ω(y; p) ≥ e + 1.

**Statement.** Under (H1)–(H5), β wins F from (y, s) by pushing p at every turn (the double step first if
ρ(p) = 2).

*Proof.* Write f for p's file and ρ₀ for ρ(p) at y.

*Step 0, three facts about F.*
- (F1) A pawn changes file only by a capture, and lands on the square of the captured piece (an e.p. capture lands
  on the file of the captured pawn). There are no officers before the first promotion, and a king is never
  captured. So a pawn enters a file only by capturing a pawn that stands on it, and a file without pawns never
  gets one.
- (F2) A king move ends F at once. So in any play in which its maker has not lost, no king moves, and both kings
  stand where they stand at y.
- (F3) A promotion ends F with a win for the promoter.

*Step 1, safety of the kings.*
- By (H2) and (F1), no pawn ever stands on a file adjacent to β's king, so no ω pawn ever attacks it. ω's king
  gives no check. So β is never in check, and no push of p is ruled out by king safety.
- By (H3) and (F1), the three files around t never hold a pawn. So t is never occupied, never attacked by a
  β pawn (p included), and is not adjacent to β's king: a move of ω's king to t is always legal, even if ω is
  in check. So ω always has a legal move: it is never stalemated, and F has no draw by stalemate in the play below.

*Step 2, the invariant.* Consider plays in which β follows the strategy Π (push p) and ω moves arbitrarily. Let
ρ_p be the current value of ρ(p) and call the files f − 1, f, f + 1 the *strip*. We show:
- (J_β) at every node with β to move, every ω pawn in the strip has ρ ≤ ρ_p + 1;
- (J_ω) at every node with ω to move, every ω pawn in the strip has ρ ≤ ρ_p, and p cannot be taken en passant;
- (I1) at every node, every square of file f ahead of p is empty.

At y: (J_β) or (J_ω), according to s, is (H1) (passed, aware), and (I1) is (H1). In the following, β's other pawns
and both kings never move, by Π and (F2).
- *β moves.* p goes from ρ_p to ρ′ ∈ {ρ_p + 1, ρ_p + 2}; the squares are empty by (I1), and the move is legal by
  Step 1. By (J_β), the ω pawns in the strip have ρ ≤ ρ_p + 1 ≤ ρ′. A double step (ρ′ = ρ_p + 2) leaves every ω
  pawn in the strip strictly below ρ′, and an e.p. capturer stands on the rank of p, so none exists. A single step
  gives no e.p. right. So (J_ω) holds, and (I1) still holds.
- *ω moves a pawn.* (a) A push or double step lowers ρ. It cannot enter p's square or a square ahead of p on file
  f, because the pawn stands at ρ ≤ ρ_p. (b) A capture lands on the square of a captured β pawn q (or on an e.p.
  target). It captures p never: (J_ω) leaves no ω pawn at ρ_p + 1 next to p, and p is not e.p.-capturable. So
  q ≠ p. If q is on file f, then q stands behind p (nothing of β stands ahead of p by (H1)), and the landing
  rank is below ρ_p. If q is on file f ± 1, then ρ(q) ≤ ρ₀ + 1 ≤ ρ_p + 1 by (H4), and the landing rank is ρ(q). An
  e.p. capture is possible only with the right offered by y when s = ω (Π double-steps only p, and p is not
  capturable): the victim q′ is a β pawn that just double-stepped, the landing square is the skipped square, one
  rank below q′. If q′ is on f ± 1, then ρ(q′) ≤ ρ₀ + 1 by (H4); if on f, it is behind p. Either way the landing
  rank is at most ρ_p + 1. (c) So every ω pawn in the strip after the move has ρ ≤ ρ_p + 1, which is (J_β),
  and nothing lands on file f ahead of p, which is (I1). Captures that land outside the strip change nothing.
  (The tempting one-line argument "ω pawns move away from p's promotion side, so none can ever stand beside its landing
  square" is false: a capture of a β pawn on a neighbouring file puts an ω pawn there. (H4) is what bounds the landing rank.)

*Step 3, consequences.* At every ω turn no ω pawn stands at ρ_p + 1 next to p, and p cannot be taken e.p., so p is
never captured; nothing stands ahead of p on file f ((I1)), so p is never blocked. At every β turn the push is
legal. So Π can be played to the end.

*Step 4, ω's moves are moves of G_ω.* In a play consistent with Π, each ω pawn move is a move of G_ω(y; p): the
squares and the captured pawns are the same, p never takes part (Step 3), β's other pawns stay (Π), the kings
stay (F2), and the only e.p. capture is the one offered at y. (G_ω has fewer obstacles, since p is deleted; this
only enlarges its move set.) So if ω promotes after k of its moves in the real play, then k ≥ μ_ω(y; p). An ω king
move loses at once (F2).

*Step 5, timing.* Under Π, β promotes with its d-th push. Before that push ω has made exactly e moves. By (H5),
e < μ_ω(y; p), so by Step 4 none of those moves promotes, and by Step 1 ω has a legal move each time, so the
play is not a draw. ω's only other moves are king moves, which lose at once. β's d-th push is legal (Step 3)
and promotes, and by (F3) β wins. ∎

**Corollary 2.11a ((V2) at a passer or race terminal of the D-model).** Let y′ be the node reached by a move of M
(N to move), and let cylcgt credit it to b ∈ {M, N}:
- only M has a passed pawn: b = M;
- only N has a passed pawn: b = N;
- both have one (a race, scored by the count rule): b = N if dp(N) ≤ dp(M), else b = M, where dp is
  `promote_distance`.

Then (V2) holds at y′ if (H1)–(H5) hold at (y′, s = N, β = b) for some pawn p of b. Then e = d if b = M (the
opponent moves first) and e = d − 1 if b = N (the beneficiary moves first). This covers the terminal's beneficiary
in both move orders, and a race won by the side to move. The corollary is the proposition at y′. It is
sufficient only (slack example below).

**Corollary 2.11b (the layout of P11).** On cyl:8×6 with `Ka1 ka6` and the b- and h-files empty, all pawns stand
on c–g and stay there (F1). Then for either colour as β: (H2) holds (the neighbours of the a-file are b and h);
(H3) holds with t = a5 for ω = Black and t = a2 for ω = White (the kings are four ranks apart); and no king stands
on p's file. So at a terminal of such a position only the passed front pawn, (H4) and (H5) have to be checked.

**Remark (the count rule is not a (V2) certificate).** In the count rule's test, β wins iff dp(ω) ≥ e + 1. This is
(H5) with μ_ω replaced by ω's fastest **passer** distance dp(ω), and dp(ω) ≥ μ_ω whenever no king stands on the
path of that passer (always so in P11's layout). The two agree only if no non-passer of ω is as fast. Without a passer of ω the count rule credits β whatever ω's pawns do, and it sees neither captures
(H4) nor kings (H1, H2) nor stalemate (H3).

**What the hypotheses do (every example is a `kpsolve --frozen --cap 1` result; the integrator re-ran each on a
separate build).** Unless a
board is named, it is cyl:8×6; β is White (p = Pc4 or Pc2) unless said otherwise.
- *(H5), both move orders.* ω to move (e = d = 2): `Ka1 ka6 Pc4 pe3 b -` (μ = 2) gives (L, L), so ω wins the tie;
  `Ka1 ka6 Pc4 pe4 b -` (μ = 3) gives (W, W). β to move (e = d − 1): `Ka1 ka6 Pc4 pe3 w -` (e = 1, μ = 2) gives (W, W);
  `Ka1 ka6 Pc3 pe3 w -` (d = 3, e = 2, μ = 2) gives (L, L). With Black as β: `Ka1 ka6 pc3 Pe4 w -` (ω to move,
  μ = 2) gives (W, W) and `Ka1 ka6 pc3 Pe3 w -` (μ = 3) gives (L, L).
- *(H5), non-passers count.* `Ka1 ka6 Pc2 Pd4 pd3 b -`: p = Pd4 is a passer (d = 2) and the only Black pawn is not
  one, but d3xc2 and c1=Q take ω two moves. (L, L), although cylcgt credits White. This is the position
  after c3xd4 in `Ka1 ka6 Pc2 Pc3 pd3 pd4 w -`, whose D-result is a White win and whose `--frozen` result is (L, L):
  the D-result and `--frozen` differ at this root. Race: `Ka1 ka6 Pc4 Pd2 pe3 pf4 b -` is (L, L); the count rule
  credits White (dp = 2 against dp(Black) = 3 for the passer f4), but Black's non-passer e3 takes d2 and promotes in two.
- *(H5) is not necessary.* cyl:7×6 `Ka1 ka6 Pc2 Pd3 Pf2 pe4 b -` has μ = e = 3 and is (W, W): the proposition says
  nothing there.
- *(H4), and the threshold ρ(p) + 1 is exact.* `Ka1 ka6 Pc2 Pd4 Pe2 pe5 b -` is (L, L): p = c2, Pd4 stands at
  ρ = ρ(p) + 2, and e5xd4 followed by d3, d2, d1 takes ω four moves (μ = 4 ≥ e + 1 = 4, so (H5) holds); the
  pawn on d4 then attacks c3 and the double step is met by dxc3 e.p. `Ka1 ka6 Pc2 Pd3 Pe2 pe5 b -`
  (Pd3 at ρ(p) + 1) is (W, W). The failure arises inside the D-model: `Ka1 ka6 Pc2 Pe2 Pe3 pd4 pe4 pe5 w -` has D-result
  "White wins" (e3xd4 makes c2 a passer, a terminal credited to White) and is (L, L) in F.
  With the bound ρ(p) + 2 in place of ρ(p) + 1, the end-to-end run below refutes 8 certified wins (9,852 roots, cyl:6×6); so does
  dropping (H4) (16 of 80 instances on cyl:6×6).
- *(H2).* `Ke2 ka6 Pc4 pf4 b -` is (L, L) (f4-f3+ forces a king move or no reply), `Ka1 ka6 Pc4 pf4 b -` is (W, W);
  in both p = c4, d = 2 and μ = 3 = e + 1.
- *(H1), kings.* `Ka1 kc5 Pc4 pf4 b -`, `Kc5 ka6 Pc4 pf4 b -`, `Kc6 ka6 Pc4 pf4 b -` and `Ka1 kc6 Pc4 pf4 b -`
  (a king of either colour on the path, or on the promotion square) are all (L, L).
- *(H1), e.p.* `Ka1 ka6 Pe4 pd4 b e3` (e4 has just been played, e.p. right on e3) is (L, L); the same position
  without the right, `... b -`, is (W, W). The textbook passed test calls e4 passed at once, the aware test does not.
  Another: `Ka1 ka6 Pc3 Pd4 Pf2 pc4 b d3` is (L, L) and `... b -` is (W, W): the right is the only reason that
  μ = 3 ≤ e = 3 (the e.p. capture is the first move of G_ω).
- *(H3).* `Ke1 ka6 Pa4 Pc5 Pg5 pa5 b -` is (D, D): p = c5 (d = 1), (H1), (H2), (H4) and (H5) hold (μ = ∞: a5 is
  blocked and has nothing to capture), but Black has no legal move: a4 covers b5 and h5 across the seam, c5
  covers b6 and g5 covers h6. Without Pg5 the king can step to h6 (and lose), and the position is (W, W). Also
  flat:7×6 `Kb1 ka6 Pa4 Pc2 Pc5 pa5 b -` is (D, D); there the static (H2) fails, but no check can occur.
  (P1a of §5.4, cyl:7×6 `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5 b -`, is (D, D) too, but it is not an example for (H3):
  the black king stands on c6, the promotion square of c5, so (H1) fails as well.)

**Checks (K10 fixer, 2026-10-22; kpsolve built privately from `kings/kpsolve.c`; data, not proof).** The
scripts (`cert.py` decides (H1)–(H5) with its own move generator, and only `passed` and `promote_distance` are cylcgt's;
`direct.py`, `direct2.py`, `e2e.py`) and their logs are copied to `kings/delegate/out/K10/scripts/`; their paths point
at the old scratchpad.
- *Proposition against `--frozen`, kings parked* (`Ka1` and a Black king on the top rank of the a-file, the b-file and the
  last file empty, pawns on files c to W − 2, ≤ 3 per side except where noted; both colours as β, both sides to move): cyl:6×6 74,410
  instances, cyl:8×6 (≤ 2 per side) 64,954, cyl:6×7 306,020, cyl:6×5 12,160, cyl:7×6 496,848: **0 violations in
  954,392**. With (H4) dropped: 16 of 80 (6×6), 56 of 456 (6×7), 32 of 368 (7×6) violate.
- *Kings anywhere* (random placements, so that (H2), (H3) and the king clause of (H1) are tested as stated): cyl:7×6,
  cyl:8×6 and cyl:6×7, 20,000 instances each, ≤ 3 pawns a side: 0 violations in 60,000. With one hypothesis dropped,
  the violations are: (H2) 1,744, 1,853 and 1,394 of 20,000; (H3) 8 of 19,033, 8 of 16,599 and 5 of 20,000; the king
  clause of (H1) 563 of 1,315, 469 of 1,020 and 556 of 1,783; (H4) 0 of 4 and 0 of 9 (too few) and 2 of 11.
- *Chain D → P, end to end* (kings parked; no passer at the root; both sides to move): cyl:6×6 files c–e, ≤ 3 pawns a
  side, 9,852 roots; cyl:7×6 files c–f, ≤ 3 a side, 40,204 roots; cyl:8×6 ≤ 2 a side, 5,384 roots; cyl:6×6 ≤ 2, 1,432
  roots; 56,872 in all. The conservative D-game in which a side's own terminals, and the opponent's moves into
  terminals credited to it, must be certified by Corollary 2.11a gives a win only if `--frozen` agrees: 48,000
  certified wins, 0 violations. When **every** terminal of the D-game is certified (26,014 roots), `--frozen` equals
  the D-result (o(W)): 0 violations. Without (H4) in the certificate: 8 violations (cyl:6×6). `--frozen` differs from
  o(W) at 3,194 of the 56,872 roots, all of them with some uncertified terminal.

**Remark 2.11 (the certificate is not special to kings; real kings).** The same (V2) question arises for passer
terminals. The certificate of Definition 2.6 (king moves) does not apply to a passer as written (Q_Z deletes the
passer, r is not a king capture, the owner's king may leave F_Z, the component's own pawns are unaddressed).
Proposition 2.11 supplies the missing certificate for passer and race terminals **in the frozen model**, and
Corollary 2.11a states it for the D-model.
- **Proved about real kings: nothing.** Every step above uses (F2). The hypotheses are not enough with real kings:
  `Ka1 ka6 Pc2 w -` (cyl:8×6) satisfies (H1)–(H5) with μ = ∞ and is (W, W) in F, but P with real kings (a private
  `--pmodel` build, `kings/delegate/out/K7/scripts/draft/kp_p.c`) and chess (kpsolve exact) both give (D, D).
- **Corollary 2.8** is the real-king statement for one pawn: a single-pawn local game with a king beyond reach.
- **CONJECTURE (real-king square rule, label kept).** Let β's king be sheltered as in (H2) and the pawn data satisfy
  (H1), (H4), and (H5) with ω's king allowed to move and to capture β's other pawns in G_ω. Let q₀, …, q_d be the
  squares p occupies before its first push and after each push, and n_j = j if s = ω, j − 1 if s = β, the number of
  ω moves before the j-th push. If d(k_ω, q_j) ≥ n_j + 2 for every j (for j = 0 only if s = ω), then β wins P with
  real kings. This follows from d(k_ω, q_d) ≥ d + 2 (s = ω) or d + 1 (s = β) by the triangle inequality. The
  sketch is the proof above with Step 1 replaced by the rule of the square (no capture and no block), but ω could
  steer into a stalemate or a draw by king-and-pawn play, which the sketch does not exclude. Scratch evidence
  only: β = White, `Ka1`, ≤ 2 + 2 pawns, `--pmodel`: cyl:6×6 30,847 legal instances and cyl:7×6 158,840, 0
  violations. The chess form needs (A_Q) at the resulting position (§1.2) and is not claimed.
- P11 in §6 relies on Proposition 2.11 in the sense given there (revised after K10, 2026-10-22).
>>>>>>> NEW

### EDIT 2
<<<<<<< OLD
| R2.11 | GAP → heuristic only. No certificate for passers is claimed | R3 item 6 |
=======
| R2.11 | GAP → PROVED in P (frozen), as a sufficient condition (revised after K10, 2026-10-22): Proposition 2.11 and Corollary 2.11a give (V2) at a passer or race terminal under (H1)–(H5): a clear path for pawns and kings of both colours, no check, no stalemate, no interference of an ω pawn that captures a β pawn on a neighbouring file, and the timing bound for both move orders over all ω pawns. K10's first draft was FALSE (it ignored all of these); the statement and proof were rebuilt by a Sonnet agent and read step by step by the integrator. One AI proof, checked on 954,392 parked and 60,000 random-king instances against `kpsolve --frozen` (0 violations; scripts in `kings/delegate/out/K10/scripts/`). Real kings: nothing proved, the square rule is a CONJECTURE (scratch evidence) | R3 item 6; K10 |
>>>>>>> NEW

### EDIT 3
<<<<<<< OLD
| P11 | GAP (proof incomplete): W(X) and HSS defined; (V1b) checked from the layout (revised after K3 check) | R1 item 11 |
=======
| P11 | PROVED in P, in conditional form (revised after K10, 2026-10-22): `--frozen` = o(W(X)) for every X of the layout whose passer and race terminals are all certified by Corollary 2.11a. The chain is Theorem 1.14(i) with (V1) from the layout (no check is possible, and a king move is always legal), (V3) by fiat, and (V2) by Corollary 2.11a at every terminal; the o(S) clause adds HSS with Theorem 1.11(c) and Theorem 1.14(ii). Without the certificate the equality is FALSE (`Ka1 ka6 Pc2 Pc3 pd3 pd4 w -`: o(W) is a White win, `--frozen` is (L, L)). Not yet done: P11's own harness does not test (H4) and (H5) (the K10 end-to-end script `kings/delegate/out/K10/scripts/e2e.py` does, on the roots listed under Proposition 2.11), and no second model has re-derived Proposition 2.11 | R1 item 11; K10 |
>>>>>>> NEW

### EDIT 4
<<<<<<< OLD
| P11 | cyl:8x6, `--frozen` | Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; every passer and race node speed-certified (Remark 2.11 with frozen kings); condition (E). Here W(X) is the D-game of X with its own winning side, and "hereditarily sum-safe" (HSS) means that every component of X is itself sum-safe in the sense of Theorem 1.14(ii) | kpsolve `--frozen` = o(W(X)); also = o(S(X)) when hereditarily sum-safe. Where o(S) ≠ o(W) (opposite threats, Prop 1.12), `--frozen` sides with W | — | — (a harness check, not one position) | Thm 1.11 + Thm 1.14 (frozen kings satisfy V1 and V3 by fiat) | GAP (proof incomplete): the harness checks the hypotheses (revised after K3 check) |
=======
| P11 | cyl:8x6, `--frozen` | Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; every passer and race terminal of the D-game of X certified by Corollary 2.11a (for the beneficiary's passed front pawn: (H4) and (H5); in this layout (H2), (H3) and the king clause of (H1) hold by Corollary 2.11b); condition (E). Here W(X) is the D-game of X with its own winning side, and "hereditarily sum-safe" (HSS) means that every component of X is itself sum-safe in the sense of Theorem 1.14(ii) | kpsolve `--frozen` = o(W(X)); also = o(S(X)) when hereditarily sum-safe. Where o(S) ≠ o(W) (opposite threats, Prop 1.12), `--frozen` sides with W | — | — (a harness check, not one position) | Thm 1.11 + Thm 1.14 (frozen kings satisfy V1 and V3 by fiat) + Proposition 2.11 / Corollary 2.11a for (V2) | PROVED in P, conditional on the certificate (revised after K10, 2026-10-22). False without it: `Ka1 ka6 Pc2 Pc3 pd3 pd4 w -` is a White win in W(X) and (L, L) in `--frozen`; checked end to end on 56,872 roots of cyl:6×6, cyl:7×6 and cyl:8×6 (0 violations when every terminal is certified; 3,194 roots differ otherwise) |
>>>>>>> NEW

### EDIT 5: preamble, P11 after K10
<<<<<<< OLD
another reviewer (revised after K9, 2026-10-22). So, of K3's four GAP downgrades, only P11 remains GAP. The scripts behind the checks
=======
another reviewer (revised after K9, 2026-10-22). **Caveat for K10 (Proposition 2.11, P11):** a free model drafted a
passer certificate; two Sonnet reviewers found it FALSE (a capture of a β pawn on a neighbouring file lets an ω pawn
stop the passer, and checks, kings, one move order and races were ignored). A Sonnet agent rebuilt the statement and
proof, and the integrator read it step by step and re-ran its examples. No second model has re-derived it. With it,
P11 is PROVED in P in a conditional form: the passer and race terminals must be certified (revised after K10,
2026-10-22). So none of K3's four GAP downgrades remains GAP. The scripts behind the checks
>>>>>>> NEW

### EDIT 6: Remark after Theorem 2.7, citation
<<<<<<< OLD
of Theorem 1.14 (Remark 2.11, P11), and Theorem 2.7 does not claim it.
=======
of Theorem 1.14 (Proposition 2.11, P11; revised after K10, 2026-10-22), and Theorem 2.7 does not claim it.
>>>>>>> NEW

### EDIT 7: §7 item 1
<<<<<<< OLD
   - That is a (V2) failure for the passer, not a gap in Theorems 1.14 or 2.4, which assume (V2). The
     certificate of Remark 2.11 detects it through (L2).
=======
   - That is a (V2) failure for the passer, not a gap in Theorems 1.14 or 2.4, which assume (V2). With
     frozen kings, Proposition 2.11 detects it through (H5), the timing bound over all of the opponent's pawns;
     with real kings only the square-rule CONJECTURE of Remark 2.11 applies (revised after K10, 2026-10-22).
>>>>>>> NEW

### EDIT 8: §7 item 5
<<<<<<< OLD
   - Remark 2.11 requires the passer's local game to contain both kings.
=======
   - Proposition 2.11 is proved only with frozen kings. With real kings the defender's king may catch the
     passer (`Ka1 ka6 Pc2 w -` is (W, W) frozen and (D, D) with real kings); the real-king form is the square-rule
     CONJECTURE of Remark 2.11 (revised after K10, 2026-10-22).
>>>>>>> NEW
