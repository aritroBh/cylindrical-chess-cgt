# K30: a hand proof that P7 w is a draw (LOOPY open question 7)

Position X = `Ke6 Pd7 kd8 pe7`, White to move, on cyl:8x8 and on flat:8x8.

**Theorem.** In X, on both boards:

- (0) White has exactly four legal moves: Ke5, Kd5, Kf5, Kf7. Kd6, Kf6 and Kxe7 are illegal.
- (A) White cannot win. This holds in P, in EPW, in EPB and in chess.
- (B) After each of Ke5, Kd5, Kf5, Black cannot win. This holds in P, in EPW, in EPB and in chess.
- (C) Kf7 loses in P: Black wins with ...e5 and runs the pawn.
- So X is D in P, EPW, EPB and chess, and each of the three sorties draws.

Lemma 2.7a is **not needed**. The arguments are about plays without any promotion (except (C)), so they are valid in
all four games at once. They also give, as a by-product, the two statements that Lemma 2.7a would need (no White win
in EPW, no Black win in EPB).

A note on what the open question asked. The question was phrased in terms of Black having "no forced promotion and no
forced mate" after a sortie. That is part (B). "White cannot win" is part (A), and it is short. Lemma 2.9 refutes (L1)
for a defender who may pass. White cannot pass, so (B) needs a blockade rule that makes a move every turn. That rule is
Lemma D below.

## 0. Conventions

- Rules are those of `kings/SPEC.md`. P: the first promotion wins for the promoter. EPW (EPB): every promotion, by
  either side, is a White (Black) win. In all games a mate wins, and stalemate and infinite play are draws.
- Kings are never adjacent. A king may not step onto a square adjacent to the other king. Only a pawn or a king
  attacks a square here, because there are no officers. A king alone never gives check.
- N(s) is the set of squares adjacent to s (at most 8). Two squares s, t that are not adjacent have
  |N(s) ∩ N(t)| ≤ 3. (If t = s + (2, 0), the common neighbours are s + (1, -1), s + (1, 0), s + (1, 1); the cases
  (2, 1) and (2, 2) give 2 and 1.) For a corner s, |N(s) ∩ N(t)| ≤ 2. On the cylinder the same counts hold, because
  the width is 8.
- **Lemma K (a king always has a move).** Let the mover's king stand on s and the enemy king on t, not adjacent to s.
  Let there be no enemy pawn, and at most one own pawn, which stands on d7 or e7. Then the mover has a legal king
  move. If s is not a corner of a flat board, it has one to a square that is not such a corner.
  *Proof.* Call a neighbour of s *free* if it is not adjacent to t and does not hold the own pawn. A free square is a
  legal destination, because the enemy has no pawn and the kings are not adjacent afterwards.
  - s has 8 neighbours: at most 3 are adjacent to t and at most 1 holds the pawn, so at least 4 are free, and at most
    one of them is a corner.
  - s has 5 neighbours (a board-edge square that is not a corner): at least 5 - 3 - 1 = 1 is free. If s is next to a
    flat corner, the own pawn (d7 or e7) is not adjacent to s, so at least 2 are free and at most one is the corner.
    If s is not next to a corner, no neighbour is a corner.
  - s is a flat corner (3 neighbours): at most 2 are adjacent to t, and the pawn is not adjacent to s, so 1 is free.
  The cylinder has no corners (rank 1 and rank 8 squares have 5 neighbours). ∎

## 1. The legal moves at X (statement 0)

White: Ke6 has the neighbours d5, e5, f5, d6, f6, d7, e7, f7. d7 holds its own pawn. d6 and f6 are attacked by the
Black pawn e7. e7 holds the Black pawn, which is protected by kd8, so Kxe7 is illegal. d5, e5, f5, f7 are free and
not adjacent to d8. The pawn d7 cannot move: d8 is occupied and c8, e8 are empty. So the four moves are Ke5, Kd5,
Kf5, Kf7. (Wrap-around on the cylinder adds nothing: the files near d..f do not touch the seam.)

## 2. Part A: White cannot win

After any of the four moves the White king is not adjacent to d7 (the distances from d7 are 2, 2, 2, 2). Black's king
is not in check (the pawn d7 attacks c8 and e8; the kings are not adjacent). So **...Kxd7** is legal.

Then White has a king and nothing else. It has no pawn, so it can never promote. A king alone never gives check, so
Black is never mated. Hence White cannot win in P, in EPB and in chess, whatever Black does afterwards. (Black may
promote its pawn; that is a Black win in P and EPB and is harmless here.)

**EPW.** In EPW a Black promotion is a White win, so Black needs a rule that never promotes.
Black's rule tau: **never move the pawn; move the king to any free neighbour that is not a corner of a flat board.**
Black always has such a move by Lemma K (the own pawn is e7, the enemy king is White's, no White pawn exists). The
king never enters a corner, so Lemma K applies again at the next turn. If White captures the pawn the game is K against
K and nothing more can happen. So White cannot win EPW either. ∎

## 3. Part C: Kf7 loses in P

After Kf7 Black plays **...e5** (e6 and e5 are empty). From then on Black keeps the king on d8 and pushes the pawn every
move: e4, e3, e2, e1=Q. That is four more Black moves after e5.

- Black is never in check. d8 is attacked by no White piece: the pawn d7 attacks c8 and e8, and the king may not be
  adjacent to d8. The Black king never moves.
- The White pawn d7 cannot move (d8 is occupied) and has nothing to capture.
- Let W_1, ..., W_4 be White's moves after ...e5, each followed by Black's push p_k. The pawn stands on rank 6 - k before
  W_k, and p_k takes it to rank 5 - k. The White king starts on rank 7 and moves one rank per move at most, so
  before W_k it is on rank at least 8 - k, and after W_k on rank at least 7 - k.
  - It cannot capture the pawn on W_k: that needs it on rank at most 7 - k before W_k (adjacent to rank 6 - k),
    but it is on rank at least 8 - k.
  - It cannot block p_k: that needs it on the square directly in front, rank 5 - k, after W_k, but it is on rank at
    least 7 - k.
  - No White pawn can take the pawn en passant.
- So the push is always available, Black never stalemated, and p_4 promotes. P is a Black win. ∎

This is 9 plies after Kf7, 10 plies from X, which is the T = 10 of the local game (T counts plies from the sortie).
It is shorter than the line in which Black first takes d7. The claim is for P. In chess it is not claimed (and it is
not needed for (A) or (B)).

## 4. Part B: White does not lose after a sortie

Let s be one of e5, d5, f5. After Ks, Black's legal moves are (the king d8 has the neighbours c8, e8 attacked by the
pawn d7, e7 own pawn, c7 free, d7 unprotected):

| Black move | White answer (strategy sigma) | Then |
|---|---|---|
| ...Kxd7 | the rule of Lemma D | king and pawn e7 against king (4.1) |
| ...Kc7 | Ke6 | see below |
| ...e6 (the pawn is next to the White king and unprotected) | Kxe6 | free mode (4.2) |
| ...e5 (only after Kd5 or Kf5; after Ke5 e5 is occupied) | Kxe5 | free mode |

For ...Kc7: White plays Ke6 (e6 is free and not adjacent to c7). Black's moves are Kd8, Kb8, Kb7, Kb6, Kc6 (c8 is
attacked by d7, d6 is adjacent to the White king, d7 is protected, the pawn e7 is blocked by the king). After ...Kd8
the position is X again and White repeats sigma (the play is infinite: a draw). After the other four moves the pawn e7
is unprotected and White plays Kxe7: free mode.

**4.2 Free mode.** White has the king and the pawn d7. Black has only a king (or nothing). White's rule: play any
king move, never the pawn. By Lemma K White always has one. So White is never forced to promote. Black cannot mate
(a lone king never gives check) and cannot promote. If Black takes d7 the game is K against K. So Black cannot win.

**4.1 Lemma D (the blockade without a pass).** The positions: Black pawn on the e-file, rank r (2 ≤ r ≤ 7), White
king w, Black king b, nothing else, **Black to move**. Relative coordinates (x, y): file offset from e and
rank offset from r, so the pawn is (0, 0), it advances to (0, -1), and a square on file d or f is x = -1 or +1.
Name five squares (for the pawn on rank r):

    F = (0,-1)    M = (0,-2)    L = (-1,-2)    R = (+1,-2)

For r = 7: F = e6, M = e5, L = d5, R = f5. The pawn attacks (-1,-1) and (+1,-1).
Let Z_L = {x in {1, 2}, -3 ≤ y ≤ 0} (files f, g, ranks r-3..r) and Z_R = {x in {-1, -2}, -3 ≤ y ≤ 0} (files d, c).

The invariant **S** (Black to move):

- r = 4..7: (F) w = F, any b. (M) w = M, any b. (L) w = L and b not in Z_L. (R) w = R and b not in Z_R.
- r = 3: w = e2 (= F), any b. w = e1 (= M) and b not in {d3, f3}. w = d1 (= L) and b = d3. w = f1 (= R) and b = f3.
- r = 2: w = e1 and b in {d3, f3}.

(All positions are legal: the kings are not adjacent.)

White's rule rho (White to move, pawn on rank r, king on w):

1. If the White king can legally capture the pawn, it does.
2. If w = F: go to M.
3. If w = M: go to F if that is legal; otherwise go to L if b is on file d, to R if b is on file f.
4. If w = L or R: go to M if legal, otherwise to F.
5. If w is (±1, -1) (the pawn has just stepped and checks the king) and rule 1 is not legal: go to F, the square
   below the pawn.

**Lemma D.** Let a position of S be given with Black to move. After every legal Black move, rho gives a legal White
move, and the result is one of: K against K (the pawn was captured); White stalemated (no legal move, not in check);
or a position of S. In particular Black never has a promotion, White is never mated, and Black never wins.

*Proof.* By cases on w. The symmetric case R is the mirror of L. Notation: "b' ~ s" means b' adjacent to s. A legal
Black king move goes to b' not adjacent to w.

**Case F** (any r = 3..7). The pawn is blocked. Black moves the king to b'.
- If b' is not adjacent to the pawn, the pawn is unprotected, the king (adjacent to it) captures it: rule 1, K against K.
- Otherwise b' is in N(0,0) minus N(F), which is {(-1,1), (0,1), (1,1)} (the squares (±1,0) are adjacent to F).
  Rule 2: go to M. M is at least 3 ranks from b', so it is legal. The result is (M, b'), in S. For r = 3: b' is
  d4, e4 or f4, not d3 or f3, so it is in S. ✓.

**Case M** (r = 3..7, w = M).
- *Pawn step* (to F, which is empty; the double step at r = 7 is blocked by w). The pawn p' = (0,-1) now stands directly
  above w. If b is not adjacent to p', rule 1 captures: K against K. Otherwise b is in N(p') minus N(w), which is
  {(-1,0), (1,0)} (the square (0,0) was the pawn's square, so b is not there).
  - r ≥ 4: rule 2 sends w to M' = (0,-3), legal. For the new pawn this is its M, so the result is in S (r - 1 ≥ 4,
    M has no condition; for r = 4 the new rank is 3 and M' = e1 with b = d4 or f4, not in {d3, f3}, so it is in S).
  - r = 3: b would be d3 or f3, but S excludes these for (M, r = 3). So this does not occur: rule 1 captures.
- *King move to b'.* The king w is not adjacent to the pawn, so rule 1 does not apply. F is legal unless b' is adjacent
  to F, and N(F) minus N(M) = {(-1,0), (1,0)} (plus the pawn's square). If F is legal, the result is (F, b'), in S for
  every b'. If b' = (-1,0): go to L = (-1,-2), which is adjacent to w, at distance 2 from b', not attacked by the
  pawn: legal. The result is (L, b') with b' on file d, rank r, so b' is not in Z_L (x = -1) for r ≥ 4, and equals d3
  for r = 3. In S. If b' = (1,0): the mirror image.

**Case L** (r ≥ 4: w = L, b not in Z_L. r = 3: w = d1, b = d3).
- *Pawn step* (F empty). The pawn p' = (0,-1) attacks w = (-1,-2). If b is not adjacent to p', rule 1 captures. Otherwise
  b is in N(p') minus N(w) = {(1,-2), (1,-1), (1,0), (-1,0)} (and the empty square (0,0)). The first three lie in Z_L
  (r ≥ 4); for r = 3 the position (d1, d3) has b = (-1,0). So b = (-1,0). Rule 5: go to (0,-2), the square below p'.
  It is adjacent to w, not attacked by p', and at distance 2 from b = (-1,0): legal. The result is (F', b) where F'
  is the front square of the new pawn. For r - 1 ≥ 3 it is in S (case F has no condition on b). For r = 3
  the new pawn is on e2 and w = e1, b = d3: in S (the r = 2 family).
- *Double step* (r = 7 only). The pawn lands on (0,-2), next to w. If b is adjacent to it, b is in
  N((0,-2)) minus N(w) = {(1,-3), (1,-2), (1,-1)}, which is in Z_L, excluded. So the pawn is unprotected and rule 1
  captures it.
- *King move to b'.* Rule 1 does not apply. M = (0,-2) is adjacent to w. It is illegal exactly when b' is adjacent to M,
  and N(M) minus N(L) = {(1,-1), (1,-2), (1,-3)} (the squares (0,-1), (0,-3) are adjacent to L, so b' is not there).
  - r ≥ 4. If b' is not one of these three, rule 4 goes to M and the result (M, b') is in S. If b' = (1,-3): F is
    legal (F is illegal only for b' in N(F) minus N(L) = {(1,0), (1,-1), (1,-2), (-1,0)}), so rule 4 goes to F, in S. The cases b' = (1,-1) and
    (1,-2) (where both M and F are illegal) cannot occur: every neighbour of b' is either adjacent to w (so b is not
    there), or the pawn square, or in Z_L (so b is not there). For b' = (1,-1) the neighbours are (0,0), (0,-1),
    (0,-2), (1,0), (1,-2), (2,0), (2,-1), (2,-2); for b' = (1,-2) they are (0,-1), (0,-2), (0,-3), (1,-1), (1,-3),
    (2,-1), (2,-2), (2,-3). ✓.
  - r = 3: w = d1, b = d3. The king moves to b' in N(d3) not adjacent to d1: N(d3) = c2, d2, e2, c3, e3 (pawn), c4,
    d4, e4, and c2, d2, e2 are adjacent to d1. So b' is c3, c4, d4 or e4. Rule 4: e1 is legal (b' is on rank 3 or 4).
    The result (e1, b') has b' not in {d3, f3}: in S. ✓

**Case r = 2** (w = e1, b = d3 or f3; take d3). The pawn on e2 attacks d1 and f1 and is blocked by w. The king b moves
to b' in N(d3) not adjacent to e1: c2, c3, c4, d4, e3, e4 (d2 is adjacent to e1).
- b' in {c2, c3, c4, d4, e4}: not adjacent to e2, so the pawn is unprotected and Kxe2 is legal (rule 1).
- b' = e3: the pawn is protected. d1 and f1 are attacked by the pawn, d2 and f2 by the king, e2 is protected. White has
  no legal move and is not in check: stalemate, a draw. ∎

**Starting positions.** After a sortie and ...Kxd7, White to move: (Ke5, kd7): w = M, b = (-1,0). F = e6 is adjacent
to d7, so illegal. Rule 3 goes to L = d5: b = d7 is not in Z_L. Result in S. (Kd5, kd7): w = L. Rule 4 goes to M = e5,
legal. Result in S. (Kf5, kd7): w = R. Rule 4 goes to M = e5, legal. In S. So Lemma D applies from all three, and
Black cannot win.

## 5. Putting it together

- (0): section 1. (C): section 3. (A): section 2. (B): the table of section 4 and sigma: after a sortie every Black move
  is answered by sigma, and no play consistent with sigma contains a promotion (White never promotes; Black never has a
  promotion move) or a mate of White. So Black cannot win in P, in EPB and in chess. In EPW a Black win is a mate
  only (a Black promotion is a White win there), so sigma shows that Black cannot win EPW either.
- Together, X = D in all four games: (A) says no White win, (B) says no Black win.
- The proof is board-independent in its logic. It uses only: 8 ranks (the double step at r = 7 and the squares of rank
  r - 3 ≥ 1 for r ≥ 4), and files near c..g with no seam effect. The mechanical check below was run on cyl:8x8 and
  flat:8x8 only.

## 6. What the mechanical check covers

Own move generator `scripts/kpm.py`, written from `kings/SPEC.md` only. The strategies are coded in `scripts/k30lib.py`
exactly as stated above (the rule rho, the set S, the rule sigma), and nothing is read from solver tables.

- `check_kpk.py`: Lemma D. All 918 positions of S (per board: 201 for each r = 7, 6, 5, 4; 112 for r = 3; 2 for r = 2),
  all their Black moves (cyl: 6,777 pairs; flat: 5,985 pairs), the rule reply, and membership of the result in S.
  No exceptions. 1,488 distinct White-to-move positions arise. Replies: captures (cyl 2,467, flat 2,247),
  stalemates of White 2, replies landing in S (cyl 4,308, flat 3,736). The three start positions lead into S. Reached
  from the starts by play: 151 Black-to-move and 348 White-to-move positions.
- `check_A.py`: statement 0 (the four moves; the three illegal ones are not generated); Kxd7 exists after each; the
  rule tau against every White move (cyl: 3,348 White-to-move and 3,348 Black-to-move positions; flat: 3,164 and 3,164);
  Black always has a tau move, never promotes, is never in check. The Kf7 line: Black pushes every turn with the
  king on d8; the promotion comes after exactly four more pushes in every line (cyl 52, flat 47 White-to-move states).
- `check_B.py`: sigma against every Black move for each of the three sorties. Sigma is defined everywhere it is
  needed; White is never mated; Black never has a promotion move; in free mode White always has a king move
  (cyl: 3,694 / 3,696 / 3,696 White-to-move states for Ke5 / Kd5 / Kf5, of which 3,341 free mode; flat: 3,738 / 3,740 /
  3,740, of which 3,385).
- `compare.py`: the values of 15,536 (cyl) and 15,695 (flat) positions visited by the three checkers, from the own
  solver, K24's `mine.c` (models p, bb = EPW, bw = EPB) and K7's `kp_p.c --pmodel`: **0 differences** in P (own,
  `mine`, `kp_p`), in EPW and in EPB (own, `mine`). All positions of S and their White-to-move successors are D in P
  and in EPB; no position of sigma is L in P or EPB; no position of the tau check is W in EPW.
- `mutation_tests.py`: the closure check fails (as it must) if S is damaged (Z_L cut by one row; the r = 3 exclusion
  of d3, f3 dropped).

## 7. Labels

| Claim | Label |
|---|---|
| (0) the four White moves | PROVED (section 1), mechanically confirmed |
| (A) White cannot win (P, EPW, EPB, chess), both boards | PROVED (section 2, Lemma K) with a mechanical check |
| (B) Black cannot win after Ke5, Kd5, Kf5 (P, EPB, chess), both boards | PROVED (section 4, Lemmas D and K) with a mechanical check of S (all 918 positions per board) and of sigma |
| (C) Kf7 loses in P | PROVED (section 3) with a mechanical check; in chess not claimed |
| X = D in chess, both boards | PROVED directly; the K24 route through Lemma 2.7a is not needed and agrees |
| Values from three implementations on 15.5k positions | CHECKED-2 (agreement; three programs, 0 differences) |
| The same for the 6-rank analogue P5 | not covered; the method is likely to carry over, but nothing was run |
