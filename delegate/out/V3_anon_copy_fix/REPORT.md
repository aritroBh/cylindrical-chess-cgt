# V3: fix of the anonymous code copy generator (2026-11-23)

Only `dist/anon/build.py` was edited (untracked, ignored). Nothing committed. Work copies are in `<scratch>/` (`c`, `c2`, `f`).

## build.py changes
1. New constant `PROJECT_ROOT` and one line in `anonymise()`: the absolute project root is replaced by `.` before the home-directory scrub. `<root>/x` becomes `./x`, `<root>` becomes `.`, `<root>/.venv/bin/python` becomes `./.venv/bin/python`.
2. `make_readme()`: new sections "Quick checks (each under two minutes unless noted)", "Tests", "Not reproducible in minutes", "Saved quotients in `dawson/`" (inserted before "King-and-pawn solver"). Existing content and the section table are unchanged.

## Results of the rebuild
- Files containing `ANON/Downloads/Research/Chessendgames`: 0 (before: 106 .py and 32 .sh, 138 scripts, in 1,186 tracked files with a home path).
- Files containing the `ANON` placeholder: 239 before, 47 after (72 lines). Kinds: 44 times the munged agent-memory folder name `/-Users-ANON--claude-spares-ANON/`; 8 times `/-Users-ANON-Downloads-Research-Chessendgames/` (same kind); 13 bare `ANON` (scrubbed words); 1 `ANON/ANON` (the repository placeholder in `RESULTS.md`); 1 `CHECK_ANON.md` name. No path in code remains.
- `grep` for `aritro`, `bhattach`, `Users/aritro`, `ANON/Downloads` in the copy: 0 files.
- `census.py` import stage: `python3 research/sum_whole_census/census.py --help` no longer prints ModuleNotFoundError (`sys.path.insert(0, '.')`). It then fails inside `main()` because `--help` is not an argument it parses (it takes `w n shard nshards`); the full census was not run.
- `dawson/pawnboard.py` and `dawson/pawnboard_16.txt` ARE in the copy. Included set unchanged (5,676 files).
- build.py summary (last run, full, with fresh-copy runs): all PASS: identifier scan (tree and zip) True; no symlinks / no file over 5 MB / no *.log True; every path the README mentions exists True; fresh copy: venv, pytest import (offline substitute), pytest tests, verify_paper, crosscheck.compare, egt build, ./egt cyl BN, kpsolve build, pytest kings/test_kpsolve.py: all True. 5676 files, 77,160,329 bytes, zip 25,766,104 bytes. 23 RESULTS refs point to files not in the copy (as before).

## 10 versus 12 (what the records support)
- `python3 -m crosscheck.compare` (default `--setting both`) prints two runs of the same 3,028 positions: e.p.-aware passed-pawn test: 3,016 agree, 12 disagree; textbook test: 3,018 agree, 10 disagree. Under both, single components agree 1,070 of 1,070. Confirmed by running (90 s; `--setting textbook` alone 52 s).
- The 10 textbook cases are a subset of the 12 (the e.p.-aware run adds random #284 and #2188). All 12 are multi-component positions (6 with e.p. rule on, 6 off in the e.p.-aware run).
- `crosscheck/REPORT.md` (run of 2026-11-22) classifies them: cross-component race rule (a move in one component creates a passer while another supplies the opponent's passer; 10 cases without a live e.p. right) and e.p. rights that lapse after a move in another component (2 cases). `RESULTS.md` says the same ("as before, from the cross-component race rule and the e.p. right across components", CHECKED-2). `lemmas/test_L2_big.py` test T5 re-examines the 10 of `crosscheck/REPORT_after_fix.md` (textbook run): all sum_safe False, HSS False. The supplement source (`dist/tog/supp_src/s12_kings.md` line 425) mentions "The 10 multi-component disagreements". I found no sentence in the paper sources (`dist/tog/sections`) or the supplement source giving 12; the records explain 12 as the same set plus two. Whether the paper should state 12 for the engine default is the author's call. In the README note I wrote only what the records say.

## Commands run in the rebuilt copy (copied to `<scratch>/f`, outputs seen)
All matched the README table below: egt 2 s; rg 1 s (`NNPN nodes=3350`); crosscheck.py cyl:4x5 7 s (84888 positions, 0 differ); dawson.octal under 1 s; compare 90 s; compare --setting textbook 52 s; verify_paper 19 s; test_L2_big 71 s (`FAILURES: 0`, first T4 line is Proposition 7's position); trebuchet 295 s (`"trebuchet_is_mutual_zugzwang": true`, components 42, match 13). Tests with the project's venv python pointed at the copy (`PYTHONPATH=.`, nothing installed): `tests` 24 passed, `kings/test_kpsolve.py` 10 passed, together 34 passed. `python3 -m dawson.quotient 32` took 68 s and ended with `final full verification of Q_32: least failure = None`; the regenerated pickle is not byte-identical to the shipped one (not compared structurally).

## Not done / caveats
- pytest cannot be installed offline; the README says so. Peak memory of the trebuchet run was not measured (earlier report: 3.4 billion states).
- I did not run the census, the star-2 scans or the ring scans. Their reports give no running time (except atlas/flat8: 7.4 min wall enumeration, about 2 CPU-hours total; ring_family_proof/run_all.sh: about 20 and 25 minutes); the README says "no running time is stated" where so.
- The 599,098 and 231,071 labels: the first is in `research/sum_whole_census/REPORT.md` and RESULTS.md; I attributed the 231,071 flat 8x8 census to `atlas/flat8/` from RESULTS.md grep only (not read in detail).

## README text added (as generated)
## Quick checks (each under two minutes unless noted)

Every command in this README is run from the top folder of the copy. The commands below need only Python 3 and a C compiler
(`cc`); none of them needs pytest. Each row gives the claim, the command, the decisive line of output, and the time on one laptop.

| Claim in the paper | Command | Expected output (decisive line) | Time |
|---|---|---|---|
| King, bishop and knight against the bare king on the cylinder: 2,384 wins out of 9,733,264, longest mate 2 | `cc -O2 -o egt tablebase/egt_prototype.c && ./egt cyl BN` | `cyl    KBNvK: legal wtm=9733264 won=2384 (0.024%) maxDTM=2 ...` | 2 s |
| The ring M10 on C10 (Fig. 1) has value *2 | `cc -O2 -DMAXN=64 -o rg research/ring_family_proof/rg.c && echo "B4 W2 B6 W2 W3 B6 B7 W3 B7 W5" \| ./rg solve 3` | `NNPN nodes=3350` (outcomes of M10 + *h for h = 0..3: the value is *2) | 1 s |
| Proposition 7: the position `W b2 d4 g3 h5 / B a7 c7 f7 g4` on C8 is one component, not HSS, and S(X) differs from W(X) | `PYTHONPATH=. python3 lemmas/test_L2_big.py --n 300` | the first output line, `T4 Board(files=8, ranks=8, wrap=True, ep=False) W: b2 d4 g3 h5 / B: a7 c7 f7 g4: components=1 sum_safe=True HSS=False o(S)=R o(W)=N minimax=N crosscheck=N`; the last line is `FAILURES: 0` | 70 s |
| Dawson's chess on a 3 x n cylinder is a first-player win exactly for n = 3, 7, 11, 17, 23, ...; the earlier recurrence is wrong | `python3 -m dawson.octal` | `R_n = 1 (first player wins the ring) for n in [3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, 61, ...`; also `n <= 300 where paper G(n) != g(n): 270 values` and `paper Ring(n) != correct R_n: 56 values, first few [4, 5, ...` | under 1 s |
| Trebuchet: a real mutual zugzwang in the king-and-pawn game on the 6x6 cylinder (Fig. 3) | `cc -O2 -o kings/kpsolve kings/kpsolve.c && python3 kings/experiment.py --board cyl:6x6 --promote Q --cap 2` | `"trebuchet_is_mutual_zugzwang": true` in the summary printed at the end (also `"components": 42`, and counts `"match": 13`, `"race-at-start": 16`) | about 5 minutes |
| The king-and-pawn solver agrees with an independent reference solver | `python3 kings/crosscheck.py --board cyl:4x5 --material KPK KPKP KPPK --cap 1` (build `kings/kpsolve` first, as in the row above) | `cyl:4x5 KPK+KPKP+KPPK cap 1 promote QRBN ep on: 84888 positions, 0 differ` | 8 s |
| The sum model (CGT values of components) agrees with whole-board minimax on every single component; see the note below on the multi-component disagreements | `python3 -m crosscheck.compare` | `3,028 cases: 3,016 agree, 12 disagree; single components: 1,070 of 1,070 agree.` (e.p.-aware test), then `3,028 cases: 3,018 agree, 10 disagree; single components: 1,070 of 1,070 agree.` (textbook test) | 95 s |
| The puzzle values of the earlier study, recomputed with the exact engine | `python3 -m cylcgt.verify_paper` | a table for the 8x8 cylinder with e.p. on and off; one row per puzzle position with the claimed value, the computed value and the outcome class; for example `4.1 star  claim * -> *  outcome N` and `7.1  c-file  claim ±1 -> ±1  outcome N` appear in both blocks | 20 s |

About the 12 and the 10. Both runs compare the same 3,028 positions. The number depends on the passed-pawn test used by both
programs: 12 with the e.p.-aware test (the default of the engine), 10 with the textbook test (`python3 -m crosscheck.compare --setting textbook`
runs only that one). The 10 textbook cases are a subset of the 12. All of them are positions with two or more components; no
single component disagrees. `crosscheck/REPORT.md` explains them: a move in one component can create a passed pawn while another
component supplies the opponent's passer, which ends the whole board by the race rule, and an en passant right can lapse after a
move in another component. A sum of component values cannot see either event. `lemmas/test_L2_big.py` (test T5) re-examines the 10
textbook cases listed in `crosscheck/REPORT_after_fix.md` and checks that each is non-HSS and not sum-safe.

## Tests

The tests need `pytest`. The setup step above installs it and needs the network once. If pytest is already installed, run

```bash
PYTHONPATH=. python3 -m pytest -q tests kings/test_kpsolve.py
```

Expected: `24 passed` for `tests` and `10 passed` for `kings/test_kpsolve.py` (`34 passed` together). Build `kings/kpsolve` first (see below).

## Not reproducible in minutes

- The census of 599,098 flat-board positions (3 to 5 files, at most 6 pawns, no passed pawn): `research/sum_whole_census/census.py` with the
  generator `research/sum_whole_census/enum.c` and the job script `research/sum_whole_census/runjob.sh` (see `research/sum_whole_census/REPORT.md`, "Files"). The report states no running time. The raw
  per-position output is not in this copy; only small cross-check samples are.
- The census of 231,071 flat 8x8 positions: `atlas/flat8/` (see `atlas/flat8/REPORT.md`). Its report gives 7.4 minutes of wall time for the enumeration
  and about 2 CPU-hours in all, on a loaded machine.
- The least-pawn star-2 scans on flat boards: `research/star2_min_wide/reproduce.sh` (the full scan is `research/star2_min_wide/run_chain.sh`). The report states no running time.
- The least-pawn rings on small cylinders: `research/c9_rings/` and `research/star26_rings/`. No running time is stated.
- The ring family proof checks: `research/ring_family_proof/run_all.sh`. The script says about 20 minutes for the quick mode and about 25 for the slow mode on a loaded machine.

## Saved quotients in `dawson/`

The three files `dawson/quotient_Q12.pkl`, `dawson/quotient_Q29.pkl` and `dawson/quotient_Q32.pkl` are Python pickles of partial misere quotients of
Dawson's chess (the multiplication table, the P-positions and the map of strip lengths). `dawson/check_quotient.py` reads one of them and
compares it with the outcome table of `dawson/misere.c`. Do not load a pickle you do not trust. To regenerate one instead of loading it, run
`PYTHONPATH=. python3 -m dawson.quotient 32`; it rewrites `dawson/quotient_run_32.txt` and `dawson/quotient_Q32.pkl`.
It took 68 seconds on one laptop and ends with `final full verification of Q_32: least failure = None`.

## King-and-pawn solver
