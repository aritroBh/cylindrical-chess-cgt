# K22 EDITS_FINAL (fix round, 2026-10-27)

Integrator notes.
- Item: K22, Lemma 2.9 without its added hypothesis. The earlier text is replaced by the repaired lemma under (B1) and a
  counterexample remark. Referee verdict: ACCEPT WITH FIXES (`VERIFY.md`).
- LOOPY.md now also holds the K19 and K23 edits of 2026-10-27 (commit fb7d4a4). Every block below was rebased: each OLD text
  was checked against the current file and occurs exactly once. The three OLD texts of EDITS.md had not moved or changed
  (K19 and K23 did not touch the L2.9 rows or Lemma 2.9), so they are the same; the NEW texts are rewritten.
- Referee fixes applied:
  1. Status row: the claim about the 74,469,430 roots now says "no White win with at
     most one attacked s̄ pawn among 74,469,430 roots, within the boards and pawn counts searched", with the label
     COMPUTED-1 (one C++ solver, Python spot check on 92 roots, not re-run by the referee) and says that the proof of (B1) is separate.
  2. Last bullet of the Remark: now "in Q_Z, after the reply r, s has no pawn (r captures it: Kxd7, Kxb5), and s̄ has one Z-pawn, so
     (B1) holds anyway". In the starting positions (7.2 `Pd7`, P5 `Pb5`) s does have a pawn.
  3. "The smallest board is 5 ranks" is now "a counterexample needs at least 5 ranks" and says that width minimality is not established.
     In fact the integrator found a narrower counterexample than the flat:4×5 one: flat:3×5 `Kc4 ka5 Pa2 Pa3 pb3 pb4`
     (Black to move, T = 3 with and without the queen clause, K22's Python solver `local_py.py` and the referee's `mylocal.py` agree;
     the integrator re-ran both). So the old sentence "flat:4×5 is the smallest found" would have been wrong, and the text now says
     that 3 files is the narrowest found and that fewer than 3 files was not searched.
- Further label corrections made by the integrator (no label stronger than the evidence):
  - The P-model win of the cyl:7×6 position is COMPUTED-1 (one kpsolve build; the referee's `kp_p` is the same code, which by the
    Labels rule does not count as a second implementation). EDITS.md had written "CHECKED-2 and a P-model run" for the whole
    sentence. The local-game counterexamples keep CHECKED-2: K22's C++ solver, K22's independent Python solver and the referee's
    solver, written from Definition 2.6, agree.
  - The 74.5 M count and the 22,456 / 2,233,320 figure are COMPUTED-1 and say that the referee did not reproduce them; the referee's
    own samples give 5% to 8% lost among roots with two or more attacked pawns, because of small boards and capped pawn counts, so
    the 1.0% is a property of K22's enumeration only. The text says so.
  - "(revised after K22, 2026-10-27)" tags added to the status row, the summary row and the Remark.
  - One line added to the lemma's proof: a capture by s is never a promotion (the referee checked this step; the text did not say it).
  - The checks of the proof (referee's step-by-step re-derivation, small machine runs of the strategy) are recorded in the Remark as an
    AI check and as COMPUTED-1 data, not as part of the proof.
- Referee point 2 of the EDITS list (the quotation of R3 item 4) was withdrawn by the referee. The quotation is kept, with the
  hyphen of REVIEWS.md line 241 ("s-pawn") restored, so that it is word for word.
- Points not adopted: none.
- Not changed, but noticed (outside the referee's list, for the integrator to decide): §5.2, "White's sorties", says that Lemma 2.9
  makes (L1) fail for Kd5, Ke5 and Kf5. For Kd5 and Kf5 the king is not yet on the e file at Q_Z, so the lemma as stated does not apply
  at once. The argument still works (s moves Ke5 at its first turn, which is a legal move, and from s̄'s first turn on (J1) and (J2)
  hold: s has no pawn, and s̄ has the single pawn e7), so the claim is true, but the lemma would need the clause "or the king can step
  onto such a square at once, when no s̄ pawn can move first". This is old text (it predates K22), so no block is proposed here.
- No block is needed for the other uses of Lemma 2.9 (the P5 and P7 table rows, line 92 of the status table, §5.2): there s̄ has one
  Z-pawn, so (B1) is automatic.

### EDIT L2.9 status row
<<<<<<< OLD
| L2.9 | GAP → PROVED after repair (added hypothesis: s has no pawn on f ± 1). Without that hypothesis: CONJECTURE | R1 item 9, R3 item 4 |
=======
| L2.9 | GAP → PROVED after repair, now under the weaker hypothesis (B1): at most one s̄ pawn is attacked by an s pawn (it holds if s has no pawn on f ± 1, if s̄ has a single Z-pawn, and automatically on boards with 4 ranks) (revised after K22, 2026-10-27). **The statement without any hypothesis is FALSE** (revised after K22, 2026-10-27): with two attacked s̄ pawns s can lose, for example cyl:7×6 `Ka5 kc6 Pc3 Pc4 pb4 pb5` with Black (s) to move, F_Z = {a, b, c}: White (s̄) forces a promotion within 3 moves against a defender who may pass (CHECKED-2: K22's C++ and Python solvers and the referee's own solver agree). The flat:4×5 version `Kd4 kb5 Pb2 Pb3 pc3 pc4` is also hand-verified, and a flat:3×5 version `Kc4 ka5 Pa2 Pa3 pb3 pb4` is CHECKED-2. The cylinder position is also a White win in P with real kings (COMPUTED-1: one kpsolve build). Bounded search (K22: up to 3 + 3 pawns, and 4 + 4 on some small boards): no White win with at most one attacked s̄ pawn among 74,469,430 roots, within the boards and pawn counts searched (COMPUTED-1: one C++ solver, with a Python spot check on 92 roots; the proof of (B1) is separate and does not use this search) | R1 item 9, R3 item 4; K22 |
>>>>>>> NEW

### EDIT L2.9 summary row
<<<<<<< OLD
| L2.9 | Blockade: a defender who may pass and whose king stands in front of the pawn is never beaten | PROVED after repair, with the added hypothesis that s has no pawn on f ± 1 (CONJECTURE without it) |
=======
| L2.9 | Blockade: a defender who may pass and whose king stands in front of the pawn is never beaten, provided at most one s̄ pawn is attacked by an s pawn (B1) | PROVED after repair under (B1) (revised after K22, 2026-10-27); (B1) covers "s has no pawn on f ± 1" and "s̄ has one Z-pawn". Without (B1) the statement is FALSE: counterexamples with two attacked s̄ pawns, hand-verified for one and CHECKED-2 for the others |
>>>>>>> NEW

### EDIT Lemma 2.9 statement and proof
<<<<<<< OLD
**Lemma 2.9 (blockade). PROVED after repair (added hypothesis).** In Q_Z, suppose s̄'s only Z-pawns are on
one file f, and s's king stands on a square of f in front of s̄'s front pawn there. **Assume further that s
has no pawn on f ± 1 that an s̄ pawn could capture.** If s may pass (k = ∞), s̄ never promotes.

*Proof.*
- s passes forever. That is legal: s is never in check, because s̄'s pawns on f attack only files f ± 1, and
  a king never gives check.
- No s̄ pawn leaves file f: a capture needs an s-piece on f ± 1. By hypothesis s has no such pawn, and its
  king cannot be captured.
- So every s̄ pawn on f must pass the king's square, which never empties. ∎

**Without the added hypothesis the statement is a CONJECTURE** (an s-pawn on f ± 1 could be captured,
letting an s̄ pawn leave f). The uses in §5.2 and P5 are unaffected because s has no pawns there (revised
after review: R1 item 9, R3 item 4).
=======
**Lemma 2.9 (blockade). PROVED after repair, under the hypothesis (B1) (revised after K22, 2026-10-27).** In Q_Z, suppose:
- all of s̄'s Z-pawns stand on one file f, and s's king stands on a square of f in front of s̄'s front pawn, so above every s̄ pawn;
- **(B1)** at most one s̄ pawn is *attacked by an s pawn*. An s̄ pawn on (f, x) is attacked iff an s pawn stands on the square
  diagonally in front of it (on file f ± 1, one rank on in s̄'s direction). The relation is symmetric: the two pawns attack each
  other, and the one that is to move may capture. (B1) holds if s has no pawn on f ± 1 (the earlier hypothesis), whenever s̄ has
  exactly one Z-pawn, and on every 4-rank board (counted from s̄'s side, s̄ pawns stand on rank 2 or higher, so two attacked s̄ pawns
  need an s̄ pawn on rank 3 or higher, attacked by an s pawn on rank 4 = s̄'s last rank, where no s pawn stands; so H ≥ 5 is needed);
- s is to move and may pass (k = ∞). An e.p. right carried by Q_Z was therefore created by s̄.

Then s has a strategy against which no s̄ pawn ever promotes and s is never mated. So s̄ wins L_T(Q_Z) for no T, in the reading
(L1) and in the reading (L1_P).

*Proof.* The strategy of s: if some s̄ pawn is attacked by an s pawn, capture it with an s pawn that attacks it; otherwise pass.
The king of s never moves. Let k be its rank. Write "attacked" for "attacked by an s pawn". Claim (J): at every turn of s̄, (J1) every
s̄ pawn stands on file f, below the king of s; (J2) no s̄ pawn is attacked. At the root, (J1) is the hypothesis. (J2) is not yet true
there, but at s's first turn (B1) leaves at most one attacked pawn, and the strategy captures it, so (J2) holds at s̄'s first turn.
Then the induction:
- *s̄ moves; (J1) and (J2) hold before its move.* A king move changes no pawn of either side except that it may capture an s pawn,
  and removing pawns attacks nothing new. A pawn move on f stays on f and below the king: a push needs an empty target and a double
  step needs two empty squares, and the king's square is occupied; so no s̄ pawn reaches a rank above k − 1, in particular none
  reaches its last rank (k ≤ H), and **no promotion is possible** by a pawn on f. A pawn capture needs an s pawn diagonally in front,
  which is exactly an attack, and by (J2) there is none; an e.p. capture needs an e.p. right created by a double step of s, and s
  never double-steps (it captures or passes), while a right present in Q_Z was created by s̄. So no s̄ pawn leaves f, and (J1) holds
  after the move. Only the moved pawn can be newly attacked, because the attack relation is a pairing of an s̄ pawn's square with an
  s pawn's square, and no other pawn moved. So at s's turn **at most one s̄ pawn is attacked**.
- *s moves.* s is not in check: its king stands on f, and s̄'s pawns stand on f and attack files f ± 1 only (on a cylinder of width
  2 the file f ± 1 is the other file, still not f); a king gives no check. So the pass is legal, and so is a capture (no sliders, no
  pins; the king stands where it was). A capture by s is never a promotion: it lands on the square of an s̄ pawn, and s̄ pawns stand
  on rank 2 or higher from s̄'s side, so that square is not on s's last rank. If an s̄ pawn P is attacked, the capture removes P. The
  capturing pawn Q came from file f ± 1 and lands on f, so it attacks no square of file f; and Q attacked only P among s̄'s pawns (it
  attacks two squares, both on files at distance 1 from Q's file, and at most one of them is on f, apart from the width-2 cylinder
  where both squares coincide). The other pairs are untouched. So after s's move (J2) holds, and (J1) holds, since P was the only pawn
  removed.
By induction, no s̄ pawn promotes, and none ever leaves f; s is never in check at its turns, so it is never mated. s̄ cannot win L_T for
any T. ∎ (The proof does not use that s̄'s king is confined to F_Z, nor the move count.)

**Remark (K22: the hypothesis (B1) is needed, and it is not necessary; revised after K22, 2026-10-27).**
- *Without (B1) the lemma is FALSE.* The earlier proof ("s passes forever") fails when an s̄ pawn can capture an s pawn. The repair
  suggested in review R3 item 4 ("pass, but capture any s̄ pawn that attacks an s-pawn") fails too, as soon as two s̄ pawns are
  attacked: s captures one and s̄ captures with the other, and the pawn that has left f is no longer blockaded. Counterexamples, all
  with Black = s to move, in the local game of Definition 2.6 with k = ∞, with and without the queen clause. For each, White (s̄)
  wins within T = 3 moves, against every Black move, the pass included. CHECKED-2 for each: at least two independently written
  solvers agree (K22's C++ solver, K22's Python solver, the referee's own solver written from the definition; see each line).
  - cyl:7×6, F_Z = {a, b, c}: `Ka5 kc6 Pc3 Pc4 pb4 pb5`. s̄ = White has two Z-pawns on c, s has b4, b5 (b4 attacks c3, b5 attacks c4).
    After 1…bxc4 White plays 2.cxb4, and the pawn runs to b6, which Ka5 guards; the black king cannot step to b5 or b6. Every Black move
    loses, the pass included (3 White moves at most). The same position is a White win in P with real kings (`kp_p --pmodel`;
    COMPUTED-1, because the referee's run used the same code as K22's); each of Black's five legal moves loses.
  - flat:4×5, F_Z = {a, b, c, d}: `Kd4 kb5 Pb2 Pb3 pc3 pc4`: each Black move, the pass included, loses within 3 White moves. After
    a pass, 2.bxc4+ and 3.c5=Q (c4 and c5 are guarded by Kd4); after 1…cxb3 2.bxc3, a black pawn run is too slow because c3–c4 gives
    check to the king on b5. Hand-verified (by K22 and again by the referee), and CHECKED-2 as above.
  - flat:3×5, F_Z = {a, b, c}, f = a: `Kc4 ka5 Pa2 Pa3 pb3 pb4`. s̄ = White has two Z-pawns on a, s has b3, b4 (b3 attacks a2, b4
    attacks a3), and the black king stands on a5, above both. CHECKED-2 (K22's Python solver and the referee's solver; the
    integrator re-ran both); not hand-verified.
  - *Size.* A counterexample needs at least 5 ranks, because (B1) is automatic on 4 ranks (PROVED, in the statement above), and 5
    ranks suffice (the flat:4×5 and flat:3×5 examples). Any violation of (B1) needs two s̄ pawns on f and two s pawns. The width is
    not established as minimal: 3 files is the narrowest board with a counterexample found, and boards with fewer than 3 files were
    not searched.
- *(B1) is sufficient and not necessary.* In K22's bounded enumeration (the boards and pawn counts of the search), s̄ wins 22,456 of
  the 2,233,320 roots with two or more attacked s̄ pawns (about 1.0%); the positions of the kings decide. COMPUTED-1: one C++
  implementation, a Python solver agreeing on a spot check of 92 sampled roots, and the referee did not reproduce the counts. The
  referee's own random samples (its solver, win searched within T ≤ 6 or 7) show the same pattern, no White win with at most one
  attacked pawn and wins only with two or more; they give 5% to 8% lost on flat:4×5 and cyl:7×6, a higher share than 1.0%
  because of the small boards and capped pawn counts, so the 1.0% describes K22's enumeration and is not a general rate.
- *Checks of the proof.* The referee re-derived the proof step by step against Definition 2.6 and found no gap (an AI check; no
  human has re-derived it). The strategy was also run on small boards: 0 violations in K22's 6,355 sampled roots with at most one
  attacked pawn on four boards, and in the referee's 4,534 roots on flat:3×5 (COMPUTED-1 each; not part of the proof).
- The uses in §5.2, P5 and P7 are unaffected. In the starting positions s may have a pawn (7.2 `Pd7`, P5 `Pb5`), but in Q_Z, after
  the reply r, s has no pawn (r captures it: Kxd7, Kxb5), and s̄ has one Z-pawn, so (B1) holds anyway.
>>>>>>> NEW
