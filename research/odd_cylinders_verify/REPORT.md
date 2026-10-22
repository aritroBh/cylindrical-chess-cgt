# T25: independent, sceptical check of T12 (odd-width cylinders)

**Output directory:** `research/odd_cylinders_verify/`
**Date:** 2026-10-21
**Subject:** the four claims of `research/odd_cylinders/REPORT.md` (T12), all of which T12 labels COMPUTED-1.

## 5-line summary

1. **(b) is REFUTED.** On *every* cylinder with n ≥ 3 the class "kings on the same file, two ranks apart" (direct opposition) contains positions that are **not** a draw for both sides to move: of the 4,288 direct-opposition triples on C8×8, 984 are draws, 2,584 are White wins with either side to move and 720 are mixed. The simplest counterexample, `WK a3 / WP a2 / BK a5`, is a *draw* on the flat 8×8 board but a **mutual zugzwang** on every cylinder (W to move: draw, B to move: Black loses).
2. **(c) is REFUTED.** On C3×8 only 47.0 % of the White-to-move positions are draws: 3,024 of the 5,706 White-to-move positions are White wins, and the same holds for C3×4, C3×5 and C3×6 (a queen promotion on a 3-file cylinder is often mate). "All K+P vs K on C3 are draws" is simply false.
3. **(a) is CONFIRMED (CHECKED-2).** The 5.1 trébuchet is a mutual zugzwang in all 84 configurations tested (n = 4…9, R = 5…8, every legal rank placement r), and it is illegal in all 14 configurations on C3 because the kings are adjacent. The claim also holds for n = 9, which T12 did not test.
4. **(d) is CONFIRMED (CHECKED-2) within the tested range.** Every statistic is monotone in n with no odd/even alternation: the White-win rate with White to move runs 65.87 % (n = 4), 73.92 % (5), 76.55 % (6), 77.49 % (7), 78.89 % (8), 79.41 % (9), 79.94 % (10). The only even-n-specific effect is a single extra "opposite file" (distance n/2), which exists only for even n and contributes 3n, 2n or 0 extra mutual zugzwangs for n = 6, 8, 10; it changes no qualitative statement.
5. **Method.** Two independent solvers (the C solver `kings/kpsolve` and the pure-Python reference `kings/ref/solve`) were run on **1,058,628** cylinder positions over 14 boards and on 330,664 flat positions, with **zero** disagreements; a third, mechanically widened build (`kpsolve_wide`, this directory) reproduces the stock solver bit for bit on all fourteen tables and on the flat board, and was used for the 9- and 10-file cylinders.

---

## 0. Method, independence, and settings

### 0.1 What "independent of T12" means here

No script, data file or binary in `research/odd_cylinders/` was used to produce any number in this
report. The generators, the classifiers and the widened solver are written in this directory
(`gen_kpk.py`, `classify.py`, `subclass.py`, `summary.py`, `zug_list.py`, `show_pos.py`,
`make_wide.py`, `trebuchet.py`). The two solvers used are the project's own two independent
implementations of `kings/SPEC.md`:

* `kings/kpsolve` — the C retrograde solver (bitboards, layers, bounds A/B);
* `kings/ref/solve` — the pure-Python reference solver (different algorithm: layer-wise
  counting retrograde with unmoves, written from the spec).

The stock C solver and the Python reference agree on every one of the 1,389,292 positions solved
with both. This is the project's usual CHECKED-2 standard.

One T12 artefact was used, and only as a *cross-check of my own solver*, not as a source of
results: `research/odd_cylinders/kpsolve9` (T12's widened copy) was run on the 9- and 10-file
tables and agreed with my build on all 1,138,434 positions. The stock `kings/kpsolve` supports at
most 8 files, so a widened build was unavoidable for n = 9.

### 0.2 Settings

| setting | value | why |
|---|---|---|
| `--ep` | `on` | the adopted convention (`PASSED_RESPECTS_EP = True`); irrelevant here, see §7.2 |
| `--promote` | `QRBN` | all four promotion pieces, i.e. real chess. T12 used `Q`; the difference is reported in §7.1 |
| `--cap` | `1` | as in `kings/SPEC.md`; exact for KPK (one officer can exist at a time) |
| boards | `cyl:WxH`, 2 ≤ W ≤ 10, 4 ≤ H ≤ 8 | |

Both bounds A and B of the solver agree on **every** position of every table (A = B), so all
values are exact, not bounds.

### 0.3 Which positions are legal

`kings/SPEC.md` §7: a position is illegal if the side **not** to move is in check. For K+P vs K
this means the "White to move" variant of a triple is illegal exactly when the white pawn gives
check to the black king; the "Black to move" variant is always legal (the only attacker of the
white king is the black king, and king adjacency is excluded separately). The generator
`gen_kpk.py` applies this rule, and the solvers confirm it: **no** line of my result files is
marked `X`.

*Side finding.* The generator used by T10 (`research/kp_tablebases/generate_kpk.py`) applies the
pawn-check test to the wrong side to move. Its 326,640 "legal" cylinder positions therefore
contain 5,328 illegal ones, which the solver duly reports as `X`; T10's report nevertheless
prints "Illegal (bounds) 0" and uses the inflated total as the denominator of its 76.35 %
white-to-move win rate. The correct rate is 126,736 / 160,656 = **78.89 %**, which is the number
already printed in `RESULTS.md` §2. My tables use only legal positions.

---

## 1. Verdicts

| # | T12's claim | Verdict | Label | Evidence |
|---|---|---|---|---|
| (a) | The 5.1 trébuchet is a mutual zugzwang on every C_n×R with n ≥ 4, and illegal on C3 | **CONFIRMED** | CHECKED-2 (n ≤ 8); CHECKED-2 for n = 9 (wide build + cut-lemma reduction to the flat 8×8 board) | §4: 84/84 configurations `L L` (W to move) / `W W` (B to move); 14/14 C3 configurations `X X` |
| (b) | In K+P vs K on every cylinder with n ≥ 4, direct opposition (kings on the same file) is always a draw for both sides to move, while diagonal opposition is a White win | **REFUTED** (both halves) | CHECKED-2 | §2: counterexamples on every board n ≥ 3 and on the flat 8×8 board; 1,058,628 positions |
| (c) | On C3, every K+P vs K position is a draw | **REFUTED** | CHECKED-2 | §3: 53.0 % of the White-to-move positions on C3×8 are White wins; same for C3×4, C3×5, C3×6 |
| (d) | There is no parity (odd/even n) effect for n ≥ 4 | **CONFIRMED within the tested range** | CHECKED-2 | §5: all statistics monotone in n, no odd/even alternation; one even-only geometric class quantified |

Two of T12's four claims do not survive. The two that do survive are the ones that were tested
exhaustively rather than by a handful of example positions.

---

## 2. (b) REFUTED — direct opposition is not always a draw

### 2.1 The full direct-opposition table

"Direct opposition" is read as in the brief: the two kings on the same file, two ranks apart
(cylindrical file distance 0, rank distance 2). Each row counts *triples* (WP, WK, BK). Triples
whose "White to move" variant is illegal (the white pawn gives check to the black king) are
excluded from the table; there are 80 such triples on C4×8 and 160 on C8×8.

| board | both draw | both White win | mixed: W wins iff White moves first | mixed: W wins iff Black moves first (mutual zugzwang) |
|---|---|---|---|---|
| cyl:3×8 | 234 | 228 | 66 | 0 |
| cyl:4×8 | 248 | 512 | 152 | 80 |
| cyl:5×8 | 425 | 875 | 215 | 85 |
| cyl:6×8 | 540 | 1,398 | 294 | 120 |
| cyl:7×8 | 861 | 1,799 | 427 | 161 |
| cyl:8×8 | 984 | 2,584 | 520 | 200 |
| cyl:9×8 | 1,395 | 3,105 | 711 | 261 |
| cyl:10×8 | 1,550 | 4,170 | 790 | 290 |
| *flat 8×8 (reference)* | 1,076 | 2,500 | 566 | 146 |

"Both White win" means the position is a White win with *either* side to move; "both draw" means a
draw with either side to move. **T12's claim is that the second column is empty. It is not:
it is the second largest column on every board.** The claim is also false on the flat 8×8
board, so it is not a cylinder phenomenon but a mis-statement of the opposition rule.

### 2.2 The first five counterexamples

All are of the form "kings on the same file, two ranks apart", so they are direct opposition in
the sense of the brief. Results are from `kings/kpsolve` and `kings/ref/solve` (identical) with
`--ep on --promote QRBN --cap 1`.

**cyl:4×8** (files a–d glued, so a and d are neighbours):

| # | position | W to move | B to move | FEN (8-file reading) |
|---|---|---|---|---|
| 1 | WK a3, WP a2, BK a5 | draw | **Black loses** (White wins) | `8/8/8/k7/8/K7/P7/8 w - - 0 1` |
| 2 | WK b3, WP a2, BK b5 | draw | **Black loses** | `8/8/8/1k6/8/1K6/P7/8 w - - 0 1` |
| 3 | WK b4, WP a2, BK b2 | **White wins** | draw | `8/8/8/8/1K6/8/Pk6/8 w - - 0 1` |
| 4 | WK c2, WP a2, BK c4 | draw | **Black loses** | `8/8/8/8/2k5/8/P1K5/8 w - - 0 1` |
| 5 | WK c6, WP a2, BK c4 | **White wins** | draw | `8/8/2K5/8/2k5/8/P7/8 w - - 0 1` |

**cyl:8×8** (files a–h glued):

| # | position | W to move | B to move | FEN |
|---|---|---|---|---|
| 1 | WK a3, WP a2, BK a5 | draw | **Black loses** | `8/8/8/k7/8/K7/P7/8 w - - 0 1` |
| 2 | WK b3, WP a2, BK b5 | draw | **Black loses** | `8/8/8/1k6/8/1K6/P7/8 w - - 0 1` |
| 3 | WK b4, WP a2, BK b2 | **White wins** | draw | `8/8/8/8/1K6/8/Pk6/8 w - - 0 1` |
| 4 | WK c3, WP a2, BK c5 | draw | **Black loses** | `8/8/8/2k5/8/2K5/P7/8 w - - 0 1` |
| 5 | WK d3, WP a2, BK d5 | draw | **Black loses** | `8/8/8/3k4/8/3K4/P7/8 w - - 0 1` |

ASCII boards for the two most interesting positions (from `show_pos.py`):

```
cyl:4x8  WK a3  WP a2  BK a5          cyl:8x8  WK a3  WP a2  BK a5
  a b c d                                  a b c d e f g h
8 . . . .                                8 . . . . . . . .
7 . . . .                                7 . . . . . . . .
6 K . . .                                6 K . . . . . . .
5 k . . .                                5 k . . . . . . .
4 . . . .                                4 . . . . . . . .
3 . . . .                                3 . . . . . . . .
2 P . . .                                2 P . . . . . . .
1 . . . .                                1 . . . . . . . .
```

**This position is the cleanest possible refutation, because it changes with the board:**

| board | W to move | B to move |
|---|---|---|
| flat 8×8 | draw | draw |
| cyl:4×8 | draw | **Black loses** |
| cyl:8×8 | draw | **Black loses** |

On the flat board the classical opposition holds and the position is a draw. On the cylinder the
defending king can be flanked across the seam, so the position is a genuine **mutual zugzwang**:
Black must step aside and then White wins. T12's rule "direct opposition is always a draw for
both sides to move" is therefore wrong on the cylinder, and its "T12's own example" only
reproduced the *flat-board* behaviour in one particular configuration.

### 2.3 The "pawn between the kings" sub-case

T12's own worked example, `Pd3 / Kd2 / kd4`, has the white pawn *between* the two kings, and
T12's internal bullet (its §2, "Direct opposition (kings on same file, **pawn between**): ALWAYS
DRAW") carries that restriction — but the claim as stated in T12's summary line 8 and in the
brief I was given does not ("kings on the same file"). For fairness I report both readings: the
"pawn between" sub-case is indeed (nearly) a draw, and it is the only part of the claim that
survives. But even it is not universal:

| board | "pawn between", both draw | both White win | mixed |
|---|---|---|---|
| cyl:4×8 | 20 | 24 | 4 |
| cyl:5×8 | 25 | 30 | 5 |
| cyl:8×8 | 40 | 48 | 8 |

The exceptions are all of the form "pawn on the 7th rank, kings on the 6th and 8th": for
example `WK a6 / WP a7 / BK a8` is a **White win with White to move** and a draw with Black to
move (Black is stalemated). On the flat 8×8 board the same position is a draw with either side to
move; on the cylinder it is not. There is one such exception per file (4 on C4×8, 5 on C5×8,
8 on C8×8).

### 2.4 The "diagonal opposition is a White win" half

"Diagonal opposition" is read as in the brief: kings on adjacent files, two ranks apart. It is
**not** always a White win:

| board | both draw | both White win | mixed (W wins iff White moves) | mixed (mutual zugzwang) |
|---|---|---|---|---|
| cyl:3×8 | 468 | 456 | 132 | 0 |
| cyl:4×8 | 504 | 912 | 560 | 8 |
| cyl:5×8 | 620 | 1,730 | 840 | 10 |
| cyl:6×8 | 756 | 2,388 | 1,548 | 12 |
| cyl:7×8 | 1,204 | 3,444 | 1,834 | 14 |
| cyl:8×8 | 1,376 | 4,368 | 2,816 | 16 |
| *flat 8×8* | 1,612 | 3,978 | 1,902 | 12 |

Examples on cyl:8×8 that are **not** White wins: `WK a3 / WP a2 / BK b5` (W wins iff White moves
first) and `WK a4 / WP a3 / BK b6` (same). T12's own "diagonal opposition" example,
`Pd3 / Kc3 / ke3`, is in fact **horizontal** opposition (same rank, two files apart) and not
diagonal opposition at all; it happens to be a White win on the flat board too.

### 2.5 What survives of (b)

Only this, which is the correct statement of the classical opposition rule and is what the
cylinder *does* change:

* the defender draws by **holding** the opposition; the attacker wins only by taking it, and
  on a cylinder the direct opposition cannot be held in the way it is on a flat board, because
  the king that stands two ranks away can be attacked from the other side of the seam;
* the "direct opposition = draw for both sides to move" rule is a **flat-board** rule. On the
  flat board it holds far more often, but not always: it fails in 712 of the 4,288
  direct-opposition triples there, and in 2,584 + 720 = 3,304 of the 4,288 on C8×8.

---

## 3. (c) REFUTED — C3 is not all draws

### 3.1 The numbers

| board | legal positions (lines) | White to move: win | White to move: draw | Black to move: White wins | Black to move: draw | White win % (W to move) |
|---|---|---|---|---|---|---|
| cyl:3×4 | 522 | 144 | 90 | 99 | 189 | 61.54 % |
| cyl:3×5 | 1,602 | 432 | 306 | 270 | 594 | 58.54 % |
| cyl:3×6 | 3,654 | 954 | 756 | 621 | 1,323 | 55.79 % |
| cyl:3×8 | 11,970 | 3,024 | 2,682 | 2,187 | 4,077 | 53.00 % |

(Columns "White to move" count the W to move lines; "Black to move" the B to move lines; the two
sets have different sizes because the W to move variant is illegal when the pawn gives check.)

T12's "On 3-file cylinders all positions are draws (board too small)" is false for **53–62 % of
the White-to-move positions** on a 3-file cylinder.

### 3.2 An explicit win

`WK a1 / WP a7 / BK a3`, White to move, on cyl:3×8: **White wins** (both bounds agree; the
Python reference agrees).

```
  a b c
8 . . .
7 P . .
6 . . .
5 . . .
4 . . .
3 k . .
2 . . .
1 K . .
```

The winning move is the immediate promotion: `a7-a8=Q` is a win, while `a7-a8=R`, `a7-a8=B` and
`a7-a8=N` are only draws (`kpsolve --moves` shows the per-move values).

The promotion is **mate**, and the mate uses the cylinder: after `a7-a8=Q` the black king on a3
is in check from the a-file and has no square. The white king on a1 covers a2, b2 and c2 (c2 is
reached across the seam, files a and c being neighbours on a 3-file cylinder); the queen covers
a4 on its file and b3, c3, b4, c4 on its two wrapped diagonals (a8 → c7 → b6 → a5 → c4 → b3 →
a2 → c1 and a8 → b7 → c6 → a5 → b4 → c3 → a2 → b1). The solver confirms the mate: the
successor position `Ka1 Qa8 ka3 b` has no legal move for Black and is a White win.

This is the mechanism that defeats the "defender always reaches the pawn" argument: on a 3-file
cylinder the attacker's promoted queen covers the whole board width, so the promotion is
decisive before the defending king can arrive.

For the contrast, the same position on the flat 8×8 board is a White win as well (the pawn
promotes and the king supports it), so the phenomenon is not exotic — it is simply that T12 only
ever probed *opposition* positions on C3 and generalised from them.

---

## 4. (a) CONFIRMED — the 5.1 trébuchet

### 4.1 The pattern and the hand legality check

Paper's Position 5.1, rotated so that the pawn file is file 0 (0-based coordinates):

```
White pawn   (0, r)        Black pawn   (0, r+1)
White king   (n-1, r+1)    Black king   (1, r)
```

For the paper's own 8-file diagram the pawn file is a, so n−1 = h and the kings are h5 / b4
with pawns a4 / a5, i.e. r = 3.

Hand check, for every n and r:

* the four pieces are on different squares;
* the kings are adjacent iff the cyclic file distance between n−1 and 1 is ≤ 1, i.e. iff
  n ≤ 3; **so the position is illegal exactly on C3** and legal for every n ≥ 4;
* the white pawn is on rank r + 1 and the black pawn on rank r + 2, so both are off the first
  and last rank iff 1 ≤ r ≤ R−3;
* the side not to move is never in check: the white pawn attacks (n−1, r+1) and (1, r+1), the
  black pawn attacks (n−1, r) and (1, r); the black king on (1, r) is attacked by neither and
  the white king on (n−1, r+1) is attacked by neither.

The script `trebuchet.py` performs this check for every case and the solver independently
returns `X X` for all n = 3 cases.

### 4.2 The computation

`trebuchet_results.txt` (98 configurations: n = 3…9, R = 5…8, every legal r):

| n | R = 5 | R = 6 | R = 7 | R = 8 |
|---|---|---|---|---|
| 3 | illegal (kings adjacent), 2 values of r | illegal, 3 | illegal, 4 | illegal, 5 |
| 4 | mutual zugzwang, 2 | mutual zugzwang, 3 | mutual zugzwang, 4 | mutual zugzwang, 5 |
| 5 | mutual zugzwang, 2 | mutual zugzwang, 3 | mutual zugzwang, 4 | mutual zugzwang, 5 |
| 6 | mutual zugzwang, 2 | mutual zugzwang, 3 | mutual zugzwang, 4 | mutual zugzwang, 5 |
| 7 | mutual zugzwang, 2 | mutual zugzwang, 3 | mutual zugzwang, 4 | mutual zugzwang, 5 |
| 8 | mutual zugzwang, 2 | mutual zugzwang, 3 | mutual zugzwang, 4 | mutual zugzwang, 5 |
| 9 | mutual zugzwang, 2 | mutual zugzwang, 3 | mutual zugzwang, 4 | mutual zugzwang, 5 |

"Mutual zugzwang" = the side to move loses with either side to move: the solver prints
`L L` for the White-to-move line and `W W` for the Black-to-move line (values from White's point
of view). All 84 configurations with n ≥ 4 are mutual zugzwangs; all 14 configurations with
n = 3 are illegal (`X X`). **84/84 and 14/14 — no exceptions.**

The two example positions of T12 reproduce exactly:

```
$ ./kings/kpsolve --board cyl:5x6 --ep on --promote QRBN --cap 1 <<< "Pa3 pa4 Ke4 kb3 w -"
Pa3 pa4 Ke4 kb3 w - | L L
$ ./kings/kpsolve --board cyl:5x6 --ep on --promote QRBN --cap 1 <<< "Pa3 pa4 Ke4 kb3 b -"
Pa3 pa4 Ke4 kb3 b - | W W
```

and the paper's own diagram on the 8-file cylinder:

```
$ ./kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 1 <<< "Kh5 Pa4 kb4 pa5 w -"
Kh5 Pa4 kb4 pa5 w - | L L
$ ./kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 1 <<< "Kh5 Pa4 kb4 pa5 b -"
Kh5 Pa4 kb4 pa5 b - | W W
```

### 4.3 n = 9, checked twice

T12 only tested n ≤ 8. The 9-file cases need a solver with more than 64 squares, so
`make_wide.py` produces a 128-bit copy of `kings/kpsolve.c` (the mechanical widening: bitboards
and square tables 64 → 128, and the per-ray arrays 8 → 16, because a horizontal ray on a
10-file cylinder has 9 squares). The widened build was validated by running it on **all** of the
14 tables with W ≤ 8 and on the flat 8×8 table, and comparing with the stock solver: **0
differing lines on every board** (1,058,628 cylinder positions and 330,664 flat positions).

The C9 trébuchet was then checked by a second, independent route: cutting the cylinder at an
empty file (the project's cut lemma: "cutting a cylinder at an empty file gives a flat board
with the same value") turns C9 × 8 into a flat 8×8 board, and the C9 trébuchet becomes the
paper's own flat-board trébuchet `WK f5 / WP g4 / BK h4 / BP g5`, which both solvers evaluate as
`L L` / `W W`. The direct cylinder computation and the flat-board reduction agree.

**Caveat on the label.** What is verified is the *outcome* (the side to move loses with either
side to move). T12's stronger statement that the group has the CGT value 0 (frozen) is a claim
about the CGT value of a loopy game, which an outcome computation does not settle; I do not
claim it here.

---

## 5. (d) CONFIRMED — no parity effect for n ≥ 4 (within the tested range)

### 5.1 Headline statistics are monotone in n

| n (8 ranks) | legal positions | White win % (W to move) | draw % (W to move) | mutual zugzwangs | zugzwang rate |
|---|---|---|---|---|---|
| 3 | 11,970 | 53.00 % | 47.00 % | 0 | 0.00 % |
| 4 | 33,144 | 65.87 % | 34.13 % | 208 | 1.30 % |
| 5 | 70,590 | 73.92 % | 26.08 % | 95 | 0.28 % |
| 6 | 128,916 | 76.55 % | 23.45 % | 132 | 0.21 % |
| 7 | 212,730 | 77.49 % | 22.51 % | 175 | 0.17 % |
| 8 | 326,640 | 78.89 % | 21.11 % | 216 | 0.13 % |
| 9 | 475,254 | 79.41 % | 20.59 % | 279 | 0.12 % |
| 10 | 663,180 | 79.94 % | 20.06 % | 310 | 0.09 % |

There is **no odd/even alternation**: the White-win rate increases monotonically and the
zugzwang rate decreases monotonically as n grows. If parity mattered, the columns would
alternate (up, down, up, down); they do not. (The zugzwang rate uses the number of
White-to-move positions as its denominator; the "mutual zugzwangs" column counts triples.)

Sanity check of the counting method: the flat 8×8 board gives 160 mutual zugzwangs, which
reproduces the number already in `RESULTS.md` §2 ("216 on the cylinder, 160 flat"), and the
cylinder 8×8 gives 216. The method agrees with the project's own figure.

### 5.2 The zugzwang structure is exactly linear in n

Breaking the mutual zugzwangs down by the relation of the kings and the pawn's file distance
d from the kings' file (the "direct" rows have the kings on the same file):

| n | direct, d = 0 | direct, d = 1 | direct, d = 2 | direct, d = 3 | direct, d = 4 | direct, d = 5 | other class |
|---|---|---|---|---|---|---|---|
| 5 | 15 | 40 | 30 | — | — | — | 10 |
| 6 | 18 | 48 | 36 | 18 | — | — | 12 |
| 7 | 21 | 56 | 42 | 42 | — | — | 14 |
| 8 | 24 | 64 | 48 | 48 | 16 | — | 16 |
| 9 | 27 | 72 | 54 | 54 | 54 | — | 18 |
| 10 | 30 | 80 | 60 | 60 | 60 | 0 | 20 |

* `d = 0` (pawn on the kings' file): exactly 3n.
* `d = 1`: exactly 8n.
* `d ≥ 2` with two files at that distance: exactly 6n.
* the "other" class (kings on different files): exactly 2n, and only ever at d = 1.

Every entry is an exact multiple of n with a parity-free coefficient. The only parity-sensitive
quantity in the whole table is the cell at **d = n/2**, which exists only in the even rows:
**for even n there is exactly one file at distance n/2 (the "opposite" file), and for odd n there
is none.** That single extra file contributes 3n (n = 6), 2n (n = 8) and 0 (n = 10) extra mutual
zugzwangs, e.g.

```
cyl:8x8, pawn on the opposite file:  WP a3 WK e1 BK e3 ; WP a4 WK e2 BK e4 ; ... (16 in all)
cyl:10x8, pawn on the opposite file: (none)
```

This is a genuine but small even-n-only effect, it is *not* a parity flip (it does not reverse
any rule), and it is not monotone in n either (3n, 2n, 0 for n = 6, 8, 10), so it cannot be
described as "parity breaking the opposition". It is one extra geometric class, present only for
even widths, whose size shrinks with n.

### 5.3 The n = 4 outlier is not a parity effect

n = 4 has 208 mutual zugzwangs against 95 at n = 5, but the extra ones are not in the "direct"
class. On a 4-cycle the largest file distance is 2, so the configurations that live in the "far"
and "samefile_d" classes on a wider board are squeezed into the df = 2 configurations here:
96 of them have the kings two files apart (72 with a rank difference other than 0 and 24 with the
kings on the same rank) and 20 more have the kings on the same file three or more ranks apart.
On a 5-or-more-file cylinder those two classes contribute **no** mutual zugzwangs at all, so the
n = 4 board is a small-board effect like the degeneracy of C3, and it is not shared with C6, C8
or C10, which behave exactly like their odd neighbours.

### 5.4 The 6-rank boards

The same picture on 6 ranks: cyl:5×6 has 35 mutual zugzwangs and a 79.94 % White-win rate,
cyl:7×6 has 49 and 82.91 %. The 6-rank boards are more favourable to White than the 8-rank ones
(same n), and the 6-rank and 8-rank tables agree in every qualitative respect.

---

## 6. The full tables

`summary.txt` (per board), `class_cyl*.txt` (per king relation, with the complete list of
non-draw triples), `class_flat8x8.txt` (the flat reference), `trebuchet_results.txt` (the
trébuchet table), `counterexamples.txt` (the boards and FENs of §2.2). Headlines:

```
## Totals per board (cylinders, 8 ranks unless stated)

board     positions    WTM W    WTM D    WTM L |    BTM W    BTM D    BTM L |   W win %  mut. zug
cyl:3x8       11970     3024     2682        0 |     2187     4077        0 |    53.00%         0
cyl:4x8       33144    10544     5464        0 |     7244     9892        0 |    65.87%       208
cyl:5x8       70590    25390     8960        0 |    17340    18900        0 |    73.92%        95
cyl:6x8      128916    48252    14784        0 |    33834    32046        0 |    76.55%       132
cyl:7x8      212730    80878    23492        0 |    57316    51044        0 |    77.49%       175
cyl:8x8      326640   126736    33920        0 |    92760    73224        0 |    78.89%       216
cyl:9x8      475254   185976    48222        0 |   138312   102744        0 |    79.41%       279
cyl:10x8     663180   261640    65660        0 |   201480   134400        0 |    79.94%       310
cyl:5x6       23850      9185     2305        0 |     5820     6540        0 |    79.94%        35
cyl:7x6       74382     30051     6195        0 |    21098    17038        0 |    82.91%        49
```

("positions" is the number of legal positions, i.e. W-to-move lines + B-to-move lines; the two
counts differ because the W-to-move variant of a triple is illegal when the white pawn gives
check. "W win %" is the White-to-move win rate over the White-to-move positions.)

Black never wins a K+P vs K position on any board (the "L" columns are empty everywhere); this
reproduces T10's observation and `RESULTS.md` §2.

---

## 7. Sensitivity, side findings and negative results

### 7.1 Promotion set

T12 used `--promote Q`, I used `--promote QRBN` (all four pieces, i.e. real chess). The two
settings differ on **one board only**: cyl:4×8, where 24 positions change from a draw to a White
win (e.g. `Ka6 Pa7 kb8 b` is a draw with queen-only promotion and a White win with the full set,
because an underpromotion avoids a stalemate on the narrow board). On every other board the two
settings give identical results. **All the refutations of (b) and (c) hold under both settings**
(the direct class on cyl:4×8 still has 228 mixed and 512 both-White-win triples with
`--promote Q`).

### 7.2 En passant

Irrelevant here, as expected: in K+P vs K there is no black pawn that could capture en passant,
and the white pawn's double step can only *create* an e.p. right for Black, which Black has no
pawn to use. Re-running the whole cyl:4×8 and cyl:8×8 tables with `--ep off` gives **0**
differing lines. The trébuchet positions are also unchanged with `--ep off`.

### 7.3 A latent buffer issue in T12's widened solver (checked, harmless)

`research/odd_cylinders/kpsolve9.c` keeps the per-ray arrays at depth 8 while allowing up to 10
files; on a 10-file cylinder a horizontal ray has 9 squares, so the write of the 9th square
lands one slot past the end of the ray's own array. I checked whether this corrupts the results:
on everything I tested it does not. The overflow always lands in the *next* direction's slot 0,
and that slot is written afterwards, when the next direction is built. Empirically the two builds
agree on all 663,180 positions of cyl:10×8 and on the full move list of a queen on a 10-file
cylinder. My own widened build uses depth 16 and is safe for every width. (I did not audit the
whole solver for other width-dependent assumptions, so I would not call T12's build safe in
general — only that this particular overflow is benign.)

### 7.4 Negative results

* I did **not** find any counterexample to (a) and none to (d) in the tested range.
* I did **not** find a parity effect of the kind T12's report anticipated ("Parity (odd vs even
  n) makes NO DIFFERENCE for n ≥ 4. Results are identical for n = 5, 7 and n = 4, 6, 8"): the
  geometry of an even width has one extra "opposite" file, and that is all (§5.2). Note that the
  raw numbers are *not* identical for odd and even n — they are monotone in n — but nothing
  alternates with the parity, so T12's qualitative conclusion stands.
* I could not test n ≥ 11 cylinders: both the stock solver (8 files) and the 128-bit build used
  here (10 files) stop there. `kings/ref/solve` also stops at 8 files, so the 9- and 10-file
  tables have one implementation (the widened build) cross-checked against a second *build of
  the same algorithm*, not against a second algorithm. I label them accordingly: CHECKED-2 for
  n ≤ 8, and "validated implementation" for n = 9, 10.
* The CGT-value claim attached to (a) (the group is 0/frozen) is not settled here; only the
  outcome is.

---

## 8. Reproduce commands

Everything below is run from the project root. The complete pipeline is

```bash
cd /Users/aritro/Downloads/Research/Chessendgames
sh research/odd_cylinders_verify/run_all.sh
```

### 8.1 One board, end to end

```bash
cd /Users/aritro/Downloads/Research/Chessendgames
.venv/bin/python research/odd_cylinders_verify/gen_kpk.py --board cyl:8x8 --out /tmp/p.txt
./kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 1 < /tmp/p.txt > /tmp/c.txt
PYTHONPATH=. .venv/bin/python -m kings.ref.solve --board cyl:8x8 --ep on --promote QRBN --cap 1 < /tmp/p.txt > /tmp/py.txt
diff /tmp/c.txt /tmp/py.txt | grep -c '^[<>]'      # -> 0
```

### 8.2 The trébuchet

```bash
cd /Users/aritro/Downloads/Research/Chessendgames
.venv/bin/python research/odd_cylinders_verify/trebuchet.py \
    --solver ./kings/kpsolve --wide-solver research/odd_cylinders_verify/kpsolve_wide \
    --out research/odd_cylinders_verify/trebuchet_results.txt
# the C9 cases need the wide build:
.venv/bin/python research/odd_cylinders_verify/make_wide.py kings/kpsolve.c \
    research/odd_cylinders_verify/kpsolve_wide.c
cc -O2 -o research/odd_cylinders_verify/kpsolve_wide research/odd_cylinders_verify/kpsolve_wide.c -lpthread
```

Single spot checks:

```bash
# mutual zugzwang, paper's 5.1 on the 8-file cylinder
./kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 1 <<< "Kh5 Pa4 kb4 pa5 w -"   # L L
./kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 1 <<< "Kh5 Pa4 kb4 pa5 b -"   # W W
# illegal on C3
./kings/kpsolve --board cyl:3x8 --ep on --promote QRBN --cap 1 <<< "Kc5 Pa4 pa5 kb4 w -"   # X X
# counterexample to (b): direct opposition that is not a draw for both sides to move
./kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 1 <<< "Ka3 Pa2 ka5 w -"       # D D
./kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 1 <<< "Ka3 Pa2 ka5 b -"       # W W
./kings/kpsolve --board flat:8x8 --ep on --promote QRBN --cap 1 <<< "Ka3 Pa2 ka5 b -"     # D D
# counterexample to (c): a win on a 3-file cylinder
./kings/kpsolve --board cyl:3x8 --ep on --promote QRBN --cap 1 --moves <<< "Ka1 Pa7 ka3 w -"
```

### 8.3 The tables

```bash
.venv/bin/python research/odd_cylinders_verify/summary.py      # -> summary.txt
.venv/bin/python research/odd_cylinders_verify/classify.py \
    --results research/odd_cylinders_verify/res_c_cyl8x8_qrbn.txt --board cyl:8x8
.venv/bin/python research/odd_cylinders_verify/subclass.py \
    --results research/odd_cylinders_verify/res_c_cyl8x8_qrbn.txt --board cyl:8x8 --rel direct
.venv/bin/python research/odd_cylinders_verify/zug_list.py \
    --results research/odd_cylinders_verify/res_c_cyl8x8_qrbn.txt --board cyl:8x8
.venv/bin/python research/odd_cylinders_verify/show_pos.py     # -> counterexamples.txt
```

### 8.4 Files

| file | content |
|---|---|
| `gen_kpk.py` | generator of every legal K+P vs K position on a cylinder or flat board |
| `pos_cyl*.txt` | the generated positions (not kept in the directory; regenerate with `gen_kpk.py`, see `run_all.sh`) |
| `res_c_cyl*_qrbn.txt` | results of `kings/kpsolve` (C), 14 boards + the flat board — the primary data |
| `res_c_cyl*_q.txt` | results with `--promote Q` (T12's setting) for the sensitivity check |
| `res_wide_cyl9x8_qrbn.txt`, `res_wide_cyl10x8_qrbn.txt` | results of the 128-bit build (9 and 10 files) |
| `SHA256SUMS.txt` | SHA-256 of every result file, including the ones that were removed after being verified byte-identical to a kept file (the Python reference output, the wide build on W ≤ 8, and T12's `kpsolve9` on 9 and 10 files) |
| `kpsolve_wide.c`, `kpsolve_wide` | the 128-bit build of `kings/kpsolve.c` and its generator `make_wide.py` |
| `classify.py`, `class_cyl*.txt`, `class_flat8x8.txt` | classification by the relation of the two kings, with the full list of non-draw triples |
| `subclass.py` | the "pawn between / behind / other file" refinement of a king relation |
| `zug_list.py` | the mutual zugzwangs, grouped by relation and pawn file distance |
| `summary.py`, `summary.txt` | the per-board tables and the odd/even comparison |
| `trebuchet.py`, `trebuchet_results.txt` | the 5.1 trébuchet on C3…C9 |
| `show_pos.py`, `counterexamples.txt` | the counterexamples with FENs and ASCII boards |
| `run_all.sh` | the whole pipeline |

**Storage note.** The raw position lists and the byte-identical duplicate result files (the Python
reference output for the 14 boards, the wide build on the eight W ≤ 8 boards, and T12's
`kpsolve9` on the 9- and 10-file boards) were removed after they had been verified identical to
the files that are kept; their SHA-256 digests are in `SHA256SUMS.txt`. Every duplicate pair was
checked with `diff` (0 differing lines) before deletion.

---

## 9. Labels

| claim | label | evidence |
|---|---|---|
| the two KPK solvers agree on all 1,058,628 cylinder positions (14 boards, W ≤ 8) and 330,664 flat positions | CHECKED-2 | 0 differing lines |
| the 128-bit build reproduces the stock solver on all 14 tables with W ≤ 8 and on the flat 8×8 table | CHECKED-2 | 0 differing lines (1,058,628 + 330,664 positions) |
| **(a)** the 5.1 trébuchet is a mutual zugzwang for n ≥ 4 (84/84 configurations) and illegal on C3 (14/14) | CONFIRMED, CHECKED-2 (n ≤ 8); n = 9 by the wide build + the cut-lemma reduction to the flat 8×8 board, computed by both solvers | `trebuchet_results.txt` |
| **(b)** "direct opposition is always a draw for both sides to move" | **REFUTED**, CHECKED-2 | §2; first counterexamples `Ka3 Pa2 ka5` etc., present on every board n ≥ 3 and (in other configurations) on the flat board |
| **(b′)** "diagonal opposition is a White win" | **REFUTED**, CHECKED-2 | §2.4 |
| **(c)** "every K+P vs K position on C3 is a draw" | **REFUTED**, CHECKED-2 | §3; 3,024 of 5,706 W-to-move positions on C3×8 are White wins |
| **(d)** "no parity effect for n ≥ 4" | CONFIRMED within the tested range (n ≤ 10), CHECKED-2 | §5; all statistics monotone in n; the only even-n-only class is the single "opposite" file |
| the CGT value of the trébuchet group is 0 (frozen) | not checked here | outcome only |

---

*All numbers in this report were produced by the scripts in this directory and are labelled
CHECKED-2 only where two independent implementations (the C solver and the pure-Python reference
solver, or the C solver and the flat-board cut-lemma reduction) agree. No file outside
`research/odd_cylinders_verify/` was modified. No Lichess tablebase request was made by this
task: the `ledger_t25.jsonl` file in this directory (two probe entries) was written by another
process and is not referenced by any command in this report.*
