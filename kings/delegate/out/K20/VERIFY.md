# K20 referee report (king-vs-king fights inside a group)

Referee: independent agent, 2026-10-27. Overall verdict: **ACCEPT WITH FIXES.** The mathematics and the headline numbers
reproduce, including the finite tempo +1 / -1 and the switches, from code I wrote myself from the definition text. Four
statements in the summary and in EDIT 1 are wrong or misleading (root counts, "dud is the majority", the "40 to 54
percent", `*` "in one-file boxes") and two sentences overclaim. Section 7 gives corrected text.

## 0. What I built (all in `verify/`, written from the definition text of summary.json and LOOPY only)

- `lk.cpp`: my own LK solver. Builds the king game LK for any board / pawn pairs / region, sums it with a battery, solves
  the sum by retrograde analysis (least fixed point, loopy), names roots by signature. It has its own battery B34 (standard
  CGT meanings; tis = {tisn|}, tisn = {|tis}), an own extended battery of 23,716 games ({A|B}, A, B subsets of size <= 2 of
  17 atoms incl. +, -, on, off, dud, tis, tisn, up, down, 1/2, over), and `EXT2`, the battery of the K20 description (64
  games {A|B}, A, B subsets of {+,-,0}, plus all 4489 {x|y} with x, y in {none, +, -, those 64}). Modes: `classify`, `root`,
  `allpairs` (exhaustive G+G' for all named root pairs of a configuration), `pred`.
- `pmini.cpp`, `pmini2.cpp`: my own P-model solver (first promotion wins, real kings, stalemate and infinite play draw; no
  e.p.: sound for every position tested, since no pawn ever stands on a file adjacent to a double-stepping pawn's file).
  `pmini` is one pawn per side, `pmini2` is any pawn set.
- `agg.py`, `cmpcfg.py`, `short.py`, `unionsig.py`, `runall.py`: drivers. Logs: `agg_all.txt`, `cmpcfg_final.txt`,
  `ext2_*.txt`, `*.mini*`, `pred.txt`.
- I did not use K20's scripts for any number below. I read `kg.cpp` only to understand why one comparison first looked
  different (it enumerates every non-terminal pawn mask as a root, see 2.1).

Machine load was above 200; the heavy-lock queue was never served to my kpsolve job (see 6), so no number below comes from
`kp`/`kp_p`.

## 1. Claim table

| # | claim | given label | verdict | my label |
|---|---|---|---|---|
| 1 | definition of LK; sortie-as-suicide = Box(m) by Lemma 1.7 | PROVED | CONFIRMED (3.1) | PROVED (one model, as in LOOPY's convention) |
| 2 | values that occur; none of +-2, +-3, +-1/2, up, down, over, under | COMPUTED-1 | CONFIRMED for the existence statements, three implementations agree. Three side statements REFUTED / need fixes (2.1) | CHECKED-2 |
| 3 | Python check, 57,324 roots, 0 mismatches | CHECKED-2 | not rerun; my third implementation agrees on every class count of every faithful configuration (2.1) | CHECKED-2 stands |
| 4 | +1, -1, {1|0}, {0|-1} exist on flat:6x6 (also 7x6, 8x6); B4553 and pair test | CHECKED-2 | CONFIRMED (3.2) | CHECKED-2 |
| 5 | parity: +-1 on cyl:6,8,10, none on 5,7,9 and none on any two-pair run of cyl:7x6 | COMPUTED-1 | CONFIRMED, for height 6 only (3.3) | CHECKED-2 for height 6; CONJECTURE for "every even width" |
| 6 | value depends on room: 0, tis, +1, +1 | COMPUTED-1 | CONFIRMED (3.4) | CHECKED-2 |
| 7 | `*` for two pairs on cylinders; also "in one-file boxes" | CHECKED-2 | cylinder part CONFIRMED; the one-file-box part concerns pawnless roots (3.5) | CHECKED-2 / reword |
| 8 | short roots only in one-file boxes | COMPUTED-1 | CONFIRMED on the 6x6 boards (3.6) | CHECKED-2 on 6x6 |
| 9 | additivity, 0 mismatches; on/off names inexact | COMPUTED-1 | CONFIRMED on a sample (exhaustive per configuration); 115,085,243 itself not rerun (3.7) | COMPUTED-1 for the number; CHECKED-2 for the statement |
| 10 | full board, P model, flat:8x6: 46/48 for file g; 39/72 file e; 31/56 files f,h | COMPUTED-1 | CONFIRMED by my own P solver, identical numbers (4.1); 3 of the 72 file-e positions are illegal | CHECKED-2 (my pmini2 and kp_p agree on all 176 positions) |
| 11 | D alone vs P: cyl:6x6 all agree; cyl:8x6 171/198; chess 254/256 | COMPUTED-1 | P parts CONFIRMED (4.2). The chess (kpsolve) part NOT_CHECKED by me | P parts CHECKED-2; chess part COMPUTED-1 as given |
| 12 | two tempi decisive, one-tempo race lead is not a reservoir | CONJECTURE | fine, but EDIT 1 states the race-lead explanation as fact (7) | CONJECTURE |

## 2. Counts and values

### 2.1 Class counts (claims 2, 3)

For every faithful configuration of every free run (cyl:6x6 16 configurations, cyl:7x6 16, cyl:8x6 16, flat:6x6 43, flat:7x6
55, flat:8x6 64) and for the boxes m = 0, 1, 2 of flat:6x6 and flat:8x6, my lk.cpp reproduces **every class count of K20's
log exactly** (dud, on, off, 0, *, +1, -1, tis, tisn, {on|off}, the decisive classes, and the total of the unclassified).
`cmpcfg_final.txt`: "configs with any difference 0" on all 12 runs. (K20's roots of a configuration are the roots of all
its non-terminal pawn masks: pawnless, single pairs, and for non-faithful configs also three-pawn masks. My comparison sums
my full-pawn-set counts over the sub-configurations, with the box of the whole configuration. The 6 non-faithful cyl:6x6
configurations differ only by this enumeration convention, they are models only, I did not chase them.)

Values that occur, in my run over the distinct roots with the full pawn set, B34: dud, on, off, 0, *, tis, tisn, {on|off},
+1, -1, {1|0}, {0|-1}, and the decisive classes. Over every free run (all six boards) none of +-2, +-3, +-1/2, up, down, up*,
down*, *2, over, under occurs (`agg_all.txt`). Distinct unclassified B34 signatures: 298 (cyl:6x6) and 486 (flat:6x6)
over all configurations, so "many hundreds" is right.

**What is wrong in the K20 text (all about the counting, none about the existence of values):**

1. **"about 2.0 million free roots" counts entries, not roots.** A root is listed once for every configuration whose
   pawn set contains its own (every one of the 22 / 67 / 82 / 97 configurations lists the pawnless king placements again, 1008 on cyl:6x6 and
   1040 on flat:6x6, and every single pair again under each two-pair configuration containing it). Distinct roots in the
   free runs: cyl:6x6 14,804, cyl:7x6 22,313, cyl:8x6 31,397, flat:6x6 47,196, flat:7x6 85,655, flat:8x6 140,566, total
   **341,931** against 1,989,996 entries (`agg_all.txt`, `agg.py`).
2. **"dud (the majority)" is false.** In K20's own table dud is 25.9 to 30.1 percent of the free entries and at most 48.8
   percent in the narrowest boxes; it is never a majority. Among distinct free roots dud is 2.6 to 10.3 percent (6.3
   percent on flat:6x6, 1040 of its 2996 are the pawnless roots). It is the largest *named* class among the entries, and
   the "loopy, not classified" class is larger. The same inflation makes the on/off counts (12,013 on flat:6x6) about 4.4 times
   too big (2,726 distinct).
3. **"40 to 54 percent ... depending on the board" holds only for the entries of the free runs and box(2)** (K20's table:
   40.4 to 54.1 percent) and drops to 26 to 31 percent in box(0) and box(1). Among distinct free roots the unclassified
   share is 45 percent (cyl:6x6), 53, 56, 52 (flat:6x6), 57, 62 percent (flat:8x6).
4. **`*` "in one-file boxes"** (claim 7). The `*` roots of the box(0) runs are pawnless, for example `Ka1 ka4` (two kings
   walking on the pawn file, no pawn on the board); every pawn-bearing root of a one-file box is not `*` (I checked
   flat:6x6, all configurations). The `*` of the narrative is therefore only the two-pair cylinder `*`.

### 2.2 Per-class checks

`lk root` on the named roots (B34 names, own code): `Kc3 ka4 Pa2 pa3 Pc4 pc5` = +1, `Ka3 kc4 Pa4 pa5 Pc2 pc3` = -1,
`Kd3 ka4 ...` = {1|0}, `Ka3 kd4 ...` = {0|-1} on flat:6x6 and flat:7x6 / 8x6 (same names); cyl:6x6 `Kb3 kf2 Pa2 pa3` = 0;
cyl:7x6 `Ke2 kf4 Pa2 pa3 Pc3 pc4` = *; cyl:8x6 `Kc2 kb4 Pa2 pa3 Pd3 pd4` = *; cyl:6x6 `Kd3 kd1 Pa2 pa3` = +1.

## 3. Individual claims

### 3.1 Claim 1 (definition, Lemma 1.7)

The sum of LK with any game is a D-game in the sense of Definition 1.1, and a king step out of R is, in the sum, an option
to the terminal of the opponent. Lemma 1.7 (deleting an option to the owner's loss changes no result; if it was the only
option the owner loses anyway) applies to every position of that D-game, so deleting all sorties gives the walled game
Box(m). Each step checks. Caveats, not errors: the equality is between two *models*; in chess a sortie can be a useful
move, so "sortie as suicide" is a convention (the report says so only implicitly). "Faithful" for two pairs at cyclic
distance >= 2 is correct: every capture leaves the other pawn of the pair passed, and no pawn attacks the other pair.

### 3.2 Claim 4 (a finite number exists)

- B34 (own code): +1 root: (L,W) with -1, (W,W) with 0, etc.; name +1.
- My 23,716-game extended battery: `Kc3 ka4 Pa2 pa3 Pc4 pc5` agrees with the integer 1 on **all 23,716**; cyl:6x6
  `Kd3 kd1 Pa2 pa3` too (`lk root ... ext`).
- `EXT2` (the nested-threat battery of the K20 description): on flat:6x6 a2,c4 +1 agrees (1 of 1) and {1|0} agrees (1 of 1)
  (`ext2_flat6_a2c4.txt`).
- Pair test, exhaustive over all named roots of the configuration (`lk allpairs`): flat:6x6 a2,c4: 73,984 ordered pairs, 0
  mismatches (box(2) 34,969, box(1) 14,884, box(0) 2,601, all 0). K20's "1.4 million pairs of that configuration" counts
  entries of the same inflated kind (the configuration lists its pawnless and single-pair roots); the statement "0
  mismatches" reproduces on every pair I can build.
- Independent P model (`pmini2`, flat:6x6): +1 root: W with either side to move; -1 root: L, L; the two switch roots fail on
  one side to move each (`Kd3 ka4 ...` with Black to move: D, not the D-value L; `Ka3 kd4 ...` with White to move: D, not W).
  This is the (V2) failure of the counterexample list.

### 3.3 Claim 5 (parity)

`lk classify cyl:Wx6 a<r> free`, ranks r = 2, 3, 4, counting +1 and -1 roots: W = 6: 1+3+3 = 7 (+1) and 3+3+1 = 7 (-1); W = 8:
2+4+5 = 11 and 5+4+2 = 11; W = 10: 4+4+5 = 13 and 5+4+4 = 13; W = 5, 7, 9: 0 for every rank. Every one of the 22
configurations of cyl:7x6 has no +-1 root (`agg_all.txt`). This is for height 6 only; "every even-width cylinder (6, 8, 10)"
in EDIT 1 should say height 6, and the parity statement for other widths and heights is a CONJECTURE.

### 3.4 Claim 6 (room)

`lk root flat:6x6 a2,c4 <m> "Kc3 ka4 ..."` for m = 0, 1, 2, free: 0, tis, +1, +1. `Kd3 ka4 ...`: illegal in box(0) (d3 outside),
unclassified in box(1), {1|0} in box(2) and free. Same as K20.

### 3.5 Claim 7 (`*`)

Reproduced as a root with pawns only on cylinders: cyl:7x6 `Ke2 kf4 Pa2 pa3 Pc3 pc4` (configurations a2 c3, a3 c4), cyl:8x6
a2 d3, a3 d4 (2 roots each), non-faithful cyl:6x6 a2 b3, a3 b4. Nothing on any flat board and nothing with one pair. See 2.1 item 4 for the box wording.

### 3.6 Claim 8 (short roots)

`lk classify` prints the number of roots whose reachable graph is acyclic. Free runs: 0 of 47,196 (flat:6x6), 0 of 14,804
(cyl:6x6). Box(1): 0 of 18,918 (flat:6x6). Box(0): 20 of 6,928 (flat:6x6) and 8 of 3,165 (cyl:6x6), all with the kings
on the pawn file of a box of that one file; the ones I looked at are `Ka4 ka6 Pa2 pa3` ({+|}) and `Ka6 ka4 Pa2 pa3` (0).

### 3.7 Claim 9 (additivity, on/off inexactness)

`lk allpairs` (every pair of named roots of the configuration, G+G' solved as a loopy product, compared with the reference
sum of the two named games): cyl:6x6 a2 104,329 pairs, cyl:6x6 a2,d2 252,004, cyl:7x6 a2,c3 199,809, flat:6x6 a2,c4 (free and
the boxes) 73,984 / 34,969 / 14,884 / 2,601; 0 mismatches. I did not rebuild the 115,085,243 (it counts the inflated
entries and goes to 4200 nodes).
On/off: with `EXT2` on cyl:6x6 a2,d2 my code finds 16 "on" and 8 "off" roots that the nested battery separates from on and
off, and on a3,d3 16 and 16: K20's log has the same numbers for these configurations, and 16+16+8 = 40 on, 8+16+16 = 40
off is its total. The roots named {+|on} and {off|-} are not exact either (all of them are separated in these two
configurations); K20 calls those classes "decisive" and does not test them, so no claim is contradicted.

## 4. Full-board and chess claims

### 4.1 Claim 10 (kpsolve P model, flat:8x6)

My own solver `pmini2` on K20's position lists (positions only; predictions from the table, which I recomputed for the g
file with my own CGT sums, `pred.txt`): file g contexts (48 positions, regenerated by me): **46 of 48 match**, 24 of 24 for
+1 and -1, the two misses are the bare switch roots `{1|0}, H0 stm b` and `{0|-1}, H0 stm w`, as claimed. Files f,h (56
positions): 31 match. File e (72 positions): 39 match. My P values equal K20's `kp_p` output on all 48 + 56 positions,
and on 69 of the 72 file-e positions; the 3 others are **illegal** positions (a context pawn attacks a king, e.g. `Kd3 ... Pe3 pe4 b`),
which K20's table counts as "MISMATCH" (kp_p prints X). So "39 of 72" is "39 of 69 legal positions". The explanation
"as the region dependence predicts" is not tested by anything in K20 or here (CONJECTURE).

### 4.2 Claim 11 (D alone against P)

`pmini` (one pawn per side) on every single-pair +1 / -1 root: cyl:6x6 28 of 28 positions agree with the D value (+1: W, -1:
L, either side to move). The 8 two-pair roots (a2 d4, a4 d2) are beyond `pmini` and are NOT_CHECKED by me. cyl:8x6: 44
positions (22 single-pair roots), **6 differ** (three +1 and three -1 positions, e.g. `Ke3 ke1 Pa2 pa3`, `Ke3 ke5 Pa2 pa3`
with D-win and P-draw: the other king catches the new passer); 3 of 22 per sign is 13.6 percent, exactly K20's 27 of 198
(the 198 are 9 copies of 22). `pmini` and `pmini2` agree.

## 5. Reproduce my numbers

```
cd kings/delegate/out/K20/verify
c++ -O2 -std=c++17 -o lk lk.cpp ; c++ -O2 -std=c++17 -o pmini2 pmini2.cpp ; c++ -O2 -std=c++17 -o pmini pmini.cpp
./lk classify flat:6x6 a2,c4 free dump=+1             # 1 root +1, 1 root {1|0}, 3 roots 0, ...
./lk root flat:6x6 a2,c4 free "Kc3 ka4 Pa2 pa3 Pc4 pc5" ext     # B34 name +1; 23,716 own games agree
EXT2=1 ./lk classify cyl:6x6 a2,d2 free ext=1         # on 12 agree / 16 disagree, off 0 / 8 (full-pawn-set roots only)
./lk allpairs flat:6x6 a2,c4 free                     # 73,984 pairs, 0 mismatches
python cmpcfg.py cyl:6x6 cyl_6x6_free.log.gz free     # all class counts of all faithful configs equal K20's (see cmpcfg_final.txt)
python agg.py flat:6x6 flat_6x6_free.log.gz free      # distinct roots by class, one board
for W in 5 6 7 8 9 10; do for r in 2 3 4; do ./lk classify cyl:${W}x6 a$r free; done; done     # +-1 counts
./lk pred flat:6x6 none free > pred.txt ; ./pmini2 flat:8x6 < far8.pos > far8.mini2            # 46 of 48 (compare with far8.key)
./pmini2 flat:8x6 < full_flat8x6.pos ; ./pmini2 flat:8x6 < full_far2_flat8x6.pos              # about 55 and 60 CPU-seconds
./pmini cyl:8x6 < alone_cyl8.pos                       # 6 of 44 differ
```
(`python` = `.venv/bin/python`.) `agg.py`, `cmpcfg.py` read K20's logs only for the configuration lists and the comparison.

## 6. Not checked

- The chess results of kpsolve (cap 1): `254 of 256` on cyl:6x6 and the flat:6x6 `bounds-differ` rows. My `kp` job (cyl:6x6 and
  flat:6x6, 44 positions) stayed in the heavy-lock queue (14 waiters, both slots held by hour-long jobs) and I withdrew
  it; the files are `kpbundle.sh`, `alone_cyl6.pos`, `flat6.pos`. Everything the P model can say is checked by my
  own solver (4.1, 4.2); the chess claim keeps the label COMPUTED-1 given by K20.
- The two-pair roots on cyl:6x6 against the P model (8 positions), cyl boxes (my box-arc convention for cylinders was not
  compared with K20's), flat:7x6 boxes (K20 has none), `ext_flat_8x6` (K20 itself says partial), the 3.9 million outcome
  comparison of the Python check (not rerun), the 115 million pairs.

## 7. EDITS.md

Both OLD blocks occur exactly once in the current LOOPY.md (checked just now, after other agents' edits had moved the
line numbers by about 80: 1 occurrence each). NEW needs the fixes below before it is applied.

**EDIT "open question 3": accept after these changes.**

1. *Search:* replace "about 2.0 million free roots" by "about 2.0 million root entries (a root is listed under every
   configuration containing its pawn set; the free runs hold 341,931 distinct roots)".
2. *Values that occur:* replace "dud (the majority: both kings can shuffle)" by "dud (both kings can shuffle; the largest
   named class among the entries, 26 to 30 percent of them, but only 3 to 10 percent of the distinct roots)". Replace
   "40 to 54 percent of all roots, depending on the board" by "41 to 54 percent of the entries of the free runs (45 to 62
   percent of the distinct roots), and 26 to 31 percent in the narrowest boxes".
3. *A finite tempo exists:* "On every even-width cylinder (6, 8, 10)" -> "On the cylinders of width 6, 8, 10 with six ranks"; and
   "Proposition 4.3 is not contradicted: the tempo is a one-tempo race lead between two kings that reply inside Z, not a
   reservoir" -> add "(interpretation, CONJECTURE: nothing computed distinguishes a race lead from other mechanisms)".
   The first half stands: Proposition 4.3 is scoped to a frozen opponent.
4. *Full-board confirmation:* "39 of 72" -> "39 of 69 legal positions (3 of the 72 are illegal: a context pawn attacks a king)";
   add "my own P-model solver reproduces all three numbers (CHECKED-2)"; delete "as the region dependence predicts" or
   mark it CONJECTURE. The chess sentence ("In chess (cap 1) ... 254 of 256") stays COMPUTED-1.
5. Add one clause to the *Model* or *Search* bullet: "Names are battery names; on, off, {+|on} and {off|-} are not exact
   (B4553 separates some of them)". (Already partly in "Not settled", which names only on and off.)
6. Optionally add: independent re-implementation (the referee's `lk.cpp`) reproduces all class counts, so the B34 part is
   CHECKED-2 on three implementations.

**EDIT "section 4 sentence on king fights": accept after one change.** "no other number: 'any value' was too strong
(COMPUTED-1)" overstates: no other number occurs *in the searched games* (at most 2 pairs, boards of at most 8 files, B34).
Replace by "...and, among the searched games (at most two pairs, boards up to 8 files, battery B34), no other number;
'any value' is not supported (COMPUTED-1)".

**Suggested third edit (not in EDITS.md):** the title of Proposition 4.3 ("no finite king tempo in isolated K+P groups") is
now misleading, since K20 found a finite king tempo in an isolated K+P group whose opponent is not frozen. The statement
and proof are correctly scoped; the title should read "(no finite king tempo from safe king steps inside F_Z against a
frozen opponent)". The status row P4.3 already has the right scope.

## 8. Summary of findings

Confirmed independently: all value-existence claims (+1, -1, {1|0}, {0|-1}, *, 0, tis, tisn, {on|off}; no +-2, +-3,
+-1/2, up, down, over, under), the class counts of all faithful configurations on six boards, the parity counts, the room
dependence, additivity on every pair I could build, the on/off inexactness, the P-model comparisons on flat:8x6 and the
cylinders. Refuted or to be fixed: the root count (341,931 distinct, not 2.0 million), "dud is the majority", "40 to 54
percent" as a statement about roots, `*` "in one-file boxes", 3 illegal positions counted in "39 of 72", and two overclaims.
Not checked: kpsolve chess results.
