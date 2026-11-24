# V2: reviewer-style run of the anonymous code copy (2026-11-23)

Copy: `dist/anon/out/cylinder-chess-review` (copied with `cp -R`, worked only in the copy). Paper: `dist/tog/tog_review.pdf`.
Machine: macOS, system python 3.14.7, `cc` present, no network. Heavy commands run under `nice -n 15`, one or two at a time.

## 1. README walk-through (in order, as a stranger)

| # | README command | Wall | Result |
|---|---|---|---|
| 1 | `python3 -m venv .venv` | 1.6 s | OK |
| 2 | `.venv/bin/python -m pip install pytest` | n/a | NOT RUN: reviewer rule "no network". It cannot succeed offline, and pytest is not on the system python either (`/usr/bin/python3`, Homebrew python3 both lack it). Everything that needs pytest was then run with the author's own project venv (pytest 9.1.1) pointed at the copy. |
| 3 | `.venv/bin/python -m pytest -q tests` | 3.7 s | 24 passed (author's venv python on the copy). With `python -I` it fails collection: `ModuleNotFoundError: cylcgt` (needs the top folder on the path; the README form without `-I` works). |
| 4 | `.venv/bin/python -m cylcgt.verify_paper` ("about 30 s") | 19.4 s | Runs, prints the puzzle table for 8x8 cylinder with e.p. on and off. README gives no expected values; see sec. 3 for what it shows. |
| 5 | `.venv/bin/python -m crosscheck.compare` ("2 to 5 minutes") | 91.5 s | Runs. e.p.-aware test: 3,028 cases, 3,016 agree, 12 disagree, single components 1,070 of 1,070. Textbook test: 3,018 agree, 10 disagree. README states no expected number; the supplement/RESULTS say the 10 disagreements are the known non-HSS ones (lemmas/test_L2_big.py T5 re-checks 10: all explained). |
| 6 | `cc -O2 -o egt tablebase/egt_prototype.c` | 0.2 s | OK, no warnings shown |
| 7 | `./egt cyl BN` | 1.9 s | `KBNvK: legal wtm=9733264 won=2384 (0.024%) maxDTM=2`. README says 2,384 of 9,733,264 (0.0245%), longest mate 2. **MATCH** (it prints 0.024%, the README 0.0245%: rounding only). |
| 8 | `cc -O2 -o kings/kpsolve kings/kpsolve.c` | 0.3 s | OK |
| 9 | `pytest -q kings/test_kpsolve.py` | 2.7 s | 10 passed |

Extra commands taken from `kings/REPORT.md` section 9: `kings/crosscheck.py --board cyl:4x5 ...` (7.8 s, 84,888 positions, 0 differ); `kings/lichess_check.py --max-men 4` (3.8 s, 3 positions, 0 DISAGREE, but "0 agree exactly, 3 with differing cap bounds that contain the truth"); `kings/failures.py` (0.03 s, wrote `kings/results/FAILURES.md`); `kings/experiment.py --board cyl:6x6 --promote Q --cap 2` (300 s, within the "about 5 minutes" claim; summary JSON: 42 components, 13 match, 13 mismatch all "king effect", 16 race-at-start, same as the section 4 table row `6x6 cylinder | d | 42 | 16 | 26 | 13 | 13 | 13`). Peak memory of that run was not measured (kpsolve reported 3.4 billion states; I did not check the 4 GB limit).

**Test totals.** `tests/`: 24 passed, 0 failed. `kings/test_kpsolve.py`: 10 passed. Other test-like scripts: `lemmas/test_L2_big.py --n 300` (72 s): "FAILURES: 0". Total pytest: 34 passed, 0 failed. No other `tests/` or pytest files were looked for beyond these (the README names two).

## 2. Instructions that were unclear, wrong or missing

1. The setup block cannot be followed offline and the README never says which pytest version; a stranger with no network has no pytest. `python3 -m pytest` works only if pytest is installed.
2. The README makes `.venv` but every command then assumes it holds pytest; with no network the venv is useless, and I had to substitute another interpreter.
3. `README.md` says "Some links in `RESULTS.md` point to working notes that are not part of this copy." True; the links break. `RESULTS.md` also names `notes/lemmas.md`, `delegate/out/K5/REVIEW.md`, `RESEARCH_PLAN.md`, none of which exist in the copy.
4. Hard-coded paths: 106 `.py` and 32 `.sh` files contain `/ANON/Downloads/Research/Chessendgames` (the anonymiser's placeholder for the author's home directory). Scripts that do `sys.path.insert(0, '/ANON/...')` then fail, e.g. `research/sum_whole_census/census.py 3 2 0 1` gives `ModuleNotFoundError: No module named 'lemmas'`; `census.py`'s `runjob.sh` does `cd /ANON/...`. So the 599,098-position census cannot be rerun without editing the files. 255 scripts also expect `../../.venv/bin/python` relative to the project root.
5. `research/star2_min_wide/reproduce.sh` and `research/ring_family_proof/run_all.sh` are only runnable from the project root with `.venv`; the long ones (the "quick" mode of run_all.sh alone says about 20 minutes) were not run.
6. The README gives expected output for only one command (the tablebase); `verify_paper` and `crosscheck.compare` print tables without saying what they should show, so a reviewer cannot judge MATCH/MISMATCH from the README.
7. `dist/` in the copy has only the two PDFs; large raw outputs are missing by design (the README says so), so the census numbers (599,098 etc.) rest on the report text, not on data a reviewer can recompute: `research/sum_whole_census/data/` holds only 24 KB of cross-check samples.
8. The copy contains `.pkl` pickle files (`dawson/quotient_Q12.pkl`, `Q29`, `Q32`): loading pickles from a code copy is a small safety concern; not opened.

## 3. Headline claims

| Claim in the paper (page) | Command | Output | Verdict |
|---|---|---|---|
| KBN against bare king on the cylinder: 2,384 wins of 9,733,264, longest mate 2 (sec. IX, p. 9; README) | `./egt cyl BN` | `legal wtm=9733264 won=2384 (0.024%) maxDTM=2` | MATCH |
| Ring M10 on C10 is value *2: "i7 on C10 (the ring M10 of Fig. 1) ... are *2" (p. 7, Fig. 1/6) | `echo "B4 W2 B6 W2 W3 B6 B7 W3 B7 W5" \| rg solve 3` after `cc -O2 -DMAXN=64 -o rg research/ring_family_proof/rg.c` (position from `research/c9_rings/REPORT.md`) | `NNPN` (outcomes of G+*h, h=0..3: that is *2) | MATCH (by the independent whole-board engine rg; the cylcgt value was not rerun) |
| Proposition 7: on C8, e.p. off, count rule, X = W b2 d4 g3 h5 / B a7 c7 f7 g4 is one component, S(X) is a black win whoever starts, W(X) a first-player win; X is not HSS (p. 6) | `PYTHONPATH=. python lemmas/test_L2_big.py --n 300` (T4) | `components=1 sum_safe=True HSS=False o(S)=R o(W)=N minimax=N crosscheck=N`; FAILURES: 0 | MATCH |
| Dawson's chess: 3 x n cylinder is a first-player win exactly when g(n-3)=0, for n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57 ... (Thm 16, Fig. 7) | `PYTHONPATH=. python -m dawson.octal` | `R_n = 1 for n in [3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, 61, ...]`; g(n) period 34 | MATCH |
| Earlier recurrence "agrees with g at only 31 of the 301 values n<=300, wrong cylinder outcome for 56 of them, the first at n=4" (p. 10) | same command | paper G != g at 270 values (so agrees at 31 of 301) ; ring outcome differs at 56 values, first n=4 | MATCH |
| 599,098 positions (flat boards 3-5 files, <=6 pawns, no passed pawn); 540,503 HSS ones agree; 19.3% of the rest differ (p. 6) | none in README; `research/sum_whole_census/census.py` is broken by `/ANON/...` paths and needs `./enum` and long runs | report text `research/sum_whole_census/REPORT.md` says 599,098; 540,503; 19.3% [19.0, 19.6] | NO COMMAND (not recomputable from the copy as shipped; reported text is consistent with the paper) |
| Smallest S != W position W a5 d3 / B b6 e4, a second-player win as a sum and a first-player win on the board (p. 6) | none direct | `research/sum_whole_census/REPORT.md` lists it with S=P, W=N | NO COMMAND (text only) |
| Least-pawn star-2 rings, n+3 pawns for n=3..7; ten pawns on C8, C9, C7 star-3 (Fig. 6, p. 7) | `research/star2_min_wide/reproduce.sh`, `research/c9_rings` jobs | multi-hour enumeration (4.3 million rings for C10 alone); not run | TOO LONG (and several scripts need `/ANON` edits) |
| 1/8, up-2-star, tiny(1) values beside the trebuchet; 1/8 and up2* in all nine settings (Sec. VI, Table) | `cylcgt.verify_paper` prints puzzle values only; the atlas runs need long jobs (`atlas/targets`) | verify_paper reproduces its own Puzzle 1 values (e.g. c-file ±1, f-file {3/2±1/2 | 0}); the claim about the 5/10/13 positions of Elkies' values was not rerun | NO COMMAND (README maps no quick command) |
| Trebuchet is a real mutual zugzwang, 0 (Fig. 3, Sec. IV) | `kings/experiment.py --board cyl:6x6 ...` summary field `trebuchet_is_mutual_zugzwang: true` (Pa3 pa4 Kf4 kb3); `kings/lichess_check.py` | true; table row 42/13/13/13 equals kings/REPORT.md | MATCH (for the 6x6 trebuchet; the 8x8 trebuchet table in kings/REPORT.md sec. 3 was not rerun) |
| e.p.-aware cross-check: whole-board solver vs CGT, the 10 disagreements are non-HSS (p. 6-7) | `python -m crosscheck.compare` and `lemmas/test_L2_big.py` T5 | textbook test 10 disagree (matches "10"); e.p.-aware test 12 disagree | PARTLY: the 10 matches the textbook run; the e.p.-aware run (the default setting) prints 12, a number I could not find in the paper. |

## 4. Anonymity

Command: `grep -rIn -i -E 'aritro|bhattacharjee|morley|uiuc|illinois|/Users/|gmail|github\.com/[a-z]'` (text files, `.venv` excluded).
- One hit file only: `engine/FAIRY_CYLINDER.md:15`, the URL `github.com/fairy-stockfish/Fairy-Stockfish/issues/753` (a third-party project): generic, not an author.
- Binary grep of the copy for `aritro|bhattacharjee`: no hits. The two PDFs have no author field (title, creator "LaTeX with hyperref" only).
- Not names, but leaks of provenance: 239 text files contain the placeholder `ANON` (e.g. `/ANON/Downloads/Research/Chessendgames` in code and reports): shows an author home path was scrubbed and makes scripts break. Many reports and `RESULTS.md` also describe the work as written by "Claude", "Codex", "OpenCode" models and mention an "orchestrating session"; that discloses tooling (and "the 2025 paper" in `dawson/REPORT.md` refers to the author's own earlier paper in the third person, which is a mild de-anonymisation risk). Directory names such as `delegate/out/K5/REVIEW.md` are cited but absent.
- `pytest` run on the copy wrote `__pycache__` and `kings/results/*` files into my working copy only; nothing was touched in the repository.

## 5. Verdict, as a reviewer

Could I reproduce the main numbers? Partly. The quick ones all reproduced exactly: KBN 2,384 / 9,733,264, mate length 2; Proposition 7's position (S black win, W first-player win, not HSS); Dawson's 3 x n cylinder win set and the 31/301 and 56 error counts; M10 is *2 under the independent engine; 34 tests pass; the 6x6 king sweep reproduces its table row. The costly headline results did not: the 599,098-position census, the 231,071-position flat census, the least-pawn star-2 ring table and the Elkies values need hours, large raw data that is deliberately removed, and scripts that are broken by `/ANON/...` paths. I could not check a single one of those numbers from the copy, only read them in the reports.

Complaints:
1. A reviewer without network cannot even run the tests (pytest). Vendor a one-line `python3 -m unittest`-style fallback or say so.
2. The README states expected output for one command only; add expected output for `verify_paper` and `crosscheck.compare` (the latter prints 12 disagreements in the default e.p.-aware setting but the paper's figure is 10; say which setting each number refers to).
3. 138 scripts hard-code `/ANON/...`; at least one runnable command per headline table (flat census, ring table, atlas) should run unedited from the top folder with relative paths.
4. A table in the README mapping each headline number in the paper to one command, with its expected output and running time.
5. Broken links to files not in the copy (`notes/lemmas.md`, `RESEARCH_PLAN.md`, `delegate/out/...`).
6. The reports narrate the production process (named AI tools, sessions, "verifier cut off by a usage limit"); a reviewer will wonder who vouches for it. The same files include self-confessed earlier mistakes, which is honest but makes "verified" labels hard to trust without a human referee (the paper itself says no human referee has yet checked the ring proofs).
