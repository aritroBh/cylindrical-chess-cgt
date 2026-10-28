# K20 final edits (fix round, 2026-10-27)

Integrator notes.

- LOOPY.md has changed since K20 wrote its EDITS.md (latest commit 44d1e72, and the K19 edits of 2026-10-27). Every OLD
  block below was rebased onto the current text and occurs exactly once in it (checked mechanically with
  `kings/delegate/apply_edits.py`: 0 rejected).
- K20 could not write a report file. Its report text is the `narrative` field of `kings/delegate/out/K20/summary.json`;
  cite that file and the referee report `kings/delegate/out/K20/VERIFY.md` (referee code in `kings/delegate/out/K20/verify/`).
- Every fix of VERIFY.md section 7 is applied in EDIT 1 and EDIT 2, and the new block the referee asks for (the title of
  Proposition 4.3) is EDIT 3. EDIT 4 is one more stale spot: the status row P4.3 states the scope correctly, but its first
  words ("In an isolated K+P group") read like the old title, so it now says that the scope is a frozen opponent.
- Fix list. (a) Distinct free roots are 341,931; 1,989,996 is the number of entries, which list sub-configurations.
  (b) dud is not the majority: 25.9 to 30.1 percent of K20's free entries, 2.6 to 10.3 percent of the distinct roots.
  (c) The unclassified share is 40.4 to 54.1 percent of the entries only for the free runs and box(2) (26 to 31 percent in
  box(0) and box(1)), and 45 to 62 percent of the distinct free roots. (d) `*` in one-file boxes means pawnless corridor
  roots. (e) "39 of 72" is 39 of 69 legal positions. (f) "No other number" is stated for the searched games only (at most
  two pairs, boards up to 8 files, B34). (g) "Every even-width cylinder" is height 6 only; the general parity is a
  CONJECTURE. (h) "A one-tempo race lead between two kings" is an interpretation: CONJECTURE. (i) "As the region
  dependence predicts" is untested: CONJECTURE. (j) on, off, {+|on}, {off|-} are battery names, not exact values.
  (k) The title of Proposition 4.3 no longer suggests that no finite king tempo exists anywhere.
- Labels. The +1, -1, {1|0}, {0|-1} examples on flat:6x6 and the class counts the referee reproduced are CHECKED-2 (K20's
  `kg.cpp`, K20's independent Python implementation, and the referee's `lk.cpp`, with its own 23,716-game battery). The
  referee's distinct-root counts and percentages come from one program (`lk.cpp` and its drivers) and are COMPUTED-1. The
  kpsolve chess results were not checked by the referee: COMPUTED-1. The P-model comparisons on flat:8x6 and the
  cylinders were reproduced by the referee's own P solver: CHECKED-2.
- Two judgment calls. (1) The referee's suggested text for the section 4 sentence ends in COMPUTED-1. EDIT 2 says
  CHECKED-2 for B34 on the searched games, because the absence of other numbers is a statement about class counts, which
  two implementations reproduce (the referee's `agg_all.txt` finds none of them on all six free boards), and LOOPY's
  definition of CHECKED-2 asks for two independently written implementations that agree. The wording keeps the scope
  (searched games, battery names) so no claim about all sums is made. (2) "About 1 percent" replaces K20's "up to 1
  percent" for the on and off names: 40 of 3,883 on cyl:6x6 is 1.03 percent.
- Not changed: the LK definition and the Sortie bullet's PROVED label (Lemma 1.7 gives equality of two models; EDIT 1 now
  says that "sortie as suicide" is a convention, because in chess a sortie can be a useful move, as the referee notes).

### EDIT open question 3, king fights (K20)
<<<<<<< OLD
3. King-against-king fights inside Z (opposition, shouldering) are genuine short or loopy games. What values
   occur? This is where finite king tempo can live, by Proposition 4.3.
=======
3. King-against-king fights inside Z (opposition, shouldering) are genuine short or loopy games. What values
   occur? This is where finite king tempo can live, by Proposition 4.3. **Answered in part by K20**
   (`kings/delegate/out/K20/summary.json`, task 2026-10-27, referee report `kings/delegate/out/K20/VERIFY.md`;
   AI work, no human re-derivation; revised after K20, 2026-10-27).
   - *Model.* The local game LK of K20: both kings move, the blocked pawn pairs (at most two, white pawn on rank
     r and black pawn on r + 1, files within a window of 4) are frozen, a king capture after which exactly one
     side has a passed pawn is a terminal for that side, a player with no move loses. A pass is a move in a
     summand (on, off, dud, the integers); a sortie is a step outside a region R (free board, or the pawn files
     widened by m = 0, 1, 2), and a sortie counted as a suicide gives the same values as a wall (PROVED, Lemma
     1.7; this is an equality of two models, and "sortie as suicide" is a convention, since in chess a sortie can
     be a useful move). A configuration is "faithful" when the frozen pawns are chess-frozen (two pairs on files
     at cyclic distance >= 2); the non-faithful configurations of cyl:6x6 are models only.
   - *Search.* cyl:6x6, 7x6, 8x6 and flat:6x6, 7x6, 8x6, 0 to 2 pairs, every legal king placement, free and
     box(0, 1, 2): 22 configurations per cylinder and 67, 82, 97 per flat board. The free runs list 1,989,996 root
     entries. A root is listed under every configuration whose pawn set contains its own (the pawnless king
     placements again and again, every single pair under each two-pair configuration containing it), so the free
     runs hold **341,931 distinct roots** (cyl:6x6 14,804, cyl:7x6 22,313, cyl:8x6 31,397, flat:6x6 47,196,
     flat:7x6 85,655, flat:8x6 140,566; the referee's count, COMPUTED-1). Value = outcome pair in the D-sum with a
     battery of 34 games (B34), and with 4553 games (B4553) for the named classes. The names are battery names:
     on, off, {+|on} and {off|-} are not exact values (B4553 separates some of the roots they name, see "Not
     settled"). For every faithful configuration of every free run (cyl 16 each, flat:6x6 43, flat:7x6 55,
     flat:8x6 64) and for the boxes m = 0, 1, 2 of flat:6x6 and flat:8x6, all class counts of K20's `kg.cpp` equal
     those of the referee's own `lk.cpp`, written from the definition text (CHECKED-2). K20's independent Python
     implementation also agrees for B34 on 57,324 roots of 16 configurations, not all (0 mismatches over 3,898,032
     outcomes; CHECKED-2). Percentages below are shares of the root entries (K20's tables, which the referee
     reproduced) unless they say "distinct".
   - *Values that occur* (battery sense; existence of each named value CHECKED-2, three implementations): dud
     (both kings can shuffle; the largest named class among the entries, 26 to 30 percent of the free entries, but
     only 3 to 10 percent of the distinct free roots), on and off (one king frozen), 0 (a mutual zugzwang in which
     both kings have moves, cyl:6x6 `Kb3 kf2 Pa2 pa3`), \*, tis and tisn, {on|off}, the switches {1|0} and
     {0|-1}, and the **finite tempi +1 and -1**. The `*` roots with pawns occur only for two pairs on cylinders
     (faithful cases cyl:7x6 `Ke2 kf4 Pa2 pa3 Pc3 pc4` and cyl:8x6 `Kc2 kb4 Pa2 pa3 Pd3 pd4`; none with one pair,
     none on a flat board). The `*` roots of one-file boxes are pawnless corridor roots, for example `Ka1 ka4`
     (two kings walking on the pawn file, no pawn on the board), and no pawn-bearing root of a one-file box is
     `*`. No root equals +-2, +-3, +-1/2, up, down, up\*, down\*, \*2, over or under in B34, on any of the six free
     boards. Everything else is decisive (a forced decisive event in some context: {+|}, {|-}, {+|-}, {+|0},
     {0|-}, {+|on}, {off|-}) or "loopy, not classified" (298 distinct B34 signatures on cyl:6x6 and 486 on
     flat:6x6 over all configurations; COMPUTED-1). The unclassified share is 40.4 to 54.1 percent of the entries
     of the free runs and of box(2), 26 to 31 percent in box(0) and box(1), and 45 to 62 percent of the distinct
     free roots (COMPUTED-1). Short roots (acyclic game graphs) occur only in one-file boxes, with the kings on
     the pawn file (for example `Ka4 ka6 Pa2 pa3` is {+|} and `Ka6 ka4 Pa2 pa3` is 0); the free runs and,
     on flat:6x6, box(1) have none (CHECKED-2 on the 6x6 boards). Every other root is loopy.
   - *A finite tempo exists* (CHECKED-2: `kg.cpp`, the Python implementation and the referee's `lk.cpp`).
     flat:6x6 `Kc3 ka4 Pa2 pa3 Pc4 pc5` (faithful, F_Z = {a, b, c}, both kings on F_Z) has value +1 and `Ka3 kc4
     Pa4 pa5 Pc2 pc3` has -1; `Kd3 ka4 Pa2 pa3 Pc4 pc5` is {1|0} and `Ka3 kd4 Pa4 pa5 Pc2 pc3` is {0|-1} (the same
     names on flat:7x6 and 8x6). The +1 root agrees with the integer 1 on all 4553 games of B4553 and on all
     23,716 games of the referee's own extended battery. Sum test: every ordered pair of named roots of this
     configuration adds as the references do (referee's exhaustive `lk allpairs`: 73,984 pairs, and 2,601, 14,884,
     34,969 in the boxes m = 0, 1, 2, 0 mismatches; CHECKED-2). K20 reports 115,085,243 pairs of root entries over
     the configurations of three boards, 0 mismatches (COMPUTED-1; the referee did not rerun that count). On the
     cylinders of width 6, 8, 10 with six ranks each single blocked pair has king placements of value +1 and -1
     (cyl:6x6 `Kd3 kd1 Pa2 pa3`; 7, 11, 13 roots of each sign over the pawn ranks 2, 3, 4), on no cylinder of width
     5, 7, 9 with six ranks, and no two-pair run of cyl:7x6 has one (B34 names; CHECKED-2). CONJECTURE: the same
     parity holds for other heights and for other widths; it is untested. Proposition 4.3 is not contradicted:
     its statement is scoped to a frozen opponent, and in these roots the opponent has king moves inside Z.
     Interpretation, CONJECTURE: the tempo is a one-tempo race lead between two kings that reply inside Z, not a
     reservoir (nothing computed distinguishes a race lead from other mechanisms). CONJECTURE: a lead of two
     tempi is already decisive, which would explain why +-2 and +-3 never occur (untested).
   - *The value depends on the room outside F_Z* (CHECKED-2). The same root `Kc3 ka4 Pa2 pa3 Pc4 pc5` is 0 when
     the kings are confined to {a, b, c}, tis when they have {a..d}, +1 when they have {a..e} or the whole board;
     `Kd3 ka4 ...` is unclassified with {a..d} and {1|0} with {a..e} or the whole board. So the tempo is a value
     of the group together with its buffer, not of F_Z alone.
   - *Full-board confirmation in the promotion model P* (kpsolve `kp_p --pmodel` with real kings, flat:8x6; the
     referee's own P-model solver `pmini2` gives the same P results on every legal position, 48 + 56 + 69, CHECKED-2).
     The group beside a context on file g (H0, Hp1, Hm1, H\*, H\*2 of PREDICTIONS.md; prediction = outcome of
     value(G) + value(H), value(H) by cylcgt; the referee recomputed these predictions with its own sums) matches
     in 46 of 48 positions, all 24 for the values +1 and -1; the two misses are the bare switch roots (a decisive
     event that is not a P-win, a (V2) failure). With the context on file e (next to the buffer) 39 of 69 legal
     positions match (3 of the 72 are illegal: a context pawn attacks a king), with contexts on f and h 31 of 56
     (CHECKED-2). CONJECTURE: the misses on files e, f, h come from the room that the context pawns take away from
     the kings; nothing computed tests this.
   - *D-model against P and chess.* The D-model decisive event is not always a P-win. For the +-1 roots of cyl:6x6
     the D-value agrees with the P result in every position tested (the referee's `pmini`: 28 of 28 single-pair
     positions; the 8 two-pair roots were not rechecked); on cyl:8x6 it agrees in 171 of 198 positions of K20
     (13.6 percent differ, the other king catches the new passer; the referee's solver reproduces the rate, 6 of
     44 single-pair positions differ). The P parts are CHECKED-2. In chess (kpsolve, cap 1) the +-1 roots of
     cyl:6x6 agree with the D-value in 254 of 256 positions (2 undecided bounds): COMPUTED-1, not checked by the
     referee, and the chess rows of the flat:6x6 runs (some with differing bounds) were not checked either.
   - *Not settled.* B34 and B4553 name values only up to those batteries (a proof of equality in all sums is
     open question 4). The names on and off are not exact for about 1 percent of the roots they name (B4553
     separates 40 of 3,883 on cyl:6x6; {on|off} 6 of 130 on flat:6x6), and with the nested battery of the K20
     description the referee found the roots named {+|on} and {off|-} separated as well, on two configurations of
     cyl:6x6. The contexts tested are small pawn sets on one or two files. B4553 was run in full only on flat:6x6,
     cyl:6x6 and cyl:8x6 (selected configurations elsewhere), and the full flat:8x6 run was stopped early. Nothing
     was proved beyond Lemma 1.7 for the sortie convention.
>>>>>>> NEW

### EDIT section 4 sentence on king fights (K20)
<<<<<<< OLD
- It can also come from genuine king-against-king fights, where the opponent *replies inside Z*: opposition
  and shouldering. Those are not reservoirs, and they can have any value.
=======
- It can also come from genuine king-against-king fights, where the opponent *replies inside Z*: opposition
  and shouldering. Those are not reservoirs. K20 found the finite values +1 and -1 and the switches {1|0} and
  {0|-1} among them (§8, question 3) and, among the searched games (at most two pairs, boards up to 8 files,
  battery B34), no other number; "any value" is not supported (CHECKED-2 for B34 on the searched games, battery
  names only; revised after K20, 2026-10-27).
>>>>>>> NEW

### EDIT Proposition 4.3 title (K20 referee)
<<<<<<< OLD
**Proposition 4.3 (no finite king tempo in isolated K+P groups). FALSE as originally stated →
PROVED after repair.** Let Z be a king group in a position without officers, with a buffer. Suppose side s plays a
=======
**Proposition 4.3 (no finite king tempo from safe king steps inside F_Z against a frozen opponent; title revised
after K20, 2026-10-27). FALSE as originally stated → PROVED after repair.** The statement and the proof are unchanged
and were already scoped to a frozen opponent. A finite king tempo does exist in isolated K+P groups when the opponent
is not frozen (K20, §8 question 3; CHECKED-2), so the old title ("in isolated K+P groups") suggested too much.
Let Z be a king group in a position without officers, with a buffer. Suppose side s plays a
>>>>>>> NEW

### EDIT status row P4.3 scope (K20 referee)
<<<<<<< OLD
| P4.3 | In an isolated K+P group, a king's spare tempo from safe steps inside F_Z (opponent frozen at both ends, mover not in check) is 0 or ∞, never a finite n ≥ 1 | PROVED after repair (hypotheses added) |
=======
| P4.3 | In an isolated K+P group, a king's spare tempo from safe steps inside F_Z (opponent frozen at both ends, mover not in check) is 0 or ∞, never a finite n ≥ 1. The scope is a frozen opponent: against an opponent that is not frozen a finite king tempo exists (the +1 and -1 roots of K20, §8 question 3; CHECKED-2; revised after K20, 2026-10-27) | PROVED after repair (hypotheses added) |
>>>>>>> NEW
