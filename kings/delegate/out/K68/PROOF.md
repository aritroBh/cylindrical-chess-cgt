# K68: the seven-man group C125_05 by hand

`Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` on the ordinary 8×8 board. One AI proof (K68, 2026-11-25), not yet refereed.

## 0. Summary

Labels: **PROVED** = complete hand proof below; **PROVED given KNOWN** = hand proof that uses a named standard or
tablebase fact; **CHECKED-2** = two separately written programs agree; **COMPUTED-1** = one program only.

| statement | label |
|---|---|
| (O0) no king in check at the roots and q's; no e.p. right | PROVED (§2) |
| (O1) Black's only moves are king moves; the shuttle b4↔b5 is legal; each of the six other root moves (…Ka3, …Ka4, …Ka5 at b4; …Ka4, …Ka5, …Ka6 at b5) loses at once | PROVED (Lemma A, §3) |
| (O2) c2–c4 at b4 and c2–c3 at b5 do not lose (they win); no White root move promotes | PROVED |
| (O3) q1 and q2, Black to move: every Black move (…Ka3, …Ka4, …Ka5, …Kb3 in q1; …Ka4, …Ka5, …Ka6 in q2) loses at once | PROVED (Lemma A) |
| The wrong pawn step (c2–c3+ at b4, c2–c4+ at b5, c3–c4+ in q2) loses at once, given (O4) at the other q | PROVED (Lemma C) |
| Every White king move at the roots and in q1, q2 loses at once; hence the freezes are exactly c2–c4 (b4) and c2–c3 (b5), and (O4) holds | PROVED **given Lemma B** (Lemma C) |
| Lemma B: White to move, Black Kb6, pb7, pc6, one White pawn on c2, c3 or c4, White king on any legal square (not b4 when the pawn is on c4): Black wins P (162 positions) | **CHECKED-2** (o68 and the K65 referee's ax65 solver; no hand proof) |
| (B1) at all six bad moves: White wins beside −1 under the sum's rule | PROVED (Lemma A′, §4) |
| Proposition 4.25: G has the results of ω beside every finite D-game | PROVED given Lemma B (CHECKED-2); every other ingredient by hand |
| Chess: roots with Black to move lost for Black (every move); roots with White to move won for White (by the freeze); q1, q2 with Black to move lost for Black (every move) | PROVED given KNOWN (KQ against one pawn that is three or more moves from promotion, §6) |
| Chess: q1, q2 with White to move lost for White; every non-freeze White root move loses | KNOWN (Syzygy, K65 cache), not proved by hand |

What is not by hand is exactly the Black half: once White's king leaves d4, Black takes c5 and b6 and then wins a
long K + 2P against K + P ending (Lemma B, up to 20 Black moves with best defence). The proof reduces every Black-win
claim to Lemma B by hand. The White half (O1), (O3) and (B1) is one short strategy of eight moves.

## 1. The position and the rules

```
   a b c d e f g h
8  . . . . . . . .
7  . p . . . . . .
6  . P p . . . . .
5  . k P . . . . .     (b5 root: Black king on b5)
4  . k . K . . . .     (b4 root: Black king on b4)
3  . . . . . . . .
2  . . P . . . . .
1  . . . . . . . .
```

White Kd4, Pb6, Pc5, Pc2; Black K on b4 or b5, pb7, pc6. FEN `8/1p6/1Pp5/2P5/1k1K4/8/2P5/8` (b4) and
`8/1p6/1Pp5/1kP5/3K4/8/2P5/8` (b5). γ denotes White's c-pawn (on c2, c3 or c4).
q1 = Kd4, Pb6, Pc4, Pc5 / Kb4, pb7, pc6 (after c2–c4 at the b4 root); q2 = Kd4, Pb6, Pc3, Pc5 / Kb5, pb7, pc6
(after c2–c3 at the b5 root). x_m = the position after a non-shuttle Black root move m, White to move.

P: the promotion game: a promotion wins for the promoter and ends the play; checkmate loses; stalemate is a draw;
infinite play is a draw. Beside −1 (for (B1)): Black may once move elsewhere instead of on the board, not while in
check; a side with no move at all loses (so stalemate becomes a loss). Definition 4.8 is used in the clause form
(O0)–(O4) of the K61 packet §1.5, which is Definition 4.8 of `kings/theory/LOOPY.md` for over groups.

## 2. Static facts

**Fact 1 (the pawns).** While Pb6, Pc5 stand, pb7 is blocked by b6 and pc6 by c5, and no Black pawn can capture
(b7 attacks a6, c6; c6 attacks b5, d5; none holds a White unit). Pb6 is blocked by b7 and attacks a7, c7; Pc5 is
blocked by c6 and attacks b6, d6. So until a capture the only moves are king moves and steps of γ.

**Fact 2 (forbidden squares).** The Black king may never stand on a7 or c7 (Pb6) or on d6 (Pc5, while it stands);
b6 is protected by c5. The White king may never stand on b5 or d5 (pc6) or on a6 (pb7). γ on c_j forbids b_{j+1},
d_{j+1} to the Black king.

**(O0).** At both roots and at q1, q2 the kings are two files apart; Black's pawns attack b5, d5, a6, c6, not d4; γ
attacks b3/d3 (c2), b4/d4 (c3) or b5/d5 (c4), never the Black king's square (b4 with γ on c2 or c4; b5 with γ on c2
or c3). The double step c2–c4 gives no e.p. right (no Black pawn on b4 or d4). PROVED.

**Move lists.** Black at the b4 root: Ka3, Ka4, Ka5, Kb5 (b3: γ; c3, c4: next to Kd4; c5: protected by Kd4).
Black at the b5 root: Ka4, Ka5, Ka6, Kb4 (b6, c5 protected; c4 next to Kd4; c6 own pawn). Black in q1: Ka3, Ka4,
Ka5, Kb3 (b5 attacked by c4). Black in q2: Ka4, Ka5, Ka6 (b4 attacked by c3). White at the b4 root: Kd3, Ke3, Ke4,
Ke5, c2–c3+, c2–c4 (c3, c4 next to b4; d5 attacked; c5 own). White at the b5 root: Kc3, Kd3, Ke3, Ke4, Ke5, c2–c3,
c2–c4+. White in q1: Kd3, Ke3, Ke4, Ke5 (γ blocked by c5). White in q2: Kd3, Ke3, Ke4, Ke5, c3–c4+. So at the roots
every Black move is a king move and the shuttle is legal: the shuttle is the only Black move that keeps the
structure (the Black king on {b4, b5}), as (O1) requires.

## 3. White's plan: Lemma A (P)

Starting set 𝒜 (White to move; White Kd4, Pb6, Pc5, γ; Black pb7, pc6):
γ = c2 and Black king k₀ ∈ {a3, a4, a5, a6} (the boards x_m of the six bad moves; a4, a5 occur twice);
γ = c4 and k₀ ∈ {a3, a4, a5, b3} (q1 after each Black move); γ = c3 and k₀ ∈ {a4, a5, a6} (q2 after each Black move).
In all of them k₀ is at distance at least 2 from c5.

**Strategy S_A for White.**
1. King d4 → e5 → d6 → c7 (White's moves 1–3).
2. King on c7 or b8 with pb7 still on the board: if the Black king stands on a6, step to the other of c7, b8;
   otherwise take: K×b7.
3. King on b7 (after K×b7): step to c7, unless the Black king is next to c7; then to a7.
4. Then b6–b7, then b7–b8 (promotion).

**Lemma A. PROVED.** From every position of 𝒜, S_A promotes on b8 by White's 8th move, every move of S_A is legal,
and Black neither promotes before nor is ever stalemated. Hence every position of 𝒜 is a White win in P.

*Proof.* Write B_t for Black's t-th move (B_t comes after White's t-th).

(a) *Black cannot take c5 before B₃.* At B₁ the White king is on e5 and c5 is unprotected, but the Black king is on
k₀, not next to c5. Before B₂ the White king is on d6 and protects c5. So c5 falls at B₃ at the earliest, and until
then d6 is forbidden to Black (Fact 2), and so is c7 (Pb6, which stands until White's step 4).

(b) *Legality of steps 1 and 2.* Ke5: k₀ lies on the a- or b-file. Kd6: after B₁ the Black king is on files a–c and
rank ≤ 6 and the squares next to d6 that it could reach are c7 (forbidden) and c5, c6 (pawns); d6 is not attacked by a
Black pawn. Kc7: the squares next to c7 are b6, b7, c6 (pawns), b8, c8, d8, d7, d6; d6 is forbidden (a), and the
Black king cannot reach rank 7 or 8 by B₂: from rank ≤ 6 the entrances to rank 7 near the queenside are a7, c7
(forbidden), b7 (own pawn), and d7, e7 need a king on d6, e6 first; d6 is forbidden and e6 is at distance ≥ 3 from
every k₀ except b3, from which the only two-move route b3–c4/…–d5–e6 needs d5, which is next to Kd6 at B₂.
The squares next to b7 are a6, a7, a8, b8, c8, c6, c7, b6; of these the Black king can reach only a6 (a7 forbidden,
rank 8 unreachable as just shown, and the same argument covers B₃, B₄: d6 is next to Kc7 at B₃, and in the branch
with Kb8 the Black king is on a6 at B₃). So "b7 protected" means "Black king on a6", and K×b7 is legal otherwise.
Kb8 is legal (b8 is not next to a6). With the Black king on a6 and the White king on c7 or b8, Black to move must
leave a6: its moves are a5 (always legal: no White pawn on b4, White king not adjacent) and b5 (unless γ = c4); a7
is attacked by b6, b6 protected by c5 (c5 still stands: Black's king came to a6, it did not take c5), b7 own pawn.
After that White takes on b7. So K×b7 comes at White's move 4 or 5.

(c) *Where the Black king is when White plays K×b7: on rank ≤ 5.* If K×b7 is White's 4th move, the Black king made
three moves: it is not on a6 (b7 unprotected), not on b6/c6 (pawns), not on d6 (next to Kc7 at B₃), not on e6 or
beyond (as in (b)), so on rank ≤ 5. If it is White's 5th move, B₄ went from a6 to a5 or b5.

(d) *Steps 3 and 4 are legal and win.* After K×b7, Black makes B (from rank ≤ 5 to rank ≤ 6). Step 3: c7 and a7 are
not attacked by Black pawns (pc6 or what is left of it attacks rank ≤ 5); the Black king cannot be next to both (the
rank-≤6 squares next to c7 are b6, c6, d6; next to a7: a6, b6); both c7 and a7 protect b6, so b6 cannot be taken.
Step 4: b6–b7 (b7 is empty), the pawn on b7 is protected by the king on a7 or c7. b7–b8: b8 is empty, since the
Black king would have to stand next to b8 before Black's last move, i.e. on a7 or c7 (attacked by Pb6 until b6–b7),
on b7 (next to the White king on a7/c7), or on a8/c8, which it cannot reach in two moves from rank ≤ 5.
So White promotes on its move 7 or 8.

(e) *Black cannot promote first.* pb7 never moves (blocked by b6, then taken). pc6 can promote only after the c-file
is cleared of c5 and γ (γ cannot leave the c-file: there is no Black pawn for it to take) and the Black king has left
it. That takes at least K×c5, K×γ, one more king move off the c-file square of γ (the king then stands on the c-file
in front of the pawn; for γ on c4 the move K×c4 also leaves c5, but the king must still leave c4), and five pawn
moves: at least 8 Black moves, the first not before B₃. So Black promotes at B₁₀ at the earliest; White promotes by
its move 8, which comes before B₈. Black cannot mate either: the White king is never in check (pc6 and a pawn on
c5/c4 attack b5, d5, b4, d4, which the White king never visits after move 1) and S_A always supplies a legal move.

(f) *No stalemate* (stalemate would be a draw in P). Lemma A2: at every Black turn the Black king has a legal move to
the rank below its own (on the first rank: along it). At B₁ and B₂ the king is on files a–c within two steps of k₀;
on the a- or b-file the square a_{r−1} is free (no White pawn attacks the a-file below rank 7, the White king is on
e5/d6); on the c-file (only from k₀ = b3) the three squares below are on ranks ≤ 3 and free (γ on c4 attacks b5,
d5). From B₃ on, the White king stands on rank 7 or 8, so on ranks ≤ 5 the only squares the Black king may not enter
are the two squares attacked by γ (files b and d, one rank), and the square of its own c-pawn; c5 and γ, if present,
are unprotected (no White unit protects them any more) and may be taken. A king on rank r ≤ 6 off the c-file has a
square below it on the a-, e-, f-, g- or h-file, or a_{r−1} next to b, e_{r−1} next to d: free. On the c-file, the
three squares below are blocked only if Black's own pawn stands directly below and γ attacks the two others, i.e.
the pawn stands directly in front of γ; this needs K×c5, a king move off c5, two pawn moves and a return to c5 or
c6: not before B₈, which never comes. On rank 7 (only after K×b7, files d–h by (b)), e6 or f6 etc. below is free
(the White king is on the queenside, no White pawn attacks rank 6 there). ∎

The play is short: S_A promotes by White's 8th move from every position of 𝒜 (16 plies at most), which matches the
solver values W15 (after …Ka4 etc.) and L16 (q1, q2, Black to move).

**Consequences.** (O1): each of the six bad moves leads to 𝒜 (γ = c2), a White win: they lose at once. (O3): every
Black move in q1 and q2 leads to 𝒜: q1 and q2 with Black to move are lost for Black, every move loses at once, and a
move exists. (O2): c2–c4 at b4 and c2–c3 at b5 lead to q1, q2 with Black to move, White wins: these moves win, so
they do not lose at once; no White root move promotes (γ is on c2). All PROVED. The shuttle also loses (it leads to
the other root with White to move, which White wins by its freeze), as Definition 4.8 allows.

## 4. (B1): Lemma A′

**Lemma A′. PROVED.** For each of the six bad moves m, x_m (γ = c2, k₀ ∈ {a3, a4, a5, a6}) is a White win beside −1
under the sum's rule: S_A promotes by White's 9th move.

*Proof.* Black is never in check in S_A (White's king never checks; the only White pawn moves are b6–b7, which
attacks a8, c8, where the Black king never stands, and the promotion), so it may use its token at any turn; it clears
no right (there is none). The token changes nothing in Lemma A except at rule 2: if Black passes with its king on a6
and the White king on c7 or b8, White steps to the other square, and now Black, with no token, must move off a6. This
costs White one move, at most once. Every bound on Black's king in (a)–(d) counts Black's moves and only gets
better when one turn is a pass. Black still needs eight board moves from B₃ on to promote, i.e. its 11th turn with a
pass, and White promotes by its 9th move. Under the sum's rule a Black stalemate is a Black loss, which only helps
White, and (f) shows Black always has a board move anyway. ∎

There are no checks at x_m and no e.p. rights, so the sum's rule needs nothing more.

## 5. White's other moves: Lemma C (reduction) and Lemma B (computed)

**Lemma B. CHECKED-2, not proved by hand.** White to move, Black Kb6, pb7, pc6, White γ on c2, c3 or c4 and the
White king on any legal square: Black wins P, except γ = c4 with the White king on b4 (a draw). (162 positions:
161 Black wins, 1 draw; o68 and ax68q agree on every one, `logs/compare_values.txt`.)

**Lemma C. PROVED given Lemma B.** (i) Let R1, R2 be the roots and Q1, Q2 the q's, each with White to move. After
every White king move there (Kd3, Ke3, Ke4, Ke5 in R1, Q1, Q2; also Kc3 in R2) the position is a Black win.
(ii) c2–c3+ in R1, c2–c4+ in R2 and c3–c4+ in Q2 lose at once, given that Q1 and Q2 are Black wins.
(iii) Hence Q1 and Q2 are Black wins ((O4): a move exists, and every White move loses at once), and at R1, R2 every
White move except c2–c4 (R1), c2–c3 (R2) loses at once: these are the only freezes.

*Proof.* (i) The king lands on Y ∈ {c3, d3, e3, e4, e5}, none next to c5. Black plays K×c5 (the Black king on b4 or
b5 is next to c5; c5 is protected neither by the White king nor by a pawn on b4/d4). White moves anything; it cannot
protect b6 (the squares next to b6 reachable from Y in one step are b4, c4 from c3, both next to the Black king on
c5), cannot capture, cannot check (γ on c4 attacks b5, d5). Black plays K×b6 (b6 is not attacked by a White pawn).
The result is a position of Lemma B with White to move; the White king is not on b4, because the only way there was
a step next to the Black king on c5. So Black wins by Lemma B. (ii) c2–c3+ in R1: Black plays Kb5 (legal: c3 attacks
b4, d4) and reaches Q2 with White to move. c2–c4+ in R2 (no e.p. right) and c3–c4+ in Q2: Black plays Kb4 and reaches
Q1 with White to move. (iii) In Q1 White has only king moves; in Q2 king moves and c3–c4+, whose result Kb4 reaches Q1;
so by (i) Q1 is a Black win, then Q2 by (i) and (ii); then R1, R2 by (i), (ii). ∎

With Lemma C, (O2)–(O4) hold with exactly the freezes c2–c4 at b4 and c2–c3 at b5, and Definition 4.8 holds:
**G is an exact over group, PROVED given Lemma B.**

## 6. The theorem in P

**Proposition 4.25. PROVED given Lemma B (CHECKED-2).** G = `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` on the flat 8×8 board,
as the P game of its own pieces in a D-sum, has the results of ω beside every finite D-game (both roots, either side
to move; each q, Black to move with or without the right and White to move, has the results of 0_D).
*Proof.* Definition 4.8: §§2–3 and Lemma C. (B1): Lemma A′. Lemma 4.15. ∎
Without Lemma B the hand proof gives (O0), (O1), (O3), the freezes being non-losing, and (B1); what remains open by
hand is that White's king moves at R1, R2, Q1, Q2 lose (and so that the freezes are the only non-losing moves and that
(O4) holds).

## 7. Chess (promotion to real pieces)

Before the first promotion chess and P have the same moves; stalemate is a draw in both. In S_A White promotes to a
queen on b8 with: the queen protected by the king on a7 or c7 (both are next to b8); Black's only pawn on c4, c5 or
c6, so at least three moves from promotion (by (e) it moves at most from B₅ on: from B₅ if K×c5 came at B₃, which
means K×b7 at White's move 4 and promotion at move 7, so at most two pawn moves (B₅, B₆); if K×c5 comes at B₄
(then K×b7 was White's 4th move and promotion is at move 7) or later (promotion at move 8), at most one pawn move); and Black to move and not stalemated. *No stalemate after b8=Q*,
with the Black king on x = (file, rank r) and the White king on a7 or c7: the queen attacks the b-file, the 8th rank,
a7 and the diagonal c7–d6–e5–f4–g3–h2 (one square on each file); the White king touches files a–d only; γ and c5
attack only b- and d-file squares; Black's own pawn is on the c-file. If x is on the b-file or the 8th rank, or is
c7, Black is in check, so not stalemated. If x is on files d–h, the two or three neighbours of x on the next file to
the right (on the g-file for x on h) are attacked only by the diagonal, so one is free. If x = a_r (r ≤ 5, since a6 and
a8 are next to a7 and c7 is not, and a6 is next to the White king only when it is on a7; with the king on c7, x = a6
has a5 free), a_{r−1} (r ≥ 2) or a2 (r = 1) is free. If x = c_r with r ≤ 6, of d_{r−1}, d_r, d_{r+1} γ attacks at most
one, the queen at most d6, the pawn c5 (if present) d6, the White king d6–d8 (only on c7, which excludes x = c6);
for r ≤ 4 two of the three are free, for r = 5 one of d4, d5 is free, for r = 6 (king on a7) d7 is free. The check
that the queen is never lost at once and Black is never stalemated was also run mechanically
(`src/check_lemmaA.py`, test only).

**KNOWN fact used.** King and queen (with or without White pawns) against king and one pawn that needs three or more
moves to promote, the queen not capturable, the weaker side not stalemated: the queen wins (standard: only a pawn on
its seventh rank can draw against a queen; e.g. the KQKP tablebase).

**Chess values. PROVED given that fact.** (1) Every position of 𝒜 is a White win in chess. (2) Roots, Black to move:
lost for Black, every move: the six bad moves by (1); the shuttle is met by the freeze, reaching q1/q2 with Black to
move, lost by (1). (3) Roots, White to move: won by the freeze. (4) q1, q2, Black to move: lost, every move loses.
**Left to the tablebase (KNOWN, K65 cache):** q1, q2 with White to move are lost for White
(`8/1p6/1Pp5/2P5/1kPK4/8/8/8 w`, `8/1p6/1Pp5/1kP5/3K4/2P5/8/8 w`), and the non-freeze root moves lose
(`8/1p6/1Pp5/2P5/1k1K4/8/2P5/8 w`: Kd3, Ke3, Ke4, Ke5, c2–c3; `8/1p6/1Pp5/1kP5/3K4/8/2P5/8 w`: Kc3, Kd3, Ke3, Ke4,
Ke5, c2–c4). So "exact in chess" is PROVED for its White-win half and KNOWN for its Black-win half.

## 8. Why it works

The hinge is c5. White's king protects it only from d4 or d6 (d5 is covered by c6), and the only road from d4 to d6
runs through e5; Black's king attacks it only from b4 or b5 (a7, c7 and d6 are covered by White's pawns, and the
a-file is one step too far). So Kd4 against Kb4/Kb5 are corresponding squares: whoever has to move first loses. If
Black's king leaves the pair, Ke5–d6–c7 wins b7 and the b-pawn queens; if White's king leaves d4, …K×c5 and …K×b6 win.
White's spare c-pawn decides who moves first, and the single or double step matters because the pawn must take away
the shuttle square the Black king does **not** stand on: on b4, c2–c4 covers b5, while c2–c3 would give check and
drive the king to b5, the mutual zugzwang with White to move; on b5 it is the other way round. In the 2 + 2 groups
(F2, K63) the decisive P lines are pawn races in which the loser queens one move later, which chess scores as a draw.
Here there is no race: when White queens, Black's last pawn is at least three moves from promotion and blocked by γ,
so P's "first promotion wins" and chess agree.

## 9. Oracle comparison (tests, not proofs)

- `src/check_lemmaA.py` (python-chess, independent of both solvers): S_A exactly as written, against every Black
  reply from all 11 positions of 𝒜 in P (White promotes by move 8) and the 4 boards x_m beside −1 (by move 9); also
  Lemma A2 (a move to the rank below at every Black turn), (a) (K×c5 not before B₃), (c) (Black's king on rank ≤ 5
  at K×b7), the Black king never on rank 7/8 before K×b7, the queen never capturable and Black never stalemated after
  b8=Q, Black's pawn on rank 4–6 at the promotion. All hold (`logs/check_lemmaA.out`).
- `src/o68.cpp` (new) and `src/ax68q.cpp` (the K65 referee's ax65 with a query block): P values of 255 positions
  (roots, q's, every move there, the Lemma C reduction positions, the whole Lemma B family): 0 disagreements. ax68q on
  the group: Definition 4.8 exact, freezes c2–c4 (b4), c2–c3 (b5), (B1) at all six bad moves
  (`logs/ax68q_group.out`); o68 beside −1: W17 (nine White moves) at all four boards (`logs/o68_b1.out`).
- Chess: the cached Syzygy answers of all eight root and q positions agree with every chess claim of §7
  (`logs/chess_check.out`); move lists equal python-chess's.
- No mismatch between the text and any program was found.
