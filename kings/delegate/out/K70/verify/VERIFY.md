# K73: referee of K70's case-table proof of Lemma B

Referee, 2026-11-25. Brief: `kings/delegate/briefs/K73_brief.md`. Object: `kings/delegate/out/K70/PROOF.md`.

## 0. Verdict and recommended label

- **The tables are correct.** My own checker (written from PROOF.md's prose before I opened anything in
  `K70/src/`) parses Tables B and D from PROOF.md and finds **0 failures** over all 583 rows, 7,830 positions and
  40,310 non-terminal replies, the opening rule for all 162 starts, and the entry into Table D. K70's own `check.py`
  (run on a scratch copy) gives the same counts. The independent solver r68 (K68 referee) agrees on every position:
  all 6,742 Table B positions are Black wins, and none of the 1,088 Table D positions or 716 blockade instances is a
  Black win. The 162 values are 161 Black wins and the draw at c4/Kb4.
- I checked **42 rows** by hand (36 of Table B, 6 of Table D) and every prose argument: no error in any row. There
  are two wording slips in the prose and one ambiguity in the table conventions (§3). The ambiguity has one reading
  under which the table closes, and that reading is the natural one.
- **The PROVED labels in PROOF.md are overstated.** "PROVED by descending induction" (Table B) and "PROVED by
  closure" (Table D) rest on tables that only programs have checked in full. The certificate *can* be checked on a
  board, but no one has done so, and it is about 40,000 replies long (§4).
- **Recommended label for Lemma B: CHECKED-2** (unchanged), with a note that a certificate exists that can be checked
  on a board: 583 rows, verified in full by two checkers written separately, and 42 rows plus all prose re-derived by
  hand. The middle option of the brief ("PROVED by a finite case table … checked by two separately written
  programs") describes the situation accurately, but it applies the word PROVED to a table that only programs have
  checked, and the brief's own rule forbids that. `EDITS.md` gives the new wording for Proposition 4.25.
- **The 42 needed positions do not shorten the certificate.** They reach **484 of the 486** rows of Table B (6,613 of
  the 6,742 positions; rows 165 and 417 are never reached). See `TABLE42.md`.

## 1. My checker (`src/k73_check.py`)

These are the conventions as I read them from "How the remaining winning variations are proved":

- **Rows.** Section heading = all pawns. Table B: King = Black king, Zone = White king, Black to move. Table D: King =
  White king (optional `(ep x)` = e.p. target), Zone = Black king, White to move.
- **Zones.** `x–y` is the closed rectangle; commas give a union; a leading `!` complements the whole union; `*` is
  every square. Then discard: occupied squares; squares at king distance ≤ 1 from the listed king; squares where the
  other king would be in pawn check on the listed player's turn. The listed king may be in check.
- **Play.** `Kd2`, `Kxc2`, `c5`, `cxb6` and so on, played by the side to move. The checker requires it to be legal
  under P's move rules (king steps, single and double steps, captures, e.p., check rule). My generator is my own.
- **Replies.** Every legal reply is classed: `K` for a quiet king step, `Kx<sq>` for a king capture, `<sq>` for a
  pawn step, `<f>x<sq>` for a pawn capture (e.p. included). The class must be listed. The resulting position must
  match (pieces, king, zone, e.p. state) one of the cited rows, and in Table B every cited number must be smaller.
  A promoting reply by the loser is a failure.
- **Terminals.** `end→P`: Play promotes. Table D `end→0`: after Play, Black has no pawn. Table D `end→F`: after Play
  the position is one of the blockade shapes A, B, C or last-rank (Black to move, one Black c-pawn, White without a
  pawn or with one pawn on b6 or b7). In Table B a non-terminal Play must leave White a legal move: stalemate is a
  failure; mate would be allowed, and does not occur.
- **Opening.** For each of the 162 starts and each legal White first move, the resulting position must lie in an entry
  row listed for that move class (the c2/c3/c4 table of PROOF.md). The entry row's Play must equal the move given by
  the opening rule table. c4/Kb4 → 1.c5+ is the draw case. There, Black's legal replies must enter D80 or D81.

Counts (`logs/k73_check.out`):

| | rows | positions | terminal | non-terminal replies |
|---|---:|---:|---:|---:|
| Table B | 486 | 6,742 | 643 (`end→P`) | 36,408 |
| Table D | 97 | 1,088 | 246 promote, 88 bare king, 170 blockade (159 B, 8 C, 3 A) | 3,902 |
| Starts | – | 162 | 1 draw | 1,149 White first moves |

Results: 0 failures. Every row has a non-empty zone. Every cited (class, row) pair is used by at least one position,
so no reference is dead. No Table B reply lies in two cited rows. No White double step ever gives Black an e.p. right, so
Table B needs no `(ep)` annotation. After 1.c5+ at c4/Kb4, Black has exactly Ka6, Ka7 (→ D80) and Kc7 (→ D81).
F has 716 legal instances, the same number PROOF.md gives.

Sensitivity (`logs/k73_mutations.out`): ten one-row corruptions of a scratch copy of PROOF.md all produce failures.
They are a wrong reference, a zone that is too small, a dropped Kxb7, an upward reference, an illegal Play, a wrong
opening move, a lost e.p. annotation, a blockade that is not a blockade, and B22 with c1 added to its zone, which
reaches the last-rank trap.

## 2. Solver comparison (r68)

I used `kings/delegate/out/K68/verify/src/r68.cpp`, which K68's referee wrote without seeing K70. I patched a scratch
copy (`src/k73_r68_patch.py`) only to read an e.p. field and to answer one query per line; solver, move generator
and closure are unchanged. 8,708 positions went in: every Table B and D position from my checker, the 162 starts, and
the 716 F instances. It ran in 11 s with 26 MB. Results (`logs/k73_r68_cmp.out`, raw values `logs/k73_r68_vals.out.xz`):

| set | r68 value (White's view) | claim | agree |
|---|---|---|---|
| Table B, 6,742 | L 6,742 | Black wins | yes |
| Table D, 1,088 | W 951, D 137 | not a Black win | yes |
| F instances, 716 | W 380, D 336 | not a Black win | yes |
| starts, 162 | L 161, D 1 (c4, Kb4) | 161 wins + 1 draw | yes |

The longest Black win at a start is 38 plies, or 19 Black moves, as claimed. All 42 positions of K68 VERIFY.md §5 are
among the 161 wins.

## 3. By hand

### Rows (42), each checked on a board: legality of Play, every legal reply, the cited row

| row | what was checked | verdict |
|---|---|---|
| B1 | Kd2+c2, c1 is next to d2 so empty; promotion legal | correct |
| B2 | Kb3, c1 kept empty; a1 is excluded although legal (the zone is not maximal, harmless) | correct |
| B3 | Kc4, !a1–c3 keeps c1 empty | correct |
| B4 | …c2; Kb1+ cannot take (c2 guarded); every step lands in B1 (*) | correct |
| B5 | …Kd2 from c2; from f3/a2/rank ≥ 4 all steps lie in a2–g8,a1,b1 | correct |
| B9 | Ka1: after …Kc2 only Ka2, in B5 | correct |
| B22 | …c3; b1 cannot be reached, and Kd1 goes to B19 (…Kb2, not …c2+ Kc1, the last-rank trap) | correct |
| B33 | …b1, b1 kept empty; a1 and c1 are attacked by b2 | correct |
| B37 | Kb1: …Kd3; White has Ka2 (→B34) and Kxb2 (→B31) only | correct |
| B39 | …c4 from c5; c4 guarded; a1/c1 → B29, rest → B22; Ka1 still has Kb1 | correct |
| B47 | …Kc4 v Kc2; b2 → B45, b1/c1/d1/d2 → B41 | correct |
| B48 | …Kb4; d4 excluded (pawn check); c2 → B47, b6/c6/d5/d6 → B44 | correct |
| B69 | …c5 v king on a7–c8; every step lies outside a1–c3 (B48) | correct |
| B70 | Kb7: …Kb5 leaves a7, a8, b8, c7, c8, all in B69 | correct |
| B99 | Kxb4 with the White king outside a1–d5; it cannot reach a1–c2 | correct |
| B102 | Kxb5 with the White king outside a1–d6; it cannot reach a1–c3 | correct |
| B113 | Kxc2 v king on rank ≥ 4; a3/f3/rank ≥ 4 → B5, e3 → B18 | correct |
| B117 | Kxb3; a2–a4 guard b3; b1/d1 excluded because Kc1 or Ka1 would leave B22 | correct |
| B124 | Kxc4 v Kb6/Kb7; b5 is next to c4; a5..c8 → B41, b6/c6 → B46 | correct |
| B144 | …b6; Kxb6 is legal (c5 does not guard b6) → B46 | correct |
| B146 | Kb6: …Kb4; a6 and c6 are attacked by b7, so only Ka7, Kc7 (→B145) and Kxb7 (→B42) | correct |
| B162 | …c5; Kxb7 from a7/a8/b8/c7/c8 → B48 | correct |
| B200 | …b3; cxb3 → B117 (same exclusions); king steps cannot reach a1, a3, c1 | correct |
| B211 | …b4; cxb4 gives check, …Kxb4 (B99) | correct |
| B315 | Ka7: …b5; cxb5 → B102; Ka6, Ka8, Kb8 → B260 | correct |
| B378 | …b5 (double step, no e.p.: White's pawn is on c4); cxb5 → B102 | correct |
| B414 | Kxc5 out of check; c5 unguarded off b4–d6; Kxb7 → B70 | correct |
| B415 | Kd3: …Kxc5; all steps of d3 lie in B164 | correct |
| B416 | …Kb5 v Kd4/Kd6; c5 is stuck; every step lies in B413 | correct |
| B442 | …c5 v c3, c7, d3, d7, e3–e7; destinations checked square by square in B379/396/410 | correct |
| B445 | …c5; the White king can never reach b4, d4 (attacked), d5 or d6 (all neighbours excluded or occupied) | correct |
| B447 | Kd3: …Kb4; c4–c5 → B415; king steps lie in c2–e5 | correct |
| B448 | …Kc5 v e4–e7, d7: only Kd3 (from e4) still guards c4 | correct |
| B451 | …Ka6 v Kd4/Kd6; the destination lists of the prose are exact | correct |
| B475 | …c5; Kb4 is in check: a3/b3 → B438, a4/c4 → B435; c3–c4 → B390–409 | correct |
| B486 | Kd6: …Kb5; c3 → B476, c4+ → B450, c7 → B485, the others → B482 | correct |
| D9 | Ka4 v Kb6: Kb4 gives shape A, r = 6 | correct |
| D14 | Kxc4 unguarded → bare Black king | correct |
| D57 | Kxc6: every guard square is excluded | correct |
| D61 | Ka4 in check from b5: cxb6 e.p.; Kxb6 → D9; on a7 the king is in check, so …c5 only from a6/a8 → D27 | correct |
| D80 | Ka4 v Ka6–a8; b6 → D71; b5+ → D61 (e.p.) | correct |
| D81 | Kc4 v c7/b8/c8; b8, a7, a8 → D83; c8, d7, d8 → D84; b6 → D72; b5+ → D62 | correct |

My hand checks also traced the line of PROOF.md §1, 1.Ka2 c5 2.Kb2 Kc6 3.Kb1 Kd6 4.Kc2 Ke5 5.Kd3 Kf4, …Ke4 and
…b6, through B395, B394, B389, B388, B380 and B376: each Black move is the Play of the row that the position lies in.

### Prose arguments

- **Black's first reply** (§1, two tables). Correct. A king on d5 is in check, so it must move and cannot push the
  pawn. Neither Black pawn can be taken. The entries agree with the opening rule at all 1,149 first moves (checker).
- **The c5 paragraph.** Correct in substance. *Slip 1:* "b5 and c6 were adjacent to the original Black king" — c6
  holds Black's pawn, and b6 (the Black king) is not mentioned. Repair: "b5 is next to the Black king, b6 and c6 are
  occupied, c4 was occupied before the push, and a king on d5 was in check; that leaves b4, d4 and d6." The rest
  holds: after …Kb5 the White king on d4 or d6 has no square left that guards c5 (c4 is next to b5, d5 is attacked by
  c6, c6 is guarded by b7).
- **The two detours with the pawn on c4.** Correct. From e4 the destinations are d3, e3, e5, f3, f4, f5, and only d3
  guards c4. From e5, e6, e7 and d7 none does. The destination lists from d4 and d6 are exact.
- **Kxb7 counterplay (straight pushes).** Correct. The gap of at least two ranks never shrinks. The king is on rank
  ≥ 4 while the pawn has not promoted. On ranks 4–6 it is off files a–c because every such square is next to b5.
  The step up (or along rank 8) is always legal, so there is no stalemate. The pawn's path is clear.
- **The locked c-file paragraph.** Correct (traced above).
- **B70/B69/B1 example and the entry table.** Correct.
- **The draw, Black's side.** Correct. The five squares a7, a8, b8, c8, c7 all guard b7. From c7, c8 is always free;
  from c8, c7 is free unless the White king is on b6 or d6, and then b8 is free; from b8, a8 and c8 cannot both be
  attacked. White's pawn is blocked, b7 is never loose, and c6 is guarded by b7.
- **Blockade F.** Correct in shapes A, B, C and the last rank. In A the push always checks, and c(r−1) is legal
  against every Black king step. In B a Black king that still guards the pawn is on rank r+1, so c(r−2) is legal.
  In C the push loses the pawn, b(r) or d(r) is met by opposition, and anything else by c(r−1). In the last-rank case
  …Kc3 stalemates a bare king; with b6/b7, White promotes first. The extra White pawn only takes squares from Black
  (r68: no F instance is a Black win).
- **White's side of the draw.** 1.c5+ Ka6/Ka7 2.Ka4 and 1…Kc7 2.Kc4, the 2…b5+ 3.cxb6 e.p. Kxb6 4.Kb4 example, and
  the remark on …c5 checks: correct. The closure itself is Table D (checked by program).
- **Uniqueness of 1.c5+.** Ka3, Ka4, Kb3 and Kc3 enter B445 (checker), and these are White's only other moves.

### Ambiguity in the conventions

**A1 (Table D, `end→F` beside other replies).** Six rows (D8, D29, D45, D50, D62, D72) list `end→F` *and* reply
references. The prose says only "If F applies, no further row is needed". The table closes when the rule is applied
**per position**: F where the shape holds after Play, the cited rows elsewhere (7 positions use F, 54 use the
replies). If a whole row must close in one way, the tables fail 17 times in these six rows
(`logs/k73_check_strict_mixedF.out`). Repair: add "In a row with `end→F` and other entries, F covers the positions
where it applies after Play, and the entries cover the rest." This costs a hand checker a shape test at every
position of those six rows. I count it as minor.

Not ambiguities, but worth stating for a hand checker. Zones are not maximal (B2 drops a1, which is legal). Some
zones name squares that the discard rule removes (B368's zone contains the Black king's own square a6). The `ep`
annotation never arises in Table B.

**Slip 2 (labels).** PROOF.md's summary, "PROVED by descending induction" (Table B) and "PROVED by closure"
(Table D) should say CHECKED (two checkers), with the induction scheme PROVED. REPORT.md line 3 labels a remark
about audit size "PROVED".

## 4. Can a careful reader check it without a computer? The label

- **Size.** 583 rows; 7,830 positions; 40,310 non-terminal replies, plus 889 promotions and 258 bare-king or F terminals; 162 starts with 1,149
  first moves; 716 F instances are covered by the prose lemma, not by enumeration. Each row is checkable on a board
  by the set method that the prose describes. The 42 rows above took me about 2–6 minutes each when done carefully.
  At that rate the whole table is roughly 30–50 hours of concentrated work, and errors by the checker are likely at
  that length.
- **Well-founded as written.** Yes. In Table B every cited number is smaller than its row (checker, and in all 42 rows
  checked by hand). The terminal rows promote at once, and no non-terminal row stalemates
  White. So the descending induction gives a finite Black win at every position of every row, with no repetition
  needed. Table D may cycle, which is correct for a draw. Its terminals are White promotions, bare Black kings and F,
  all non-losses for White. Black never promotes on a listed reply and is never left a mating move: every reply lands
  in a row whose Play is legal.
- **Label.** **CHECKED-2.** Two checkers, written separately and from different starting points, verify all of the
  certificate. A third program (r68) agrees with every value. The arguments around the tables are PROVED (re-derived
  by hand here). But no one has checked the table itself in full by hand. The brief's rule says that a table only
  programs have checked is CHECKED, so PROVED in any form overstates. A wording for LOOPY.md that credits the
  certificate without overstating it is in `EDITS.md`: "CHECKED-2; a certificate that can be checked on a board
  exists, but no one has checked all of it by hand". If a human checks all 583 rows, the middle label of the brief
  becomes correct.

## 5. The part Proposition 4.25 needs (`TABLE42.md`)

From the 42 positions of `kings/delegate/out/K68/verify/VERIFY.md` §5, I followed every legal White first move into
its entry row (481, 486, 475, 480, 445, 448, 451, 414) and then the table's strategy against every White reply:

- **6,613 positions** are reached, in **484 rows** of Table B. Rows 165 and 417 are never reached.
- The closure of the entry rows under all cited references (full zones) has 485 rows (only 417 is outside it).
- `TABLE42.md` lists the entry row for each of the 42 positions after each of its 8–10 legal first moves, and the 484
  rows. Each row keeps PROOF.md's zone and lists the squares of the zone that are never reached. Citations of rows
  that are never reached are dropped. Self-check: 0 replies leave the reached set.

So limiting Lemma B to the 42 positions saves almost nothing in the certificate.

## 6. Process

- **Blind: yes, as far as the files show.** No file in `K70/` refers to another folder or result: no `kings/theory`,
  no other `out/` directory, no K68 or r68. The run log (`kings/delegate/logs/K70.log`, 3,309 lines) shows 50-odd
  shell commands. All of them read or write inside `kings/delegate/out/K70/`, except one temporary copy of
  `solve.cpp` in `/private/tmp`, which was deleted at once. That copy is a small breach of "write only there". The
  forbidden paths appear only as quotations of the brief inside the prompt.
- **Files.** 2 + 10 files: PROOF.md (49 KB), REPORT.md (5 lines), and src/ with 6 .py, 2 .cpp and 2 .txt. No binaries,
  no `__pycache__`, no executable bits, no absolute home path in any text file. Intermediate files the log mentions
  (`explore.py`, `strategy.py`, `race.py`, `table-*.tmp`, `race-*.tmp`) have been removed.
- **Reproduction writes into the repository.** `check.py` and `repertoire.py` compile a shared library in a temporary
  directory under `K70/src/`, and delete it afterwards. I therefore ran `check.py` on a scratch copy outside the
  repository (`logs/k70_check_py_in_scratch_copy.out`): it prints the same counts as mine, and 716 F instances.
- **"A separate move enumerator".** check.py uses `board.py`, while the search uses `zones.py`/`reach.cpp`. They are
  separate code by the same author. My checker is the independent one.

## 7. Files and reproduction

- `src/k73_check.py`: the checker. Options: `--dump DIR`; environment `K73_PROOF=` (another copy) and
  `K73_MIXED_STRICT=1` (reading A1 strictly).
- `src/k73_table42.py`: writes `TABLE42.md`.
- `src/k73_r68_patch.py`, `src/k73_cmp.py`: the r68 comparison. The steps are in the patch script's docstring.
- `logs/`: `k73_check.out`, `k73_check_strict_mixedF.out`, `k73_mutations.out`, `k73_r68_cmp.out`,
  `k73_r68_vals.out.xz`, `k70_check_py_in_scratch_copy.out`.

```sh
.venv/bin/python -B -I kings/delegate/out/K70/verify/src/k73_check.py
.venv/bin/python -B -I kings/delegate/out/K70/verify/src/k73_table42.py > kings/delegate/out/K70/verify/TABLE42.md
```

Rules: I read nothing in `K70/src/` until the checker had run with 0 failures. Binaries were built only in a scratch
directory outside the repository and deleted afterwards. No git command was run, and no process was signalled.
