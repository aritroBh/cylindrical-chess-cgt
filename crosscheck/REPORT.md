# Independent pawn-chess cross-check

> The sections below up to the first "Run 2026-11-22" heading are the archived record of 2026-10-15, produced with the textbook passed-pawn test only (before `PASSED_RESPECTS_EP`). They are kept unchanged. Later runs are appended by `.venv/bin/python -m crosscheck.compare --write`, one section per setting.

## Method

`minimax.py` searches the whole board and includes side to move and the expiring en-passant right in each memoized state. It does not import `cylcgt`; only this comparison harness imports the CGT implementation. Outcome classes are derived from the winners with White and Black to move.

Compared all 14 `verify_paper.CLAIMS` positions with e.p. enabled and disabled (28 claim cases), plus 3,000 distinct random positions (seed `20261015`; 2–7 pawns; 2,400 cylindrical and 600 flat; e.p. rule enabled and disabled in each geometry). The random set skipped starting positions where both sides already had passers. It generated 307 live e.p. rights.

Random candidates skipped for two starting passer sides: 10,138. White pawns on rank 1 and pawns on rank 8 are included in sampling.

## Summary

| Components | E.p. rule | Agree | Disagree | Total |
|---|---:|---:|---:|---:|
| single | on | 554 | 0 | 554 |
| single | off | 516 | 0 | 516 |
| multi | on | 956 | 4 | 960 |
| multi | off | 992 | 6 | 998 |
| **all** | — | **3018** | **10** | **3028** |


Single-component rows are the decisive check: the exact search and `cylcgt` must agree there. Multi-component results expose the limits of the disjunctive-sum approximation.

## Disagreement diagnosis

- **Single component: 0 mismatch(es).** A component sum cannot explain these; they indicate a disagreement in rule handling or an implementation bug. Inspect these first before assigning blame.
- **Multiple components with a live e.p. right: 0 mismatch(es).** These are consistent with the known approximation: real e.p. expires after any opposing move, even one in another component, while a disjunctive sum models component options independently.
- **Multiple components without a live e.p. right: 10 mismatch(es).** These cannot be blamed on live e.p. The main structural risk is the global passer/race rule: a move in one component can create a passer while another component supplies the opponent's passer, ending the whole position by the race rule. Summing local component values does not encode that cross-component terminal event.


The categories above identify the likely source, not proof by label. In particular, each single-component mismatch must be replayed against the move/race rules; multi-component mismatches without live e.p. need a concrete cross-component race witness before being attributed to that approximation.

## First 15 disagreements

### 1. random #77

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: c2 f1 f6 / B: b6 c7 e7 f5`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | 0} | {{{{-W, -1±+W | -W} | -W}, {{{-W, -1±+W | -W} | -W} | -W} | -W} | {{{-W, -2±+W | -W} | -W}, {{{-W, -2±+W | -W} | -W} | -W} | -W}}}`; outcome class `R`
- Components (2): `W: c2 / B: b6 c7; W: f1 f6 / B: e7 f5`

### 2. random #221

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: b6 e3 f1 / B: a7 c7 e6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `+W±+W`; outcome class `L`
- Components (2): `W: b6 / B: a7 c7; W: e3 f1 / B: e6`

### 3. random #556

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: a2 d4 h2 / B: b3 b8 e5 h4`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{{+W | +W, +W*} | 0} | {{-W | -W, -W*} | -W}}`; outcome class `R`
- Components (2): `W: a2 h2 / B: b3 b8 h4; W: d4 / B: e5`

### 4. random #756

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a2 c1 e2 / B: a6 d7 h4`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{↑ | {-W | -W*}, {↑ | {-W | -W*}}}`; outcome class `N`
- Components (2): `W: a2 / B: a6 h4; W: c1 e2 / B: d7`

### 5. random #1719

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a7 d3 e1 / B: b8 e5`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{+W | +W±+W} | tiny(+W)}`; outcome class `L`
- Components (2): `W: a7 / B: b8; W: d3 e1 / B: e5`

### 6. random #2123

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: d2 g3 g4 h1 / B: e3 e5 g8`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{+W* | +W*} | 5±1}`; outcome class `L`
- Components (2): `W: d2 / B: e3 e5; W: g3 g4 h1 / B: g8`

### 7. random #2276

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: b4 f1 / B: c5 f2 g6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `-W±+W`; outcome class `R`
- Components (2): `W: b4 / B: c5; W: f1 / B: f2 g6`

### 8. random #2298

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: b3 g4 h1 / B: b7 c6 h8`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{0, {0, +W±+W | 0} | {{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | {{{{0, +W±+W | 0} | 0} | 0} | {{{{+W* | -W*} | -W*} | -W, -W*} | -W}}, {{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | {{{{0, +W±+W | 0} | 0} | 0} | {{{{+W* | -W*} | -W*} | -W, -W*} | -W}}}}}`; outcome class `N`
- Components (2): `W: b3 / B: b7 c6; W: g4 h1 / B: h8`

### 9. random #2930

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: d3 e1 h4 / B: a6 e8 h6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{0 | {0 | tiny(+W), {0 | tiny(+W)}}}`; outcome class `L`
- Components (2): `W: h4 / B: a6 h6; W: d3 e1 / B: e8`

### 10. random #2931

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a5 b3 d6 g4 / B: a8 e7 g6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{+W* | 2*}`; outcome class `L`
- Components (3): `W: a5 b3 / B: a8; W: d6 / B: e7; W: g4 / B: g6`

## Run 2026-11-22: e.p.-aware passed-pawn test (PASSED_RESPECTS_EP=True), race rule `count`

3,028 cases, 3,016 agree, 12 disagree. Solver setting `ep_passed=True` in `minimax.py`, `pawns.PASSED_RESPECTS_EP=True` in `cylcgt`.

| Components | E.p. rule | Agree | Disagree | Total |
|---|---:|---:|---:|---:|
| single | on | 554 | 0 | 554 |
| single | off | 516 | 0 | 516 |
| multi | on | 954 | 6 | 960 |
| multi | off | 992 | 6 | 998 |
| **all** | — | **3016** | **12** | **3028** |

- **Single component: 0 mismatch(es).** A component sum cannot explain these; they indicate a disagreement in rule handling or an implementation bug. Inspect these first before assigning blame.
- **Multiple components with a live e.p. right: 2 mismatch(es).** These are consistent with the known approximation: real e.p. expires after any opposing move, even one in another component, while a disjunctive sum models component options independently.
- **Multiple components without a live e.p. right: 10 mismatch(es).** These cannot be blamed on live e.p. The main structural risk is the global passer/race rule: a move in one component can create a passer while another component supplies the opponent's passer, ending the whole position by the race rule. Summing local component values does not encode that cross-component terminal event.

### Disagreements (e.p.-aware, first 15)

### 1. random #77

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: c2 f1 f6 / B: b6 c7 e7 f5`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | 0} | {{{{-W, -1±+W | -W} | -W}, {{{-W, -1±+W | -W} | -W} | -W} | -W} | {{{-W, -2±+W | -W} | -W}, {{{-W, -2±+W | -W} | -W} | -W} | -W}}}`; outcome class `R`
- Components (2): `W: c2 / B: b6 c7; W: f1 f6 / B: e7 f5`

### 2. random #221

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: b6 e3 f1 / B: a7 c7 e6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{+W | +W±1/2} | {0 | -W±1/2}}`; outcome class `L`
- Components (2): `W: b6 / B: a7 c7; W: e3 f1 / B: e6`

### 3. random #284

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: a5 b4 e6 f4 / B: b8 f7 h5 (ep h6 for W)`
- Live e.p. state: `target=(7, 6), captured=(7, 5), side=W`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{+W±+W | -W±+W}`; outcome class `L`
- Components (2): `W: a5 b4 / B: b8 h5 (ep h6); W: e6 f4 / B: f7`

### 4. random #556

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: a2 d4 h2 / B: b3 b8 e5 h4`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{{+W | +W, +W*} | 0} | {{-W | -W, -W*} | -W}}`; outcome class `R`
- Components (2): `W: a2 h2 / B: b3 b8 h4; W: d4 / B: e5`

### 5. random #756

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a2 c1 e2 / B: a6 d7 h4`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{↑ | {-W | -W*}, {↑ | {-W | -W*}}}`; outcome class `N`
- Components (2): `W: a2 / B: a6 h4; W: c1 e2 / B: d7`

### 6. random #1719

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a7 d3 e1 / B: b8 e5`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{+W | +W±+W} | tiny(+W)}`; outcome class `L`
- Components (2): `W: a7 / B: b8; W: d3 e1 / B: e5`

### 7. random #2123

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: d2 g3 g4 h1 / B: e3 e5 g8`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{+W* | +W*} | 5±1}`; outcome class `L`
- Components (2): `W: d2 / B: e3 e5; W: g3 g4 h1 / B: g8`

### 8. random #2188

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: c5 f4 g1 / B: c7 d5 g7 (ep d6 for W)`
- Live e.p. state: `target=(3, 6), captured=(3, 5), side=W`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{{{+W | {+W | +W*}, {+W | {+W | +W*}}} | {0 | {0 | -W*}, {0 | {0 | -W*}}}} | {0 | {0 | -W*}, {0 | {0 | -W*}}}, {{0, +W±+W | 0}, {{+W | +W*} | {0 | -W*}} | {0 | -W*}, {{+W* | -W*} | -W*}}}`; outcome class `L`
- Components (2): `W: c5 / B: c7 d5 (ep d6); W: f4 g1 / B: g7`

### 9. random #2276

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: b4 f1 / B: c5 f2 g6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `-W±+W`; outcome class `R`
- Components (2): `W: b4 / B: c5; W: f1 / B: f2 g6`

### 10. random #2298

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: b3 g4 h1 / B: b7 c6 h8`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{0, {0, +W±+W | 0} | {{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | {{{{0, +W±+W | 0} | 0} | 0} | {{{{+W* | -W*} | -W*} | -W, -W*} | -W}}, {{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | {{{{0, +W±+W | 0} | 0} | 0} | {{{{+W* | -W*} | -W*} | -W, -W*} | -W}}}}}`; outcome class `N`
- Components (2): `W: b3 / B: b7 c6; W: g4 h1 / B: h8`

### 11. random #2930

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: d3 e1 h4 / B: a6 e8 h6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{0 | {0 | tiny(+W), {0 | tiny(+W)}}}`; outcome class `L`
- Components (2): `W: h4 / B: a6 h6; W: d3 e1 / B: e8`

### 12. random #2931

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a5 b3 d6 g4 / B: a8 e7 g6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{+W* | 2*}`; outcome class `L`
- Components (3): `W: a5 b3 / B: a8; W: d6 / B: e7; W: g4 / B: g6`

## Run 2026-11-22: textbook passed-pawn test (PASSED_RESPECTS_EP=False), race rule `count`

3,028 cases, 3,018 agree, 10 disagree. Solver setting `ep_passed=False` in `minimax.py`, `pawns.PASSED_RESPECTS_EP=False` in `cylcgt`.

| Components | E.p. rule | Agree | Disagree | Total |
|---|---:|---:|---:|---:|
| single | on | 554 | 0 | 554 |
| single | off | 516 | 0 | 516 |
| multi | on | 956 | 4 | 960 |
| multi | off | 992 | 6 | 998 |
| **all** | — | **3018** | **10** | **3028** |

- **Single component: 0 mismatch(es).** A component sum cannot explain these; they indicate a disagreement in rule handling or an implementation bug. Inspect these first before assigning blame.
- **Multiple components with a live e.p. right: 0 mismatch(es).** These are consistent with the known approximation: real e.p. expires after any opposing move, even one in another component, while a disjunctive sum models component options independently.
- **Multiple components without a live e.p. right: 10 mismatch(es).** These cannot be blamed on live e.p. The main structural risk is the global passer/race rule: a move in one component can create a passer while another component supplies the opponent's passer, ending the whole position by the race rule. Summing local component values does not encode that cross-component terminal event.

### Disagreements (textbook, first 15)

### 1. random #77

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: c2 f1 f6 / B: b6 c7 e7 f5`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | 0} | {{{{-W, -1±+W | -W} | -W}, {{{-W, -1±+W | -W} | -W} | -W} | -W} | {{{-W, -2±+W | -W} | -W}, {{{-W, -2±+W | -W} | -W} | -W} | -W}}}`; outcome class `R`
- Components (2): `W: c2 / B: b6 c7; W: f1 f6 / B: e7 f5`

### 2. random #221

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: b6 e3 f1 / B: a7 c7 e6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `+W±+W`; outcome class `L`
- Components (2): `W: b6 / B: a7 c7; W: e3 f1 / B: e6`

### 3. random #556

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: a2 d4 h2 / B: b3 b8 e5 h4`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{{+W | +W, +W*} | 0} | {{-W | -W, -W*} | -W}}`; outcome class `R`
- Components (2): `W: a2 h2 / B: b3 b8 h4; W: d4 / B: e5`

### 4. random #756

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a2 c1 e2 / B: a6 d7 h4`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{↑ | {-W | -W*}, {↑ | {-W | -W*}}}`; outcome class `N`
- Components (2): `W: a2 / B: a6 h4; W: c1 e2 / B: d7`

### 5. random #1719

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a7 d3 e1 / B: b8 e5`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{+W | +W±+W} | tiny(+W)}`; outcome class `L`
- Components (2): `W: a7 / B: b8; W: d3 e1 / B: e5`

### 6. random #2123

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: d2 g3 g4 h1 / B: e3 e5 g8`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{{+W* | +W*} | 5±1}`; outcome class `L`
- Components (2): `W: d2 / B: e3 e5; W: g3 g4 h1 / B: g8`

### 7. random #2276

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: b4 f1 / B: c5 f2 g6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `-W±+W`; outcome class `R`
- Components (2): `W: b4 / B: c5; W: f1 / B: f2 g6`

### 8. random #2298

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: b3 g4 h1 / B: b7 c6 h8`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{0, {0, +W±+W | 0} | {{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | {{{{0, +W±+W | 0} | 0} | 0} | {{{{+W* | -W*} | -W*} | -W, -W*} | -W}}, {{{0, +W±+W | 0} | 0}, {{{0, +W±+W | 0} | 0} | 0} | {{{{0, +W±+W | 0} | 0} | 0} | {{{{+W* | -W*} | -W*} | -W, -W*} | -W}}}}}`; outcome class `N`
- Components (2): `W: b3 / B: b7 c6; W: g4 h1 / B: h8`

### 9. random #2930

- Source: random; board: cylinder, 8x8; e.p. rule: on
- Position: `W: d3 e1 h4 / B: a6 e8 h6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `B`; Black to move → `B`; class `R`
- CGT: value `{0 | {0 | tiny(+W), {0 | tiny(+W)}}}`; outcome class `L`
- Components (2): `W: h4 / B: a6 h6; W: d3 e1 / B: e8`

### 10. random #2931

- Source: random; board: cylinder, 8x8; e.p. rule: off
- Position: `W: a5 b3 d6 g4 / B: a8 e7 g6`
- Live e.p. state: `none`; starting passers (W, B): `(False, False)`
- Exact wins: White to move → `W`; Black to move → `B`; class `N`
- CGT: value `{+W* | 2*}`; outcome class `L`
- Components (3): `W: a5 b3 / B: a8; W: d6 / B: e7; W: g4 / B: g6`
