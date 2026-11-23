# K47 PROOF: the K45 over group Z_O on cyl:8x6, by hand (partial)

AI work, no human re-derivation. Model P (Definition 1.5: SPEC.md rules, e.p. on, the first promotion wins for the
promoter, stalemate and endless play are draws). Board cyl:8x6: files a..h with h next to a, ranks 1..6; White
promotes on rank 6, Black on rank 1; a Black pawn on rank 5 may double-step. "dist" is the king distance with the
file wrap (max of the cyclic file distance and the rank distance).

    Z_O roots:  Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5   (root A, shuttler on d4)
                Kf5 kd5 Pb2 Pb4 Pe2 pa4 pb5 pe5   (root B, shuttler on d5)
    freezes:    q_A = Kf5 kd4 Pb2 Pb4 Pe4 pa4 pb5 pe5  (e2-e4 at root A)
                q_B = Kf5 kd5 Pb2 Pb4 Pe3 pa4 pb5 pe5  (e2-e3 at root B)

**What is proved here (PROVED, by hand):** the freeze q_A is a mutual zugzwang of P, i.e. clauses (O3) and (O4) of
Definition 4.8 (colour mirror) at root A hold, together with the existence of a freeze at root A ((O2) at A, first
half), and the move lists of all eight positions. The argument holds unchanged on every cyl:Wx6 with W >= 8
(Remark at the end).

**What is not proved by hand:** (O1) at both roots, (O3) and (O4) at q_B, and the claim that every White move at a
root other than the freeze loses (which is needed to know that e2-e4 and e2-e3 are the only freezes). These rest on
computation: K45 (CHECKED-2, four solvers) and K47 (own solver za agrees with ref3m on 66,997 sampled states of the
group's component, and its move counts and values at the eight positions equal K45's). So the exactness of Z_O as a
whole stays CHECKED-2, not PROVED. The solver trees (depth to the end in plies; `logs/tree_d3.txt`, the full trees of
the four freeze positions `logs/tree_q_full.txt`) show why a short case list does not suffice: the deepest lines
are 23 to 25 plies (root A, ...e5-e4 and ...e5-e3, met by Kf4), and the full proof tree of q_B with Black to move
alone has tens of thousands of nodes.

## 1. Move lists (hand-checked)

Squares attacked by the White pawns at the roots: b2: a3, c3; b4: a5, c5; e2: d3, f3. By the Black pawns: a4: b3,
h3; b5: a4, c4; e5: d4, f4. The kings: Kf5 covers e4..g6; kd4 covers c3..e5.

| position | side | legal moves |
|---|---|---|
| root A | Black | Kc4, Kd5 (shuttle), Ke3, a3, e4, e3 (6) |
| root A | White | Ke6, Kf6, Kg4, Kg5, Kg6, b3, e3, e4 (8) |
| root B | Black | Kc4, Kc6, Kd4 (shuttle), Kd6, a3, e4, e3 (7) |
| root B | White | Kf6, Kg4, Kg5, Kg6, b3, e3, e4 (7) |
| q_A | Black | Kc4, Kd3, Ke3, a3 (4) |
| q_A | White | Ke6, Kf6, Kg4, Kg5, Kg6, b3 (6) |
| q_B | Black | Kc4, Kc6, Kd6, a3, e4 (5) |
| q_B | White | Kf6, Kg4, Kg5, Kg6, b3, e4 (6) |

(At root A, Kxe5 is illegal because d4 guards e5, Kf4 because e5 attacks f4, Ke4 because it touches d4; at root B
Ke6 also touches d5. In q_A the pawn e4 covers d5 and f5, so Black's Kd5 is illegal and Black's e-pawn is blocked;
in q_B the pawn e3 covers d4 and f4. q_A carries the e.p. target e3 after the double step, but no Black pawn stands
on d4 or f4, so the flag changes nothing.) These counts are K45's (6, 7; 4, 5; 6, 6) and the solver's.

## 2. q_A with Black to move: every Black move loses ((O3) at root A)

**Lemma E (White's e-pawn runs).** White: pawn e4, king on d5 or d6, e5 and e6 empty; Black to move, with
(a) every Black pawn on rank 4 or higher, (b) if the White king is on d6, the Black king not next to e4,
(c) the Black king not on d6 or f6, (d) no Black pawn can ever check a king on the d-file (true whenever the Black pawns
are on the a- and b-files). Then White wins: e4-e5 and e5-e6.

*Proof.* Black moves (m1), White plays e5, Black moves (m2), White promotes on e6. The White king guards e5 and e6
(both squares touch d5 and d6), and on d5 also e4; by (b) on d6 the Black king cannot take e4 at m1. So Black can
neither take the pawn nor stand in front of it. By (a) a Black pawn needs at least three moves to promote, and Black
has two. By (d) White is never in check, so both pawn moves are legal. Black is never stalemated: if m1 was a king
move, at m2 the king can go back (that square is empty, still away from the unmoved White king, and e5 newly attacks
only d6 and f6, excluded by (c)); if m1 was a pawn move a4-a3 (the only pawn move that can occur), a3-a2 is available.
So the promotion comes first. ∎

**Lemma F.** Let White have Ke5, Pb4, Pe4 and either (i) Pb2 with a Black pawn a4, or (ii) Pa3 and no Black a-pawn;
Black: pb5 and the king on x ∈ {c3, c4, d3, e3} (x ≠ c3 in case (i), where b2 covers c3). Black to move. Then
White wins.

*Proof.* In case (i), if Black plays a4-a3, White plays bxa3, which gives case (ii) with Black to move and the same x.
Every other Black move is a king move (pb5 is blocked by b4 and has nothing to take on a4 or c4) to a square y next to
x with dist(y, e5) >= 2. White answers:
- Kd5 if dist(y, d5) >= 2;
- otherwise y touches d5 but not e5, so y ∈ {c4, c5, c6}; c5 is covered by b4 and c6 is not next to any x, so y = c4,
  and White plays Kd6 (dist(c4, d6) = 2).

d5 and d6 are not attacked by Black pawns (that needs a pawn on c6, e6, c7 or e7). Lemma E applies: (a) the Black pawns
are on a4 (or gone) and b5; (b) y = c4 is not next to e4; (c) dist(y, e5) >= 2 excludes d6 and f6; (d) the Black pawns
are on the a- and b-files. ∎

**Proposition 1. PROVED.** In q_A with Black to move every Black move loses.

*Proof.* The four moves of §1:
- Kc4, Kd3, Ke3: White plays Kxe5 (e5 is two squares from c4, d3 and e3, and no Black pawn guards it). This is Lemma
  F, case (i), with x = c4, d3, e3.
- a3: White plays bxa3. Black has only king moves (b5 blocked, e5 blocked by e4, nothing to capture), to x ∈ {c3, c4,
  d3, e3} (c5 is covered by b4, d5 by e4, e4 is guarded by Kf5). White plays Kxe5, legal for each x, giving Lemma F,
  case (ii). ∎

## 3. q_A with White to move: every White move loses ((O4) at root A)

Here Black's winning tool is the double step e5-e3 behind a king on d3 or d2. The White pawns stay on the a- and
b-files, so they never check a Black king on the d-file and never promote quickly: from b2 the fastest promotion is
b3, bxa4, a5, a6 (four moves), because b4 is blocked by b5.

**Lemma G (king on d3).** Black: king d3, pawn e3 (e2, e1 empty); White to move, its king not next to d1, e1 or f1,
its pawns on the a- and b-files with no promotion in its next two moves. Then Black wins (e2, e1).

*Proof.* The squares next to e1 are d1, d2, e2, f1, f2. At its first move White cannot take e3 or step to e2 (both
guarded by d3), nor to d2 or f2 (attacked by e3; d2 also touches d3), nor to d1 or f1 (not next to the king). Black
plays e2. At its second move White cannot take e2 (guarded) and cannot reach e1, because after its first move it
stands on none of d1, d2, e2, f1, f2. Black promotes on e1; the Black king is never in check. White is never
stalemated in the lines below (see the remark after Proposition 2). ∎

**Lemma G' (king on d2).** Black: king d2, pawn e5 with e4 and e3 empty; Black to move; White's pawns on the a- and
b-files with no promotion in its next three moves. Then Black wins: e5-e3, e2, e1. The squares e3, e2, e1 all touch
d2, so the White king can neither take the pawn nor stand in front of it. ∎

**Lemma H (after b2-b3).** White has just played b2-b3 (White pawns b3, b4; Black pawns a4, b5, Black king and the
rest anywhere, no White pawn able to promote within two moves). Black to move.
- If dist(K_W, a2) >= 3 and dist(K_W, a1) >= 3, Black wins by a4-a3, a2, a1.
- If dist(K_W, b2) >= 3 and dist(K_W, b1) >= 3, Black wins by a4xb3, b2, b1.

*Proof.* The pawn b3 attacks a4 and c4, so it can take neither a3 nor a2 (nor b2, b1 in the second line). To stop the
pawn the White king must take it or stand in front of it within two moves: in the first line it must reach a3 at
once, a2 within one move or a1 within two, all excluded by the distances (dist(K_W, a3) >= dist(K_W, a2) - 1 >= 2);
the second line is the same with b3, b2, b1. White's pawns b3 and b4 are blocked or have nothing to take, and White's
king never gives check. ∎

**Proposition 2. PROVED.** In q_A with White to move every White move loses.

*Proof.* The six moves of §1.
- **b3.** Lemma H, second line (White king f5: dist(f5, b2) = dist(f5, b1) = 4; White's e4 is blocked by e5, so White
  has no pawn that can promote).
- **K to s ∈ {e6, f6, g4, g5, g6}.** Black plays Kxe4 (e4 is not next to s, and no White pawn guards it). Then White to
  move; the White pawns are b2, b4.
  - W1 = b3: Lemma H. For s = e6, f6, g6, g5: dist(s, a2) = 4, 4, 4, 3 and dist(s, a1) = 5, 5, 5, 4, first line. For
    s = g4: dist(g4, a2) = 2 (g, h, a), so the second line: dist(g4, b2) = dist(g4, b1) = 3.
  - W1 = a king move to w1 (not next to e4): Black plays Kd3 (w1 is next to s, so it has rank >= 5, or it lies on the
    f-, g- or h-file; either way it does not touch d3; no White pawn covers d3). Now:
    - W2 = b3: Black plays e5-e3 (e4 and e3 are empty: the White king cannot stand on them, both touch d3). Lemma G,
      with White's king on w1 (rank >= 3, so not next to rank 1) and White's fastest promotion bxa4, a5, a6 three moves
      away.
    - W2 = a king move to w2. If w2 is on rank 3 or higher, or is not next to d1, e1, f1, Black plays e5-e3 and Lemma G
      applies. Since s has rank >= 4, w2 can be on rank 2 only for s = g4 (w1 = g3 or h3, w2 ∈ {f2, g2, h2, a2}); h2 and
      a2 are not next to d1, e1, f1. For w2 = f2 or g2 Black plays Kd3-d2 (it does not touch f2 or g2), White moves
      (W3: the king cannot reach e3 or e4 from f2 or g2 in one move, e3 touches d2), and Lemma G' applies (the b-pawn
      plan needs at least three more White moves after W3; if W3 = b3, four).
  ∎

*Remark (no stalemate).* In Proposition 1 Black is never stalemated (Lemma E's argument). In Proposition 2 White is
never stalemated: Black attacks no square of rank 6, on rank 5 only d5, e5 and f5 (next to a king on e4), and no
square of the g-file at all (its king stays on d2, d3 or e4; its pawns attack b3, h3, a4, c4, d4, f4, d2, f2, d1, f1).
A White king on rank 5 or 6 can step along rank 6; one on ranks 2 to 4 (only in the lines s = g4, g5) stands on the f-,
g-, h- or a-file and has a free neighbour on the g-file, or, on the a-file, the free square one rank up. (The solver
confirms every line as a decisive result, not a draw.)

**Corollary 3. PROVED.** At root A with White to move, e2-e4 does not lose (it reaches q_A with Black to move, a White
win), so root A has a freeze; q_A is a mutual zugzwang of P (0_D of Definition 4.4 in the P sense).

## 4. Widths

The proofs use only squares on files a to h around the group and distances to a1, a2, b1, b2 from the White king on
files e to h. On cyl:Wx6 with W >= 9 the move lists of q_A are the same (the extra files lie between h and a, where no
piece stands), the wrap distances from the e- to h-files to the a- and b-files only grow, and no new attack appears;
so Propositions 1 and 2 hold on every cyl:Wx6, W >= 8. (On W = 7 the file set is different: K45 found no group there.)

## 5. The rest: what the solver says (not proved)

Depths are plies to the end under best play (za/ztree, model P; the same values as K45's four solvers):
- root A, Black to move (O1): Kc4 11, Ke3 15, a3 11, e4 25, e3 23 (all answered by Kxe5, Kxe5, bxa3, Kf4, Kf4); the
  shuttle Kd5 (15) is answered by e2-e3 (root B's freeze).
- root A, White to move: Ke6 19, Kf6 13, Kg4 11, Kg5 11, Kg6 11, b3 7, e3 13 lose; e4 wins in 11 (Corollary 3).
- root B, Black to move (O1): Kc4 11, Kc6 11, Kd6 11, a3 11, e4 13, e3 25; the shuttle Kd4 (11) is answered by e2-e4.
- root B, White to move: Kf6 13, Kg4 11, Kg5 11, Kg6 11, b3 7, e4 13 lose; e3 wins in 15.
- q_B, Black to move (O3): Kc4 11, Kc6 11, Kd6 11 (Kxe5, Kxe5, e3-e4), a3 11 (bxa3), e4 13 (Kf4).
- q_B, White to move (O4): Kf6 15, Kg4 11, Kg5 11, Kg6 11, b3 7, e4 13.
A hand proof of these would follow the same pattern (the e-pawn races of Lemmas E, G and G' and the a/b-pawn race of
Lemma H) but needs more case splits; it was not written.
