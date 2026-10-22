# Spec: the IEEE version of the paper (one continuous paper)

Owner: Aritro Bhattacharjee. Orchestrator: Claude. Writers: subagents. This file is the contract; when a
source disagrees with it, ask the orchestrator rather than guessing.

## Goal

One continuous, concise paper that reads easily from start to finish:
- **Format:** IEEE journal format (`\documentclass[journal]{IEEEtran}`), two columns, ready for IEEE
  Transactions on Games and for arXiv.
- **Base:** Aritro's 2025 paper (`paper/part1_2025.tex`): its rules, the basic positions, the Trebuchet, the
  puzzles and Dawson's chess. Keep his voice and his explanations, fix his errors **in place**, and continue
  straight on to the new results.
- **No seams:** no "Part 1 / Part 2" and no "2025 vs 2026" in the body. One sentence in the introduction says the
  paper extends an unpublished 2025 study.
- **No placeholders:** no TODO, VERIFY, "to appear", empty boxes or "compile on Overleaf".
- **No code listings:** one Code Availability paragraph only (see below).

## Output layout

```
paper/ieee/main.tex                 IEEEtran journal; \input{sections/...}
paper/ieee/sections/00_abstract.tex abstract (150-250 words) + IEEEkeywords
paper/ieee/sections/01_intro.tex ... 12_conclusion.tex
paper/ieee/sections/appendix_positions.tex
paper/ieee/refs.bib                 IEEEtran.bst, numbered [1], [2], ...
paper/ieee/figures -> ../figures    vector PDFs made by paper/figures/make_figures.py
```

Build with `cd paper/ieee && tectonic -X compile main.tex`. It must build with no errors, no undefined
references and no overfull boxes wider than 5pt.

## Voice (from the 2025 paper; see `paper/STYLE.md`)

- Write with "we". Explain positions move by move: "If white (Left) moves first, a2--a4 locks the a-file and
  leaves the zero game; ... Thus $G=\{0\mid 1/4\}=1/8$." Define each value the first time it is used.
- Concise and professional: short paragraphs, no repetition, no hype. Do not use "novel", "groundbreaking"
  or "comprehensive".
- Keep Aritro's own sentences where they are correct, trimmed only for length.

## Section plan (target about 12–14 pages including references)

| # | Title | Content | Main sources |
|---|---|---|---|
| — | Abstract + Index Terms | one paragraph: board, CGT, e.p.-aware test, \*2 at 7 pawns, 1/8 real-chess status, tablebases, Dawson | this spec |
| I | Introduction | cylinder chess; CGT and Elkies [Elkies96]; the \*2 question; contributions (bulleted, 6–7 items); organization | part1 intro, `archive/formal_v1/sections/01_introduction.tex` |
| II | Rules, Values and Conventions | board and moves (2025 §1, corrected knight/king wrap sentence); normal play; passed pawn = $\pm\BIG$; race rules; the e.p.-aware passed test (Def.) with the a2/b4 example; components and the cut lemma (Thm); CGT notation in one compact paragraph | part1 §1, `sections/10_fine_print.tex`, formal 02–03 |
| III | Basic Positions on the Cylinder | 2025 §2–4: 0, ±1, ±2, $\star$, $\uparrow$, Tiny 1. One figure with 4–6 small boards (subfigures) and their values; walk-throughs from part1, Position 4.2 corrected (pawns e2/e5) | part1 §2–4 |
| IV | Kings: the Trebuchet and When It Is Exact | 2025 §5; real mutual zugzwang (Lichess and kpsolve); validity conditions (V1)–(V4) theorem; loopy on/off/dud; king group 7.2 is not a zugzwang; the failure rates 159/500 | part1 §5, formal 07 |
| V | Sums, Temperature and the Puzzles Revisited | Principles 1–2 (2025 §6); puzzles 7.1–7.3 with corrected values (Table); the sum-safety theorem (HSS) and its counterexample; the two models (sum vs whole board) | part1 §6–7, sections/09 (Table 9.1), sections/10 |
| VI | Value Atlases: What Only the Cylinder Can Do | atlas scope; value classes; ±3 hottest (fig); cylinder-only values come from rings (40 three-file, 13 four-file, textbook); race-rule correction | `sections/11_every_small_position.tex`, formal 05 |
| VII | Elkies' Small Values | targets table; 1/8, ↑²\*, Tiny(1) positions with walk-throughs (moves below); reachability | formal 05 |
| VIII | The \*2 Question | candidate W a2 c2 / B b7 d7 and why it fails (e.p.); census: no \*2 with ≤6 pawns; **new: \*2 with 7 pawns** (two positions, walk-throughs, bar-chart figure); settings table | formal 06, facts below |
| IX | From the Model to Real Chess | the real-chess oracle value (Def. + sandwich lemma); the candidate's real result; the 1/8 certification status (4 decisive end positions; all 7 open sides decisive) | formal 06, formal 05 §eighth-real |
| X | Mating Without Corners: Tablebases | 4-man table + bar chart; KPK table + bar chart; rook-pawn example | formal 08 |
| XI | Dawson's Chess on the Cylinder | 2025 §8, corrected: the real rules (3×n, compulsory captures), octal 0.137, ring theorem, Grundy figure, misère quotient | part1 §8, formal 09 |
| XII | Engines and Learning | Stockfish by CGT class (table); Lc0; ChessSums; engines on sums (model ground truth, caveat); Dawson ML negative result | formal 10, facts below |
| XIII | Verification and Reproducibility | evidence labels; cross-checks; real-chess tools; AI-assisted development statement; Code Availability | formal 11 |
| XIV | Conclusion and Open Problems | 4–6 crisp open problems | formal 12, MILESTONES.md |
| — | Acknowledgment | Thomas Morley mentored the 2025 study; Lichess, Stockfish, Lc0 | |
| — | References | IEEE style | `paper/archive/formal_v1/refs.bib` |
| App. | Positions | FEN table of every position used | formal appendix |

Section titles may be shortened. Merge or cut whatever turns out repetitive.

## Figures and tables

- Make every board picture with `paper/figures/make_figures.py`. Add entries there (pieces as
  `"Pa2 pb7 Kf5 ..."`, upper case = white) and never draw boards by hand.
  - Boards are `\columnwidth` or narrower. Use `subfigure` (subcaption package) for groups.
  - Captions are IEEE style ("Fig. 3. ..."), name the position and its value, and say "(cylinder: files a and h
    adjacent)" or "(ordinary board)".
- Graphs already exist: `tb_bars`, `kpk_bars`, `star2_by_pawns`, `dawson_grundy`. Restyle them to column width
  if needed.
- Tables use booktabs, with the caption above.
- Fig. 1 may be Aritro's 2025 cover picture of the cylindrical board (`Pictures/CoverPic.png`, Wikimedia
  Commons), credited in the caption and the references.

## Evidence labels

Keep them, but compactly: one sentence in §I or §XIII defines **[P]** proved, **[C2]** checked by two independent
programs, **[C1]** computed by one program, and conjecture. Mark each theorem and headline number with one.

## Code Availability (the only place code is mentioned)

> The code and data are available at `\url{\repourl}`. The CGT engine (`cylcgt`) and most tools are in Python 3
> (standard library only). The fast solvers (`kpsolve`, the census scanner, the tablebase generators) are in C.
> Real-chess checks use the Lichess Syzygy tablebase API. The engine experiments use Stockfish 19 and Lc0. The
> learning baselines use PyTorch.

Define `\newcommand{\repourl}{https://github.com/aritroBh/cylindrical-chess-cgt}` once in main.tex. The
orchestrator will confirm the URL with the owner.

## Verified fact sheet: the only numbers you may use

Sources: `RESULTS.md`, `delegate/REVIEW.md`, `delegate/checks/*.out`. If you need a number that is not here,
read those files. If it is not there, leave the number out.

**Census and \*2**
- Flat census: widths 1–4, at most 6 pawns, 8 ranks. 231,071 records standing for 459,443 positions.
- Under the e.p.-aware test (count rule, e.p. on): 6,724 zeros, 4,042 stars, no \*k for k ≥ 2 [C2]. The C solver
  and cylcgt agree on all records. The Codex solver finds no \*k for 2 ≤ k ≤ 292 among 793,299 labelled
  placements.
- The e.p.-aware test changes at least 18,137 of the 231,071 values, and 4,070 of them in outcome (atlas/flat8/rerun/REPORT.md; the old 21,441 / 4,068 came from a raw-string comparison and is wrong).
- Textbook candidate `W a2 c2 / B b7 d7` (FEN `8/1p1p4/8/5Kp1/6Pk/8/P1P5/8`):
  - \*2 under count and mover, e.p. on or off; 0 under opponent;
  - e.p.-aware: {2±1 | −2±1} [C2].
  - Moves: a2–a4 gives \*, c2–c4 gives 2±1, a2–a3 gives {1±1|−1}, c2–c3 gives {2±1|−1}; black d7–d5 gives \*,
    b7–b5 gives −2±1.
- Real chess for the candidate: the root is N (win for the side to move). With Black to move only 1…b5 wins; with
  White to move 1.c4 wins. The oracle value ≠ \*2 and ≠ 0 under every treatment.
- Refuted second candidate: `W a3 b3 c2 / B b5 b7 c6` has positive oracle value under every treatment [C2].
- **New: \*2 with seven pawns** (count rule, e.p.-aware, e.p. on; also \*2 under count/textbook, mover/textbook and
  mover/e.p.-aware; not \*2 with e.p. off or under the opponent rule) [C2: three programs].
  - A = `W a4 b3 d2 d3 / B a7 b7 c5`.
    - White: a4–a5 → 0; d3–d4 forces c5xd4, then b3–b4 → \*.
    - Black: a7–a5 → 0; b7–b6 → \*.
    - So G = {0,\* | 0,\*} = \*2.
  - B = `W b4 c2 d2 / B a6 a7 c6 d5`.
    - White: d2–d4 → 0; c2–c3 → \*.
    - Black: d5–d4 → 0; a6–a5 forces b4xa5, then c6–c5 → \*.
    - So G = \*2.
  - Both embed legally beside the trébuchet on files f–h.
  - Count of \*2 positions by pawn number (flat, width ≤ 4, count/e.p.-aware): 4, 5, 6 pawns: 0 [C2]; 7 pawns: 2;
    8 pawns: 4. The 7- and 8-pawn counts are [C1] for completeness (T8 scanner, 5,503,282 roots); each listed
    hit was re-checked [C2].
  - On 5 files, three 8-pawn flat positions are \*2 [C2], e.g. `W a3 b3 c2 e2 / B a6 c5 d5 e3`. No \*3 or
    higher at count/e.p.-aware in any scope.
  - Real-chess status of these \*2 positions: open (11–12 men; future work).

**Elkies' targets** (flat census, count rule, e.p. on; columns textbook / e.p.-aware)
- 1/8: 13 / 9. 1/16: 3 / 2. 1/32: 1 / 0. ↑²: 5 / 2. ↑²\*: 10 / 10. tiny(1): 13 / 16. tiny(x) with x not an
  integer: 0 / 0. Each identity was checked by an independent C solver (G − T = 0) [C2].
- 1/8 at `W a2 b2 b3 / B a5 a6 b6` (FEN `8/8/pp6/p4Kp1/6Pk/1P6/PP6/8`).
  - Same value in all 9 settings and for every assignment of race outcomes [C2; Codex agrees in all 9].
  - Reachable: c2xb3, a7–a5, b7xa6, c7xb6.
  - Moves: white a2–a4 → 0 (a2–a3 → \*; b3–b4 is bad, black answers to −3); black b6–b5 → 1/4 (a5–a4 is bad).
  - So G = {0 | 1/4} = 1/8.
- ↑²\* = {0,\*|↓} at `W a2 b2 b6 / B a6 b7 c5` (FEN `8/1p6/pP6/2p2Kp1/6Pk/8/PP6/8`), all 9 settings.
  - White a2–a3 → \*, a2–a4 → 0; black a6–a5 → ↓.
- tiny(1) = {0 ‖ 0 | −1} at `W a2 b2 b6 / B a6 b7 c6` (e.p. on, every race rule).
  - White a2–a3 → 0; black a6–a5 → −1/2 ± 1/2 = {0 | −1}.
- The textbook "best reachable 1/8" `W a2 b2 d2 / B a5 c4 d7` becomes −3/2±3/2 under the e.p.-aware test. The
  best ↑², `W a3 c5 d4 / B a7 b7 d7`, becomes {3/4 | ↓\*}.

**1/8 in real chess** (oracle; `realchess/targets18`)
- All 306 end-position sides with ≤ 7 men are resolved: 283 agree with the model, 5 disagree, 2 are draws.
- Bounds with exact results only: −1/2 ≤ O ≤ 3/8 ± 1/8.
- A greedy minimal-support search leaves 4 decisive end positions (three with 9 men, `W b2 b5 / B a5 b4` with 8).
  - If they go as the model says, O = 1/8 exactly. Each of the 7 open sides is individually decisive.
  - Exact so far (kpsolve, queen promotion): `W b2 b5 / B a5 b4` with White to move, White wins, as the model
    says. The other sides are being solved.
- One 8-man decisive side disagrees with the model: Black to move in `W a3 a5 / B b4 b5`, Black wins.

**Atlas**
- 1,223,689 positions with ≤ 5 pawns on C3–C8 and F3–F8; 10,369 distinct values (textbook), 10,561 (e.p.-aware).
- 53 cylinder-only values (textbook): 40 from 3-file rings (3/4 at `W a2 b4 / B b7 c6`; 1/4±1/4 at
  `W a2 b2 / B c5 c6`), 13 from 4-file rings ({3/2±1/2 | −3/2±1/2} at `W a2 c2 / B b7 d7`, which becomes
  {2±1|−2±1} under e.p.-aware). The converse is empty.
- Race-rule dependence: 3/4 becomes 0 under mover. The 4-file values change only with e.p. off. No value is
  cylinder-only in all settings.
- Hottest without ±BIG: ±3 at `W a2 b4 / B a5 b7`; b4xa5 → 3, a5xb4 → −3.
- Value classes (≤ 5 pawns): nimbers \* (and \*2 textbook only); ups ↑, ↑\*, ⇑, ⇑\*; fractions ±1/2, ±1/4, ±3/2,
  ±5/2 on both boards; ±3/4 only on 3-file rings.
- Single file: `W a2 / B a6` = ⇑\*.

**Model rules**
- Cut lemma [P, C2].
- HSS theorem [P; tested on 1,500 random positions].
- Old sum-safety test counterexample: `W b2 d4 g3 h5 / B a7 c7 f7 g4` on C8 with e.p. off. The sum says R, the
  whole board is N [C2].
- Without condition (E): F6×6 `W a4 f4 / B b4 e5` with a black e.p. right on a3. The whole board is {0 | −4,
  −3±2} (N); the sum is {−1\* | −5\*} (R) [C1].
- Sum vs whole board: these agree on all headline values. They differ, e.g., on `W a3 b3 c2 e2 / B a6 c5 d5 e3`
  under opponent/e.p.-aware (⇑ vs \*2).

**Audit of the 2025 positions** (fix in place in §III and §V)
- Correct: 2.1, 2.2 (but a pawn on h1 is illegal), 3.1 (= 1, only via wrap-around e.p.; 2 without e.p.), 3.2 (value
  2 correct, option list not), 4.1, 4.3, 5.1 (zugzwang only because of the seam), 7.1 c-file ±1, 7.1 f-file
  {{2|1}|0} (mean 3/4).
- Fix:
  - 4.2 (the diagram is one rank off; e2/e5 gives ↑);
  - 7.1 a/h files = {+BIG | \*} (hot), not 1;
  - 7.2 pawns: an infinitesimal with mean 0, not ±1;
  - 7.2 king group: not a zugzwang in real chess (White to move draws with Kd5, Ke5 or Kf5);
  - 7.3: already decided (a5 and f7 are passed);
  - 7.3 {c,d}: tiny(1), not 1;
  - §1: a knight on h1 goes to a3 and b2 across the seam, not to a1 and a2 (those are king squares);
  - §8 Dawson: under the stated rule no first move exists.

**Kings**
- kpsolve agrees with an independent reference solver on 1,418,480 positions.
- Trébuchets are real mutual zugzwangs: the 5.1 cylinder group (Kh5 Pa4 / Kb4 Pa5) and the f/g/h group
  (Kf5 Pg4 / Kh4 Pg5), confirmed by Lichess.
- 7.2 group (Ke6 Pd7 / Kd8 Pe7): White to move draws.
- Theorem (V1)–(V4) [P, reviewed]. The local certificate with T = 1 holds in every context [P]. T ≥ 2:
  conjecture. Real trébuchets have T ≈ 5–7.
- Loopy: on, off, dud [P].
- Failure sweep on small boards: 159 of 500 components get the wrong outcome; 107 are caused by the kings, 52 by
  the pawn convention (18 through e.p., 34 because a passed pawn loses its race) [C1].

**Tablebases**
- 4-man pawnless tables, plane / cylinder / torus. 24 tables, about 607 million values; two solvers agree [C2].
  Plane maxima: KQK 10, KRK 16, KBBK 19, KBNK 33.
- Won % with White to move and the longest mate, plane / cylinder / torus:
  - KQK 100 (10) / 100 (10) / 0
  - KRK 100 (16) / 2.80 (3) / 0
  - KBBK opposite colours 99.98 (19) / 100 (14) / 0
  - KBNK 99.51 (33) / 0.0245 (2) / 0
  - KNNK 0.0107 (1) / 0.0077 (1) / 0
  - KRBK 100 (16) / 99.74 (13) / 0.0218 (1)
  - KRRK 100 (7) / 100 (8) / 100 (7)
  - KQRK 100 (6) / 100 (5) / 100 (5)
- KPK (two solvers; they agree on all 326,640 cylinder positions; 6 flat differences, all rook-underpromotion
  positions):
  - plane: White to move 124,960 / 163,328 wins (76.51%); Black to move 97,604 / 168,024 (58.09%);
  - cylinder: White to move 126,736 / 160,656 (78.89%); Black to move 92,760 / 165,984 (55.88%);
  - 16,538 flat draws become cylinder wins, including Ka6 Pa5 vs Ka8;
  - 15,930 flat wins become cylinder draws;
  - mutual zugzwangs: 216 cylinder, 160 plane.
- Do **not** cite Muller's claim until it is verified (leave it out).

**Dawson**
- Octal 0.137; period 34 with last exception 51, reproduced for n ≤ 300 [C2].
- The 2025 recurrence agrees with the true g at only 31 of the values n = 0..300. The cylinder predictions are
  wrong for 56 values of n ≤ 300.
- Ring theorem [P, machine-checked n ≤ 22]: the first player wins the 3×n cylinder iff g(n−3) = 0, i.e.
  n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, ….
- Misère: the Plambeck–Siegel quotient for strips ≤ 32 is reproduced, order 638 with 109 P-positions, and agrees
  with exhaustive search on 7.4M positions [C2]. The next quotient did not converge.
- Partizan per-board values are not additive (D5 = \* while g(5) = 3).
- ML: an LSTM reaches 0.82 test accuracy on totals 31–80 against a majority baseline of about 0.79; probes do not
  recover Grundy values [C1].

**Engines**
- Suite: 233 legal positions with ≤ 7 men. In 181 the CGT winning moves are confirmed by Lichess; in 52 CGT and
  the tablebase disagree.
- Stockfish 19 (1 thread, no tablebases) solves all 233 at 10^5 nodes (232 at 10^3).
  - Shallow-depth accuracy by class, at depth 1 / 2 / 4 / 6 / 8 / 12:
    - hot 81 / 78 / 91 / 97 / 99 / 100 (n = 68);
    - number 79 / 81 / 84 / 93 / 95 / 98 (57);
    - switch 73 / 78 / 89 / 100 / 100 / 100 (37);
    - infinitesimal 30 / 26 / 59 / 85 / 100 / 100 (27);
    - nimber 53 / 65 / 88 / 100 / 100 / 100 (17).
- Lc0 is perfect at 10^3–10^5 nodes.
- ChessSums: 418 components, 37 values, 26,000 rows; whole-board alpha–beta confirmed; it grows 4–9× per added
  component.
- Engines on sums (15–20 men, model ground truth, [C1]): on 200 positions, Stockfish picks a move in the winning
  set 26.5–28.0% of the time (10^3–10^6 nodes), Lc0 32.5–33.5%. Both drop with the number of components. The
  caveat: this is agreement with the model, not proof of real-chess error.

**Verification**
- Brute-force sum solver: 4,967,550 outcome predictions, plus 2,483,775 under e.p.-aware, on 55,195 positions.
- Whole-board minimax: 1,070 positions.
- C solver: all 231,071 census records.
- Codex solver: all headline values, all 9 settings.
- Move generator: 160/160 against Lichess.
- Proofs: drafted with AI help, 8 of 9 confirmed by a second model, one gap now stated as a conjecture; a human
  check is pending.
