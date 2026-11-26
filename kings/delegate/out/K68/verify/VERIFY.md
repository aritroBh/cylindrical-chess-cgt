# K68 referee report: `kings/delegate/out/K68/PROOF.md` (C125_05 by hand)

Referee: K68 referee (one AI), 2026-11-25. Read: PROOF.md, findings.txt, EDITS.md, the K68 brief, LOOPY.md
(Definitions 1.1–1.3, 4.8, Lemma 4.15) and the K61 packet §1. My own programs were written before I read any of the
investigator's logs; I never opened `src/o68.cpp`, `src/ax68q.cpp`, `ax65.cpp` or `kings/delegate/out/K70/`.

## 0. Verdict

**The hand proof is correct after two small repairs, and the labels need two changes.**

- In P, every hand step re-derives: (O0), (O1), (O2), (O3), (B1) at all six bad moves (Lemma A, A′), and the reduction
  of (O4) and "the freezes are the only non-losing root moves" to Lemma B (Lemma C). Lemma 4.15's hypotheses are all
  met, so **Proposition 4.25 is PROVED given Lemma B (CHECKED-2)**. Two gaps need a repaired sentence (G1, G2 below).
  Neither changes a statement.
- **Lemma B is not proved by hand** (I did not manage it either, §6). It is now computed by three programs that share
  no code (o68, ax68q, and my r68): CHECKED-2 is right. Lemma C needs only **42** of the 162 positions (§5).
- **Chess section: the cited KNOWN fact is wrong as stated** (G3). "Queen beats a pawn three or more moves from
  promotion" is not a standard fact, and my conservative solver leaves 87 such positions with a c4-pawn unwon. The
  chess values themselves are right: all eight root and q positions agree with the Syzygy cache, and White wins at all
  460 positions that S_A reaches after b8=Q (my q68, COMPUTED-1). The chess row should be "KNOWN (Syzygy)". The
  hand reduction gives "PROVED given COMPUTED-1 (460 leaves)", not "PROVED given KNOWN".
- Oracle: **no mismatch** between any value or "only move" / "every move loses" claim in PROOF.md and my solver. My
  solver also agrees with o68/ax68q on all 255 of their positions. S_A, played literally against every Black reply,
  promotes by move 8 in P (298,179 plays) and by move 9 beside −1 (131,902 plays). The bound 9 is attained.

## 1. Step-by-step table

| step | verdict |
|---|---|
| §1 rules of P and of "beside −1" | correct as written |
| Fact 1 (pawns blocked, no pawn capture) | correct |
| Fact 2 (forbidden squares) | correct (c6 is also barred to White's king: protected by b7; harmless) |
| (O0) | correct; **gap G0**: K1/K2 of Definition 4.8 not stated; one line, below |
| Move lists (8 lists) | correct, square by square (§2) |
| Lemma A (a) K×c5 not before B₃ | correct |
| Lemma A (b) legality of Ke5, Kd6, Kc7, K×b7, Kb8; "b7 guarded only from a6" | correct in substance. Minor slip: "e6 is at distance ≥ 3 from every k₀ except b3" (b3–e6 is also 3). The sentence actually serves (c). Repair: every k₀ is at distance ≥ 3 from e6. A Black king on e6 at B₃ needs d5 at B₂, and d5 is next to Kd6. |
| Lemma A (c) Black king on rank ≤ 5 at K×b7 | correct (oracle: 0 exceptions) |
| Lemma A (d) steps 3, 4 legal, promotion by move 7 or 8 | correct |
| Lemma A (e) Black cannot promote or mate | correct ("γ cannot leave the c-file" holds: Black's c-pawn can never stand on b/d, since no White unit ever stands on b5/d5) |
| Lemma A (f) / A2 no stalemate | **gap G1** (wrong count, conclusion true), repaired below |
| Consequences (O1), (O2), (O3) | correct |
| Lemma A′ / (B1), token count | correct. The pass delays White only at the a6 shuffle, and only once, because a king on a6 has no waiting move. "Never in check" holds; the oracle confirms "by move 9" exactly. |
| Lemma C (i) | conclusion correct; **gap G2** (wrong reason for "cannot protect b6"), repaired below |
| Lemma C (ii), (iii) | correct; the order Q1 → Q2 → R1, R2 is sound |
| §5 "G exact, PROVED given Lemma B" | correct: Definition 4.8 needs Lemma C, because every non-losing White root move is a freeze and must satisfy (O3)/(O4) |
| §6 Proposition 4.25 via Lemma 4.15 | correct; every hypothesis checked (§3) |
| §7 chess: reduction to leaves, no stalemate, queen safe, pawn on c4–c6 | correct (oracle: 460 distinct leaves, 0 stalemates, 0 capturable queens, pawn rank 4–6). The stalemate wording is loose: for x on rank 7, the next-file neighbour on rank 8 is attacked along the 8th rank, not "only by the diagonal". Still, at most two of the three are attacked, so the conclusion stands. |
| §7 KNOWN fact (KQ vs pawn ≥ 3 moves away) | **error G3**: not a correct general fact; replace (below) |
| §7 "left to the tablebase" | correct, and agrees with the cache |
| §8 "Why it works" | two expository errors (G4) |
| §0 labels | Lemma B row fine (now three programs). Chess row 1 must change (G3). |

## 2. Move lists (re-derived)

b4 root, Black: neighbours a3, a4, a5, b3 (c2 attacks), b5, c3 and c4 (next to d4), c5 (protected by d4). So Ka3, Ka4,
Ka5, Kb5. b5 root, Black: a4, a5, a6, b4 (not attacked by c2), b6 (protected by c5), c4 (next to d4), c5, c6. So
Ka4, Ka5, Ka6, Kb4. q1 (γ c4): b5 is attacked by c4, c3 is next to d4, so Ka3, Ka4, Ka5, Kb3. q2 (γ c3): b4 is
attacked by c3, so Ka4, Ka5, Ka6. White at b4: Kd3, Ke3, Ke4, Ke5, c3+, c4 (c3/c4 next to b4, d5 attacked by c6).
At b5: Kc3 (c3–b5 distance 2), Kd3, Ke3, Ke4, Ke5, c3, c4+. q1: four king moves (γ blocked). q2: four king moves and
c4+. Identical to PROOF.md and to my generator. No e.p. right anywhere: c2–c4 meets no Black pawn on b4/d4. No check
at the roots or q's.

## 3. Definition 4.8 and Lemma 4.15: hypotheses

- K1 (over form): no White pawn attacks b4 or b5 (c2→b3, d3; b6→a7, c7; c5→b6, d6), and no Black pawn attacks d4
  (c6→b5, d5). K2: king distance 2 at both roots. **G0 repair: add this line to §2.**
- (O1) mirror of (U1): every non-shuttle Black move loses at once (Lemma A), and the shuttle is legal. (O2): the
  freezes c2–c4/c2–c3 win; no root move promotes. (O3): after each freeze, Black to move (no right) loses with every
  move (Lemma A). (O4): q with White to move is legal (no check), White has a move, and every move loses (Lemma C,
  needs Lemma B). Because "freeze" means *any* non-losing White root move, Lemma C (iii) is also needed for (O3)/(O4):
  it shows there are no other freezes.
- (B1): at the four boards x_m (six moves), with White to move and Black holding one token under the sum's rule:
  Lemma A′. No check at x_m, no e.p. right.
- So Lemma 4.15 gives the results of ω at both roots and of 0_D at the q-states (q1, q2 with Black to move, and with
  White to move). The e.p.-right variants do not arise.

## 4. Gaps and errors, with repairs written out

**G0 (minor, §2).** Insert after (O0): "K1 and K2 of Definition 4.8 hold: no White pawn attacks b4 or b5 (c2 attacks
b3, d3; b6 attacks a7, c7; c5 attacks b6, d6), no Black pawn attacks d4 (c6 attacks b5, d5), and the kings are at
distance 2 at both roots."

**G1 (Lemma A (f), the c-file case).** The text says the blocked configuration (king on c_r, own pawn on c_{r−1},
γ on c_{r−2}) "needs K×c5, a king move off c5, two pawn moves and a return …: not before B₈". For γ on c4 one pawn
move is enough: K×c5, Kd6 (or Kb6), …c5, Kc6. So the configuration can stand after B₆ when K×c5 is B₃. Replace the
sentence by:

> This needs K×c5, a king move off c5 to a square other than γ's, at least one pawn move, and a king move onto the
> square behind the pawn: four Black moves from the capture on, so the configuration can face Black at B₇ at the
> earliest, and only if K×c5 was B₃. In that case the Black king was not on a6 at B₃, so K×b7 was White's 4th move and
> White promoted at its 7th move, before B₇. If K×c5 was B₄ or later, the configuration needs B₈, which never comes
> (White promotes by its 8th move). For γ on c3 or c2 more pawn moves are needed (B₈ at the earliest in any case).

(Oracle: A2 holds at every Black turn of all 298,179 plays.)

**G2 (Lemma C (i), "cannot protect b6").** The given reason is wrong: b4 and c4 are not next to b6. Replace by:

> The squares next to b6 are a5, a6, a7, b5, b7, c5, c6, c7. Here b7, c5 and c6 are occupied, and each of the other
> five is at distance ≥ 2 from every Y ∈ {c3, d3, e3, e4, e5} and from every square one step from Y. So White's
> reply cannot protect b6. It cannot capture or check either, and K×b6 is legal (b6 is attacked by no White pawn,
> since γ is on the c-file).

(Oracle: …K×c5 and then …K×b6 are legal after all 17 king moves and all 119 White replies.)

**G3 (§7, the KNOWN fact; error).** "KQ against K + one pawn needing three or more moves, queen safe, not stalemated:
the queen wins" is not a standard fact. In my conservative chess solver q68 (White may not promote; a Black promotion
or capture of the queen counts as a Black win), 87 of 180,204 such positions with the pawn on c4 are not won. Example:
White Kh1, Qd7 against Black Kc1, pc4, Black to move, the bishop-pawn draw after …c3, …c2. Even in the leaves' own
shape (Qb8, king on a7/c7), Black Kc1 with pc4 is not won. There are 35 such positions with b4 and 63 with d4; none
with a4, c5 or c6. These are conservative non-wins; whether they are true draws needs KQKQ, which I did not run. Either
way the fact cannot be cited. Replace the paragraph by:

> **Leaf fact (COMPUTED-1).** At each of the 460 positions that S_A reaches right after b8=Q (listed in
> `verify/logs/leaves460.txt`), White wins in chess. This is checked by q68, which solves K+Q+pawns against K+pawns
> with two changes that only hurt White: White may not promote, and a Black promotion or capture of the queen counts
> as a Black win. All 460 are White wins (`verify/logs/q68_leaves.out`).

Then "Chess values (1)–(4)" become **PROVED given COMPUTED-1**, and they are KNOWN anyway from the Syzygy cache
(`verify/logs/tb_k68.out`). The 50-move rule does not matter: the cache shows plain wins and losses, with no cursed
results. Also in §8: "blocked by γ" is false in some leaves, because Black's king can take γ (on c4 from b3 at once).
Of the 460 leaves, 78 have no White pawn left.

**G4 (§8, exposition).** "White's king protects c5 only from d4 or d6": from b4 and c4 as well in general. Within the
group these squares are next to Black's king, so say "with Black's king on b4 or b5". "Black's king attacks it only
from b4 or b5": also from c4/d4 in general; same qualifier. "Blocked by γ": see G3.

## 5. Oracle comparison (my programs; COMPUTED-1 each, CHECKED-2 where they reproduce another program)

`src/r68.cpp` solves P from the definitions: pawn configurations closed under every pawn move or capture, solved as a
DAG with a worklist inside each configuration. It has three layers: P alone; the sum rule with nothing beside; the sum
rule beside −1, where Black holds one token (pass not in check, clears e.p.). There are 469 configurations, solved in
10 s with 25 MB.

- **Every value in PROOF.md** (`logs/r68_main.out`): roots W to move W17 (P), Black to move W18. Every Black root move
  is a White win: the bad ones W15, the shuttle W17. At b4: c2–c4 W16 for White, every other White move a Black win.
  At b5: c2–c3 wins, all others lose. q1/q2, Black to move: every move W15. q1/q2, White to move: every move a Black
  win (q1 L42, q2 L44). The W15 and L16 of PROOF.md match.
- **(B1)**: the four boards x_m, White to move, Black token, sum rule: W17 (nine White moves) at all four.
- **Lemma B**: 162 positions; 161 Black wins and 1 draw (γ c4, Kb4). Same exception as claimed
  (`logs/r68_lemmaB.out`).
- **o68/ax68q comparison**: their 255 positions, 0 disagreements with r68 (`logs/r68_vs_k68.out`, `src/cmp_k68.py`).
- **S_A literally** (`logs/r68_strat.out`). P, all 11 starts of 𝒜: 298,179 plays, 0 failures (illegal move, missing
  rule, Black promotion, stalemate, late promotion), promotion at move 7 or 8. Side claims, 0 exceptions: A2;
  K×c5 before B₃; Black's king on rank 7/8 before K×b7; Black's king above rank 5 at K×b7. Beside −1 with the token,
  the four x_m boards: 131,902 plays, all promote by move 9; with bound 8, 3,995 plays fail, so 9 is needed. All 11
  starts with the token: also by move 9.
- **Lemma C reduction** (`logs/r68_needed.out`): from R1, R2, Q1, Q2, after each of the 17 White king moves …K×c5 is
  legal, and after each of the 119 White replies …K×b6 is legal. The result is one of **42** Lemma B positions, all
  Black wins:
  - c2: K on b2, b3, c3, d2, d3, e2, e3, e4, e5, e6, f2, f3, f4, f5, f6 (15)
  - c3: K on c2, d2, d3, e2, e3, e4, e5, e6, f2, f3, f4, f5, f6 (13)
  - c4: K on c2, c3, d2, d3, e2, e3, e4, e5, e6, f2, f3, f4, f5, f6 (14)

  This is the **minimal family for the proof as written** (each arises from a legal White reply).
- **Chess.** Cached Syzygy (unpacked copy, `src/tb_k68.py`, `logs/tb_k68.out`; the copy was deleted after use). All
  eight root/q positions and every move there agree with PROOF.md §7: roots, Black to move, every move a White win;
  roots, White to move, only the freeze wins; q's, Black to move, every move loses; q's, White to move, every move
  loses. The leaves: `src/q68.cpp` finds White wins at 460/460 (`logs/q68_leaves.out`). The audit of G3 is in
  `logs/q68_audit_all.out` and `q68_audit_pattern.out`. Sanity checks of q68: stalemate draws, KQK wins, Kb2+pc2 against
  Qe1/Kh8 (White to move) does not win.

## 6. Lemma B by hand: not achieved

I did not find a hand proof of even the 42-position family.

- No uniform first move works. Over the 119 Black-to-move positions after White's first move in the family, the most
  common winning moves are …Ka5 (116), …Ka6 (114), …Ka7 (109) and …c5 (96). None wins in all.
- **Hard cases**: γ on c2 with White's king on b3, c3 or d3 (P: L36); γ on c4 with the king on c3 (L38). White's king
  reaches b4/c4 and attacks the pawn pair. White also defends with **stalemate**: the P lengths exceed the sum-rule
  lengths by up to 12 plies (e.g. Kc3/γ c4: L38 in P against L26 when stalemate loses). So a hand proof has to handle
  stalemate traps of Black's own king, not only races.
- **Easier part**: White's king on the e/f files at rank ≥ 4 (L18–L28). Here a plan of the kind "…Ka5–a4–b3 takes γ
  while pc6 keeps γ blocked, then the b-pawn runs" looks feasible, but I have not written it out. Black's c6 pawn
  blocks γ for good, so White can only win by taking both Black pawns, or b7 and then c6, before Black promotes. A
  zone proof would bound that race.

So Proposition 4.25 stays **PROVED given CHECKED-2 (Lemma B, 42 positions)**. The K70 blind attempt is the place to
look next (I did not read it).

## 7. Labels (PROOF.md §0)

| row | PROOF.md | referee |
|---|---|---|
| (O0) | PROVED | PROVED (add K1/K2, G0) |
| (O1) | PROVED | PROVED (with G1) |
| (O2) | PROVED | PROVED |
| (O3) | PROVED | PROVED (with G1) |
| wrong pawn step loses | PROVED | PROVED (given (O4) at the other q, as stated) |
| king moves lose, freezes exact, (O4) | PROVED given Lemma B | PROVED given Lemma B (with G2) |
| Lemma B | CHECKED-2 | CHECKED-2 (three programs: o68, ax68q, r68); only 42 positions used |
| (B1) | PROVED | PROVED |
| Proposition 4.25 | PROVED given Lemma B | PROVED given CHECKED-2 (Lemma B) |
| chess, Black to move / freeze rows | PROVED given KNOWN | **KNOWN (Syzygy)**; hand reduction PROVED given COMPUTED-1 (460 leaves, q68). Not "given KNOWN" (G3). |
| chess, q's White to move, non-freeze root moves | KNOWN | KNOWN (cache agrees) |

The corrected statement of Proposition 4.25 is in `EDITS.md`. It replaces the investigator's edit and was tested with
`apply_edits.py` on a scratch copy: 1 applied, 0 rejected.

## 8. Reproduce

```
c++ -O2 -std=c++17 -o r68 src/r68.cpp     # solver; ~10 s, 25 MB
./r68 query < logs/q_main.txt             # values of roots, q's and every move (P, sum, beside -1)
./r68 lemmaB ; ./r68 needed               # Lemma B family; Lemma C reduction set
LEAVES=leaves.txt ./r68 strat             # S_A against every reply; writes the chess leaves
python3 -I src/cmp_k68.py ../logs/compare_values.txt ./r68
c++ -O2 -std=c++17 -o q68 src/q68.cpp ; ./q68 < logs/leaves460.txt     # ~6 s, 55 MB
printf "AUDIT c4\nAUDIT c5\n" | ./q68     # (PATTERN=1 for the Qb8, Ka7/Kc7 shape)
mkdir tb && tar -xJf ../../K65/verify/logs/tbcache.tar.xz -C tb && python3 -I src/tb_k68.py tb/tbcache
```

Binaries were built in a scratch directory outside the repository; no process was left running.
