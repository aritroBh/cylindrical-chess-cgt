# Flat 8x8 atlas and nimber search (workstream A2-search)

Saved by the parent session from the workstream's final report (workflow `wf_3dfce063-f42`, 2026-10-16). The subagent harness does not let workflow agents write report files, so the text below is the agent's, unedited except for removing that notice.

**Convention note (added 2026-10-16).** These results use cylcgt as of commit 6b8ca2f, where a pawn that can still be taken en passant already counts as passed. The user has since chosen the e.p.-aware test (`PASSED_RESPECTS_EP = True`). Values that depend on a live e.p. right change under it, notably the \*2 candidate; see [RESULTS.md](../../RESULTS.md).

All values come from the pawn-only model in cylcgt: one-sided passed pawn = ±256, races settled by RACE_RULE, normal play. Nothing is checked with real kings.

SCOPE
- Flat 8-rank boards, widths 1-4, pawns on ranks 2-7, at least one pawn per side.
- Positions where either side already has a passed pawn are skipped.
- A position is listed under width W only if both edge files are occupied, so each position that fits on 4 files appears once up to translation. Mirror images are reduced.
- Every (w,b) with w+b <= 6 was covered on all four widths. That includes the optional w+b=6 class on width 4; nothing in scope was skipped.
- Result: 231,071 canonical records, standing for 459,443 board positions. 47,255 of them are sums of separate components (all sum_safe).
- Database settings: en passant on, RACE_RULE count.

COMPUTE
- Enumeration: 2,796 CPU-s (46.6 CPU-min), 7.4 min wall. The pilot estimate was 8,443 CPU-s.
- Independent census: 1,722 CPU-s.
- Analyses: about 75 min of wall time, mostly single-process, on a machine with load average 40-150 from other sessions.
- Total is about 2 CPU-hours, which is over the "about 40 minutes" if that meant CPU time. No single job ran past about 13 min wall.

NIMBERS
- The only *k with k >= 2 in the database is the known candidate W a2 c2 / B b7 d7 on 4 files (plus its mirror). There is no *3 or *4.
- An independent search agrees on the nimber column for all 231,071 records (k <= 4): 6,470 zeros, 3,891 stars, one *2. It plays G + *j over the Codex rules code in crosscheck/.
- The candidate is not robust:

| Setting | Value |
|---|---|
| count, e.p. on / off | *2 |
| mover, e.p. on / off | *2 |
| opponent, e.p. on / off | 0 |
| every race won by White | up |
| every race won by Black | down |

- Both implementations agree in every setting, including "strict" e.p. (a heap move cancels a pending e.p. right).
- Race nodes with e.p. on: 398 edges and 224 distinct positions. 256 edges and 154 distinct positions come before any capture.
- Only 6 race positions matter. Fix them to the count-rule result and let every other race go to White, or every other race to Black: the value is *2 both ways. By monotonicity it is then *2 for any win/loss outcome of the other 218 races.
- This set of 6 is inclusion-minimal and was re-checked with the independent search.
- All 6 come after a capture, so each is 7 men in the embedding and inside Syzygy. White to move, count says Black wins:
  - 8/8/3p4/5Kp1/2p3Pk/8/P7/8 w
  - 8/3p4/8/5Kp1/2p3Pk/8/P7/8 w
  - 8/8/3p4/5Kp1/2p3Pk/P7/8/8 w
- Black to move, count says White wins:
  - 8/3p4/8/1P3Kp1/6Pk/8/P7/8 b
  - 8/8/3p4/1P3Kp1/6Pk/P7/8/8 b
  - 8/3p4/8/1P3Kp1/6Pk/P7/8/8 b
- No *k >= 2 is robust in scope: such a position would have to be *k under count with e.p. on, and the only one is the candidate.
- The independent census under all 13 race/e.p. settings found three other *2s, each under one non-default setting only:
  - W a2 b3 c3 / B a6 b5 b7 and its colour reversal W a3 b2 b4 / B a7 b6 c6, under opponent with e.p. on;
  - W a3 b2 d3 / B a6 c7 d6, under mover with e.p. off.
- With every race won by one side there is no *2 at all.

OTHER ELKIES TARGETS
These hold in the model only. Each was checked two ways (G - T is a second-player win) in all 10 settings: 550 position-settings, all in agreement.
- 1/8 occurs at 13 positions (and -1/8 at their colour reversals). 1/16 occurs at 3, 1/32 at 1.
  - W a2 a3 b2 / B a6 b5 b6 is 1/8 under all 6 settings and every race outcome. Its pawn structure cannot arise in chess: the a3 pawn has no file it could have come from.
  - The best reachable one is W a2 b2 d2 / B a5 c4 d7 (FEN 8/3p4/8/p4Kp1/2p3Pk/8/PP1P4/8 w). It is 1/8 under all three race rules and every race outcome, with e.p. on only.
- Up-second is {0 | down*}. I checked this against the CGSuite source by Siegel; I could not read the book itself. cgt confirms it is positive, that n times it is below up for n <= 64, and that up + up-second = {up | *}.
  - Exact up-second occurs at 5 positions. The best is W a3 c5 d4 / B a7 b7 d7 (FEN 8/pp1p4/8/2P2Kp1/3P2Pk/P7/8/8 w): up-second under all race rules and every race outcome with e.p. on, but a different value with e.p. off.
  - Up-second-star occurs at W a2 b2 b6 / B a6 b7 c5 (FEN 8/1p6/pP6/2p2Kp1/6Pk/8/PP6/8 w): the same under all 6 settings and every race outcome. The pawn structure is reachable, 10 men, 13 race edges, none before a capture.
  - No up-third component appears.
- No fractional tiny: tiny(x) never occurs for non-integer x. tiny(1) occurs at 13 positions and tiny(4) at 1. Number + tiny(1-down) and -1 + tiny(2-up) occur; tiny(1-up), which Elkies asked about, does not.

CONSISTENCY CHECKS
- Colour reversal: invariants hold on all 231,071 records; exact negation holds on a 400-record sample.
- Outcomes agree with crosscheck minimax on 1,600 of 1,600 sampled single components and 400 of 400 sampled sums.
- Elkies 1996 single-file values are reproduced: W a2 / B a4 = *, a5 = up, a6 = double-up-star, a7 = 0.

CAVEATS
- The database values (value, temperature, mean) were computed once, by cylcgt. Only the nimber column, a sample of outcomes and the specific claims above were checked a second way.
- The independent check reuses Codex's rules code, so both implementations share the count-rule encoding.
- "Robust" covers only the model's conventions. Every result still rests on: a one-sided passed pawn wins (+/-BIG), the trebuchet is a frozen zugzwang, and there are no draws.
- legal8x8 tests necessary conditions only (3,998 records fail them).
- I have not checked novelty against the literature.

## Claims

| id | importance | worker status | adversarial verification | statement |
|---|---|---|---|---|
| C1 | headline | checked-two-ways | not verified | Under RACE_RULE count with e.p. on, the only position in scope whose value is *k with k >= 2 is W: a2 c2 / B: b7 d7 on 4 files, plus its mirror image. Scope: flat, 8 ranks, widths 1-4, w+b <= 6, no passed pawn at the root. No *3 or *4 occurs. |
| C2 | headline | checked-two-ways | not verified | The candidate W a2 c2 / B b7 d7 is *2 under count and mover, with e.p. on or off. It is 0 under opponent, up when every race goes to White, and down when every race goes to Black. So it is not robust. |
| C3 | key | computed-once | not verified | Race nodes of the candidate. With e.p. on: 398 race edges (len(pawns.race_hits) from a cold cache), 224 distinct race positions; 256 edges and 154 distinct positions arise before any capture (all 4 pawns left). With e.p. off: 224 edges and 206 distinct positions; 154 edges and 136 distinct positions before any capture. |
| C4 | headline | checked-two-ways | not verified | The candidate's *2 (count rule, e.p. on or off) is certified by an inclusion-minimal set of 6 race positions, all after a capture (3 pawns, so 7 men with the trebuchet). If each goes the way the count rule says, the value is *2 for every White-win/Black-win outcome of the other races. |
| C5 | minor | computed-once | not verified | Flipping a single race outcome away from the count rule changes the candidate's value for only 4 of its 224 race positions (e.p. on) and 4 of 206 (e.p. off). All four come after a capture, and the new value is up or down. |
| C6 | headline | checked-two-ways | not verified | No position in scope is *k (k >= 2) under all six race/e.p. settings. The independent census under the 13 settings run finds only three other *2 positions, each under one non-default setting: W a2 b3 c3 / B a6 b5 b7 and its colour reversal, under opponent with e.p. on; W a3 b2 d3 / B a6 c7 d6, under mover with e.p. off. With every race given to one side there is no *2 at all. |
| C7 | headline | checked-two-ways | not verified | 1/8 occurs as an exact value at 13 positions under count with e.p. on (and -1/8 at their colour reversals). W a2 a3 b2 / B a6 b5 b6 is 1/8 under all 6 settings and every race outcome, but its pawn structure cannot arise in chess: with a2 and b2 both unmoved, the a3 pawn has no file it could have come from. The best reachable one is W a2 b2 d2 / B a5 c4 d7: 1/8 under all three race rules and every race outcome, with e.p. on only. |
| C8 | headline | checked-two-ways | not verified | Up-second-star ({0,* \| down}) occurs at W a2 b2 b6 / B a6 b7 c5 (3 files) with the same value under all 6 settings and every race outcome. The pawn structure passes the reachability conditions; 10 men; 13 race edges, none before a capture. Exact up-second ({0 \| down*}) occurs at 5 positions. The best, W a3 c5 d4 / B a7 b7 d7, is up-second under all race rules and every race outcome with e.p. on, but not with e.p. off. No up-third component appears. |
| C9 | key | computed-once | not verified | Definition used: up-second = {0 \| down*}. This is checked against Siegel's CGSuite source, not the book, which I could not access. CGSuite defines G^n = {0 \| H - G^->(n-1)} for G = {0\|H}. In cgt it is canonical and positive, n times it is below up for n = 1..64, and up + up-second = {up \| *}. |
| C10 | key | checked-two-ways | not verified | tiny(x) does not occur for any non-integer dyadic x tested (odd/2^j, j = 1..4, x < 8). tiny(1) occurs at 13 positions and tiny(4) at 1. The best tiny(1), W a2 b2 b6 / B a6 b7 c6, holds under all race rules and every race outcome with e.p. on. 1 + tiny(1-down), 2 + tiny(1-down) and -1 + tiny(2-up) occur; tiny(1-up) does not. |
| C11 | key | computed-once | not verified | The database has 231,071 canonical records (459,443 board positions). Settings: e.p. on, count rule. It covers every class in scope, including w+b=6 on width 4. Distinct values: 51,940, of which 1,441 do not involve BIG. 3,998 records fail the 8x8 pawn-structure conditions. |
| C12 | key | checked-two-ways | not verified | Consistency checks pass. Colour-reversal invariants hold on all 231,071 records, and exact negation holds on a 400-record sample. Outcome classes agree with crosscheck/minimax.py on 1,600 of 1,600 sampled single components and 400 of 400 sampled sums. Elkies 1996 single-file values are reproduced. |
| C13 | minor | computed-once | not verified | Compute went over budget. Enumeration took 46.6 CPU-min (7.4 min wall). With the census (about 29 CPU-min) and the analyses, the total is about 2 CPU-hours. |

### How to reproduce each claim

- **C1**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/enumerate.py enum ... (two phases, see C11), then merge; PYTHONPATH=. .venv/bin/python atlas/flat8/indep_scan.py --max-pawns 6 --workers 6 --out indep_scan.json
  ```
- **C2**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py robust
  ```
- **C3**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py robust
  ```
- **C4**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py cert
  ```
- **C5**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py sens
  ```
- **C6**:

  ```
  bash atlas/flat8/run_census.sh; PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py robust
  ```
- **C7**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py fractions; PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py summary
  ```
- **C8**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py targets; ... values; ... ups; ... summary
  ```
- **C9**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py targets
  ```
- **C10**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py targets; ... values
  ```
- **C11**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/enumerate.py enum --workers 6 --chunk 200 --six-widths 1,2,3 --out values_phase1.jsonl --log enum_log_phase1.json; PYTHONPATH=. .venv/bin/python atlas/flat8/enumerate.py enum --workers 8 --chunk 200 --classes 4:2:4,4:3:3,4:4:2 --out values_phase2.jsonl --log enum_log_phase2.json; PYTHONPATH=. .venv/bin/python atlas/flat8/enumerate.py merge values_phase1.jsonl values_phase2.jsonl --out values.jsonl; PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py legality
  ```
- **C12**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/analyze.py checks
  ```
- **C13**:

  ```
  n/a
  ```

## Bugs found

- No correctness bugs found in cylcgt/ or crosscheck/ in this run; the two agreed on every comparison made.
- Caveat, not a bug: cgt.show prints every number with |x| >= 128 as +W or -W, so value strings that contain W are not unique identifiers. Robustness comparisons in my code use game identity, or BIG-free strings, for that reason.
- Caveat: pawns.race_hits records races only for _value nodes not yet in the cache, so race counts are meaningful only after pawns._value.cache_clear(). My code always clears the cache before counting.

## Open questions

- Real chess (A2): are the 6 certificate race FENs won as the count rule says in Syzygy 7-man? If yes, the race part of the *2 claim is settled, apart from draws and the passer and trebuchet assumptions.
- Do the robust model values (up-second-star at W a2 b2 b6 / B a6 b7 c5; up-second at W a3 c5 d4 / B a7 b7 d7; 1/8 at W a2 b2 d2 / B a5 c4 d7) survive real king play in the trebuchet embedding? Are these pawn structures fully reachable, beyond the necessary conditions checked?
- Is any of the up-second, 1/8, 1/16 or 1/32 pawn configurations already in the literature? Novelty was not checked.
- Does a race position whose true chess result is a draw break any of these CGT identities? The model has no draws.
- Do 7-pawn components, or kingless constructions other than the 3-file trebuchet, give *4 or a robust *2?

## Next steps

- Write REPORT.md from this output's summary and claims, in a session that is allowed to write report files (the harness blocked it here).
- A2 verification: probe the 6 certificate FENs in Syzygy, plus the root FEN 8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 w and Black-to-move with Stockfish, or with the partial 8-man tablebase if it covers them.
- Run the same certificate analysis and real-chess checks on the up-second candidate W a3 c5 d4 / B a7 b7 d7 and the 1/8 candidate W a2 b2 d2 / B a5 c4 d7. For e.p. on, their race outcomes already do not matter.
- Have a second implementation recompute the full value column, not just the nimber column, for example the planned Rust atlas.
- Run a full retrograde reachability check of the candidate pawn structures with kings.
