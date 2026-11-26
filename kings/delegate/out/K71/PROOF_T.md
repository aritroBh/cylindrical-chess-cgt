# K71: statement (T) of Proposition 4.25 by hand — a partial result

One AI investigator (K71, 2026-11-25). Not refereed. K70 was not opened.

## 0. Summary and labels

**(T) is not fully proved by hand.** Here is what is proved, and what is left.

- **PROVED given F0 (CHECKED-2):** after **three** of the 17 White king moves, namely Q1: Ke3, Ke4, Ke5, Black wins
  P (Lemma E, §3). The only computed input is the pawnless lemma F0: a lone White king against Black Kb6, pb7, pc6,
  White to move (55 positions; two programs with no shared code, §2). Lemma B is not used.
- **PROVED given F0** for a fourth move, Q1: Kd3, except one reply. After …K×c5, White has six moves. Five of them
  (Kc2, Kd2, Ke2, Ke3, Ke4) lose by Lemma E. The sixth, **Kc3**, is left.
- **PROVED given F0** inside the 13 other starts: the reply that puts the c-pawn on c4 unprotected loses (Lemma E,
  family E3). These replies are …K×c5 c2–c4 after R1 and R2 Ke3, Ke4, Ke5, and …K×c5 c3–c4 after Q2 Ke3, Ke4, Ke5.
- **PROVED given F (CHECKED-2), as a tool:** Lemma K (§4), the key-square finish of the oracle's main lines. Take
  White's c-pawn on c_j (j = 2, 3, 4), Black's c-pawn on c_{j+1} in front of it, Black's pawn on b7, and Black's
  king on d_j or b_j. Then Black takes the c-pawn within two moves, with either side to move and the White king
  anywhere. Lemma K does not finish any of the 17 positions by itself.
- **Left (not proved by hand): 14 positions**, listed in §5 (`logs/left14.txt`). They are:
  - the starts R1 Kd3, Ke3, Ke4, Ke5; R2 Kc3, Kd3, Ke3, Ke4, Ke5; Q2 Kd3, Ke3, Ke4, Ke5 (oracle L29 to L39);
  - Q1 Kd3 …K×c5 Kc3 (oracle L39).

  Through K68's reduction, these 14 positions need **30** of the 42 Lemma B positions (was 42;
  `logs/needed30.txt`).
- **Consequence for Definition 4.8.** (O4) at Q1 needs all four Q1 king moves to lose. Three are proved, and Q1 Kd3 is
  proved except the reply Kc3. (O4) at Q2, and exactness at R1 and R2, still rest on Lemma B.
- **No label change for Proposition 4.25.** It stays "PROVED given CHECKED-2". The computed input is now Lemma B on
  30 positions, plus the pawnless F. So there is no `EDITS.md`.

| statement | label |
|---|---|
| F: lone White king against Black K with a b-pawn and/or a c-pawn. Values in P as computed; in particular F0 (Kb6, b7, c6, White to move): all 55 positions are Black wins | **CHECKED-2** (k71 = r68 core, and `src/f0check.py`: 273,227 common positions, 0 disagreements) |
| Lemma E: Q1 after Ke3, Ke4, Ke5; Q1 Kd3 …K×c5 and every reply except Kc3; the γ→c4 replies listed above. Black wins, reaching F0 by Black's 5th move at the latest | **PROVED given F0** |
| (T) at Q1 Ke3, Q1 Ke4, Q1 Ke5 | **PROVED given F0** |
| Lemma K (key squares; b-pawn on b7) | **PROVED given F** (the 199 leaves of §7 are F-positions, Black wins in both programs) |
| (T) at the other 14 king moves | **not proved by hand**; Lemma B (CHECKED-2, K68), now 30 positions |
| "Local battle" universality, Lemma B universality for γ on c2 and c3, the 4 hard positions (§8) | **COMPUTED-1**, a roadmap only |

## 1. Setting

The rules of P and the notation follow `kings/delegate/out/K68/PROOF.md` §1. A promotion wins for the promoter.
Checkmate loses. Stalemate and infinite play are draws. γ is White's c-pawn.

- R1 = `8/1p6/1Pp5/2P5/1k1K4/8/2P5/8 w`.
- R2 = `8/1p6/1Pp5/1kP5/3K4/8/2P5/8 w`.
- Q1 = `8/1p6/1Pp5/2P5/1kPK4/8/8/8 w`.
- Q2 = `8/1p6/1Pp5/1kP5/3K4/2P5/8/8 w`.

(T): after each White king move in these positions (17 in all), Black, to move, wins P.

N(s) is the set of squares next to s. dist is king distance.

## 2. The pawnless lemma F (CHECKED-2)

**F.** The positions are a lone White king against a Black king with a pawn on the b-file and/or a pawn on the
c-file (pawns on ranks 2–7), either side to move. Their values in P are those computed by two programs:

- k71 (the K68 referee's r68 solver core, unchanged);
- `src/f0check.py`, written for K71 from the rules of P alone. It is a retrograde with counters and shares no code
  with r68.

They agree on all 273,227 positions that both cover (`logs/f0check_compare.out`).

**F0** is the special case Black Kb6, pb7, pc6, White to move. Black wins all 55 positions (legal White king
squares).

For orientation (COMPUTED-1, `logs/universal.out`): with a b-pawn on b3 to b7 and any c-pawn, every placement is a
Black win, either side to move. With a single pawn this fails. F is a textbook-type ending (two pawns on adjacent
files against a bare king), but **no hand proof of F or F0 is given here**. The longest F0 lines are 22 plies.

## 3. Lemma E: the lines where the c-pawn on c4 cannot be held (PROVED given F0)

**Positions.** Black is to move in each.

- **E1.** Q1 after Ke3 or Ke4: White Ke3 or Ke4, Pb6, Pc4, Pc5; Black Kb4, pb7, pc6.
- **E2.** Q1 after Ke5.
- **E3.** T_w for w ∈ W = {c2, d2, e2, e3, e4, e5, e6, f4, f5, f6}: White Kw, Pb6, Pc4; Black Kc5, pb7, pc6.
  - Q1 Kd3 …K×c5 followed by Kc2, Kd2, Ke2, Ke3 or Ke4 gives T_w with w ∈ {c2, d2, e2, e3, e4}.
  - R1 or R2 after Ke3, Ke4 or Ke5, then …K×c5 c2–c4, gives T_w with w ∈ {e3, e4, e5}.
  - Q2 after Ke3, Ke4 or Ke5, then …K×c5 c3–c4, does the same.
  - No e.p. right arises, because no Black pawn stands on b4 or d4.

**Strategy S_E.** The first move is K×c4 in E1, K×c5 in E2, and K×c4 in E3 (rule E1). After that, the first rule
that applies is played:

- (E1) take on c4;
- (E2) take on c5;
- (E3) take on b6 when b6 is White's last pawn;
- (E4) with the king on c4 and Pb6 on the board, play Kb5;
- (E5) with the king on b5, play Ka6.

**Fixed facts during S_E.**

- (a) pb7 and pc6 never move.
- (b) White's pawns never move:
  - Pb6 is blocked by b7;
  - Pc5 is blocked by c6;
  - in E2, Pc4 is blocked by Black's king on c5 and is taken next.
  So White has only king moves, and White never promotes.
- (c) Black pawns attack only a6 and c6 (from b7), and b5 and d5 (from c6). c6 stays protected by b7 throughout.
  White can take b7 only from a7, a8, b8, c7 or c8, and only when no Black unit protects it.
- (d) b6 has neighbours a5, a6, a7, b5, b7, c5, c6, c7. Of these, a6 and b5 are attacked (by b7 and c6), and b7
  and c6 hold Black pawns. So White's king can protect b6 only from a5, a7, c5 or c7.
- (e) White is never stalemated. In these lines White's king stands on files b–g, and Black's king on files a–c.
  Call r(s) the square one file to the right of the White king's square s.
  - If the White king's file is at least the Black king's, r(s) is farther from Black's king than s is, so it is
    not next to it.
  - The b-file occurs only from w = c2 (squares b1 and b2), while Black's king is on c4 or b5. Then c1 and c2 are
    free.
  - r(s) is never attacked by a Black pawn. That would need r(s) ∈ {a6, b5, c6, d5}, that is, the White king on the
    a-file, on b6 (its own pawn) or on c5. It never stands on c5, which is next to or occupied by Black's king.
  So r(s) is always a legal move.
- (f) Black always has the prescribed move. This is shown case by case below. So Black is never stalemated either.

**Claim E3. From T_w (w ∈ W), S_E reaches F0 with White to move, by Black's 3rd move or, in one case, by the 4th.**

1. **Black's move 1: K×c4.** It is legal:
   - c4 is next to c5;
   - every w ∈ W is at distance ≥ 2 from c4;
   - Pb6 attacks only a7 and c7.

   **White's move 1** is a king move to some x ∈ N(w). It captures nothing: every w ∈ W is at distance ≥ 3 from b7.
   Moreover x ∉ {a7, a8, b8, c7, c8}, because these squares are at distance ≥ 2 from every w ∈ W.

2. **Black's move 2 (E4): Kb5.** It is legal. The neighbours of b5 are a4, a5, a6, b4, b6, c4, c5, c6. None of them
   is in N(w) for any w ∈ W, so x is not next to b5. No White pawn attacks b5 any more.

   **White's move 2** goes to some y ∈ N(x). It cannot take b7: that would need x ∈ {a7, a8, b8, c7, c8}, which is
   impossible as just shown.

3. **Black's move 3.**
   - **If y ∉ {a7, c7}.** Then b6 is unprotected by (d): a5 and c5 are next to Black's king on b5. Also y is not
     next to b6. So (E3) K×b6 is legal and gives F0 with White to move.
     This includes y = c8 (reachable only from w = e6, via d7). In that case b7 was attacked but not taken. After
     K×b6 the king protects it.
   - **If y ∈ {a7, c7}.** Then dist(w, y) ≤ 2, which forces y = c7 and w ∈ {e5, e6} (a7 is at distance ≥ 4 from W).
     Black plays (E5) Ka6, which is legal (a6 is at distance 2 from c7, and Pb6 attacks a7 and c7). Now b7 is
     protected.

     **White's move 3** is from c7 to b8, c8, d8, d7 or d6. White cannot take b7 (protected by Ka6) or c6 (protected
     by b7). At least d6 is legal, and none of these five squares is next to b6.

     **Black's move 4 (E3): K×b6** is legal and gives F0. ∎

**E1 (Q1 Ke3 or Ke4).**

1. **Black's move 1: K×c4.** It is legal:
   - c4 is next to b4;
   - e3 and e4 are at distance 2 from c4;
   - Pb6 attacks a7 and c7, and Pc5 attacks b6 and d6.

   **White's move 1** cannot protect c5. Its neighbours, as White-king squares, are excluded as follows:
   - b4 and d4 are next to Black's king on c4;
   - b5 and d5 are attacked by c6;
   - b6 and c6 are occupied;
   - d6 is at distance ≥ 2 from e3 and e4.
2. **Black's move 2 (E2): K×c5.** It is legal: c5 is unprotected and not attacked by Pb6.

   **White's move 2.** The White king is now within two moves of e3 or e4.
3. **Black's move 3 (E3): K×b6.** It is legal. By (d), b6 could be protected only from a5 or a7 (at distance ≥ 4 from
   e3 and e4), from c7 (at distance 3 from e4 and 4 from e3) or from c5 (Black's king). White has made two king moves
   from e3 or e4. So b6 is unprotected and not next to the White king. Taking b7 at White's move 2 would have needed
   the king on a7, a8, b8, c7 or c8 after move 1, which is impossible. This gives F0. ∎

**E2 (Q1 Ke5).**

1. **Black's move 1: K×c5.** It is legal:
   - c5 is next to b4 and at distance 2 from e5;
   - Pb6 attacks a7 and c7, and Pc4 attacks b5 and d5.
2. **White's move 1.** White's pawns are blocked: Pb6 by b7, and Pc4 by Black's king on c5. From e5, the king cannot
   go to d4 or d6 (next to c5) or to d5 (attacked by c6). So it goes to x₀ ∈ {e4, e6, f4, f5, f6} ⊂ W.

This is T_{x₀}, and Claim E3 applies. Note that K×c4 at move 1 would lose here (oracle W13): the White king reaches c7
one move earlier. ∎

**Lemma E. PROVED given F0.** From every position of E1, E2 and E3, S_E reaches F0 with White to move:

- in E1, by Black's 3rd move;
- in E3, by the 3rd move, or the 4th when the White king goes to c7;
- in E2, by the 4th move, or the 5th when the White king goes to c7.

The longest play is 9 plies (E2 with the king route e5–e6–d6/d7–c7).

The oracle lengths of these starts are L23 (Q1 Ke4), L25 (Q1 Ke5) and L27 (Q1 Ke3) to promotion. All of the length
lies in F0.

## 4. Lemma K: the key-square finish (PROVED given F)

**Lemma K.** Let j ∈ {2, 3, 4}. White has its king and a pawn γ on c_j. Black has a pawn on c_{j+1} (the "blocker"),
a pawn on b7, and its king on d_j or on b_j. There are no other men. The White king is on any legal square, and
either side is to move. Then Black wins P.

**Strategy S_K.**

- (K1) If K×γ is legal, play it.
- (K2) Otherwise play b7–b6.

**Proof.**

1. **The blocker is safe and γ is frozen.** The blocker is protected by Black's king, since d_j and b_j are both next
   to c_{j+1}. Until K×γ, γ cannot move. Its only captures would be on b_{j+1} or d_{j+1}, and no Black man ever
   stands there. So White has only king moves.

2. **The squares that protect γ.** The White king protects γ only from a square next to c_j: b_{j−1}, c_{j−1},
   d_{j−1}, b_j, d_j, b_{j+1}, d_{j+1}. Of these, b_j and d_j are attacked by the blocker.
   - With Black's king on d_j, c_{j−1}, d_{j−1} and d_{j+1} are next to it. So γ is protected iff the White king is
     on P_d = {b_{j−1}, b_{j+1}}.
   - Symmetrically, with Black's king on b_j, P_b = {d_{j−1}, d_{j+1}}.

3. **Black to move with γ unprotected.** K×γ is legal: c_j is next to Black's king and not next to White's, and no
   White pawn is left to attack it.

4. **Black to move with γ protected.** Say Black's king is on d_j and the White king on b_{j±1}.
   - b6 is empty, since b_{j+1} ≤ b5. So b7–b6 is legal.
   - From b_{j−1}, the White king's squares are a_{j−2..j}, b_{j−2} and c_{j−2}. The other neighbours are
     excluded: b_j (attacked), c_{j−1} (next to d_j) and c_j (own pawn). None of the available squares is next to
     c_j. For j = 2, rank 0 does not exist.
   - From b_{j+1}, the squares are a_{j..j+2}, b_{j+2} and c_{j+2}. b_{j+2} can be a capture of the pawn on b6 when
     j = 4. The other neighbours are excluded: b_j (attacked), c_{j+1} (protected) and c_j. None of the available
     squares is next to c_j.
   - In each case the White king has a legal move, so it is not stalemated. a_j is always available: it is next to
     b_{j±1}, at distance 3 from d_j, and not attacked (the blocker attacks b_j and d_j, the pawn on b6 attacks a5
     and c5).
   - With Black's king on b_j and the White king on d_{j±1}, the same holds by symmetry. Its squares are c_{j−2},
     d_{j−2}, e_{j−2..j} (from d_{j−1}) or c_{j+2}, d_{j+2}, e_{j..j+2} (from d_{j+1}), none next to c_j. e_j is
     always available. The pawn on b6 is at distance ≥ 2 from the d-file.

   After White's move γ is unprotected, and (K1) follows.

5. **White to move.** After White's move, γ is either unprotected, giving (K1), or the White king is in P, giving
   step 4. This includes a first move K×b7, after which the king is at distance ≥ 3 from c_j.

So Black plays K×γ by its second move. The result is a pawnless position: Black's king on c_j, the pawn on c_{j+1},
and the b-pawn on b7 or b6 (or gone, if White took it). By F these are Black wins: all 199 that occur are Black wins
in both programs (§7). ∎

Lemma K is the end of the oracle's main lines in the hard cases (for example the K68 referee's lines with …Kd2 or
…Kd4 followed by …b6–b5 and …K×γ). What is missing is a hand proof that Black reaches it. See §8.

## 5. What is left

The 14 positions (Black to move) are in `logs/left14.txt`, with their oracle values:

| position | FEN | P (oracle) |
|---|---|---|
| R1 Kd3 | `8/1p6/1Pp5/2P5/1k6/3K4/2P5/8 b` | L39 |
| R1 Ke3 | `8/1p6/1Pp5/2P5/1k6/4K3/2P5/8 b` | L39 |
| R1 Ke4 | `8/1p6/1Pp5/2P5/1k2K3/8/2P5/8 b` | L39 |
| R1 Ke5 | `8/1p6/1Pp5/2P1K3/1k6/8/2P5/8 b` | L29 |
| R2 Kc3 | `8/1p6/1Pp5/1kP5/8/2K5/2P5/8 b` | L39 |
| R2 Kd3 | `8/1p6/1Pp5/1kP5/8/3K4/2P5/8 b` | L39 |
| R2 Ke3 | `8/1p6/1Pp5/1kP5/8/4K3/2P5/8 b` | L39 |
| R2 Ke4 | `8/1p6/1Pp5/1kP5/4K3/8/2P5/8 b` | L39 |
| R2 Ke5 | `8/1p6/1Pp5/1kP1K3/8/8/2P5/8 b` | L29 |
| Q2 Kd3 | `8/1p6/1Pp5/1kP5/8/2PK4/8/8 b` | L31 |
| Q2 Ke3 | `8/1p6/1Pp5/1kP5/8/2P1K3/8/8 b` | L33 |
| Q2 Ke4 | `8/1p6/1Pp5/1kP5/4K3/2P5/8/8 b` | L31 |
| Q2 Ke5 | `8/1p6/1Pp5/1kP1K3/8/2P5/8/8 b` | L29 |
| Q1 Kd3 …K×c5 Kc3 | `8/1p6/1Pp5/2k5/2P5/2K5/8/8 b` | L39 |

L n means Black promotes at ply n with best play, counted from this position.

**Status of the 14.**

- By K68's Lemma C reduction, the 14 reach 30 of the 42 Lemma B positions (`logs/needed30.txt`). The 12 that are no
  longer needed are all the γ-on-c4 positions except the one with the White king on c3, and except c4 with the king
  on d3 (reached via R1/R2/Q2 Kd3 and γ→c4).
- Inside the 13 starts, …K×c5 followed by γ→c4 unprotected is proved (E3).
- Every other White reply after …K×c5 (`logs/level2.out`) needs 9 to 33 more plies before Black reaches any
  configuration proved here (Lemma K, F). The DTM strategy trees for them have 2,000 or more leaves.

## 6. Routes (item 1 of the brief)

Measured with the oracle (`logs/routes.out`, `logs/level2.out`). "Longest line" is the P length with best play. Two
measures depend on the strategy chosen, so the DTM-fastest strategy was used for them:

- "reach": the number of plies until a configuration covered by a proved lemma;
- "tree": the leaves of the strategy tree.

| route | idea | longest line / reach | zones a hand proof needs | outcome |
|---|---|---|---|---|
| A (K68) | …K×c5, …K×b6, then Lemma B | starts L23–L41; Lemma B up to L38 | Lemma B: 42 positions, no hand proof (K68 referee, §6) | CHECKED-2 only |
| **B (chosen)** | γ first: …K×c4 as soon as it is unprotected (Q1 Ke3 or Ke4 at once; after Ke5 first …K×c5), then …Kb5(–a6), …K×b6; a counted race against Kd6–c7 | 9 plies to F0 (S_E); 124 Black positions; 654 plays | 3 zones: take γ (and c5), approach b6, F0 | PROVED given F0 for 3 moves, plus 5 of the 6 replies to Q1 Kd3 …K×c5, plus the γ→c4 replies |
| C | king in front, queenside: after …K×b6, Black's king only on files a–c | the restricted game wins 38 of 42 Lemma B positions (reach to the γ capture ≤ 24 plies). It fails exactly the 4 hard ones: γ c2 with the White king on b3, c3 or d3, and γ c4 with the king on c3. From the starts it wins R1 Ke5, R2 Ke5 (L35), Q1 Ke3/Ke4/Ke5 and all of Q2 (L31–L37); it fails R1 Kd3/Ke3/Ke4, R2 Kc3/Kd3/Ke3/Ke4 and Q1 Kd3. Files a–e give the same set | a zone proof over 38 Lemma B positions, 10 to 24 plies deep | not written |
| D | blocker and key square: the c-pawn goes to c_{j+1} in front of γ, then the king to d_j or b_j (Lemma K) | reach to the Lemma K configuration from the starts: 17–39 plies; to the "local-battle box" of §8: 5–23 plies | Lemma K (done), local battle (COMPUTED-1 universal), blocker phase (no proof). DTM trees from Q2: 10⁵ leaves | Lemma K PROVED given F; rest open |
| frozen pawns | b-pawn frozen, c-pawn frozen, or both, until γ falls | wins only Q1 Ke3/Ke4/Ke5 (c-pawn frozen: also Q2 Kd3 L33 and Ke3 L45) | — | rejected |

**Why B was chosen.** It is the only route whose hand proof is short: 3 zones, at most 9 plies, and an explicit
count. It closes exactly the lines in which White cannot hold c4. All other lines are, by the oracle, long fights
(13–39 plies) around a protected γ. In these, White's king is on b3, c3 or d3 (γ on c2) or on c3 (γ on c4), and in
them the K68 referee's difficulty (stalemate defences, no uniform Black move) is real.

## 7. Strategy tests (item 3 of the brief)

The written rules were played literally against every White reply (`src/k71.cpp`, commands `testE` and `testK`):

- illegal or missing rules count as failures;
- so do repetitions, a stalemate of either side, and a White promotion;
- leaves are checked against both programs.

- **S_E**, from the 10 starting positions of `logs/testE_starts.txt` (E1 twice, E2, and E3 with every w that occurs):
  - **654 plays, 0 failures**;
  - longest play 9 plies;
  - 124 distinct Black-to-move positions;
  - 49 distinct F0 leaves, all Black wins in k71 and in `f0check.py`.

  Rules used: Kxc4 10, Kxc5 9, Kb5 27, Ka6 1, Kxb6 77 (distinct positions; `logs/testE_rulecount.out`).
- **S_K**, from every Lemma K position:
  - j = 2, 3, 4; king on d_j or b_j; every White king square; both sides to move;
  - **2,412 plays, 0 failures**;
  - longest play 4 plies;
  - 356 Black positions;
  - 199 pawnless leaves, all Black wins in both programs.

  (`logs/testK.out`, `logs/f0check_leavesK.out`.)
- **F**: 273,227 positions compared, 0 disagreements (`logs/f0check_compare.out`). F0: 55 of 55 positions are Black
  wins.

A passed test is a check, not a proof. The proofs of §3 and §4 do not use it.

## 8. Roadmap for the rest (COMPUTED-1, not used in any proof)

`logs/universal.out` lists, for each pawn structure, the Black king squares from which Black wins against every White
king square.

1. **Lemma B is "universal" for γ on c2 and on c3.** With Black Kb6, b7, c6 and White to move, Black wins for every
   White king square. For γ on c4 the only exception is the White king on b4.
2. **Local battle.** Take the blocker on c_{j+1} and b7. With Black to move, Black wins against every White king when
   Black's king is on files a–e, ranks j−1 to j+1, and the blocker is not en prise. For j = 2, rank 1 is excluded
   except c1.
   - On ranks j−1 and j, "take γ, else go to d_j or b_j (Lemma K), else play b7–b6" decides at once.
   - The long cases are Black's king on a_{j+1} or e_{j+1} against the White king on its own side. For j = 4 these
     are a5 against a3/b3, and e5 against d3/e3 (oracle 25 to 37 plies): Black's king must walk round.
   - This is the piece that a full proof most needs.
3. **The hard core** is four Lemma B positions:
   - γ c2 with the White king on b3, c3 or d3 (L36 each);
   - γ c4 with the White king on c3 (L38).

   No Black strategy that keeps its king on files a–e wins them: Black's king must reach the f-file, as in the
   referee's lines (…Kd5–e4–f3–e2–d2).
4. **Most robust first moves.** In the 119 positions after White's first move in Lemma B, …Ka5 wins in 116. The three
   exceptions have the White king on b4 or a4. A proof built on "…Ka5 and the a-file" covers neither the hard core
   nor the γ-on-c2 starts.

A complete proof along route D would need three hand lemmas:

- the blocker phase (the c-pawn to c_{j+1}; for γ on c2 this takes up to 19 plies);
- the local battle (item 2);
- Lemma K (done).

## 9. Reproduce

```
c++ -O2 -std=c++17 -o k71 src/k71.cpp                      # scratch directory; about 10 s per run, < 30 MB
LAYERS=1 ./k71 testE < logs/testE_starts.txt               # S_E test (section 7)
LAYERS=1 ./k71 testK                                        # S_K test
LAYERS=1 ./k71 dumpf > dumpf.txt                            # pawnless values from the r68 core
python3 -I src/f0check.py dumpf.txt                         # independent solver, comparison (F, F0)
python3 -I src/f0check.py --list logs/leavesE_F0.txt        # the 49 F0 leaves of S_E
LAYERS=3 ./k71 query < q.txt                                # values of FEN lines (as r68 query)
TARGET=8193 LAYERS=2 ./k71 level2 < starts.txt              # per-reply table of logs/level2.out
```

The 17 starts are the unindented FEN lines of `logs/values17.out`. No binary was left in the repository, and no process
is left running.
