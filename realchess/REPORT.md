# Real-chess certification of the *2 candidate (workstream A2-realchess)

Saved by the parent session from the workstream's final report (workflow `wf_3dfce063-f42`). Workflow agents may not write report files, so the text below is the agent's, unedited apart from removing that notice. Verification verdicts come from the workflow's adversarial verifiers; "not verified" includes verifiers that were cut off by a usage limit.

The real-chess oracle value of the embedded W a2 c2 / B b7 d7 component is not *2. Under the treatment "draws count as Black wins" (White must win), it is certified to be exactly {2±1 | -2±1} in both the textbook and the e.p.-aware model trees. That is the e.p.-aware model value; the textbook *2 does not survive real chess. This candidate does not answer Elkies' *2 question. Values are computed once; the terminal results under them are checked two ways.

# REPORT: A2-realchess, real-chess certification of W a2 c2 / B b7 d7 with the g-file trebuchet

**Labels.** "Checked two ways" means two independent programs agree. "Computed once" means one program produced it. "Tablebase" means a Lichess category. Every number has a reproduce command under "claims".

**Setup.** Root FEN 8/1p1p4/8/5Kp1/6Pk/8/P1P5/8, with White and with Black to move.

**Starting point.** This run continued the previous attempt (commit 28d790f). It reused all of that run's cached data and spent no requests twice.

## 0. Bottom line
1. **Real chess at the root: the side to move wins either way (outcome N).**
   - Proved by explicit certificates: 30 and 40 internal nodes, depth at most 6.
   - The result is the same when 50-move outcomes count as draws.
   - It is consistent with both *2 and {2±1 | -2±1}. It refutes the race rule "opponent", whose model value is 0 (a P-position).
2. **Root move tables.**
   - **Black to move (complete):** only 1...b5 wins. 1...b6, 1...d6, 1...d5, 1...Kg3 and 1...Kh3 all lose.
   - **White to move:** 1.c4 wins, and all four king moves lose to ...Kxg4 (tablebase). 1.a3, 1.a4 and 1.c3 are unresolved.
   - Both conventions, under the count and mover rules, predict exactly c4 and b5 as the only winning moves. Real chess agrees on every resolved move. All 13 decisive entries were re-proved by an independent prover.
3. **The real-chess oracle value.** This is the pawn-move tree with each model terminal replaced by its tablebase outcome class.
   - **It is never *2 or 0.**
     - In the adopted e.p.-aware tree this holds for every treatment of N, P and draw terminals, even when each such terminal may be any game in [-2BIG, +2BIG]. The bounds force Left stop ≥ 1 and Right stop ≤ -1, while *2 has stops 0 and 0.
     - In the textbook tree it holds only when draws count as wins for one side (N becomes {+BIG | -BIG}, P becomes 0). That needed an exact enumeration over the 9 terminals where a pawn can still be taken en passant.
   - **"White must win" (draw counted as a Black win):** the value is certified to be exactly {2±1 | -2±1} in both trees.
     - e.p.-aware: 9/9 cases pinned over its 2 open 8-man sides.
     - Textbook: 256/256 cases over 8 open sides.
     - In 40 random completions per tree, every one gave {2±1 | -2±1}.
     - This equals the e.p.-aware model value under count and mover.
   - **Draw counted as 0** (e.p.-aware): {2±1 | -2±1} ≤ G ≤ {5/2±3/2 | -2±1}. G equals the upper bound if the 8-man position 8/3p4/Pp6/2P2Kp1/6Pk/8/8/8 b is a White win. The model says it is; it was not resolved.
   - **"Black must win" (draw counted as a White win):** not pinned (58 essential open sides). *2 is still excluded.
4. **Interpretation.** The textbook *2 comes from the e.p. rule in the passed test. Real chess sides with the e.p.-aware model.
5. **Limits.**
   - The oracle value models king moves as losing. Real king moves are not always losing: 6 king moves were proven to draw, and at 3 nodes a king move is a best move.
   - Real node results disagree with the model at 14 (e.p.-aware, count) of 282 decisive node positions, mostly where the model says ±BIG.
   - A sum test is impossible on 8×8: there is no room for a second component.

## 1. Budget and data
- **Requests:** 1199 of 1200 used (1198 HTTP 200, one 429).
  - Previous run: 1171 (validation 160, roots 105, nodes 380, oracle 525, cli 1).
  - This run: 28. Six probed the root king-move children, 12 the 7-man terminal sides that the pin estimate marked essential, and 10 resolved Black's root moves b6, d6 and d5.
- **Offline knowledge base** (realchess/kb.py): 1512 records answering 7691 positions, with no conflicts.
  - 1205 records are in realchess/cache: 1198 fetched under my ledger and 7 written there by other workstreams under their own ledgers.
  - 307 are read-only, from engine/suite/tbcache and verify/engines/*/tbcache.
  - About 400 terminal sides were resolved for free by indexing the move categories inside cached records.
- **8-man positions:** contrary to the brief, Lichess returned a root category for 678 of the 915 8-man records cached (619 win, 41 loss, 18 draw). It apparently looks a ply or two ahead into the 7-man tables.
  - The main results use only ≤7-man tablebase data.
  - Where Lichess's 8-man category exists, it agrees with my search everywhere: 201/201 nodes, 125/125 textbook and 135/135 e.p.-aware terminal sides.
  - A labelled variant that uses these 8-man categories (_l8) agrees on all 626 shared sides and adds 70 more.

## 2. Move generator and probe client
- **movegen.py:** fully legal moves, FEN in and out, ep normalisation.
  - It matched the Lichess move lists exactly on 160/160 positions of up to 7 men: 30 hand-made, 30 e.p., 20 checks, 20 promotions, 18 pins, 8 double checks, 8 mates, 8 stalemates, 18 general. That run predates this one.
- **probe.py:** one file per FEN hash with atomic writes, an fcntl lock machine-wide, at least 1.05 s between requests, a 60 s back-off on 429, and a hard cap counted on a ledger.
- **New this run:**
  - kb.py: the offline index.
  - search.py: consults the KB first.
  - solve_candidate.py: new options `--offline` and `--label`; new stages oracle-all, kings and resolve.

## 3. Model nodes (8-man; textbook tree, both sides to move, 462 positions)
- **Coverage:** 295 resolved for the side to move (252 wins, 30 losses, 13 draws). Raising the off-model depth from 4 to 6 resolved nothing more: the data, not the depth, is the limit.
- **Independent check:** an AND/OR prover re-proved all 282 decisive results, and no opposite claim is provable.
- **Configurations:** 119 have both sides to move resolved. Real classes: N 89, L 10, R 6, P 1, draw 13.

Agreement of the model's outcome class with real chess, over the 119 configurations:

| Convention | count | mover | opponent |
|---|---|---|---|
| textbook | 91 | 90 | 85 |
| e.p.-aware | 92 | 91 | 85 |

Agreement per position (agree / disagree, plus 13 real draws in each case):

| Convention | count | mover | opponent |
|---|---|---|---|
| textbook | 263 / 19 | 261 / 21 | 239 / 43 |
| e.p.-aware | 268 / 14 | 266 / 16 | 247 / 35 |

- **Pattern:** the model says N, i.e. ±BIG ("whoever moves first makes a passer"), but real chess gives R, L or a draw. Examples: W a2 c2 / B b3 d3 is R; W a6 c6 / B b7 d7 is L.

## 4. King moves (1431 at the 462 node positions)
- **Proven to lose:** 133, each with a refutation from tablebase data or a bounded search.
- **Proven to draw:** 6. No king move is proven to win.
- **Unresolved and flagged:** 1292. Settling each would cost about one request.
- **Root:** all six king moves lose, to Kxg4 for White's and Kxg5 for Black's.
- **Drawing king moves:**
  - Kg6 in 8/3p4/8/2P2Kp1/1p4Pk/8/P7/8 w: the node is a draw.
  - Ke6 and Ke5 in 8/1p6/8/P2p1Kp1/6Pk/2P5/8/8 w: the node is a draw.
  - Kf6 in 8/1p6/3p4/P4Kp1/2P3Pk/8/8/8 w: the node is a draw.
  - Kg6 in 8/3p4/8/1pP2Kp1/6Pk/P7/8/8 w, without e.p.: the node is unresolved.
  - Kg6 in the same position with e.p. on b6: the node is a White win, so the king move is not best.

## 5. 50-move rule and draws
- No cursed-win, blessed-loss, maybe-win or maybe-loss category appears in any of the 1512 records, roots or moves. The "pure" and "fifty" modes therefore coincide.
- Draw terminals: 3, the same in both trees. In each, White to move draws and Black to move wins: W a4 / B b7 c6; W a5 / B b7 c5; W c4 / B a6 d6.

## 6. Oracle terminals

| | textbook tree | e.p.-aware tree |
|---|---|---|
| Internal nodes | 405 | 423 |
| Terminals (7-man / 8-man) | 670 (370 / 300) | 732 (394 / 338) |
| Sides resolved | 601 | 626 |
| Resolved both ways | 128 | 126 |
| Classes (L / R / N / draw) | 60 / 42 / 23 / 3 | 60 / 42 / 21 / 3 |

- **Independent check:** every resolved 8-man terminal side was re-proved by the prover (148 textbook, 156 e.p.-aware).
- **L/R terminals the count model gets wrong** (4 in each tree):
  - e.p.-aware: W a4 c5 / B b6 d5, the same with e.p. on a3, W a6 c5 / B b7 d4, and W a6 c5 / B b7 d5.
  - Under the opponent rule there are 20.
- **Races:** 22 race terminals were resolved. Five 7-man races that the count rule scores as Black wins are really N: W a2 / B c5 d7; W a3 / B c5 d6; W a3 / B c5 d7; W a4 / B c4 d6; W a4 / B c4 d7.
- **Treatments, and why:**
  - L becomes +BIG and R becomes -BIG.
  - N becomes {+BIG | -BIG} and P becomes 0, the canonical "the mover wins / loses big" games.
  - Draws are counted three ways: as Black wins (the binary game "White must win"), as White wins ("Black must win"), or as 0.
  - "Free" lets every non-L/R or unresolved terminal be any game in [-2BIG, +2BIG]. The width matters: ±BIG is confused with both +BIG and -BIG.
- **Certification method:** monotone sandwich bounds (raising an option never lowers a game), plus exact enumeration of the few essential open sides.

## 7. Model values, both conventions (4-file flat board)
- **Textbook:**
  - e.p. on: count *2, mover *2, opponent 0.
  - e.p. off: the same.
- **e.p.-aware:**
  - e.p. on: count {2±1 | -2±1}, mover {2±1 | -2±1}, opponent 0.
  - e.p. off: *2, *2, 0.
- **Control:** the e.p.-aware worktree run with the flag off reproduces the textbook values exactly.
- **Benchmark eligibility:** no. The component's value varies across conventions, race rules and e.p. settings.

## 8. Unresolved and caveats
- **White's root moves:** 1.a3, 1.a4 and 1.c3 are unresolved. The estimate is 8-12 requests each.
- **"Black must win" value:** not pinned.
- **Draw-as-0 value:** depends on one 8-man position (8/3p4/Pp6/2P2Kp1/6Pk/8/8/8 b).
- **Textbook draw-as-0 exclusion:** I stopped this at the 30-minute limit, so it is not determined.
- **The hybrid oracle object:** it ignores king resources, which section 4 shows exist.
- **One CGT engine:** all bounds, pins and exclusions use one canonical-form implementation (cylcgt/cgt.py) plus my bounds code. They are computed once. A randomized cross-check agreed (40/40 samples per run).

## Claims

| id | importance | worker status | adversarial verification | statement |
|---|---|---|---|---|
| C1 | headline | checked-two-ways | not verified | In real chess the embedded root 8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 is a win for the side to move with White to move and with Black to move (outcome class N). Also holds when 50-move outcomes count as draws. |
| C2 | headline | computed-once | not verified | e.p.-aware tree: the real-chess oracle value is neither *2 nor 0 under every treatment of N, P and draw terminals, including 'free', where each non-L/R or unresolved terminal is any game in [-2BIG, +2BIG]. The sandwich bounds give Left stop >= 1 and Right stop <= -1. |
| C3 | headline | computed-once | not verified | With draws counted as Black wins (the binary game 'White must win'; N becomes {+BIG\|-BIG}, P becomes 0), the real-chess oracle value is exactly {2±1 \| -2±1} in BOTH the e.p.-aware and the textbook trees. This equals the e.p.-aware model value under count and mover, and differs from the textbook model's *2. |
| C4 | key | computed-once | not verified | Textbook tree: *2 is excluded when draws count as wins for either side (N becomes a switch, P becomes 0), by exact enumeration over the 9 positions where a pawn can still be taken en passant. With the 'free' treatment the textbook sandwich does NOT exclude *2: its stops are only 0 and 0. |
| C5 | key | computed-once | not verified | e.p.-aware tree, draws counted as 0: {2±1 \| -2±1} <= G <= {5/2±3/2 \| -2±1}. G equals the upper bound if 8/3p4/Pp6/2P2Kp1/6Pk/8/8/8 b (W a6 c5 / B b6 d7, Black to move) is a White win, which is the model's prediction; this side is unresolved. With draws counted as White wins the value is not pinned (58 essential open sides). |
| C6 | key | checked-two-ways | not verified | Root move tables. With Black to move, only 1...b5 wins; b6, d6, d5, Kg3 and Kh3 lose (complete). With White to move, 1.c4 wins and all four king moves lose to ...Kxg4; a3, a4 and c3 are unresolved. Both conventions, under count and mover, predict exactly c4 and b5 as the only winners, and real chess agrees on every resolved move. |
| C7 | key | checked-two-ways | not verified | 8-man model nodes (462 embedded positions): 295 resolved (252 wins, 30 losses, 13 draws). Of 119 configurations with both sides resolved: N 89, L 10, R 6, P 1, draw 13. The model's outcome class agrees in 91/90/85 (textbook count/mover/opponent) and 92/91/85 (e.p.-aware). Most errors are model ±BIG positions that are really L, R or a draw. |
| C8 | key | computed-once | not verified | King-move audit: of 1431 king moves at the 462 node positions, 133 are proven to lose, 6 are proven to draw, none is proven to win, and 1292 are unresolved (flagged). Four of the 6 drawing king moves sit at 3 nodes whose real value is a draw, so a king move is a best move there; the pawn-only model ignores this. |
| C9 | key | checked-two-ways | not verified | Terminals with an N, P or draw class. e.p.-aware: 21 N and 3 draws among 126 terminals resolved both ways (L 60, R 42). Textbook: 23 N and 3 draws among 128. The draws are W a4/B b7 c6, W a5/B b7 c5 and W c4/B a6 d6, each a draw with White to move and a Black win with Black to move. Five 7-man race terminals that the count rule scores as Black wins are really N. Four L/R terminals contradict the count model in each tree. |
| C10 | key | checked-two-ways | not verified | Model values on the 4-file flat board. Textbook: *2 under count and mover, 0 under opponent, with e.p. on or off. e.p.-aware: {2±1 \| -2±1} under count and mover and 0 under opponent with e.p. on; *2, *2, 0 with e.p. off. Not benchmark-eligible. |
| C11 | key | checked-two-ways | not verified | The move generator's legal move set matches the Lichess 'moves' list exactly on 160 of 160 positions of up to 7 men, covering e.p., promotions, checks, double checks, pins, mates and stalemates. |
| C12 | minor | computed-once | not verified | No cursed-win, blessed-loss, maybe-win or maybe-loss category occurs in any of the 1512 cached records, at the root or in the move lists, so the 50-move rule never matters here. |
| C13 | minor | checked-two-ways | not verified | Lichess returns categories for many 8-man positions: 678 of 915 cached 8-man records carry a root category (619 win, 41 loss, 18 draw), apparently from a shallow look-ahead into the 7-man tables. My search agrees with them on every overlap. |

### How to reproduce each claim

- **C1**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && for s in w b; do PYTHONPATH=. .venv/bin/python -m realchess.verify_proof "8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 $s - - 0 1" --claim win --depth 40 [--fifty]; done
  ```
- **C2**:

  ```
  EP=/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt; R=/Users/aritro/Downloads/Research/Chessendgames; cd $EP && PYTHONPATH=$EP:$R $R/.venv/bin/python -m realchess.solve_candidate oracle-all --offline --ext 4 --label _epaware_offline && PYTHONPATH=$EP:$R $R/.venv/bin/python -m realchess.stops_check --label _epaware_offline
  ```
- **C3**:

  ```
  (cd $EP && PYTHONPATH=$EP:$R $R/.venv/bin/python -m realchess.pin pin --label _epaware_offline --treatment "switch, draw = Black win"); cd $R && for i in 0 1 2 3 4 5 6 7; do PYTHONPATH=. .venv/bin/python -m realchess.pin pin --label _textbook_offline --treatment "switch, draw = Black win" --shard $i/8; done; PYTHONPATH=. .venv/bin/python -m realchess.random_check --label _textbook_offline --treatment "switch, draw = Black win" --samples 40 --certified "{2±1 | -2±1}"
  ```
- **C4**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.pin exclude --label _textbook_offline --treatment "switch, draw = Black win" --test lower --target "*2"   (also --test upper, and draw = White win)
  ```
- **C5**:

  ```
  (cd $EP && PYTHONPATH=$EP:$R $R/.venv/bin/python -m realchess.pin pin --label _epaware_offline --treatment "switch, draw = 0")
  ```
- **C6**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.root_table --print-resolve-command | sh; PYTHONPATH=. .venv/bin/python -m realchess.root_table; (cd $EP && PYTHONPATH=$EP:$R $R/.venv/bin/python -m realchess.root_table); results/comp_Wa2c2_Bb7d7_root_children_verified.json
  ```
- **C7**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.solve_candidate nodes --offline --ext 4 --label _offline && PYTHONPATH=. .venv/bin/python -m realchess.compare_nodes --label _offline && PYTHONPATH=. .venv/bin/python -m realchess.verify_nodes --label _offline --depth 12
  ```
- **C8**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.solve_candidate kings --offline --ext 2 --label _offline
  ```
- **C9**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.verify_nodes --oracleall comp_Wa2c2_Bb7d7_oracleall_pure_epaware_offline.json --depth 12
  ```
- **C10**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.model_values --out realchess/results/comp_Wa2c2_Bb7d7_model_values.json
  ```
- **C11**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.validate_movegen --cap 1200 --ledger realchess/logs/ledger.jsonl --out realchess/results/movegen_validation.json  (all cached: no new requests)
  ```
- **C12**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.kb
  ```
- **C13**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.verify_nodes --label _offline
  ```

## Tool usage

How to certify a different component with the same trebuchet. The trebuchet is WK f5, Pg4 / BK h4, Pg5, with file e empty. The component is pawns on files a-d only, for example C="W: a3 c2 / B: b7 d6". Every stage takes --component.

Setup:
- Run everything from R=/Users/aritro/Downloads/Research/Chessendgames. Stdlib only.
- e.p.-aware worktree: EP=/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt (git branch ep-aware-passed). Set REALCHESS_EPAWARE_PATH if it moves.
- e.p.-aware runs MUST use cwd=$EP with PYTHONPATH=$EP:$R, because `python -m` puts cwd first on sys.path. model_values and compare_nodes do this themselves and assert which cylcgt they loaded.

Budget:
- The shared ledger realchess/logs/ledger.jsonl is at 1199 of 1200. Use your own with --ledger <dir>/ledger.jsonl --cap N.
- The 1 request/s limit (a machine-wide lock in realchess/cache/.net.lock), the 60 s back-off on 429 and the cache dedupe across processes are automatic.
- All tablebase data already cached, including read-only sibling caches, is used for free through realchess/kb.py.

Steps:
0. Model values and benchmark eligibility: `PYTHONPATH=. .venv/bin/python -m realchess.model_values --component "$C" --out realchess/results/<tag>_model_values.json`. benchmark_eligible must be true for a benchmark component.
1. Cost estimate, no requests: `python -m realchess.solve_candidate roots --component "$C" --dry-run --hybrid --ext 6 --max-new 400`. Use the same flags with `nodes` or `resolve --fen ...`.
2. Roots: `... roots --component "$C" --ledger L --cap N --max-new 150 --ext 6`. Certificate: `python -m realchess.verify_proof "<root FEN>" --claim win --kb --depth 40 --out ...`.
3. All model nodes:
   - Offline first: `... nodes --component "$C" --offline --ext 4 --label _offline`.
   - Then online to fill gaps: `--ledger L --cap N --max-new k --per-target 25`.
   - Compare with the model under both conventions: `python -m realchess.compare_nodes --component "$C" --label _offline`.
   - Re-prove the results: `python -m realchess.verify_nodes --component "$C" --label _offline`.
4. Root move tables: `python -m realchess.root_table --component "$C" --print-resolve-command | sh`, then `python -m realchess.root_table --component "$C"`, and run it again from $EP for the e.p.-aware table.
5. King moves: `... kings --component "$C" --offline --ext 2 --label _offline`. To settle specific nodes online: `... kings --fen <FEN> --ledger L --cap N --max-new k --ext 0`, about 1 request per king move.
6. Oracle terminals:
   - Textbook tree: `... oracle-all --component "$C" --offline --ext 4 --label _textbook_offline`.
   - e.p.-aware tree: `(cd $EP && PYTHONPATH=$EP:$R $R/.venv/bin/python -m realchess.solve_candidate oracle-all --component "$C" --offline --ext 4 --label _epaware_offline)`.
   - Without --offline it probes unresolved 7-man terminals (1 request each) and searches 8-man ones, so cap it with --max-new.
   - `--use-l8` adds Lichess 8-man categories as leaves; give that run its own label.
   - `--resume` re-analyses a saved JSON without searching.
7. Pin or exclude:
   - Pin: `python -m realchess.pin pin --component "$C" --label _epaware_offline --treatment "switch, draw = Black win"`, run from $EP for the e.p.-aware tree. Treatments: "switch, draw = Black win|White win|0" and "free (only L/R fixed)".
   - The pin output lists the essential open sides. Probe the 7-man ones with `python -m realchess.solve_candidate resolve --component "$C" --fen <fen_W or fen_B from the oracleall JSON> --ledger L --cap N --max-new k --per-target 1 --ext 0`, then rerun steps 6 and 7.
   - Use `--shard i/n` to parallelise and `--max-cases` to raise the enumeration limit.
   - Exclusion: `python -m realchess.pin exclude --component "$C" --label ... --treatment ... --test lower|upper --target "*2"|"0"`.
8. Checks and summary:
   - `python -m realchess.random_check --component "$C" --label ... --treatment ...`
   - `python -m realchess.stops_check --component "$C" --label ...`
   - `python -m realchess.verify_nodes --component "$C" --oracleall <oracleall file>`
   - `python -m realchess.final_summary --component "$C"`, which writes results/<tag>_final_summary.json and needs all the earlier outputs.
- Output names use tag = comp_W<white squares>_B<black squares>, for example comp_Wa2c2_Bb7d7.
- Tests: `PYTHONPATH=. .venv/bin/python -m pytest -q realchess/tests` (32 pass, about 80 s).

## Bugs found

- Path pitfall, not a code bug. Running `PYTHONPATH=<ep-aware worktree> .venv/bin/python -m ...` from the project root silently imports the MAIN checkout's (textbook) cylcgt, because `python -m` puts the working directory ahead of PYTHONPATH on sys.path. I hit it once; it raised an error because the flag was missing. My tools now run inside the worktree and assert which cylcgt file was loaded. Worth checking that the e.p.-aware atlas recomputation (atlas/flat8/values_aware.jsonl.gz) was not run this way; I did not check.
- My first per-terminal bound wrongly treated N as lying between -BIG and +BIG. In fact ±BIG = {BIG | -BIG} is confused with both +BIG and -BIG. A unit test caught it, and it was fixed before any result was used: bounds now fall back to ±2BIG. The previous run's code was already correct on this.
- The brief says Lichess covers only up to 7 men and that 8-man roots return 'unknown'. In this data, 678 of 915 8-man records have a root category. Main results still use only ≤7-man data; the 8-man categories serve as a cross-check and in one clearly labelled variant (_l8).
- Minor: the node table (model_node_table / compare_nodes per-configuration counts) keys configurations without the e.p. right, so an e.p. variant and the plain position share one row. Per-position comparisons are unaffected.
- RESULTS.md section 1 still says 'Of 65 end positions resolved, 3 first-player wins and 2 draws...'. That is superseded: 126 (e.p.-aware) / 128 (textbook) end positions are now resolved both ways, with 21/23 N and 3 draws, and the value is pinned under the 'White must win' treatment. The older realchess/consistency.py and summarize.py reflect the partial earlier data and are superseded by compare_nodes.py and final_summary.py.

## Open questions

- What is the oracle value when draws count as White wins (the game 'Black must win')? It is not pinned: 58 essential open sides, 43 of them 8-man.
- e.p.-aware, draw = 0: is 8/3p4/Pp6/2P2Kp1/6Pk/8/8/8 b a White win, as the model says? If so the value is {5/2±3/2 | -2±1}. It needs an 8-man search; the hybrid dry run needs at least 14 requests and still did not resolve it.
- Real results of White's root moves 1.a3, 1.a4 and 1.c3: estimated at 8-12 requests each.
- 1292 king moves at 8-man nodes are unresolved. How often does a king move beat the pawn moves the model plays?
- Which draw treatment is the right CGT reading of real chess? Each binary game (White must win / Black must win) is well defined, but the two give different values. A loopy or affine treatment may be the principled answer.
- Does the oracle value predict real play in sums? That cannot be tested on 8×8, because there is no room for a second component; it would need a wider board, which has no tablebase.

## Next steps

- Give the remaining gaps a fresh ledger and budget: White's root moves a3, a4, c3; the open 8-man side for the draw-as-0 case; king-move refutations at nodes near the root.
- Run the pipeline on benchmark-eligible components (same value under both passed tests, all race rules, e.p. on and off), starting with the dry-run cost estimates.
- Check the e.p.-aware atlas commands for the `python -m` path pitfall.
- Update RESULTS.md section 1: real chess gives N at the root, the Black root move table matches CGT, and the oracle value is {2±1|-2±1} under 'White must win' in both trees, so not *2.
- Consider an exact treatment of king resources (the kings/ loopy modelling), since drawing king moves exist.
