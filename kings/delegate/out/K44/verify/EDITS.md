# K44 edits for LOOPY.md (section 8, open question 3), 2026-11-22 (referee's replacement set; changes: labels upgraded where the referee's own solver `rk` reproduces the numbers)

Every OLD block occurs exactly once in the current LOOPY.md (checked with `kings/delegate/apply_edits.py` on a copy).
Labels follow the note: nothing here is PROVED; solver results are COMPUTED-1 or CHECKED-2.

### EDIT K44 main bullet, before the room paragraph
<<<<<<< OLD
   - *The value depends on the room outside F_Z* (CHECKED-2). The same root `Kc3 ka4 Pa2 pa3 Pc4 pc5` is 0 when
=======
   - **K44 extended the search (new, K44, 2026-11-22; `kings/delegate/out/K44/findings.txt`, with scripts, logs and tables; AI work, no human
     re-derivation).** Same LK and battery B34. Boards cyl:W×6, W = 6 to 10 (extra: W = 11, 12 over all configurations, W up to 16 and H = 7 for the over configuration); one, two or three blocked
     pairs on distinct files inside an arc of at most 6 files (K20: two pairs inside 4 files), pair ranks 2 to 4; the free board and the boxes
     m = 0, 1, 2 (kings confined to the minimal arc of files that holds the pawn files, widened by m; every minimal arc is its own region).
     2,131 (configuration, region) cases (793 faithful), 1,756,517 root entries. Baseline: K20's own enumeration re-run on cyl:6 to 10 and
     flat:6 to 8 (1,137 distinct B34 signatures; the free runs give the referee's distinct-root counts 14,804, 22,313 and 31,397). Three
     implementations: `kg44` (K20's `kg.cpp` with a configuration-file flag), the K20 referee's `lk.cpp` unchanged, and a new Python solver
     `lk3.py` written from the definition. `kg44` and `lk` agree on all 2,131 cases: every class count, the number of unclassified
     roots, and the set of distinct unclassified B34 signatures of every case (66,518 signatures in all; `lk` prints them in its own context order, translated). `kg44` and `lk3` agree on W = 6 (196 cases), W = 7 (288) and W = 8 (429), 0 differences in each (CHECKED-2).
     The K44 referee's solver `rk` (written from the definition text, a fourth implementation) gives the same multiset of B34 signatures as `kg44` in every
     one of the 2,131 cases (1,756,517 root entries), the same baseline (1,137 signatures: 967 on cylinders, 676 on flat boards) and the same 1,909 new signatures (CHECKED-2).
     - **over and under occur (CHECKED-2).** On cyl:10x6 with the three faithful pairs a2 c4 f2, the roots `Kc3 ka4 Pa2 pa3 Pc4 pc5 Pf2 pf3`
       and `Kc3 ka5 ...` have the B34 signature of over = {0 | over} (2 of 1,994 roots; each is a Black option of the other), and in
       the colour mirror a2 c4 h4 the roots `Kc2 ka4 ... Ph4 ph5` and `Kc3 ka4 ...` have that of under. They agree with over (under) on the
       4,553-game battery B4553 (`kg44`), on the referee's 23,716-game battery (`lk`) and on every D-sum of at most two B34 games (629
       contexts, both movers; `lk3`). The same configuration gives over on cyl:11x6 and cyl:12x6 (`lk`, `lk3` and the referee's `rk`), 13x6, 14x6, 16x6 and
       cyl:10x7 (`lk` and `rk`, CHECKED-2); not on cyl:9x6, and in none of the box regions. Before K44 over and under were absent from every
       search (the sentence above). The root graph is not a stopper (kings can shuffle), so "equals over" is a statement about the batteries,
       not about all sums. This is a value of the local king game LK, not an exact over group of Definition 4.8 in P (see the bullet "Over, none found").
     - **+1 and -1 on odd widths (CHECKED-2).** Three pairs on the files -2, 0, 2 with ranks 4, 2, 3 (faithful) have one +1 root for every width
       7 to 12: cyl:7x6 `Kf3 ka4 Pa2 pa3 Pc3 pc4 Pf4 pf5`, cyl:9x6 `Kh3 ka4 Pa2 pa3 Pc3 pc4 Ph4 ph5`, cyl:11x6 `Kj3 ka4 ...` (the first two by
       `kg44`, `lk`, `lk3`; the 11 and 12 by `lk` and `lk3`); the colour mirror has -1. So the parity rule of K31 below (+-1 only for even W) is a
       statement about one blocked pair, and so is "both kings on file W/2" (the cyl:7x6 root has the kings on files f and a). Two pairs: none
       on cyl:7x6, as before.
     - **Switches on cylinders (CHECKED-2).** {1|0} and {0|-1}, which K20 found on flat boards, occur on cylinders of width 7 to 12 with three
       pairs (faithful: cyl:8x6 `Kf3 ka4 Pa2 pa3 Pc3 pc4 Pg4 pg5` is {1|0}, `Kc3 kh4 Pa2 pa3 Pc4 pc5 Pe3 pe4` is {0|-1}); `*` occurs with two
       and three pairs. No root equals +-2, +-3, +-1/2, up, down, up\*, down\* or \*2 in any of the 2,131 cases (B34 names, CHECKED-2).
       So the numbers that occur are 0, +1, -1, and the infinitesimals are \*, over, under.
     - **Value classes (root entries of the 2,131 cases; CHECKED-2: class counts per case by `kg44` and `lk`, and the totals by the referee's `rk`).** 0 2,996; \* 76; +1 and -1
       98 each; over and under 4 each; {1|0} and {0|-1} 21 each; tis and tisn 336 each; {on|off} 3,938; dud 88,554; on and off 64,078 each; the
       decisive named classes 646,164; unclassified loopy 885,715 (56.6 percent of the free entries, 40.2 of box(0), 39.4 of box(1), 51.8 of
       box(2); dud 1.1 percent of the free entries and 12.0 of box(0)). The unclassified roots have 2,955 distinct B34 signatures (950 in the
       baseline); only 65 of them equal the signature of a D-sum of at most four B34 games, so most are not sums of battery games.
     - **New values and the smallest.** 1,909 of the 2,976 B34 signatures of the new runs are absent from the baseline (206 of them in faithful
       cases); two are named (over, under). Smallest by pieces: two pairs at file distance 4 on cyl:8x6 (K20's window was 4 files), for example
       `Ka1 kb6 Pa3 pa4 Pe3 pe4`, faithful, a loopy value with 1,332 reachable nodes and a bisimulation-minimal graph of 353 nodes (given
       in full in `kings/delegate/out/K44/canonical/`; outcomes against the 34 contexts in `findings.txt`); it is not one of the 34 names and not the
       signature of a D-sum of at most four of them. Smallest named new value: the over root above (eight pieces, 1,994-node graph, no reduction by
       bisimulation). Every new signature is reproduced by `lk` (set comparison above); `lk3` also recomputed all 206 new signatures that occur in faithful
       cases (206 of 206 agree) and 1,625 of the 1,909 in all (0 disagreements); the referee's `rk` reproduces all 1,909.
     - **Faithful configurations in P (CHECKED-2).** The local game "alone" against the full-board P result (first promotion wins, real kings),
       every root with both sides to move; `ref3m` and `kp_p --pmodel` (file limit raised to 10 for cyl:10x6) agree on all 135,000 legal positions (140,504 lines; the rest is a placeholder for the pawnless configuration, illegal in both). The LK "alone" column was recomputed by the referee's `rk` (0 differences).
       cyl:7x6, the 33 faithful configurations with pawns of the free runs (K20's 15 and 18 with three pairs): 52,814 of 57,030 legal positions agree (92.6
       percent; one pair 73.2, two pairs 96.5, three pairs 94.3); cyl:8x6, 21 faithful configurations with at most two pairs: 52,992 of 57,944
       (91.5 percent); cyl:7x6, the six non-faithful two-pair configurations of K20: 6,980 of 12,050 (57.9 percent); cyl:10x6 a2 c4 f2 and a2 c4 h4:
       7,488 of 7,976, and all 4 over and 4 under positions agree. The misses are the known kind (a decisive event that the other king catches in P,
       K20's 13.6 percent on cyl:8x6; not traced one by one). Sums with contexts in P were not run for over, under or the odd-width +-1 roots.
     - **Not done.** Pairs on one file, more than three pairs, windows beyond 6 files, boxes beyond m = 2, heights other than 6 (except the over configuration on cyl:10x7), W above 12;
       why over needs W >= 10 and a third pair 5 files from the first is unexplained (CONJECTURE only: a single spare resource of one side).
   - *The value depends on the room outside F_Z* (CHECKED-2). The same root `Kc3 ka4 Pa2 pa3 Pc4 pc5` is 0 when
>>>>>>> NEW

### EDIT star roots with three pairs
<<<<<<< OLD
The `*` roots with pawns occur only for two pairs on cylinders
     (faithful cases cyl:7x6 `Ke2 kf4 Pa2 pa3 Pc3 pc4` and cyl:8x6 `Kc2 kb4 Pa2 pa3 Pd3 pd4`; none with one pair,
     none on a flat board).
=======
The `*` roots with pawns occur only for two or three pairs on cylinders (K44, 2026-11-22: three pairs added)
     (faithful cases cyl:7x6 `Ke2 kf4 Pa2 pa3 Pc3 pc4` and cyl:8x6 `Kc2 kb4 Pa2 pa3 Pd3 pd4`; none with one pair,
     none on a flat board).
>>>>>>> NEW

### EDIT no over or under, scope
<<<<<<< OLD
No root equals +-2, +-3, +-1/2, up, down, up\*, down\*, \*2, over or under in B34, on any of the six free
     boards.
=======
No root equals +-2, +-3, +-1/2, up, down, up\*, down\*, \*2, over or under in B34, on any of the six free
     boards (with at most two pairs inside four files; revised after K44, 2026-11-22: over and under do occur with three pairs on cyl:10x6 and wider,
     see the K44 paragraph below; the others still do not occur in any of K44's 2,131 cases).
>>>>>>> NEW

### EDIT parity of +-1, scope
<<<<<<< OLD
and no two-pair run of cyl:7x6 has one (B34 names; CHECKED-2).
=======
and no two-pair run of cyl:7x6 has one (B34 names; CHECKED-2). (Revised after K44, 2026-11-22: with three pairs there are +-1 roots on the odd
     widths 7, 9, 11; the statement is for one or two blocked pairs.)
>>>>>>> NEW

### EDIT over, none found, pointer
<<<<<<< OLD
   - *Over, none found.* See Conjecture 4.7: no exact over or under group (Definition 4.8) in K26's ranges, no structural over or under root against free passes in
     K15's ranges, and every over candidate of K15 (a tempo-signature search, the near-over groups) is refuted beside contexts but one placement without a context file.
=======
   - *Over, none found.* See Conjecture 4.7: no exact over or under group (Definition 4.8) in K26's ranges, no structural over or under root against free passes in
     K15's ranges, and every over candidate of K15 (a tempo-signature search, the near-over groups) is refuted beside contexts but one placement without a context file.
     (K44, 2026-11-22: the local king game LK of §8 question 3 does have roots equal to over and under on the batteries, with three blocked pairs on cyl:10x6 and wider;
     that is a D-model value of a king fight, not a group of Definition 4.8 in P. In P the over roots agree with LK "alone" (CHECKED-2), but no context was run beside them in P.)
>>>>>>> NEW

### EDIT short roots
<<<<<<< OLD
Short roots (acyclic game graphs) occur only in one-file boxes, with the kings on
     the pawn file (for example `Ka4 ka6 Pa2 pa3` is {+|} and `Ka6 ka4 Pa2 pa3` is 0); the free runs and,
     on flat:6x6, box(1) have none (CHECKED-2 on the 6x6 boards).
=======
Short roots (acyclic game graphs) occur only in one-file boxes, with the kings on
     the pawn file (for example `Ka4 ka6 Pa2 pa3` is {+|} and `Ka6 ka4 Pa2 pa3` is 0); the free runs and,
     on flat:6x6, box(1) have none (CHECKED-2 on the 6x6 boards). (Revised after K44, 2026-11-22: on cylinders cyl:6 to 10 the box(0) of two pairs
     on three files also has short roots, {|-} `Ka1 kc1 Pa2 pa3 Pc2 pc3` and {+|} `Kb5 ka1 Pa4 pa5 Pc4 pc5` (faithful), and so do three pairs on adjacent files
     (not faithful); 80 short roots in all; `kg44` and `lk` give the same count in all 687 box(0) cases (CHECKED-2 there); none in the free runs, box(1) or box(2) by `kg44` alone, COMPUTED-1.)
>>>>>>> NEW
