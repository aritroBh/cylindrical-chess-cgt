# L2: referee report on `lean/CylChess/Rules.lean`

Referee: an independent AI reader, 2026-11-25. I read the rules before the Lean file (blind read), and read `lean/notes/L1.md` only after my
tests. No Python file was opened. Scratch tests: `lean/scratch/L2Referee.lean`, run with
`nice -n 15 lake env lean scratch/L2Referee.lean` (no `lake build`).

**Verdict in one line:** no definition contradicts the paper. Every choice where the paper is silent is one I can defend, and every
edge case I built gives the result the paper (or N5, where only N5 speaks) requires. The file can be the trusted base once
four small changes are made (section 5). None of the four changes a published number.

## 1. The rules as I read them (blind, from §2, S6 and N5 §1)

Sources: §2 = `dist/tog/sections/02_rules.tex`, §5 = `sections/05_sums.tex`, S6 = `dist/tog/supp/s06.tex` (Rings on the Möbius
Strip, Boards of Other Heights), N5 = `dist/tog/supp_src/s15_note5.md` §1.

1. Board: n files, R ranks (8 unless stated). Flat: edge files have one neighbour. Cylinder: files wrap and ranks do not. Strip:
   files wrap with ranks reversed, "(n,r) is beside (1,9-r)" (S6).
2. Pawns only; kings are frozen outside the model. White moves up, Black down. On the strip every pawn carries a direction,
   which starts as on the flat board.
3. Step: one square ahead to an empty square. Double step: from the home rank, with both squares empty. The home rank is rank 2
   up and rank R-1 down (S6 heights). On the strip "Double step and promotion follow the direction" (S6), and N5 adds that
   "home rank, double step and distance follow d".
4. Capture: diagonally forward onto an enemy pawn, across the seam too (§2.1). On the strip the capturer lands on the
   mirrored rank and reverses its direction (S6, N5).
5. En passant: on the next move only, onto the skipped square, across the seam too (§2.1). N5 gives the exact rule: "any pawn
   whose diagonal capture square it is".
6. Normal play: a player with no move loses (§2.3).
7. Textbook passed test: no enemy pawn ahead on the pawn's own file or a neighbouring file (§2.4). On the strip the test reads
   "strictly ahead, in its own direction, ... seam neighbor ... in mirrored ranks" (S6), and N5 adds "(either direction)". A
   pawn on its last rank counts as passed (§2.3).
8. E.p.-aware test (Definition def:epaware): the textbook test holds and the pawn "cannot be captured en passant on the
   opponent's next move".
9. Three e.p. options (textbook test, e.p.-aware test, e.p. off) times three race rules make nine settings. The default is the
   count rule with the e.p.-aware test.
10. End: after a move, if exactly one side has a passed pawn, that side wins. If both have one, the position is a race, decided by
    the race rule. In the whole-board game the first passed pawn ends the game (§5).
11. Count rule: the side whose passed pawn needs fewer moves wins, "counting as on an empty board with a double step as one move";
    a tie goes to the side that did not move. Mover rule: the mover wins. Opponent rule: the other side wins.
12. Components are maximal blocks of neighbouring occupied files; on the cylinder a component is an arc or a ring (§2.5).

**Where the paper is silent or can be read two ways (my list before reading Lean):**

- A1. The cylinder or strip with 1 or 2 files. The paper uses C_3 and up, and the strip from 3 files.
- A2. A race "at the root", that is, a given position in which both sides are already passed and there is no mover.
- A3. A side with several passed pawns: the paper implies but does not state that the minimum distance counts. "As on an empty
  board" is also unclear when the side's own pawns stand on the same file (N5: only front pawns count).
- A4. Strip: can a reversed pawn that arrives on "its" home rank double-step? S6 says the double step follows the direction,
  and N5 says yes.
- A5. Strip e.p.: is the capturer required to stand beside the arrival square, as in chess, or is any pawn whose diagonal
  capture square is the skipped square allowed? Only N5 answers (the second).
- A6. Strip passed test: does an enemy pawn block whatever its direction? Only N5 answers (yes).
- A7. In a sum, what happens to an e.p. right when the reply is played in another component? §5 sidesteps it with condition
  (E); N5 keeps the flag over heap moves and clears it at the next move in the component.
- A8. Pawns on their own first rank (W rank 1, B rank R) and positions with a pawn already on its last rank. The atlas uses
  "every pawn on ranks 2-7", but the rules do not forbid them.
- A9. The strip on heights other than 8 (S6 writes 9-r). The paper uses the strip only with 8 ranks.

## 2. Verdict per definition

| Lean | Verdict | Paper sentence |
|---|---|---|
| `Color`, `Color.other` | agrees | §2.2 "white (Left) ... black (Right)" |
| `Topology`, `Board` | agrees; silent on files ≥ ? (A1) | §2.1 "Only the files wrap"; S6 "(n,r) is beside (1,9-r)" |
| `Board.onBoard`, `Board.mirror` | agrees (`ranks+1-r` generalises `9-r`, A9) | S6 |
| `Board.beside` | agrees for n ≥ 3. For n = 2 on the strip, file 1 is beside file 0 twice (straight and mirrored), which is geometrically right. For n = 1, file a is its own neighbour (A1) | §2.4 "on the cylinder, a and h are neighbors" |
| `Pawn`, `ahead`, `isAhead` | agrees | S6 "Every pawn has a direction" |
| `Board.homeRank` | agrees (R-1 for Black; on the strip it follows the direction, N5, A4) | S6 heights "black pawns on rank R-1, and the double step is allowed only from there"; S6 "Double step and promotion follow the direction" |
| `Position` | agrees, but which colour may use `ep` is left implicit (the opponent of the pawn on `ep`) | — |
| `EpRule`, `RaceRule`, `Settings`, `Settings.default`, `BIG` | agrees | §2.4 "nine settings ... default setting (count rule, e.p.-aware test)"; §2.3 "BIG=256" |
| `Board.captureTo`, `captureTargets` | agrees | §2.1 "a white pawn on h4 can capture on a5"; S6 "lands on the mirrored rank and reverses the direction" |
| `Board.epCaptures` | agrees with N5; the paper's main text says only "across the seam too" (A5) | N5 "any pawn whose diagonal capture square it is" |
| `moves` | agrees | §2.1, §2.3 "a player who has no move loses; there are no null moves" |
| `Board.blocks`, `textbookPassed` | agrees (last-rank clause holds automatically) | §2.4 textbook test; §2.3 "a pawn on its last rank counts as passed"; S6 mirrored reading; N5 "either direction" (A6) |
| `epCapturable`, `passed`, `hasPassed` | agrees | Definition def:epaware |
| `Board.distance` | agrees ("double step as one move", only where a double step exists) | §2.3 count rule |
| `isFront`, `raceDistance` | agrees with N5. On flat boards and cylinders it gives the same minimum as the main text (proof in section 4, D6). On the strip it can differ from "as on an empty board" (test T17) | §2.3; N5 "over front passed pawns", "+∞" |
| `leInf`, `raceWinner` | agrees (opponent wins when its distance ≤ mover's) | §2.3 "a tie goes to the side that did not move" |
| `Outcome`, `classify` | agrees for positions reached by a move. A2 is a silence: `classify` needs a mover even at the root | §2.3; §5 "the first passed pawn ends the game" |
| `runs`, `restrict`, `components` | agrees (arcs wrap on cylinder and strip, one ring if all files occupied) | §2.5 |
| `Position.normalize` | not in the paper (normal form); consistent with N5's "canonical" flag | N5 "the flag is stored only if such a capture exists" |
| `Position.valid` | paper silent (A1, A8). It admits W on rank 1, B on rank R, and 1-file and 2-file cylinders | atlas: "every pawn on ranks 2--7" |

## 3. Test positions (all in `lean/scratch/L2Referee.lean`; a = file 0)

Each row states what the paper says should happen, then what Lean computed. Every result matches; the comments note where only
N5 settles the expected result.

| # | Position / question | Expected (paper) | Lean |
|---|---|---|---|
| T1 | C8, W h4 / B a5: both seam captures | h4xa5 and a5xh4 legal | both present |
| T2 | C2, W a4 / B b5; passed tests with B b3 and B b6 | one capture (b is the neighbour on both sides), plus a5; passed with b3 behind, not with b6 | `[a5, axb5]` (duplicate removed); passed true / false |
| T3 | C3, W a4 / B c5 and W c4 / B a5 | a4xc5, c4xa5 across the seam | both present |
| T4 | C8, W h2 / B a4: h2-h4, then black e.p. across the seam | right recorded on h4; a4xh3 e.p. | `ep = some (7,4)`; e.p. capture present. Classification: default `won black`, textbook `race black` (after h2-h4 the black a4 is passed too, since h4 is no longer ahead of it) |
| T5 | flat, W a2 / B a3; W a2 / B a4 | no move at all; only a3 | `[]`; `[a3]` |
| T6 | right on a4 (B b4 can take); black plays g7-g6 instead; then black again | e.p. capture offered at first; the right lapses with any move | e.p. present in T6a; after g6 no right and no e.p. in T6b; a white move also clears it (T6c) |
| T7 | flat W a5 / B b5 after a4-a5 | an enemy pawn beside on the same rank is not "ahead", so both are passed: a race, W 3 vs B 4, white wins | `race white` |
| T7b | e.p. off, W a2 / B b4 | a2-a4 records no right; then both pawns are passed, race W 4 v B 3, black wins | as expected |
| T8 | W a6 / B h3, 2 v 2, under count, mover and opponent | count: the side that did not move; mover; opponent | white moved → black; black moved → white; mover rule → black; opponent rule → white |
| T9 | W a2 / B h4 | distance 5 (double step as one) v 3: black | `race black` both ways; distance a2 = 5, h7 (black) = 5, h4 = 3 |
| T10 | W a3 a4 / B h3, white race distance | front pawn a4: 4 | 4 |
| T11 | heights R = 5, 6, 7: black home 4, 5, 6; double steps; e.p. on 6 ranks; distances | home R-1; b4-b2 on R=5 with right (a2 can take b3); a3xb4 e.p. on R=6; b6-b4 on R=7 with no right; distance b6 on R=7 is 4 | all as expected |
| T12 | strip, W h5 / B a5, black takes across the seam | lands on h(9-4)=h5, now moving up; distance 3 | `⟨7,5,up⟩`, distance 3 |
| T13 | strip, W a2 / B h7 (down): a2-a4 | per N5, h7's diagonal capture square across the seam is a(9-6)=a3, so a right is recorded and h7 takes e.p., landing on a3 moving up; a4 is textbook-passed but not e.p.-aware-passed | right `(0,4)`; e.p. capture to `⟨0,3,up⟩`; default `notEnded`, textbook `won white` |
| T14 | strip, reversed W on d7 moving down; reversed B on f2 moving up | both may double-step (N5, A4) | d7-d5 and f2-f4 present |
| T15 | strip of 2 files, W a4 v B b4 and v B b5 | b is beside a straight (b5) and mirrored (b(9-5)=b4) | a4 takes b4 (lands moving down) and takes b5 (moving up) |
| T16 | C1, W a4 / B a5 | paper silent (A1) | a4 "captures" a5 straight ahead; L1 lists this as D9 |
| T17 | strip, W a3 (up) and W a6 (down) facing each other, B e6; after black's move | main text "as on an empty board": W 5 v B 5, tie, white wins; N5 front rule: neither white pawn is front, so white's distance is ∞ and black wins | `race black` (N5 reading) |
| T18 | W a4 / B h5, flat v cylinder | passed on flat; not passed on cylinder | true / false |
| T19 | W a8 / B b2 | last rank counts as passed; race 0 v 1, white wins | `race white` either mover |
| T20 | strip, W a4 v B h4 (down) and B h6 (down) | h4 is seen at rank 5 (ahead), so a4 is not passed; h6 is seen at 3 (behind), so a4 is passed | false / true |
| T21 | components: files {0,1,3,7} on C8, strip, flat; full ring on C3 | 2, 2, 3, 1 | 2, 2, 3, 1 |
| T22 | `normalize`: fake right on a5, real right on a4, real right with e.p. off | none, kept, none | none, `(0,4)`, none |
| T23 | §2.4 example W a2 b3 / B b4 | black has no move; white has a3 and a4 (with a right) | as expected |
| T24 | §3 example W a5 h2 / B a6 h7 on C8 | h7-h5 is met by a5xh6 e.p. across the seam | right `(7,5)`; e.p. capture lands on h6 |
| T25 | `valid` with W a1 / B b8 | paper silent (A8) | accepted |
| T26 | strip race, reversed black pawn h5 moving up (3) v W c6 (2), black moved | white | `race white` |

## 4. The author's list (L1.md §3), item by item

| Item | Do I agree with the choice? | Did I find it myself? |
|---|---|---|
| D1 minimax.py black home rank 7 on all heights | Yes, Lean (R-1) is right per S6 heights. This is a Python bug, not a Lean one. It should be followed up, because the heights table (S6) rests on solvers whose rules must use R-1 | No (Python not read) |
| D2 RULES.md Möbius double step by colour | Yes, Lean follows S6/N5 | Partly: A4 is the same silence; I did not see RULES.md |
| D3 strip with two files | Yes. Reading file 1 both straight and mirrored is the geometry. The strip with one file is undefined; enforce it in code (section 5) | Yes (T15) |
| D4 strip e.p. by any pawn whose diagonal square it is; blocking by either direction | Yes. It is the natural principle (e.p. undoes the double step for every pawn that could have taken the single step), and T13 shows a capturer that is not beside the arrival square. S6 in the paper should state it, since only N5 does | Yes (A5, A6, T13) |
| D5 race at the root | Yes. Requiring a mover is the honest encoding | Yes (A2) |
| D6 front passed pawns only | Yes for flat boards and cylinders, where it gives the same minimum for every position, not only reachable ones. A rear passed pawn has the same blockers or more, and if the front pawn fails only by e.p., the capturer stands beside it and is ahead of the rear pawn. **But L1's note is incomplete for the strip:** two pawns of one colour facing each other on a file are both non-front, so the side's distance is ∞ although it has passed pawns (T17). Lean matches N5, and the programs used N5, so no number changes. The paper's §2.3 sentence "as on an empty board" does not describe this case, and S6 should say "front" | Yes, including the strip case (T17), which L1 misses |
| D7 dead e.p. rights not stored | Yes; it changes no move and no test | Yes (canonical flag in N5, T22) |
| D8 distance on boards of ≤ 3 ranks | Yes | Yes (I checked the `2 ≤ d` guard) |
| D9 one-file cylinder | Agree that the paper is silent. Prefer excluding it (section 5) to keeping a "capture straight ahead" rule | Yes (T16) |
| D10 e.p. rights in the sum model | Yes. This is a matter for the S(X) layer, which must state N5's convention (flag kept over moves elsewhere, used only by the eligible colour, cleared by the next move in the component) or rely on condition (E) | Yes (A7) |
| D11 pawns on their first rank | Agree that the paper is silent. Note that such a pawn single-steps to its home rank and may then double-step, which no chess position allows (T25). Recommend `valid` exclude them on flat boards and cylinders, as the atlas does ("ranks 2-7") | Yes (A8, T25) |
| D12 mirror on other heights | Yes | Yes (A9) |
| D13 printing | No opinion (not in Rules.lean) | No |

## 5. Readability: what a human will find hard

1. `Board.beside`: `seam.map ((0, ·))` hides the three topologies. An explicit `match b.topology` in each branch would read
   like the paper.
2. `components`: the pattern `first :: middle@(_ :: _)` with `(last ++ first) :: middle.dropLast` is the hardest line in
   the file. Add a one-line comment ("merge the run ending at file n-1 with the run starting at file 0") or a lemma.
3. `moves` is one 30-line function. Splitting it into `stepMoves`, `doubleStep`, `captureMoves` and `epMoves`, each with its
   own paper quote, would let a reader check one rule at a time.
4. `Position.ep`: say in the docstring that the right belongs to the colour *not* owning the pawn on that square. Also say that
   asking `moves` for the owner's colour (a second move in the same component, as in a sum) simply clears it.
5. `raceWinner`: the inequality `leInf (opp) (mover) → opp` encodes "tie to the side that did not move". Say so in a comment
   next to the line.
6. `classify` takes `mover`, which matters only for races; document that it must be the colour that has just moved.
7. `Settings` is built anonymously as `⟨.aware, .count⟩`. Named fields (`{ ep := .aware, race := .count }`) remove the risk
   of swapping the two.
8. `Nat` subtraction: `ahead false 1 = 0` and `b.ranks - 1` rely on `onBoard` to reject rank 0. A one-line note avoids a
   reader's worry.
9. `textbookPassed`'s docstring cites the last-rank rule as if it were coded; say "holds automatically: nothing is ahead".

## 6. Final verdict

**Fit to be the trusted base, after these changes (none touches a published setting):**

1. **Board validity.** Add `Board.valid` (or document it inside Rules.lean, not only in L1.md) requiring `files ≥ 1` on flat
   boards and `files ≥ 3` on the cylinder and strip, the range the paper uses. Otherwise state in Rules.lean what C_1, C_2
   and the 2-file strip mean (T15, T16).
2. **Position validity.** On flat boards and cylinders, exclude white pawns on rank 1 and black pawns on rank R, matching the
   atlas ("ranks 2-7") and chess (T25). Otherwise every theorem quantifying over `valid` positions ranges over positions the
   paper never meant.
3. **State the N5-only rules in the file header** as choices the main text does not make: e.p. by any pawn whose diagonal
   capture square is the skipped square; blocking by enemy pawns of either direction; home rank following the direction;
   race distance over front passed pawns (with the strip case T17). These are what all the programs use, but a reader of
   §2 alone would not find them.
4. **Make the e.p. owner and the `classify` mover explicit** in the docstrings (section 5, items 4 and 6).

For the paper (not for this file): §2.3 "as on an empty board" and S6 should mention the front-pawn rule, and S6 should state
the e.p. rule of N5.
