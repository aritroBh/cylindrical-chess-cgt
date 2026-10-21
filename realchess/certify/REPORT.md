# Real-chess certification of the other *2 candidates (workstream A2-certify)

Saved by the parent session from the workstream's final report (workflow `wf_3dfce063-f42`). Workflow agents may not write report files, so the text below is the agent's, unedited apart from removing that notice. Verification verdicts come from the workflow's adversarial verifiers; "not verified" includes verifiers that were cut off by a usage limit.

I certified none of the candidates as a king-and-pawn *2 on 8x8, and Elkies' question stays open. One 10-man candidate, W a3 b3 c2 / B b5 b7 c6, is now refuted at the oracle level. For the other four 10-man candidates, the tablebase contradicts the race rule their *2 depends on, but their oracle values cannot be settled with tablebases of 7 men or fewer. I used 863 of my 1,200 requests; the shared ledger was not touched.

# REPORT: A2-certify. Real-chess certification of the *2 candidates (trebuchet WK f5, Pg4 / BK h4, Pg5; file e empty)

**Labels.**
- *Tablebase*: a Lichess category for a position of 7 men or fewer.
- *l8*: Lichess's own category for an 8-man position. It is computed by looking ahead into the 7-man tables, not from 8-man tables (records have dtz=1 and dtc=null). It is used only where labelled.
- *Search*: exact realchess search, with the tablebase at every capture.
- *Checked two ways*: two independent programs agree.
- *Computed once*: one program produced the result.
- *Engine*: a Stockfish 19 evaluation. It is evidence, not proof.
- *Model*: the cylcgt pawn-only model.

**The oracle value**, as defined in realchess/oracle_value.py: take the pawn-move tree, and replace each terminal (first passed pawn) by a game built from its real results with White to move and with Black to move. L becomes +BIG, R becomes -BIG; the treatments decide N, P and draws.
- **"Free" treatment**: only certain L/R terminals are fixed, and every other terminal is any game in [-2BIG, +2BIG].
- A bound proved under "free" therefore holds for every treatment.
- King moves are outside this tree.

## 0. Bottom line

1. **No candidate is certified *2.** None of the six answers Elkies' question on present evidence.

2. **Candidate 2, W a3 b3 c2 / B b5 b7 c6, is refuted at the oracle level.**
   - FEN: 8/1p6/2p5/1p3Kp1/6Pk/PP6/2P5/8, 10 men, legal, kings and pawns only.
   - In both the textbook and the e.p.-aware pawn tree, the oracle value G satisfies G ≥ G_lo = {0 | {0 | -2, -1±1}} > 0. That holds whatever games in [-2BIG, +2BIG] are given to the 1,698 terminals that are not certified. So G ≠ *2 (and G ≠ 0).
   - It rests on only 5 terminals (10 sides, 7-8 men) that the tablebase plus search certify as White wins with either side to move.
   - **Each side is checked two ways:** by search with no l8, and by the independent AND/OR prover realchess/verify_proof using cached ≤7-man records only. None depends on Lichess 8-man categories.
   - **The bound is checked two ways:** by canonical forms (cylcgt), and by a direct win/loss minimax of G_lo and G_lo + *2. The direct solver agreed with cylcgt on 20/20 random terminal assignments.
   - **What White does:** White's pawn strategy has 57 nodes with Black first and 44 with White first. It ends in one of the 5 certified terminals, or in a position where Black has no pawn move (8, resp. 4 such positions).
   - **Limits:**
     - The oracle tree ignores king moves.
     - A full real-chess proof that the root is won for White either way is incomplete: 12 Black king-move positions with 9-10 men are unresolved after 200 requests.
     - Engine: all 62 Black king moves in White's strategy evaluate as White wins (34 mate scores, mate in 11-19; the rest ≥ +7.61; 5 s each, depth ≥ 32).

3. **Candidates 3-5** (W a3 b2 b4 / B a7 b6 c6; W a3 b2 c2 / B a4 b6 c5; W a5 b3 c4 / B a6 b7 c7):
   - **Model:** *2 only under the race rule "opponent". For candidate 3 that holds under both passed tests; for 4 and 5 only under the e.p.-aware test. Under the adopted count rule none is *2.
   - **Decisive races:** the *2 is pinned by a few race entries of 6-7 men (5, 3 and 3 entries). The tablebase contradicts the opponent rule at 3/5, 2/3 and 2/3 of them.
   - **Oracle value: undetermined.** It depends on 9-man terminals that the tablebase cannot reach.
   - **Conditional result:** if unresolved one-sided terminals are taken as wins for the passer's owner (the model convention) and races are left free, *2 is excluded:
     - candidate 3 under the three switch treatments;
     - candidate 4 under the switch treatments;
     - candidate 5 under all four treatments (e.p.-aware), or the two "switch, draw = Black/White win" treatments (textbook).
   - **That conditional value is fragile.** For candidate 4, an intermediate data set (34-35 resolved sides) gave exactly *2 under "draw = White win" and "draw = 0", in both trees. 18 more 6-7-man sides moved it away again.
   - **No certificate is possible here:** pinning candidate 4's value needs 32-63 terminals, 15-34 of them with 9 men.

4. **Candidate 6** (W a3 b2 d3 / B a6 c7 d6):
   - *2 only with e.p. switched off (mover rule).
   - With the e.p. rule (as in real chess), it is *2 under no race rule and under neither passed test.
   - Real-chess races are at 9-10 men, so only the engine was used.

5. **No embedding of 7 men or fewer exists.**
   - The trebuchet costs 4 men.
   - In the flat-8 census (231,071 positions, 9 settings), every *k with k ≥ 2 has 4 or 6 pawns (atlas/flat8/rerun/census_summary.json).
   - So the only 8-man candidate is the original, and the rest have 10 men.
   - I did not search for other king freezes.

6. **The original W a2 c2 / B b7 d7 is not *2 in real chess at the oracle level (e.p.-aware tree).** Details are in section 2.

7. **Engine roots** (Stockfish 19, 60 s, depth 36-41; engine evidence only).
   - Candidates 2, 3 and 6 look like outcome L: White wins with either side to move. That is incompatible with *2, which is N.
   - Candidates 4 and 5 look like N.

| Candidate | White to move | Black to move | Outcome |
|---|---|---|---|
| 2 | c3, +7.21 | c5, -12.97 | L |
| 3 | a4, +5.96 | a6, -6.46 | L |
| 4 | c4, mate 19 | c4, +10.18 | N |
| 5 | c5, +17.81 | c5, +17.08 | N |
| 6 | d4, +10.75 | a5, -5.25 | L |

(Scores are for the side to move.)

## 1. Model values and tree statistics (cylcgt; both trees, run from each worktree)
- **Candidate 2:**
  - count and mover: {0 | {0, *, …}} (outcome L) under both tests.
  - opponent: *2.
  - e.p. off: count/mover {0 | {0 | ↓*}}, opponent ↑*.
  - Tree: 1,384 internal nodes, 1,703 terminals (by men 5:13, 6:34, 7:287, 8:717, 9:562, 10:90). Races occur only at 6-8 men.
- **Candidate 3:** count and mover give an outcome-R game; opponent gives *2 (e.p. off ↓*). The tree has the same shape as candidate 2's.
- **Candidate 4:**
  - Textbook: count *, opponent ↑*.
  - E.p.-aware: count -1/4±1/4, opponent *2.
  - E.p. off: 1/4.
  - Tree: 273 internal nodes, 440 terminals (9 men at most).
- **Candidate 5:** colour reversal of 4. E.p.-aware count 1/4±1/4, opponent *2.
- **Candidate 6:** mover/epoff *2. Every e.p.-on value is a different N game. Tree: 1,296 internal nodes, 1,470 terminals, 248-256 races with up to 10 men.
- **Benchmark eligibility:** none of the six is eligible.

**Decisive race entries** (from tree_stats.py, with the tablebase result for the side to move):

| Candidate | Race (side to move) | Opponent rule says | Tablebase |
|---|---|---|---|
| 2 | c4 / b4 (W) | W | Black wins |
| 2 | c5 / b5 (W) | W | White wins |
| 2 | a3 / c4 c5 (W) | W | draw |
| 2 | a3 b5 / c5 (B) | B | White wins |
| 2 | a4 / c5 c6 (W) | W | White wins |
| 3 | b4 / a4 (B) | B | Black wins |
| 3 | b5 / a5 (B) | B | White wins |
| 3 | a3 a4 / c5 (B) | B | White wins |
| 3 | a4 / b4 c6 (W) | W | White wins |
| 3 | a4 a5 / c6 (B) | B | White wins |
| 4 | a3 / c4 (W) | W | draw |
| 4 | a4 / c5 (B) | B | White wins |
| 4 | c3 / a4 (B) | B | Black wins |
| 5 | a5 / c6 (W) | W | White wins |
| 5 | c4 / a5 (W) | W | draw |
| 5 | c5 / a6 (B) | B | White wins |

- **Pattern:** the trebuchet is asymmetric. With the white king on f5 and the black king on h4 at the edge, White does better in queen races than the count rule predicts.
- **One-sided terminals:** across all resolved one-sided terminal sides, real chess agrees with the model's "passer wins" in 65 of 72 (textbook tree), mostly at 7-8 men.

## 2. Status of the original candidate W a2 c2 / B b7 d7 (8 men; 8/1p1p4/8/5Kp1/6Pk/8/P1P5/8)
- **Model:**
  - Textbook: *2 under count and mover (e.p. on and off); 0 under opponent.
  - E.p.-aware: {2±1 | -2±1} under count and mover; 0 under opponent; *2 with e.p. off.
  - These reproduce the A2-realchess numbers exactly.
- **Real root: outcome N.** The A2 certificates (30 and 40 nodes) re-verify offline here.
- **Root move tables:**
  - Black to move (from A2): only 1...b5 wins.
  - White to move:
    - 1.c4 wins (from A2), and all king moves lose (from A2).
    - **New: 1.a3 and 1.c3 lose.** Black to move wins in both 8-man positions, checked two ways (search, and an independent prover with ≤7-man leaves, 16 nodes each).
    - 1.a4 is still unresolved after 23 requests.
  - The real table agrees with the count/mover prediction at every resolved move.
- **Oracle value:**
  - **E.p.-aware tree:** *2 is excluded under every treatment, including "free". I re-checked this independently with the direct minimax: lower and upper tests both hold on A2's data, with supports of 13 and 12 terminals. So this is now checked two ways.
  - **Textbook tree:** "free" does not exclude *2 (confirmed). A2's exclusion under the switch treatments, by enumeration, was not re-checked here.
  - **"White must win":** {2±1 | -2±1} in both trees (from A2, computed once).
  - **"Draw = 0" (e.p.-aware):** still between {2±1 | -2±1} and {5/2±3/2 | -2±1}. 100 requests spent on its 4 essential 8-man sides resolved none.
- **Verdict:** the textbook *2 does not survive real chess, and this does not answer Elkies' question.

## 3. Budget
- **Total:** 863 requests of my 1,200 (ledger realchess/certify/logs/ledger.jsonl); 863 HTTP 200, no 429s. The shared ledger stays at 1,199.
- **By tag:** iterate 440, realproof 200, A2-resolve 127 (original), resolve-list 56, oracle10 16, races 14, verify 9, test9 1.
- **Lichess at 9 men:** it returns "unknown" for every move of a 9-man position (one probe: 8/8/8/5Kp1/Ppp3Pk/P1P5/8/8 w). Beyond 8 men, only searches down to 8 men work.
- **Wasted spend:** 100 requests on the original's draw-0 sides and about 240 on unconditional attempts for candidates 3-5 produced no certificate.
- **Unspent:** 337 requests.

## 4. New tools (realchess/certify/; existing code untouched)
| File | What it does |
|---|---|
| `infra.py` | Prober that writes only to certify/cache with its own ledger, holds the shared lock read-only, and keeps a KB over all caches |
| `run.py` | Runs realchess stages with that plumbing |
| `tree_stats.py` | Race sensitivity and pinning race sets |
| `races.py` | Real results of the decisive races |
| `oracle10.py` | Resolve terminals; bounds under each fill policy |
| `search9.py` | Searcher that handles ≥9 men; optional l8 |
| `iterate.py` | Adaptive exclusion loop |
| `need.py`, `pinneed.py` | Planning for exclusion and for pins |
| `certify_check.py` | CGT + direct minimax certificate, minimal support, `--oracleall` |
| `verify_sides.py` | Re-proves each support side two ways |
| `support_bound.py` | Bound with only the support fixed |
| `strategy.py`, `strategy_kings.py` | White's strategy; Black king moves along it |
| `realproof.py` | Attempt at a full real-chess root proof |
| `resolve_list.py` | Resolves listed terminal sides |
| `sf_eval.py`, `sf_batch.py` | Stockfish evidence |
| `termdb.py` | `realdb.jsonl`, real results keyed by FEN |
| `summary.py` | Writes `results/certify_summary.json` |

Notes:
- To run: `source realchess/certify/env.sh` defines `tb` (textbook: cd $R, PYTHONPATH=$R) and `ea` (e.p.-aware: cd $EP, PYTHONPATH=$EP:$R).
- Background jobs go through `bg.sh`.
- Every online command is cache-first, so re-running any of them now costs no requests.

## 5. Caveats
- **King moves:** the oracle value ignores them. Candidate 2's king moves are covered by the engine only.
- **One model:** the tree is built from one model implementation (cylcgt rules). The direct minimax re-checks only the CGT inequality, not the tree.
- **Conditional results are not certificates.** The model fill for 9-man terminals is an assumption, and candidate 4 shows that it can flip the answer.
- **l8 categories** are trusted only in labelled runs. Candidate 2's certificate holds without them.

## Claims

| id | importance | worker status | adversarial verification | statement |
|---|---|---|---|---|
| C1 | headline | checked-two-ways | not verified | Candidate W a3 b3 c2 / B b5 b7 c6 embedded as 8/1p6/2p5/1p3Kp1/6Pk/PP6/2P5/8 (legal, 10 men, kings and pawns only): in both the textbook and the e.p.-aware pawn tree, the real-chess oracle value G satisfies G >= G_lo = {0 \| {0 \| -2, -1±1}} > 0. This holds for every assignment of games in [-2BIG,+2BIG] to the 1,698 terminals that are not certified, so G is not *2 (and not 0). The support is 5 terminals (10 sides, 7-8 men) that are tablebase-certified White wins with either side to move: W a3 b5/B c5; W b3 b6/B b4; W b5 c4/B c5; W b3 c4 c5/B b5; W b3 c5/B b4 b5 (ep b6). No Lichess 8-man category is used. King moves are outside the tree. |
| C2 | headline | computed-once | not verified | No candidate is certified *2 as an 8x8 king-and-pawn position. Elkies' question (a *2 from kings and pawns only on 8x8) remains open. |
| C3 | key | checked-two-ways | not verified | Original W a2 c2 / B b7 d7 (8/1p1p4/8/5Kp1/6Pk/8/P1P5/8): in the e.p.-aware tree its real-chess oracle value is not *2 under any treatment. With every non-L/R terminal free on A2-realchess's resolved data, both the lower test (support 13 terminals) and the upper test (support 12) hold. In the textbook tree the free treatment does not exclude *2. |
| C4 | minor | checked-two-ways | not verified | Original candidate, White to move at the root: 1.a3 and 1.c3 lose; Black to move wins in 8/1p1p4/8/5Kp1/6Pk/P7/2P5/8 b and in 8/1p1p4/8/5Kp1/6Pk/2P5/P7/8 b. 1.a4 is unresolved after 23 requests. Together with A2: 1.c4 is the only winning White move found, and the king moves lose. |
| C5 | key | computed-once | not verified | Candidates 3, 4 and 5 are *2 in the model only under the race rule 'opponent'. Their *2 is pinned by 5, 3 and 3 race entries of 6-7 men. The tablebase contradicts the opponent verdict at 3/5, 2/3 and 2/3 of them; candidate 2 also has 3/5. Their real-chess oracle values are undetermined: certifying them needs 9-man terminals, which are beyond the tablebase. Pinning candidate 4 needs 32-63 terminals, 15-34 of them with 9 men. Two 8-9-man sides stayed unresolved after 188 requests. |
| C6 | key | computed-once | not verified | Conditional only, not a certificate. Take the unresolved one-sided terminals as wins for the passer's owner, and leave the unresolved races free. Then *2 is excluded for candidate 3 under the three switch treatments, for candidate 4 under the switch treatments, and for candidate 5 under all four treatments (e.p.-aware tree). These fill-based values are unstable: for candidate 4, with 34-35 resolved sides and races filled by the count rule, the value was exactly *2 under 'draw = White win' and 'draw = 0' in both trees. 18 further 6-7-man sides moved it to non-*2 games. |
| C7 | minor | computed-once | not verified | Candidate 6, W a3 b2 d3 / B a6 c7 d6: *2 only under mover with e.p. off. With e.p. on it is not *2 under count, mover or opponent, under either passed test. Its races reach 9-10 men, so the real-chess oracle was not attempted. |
| C8 | key | computed-once | not verified | No candidate has a king-and-pawn embedding of 7 men or fewer. The trebuchet takes 4 men, and in the flat-8 census every *k (k>=2) under any of the 9 settings has 4 or 6 pawns. The original is the only 8-man candidate; the other five have 10 men. |
| C9 | key | conjecture | not verified | Engine evidence only (Stockfish 19, 1 thread, 60 s, depth 36-41, no tablebases). Candidates 2, 3 and 6 look like outcome L at the root (White wins with either side to move), which is incompatible with *2. Candidates 4 and 5 look like N. |
| C10 | minor | conjecture | not verified | Candidate 2, real-chess side conditions: - Black king moves: all 62 positions after a Black king move in White's strategy tree evaluate as White wins for the engine (34 mate scores, mate in 11-19; the rest >= +7.61; 5 s each, depth >= 32). - Zugzwang nodes: 4 of the 8 nodes where Black has no pawn move are tablebase/search-confirmed White wins (7, 7, 8, 8 men). The three 9-man ones are unresolved. - Full proof: the real-chess proof of the root (Black first) is incomplete, with 12 of 15 leaves open after 200 requests. |
| C11 | minor | computed-once | not verified | Lichess returns category 'unknown' for a 9-man position and for every one of its moves, including captures into 8 men. Its 8-man categories carry dtz=1 and dtc=null, consistent with a look-ahead into the 7-man tables. |
| C12 | minor | computed-once | not verified | Original candidate, draw counted as 0 (e.p.-aware): the value is still only bounded between {2±1 \| -2±1} and {5/2±3/2 \| -2±1}. 100 requests on its 4 essential 8-man sides resolved none of them. |

### How to reproduce each claim

- **C1**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m realchess.certify.certify_check --component "W: a3 b3 c2 / B: b5 b7 c6" --no-l8-rows --sanity 10 --out realchess/certify/results/comp_Wa3b3c2_Bb5b7c6_cert_textbook_nol8.json ; PYTHONPATH=. .venv/bin/python -m realchess.certify.support_bound realchess/certify/results/comp_Wa3b3c2_Bb5b7c6_cert_textbook.json lower ; PYTHONPATH=. .venv/bin/python -m realchess.certify.verify_sides realchess/certify/results/comp_Wa3b3c2_Bb5b7c6_cert_textbook.json --max-new 0 ; e.p.-aware: same commands with cwd=$EP and PYTHONPATH=$EP:$R (EP=/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt), files *_cert_epaware*. The data came from: realchess.certify.iterate --component "W: a3 b3 c2 / B: b5 b7 c6" --cap 1200 --max-new 100 --per-side 20 --ext 6 --use-l8 --race-prior count --out realchess/certify/results/comp_Wa3b3c2_Bb5b7c6_iterate_tb_l8.json
  ```
- **C2**:

  ```
  See C1, C3, C5, C7.
  ```
- **C3**:

  ```
  cd $EP && PYTHONPATH=$EP:$R $R/.venv/bin/python -m realchess.certify.certify_check --component "W: a2 c2 / B: b7 d7" --sanity 20 --oracleall $R/realchess/results/comp_Wa2c2_Bb7d7_oracleall_pure_epaware_offline.json --out $R/realchess/certify/results/comp_Wa2c2_Bb7d7_cert_epaware_from_A2.json ; textbook: cd $R && PYTHONPATH=. .venv/bin/python -m realchess.certify.certify_check --component "W: a2 c2 / B: b7 d7" --oracleall realchess/results/comp_Wa2c2_Bb7d7_oracleall_pure_textbook_offline.json --out realchess/certify/results/comp_Wa2c2_Bb7d7_cert_textbook_from_A2.json
  ```
- **C4**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m realchess.certify.run solve_candidate resolve --component "W: a2 c2 / B: b7 d7" --cap 1200 --max-new 45 --per-target 15 --ext 4 --fen "8/1p1p4/8/5Kp1/6Pk/P7/2P5/8 b - - 0 1" --fen "8/1p1p4/8/5Kp1/P5Pk/8/2P5/8 b - - 0 1" --fen "8/1p1p4/8/5Kp1/6Pk/2P5/P7/8 b - - 0 1" --out realchess/certify/results/comp_Wa2c2_Bb7d7_root_white_children_resolve.json ; PYTHONPATH=. .venv/bin/python -m realchess.certify.run verify_proof "8/1p1p4/8/5Kp1/6Pk/P7/2P5/8 b - - 0 1" --claim win --kb --depth 30 (and the same for the 2P5/P7 FEN)
  ```
- **C5**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.certify.tree_stats --component "<C>" --ref-rule opponent --out realchess/certify/results/comp_<tag>_tree.json ; PYTHONPATH=. .venv/bin/python -m realchess.certify.races --tree realchess/certify/results/comp_<tag>_tree.json --cap 1200 --max-new 15 --ext 4 --out realchess/certify/results/comp_<tag>_races_real.json ; pins: PYTHONPATH=. .venv/bin/python -m realchess.certify.pinneed --component "W: a3 b2 c2 / B: a4 b6 c5" --treatment "switch, draw = White win" --out realchess/certify/results/comp_Wa3b2c2_Ba4b6c5_pinneed2_tb_sww.json
  ```
- **C6**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.certify.oracle10 bounds --component "W: a3 b2 c2 / B: a4 b6 c5" --out realchess/certify/results/comp_Wa3b2c2_Ba4b6c5_bounds_tb_v3.json (e.p.-aware: cwd=$EP, PYTHONPATH=$EP:$R) ; history: realchess/certify/results/comp_Wa3b2c2_Ba4b6c5_pinneed_*_sww.json (*2) vs comp_Wa3b2c2_Ba4b6c5_pinneed2_*_sww.json (not *2)
  ```
- **C7**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.model_values --component "W: a3 b2 d3 / B: a6 c7 d6" --out realchess/certify/results/comp_Wa3b2d3_Ba6c7d6_model_values.json
  ```
- **C8**:

  ```
  python3 -c "import json;d=json.load(open('atlas/flat8/rerun/census_summary.json'));print([x['npawns'] for x in d['nimbers_k_ge_2_any_setting']])"
  ```
- **C9**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.certify.sf_batch realchess/certify/results/roots10_fens.txt realchess/certify/results/sf_roots10_movetime60s.json 60000 3
  ```
- **C10**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.certify.strategy_kings realchess/certify/results/comp_Wa3b3c2_Bb5b7c6_cert_textbook.json realchess/certify/results/comp_Wa3b3c2_Bb5b7c6_strategy_kings.json ; PYTHONPATH=. .venv/bin/python -m realchess.certify.sf_batch realchess/certify/results/c2_strategy_kingmove_children.txt realchess/certify/results/sf_c2_strategy_kingmoves_5s.json 5000 1 ; PYTHONPATH=. .venv/bin/python -m realchess.certify.realproof realchess/certify/results/comp_Wa3b3c2_Bb5b7c6_cert_textbook.json --first B --max-new 200 --per-pos 15 --ext 6 --use-l8 --out realchess/certify/results/comp_Wa3b3c2_Bb5b7c6_realproof_Bfirst.json
  ```
- **C11**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.probe --offline --cache realchess/certify/cache "8/8/8/5Kp1/Ppp3Pk/P1P5/8/8 w - - 0 1"
  ```
- **C12**:

  ```
  cd $R && PYTHONPATH=. .venv/bin/python -m realchess.certify.run solve_candidate resolve --component "W: a2 c2 / B: b7 d7" --cap 1200 --max-new 100 --per-target 25 --ext 6 --fen "8/3p4/Pp6/2P2Kp1/6Pk/8/8/8 b - - 0 1" --fen "8/8/8/5Kp1/1pPp2Pk/8/P7/8 w - - 0 1" --fen "8/3p4/8/PpP2Kp1/6Pk/8/8/8 b - - 0 1" --fen "8/3p4/P7/1pP2Kp1/6Pk/8/8/8 b - - 0 1" --out realchess/certify/results/comp_Wa2c2_Bb7d7_draw0_sides_resolve.json
  ```

## Bugs found

- realchess.search.Searcher.capture_child always probes the PARENT position. For a parent with 9 or more men Lichess answers 'unknown' for every move, so the stock Searcher cannot search through 9-man positions. I worked around it in realchess/certify/search9.py (DeepSearcher) without editing the original.
- realchess.solve_candidate's --ledger defaults to the shared realchess/logs/ledger.jsonl, so an online stage run without --ledger would spend the shared budget. realchess/certify/run.py forces this workstream's own ledger.
- Not a code bug: the conditional 'model-filled' oracle values are not monotone in the amount of data. For candidate 4, 18 more resolved 6-7-man sides turned a conditional *2 back into non-*2, so conditional exclusions must not be reported as certificates.

## Open questions

- Is the real 10-man root of candidate 2 won by White with either side to move (outcome L)? The engine says yes; the proof needs 9-10-man Black king-move refutations that tablebases of 7 men or fewer cannot reach.
- What are the real-chess oracle values of candidates 3, 4 and 5? They depend on 9-man terminals, and candidate 4 even reached *2 conditionally under draw-tolerant treatments before more data moved it away.
- Is there a legal king freeze with fewer than 4 extra men? Without one, every 6-pawn candidate stays at 10 men.
- How should draws be treated in a principled CGT model of chess (draw = White win, Black win or 0)? The answer for candidate 4 and the original depends on it.
- Original: does 1.a4 lose? What is the 'draw = 0' value (4 essential 8-man sides)?

## Next steps

- Decide whether to report candidate 2 as refuted at the oracle level (C1, checked two ways), and the other candidates as undetermined with conditional, fragile values.
- To settle 9-man terminals, build a dedicated exact solver (retrograde or proof-number search) for frozen-trebuchet king-and-pawn endings with queen promotion, or obtain an 8-man tablebase source. Lichess look-ahead stops at 8 men.
- For a real-chess root proof of candidate 2: write a Stockfish-guided proof-number search for the 12 open Black king-move positions (9-10 men). Each needs a capture sequence down to 8 men.
- Search for *2 candidates whose embeddings have 8 men or fewer: other freezes, wider boards, or cylinders where a freeze exists.
- With the A8 explicit-king models, re-examine the king-move assumption of the oracle tree.
