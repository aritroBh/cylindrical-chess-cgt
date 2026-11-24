# Tall and short boards: how the number of ranks R changes the nimbers of the pawn game

Directory `research/tall_boards/`. Run 2026-11-22, about 2.7 h wall clock on a heavily loaded shared machine, at most two heavy processes at a time.
Labels: COMPUTED-1 = one program (the C solver `tw`); CHECKED-2 = `tw` and `cylcgt` (whole-board model, `.venv/bin/python`) both ran the exact claim.

## Summary (three lines)

1. **No *4 and no nimber above *3 occurs anywhere** in the {{SOLVED}} single-component positions solved (R = 5..12, cylinders of 3, 4, 5 files, flat boards of 3, 4 files); the nimbers found are only *0, *1, *2, *3 (COMPUTED-1). Positions solved by nimber, over all levels run: {{BYNIM}}.
2. **Height matters a lot and the minima are not monotone in R.** A *2 exists on short boards: with 4 pawns on R = 7 (3 files flat or cylinder, `W: a2 c2 / B: c3 b6`), with 6 to 8 pawns on R = 6 (not on R = 5, where every root on every board has been enumerated and none is *2 or *3). R = 8 gives 6 (C3), 7 (C4), 8 (C5), 7 (flat 4), 10 (flat 3) pawns, reproducing the repo's records. For R >= 9 the *2 minimum is 6 to 8 pawns and a *3 appears with 8 to 10 pawns on most boards.
3. **The paper's open question ("is there a *4 on eight ranks?") is not answered**; R = 8 reproduces every record I could match (about 200 M roots), and no height from 5 to 12 gives a *4 within the pawn counts reached (stated per row below). All 48 *2/*3 minimum positions and 16,000 random positions agree with `cylcgt`.

## The game (my reading of `cylcgt/pawns.py` and `cylcgt/cgt.py`)

Board of F files and R ranks, flat or cylindrical (file adjacency wraps). White pawns move up one square onto an empty square, and from rank 2 may also move two squares if both squares are empty. Black pawns move down, double step only from rank R-1. Captures are diagonal, forwards, onto an enemy pawn. En passant is on: after a double step with an enemy pawn beside the landing square, that enemy may capture the passed-over square, but only as its very next move; the right is gone after any other move (whole-board model: one e.p. right, cleared by any pawn move; for G + *h a move in *h does not clear it). A pawn is *passed* if no enemy pawn stands on its own or an adjacent file in front of it (ranks above for White, below for Black), except that a pawn which can be taken e.p. right now is not passed. The game ends at the first passed pawn: if only one side has one it wins (in CGT terms it is +-BIG); if one move creates passed pawns for both, the race rule "count" decides: the opponent of the mover wins unless the mover promotes strictly sooner, where a front passed pawn on rank r needs R-r moves (minus 1 for a White pawn still on rank 2, and symmetrically for Black on rank R-1). A player with no move loses (normal play). Value of G is `*k` when G + *h is a second-player win exactly for h = k, h = 0..7; I always record the 8-letter outcome string of G + *0 .. G + *7 (N first player wins, P second player, L Left, R Right) so that non-nimbers are not mistaken for nimbers: *k means the string is N in every position except P at position k.

## The solver `tw.c`

- State: two 64-bit masks (White, Black pawns) with square index `s = (rank-1)*F + file`, so any board with F*R <= 64 fits (F=5, R=12 uses 60 bits; the old packing used 8 bits per rank) plus a one-byte e.p. code (0 none; 1+sq: White just double-stepped and skipped square `sq`; 65+sq: Black did). Memo table of 2^25 entries x 24 bytes (about 0.8 GB RSS; `/usr/bin/time -l` measured 405 MB for the first 2^24 run, `ps` 788 MB for 2^25), cleared when half full.
- Each state stores two bytes, WL and WR: bit k says whether Left (Right) moving first wins G + *k, k = 0..7. Moves in G recurse; moves in *k use the mex rule. The race rule, the e.p.-aware passed test and the front-pawn distance are written from `pawns.py` (`passed`, `ep_capturable`, `promote_distance`, `_child`).
- Root class (same as `research/star4_hunt/` "roots" for flat boards, and rings as in `research/c9_rings/` for cylinders): White pawns on ranks 2..R-2, Black pawns on ranks 3..R-1 (a pawn elsewhere would be passed), distinct squares, **every file occupied** (one `cylcgt` component on a flat board; a ring on a cylinder), no passed pawn in the root, no e.p. right. Counted up to mirror (flat) or rotation and reflection (cylinder); splits nW + nB = p are taken with nW <= nB, and colour reversal (ranks flipped, colours swapped; it negates the game, so nimbers and the P/N pattern are unchanged) is identified when nW = nB. Enumeration is a file-by-file search with early passed-pawn pruning and a canonical-form test.
- **Not covered:** positions with an empty file (sums of components), flat boards of 1, 2 or 5+ files, cylinders of 6+ files. A *2 or *3 built as a sum of smaller roots is not looked for; the nim-sum argument of `research/star4_hunt/` is the only reason to expect nothing new there.

## Results: one table, board by R

"least p" = least number of pawns of a root with value *2 (*3). A number is exact when every smaller pawn count was enumerated completely; "none (space exhausted)" means every root of the board, for every pawn count, was solved; "none up to p pawns (N roots)" means every root with up to p pawns (N of them) was solved and nothing beyond was reached. The last column says up to which pawn count the enumeration was exhaustive. The nimber counts include the partly enumerated level where the run was stopped (budget), so they are lower bounds there. No hit of value >= *4 occurs in any row. COMPUTED-1 for "none" and for minimality; the existence of each reported minimum is CHECKED-2 (next section).

{{TABLE}}

Pawn counts above the "exhaustive through p" column were either not reached or only partly enumerated (per-level detail with roots, solved, complete flag and CPU time in `results/levels.tsv`; `logs/progress.txt` is the log). Per-level root counts are reproduced by `tw --count` (about 15 M roots/s), solving is 1 to 300 microseconds per root depending on height and pawn count.

### Answers to the three questions

1. Least pawns for *2 and *3, and whether *4 occurs: see the table. *4 or higher: none in any row.
2. Monotone in R? **No.** For *2 on flat 3 files: none R=5, 8 (R=6), 4 (R=7), 10 (R=8), 7 (R=9,10,11), 6 (R=12). For cylinder 3: none, none, 4, 6, 6, 6, 6, 6. For cylinder 4: none, 6, 6, 7, 6, 7, 6, 6. The same 7-pawn gadget `W: a2 b2 b5 / B: a5 b6 c7 c8` is *2 on flat 3 files for R = 9, 10 and 11, and not for R = 8 (where the c8 pawn would be on the promotion rank). **A shorter board does admit *2:** R = 6 (6 to 8 pawns, except cylinder 3) and R = 7 (4 pawns on 3 files); R = 5 admits no *2 and no *3 at all (every root of every one of the five boards enumerated: 236, 2,196, 121, 826, 5,847 roots for flat 3, flat 4, cylinder 3, 4, 5). *3 never occurs for R <= 6 or on 3 files at R = 7, 8, nor on flat 4 at R = 6 (exhaustive), but it appears with 6 pawns on flat 4, R = 7.
3. *4 candidates: **none**. Largest nimber found is *3 (positions in the next list).

### Hit positions at the least pawn count (notation of `research/star4_hunt/REPORT.md`)

{{HITS}}

Every nimber-2/3 hit found is in `results/hits.tsv` (columns: files, wrap, R, p, HIT, nimber, nW, nB, position, signature).

## Validation

**Validation 1: `tw` against `cylcgt`, full 8-letter signature (COMPUTED-1 solver, CHECKED against cylcgt).** For each R = 5..12, 2,000 random root-like positions without passed pawns (3 to 7 pawns, 3, 4 or 5 files, flat and cylinder with equal probability, not required to occupy every file, so gapped positions are also tested, whole-board model `pawns.components = lambda bd, p: [p]`), `validate.py` + `run_validate.sh`. Python skipped positions that took more than 40 s (R = 10: 1, R = 11: 6, R = 12: 11; none for R <= 9) and drew another. **Differences: 0 in all of them.**

```
{{VAL1}}
```
That is 16,000 positions with 0 differences; each R sample has 71 to 126 positions whose signature is *0 or *1, with the *2/*3 cases covered by validation 3.

**Validation 2: R = 8 control (exact matches with recorded lines).**
- `research/star4_hunt/REPORT.md` table A, flat 4 files, 11 pawns: roots 718,274 (2+9), 5,199,437 (3+8), 15,925,349 (4+7), 26,806,874 (5+6), total **48,649,934**; nimbers 0: **60,514**, 1: **24,230**, 2: **9**, 3: **1**, >= 4: 0. `tw` gives all of these (`results/control/control.out`).
- Same report, flat 5 files, 10 pawns: roots 2,658,896; 22,341,596; 64,796,378; 45,123,321, total **134,920,191**; **75 *2, 3 *3**, nothing higher. `tw` gives all of these (`results/control/control2.out`).
- `RESULTS.md` section 6c: C3 with 10 pawns, 741,110 rings (all splits, colours not exchanged), two *2: `tw --nocolsym` gives 741,110 and 2 (and 1 class up to colour reversal in the table's counting). C6 with 9 pawns: "three positions and their colour-reversed twins": `tw` finds 3 *2 in the nW < nB splits (13,506,022 roots). First ring *2 has n+3 pawns for n = 3, 4, 5: the table gives 6, 7, 8 for R = 8. "No *2 on flat boards of at most 4 files and 6 pawns": the table gives flat 4 minimum 7, flat 3 minimum 10. The flat 4-file R = 8 levels: 1 class of *2 at 7 pawns (`W: a2 b2 c4 / B: a5 b6 d6 d7`; star4 reports two 7-pawn cores A and B, which `RESULTS.md` says are one *2 up to colour reversal and mirror), 2 at 8 pawns, 5 at 9, and the first *3 at 9 pawns (`W: a2 b2 d2 c4 / B: d4 a5 b6 d6 d7`).
- Enumerator counts against `research/star4_hunt/h4 --count` at R = 8: 10 board/split combinations (flat 4, 5; cylinder 3, 4, 5) equal.
- Independent root counter (`indep_count.py`, brute force over labelled placements, no shared code) against `tw --count` at R = 5 to 12: 13 board/split cases (`results/indep_counts.txt`), all equal.

**Validation 3: every *2/*3 minimum reported is confirmed directly with `cylcgt`.** `val3.py` took the first hit at the least p for each board, R and q in {2, 3} ({{VAL3T}} cases) and ran `pycheck.py`; **{{VAL3N}} of {{VAL3T}} MATCH** the C signature (`results/validation3.txt`). Example (project root):

```
PYTHONPATH=. .venv/bin/python research/tall_boards/pycheck.py 3 0 7 "W: a2 c2 / B: c3 b6"
W: a2 c2 / B: c3 b6 | NNPNNNNN | *2
PYTHONPATH=. .venv/bin/python research/tall_boards/pycheck.py 4 0 7 "W: a2 c2 d3 / B: c3 d5 b6"
W: a2 c2 d3 / B: c3 d5 b6 | NNNPNNNN | *3
```
(arguments: files, wrap 0/1, ranks, position). No *4 candidate exists, so there was none to check.

## What was not reached (no silent caps)

- Cases whose enumeration stopped at the CPU budget are those where the last column of the table is smaller than the pawn counts of that board: levels beyond it were at most partly solved. Cases never finished at the "least *3" question: all the "none up to p pawns" cells. They are open, not negative; in particular cylinder 4 and 5 at R = 8..12 need more than 9 pawns and cylinder 5, R = 12 has no *2 up to 7 pawns (the next level has billions of roots).
- Gapped positions (sums), boards of 1-2 files and of 6 or more files, and tall boards beyond R = 12 were not run.
- `cylcgt` confirmation covers the minimum hits (existence), not "none" statements; those rest on `tw` alone, whose correctness is supported by validations 1 and 2 (16,000 + 150 M roots against records) and the enumerator counts by 23 independent comparisons.
- Python validation positions have at most 7 pawns; the 8 to 10 pawn *3 positions of the tall boards were confirmed individually (validation 3), but the solver was not compared with `cylcgt` on random 8 to 12 pawn positions.

## Rerun

From `research/tall_boards` (`tw` is built with `cc -O2 -o tw tw.c`; every heavy command below is run with `nice -n 15`):

```
cc -O2 -Wall -o tw tw.c
./tw --scan F WRAP R NW NB [--chunk i n] [--tlimit S] [--count] [--nocolsym]     # one split, e.g. ./tw --scan 4 0 8 4 5
python3 scan_driver.py WORKER BUDGET_S PASS            # all (board, R) cases; ONLY=F3c_R9 EXTEND=1 REVERSE=1 select/extend
./run_validate.sh                                       # validation 1 (needs project root venv; edit paths)
./run_controls.sh; ./run_control2.sh                    # validation 2 controls
(from project root) PYTHONPATH=. .venv/bin/python research/tall_boards/val3.py research/tall_boards/results/validation3.txt 420
./run_indep.sh; python3 aggregate.py; python3 hits_report.py; python3 make_report.py
```
Order I ran them: validation 1 with scan driver pass 1 (budget 420 s CPU per case, 240 s from R = 11 on), then pass 2 for a few cases (`F4c_R7`), pass 3-5 extensions of the narrow cases, controls, validation 3, independent counts. About {{CPU}} CPU hours of solving in total. PIDs of everything started are in `logs/*.pid` (stopped only by those PIDs; no pkill, killall, or git write command). Raw outputs are compressed with `zstd -19` and tested with `zstd -t` (`results/raw/*.zst`, `results/control/*.out.zst`, `results/val_R*.{eval,py,c}.zst`; originals removed after the test passed).

## Files

`tw.c` solver and enumerator; `scan_driver.py`, `aggregate.py`, `hits_report.py`, `make_report.py`; `validate.py`, `run_validate.sh`, `val3.py`, `pycheck.py`, `indep_count.py`, `run_indep.sh`, `run_controls.sh`, `run_control2.sh`; `results/{levels.tsv,hits.tsv,table.tsv,table.md,hits_at_minimum.md,validation1.txt,validation3.txt,indep_counts.txt}`; `logs/progress.txt`.
