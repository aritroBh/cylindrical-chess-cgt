# Diagram audit of the 2025 paper

Workstream: diagram-audit. Author: Claude (Opus 5.5) subagent, 2026-10-15.
Scratch files: `verify/diagrams/`.

**Method.** Part A was written down before I opened `cylcgt/verify_paper.py` or `notes/audit.md`.
I viewed every `prior_work/Pictures/*.png` with an image viewer, including enlarged copies of the three
puzzle diagrams (`verify/diagrams/P1_big.png`, `P2_big.png`, `P3_big.png`), and read `prior_work/main.tex`
in full. Parts B and C (comparison and solver reruns) were written afterwards.

## Part A. Independent transcription (written before reading the audit)

### A.0 Orientation and coordinates of the diagrams

All twelve board diagrams share one style (light grey and blue squares, rank numbers on the left,
file letters along the bottom).
- In every diagram a1 is a dark (blue) square and h1 is light, so the board is not flipped.
- Ranks 1 to 8 read bottom to top, and files a to h read left to right.
- Each file letter is printed toward the right edge of its own column (lichess style), not centred.
  That looks like an offset at first glance, but there are exactly 8 letters for 8 columns and "h" sits inside
  the last column. So I read no diagram as ambiguous in orientation.
- Several images have a cropped strip of piece icons along the top or bottom edge (screen-capture
  residue from the board editor). They are not on the board, and I ignored them.

No caption or sentence states a side to move for any diagram. That is expected, because a CGT value does not
depend on who moves first. The text of 7.2 analyses both sides moving first.

### A.1 Board diagrams

FEN is given with no side to move. A pawn on its own first rank (a white pawn on rank 1) is illegal in orthodox
chess, but several diagrams have one. I flag them as "rank-1 pawn".

| Pos. | File | White | Black | FEN (board part) | Paper's claim |
|---|---|---|---|---|---|
| 2.1 | ZeroGame1.png | Pe4 | Pe5 | `8/8/8/4p3/4P3/8/8/8` | 0 (both pawns stuck) |
| 2.2 | ZeroGame2.png | Pa2, **Ph1** (rank-1 pawn) | Pa3, Ph4 | `8/8/8/8/7p/p7/P7/7P` | 0 |
| 2.3 | ZeroGame3.png | Pd2, **Pc1** (rank-1 pawn) | Pd3, Pc4 | `8/8/8/8/2p5/3p4/3P4/2P5` | 0. The caption omits "a- and h-files connected", so this is the flat-board copy of 2.2 shifted by 3 files (a→d, h→c) |
| 3.1 | OneGame1.png | Pa3, **Ph1** (rank-1 pawn) | Pa4, Ph5 | `8/8/8/7p/p7/P7/8/7P` | 1 = {0 \| } |
| 3.2 | TwoGame1.png | Pa4, **Ph1** (rank-1 pawn) | Pa5, Ph6 | `8/8/7p/p7/P7/8/8/7P` | 2 = {0,1 \| } |
| 4.1 | StarGame1.png | Pe4 | Pe6 | `8/8/4p3/8/4P3/8/8/8` | \* = {0 \| 0} |
| 4.2 | UpGame1.png | **Pe3** | Pe6 | `8/8/4p3/8/8/4P3/8/8` | ↑, via "G = {0,\* \| \*}" |
| 4.3 | TinyGame1.png | Pa4, Ph2, Ph4 | Pa5, Pa6, Pa7, Ph3 | `8/p7/p7/p7/P6P/7p/7P/8` | Tiny-1 = {0 \| {0 \| −1}} |
| 5.1 | TrebuchetPosition1.png | Kh5, Pa4 | Kb4, Pa5 | `8/8/8/p6K/Pk6/8/8/8` | 0 (mutual zugzwang) |
| 7.1 | ChessPuzzle1.png | Pa4, Pa5, Pc2, Pc3, Pf3, Pf4, Ph2, Ph3 (8 pawns) | Pa7, Pc5, Pc6, Pf7, Ph6 (5 pawns) | `8/p4p2/2p4p/P1p5/P4P2/2P2P1P/2P4P/8` | G = 1 + (±1) + {{2\|1}\|0}. Components: c-file ±1; f-file {{2\|1}\|0}; {h,a} = 1 |
| 7.2 | ChessPuzzle2.png | Ke6, Pd7, Pa2, Pb2, Ph3 | Kd8, Pe7, Pa6, Pb7, Ph7 | `3k4/1p1Pp2p/p3K3/8/8/7P/PP6/8` | G = 0 ± 1. "Trebuchet" (d/e files) = 0; {a,b,h} = ±1 |
| 7.3 | ChessPuzzle3.png | Kg8, Pf7, Pa5, Pc3, Pd3, **Pa1, Pc1, Pg1, Ph1** (4 rank-1 pawns) | Kf6, Pg7, Pd6, Pd5, Pd4, Ph4, Pg3, Pc2 | `6K1/5Pp1/3p1k2/P2p4/3p3p/2PP2p1/2p5/P1P3PP` | G = 0 + 1 + 1 = 2. "Trebuchet" = 0; {c,d} = 1; {g,h,a} = 1 |

Images that are not game positions:
- `CoverPic.png` (Fig. 1) is a photograph of a physical cylindrical board with all pieces. It has no CGT claim.
- `FlatBoard.png` is not referenced in `main.tex`. It is an annular (ring) diagram of the standard initial array:
  white on the inner rings, ranks 1 to 8 going outward, files a to h around the ring. It has no CGT claim.

### A.2 Observations made while transcribing (before any solver run)

1. **4.2 (↑): the white pawn is on e3, not e2.** With W e3 / B e6 on one file, White's only move is e3–e4, giving
   W e4 / B e6. That position is \* (whoever moves to e5 freezes the file). Black's only move is e6–e5, giving W e3 / B e5,
   which is also \*. So W e3 / B e6 is {\* \| \*} = 0, not ↑. The text says White "can move to star or zero". A move to
   zero needs the double step e2–e4 from e2 to e4. The position the text describes therefore looks like W e2 / B e6, or W e2 / B e5.
   This is my hand reading. Part C checks it with the solver.
2. **7.3: the "trebuchet" is not frozen, and White has two passed pawns on the board as drawn.**
   - f8 is empty, so White's f7 pawn can promote at once (f7–f8), with check along the f-file.
   - Black's g7 pawn is not blocked (g6 is empty), so the trebuchet pawns are not immobile.
   - White's a5 pawn is already passed on the cylinder: the a-, b- and h-files hold no black pawn above rank 5.
     The paper's own text says "white's best move is just to promote its pawn on a5".
   - The pawn files are a, c, d, f, g, h; b and e are empty. So the pawn components are {c,d} and {f,g,h,a}.
     The "trebuchet" pawns f7 and g7 share the f/g files with the g/h/a group, so the decomposition
     "trebuchet + {c,d} + {g,h,a}" is not an empty-file split.
3. **7.3 text versus diagram.** The prose says "black will move to g3", but a black pawn already stands on g3.
   It also says "White will next move its pawn to h7 ... White will then move to h8", but White has no h-pawn above h1.
   These read like a5→a6→a7→a8 written with the wrong letter. The prose cannot be matched move for move to the diagram.
4. **7.2: the zugzwang is not the 5.1 trebuchet.**
   - 7.2 uses W Ke6, Pd7 / B Kd8, Pe7, a king-blocks-pawn mutual zugzwang.
     - White king moves abandon d7 (d6 and f6 are covered by e7).
     - Black's only king move is Kc7, which drops e7, because c8 and e8 are covered by d7.
   - It is a valid mutual zugzwang by my hand check, and it is central, so the seam does not matter.
     But it is a different zugzwang from Position 5.1.
   - The pawn component {a,b,h} (W a2, b2, h3 / B a6, b7, h7) is separated from the d/e pair by the empty c-, f- and g-files.
5. **5.1 on the cylinder.**
   - Four squares are adjacent to both a4 and a5: b4, b5, h4 and h5.
   - b5 and h5 are covered by the white pawn a4 (it captures towards b5 and h5). b4 and h4 are covered by the black pawn a5.
   - Each king therefore has exactly one square that guards its own pawn and attacks the enemy pawn.
     So the mutual zugzwang survives the wrap. This is a hand check only.
6. **7.1:** the files b, d, e and g are empty, so the components are {h,a}, {c} and {f}, exactly as the text says.
   No pawn is passed in the initial diagram.
7. **Rank-1 white pawns** (2.2, 2.3, 3.1, 3.2, 7.3) are illegal in orthodox chess. The values depend on the convention
   that a rank-1 pawn moves one square only. Under that convention h1–h2 then allows h2–h4, a double step later.
8. **Rules text, section 1.** "A knight on h1 can additionally move to a1 and a2" is wrong on the cylinder. The extra knight
   squares from h1 are a3 and b2; a1 and a2 are extra *king* squares. "A knight on b2 can move to h3" and "a pawn on a4 can
   capture a piece on h5" are correct.
9. **Section 8 (Dawson's chess)** has no diagram. Its prose rule (remove a pawn only if both neighbours are empty, starting
   from a full row) allows no first move, so it is not a faithful statement of Dawson's chess. It is listed for completeness.
   Positions are out of scope here.

### A.3 Positions described only in the text

| Where | Position | Claim |
|---|---|---|
| §1 | W pawn h4, B piece a5 | h4×a5 is legal on the cylinder (correct) |
| §1 | Knight b2 | can reach h3 (correct) |
| §1 | Knight h1 | "can additionally move to a1 and a2" (**wrong**: a3 and b2) |
| §1 | Pawn a4, piece h5 | a4×h5 legal (correct) |
| §2 | 2.2 with pawns moved to the c and d files | equals 2.3 (shift by 3 files) |
| §3 | −1 and −2 | colour-swap plus 180° rotation of 3.1 and 3.2 |
| §4 | ↓ | colour-swap plus rotation of 4.2 |
| §7.1 | c-file sub-game W c2,c3 / B c5,c6 | ±1 |
| §7.1 | f-file sub-game W f3,f4 / B f7 | {{2\|1}\|0} |
| §7.1 | {h,a} sub-game W a4,a5,h2,h3 / B a7,h6 | 1 |
| §7.2 | {a,b,h} sub-game W a2,b2,h3 / B a6,b7,h7 | ±1 |
| §7.3 | {c,d} sub-game W c1,c3,d3 / B c2,d4,d5,d6 | 1 |
| §7.3 | {g,h,a} sub-game W a1,a5,g1,h1 / B g3,h4 | 1 |
| §8 | Ring Dawson | Ring(n) = mex(G(n−3)), always 0 or 1 (not a chess diagram; not audited here) |

---
## Part B. Comparison with `cylcgt/verify_paper.py` CLAIMS and `notes/audit.md` (written after Part A)

Reproduce the square-by-square comparison (section 1 of the output):
`cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/rerun.py`
(about 20 s; stored output: `verify/diagrams/rerun_output.txt`).

### B.1 Pieces, squares and colours: no transcription discrepancies

Every pawn square in `CLAIMS` matches my independent reading exactly, as a set comparison done by the script.
That covers 2.1, 2.2, 3.1, 3.2, 4.1, 4.2 (as drawn), 4.3, 7.1 (total and all three sub-games), the 7.2 {a,b,h} group,
and the 7.3 pawn set with the kings removed. I found **no** wrong square, wrong piece or wrong colour. Side to move is stated
nowhere, so there is nothing to compare there.

The remaining differences are deliberate modelling choices or coverage gaps, not misreadings.

| Pos. | Difference between CLAIMS/audit and the diagram | Kind |
|---|---|---|
| 4.2 | CLAIMS adds "intended e2/e5" next to the drawn e3/e6 | deliberate reconstruction (see C.2) |
| 7.2 | CLAIMS keeps only the {a,b,h} pawns; it drops Ke6, Kd8 and the d7/e7 pawns | modelling choice (the pawn solver cannot represent the Kd8 blockade of d7) |
| 7.3 | CLAIMS drops Kg8 and Kf6 but keeps f7 and g7 | modelling choice; matches my squares |
| 2.3 | not in CLAIMS or the audit (flat-board copy of 2.2) | coverage gap; checked in C.1 |
| 5.1 | not in CLAIMS or the audit table (kings) | coverage gap; checked in C.3 |
| 7.3 sub-games | the paper's {c,d} = 1 and {g,h,a} = 1 are not computed separately | coverage gap; checked in C.4 |
| §1 text | knight on h1 "to a1 and a2" | not in the audit (text error, no value) |

### B.2 Where my reading of the diagrams disagrees with the audit's statements

1. **7.2 king group.**
   - `audit.md` says the group "is **not** a trebuchet: d7 is passed, and ...Kc7 is available".
     `RESEARCH_PLAN.md` §1.2 says the 7.2 and 7.3 king groups "are not mutual zugzwangs: both kings have spare tempo moves".
   - For 7.2 this is not what the diagram shows. Every legal king move by either side lets the enemy king take a pawn:
     - White's legal king moves are Kd5, Ke5, Kf5 and Kf7. Each allows ...Kxd7.
     - Black's only legal king move is Kc7. It allows Kxe7, and then d8=Q follows, because c8 and e8 are covered by d7.
   - Neither pawn in the group can move: d7 is blocked by Kd8 and e7 by Ke6.
   - So under the paper's convention (losing the pawn = losing) it **is** a mutual zugzwang with value 0. It is a different
     zugzwang from 5.1 (C.3).
   - The audit's literal point stands: by the pawn-only definition both d7 and e7 count as "passed". So under the paper's
     own words ("any passed pawn as an immediate win") the 7.2 diagram would be a both-sides-passed race at move 0, which is
     ill-defined. The king blockade has to be modelled explicitly.
2. **7.3 king group, a detail.** The audit lists the spare moves as "Kg8–f8/h7, Kf6–g6". Kg8–h7 (and Kg8–h8) drops f7 to
   ...Kxf7. The spare (non-losing) king moves are Kg8–f8 and Kf6–g6. On top of those, the pawn moves f7–f8 (promotion) and
   g7–g6/g5 are available. The audit's verdict ("not a zugzwang") is unchanged.
3. **7.1 {h,a} diagnosis.**
   - The audit says the paper "misses wrap captures a5×h6 and h6×a5". The paper's text does play h6×a5: "the best move for
     black ... is to capture the a-file pawn". Only h6 can capture on the a-file.
   - The value error comes from equating "White wins whether moving first or second" with the number 1.
     - The literal options are White a5–a6 → +W and Black h6×a5 → \*, so the value is {+W \| \*}.
     - White's a5×h6 exists but is not White's best move. Omitting it does not change the value.
   - The audit's computed value is correct. Only its stated reason should change.

### B.3 Orientation and coordinate ambiguity

- No diagram is ambiguous in orientation: a1 is dark in all of them, and the file letters sit inside their columns.
- Three diagrams are ambiguous in *intent*: the drawn position does not support the text's argument.
  - **4.2:** the drawn W e3 / B e6 has value 0. The text's option list {0,\* \| \*} fits W e2 / B e5 exactly (C.2).
  - **7.3 kings:** the kings look misplaced. With WK g6 and BK f8 (the 7.2 pattern reflected d→f, e→g) the group would be a clean
    mutual zugzwang (C.3). As drawn, WK g8 / BK f6 is not one. This is a conjecture about intent and cannot be checked.
  - **7.3 prose:** it cannot be matched to the diagram (A.2 item 3).

## Part C. Solver reruns on my transcription

Conventions: `cylcgt.pawns`; `Board(8,8,True,True)` (cylinder, e.p. on) and `Board(8,8,True,False)` (e.p. off), plus flat
boards where stated. The race rule is "count" unless stated; "mover" and "opponent" were also run. Unless I name a second
check, every value below is **computed once by a single implementation** (`cylcgt`).

### C.1 Every diagram, e.p. on and off (`verify/diagrams/rerun.py`, section 2)

| Pos. | e.p. on | e.p. off | Race nodes; race rule | Paper | Audit's conclusion after rerun |
|---|---|---|---|---|---|
| 2.1 | 0 | 0 | 0 | 0 | unchanged ✅ |
| 2.2 | 0 | 0 | 0 | 0 | unchanged ✅ |
| 2.3 (flat; also on the cylinder) | 0 | 0 | 0 | 0 | not in the audit; **correct** (rank-1 pawn c1) |
| 3.1 | 1 | **2** | 1; robust | 1 | unchanged (1 only with e.p.) |
| 3.2 | 2 | 2 | 1; robust | 2 | unchanged ✅ |
| 4.1 | \* | \* | 0 | \* | unchanged ✅ |
| 4.2 as drawn | **0** | **0** | 0 | ↑ | unchanged ❌ |
| 4.3 | tiny(1) | tiny(1) | 0 | tiny-1 | unchanged ✅ |
| 7.1 c-file | ±1 | ±1 | 0 | ±1 | unchanged ✅ |
| 7.1 f-file | {3/2±1/2 \| 0} = {{2\|1}\|0} | same | 0 | {{2\|1}\|0} | unchanged ✅ |
| 7.1 {h,a} | {+W \| \*} | {+W \| \*} | 1; robust | 1 | value unchanged ❌; diagnosis corrected (B.2.3) |
| 7.1 total | outcome L, mean 519/4 | same | 1; robust | 1 ± 1 + {{2\|1}\|0} | unchanged ❌ |
| 7.2 {a,b,h} | outcome **N**, value with ⇑/⇓ parts, mean 0, temp 0 | outcome **R**; value depends on the race rule | 439 robust (on); 307, value sensitive but outcome R under all three rules (off) | ±1 | unchanged ❌ |
| 7.3 all pawns | +W (a5 and f7 passed) | +W | 0 | 2 | unchanged ❌ |

Extra reproduce commands:
- Outcome classes of 7.2 under each race rule: `PYTHONPATH=. .venv/bin/python verify/diagrams/race72.py` (output `race72_output.txt`).
- The literal option lists behind 3.1 and 3.2: `PYTHONPATH=. .venv/bin/python verify/diagrams/options2.py` (`options2_output.txt`).
  - 3.1: White's only move h1–h2 goes to W a3 h2 / B a4 h5. That is 0 with e.p. and 1 without, which is why 3.1 is 1 or 2.
  - 3.2: White's only move h1–h2 goes to a position of value 1. The paper's "{0, 1 \| }" lists a move to 0 that does not
    exist, because there is no double step from h1. The value 2 is still right, since {1 \| } = 2.

### C.2 Position 4.2: which placement matches the text (`rerun.py`, section 2, "4.2 alternatives")

| Placement | Literal options | Value |
|---|---|---|
| W e3 / B e6 (as drawn) | {\* \| \*} | 0 |
| **W e2 / B e5** | **{\*, 0 \| \*}** | **↑** |
| W e2 / B e6 | {\*, 0 \| ↑} | ⇑\* |
| W e3 / B e5 | {0 \| 0} | \* |
| W e2 / B e4 | {0 \| 0} | \* |

Of the five placements tried, only W e2 / B e5 reproduces the text's "{0, \* \| \*}". This confirms the audit's reading that
the diagram is one rank too high. It also corrects my own Part A guess that W e2 / B e6 might be meant: that placement is ⇑\*.

### C.3 King groups: legal king moves on the 8×8 cylinder (`rerun.py`, section 3; `king73_alt.py`)

I wrote a small checker for this (`verify/diagrams/rerun.py`, functions `king_moves` and `capturable`).
- It uses king adjacency with file wrap and pawn attacks with file wrap.
- A king may capture only an undefended piece.

It agrees with my hand analysis in Part A, so each result below is a hand check plus one script.

| Group | White king's legal moves | Black king's legal moves | Pawn moves inside the group | Verdict |
|---|---|---|---|---|
| 5.1 (Kh5, Pa4 / Kb4, Pa5) | g4, g5, g6, h6, a6: each drops a4 | a3, b3, c3, c4, c5: each drops a5 | none | **mutual zugzwang** (h4/b5 are covered by the pawns' wrap captures) |
| 7.2 (Ke6, Pd7 / Kd8, Pe7) | d5, e5, f5, f7: each drops d7 | c7 only: drops e7 (then d8=Q) | none | **mutual zugzwang**, not the 5.1 pattern; contradicts the audit (B.2.1) |
| 7.3 as drawn (Kg8, Pf7 / Kf6, Pg7) | **f8 (safe)**; h7 and h8 drop f7 | **g6 (safe)**; e5, e6, e7, f5, g5 drop g7 | f7–f8 promotes; g7–g6/g5 | **not** a zugzwang; agrees with the audit (except Kh7, B.2.2) |
| 7.3 if WK g6, BK f8 (conjecture) | f5, g5, h5, h7: each drops f7 | e7 only: drops g7 | none | would be a mutual zugzwang |

"Drops" means the opponent's king can then capture that pawn legally. It was not checked whether the resulting king-and-pawn
endings actually win in chess. That is the same unverified assumption as the paper's "passed pawn = win".

### C.4 The paper's 7.3 sub-games, computed separately (new; not in the audit)

| Sub-game | e.p. on | e.p. off | Paper |
|---|---|---|---|
| {c,d}: W c1 c3 d3 / B c2 d4 d5 d6 | **tiny(1)** = {0 ‖ 0 \| −1} | tiny(1) | 1 |
| {g,h,a} without g7: W a1 a5 g1 h1 / B g3 h4 | +W (a5 already passed) | +W | 1 |
| The solver's own components | {c,d} and {f,g,h,a} (b and e empty) | | trebuchet + {c,d} + {g,h,a} |

The {c,d} literal options (`verify/diagrams/options.py`) are:
- White c3×d4 → 0.
- White c3–c4 → {0 \| −W\*}.
- Black d4×c3 → {0 \| −1}. After it, White d3–d4 → 0, while Black's ...d5–d4 → −1.

The paper saw that White wins either way and called the sub-game 1. It is the same tiny-one as its own Position 4.3. It is also
not 1 when moved up one rank to a legal placement (`shift.py`: tiny(1), with e.p. on and off).

**Second check** (`verify/diagrams/sumtest.py`, output `sumtest_output.txt`). An outcome-only test cannot separate tiny(1) from 1, so I
added known components on empty files and asked both `cylcgt` and the independent `crosscheck/minimax.py` for the outcome class:

| Sum | If the paper's value were right | If the solver's value is right | cylcgt | crosscheck |
|---|---|---|---|---|
| 7.3{c,d} + (−1) [W f4 / B f5 f7] | 1 − 1 = 0 → P | tiny(1) − 1 → R | R | R |
| 7.3{c,d} + \* [W f4 / B f6] | 1\* → L | tiny(1) + \* → N | N | N |
| 7.1{h,a} + (−1) [W d4 / B d5 d7] | 0 → P | {+W\|\*} − 1 → N | N | N |
| 7.1{h,a} + \* [W d4 / B d6] | 1\* → L | Right goes to \*+\* = 0 → N | N | N |

These hold with e.p. on and off. Both engines refute "= 1" for both sub-games. The exact values tiny(1) and {+W \| \*} come from
`cylcgt` alone. The sums agree with them but do not prove them.

### C.5 Robustness of the rank-1 diagrams (`verify/diagrams/shift.py`, `shift_race.py`; single implementation)

I shifted every pawn up one rank, which makes the placement legal, and recomputed. The race rule makes no difference in any case.

| Pos. | As drawn (e.p. on / off) | Shifted up one rank (e.p. on / off) |
|---|---|---|
| 2.2 | 0 / 0 | 0 / **1** |
| 2.3 | 0 / 0 | 0 / **1** |
| 3.1 | 1 / 2 | 1 / 1 |
| 3.2 | 2 / 2 | 2 / **⇑\*** |
| 7.3{c,d} | tiny(1) / tiny(1) | tiny(1) / tiny(1) |

The legal versions of 2.2, 2.3 and 3.2 keep the paper's values only with en passant. With e.p. on, the double step from rank 2
is met by an en passant capture, which is wrap-around e.p. for 2.2. This is a caveat for anyone who "repairs" the illegal
diagrams by moving them up a rank.

## Summary

- **Transcription.** I made 12 board transcriptions plus 2 non-game images. They agree with `CLAIMS` on every square, piece and
  colour. I found no orientation ambiguity.
- **The audit's value verdicts all stand** (2.1–4.3, 7.1, 7.2, 7.3) when rerun on my transcription, with e.p. on and off.
- **Where the audit should change:**
  1. The 7.2 king group *is* a mutual zugzwang under the paper's convention (hand check plus script). The statement that
     "both kings have spare tempo moves" is true of 7.3 only. The 7.2 value verdict (pawn part not ±1) is unaffected, and under
     the convention the pawn-part value becomes the whole value of 7.2.
  2. 7.3: Kg8–h7 is not a spare move. The spare moves are Kg8–f8 and Kf6–g6.
  3. 7.1 {h,a}: the paper does play h6×a5. The error is calling an L-position "1".
- **New items not in the audit:**
  - The 7.3 {c,d} sub-game is tiny(1), not 1. A second engine refutes 1 by sum tests.
  - 2.3 is correctly 0.
  - 5.1 is a valid mutual zugzwang on the cylinder.
  - §1's knight-on-h1 squares are wrong (a3/b2, not a1/a2).
  - 3.2's stated option list includes a non-existent move to 0.
  - The rank-1 diagrams keep their values when shifted to legal ranks only if e.p. is allowed.
- **Not done:** no real-chess (engine or tablebase) verification of any king group. Every "drops a pawn = loses" step relies on the
  paper's passed-pawn convention.

### Scratch files (`verify/diagrams/`)
- Enlarged diagrams: `P1_big.png`, `P2_big.png`, `P3_big.png`, `T_copy.png`.
- Scripts: `rerun.py`, `options.py`, `options2.py`, `race72.py`, `sumtest.py`, `shift.py`, `shift_race.py`, `king73_alt.py`.
- Each script has a matching `*_output.txt`.
- Run every script from the project root as `PYTHONPATH=. .venv/bin/python verify/diagrams/<script>.py`. Each finishes in under 30 s.
