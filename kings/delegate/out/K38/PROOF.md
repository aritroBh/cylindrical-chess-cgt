# K38: a hand proof that P5 w is a draw (LOOPY §8 item 7, the 6-rank analogue of 7.2)

Position X = `Kc4 Pb5 kb6 pc5`, White to move. This is Z_72 of LOOPY §5.2 (Pattern B with X = b, H = 6: WK (X+1, H−2),
WP (X, H−1), BK (X, H), BP (X+1, H−1)). LOOPY lists it on cyl:7x6. The proof below is written for cyl:7x6 and, with the
remarks marked *flat*, also holds on flat:7x6.

**Theorem.** In X, on cyl:7x6 and on flat:7x6:

- (0) White has exactly four legal moves: Kb3, Kc3, Kd3, Kd5. Kb4, Kd4, Kxc5 and every pawn move are illegal.
- (A) White cannot win. This holds in P, in EPW, in EPB and in chess.
- (B) After each of Kb3, Kc3, Kd3, Black cannot win. This holds in P, in EPW, in EPB and in chess.
- (C) Kd5 loses in P: Black wins with the double step ...c3 and runs the pawn (6 plies from X).
- So X is D in P, EPW, EPB and chess, and each of Kb3, Kc3, Kd3 draws.

This is K30's proof for 7.2 (`kings/delegate/out/K30/PROOF.md`), moved two files to the left and two ranks down. The
group stands against the top edge in both cases, so the geometry near the group is the same; the bottom edge is two
ranks closer, so the Black pawn has a shorter run (ranks 5 to 1 instead of 7 to 1) and the invariant has four pawn
ranks instead of six. Every step of K30's argument carries over; section 6 lists exactly what changes. Lemma 2.7a is not
needed: the arguments are about plays without any promotion (except (C)), so they hold in all four games at once.

## 0. Conventions

- Rules: `kings/SPEC.md`. P: the first promotion wins for the promoter. EPW (EPB): every promotion, by either side, is a
  White (Black) win. In all four games a mate wins, and stalemate and infinite play are draws. Chess differs from P only
  in what happens after a promotion.
- Black pawns move towards rank 1; a Black pawn on rank 5 (= H − 1) may double-step. A pawn attacks the two squares
  diagonally in front of it (with wrap-around on the cylinder). Only kings and pawns are on the board until a
  promotion, so only a pawn or a king attacks a square, and a king alone never gives check.
- Files a..g; on the cylinder g and a are adjacent. N(s) is the set of neighbours of s.
- For non-adjacent squares s ≠ t, |N(s) ∩ N(t)| ≤ 3 (file distance 2 gives 3, 2, 1 common neighbours for rank
  distance 0, 1, 2; file distance 3 gives none on width 7, since the neighbourhoods use files s−1..s+1 and s+2..s+4, and
  s+4 = s−3 ≠ s−1). If s is a flat corner, |N(s) ∩ N(t)| ≤ 2.

**Lemma K′ (a king always has a move).** Let the mover's king stand on s and the enemy king on t, not adjacent to s.
Let the enemy have no pawn, and the mover at most one pawn, on a square q. *Flat:* if s is a corner, let q not be an
orthogonal neighbour of s. Then the mover has a legal king move.

*Proof.* Call a neighbour of s *free* if it is not adjacent to t and is not q. A free square is a legal destination: it
is empty (t is not a neighbour of s), it is not attacked by a pawn (the enemy has none), and the kings are not adjacent
afterwards.
- 8 neighbours: at most 3 are adjacent to t and 1 is q, so at least 4 are free.
- 5 neighbours (a square on rank 1 or 6, or *flat* on file a or g, not a corner): at least 5 − 3 − 1 = 1 is free.
- *Flat* corner, 3 neighbours. If q is not a neighbour of s, at most 2 are adjacent to t and 1 is free. Otherwise q is the
  diagonal neighbour d of s (the hypothesis excludes the orthogonal ones). The two orthogonal neighbours u, v have
  N(u) ∩ N(v) = {s, d} (for s = a6: u = a5, v = b6, common neighbours a6, b5). t is neither s nor d (d holds the pawn),
  so t is adjacent to at most one of u, v, and one is free.
The cylinder has no corners. ∎

The orthogonal neighbours of the corners of flat:7x6 are a2, b1, f1, g2, a5, b6, f6, g5. The pawns to which Lemma K′ is
applied below are White's b5 and Black's c5, neither of which is among them.

## 1. The legal moves at X (statement 0)

Kc4 has the neighbours b3, c3, d3, b4, d4, b5, c5, d5. b5 holds the own pawn. b4 and d4 are attacked by the pawn c5.
c5 holds the Black pawn, protected by kb6, so Kxc5 is illegal. b3, c3, d3, d5 are empty, not attacked, and not adjacent
to b6 (d5 is two files from b6). The pawn b5 cannot move: b6 is occupied, a6 and c6 are empty. So the moves are Kb3,
Kc3, Kd3, Kd5. (The squares involved are on files b..d, so the seam between g and a adds nothing.)

## 2. Part A: White cannot win

After any of the four moves the White king is not adjacent to b5 (b3, c3, d3 are two ranks below it, d5 is two files
away). Black is not in check (b5 attacks a6 and c6; the kings are not adjacent). So **...Kxb5** is legal.

Then White has a lone king. It has no pawn, so it never promotes, and a lone king never gives check, so Black is never
mated. Hence White cannot win in P, in EPB and in chess, whatever Black does afterwards.

**EPW.** A Black promotion is a White win there, so Black needs a rule that never promotes.
Black's rule tau: **never move the pawn; play any legal king move.** By Lemma K′ (mover Black, own pawn c5 or none, no
White pawn) such a move always exists, so tau is defined at every turn and Black never promotes. If White takes
the pawn the game is K against K. So White cannot win EPW either. ∎

## 3. Part C: Kd5 loses in P

After Kd5 Black plays **...c3** (the double step: c4 and c3 are empty, the pawn stands on rank 5). From then on Black
keeps the king on b6 and pushes every move: c2, then c1 = promotion. That is two more Black moves after c3.

- Black is never in check: b5 attacks a6 and c6, and the White king is never adjacent to b6. The Black king never moves.
- The pawn b5 cannot move (b6 is occupied) and has nothing to capture. It cannot take en passant (it is not on rank 3).
- Let W_1, W_2 be White's moves after ...c3, each followed by Black's push p_k. Before W_k the pawn stands on rank 4 − k
  (rank 3, then rank 2), and p_k takes it to rank 3 − k. The White king is on rank 5 before W_1 and moves at most one rank
  per move, so it is on rank at least 6 − k before W_k and at least 5 − k after W_k.
  - It cannot capture the pawn on W_k: that needs the king on rank at most 5 − k before W_k.
  - It cannot block p_k: that needs the king on rank 3 − k (the square in front of the pawn) after W_k.
- So the push is always legal, Black is never stalemated, and p_2 promotes. P is a Black win. ∎

Plies: Kd5, c3, W_1, c2, W_2, c1 = 6 from X, the T = 6 that LOOPY records for the analogue. In chess the claim is not
made by hand; kpsolve (cap 2, exact) on both boards and K28's `ownref` (cap 1, exact, flat) give L.

## 4. Part B: White does not lose after Kb3, Kc3 or Kd3

Let s be b3, c3 or d3. After Ks Black's legal moves are as follows. kb6 has the neighbours a5, a6, b5, c5, c6 (rank 6 is
the top edge). a6 and c6 are attacked by b5, c5 is Black's own pawn, b5 is unprotected (the White king is two ranks
below it), and a5 is empty, not attacked and not adjacent to s. The pawn c5 may step to c4 (empty after the sortie), and
double-step to c3 when c3 is empty (after Kb3 and Kd3).

| Black move | White answer (strategy sigma) | Then |
|---|---|---|
| ...Kxb5 | the rule rho of Lemma D | king and pawn c5 against king (4.1) |
| ...Ka5 | Kc4 | see below |
| ...c4 (next to the White king, unprotected: b6 is two ranks away) | Kxc4 | free mode (4.2) |
| ...c3 (after Kb3 or Kd3 only; unprotected) | Kxc3 | free mode |

For ...Ka5: White plays Kc4 (c4 is empty, adjacent to b3, c3 and d3, two files from a5, and not attacked: c5 attacks b4
and d4). Black's moves from a5: on the cylinder a5 has the neighbours a4, a6, b4, b5, b6, g4, g5, g6; *flat* only the first
five. a6 is attacked by b5, b4 is adjacent to c4, b5 is protected by c4. The pawn c5 is blocked by c4 and has nothing to
capture (b4, d4 are empty). So Black has Kb6, Ka4 and, on the cylinder, Kg4, Kg5, Kg6.
- After ...Kb6 the position is X again. White repeats the same sortie; sigma depends only on the position, so the play
  is infinite or leaves the cycle by one of the other moves: a draw in the first case.
- After any other move c5 is unprotected (only a Black king adjacent to c5 could protect it; a4 is two files away, the
  g-file three files away on the cylinder), so **Kxc5** is legal: free mode.

(In P White could instead promote with b6 at once after ...Ka5; sigma does not, so that the same argument holds in
chess and in EPB.)

**4.2 Free mode.** White has the king and the pawn b5 (or no pawn); Black has a lone king. White's rule: **any legal king
move, never the pawn.** Lemma K′ (mover White, own pawn b5, no Black pawn) gives one every turn. So White never
promotes (relevant in EPB) and is never stalemated. Black cannot promote and a lone king never gives check, so Black
cannot win in any of the four games. If Black takes b5 the game is K against K.

**4.1 Lemma D (the blockade without a pass).** The positions: Black pawn on the c-file, rank r (2 ≤ r ≤ 5), White king w,
Black king b, nothing else, **Black to move**. Relative coordinates (x, y): file offset from c and rank offset from r, so
the pawn is (0, 0) and advances to (0, −1). On the cylinder x is taken in −3..3 (d, e, f = 1, 2, 3; b, a, g = −1, −2,
−3). Name the squares

    F = (0,−1)    M = (0,−2)    L = (−1,−2)    R = (+1,−2)

For r = 5: F = c4, M = c3, L = b3, R = d3. The pawn attacks (−1,−1) and (+1,−1).
Let Z_L = {x ∈ {1, 2}, −3 ≤ y ≤ 0} (files d, e, ranks r−3..r) and Z_R = {x ∈ {−1, −2}, −3 ≤ y ≤ 0} (files b, a).

The invariant **S** (Black to move):

- r = 4, 5: (F) w = F, any b. (M) w = M, any b. (L) w = L and b not in Z_L. (R) w = R and b not in Z_R.
- r = 3: w = c2 (= F), any b. w = c1 (= M) and b not in {b3, d3}. w = b1 (= L) and b = b3. w = d1 (= R) and b = d3.
- r = 2: w = c1 and b in {b3, d3}.

(Only legal positions: the kings are not adjacent and b is not the pawn's square. No position of S has White in check.)
|S| = 296 on each board: 113 for r = 5, 113 for r = 4, 68 for r = 3, 2 for r = 2.

White's rule rho (White to move, pawn on rank r, king on w):

1. If the White king can legally capture the pawn, it does.
2. If w = F: go to M.
3. If w = M: go to F if that is legal; otherwise to L if b is on file b, to R if b is on file d.
4. If w = L or R: go to M if legal, otherwise to F.
5. If w is (±1, −1) (the pawn has just stepped and checks the king) and rule 1 does not apply: go to F, the square below
   the pawn.

**Lemma D.** Let a position of S be given, Black to move. Black has no promotion, and after every legal Black move rho
gives a legal White move, and the result is one of: K against K (the pawn was captured); White stalemated (no legal
move, not in check); a position of S. In particular Black never promotes, White is never mated, and Black never wins.

*Proof.* No Black move from S promotes: for r ≥ 3 the pawn lands on rank ≥ 2, and for r = 2 it is blocked by w = c1 and
has nothing to capture (White has no pawn, and a pawn never captures a king). Below, "b′ ~ s" means b′ adjacent to s; a
legal Black king move goes to some b′ not adjacent to w. The cases by w follow; R is the mirror image of L (see the
remark after the proof).

**Case F** (r = 3..5, w = F). The pawn is blocked (the single step and, at r = 5, the double step pass through F). Black
moves the king to b′.
- If b′ is not adjacent to the pawn, the pawn is unprotected and the king, adjacent to it, captures it: rule 1, K
  against K.
- Otherwise b′ is in N(0,0) minus N(F) minus {F}, which is {(−1,1), (0,1), (1,1)} (the squares (±1,0), (±1,−1) are
  adjacent to F). Rule 2: go to M. M is three ranks from b′, not attacked by the pawn, and empty: legal. The result
  (M, b′) is in S: for r ≥ 4 there is no condition; for r = 3, b′ is on rank 4, not b3 or d3. ✓

**Case M** (r = 3..5, w = M).
- *Pawn step* to F (F is empty: b is not on F, which is adjacent to w; the double step at r = 5 would land on M, which is
  occupied). The pawn p′ = (0,−1) stands directly above w and does not attack it. If b is not adjacent to p′, rule 1
  captures: K against K. Otherwise b is in N(p′) minus N(w) minus {(0,0)} = {(−1,0), (1,0)} ((0,0) is the square the
  pawn just left, and b was not on it).
  - r ≥ 4: w is the new pawn's F, rule 2 sends w to (0,−3), the new pawn's M: it exists (r − 3 ≥ 1), it is three ranks
    from b and not attacked by p′ (which attacks (±1,−2)): legal. The result is in S: for r = 5 the new rank is 4 and M has
    no condition; for r = 4 the new rank is 3, the new M is c1 and b is b4 or d4, not in {b3, d3}. ✓
  - r = 3: b would be b3 or d3, which S excludes for (M, r = 3). So this does not occur, and rule 1 captures.
- *King move to b′.* w is two ranks from the pawn, so rule 1 does not apply. F is empty and not attacked by the pawn; it
  is illegal exactly when b′ ~ F, and N(F) minus N(M) minus {M} = {(−1,0), (1,0), (0,0)}, where (0,0) is the pawn. So F
  is legal unless b′ = (±1,0).
  - F legal: the result (F, b′) is in S for every b′ (for r = 3 the family w = c2 has no condition).
  - b′ = (−1,0) (file b): F is illegal and rule 3 goes to L = (−1,−2). L is adjacent to M, two ranks from b′, not
    attacked (the pawn attacks (±1,−1)) and empty: legal. The result (L, b′): b′ has x = −1, so it is not in Z_L (r ≥ 4;
    on the cylinder −1 ≢ 1, 2 mod 7), and for r = 3 it is (b1, b3). In S. ✓
  - b′ = (1,0) (file d): the mirror image, the result (R, b′) with b′ not in Z_R, or (d1, d3). ✓

**Case L** (r = 4, 5: w = L, b not in Z_L. r = 3: w = b1, b = b3).
- *Pawn step* to F (empty: F ~ L, so b is not there). The pawn p′ = (0,−1) attacks (±1,−2), which includes w = (−1,−2).
  If b is not adjacent to p′, rule 1 captures: K against K. Otherwise b is in N(p′) minus N(w) minus {(0,0)} =
  {(1,−2), (1,−1), (1,0), (−1,0)}. The first three lie in Z_L (r ≥ 4), and for r = 3 b is b3 = (−1,0). So b = (−1,0).
  Rule 5: go to (0,−2), the square below p′. It is adjacent to w, not attacked by p′, two ranks from b, empty: legal.
  The result has w on the new pawn's F: for r − 1 ≥ 3 it is in S (the F family has no condition); for r = 3 the new pawn
  is on c2, w = c1, b = b3: in S (the r = 2 family). ✓
- *Double step* (r = 5 only; c4 and c3 are empty because w is on b3). The pawn lands on (0,−2) = c3, next to w, and does
  not attack w (it attacks (±1,−3)). It is protected only if b is adjacent to it, that is b in N((0,−2)) minus N(w) minus
  {w} = {(1,−3), (1,−2), (1,−1)}, which is in Z_L, excluded. So the pawn is unprotected and rule 1 captures it: K against
  K. (The e.p. right is irrelevant: White has no pawn.)
- *King move to b′.* w is two ranks from the pawn, so rule 1 does not apply. M = (0,−2) is adjacent to w, empty and not
  attacked; it is illegal exactly when b′ ~ M, and N(M) minus N(L) minus {L} = {(1,−1), (1,−2), (1,−3)}.
  - r ≥ 4. If b′ is none of these three, rule 4 goes to M and (M, b′) is in S. If b′ = (1,−3): F = (0,−1) is adjacent to
    w, empty, not attacked (the pawn attacks (±1,−1)), and not adjacent to b′ (two ranks apart), so rule 4 goes to F: in
    S. The cases b′ = (1,−1) and (1,−2) cannot occur: every neighbour of b′ is adjacent to w, or is the pawn's square, or
    lies in Z_L, so b was not there. For b′ = (1,−1) the neighbours are (0,0) (pawn), (0,−1), (0,−2) (adjacent to L), and
    (1,0), (1,−2), (2,0), (2,−1), (2,−2) (in Z_L); for b′ = (1,−2) they are (0,−1), (0,−2), (0,−3) (adjacent to L) and
    (1,−1), (1,−3), (2,−1), (2,−2), (2,−3) (in Z_L). ✓ (For r = 4, y = −3 is rank 1, which exists and is in Z_L.)
  - r = 3: w = b1, b = b3. N(b3) = a2, b2, c2, a3, c3, a4, b4, c4; a2, b2, c2 are adjacent to b1 and c3 is the pawn, so
    b′ is a3, a4, b4 or c4. Rule 4: c1 is adjacent to b1, not attacked (c3 attacks b2, d2), and two or more ranks from
    b′: legal. The result (c1, b′) has b′ not in {b3, d3}: in S. ✓

**Case R** (w = R, b not in Z_R; r = 3: w = d1, b = d3): the mirror image of case L under x ↦ −x.

**Case r = 2** (w = c1, b = b3 or d3; take b3, the other is the mirror). The pawn c2 attacks b1 and d1 and is blocked
by c1. The Black king moves to b′ in N(b3) not adjacent to c1: a2, a3, a4, b4, c3, c4 (b2 is adjacent to c1, c2 is the
pawn).
- b′ in {a2, a3, a4, b4, c4}: b′ is not adjacent to c2, so the pawn is unprotected and Kxc2 is legal (rule 1).
- b′ = c3: the pawn is protected. b1 and d1 are attacked by the pawn, b2 and d2 are adjacent to c3, c2 is protected.
  White has no legal move and is not in check (c2 attacks b1, d1, not c1): stalemate, a draw. ∎

*Remark on the mirror (R from L, d3 from b3).* On cyl:7x6 the reflection x ↦ −x about the c-file (files b ↔ d, a ↔ e,
g ↔ f) is a symmetry of the board, so case R is literally case L reflected. On flat:7x6 it is not a symmetry, but the
argument for case L only names squares with |x| ≤ 2 (files a..e), which exist on both sides of c; the files f and g that
have no mirror image only add squares where Black's king may stand, and every claim about them in the reflected argument
("b′ is one of ...", "every neighbour of b′ is ...") is a claim about a subset of the listed squares. So the reflected
argument goes through line by line. The mechanical check below covers both boards and both cases.

**Starting positions.** After a sortie and ...Kxb5, White to move:
- (Kc3, kb5): w = M, b = (−1,0). F = c4 is adjacent to b5, so illegal; b is on file b, so rule 3 goes to L = b3 (adjacent
  to c3, two ranks from b5, not attacked by c5). The result (b3, b5) has b = (−1,0) not in Z_L: in S.
- (Kb3, kb5): w = L. Rule 4 goes to M = c3 (adjacent to b3, two ranks from b5, not attacked by c5): in S.
- (Kd3, kb5): w = R. Rule 4 goes to M = c3: in S.

So Lemma D applies from all three, and Black cannot win. (These replies, Kb3–c3, Kc3–b3 and Kd3–c3, are exactly the moves
that kpsolve and ref3m list as the only drawing moves in these positions; every other king move loses, in P and in chess.)

## 5. Putting it together

- (0): section 1. (C): section 3. (A): section 2. (B): the table of section 4 and sigma: after Kb3, Kc3 or Kd3 every Black
  move is answered by sigma, and no play consistent with sigma contains a promotion (White never moves the pawn; Black
  never has a promotion move in Lemma D, and in free mode Black has no pawn) or a mate of White. So Black cannot win in
  P, in EPB and in chess. In EPW a Black win is a mate only, so sigma shows that Black cannot win EPW either.
- Together: X = D in all four games, on both boards. (A) says no White win; (B) says no Black win.
- As a by-product, the two statements Lemma 2.7a needs (no White win in EPW from X, no Black win in EPB from X) are proved
  by hand, but the lemma is not used.

## 6. Where the K30 method needed changes (item 3 of the brief)

It does not break. The changes, all checked above:

1. **Translation.** Every square of K30's proof moves by (−2 files, −2 ranks): e6 → c4, d7 → b5, d8 → b6, e7 → c5; the
   sorties Ke5, Kd5, Kf5, Kf7 become Kc3, Kb3, Kd3, Kd5; ...Kc7 becomes ...Ka5 and Ke6 becomes Kc4.
2. **Shorter run.** The pawn starts on rank 5 = H − 1, so S has the pawn ranks 5, 4 (general family), 3 and 2 (special
   families), instead of 7..4, 3, 2. The general family needs the rank r − 3 ≥ 1, which holds for r = 4, 5. The double
   step is at r = 5 instead of r = 7. |S| = 296 per board instead of 918.
3. **The losing sortie is faster.** Kd5 (the analogue of Kf7) loses with the double step ...c3 at once, 6 plies from X,
   instead of 10.
4. **Width 7 and the seam.** |N(s) ∩ N(t)| ≤ 3 needs width ≥ 5; it holds. After ...Ka5 Kc4 the cylinder gives Black three
   extra moves through the seam (Kg4, Kg5, Kg6), all met by Kxc5. In Lemma D the files f and g (x = ±3, adjacent through
   the seam) never enter an adjacency claim.
5. **Lemma K.** K30's Lemma K is stated for an own pawn on d7 or e7, and its flat-board clause ("if s is next to a flat
   corner, the own pawn is not adjacent to s") is false here on flat:7x6: Black's c5 is adjacent to b6 and White's b5 to
   a5 and b6, both next to the corner a6. Lemma K′ drops the corner-avoiding clause and proves instead that a corner also
   has a move (the pawn b5 is only a *diagonal* neighbour of a6). On cyl:7x6, the board LOOPY lists, K30's argument applies
   unchanged (no corners).

## 7. What the mechanical check covers

Own move generator `scripts/p5gen.py`, written from `kings/SPEC.md` only (kings, pawns, double step, en passant, wrap,
legality, mate and stalemate; promotion ends the game in P, EPW, EPB). `scripts/p5check.py` codes S, rho, sigma and tau
exactly as stated above; nothing is read from solver tables. Logs `logs/p5check_cyl.log`, `logs/p5check_flat.log`.

- Statement 0: exactly the four moves; no pawn move.
- Lemma D: all 296 positions of S (per board), every Black move (cyl 1,991 pairs, flat 1,728), the rule's reply, and
  membership of the result in S. 0 failures. Replies: captures (cyl 789, flat 693), White stalemated 2, back in S (cyl 1,200,
  flat 1,033); 504 (cyl) and 499 (flat) distinct White-to-move positions.
- Part A: Kxb5 after each White move; tau against every White move: Black always has a king move and is never in check,
  White never has a pawn (cyl 2,724 and flat 2,788 positions each side to move).
- Part C: after Kd5 c3, against every White move Black's push is legal, and after the second White move the promotion is
  available (43 White-to-move states per board).
- Part B: sigma against every Black move for each of the three sorties; sigma is always defined, White is never mated,
  Black never has a promotion, every rho reply lands in S (cyl 2,462 / 2,460 / 2,462 and flat 782 / 775 / 782 distinct
  White-to-move positions for Kb3 / Kc3 / Kd3).
- Mutation tests (`logs/mutation_tests.log`): cutting one row from Z_L or from Z_R, or dropping the r = 3 exclusion of
  b3, d3, makes the closure check fail on both boards, as it must.
- Values: the own solver (P, EPW, EPB) on all 27,688 (cyl) and 28,373 (flat) positions reachable from X agrees with
  `kp_p --pmodel` (K7) and with `ref3` (K23) on every position in P (0 differences; `logs/compare.log`). No position of S or
  of its White-to-move successors is L in P.

## 8. Labels

| Claim | Label |
|---|---|
| (0) the four White moves | PROVED (section 1), mechanically confirmed |
| (A) White cannot win (P, EPW, EPB, chess), cyl:7x6 and flat:7x6 | PROVED (section 2, Lemma K′) with a mechanical check |
| (B) Black cannot win after Kb3, Kc3, Kd3 (P, EPW, EPB, chess), both boards | PROVED (section 4, Lemmas D and K′), with a mechanical check of S (296 positions per board) and of sigma |
| (C) Kd5 loses in P, T = 6 | PROVED (section 3) with a mechanical check |
| Kd5 loses in chess | CHECKED-2 on flat:7x6 (kpsolve cap 2 exact, `ownref` cap 1 exact); COMPUTED-1 on cyl:7x6 (kpsolve cap 2 exact) |
| X = D in P and in chess, both boards | PROVED directly; Lemma 2.7a not needed |
| P values on all positions reachable from X | CHECKED-2 (own solver, `kp_p --pmodel`, `ref3`; 0 differences) |

The proof has not been re-derived by a referee.
