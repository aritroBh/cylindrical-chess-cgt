# Cylinder value atlas (workstream A3-cylinder-atlas)

Saved by the parent session from the workstream's final report (workflow `wf_3dfce063-f42`). Workflow agents may not write report files, so the text below is the agent's, unedited apart from removing that notice. Verification verdicts come from the workflow's adversarial verifiers; "not verified" includes verifiers that were cut off by a usage limit.

**Convention note.** These results use the textbook passed test (a pawn that can still be taken en passant already counts as passed), as in cylcgt before commit `ep-aware-passed` was merged. See RESULTS.md for the e.p.-aware results.

I built the atlas for every canonical pawn position with w+b ≤ 5 on cylinders and flat strips of widths 3–8: 1,223,689 positions with 10,369 distinct values. The main findings:

- The cylinder adds new values only on 3- and 4-file boards, and every one of them changes with the race rule.
- On the 8-file cylinder, no *2 (or higher) can be frozen with a trebuchet anywhere in the enumerated range.
- The paper's cylinder trebuchet is a genuine mutual zugzwang, but only because of the seam.

**What was computed.** The model is cylcgt.pawns with Elkies' conventions: a passed pawn is worth ±W (BIG = 256), races are scored by RACE_RULE (default "count"), and en passant is on. All pawns stand on ranks 2–7, and positions with a passed pawn at the start are skipped. Cylinder positions are reduced by rotations and reflection, flat ones by mirroring.

| n | cylinder positions | flat positions | cylinder values | flat values | cylinder-only (no W / with W) | flat-only (no W / with W) |
|---|---|---|---|---|---|---|
| 3 | 10,348 | 18,782 | 2,614 | 4,116 | 42 / 1,229 | 198 / 2,575 |
| 4 | 19,983 | 50,317 | 5,550 | 7,130 | 13 / 995 | 41 / 2,547 |
| 5 | 29,682 | 103,369 | 7,336 | 7,922 | 0 / 166 | 0 / 752 |
| 6 | 40,917 | 176,703 | 7,922 | 7,964 | 0 / 0 | 0 / 42 |
| 7 | 50,967 | 272,280 | 7,964 | 7,964 | 0 / 0 | 0 / 0 |
| 8 | 62,202 | 388,139 | 7,964 | 7,964 | 0 / 0 | 0 / 0 |

"With W" means a ±W option appears somewhere in the game; only 426 of the 10,369 values have none.

**1. Cylinder vs flat.**
- **Why widths 5–8 barely differ:** a cylinder position with an empty file has the same value as the flat position on n−1 files obtained by cutting there. This follows because an empty file stays empty. It was checked by random-position tests and by a set check over the whole atlas (0 values missing for n = 4–8).
- **Where new values can come from:** so the cylinder's values are the (n−1)-file flat values plus ring values (every file occupied). Rings need at least n pawns, so with ≤ 5 pawns they exist only on 3-, 4- and 5-file cylinders.
- **Cylinder-only values:** 53 values without W occur on some cylinder but on no flat strip up to 8 files: 40 from 3-file rings and 13 from 4-file rings.
- **Flat-only values:** no value occurs on a flat strip and on no cylinder.
- **Simplest witnesses:**
  - 3/4: 3-file cylinder `W a2 b4 / B b7 c6`.
  - −3/4: 3-file cylinder `W a2 b3 / B a5 c7`.
  - 1/4±1/4: 3-file cylinder `W a2 b2 / B c5 c6`.
  - 13/4±7/4: 3-file cylinder `W a2 a3 b2 / B b6 c7`.
  - {3/2±1/2 | −3/2±1/2}: 4-file cylinder `W a2 c2 / B b7 d7`. This is the same position that is *2 on the 4-file flat strip.
  - The 4-file flat strip has 41 values the 4-file cylinder lacks, including *2. They all come back on cylinders of 5 or more files.
- **Caveat:** the 3-file cylinder is degenerate, since every file touches both others.
- **Full lists:** logs/tables.txt and summary.json.

**2. Value classes.**
- **Nimbers:** only * and *2.
- **Number + star:** x* for x = ±1/2, ±1, ±2, ±3.
- **Ups:** ↑, ↑*, ⇑ and ⇑* occur as single components. 3·↑* and 4·↑ occur only as sums of two components. Integer shifts also occur.
- **Tinies:** only shifted by an integer (for example −1+tiny(2) is `W a2 b2 / B a6 a7 c6`). No unshifted tiny occurs with ≤ 5 pawns.
- **Fractions:** ±1/2, ±1/4, ±3/2, ±5/2 on both boards; ±3/4 only on 3-file cylinder rings. No 1/8.
- **Switches:** 47 on cylinders and 43 on flat strips. One is 9/8±7/8 = {2 | 1/4}.
- **Temperature:** the maximum without W is 3 on every width and both boards, from ±3 = `W a2 b4 / B a5 b7`. With W it is 517/2. Inside rings it is 2.

**3. Ring components.**

| Cylinder | Ring positions | Values | Values in no flat component | …without W |
|---|---|---|---|---|
| 3 files | 6,905 | 2,254 | 1,267 | 40 |
| 4 files | 4,629 | 2,232 | 986 | 15 |
| 5 files | 1,034 | 496 | 166 | 0 |

- **Common ring values:** 0, ±W, ±1, *, ±2, ±1*, ↑, ⇑*, switches.
- **No ring *2** under the count rule.
- **Not computed:** rings that need 6–8 pawns.

**4. A *2 on the 8-file cylinder.**
- **Geometry:** with a trebuchet on files x−1, x, x+1, the kings' files hold no pawns. Every other pawn therefore sits on the 5 files x+2…x+6, which form a flat segment, never a ring.
  - Up to 5 files wide if it may touch both king files.
  - 4 if it may touch one.
  - 3 if it may touch neither.
  - The flat 8×8 board is less cramped: the board edge acts as a free barrier.
- **Only candidate:** the only *k ≥ 2 found is *2 from the 4-file flat `W a2 c2 / B b7 d7`, unique up to symmetry. It is 4 files wide, so on the 8-file cylinder it must touch a king's file.
- **Freeze test:** at every reachable position, no pawn may stand next to an enemy king or give check. It is model-level only.
  - 0 of 40 placements pass on the 8-file cylinder; pawns on the a- or e-file meet the h- or f-king.
  - 20 of 40 pass on the flat 8×8, all with the component on a–d and the e-file empty.
  - The proposed FEN `8/1p1p4/8/5Kp1/6Pk/8/P1P5/8` passes on the flat board but fails on the cylinder: 1.a3 is check to the king on h4 across the seam, and a pawn on a4 can be taken.
- **Opponent rule:** under it, *2 instead appears on 3-file cylinder rings (`W a2 b3 / B a5 c5`), which cannot exist inside an 8-file board.
- **Bigger cylinder:** by the geometry, a 9-file cylinder would take the 4-file *2 with two empty buffer files. Not run.
- **Paper's trebuchet (WK h5, BK b4, W a4, B a5):**
  - **Across the seam:** WK h5 attacks a4, a5 and a6, the a4 pawn covers h5, and the a5 pawn covers h4. The black king on b4 attacks nothing across the seam.
  - **White to move:** Kg4, Kg5, Kg6, Kh6 or Ka6. Kh4 is covered by the a5 pawn. Each allows …Kxa4, a king-and-pawn ending that Black wins.
  - **Black to move:** Ka3, Kb3, Kc3, Kc4 or Kc5. Kb5 is covered by the a4 pawn. Each allows Kxa5, which White wins.
  - **Verdict:** so it is a mutual zugzwang as a 4-man position. Read on a flat board it is not, because Black simply takes a4.
  - **Every trebuchet passes:** the same test passes for all 80 trebuchets on the 8-file cylinder and all 60 on the flat 8×8.
  - **King-and-pawn table:** written for this check (one implementation). It promotes only to a queen and assumes king and queen against king is a win. Flat counts with rook promotion: White to move wins 124,960 of 163,328 and Black to move 97,604 of 168,024. Classic test positions come out right. On the cylinder the rook-pawn draw becomes a win.
  - **Not tested:** the trebuchet's interaction with other pawns.

**5. Race-rule and en passant sensitivity.**
- **The flat *2:** stays *2 under count and mover, with en passant on or off. It is 0 under opponent. The game tree meets 398 race positions with en passant on and 224 with it off.
- **The 3-file cylinder ±3/4:** survives turning en passant off under count. It becomes 0 under mover, and a *2-laden game under opponent.
- **The 4-file cylinder ring values:** keep their value under all three rules but change when en passant is off (for example {3/2±1/2 | −3/2±1/2} becomes ±1/2).
- **Values that never change:** ↑, ⇑*, 1/2, 1/2*, ±3 and 4·↑.
- **Values that need en passant:** ↑* and ⇑.
- **Whole-comparison check:** for ≤ 4 pawns the whole cylinder-vs-flat comparison was rerun under all six settings.
  - Cylinder-only values without W number 31, 18, 24, 25, 15 and 24.
  - Under the mover rule, 1/8, 3/8±1/8 and tiny(1/4) appear; under the opponent rule, *2, ↑*3 and ⇑*2 appear on the 3-file cylinder.
  - No value is cylinder-only under all six settings.
- **Conclusion:** which values are "cylinder-only" is undefined until the race rule is fixed.

**Checks.**
- **Single implementation:** all values, classes and temperatures come from cylcgt alone.
- **Independent check:** the minimax in crosscheck/ agrees on who wins for all 12,568 rings and 4,000 random flat components, with 0 disagreements. It shares the same conventions and checks the winner only, not full values.
- **Self-tests:** 4 tests pass (colour swap negates the value, symmetry invariance, the cut lemma, the *2).

**Skipped.**
- **w+b = 6:** 11.1 M positions, or 360 k single components at 1–4.5 s each under load (about 10⁴ CPU-minutes).
- **7-pawn rings on the 7-file cylinder:** 29,820 positions at about 5 s each (about 40 CPU-hours).
- **8-pawn rings on the 8-file cylinder:** not counted or computed.
- **Alternative rules for all 5-pawn positions:** only 5-pawn rings and ≤ 4-pawn positions were rerun.

**Compute.** About 60 minutes of wall time, over the 45-minute guideline. The first main run hung after 48 of 240 tasks. It was killed and resumed, skipping tasks already done, so nothing was lost or duplicated. The machine's load average was 50–250 from other sessions throughout.

**Reproduce** (all from the project root unless a step says otherwise):
- **Main atlas:** `PYTHONPATH=. .venv/bin/python atlas/cylinder/atlas_run.py --widths 3,4,5,6,7,8 --minpawns 2 --maxpawns 5 --mode all --shards 2 --jobs 6`
- **Merge:** unpack parts.tar.gz, then `PYTHONPATH=. .venv/bin/python atlas/cylinder/analyze.py`
- **Tables:** `cd atlas/cylinder && ../../.venv/bin/python tables.py > logs/tables.txt`
- **Sensitivity runs:** `sh atlas/cylinder/run_sensitivity.sh`
- **Sensitivity summaries:** `cd atlas/cylinder && ../../.venv/bin/python sens_compare.py && ../../.venv/bin/python sens_levels.py`
- **Headline positions:** `PYTHONPATH=. .venv/bin/python atlas/cylinder/sensitivity.py --file atlas/cylinder/headline_positions.txt --out atlas/cylinder/headline_sensitivity.jsonl`
- **Freeze test:** `PYTHONPATH=. .venv/bin/python atlas/cylinder/freeze.py`
- **Trebuchet:** `cd atlas/cylinder && cc -O2 -o kpk kpk.c && ../../.venv/bin/python trebuchet.py`
- **King-and-pawn counts:** `./kpk 8 0 1 </dev/null; ./kpk 8 1 0 </dev/null`
- **Cross-check:** `PYTHONPATH=. .venv/bin/python atlas/cylinder/crosscheck_outcomes.py`
- **Tests:** `PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider atlas/cylinder/test_atlas.py`

## Claims

| id | importance | worker status | adversarial verification | statement |
|---|---|---|---|---|
| C1 | key | computed-once | not verified | Every canonical pawn position with w+b ≤ 5 on cylinders and flat strips of widths 3–8 (8 ranks) was evaluated under the count rule with en passant on: 1,223,689 positions and 10,369 distinct canonical values. Positions with a passed pawn at the start are excluded. |
| C2 | key | proved | not verified | Cut lemma: a cylinder position with an empty file has the same value as the flat position on n−1 files obtained by cutting at that file. Hence cylinder values = (n−1)-file flat values plus ring values, so cylinder-only values come only from rings, which need at least n pawns. |
| C3 | headline | computed-once | reproduce: partially-confirmed; refute: confirmed; theory: partially-confirmed | With w+b ≤ 5 under count rule / e.p. on, 53 values without ±W occur on some cylinder of width ≤ 8 but on no flat strip of width ≤ 8: 40 come from 3-file rings and 13 from 4-file rings. Examples: 3/4 (3-file `W a2 b4 / B b7 c6`), −3/4, 1/4±1/4 (3-file `W a2 b2 / B c5 c6`), {3/2±1/2 \| −3/2±1/2} (4-file `W a2 c2 / B b7 d7`). No value occurs on a flat strip and on no cylinder. On 7 and 8 files the cylinder and flat value sets are identical. |
| C4 | headline | computed-once | reproduce: partially-confirmed; refute: refuted; theory: partially-confirmed | None of the cylinder-only values is robust to the race rule. With ≤ 4 pawns the whole cylinder-vs-flat comparison was rerun under all six settings (count / mover / opponent, e.p. on or off). The cylinder-only sets differ by setting (31 / 18 / 24 / 25 / 15 / 24 values without ±W), and no value is cylinder-only under all six. Every cylinder-only headline position changes value under some other setting; for example the 3-file 3/4 becomes 0 under mover and {*2, {*2\|0} \| 0} under opponent. |
| C5 | headline | computed-once | reproduce: partially-confirmed; refute: partially-confirmed; theory: partially-confirmed | With w+b ≤ 5 under count rule / e.p. on, the only nimbers are * and *2. *2 comes from exactly one component up to symmetry and translation: the 4-file flat W a2 c2 / B b7 d7 (398 race nodes; *2 under count and mover, 0 under opponent). On the 4-file cylinder the same pawns are {3/2±1/2 \| −3/2±1/2}. Under the opponent rule a different *2 appears on 3-file cylinder rings (W a2 b3 / B a5 c5). No *3 or higher occurs under any setting (rerun with ≤ 4 pawns). |
| C6 | key | proved | not verified | On the 8-file cylinder, a pawn group frozen by a trebuchet (pawns on file x, kings on x±1) always lies on the 5 files x+2…x+6 and forms a flat segment, never a ring. Its width is at most 5, at most 4 if it may touch only one king's file, and at most 3 if it may touch neither. |
| C7 | headline | computed-once | reproduce: partially-confirmed; refute: partially-confirmed; theory: partially-confirmed | No *k (k ≥ 2) within the enumerated range can be embedded with a trebuchet freeze on the 8-file cylinder. The 4-file flat *2 passes the conservative freeze test in 0 of 40 cylinder placements, against 20 of 40 on the flat 8×8 (all with the group on a–d and the e-file empty). The proposed FEN 8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 passes on the flat board, but on the cylinder 1.a3 is check to Kh4 across the seam. A 9-file cylinder would fit the *2 with two empty buffer files (not run). |
| C8 | key | computed-once | not verified | The paper's cylinder trebuchet 5.1 (WK h5, BK b4, W a4, B a5) is a mutual zugzwang as a 4-man position, and only because of the seam. WK h5 attacks a4, a5 and a6 across the seam; the a4 pawn covers h5 and the a5 pawn covers h4. Every one of White's 5 king moves allows …Kxa4 into a lost king-and-pawn ending, and every one of Black's 5 allows Kxa5. Read on a flat board it is not a zugzwang. The same test passes for all 80 trebuchets on the 8-file cylinder and all 60 on the flat 8×8. |
| C9 | key | checked-two-ways | not verified | The independent minimax in crosscheck/ (it does not import cylcgt) gives the same winner as the atlas for all 12,568 ring positions (3–5 files, w+b ≤ 5) and 4,000 random flat single-component positions (3–5 files): 0 disagreements. It checks outcome class only, not full values. |
| C10 | minor | computed-once | not verified | Value classes with w+b ≤ 5 under count rule / e.p. on: - Fractions: ±1/2, ±1/4, ±3/2, ±5/2, plus ±3/4 on 3-file cylinder rings only. No 1/8. - Tinies: tiny/miny(1) and tiny/miny(2) occur only shifted by an integer. - Ups: ↑, ↑*, ⇑, ⇑* occur as single components; 3·↑* and 4·↑ only as two-component sums. - Temperature: the maximum without ±W is 3 (±3, W a2 b4 / B a5 b7) on every width of both boards; inside rings it is 2. |
| C11 | minor | computed-once | not verified | King-and-pawn table counts. On the flat 8×8, with rook promotion credited, White to move wins 124,960 of 163,328 and Black to move 97,604 of 168,024. On the 8-file cylinder, with queen promotion only, White to move wins 126,736 of 160,656. The flat rook-pawn draw (Ka6, Pa5 vs Ka8) is a win on the cylinder. |

### How to reproduce each claim

- **C1**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/cylinder/atlas_run.py --widths 3,4,5,6,7,8 --minpawns 2 --maxpawns 5 --mode all --shards 2 --jobs 6 && PYTHONPATH=. .venv/bin/python atlas/cylinder/analyze.py
  ```
- **C2**:

  ```
  PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider atlas/cylinder/test_atlas.py ; summary.json -> lemma_check
  ```
- **C3**:

  ```
  cd atlas/cylinder && ../../.venv/bin/python tables.py > logs/tables.txt
  ```
- **C4**:

  ```
  sh atlas/cylinder/run_sensitivity.sh; cd atlas/cylinder && ../../.venv/bin/python sens_levels.py; PYTHONPATH=. .venv/bin/python atlas/cylinder/sensitivity.py --file atlas/cylinder/headline_positions.txt
  ```
- **C5**:

  ```
  grep '"val":"\*2"' atlas/cylinder/values.jsonl ; PYTHONPATH=. .venv/bin/python atlas/cylinder/sensitivity.py "flat 4 W: a2 c2 / B: b7 d7" "cyl 3 W: a2 b3 / B: a5 c5"
  ```
- **C6**:

  ```
  Argument in the summary, section 4; freeze.py docstring
  ```
- **C7**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/cylinder/freeze.py
  ```
- **C8**:

  ```
  cd atlas/cylinder && cc -O2 -o kpk kpk.c && ../../.venv/bin/python trebuchet.py
  ```
- **C9**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/cylinder/crosscheck_outcomes.py
  ```
- **C10**:

  ```
  cd atlas/cylinder && ../../.venv/bin/python tables.py
  ```
- **C11**:

  ```
  cd atlas/cylinder && ./kpk 8 0 1 </dev/null; ./kpk 8 1 0 </dev/null
  ```

## Bugs found

- No bugs found in cylcgt or crosscheck.
- A bug in my own runner, now fixed: atlas_run.py recycled worker processes (max_tasks_per_child=8), and the Python 3.12 process pool then stopped handing out work after 48 of 240 tasks. Recycling is now off by default, and resuming skips finished tasks.
- Display pitfall, not a bug: cgt.show prints every number ≥ 128 as +W, so distinct values such as 256 and 257 print the same. The atlas therefore identifies values by an exact canonical key. cgt.show also has no name for 4·↑ and prints it as {0 | {0 | ⇑}}.
- The harness refused to let this subagent write atlas/cylinder/REPORT.md. The report content is in `summary`.

## Open questions

- Which race rule matches real chess? Every cylinder-only value and both *2s (the 4-file flat one under count/mover, the 3-file cylinder rings under opponent) depend on it.
- Is there a *k ≥ 2 at most 3 files wide using 6 or more pawns? It would freeze on the 8-file cylinder with no king adjacency. Not enumerated.
- Does the 4-file *2 frozen on a 9-file cylinder (two empty buffer files) survive whole-board play?
- Rings needing 6–8 pawns (6–8-file cylinders) are the only place a wide cylinder can show new values. Not computed.
- The cylinder king-and-pawn verdicts assume king and queen against king is a win on the cylinder. That rests on the project's single-implementation 4-man tablebase.

## Next steps

- Save the report text from `summary` as atlas/cylinder/REPORT.md, since the harness blocked this subagent from writing it.
- Replace the race-rule approximation with an exact promotion-race model or whole-board play with frozen kings, then rerun sens_levels.py.
- Port the canonical-form engine to C or Rust, or run a targeted search, for 6-pawn single components on 3-file flat strips and for rings on 6–8-file cylinders.
- Check the 4-file *2 in a 9-file-cylinder whole-board position (workstream A2/B4 tooling).
- Have a second implementation (Codex) recompute the full canonical values of the 53 cylinder-only values; only their winners have been checked independently.
