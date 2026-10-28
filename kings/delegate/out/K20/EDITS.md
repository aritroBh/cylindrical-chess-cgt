### EDIT open question 3, king fights (K20)
<<<<<<< OLD
3. King-against-king fights inside Z (opposition, shouldering) are genuine short or loopy games. What values
   occur? This is where finite king tempo can live, by Proposition 4.3.
=======
3. King-against-king fights inside Z (opposition, shouldering) are genuine short or loopy games. What values
   occur? This is where finite king tempo can live, by Proposition 4.3. **Answered in part by K20**
   (`kings/delegate/out/K20/summary.json`, task 2026-10-27; AI work, no human re-derivation; referee report
   `kings/delegate/out/K20/VERIFY.md`, ACCEPT WITH FIXES, fixes applied here).
   - *Model.* The local game LK of K20: both kings move, the blocked pawn pairs (at most two, white pawn on rank
     r and black pawn on r + 1, files within a window of 4) are frozen, a king capture after which exactly one
     side has a passed pawn is a terminal for that side, a player with no move loses. A pass is a move in a
     summand (on, off, dud, the integers); a sortie is a step outside a region R (free board, or the pawn files
     widened by m = 0, 1, 2), and a sortie counted as a suicide gives the same values as a wall (PROVED, Lemma
     1.7; a convention, since in chess a sortie can be a useful move). A configuration is "faithful" when the
     frozen pawns are chess-frozen (two pairs on files at cyclic distance >= 2).
   - *Search.* cyl:6x6, 7x6, 8x6 and flat:6x6, 7x6, 8x6, 0 to 2 pairs, every legal king placement, free and
     box(0, 1, 2): about 2.0 million root entries (a root is listed under every configuration containing its pawn
     set; the free runs hold 341,931 distinct roots), 22 configurations per cylinder and 67, 82, 97 per flat
     board. Value = outcome pair in the D-sum with a battery of 34 games (B34), and with 4553 games (B4553) for
     the named classes. COMPUTED-1 by `kg.cpp`; CHECKED-2 for B34 on 57,324 roots by an independent Python
     implementation (0 mismatches over 3.9 million outcomes), and every class count of every faithful
     configuration of the six free runs is reproduced by a third implementation (the referee's `lk.cpp`,
     `verify/`). Names are battery names: on, off, {+|on} and {off|-} are not exact (B4553 separates some of them).
   - *Values that occur* (battery sense; every root is loopy except the trivial roots of one-file boxes): dud (both
     kings can shuffle; the largest named class among the entries, 26 to 30 percent of them, but only 3 to 10
     percent of the distinct roots), on and off (one king frozen), 0 (a mutual zugzwang in which both kings
     have moves, cyl:6x6 `Kb3 kf2 Pa2 pa3`), \*, tis and tisn, {on|off}, the switches {1|0} and {0|-1}, and the
     **finite tempi +1 and -1**. No root equals +-2, +-3, +-1/2, up, down, over or under in B34. Everything else
     is decisive (a forced decisive event in some context: {+|}, {|-}, {+|-}, {+|0}, {0|-}) or "loopy, not
     classified" (many hundreds of distinct B34 signatures; 41 to 54 percent of the entries of the free runs, 45
     to 62 percent of the distinct roots, and 26 to 31 percent in the narrowest boxes). The value \* occurs only
     for two pairs on cylinders (and for pawnless roots of one-file boxes).
   - *A finite tempo exists.* flat:6x6 `Kc3 ka4 Pa2 pa3 Pc4 pc5` (faithful, F_Z = {a, b, c}, both kings on F_Z) has
     value +1 and `Ka3 kc4 Pa4 pa5 Pc2 pc3` has -1; `Kd3 ka4 Pa2 pa3 Pc4 pc5` is {1|0} and `Ka3 kd4 Pa4 pa5 Pc2 pc3`
     is {0|-1} (the same values on flat:7x6 and 8x6). These roots agree with the integer 1 on all 4553 games of
     B4553 (and on 23,716 games of the referee's own battery), and every ordered pair of named roots of that
     configuration adds as the references do (sum test, 0 mismatches: the referee reran all 73,984 ordered pairs of the
     free run and the box runs; K20's own count of 115 million entries over three boards was not rerun). On the cylinders of width 6, 8, 10 with six ranks each single blocked pair has king
     placements of value +1 and -1 (cyl:6x6 `Kd3 kd1 Pa2 pa3`), on no odd-width cylinder (5, 7, 9) (CHECKED-2
     for height 6; CONJECTURE for other widths and heights). Proposition 4.3 is not contradicted, because it
     is scoped to a frozen opponent: the tempo comes from kings that reply inside Z, not from a reservoir
     (interpretation, CONJECTURE: nothing computed distinguishes a one-tempo race lead from other mechanisms).
     CONJECTURE: a lead of two tempi is already decisive, which would explain why +-2 and +-3 never occur.
   - *The value depends on the room outside F_Z.* The same root `Kc3 ka4 Pa2 pa3 Pc4 pc5` is 0 when the kings are
     confined to {a, b, c}, tis when they have {a..d}, +1 when they have {a..e} or the whole board. So the
     tempo is a value of the group together with its buffer, not of F_Z alone (CHECKED-2).
   - *Full-board confirmation* (kpsolve P model with real kings, `kp_p --pmodel`, flat:8x6): the group beside a
     context on file g (H0, Hp1, Hm1, H\*, H\*2 of PREDICTIONS.md; prediction = outcome of value(G) + value(H),
     value(H) by cylcgt) matches in 46 of 48 positions, all 24 for the values +1 and -1; the two misses are the
     bare switch roots (a decisive event that is not a P-win, a (V2) failure). With the context on file e (next
     to the buffer) 39 of 69 legal positions match (3 of the 72 are illegal: a context pawn attacks a king), with
     contexts on f and h 31 of 56; that the region dependence explains the drop is a CONJECTURE. An independent
     P-model solver reproduces all of these numbers (CHECKED-2). In chess (cap 1) the +-1 roots of cyl:6x6
     agree with the D-value in 254 of 256 positions (2 undecided bounds; COMPUTED-1, not rerun by the referee).
   - *Not settled.* B34 and B4553 name values only up to those batteries (a proof of equality in all sums is
     open question 4); the names on and off are not exact for up to 1 percent of the roots they name (B4553
     separates them); the contexts tested are small pawn sets on one or two files; nothing was proved.
>>>>>>> NEW

### EDIT section 4 sentence on king fights (K20)
<<<<<<< OLD
- It can also come from genuine king-against-king fights, where the opponent *replies inside Z*: opposition
  and shouldering. Those are not reservoirs, and they can have any value.
=======
- It can also come from genuine king-against-king fights, where the opponent *replies inside Z*: opposition
  and shouldering. Those are not reservoirs. K20 found the finite values +1 and -1 and the switches {1|0} and
  {0|-1} among them (§8, question 3) and, among the searched games (at most two pairs, boards up to 8 files,
  battery B34), no other number; "any value" is not supported (COMPUTED-1).
>>>>>>> NEW

### EDIT title of Proposition 4.3 (K20 referee suggestion)
<<<<<<< OLD
**Proposition 4.3 (no finite king tempo in isolated K+P groups).
=======
**Proposition 4.3 (no finite king tempo from safe king steps inside F_Z against a frozen opponent).
>>>>>>> NEW
