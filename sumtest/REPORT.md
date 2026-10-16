# Sum-test cross-validation of cylcgt (workstream sumtest)

Saved by the parent session from the workstream's final report (workflow `wf_3dfce063-f42`, 2026-10-16). The subagent harness does not let workflow agents write report files, so the text below is the agent's, unedited except for removing that notice.

**Convention note (added 2026-10-16).** These results use cylcgt as of commit 6b8ca2f, where a pawn that can still be taken en passant already counts as passed. The user has since chosen the e.p.-aware test (`PASSED_RESPECTS_EP = True`). Values that depend on a live e.p. right change under it, notably the \*2 candidate; see [RESULTS.md](../RESULTS.md).

## Headline

1. **My solver agrees with cylcgt on all 4,967,550 outcome predictions.**
   - I wrote a brute-force outcome solver from scratch (`sumtest/sumsolver.py`). It uses no canonical forms and imports neither cylcgt nor crosscheck.
   - The comparison covers 55,195 family positions × 3 race rules × e.p. on/off × 15 reference games X.
   - With e.p. on, the agreement requires my solver to use cylcgt's textbook passed-pawn test. With e.p. off, no extra assumption is needed.
2. **The *2 candidate holds only without en passant, or with a passed-pawn test that ignores a pending e.p. capture.**
   - Candidate: G = W a2 c2 / B b7 d7, 4-file flat board.
   - Under "count" and "mover", G+*2 is P (so G = *2) in two cases: with e.p. off, and with e.p. on under the textbook passer test.
   - Under an e.p.-aware passer test (a pawn the opponent can capture en passant on the next move is not yet passed), G+*2 is N, so G ≠ *2. The hybrid value is {2±1 | −2±1}: mean 0, temperature 2.
   - Under "opponent", G = 0 under every convention.
3. **Every disagreement found is a convention mismatch, not a coding bug.**
   - `cylcgt.pawns.passed()` never reads `pos.ep`, and `_child()` resolves passed pawns before the e.p. right can be used.
   - As a result, a pawn that double-steps past an enemy pawn wins at once, before the opponent's legal e.p. capture.
4. **OpenCode never ran.** All model routes failed; details are in Part 3.

## What I built (all in sumtest/)

- **Solver** (`sumsolver.py`).
  - For each pawn state it memoises two bitmasks over all R-tree nodes: "Left moving first wins" and "Right moving first wins".
  - The R games are explicit trees built from textbook definitions. up* and double-up* are explicit sums (up+*, up+up+*).
  - Fixed by the spec:
    - White = Left, normal play.
    - Single steps, double steps, and diagonal captures that wrap on a cylinder.
    - Optional en passant, including across the seam.
    - After a move, if exactly one side has a passed pawn, the sum is decided as ±BIG.
    - If both do, it is a race. Under "count" the mover's opponent moves first, fewer moves to promote wins, and ties go to the opponent. A passed pawn still on its home rank gets credit for the double step.
  - Flags for choices the spec leaves open (default first):
    - `ep_aware`: True = e.p.-aware test; False = textbook test.
    - `ep_scope`: an e.p. right lasts until the next move in G ("component"), or until any move anywhere ("global").
    - `mode`: "whole" means the first passed pawn anywhere ends the sum; "comp" means components split at every node and their ±BIG integers add.
- **Self-tests** (`test_sumsolver.py`): 15 tests, all passing.
  - Textbook outcome of every reference game.
  - Abstract identities, e.g. *2+*2 = 0, up+down = 0, 1/2+1/2−1 = 0, ±1+±1 = 0, tiny(1) < up.
  - Hand-checked positions: one-file W a4/B a6 = *, W a2/B a5 = up, W a2/B b3 = ±BIG.
  - Outcome does not depend on which tree represents a game.
  - Colour symmetry, cylinder rotation, flat reflection.
  - In comp mode, G + (−G) behaves like 0, with e.p. on and off.
- **Proof the solver was not tuned to cylcgt.** `HASHES_before_cylcgt.txt` holds SHA-256 hashes of `sumsolver.py`, `enum_positions.py` and `candidate.py`, taken before cylcgt was first imported. They still verify.
- **Two bugs in my own code**, found by the self-tests before any comparison and fixed before hashing:
  - A resolved +BIG state reported that Right also wins moving first.
  - A test helper used the wrong canonical form for double-up* ({0,up|0}; the correct one is {0|up}).

## Part 2(a): the candidate

Board: 4 files, flat, 8 ranks. Reference order: 0 * *2 *3 up down up* dup* 1/2 -1/2 1 -1 {1|0} +-1 tiny1. The outcome vector of *2 itself is NNPNLRLLLRLRLNN.

| Race rule | e.p. | G | G+* | G+*2 | G+*3 | Full vector | Value |
|---|---|---|---|---|---|---|---|
| count | off | N | N | P | N | NNPNLRLLLRLRLNN | *2 |
| count | on, textbook test (cylcgt) | N | N | P | N | NNPNLRLLLRLRLNN | *2 |
| count | on, e.p.-aware test | N | N | N | N | NNNNNNNNNNLRNNN | {2±1 \| −2±1} (hybrid) |
| mover | all three settings | identical to count | | | | | |
| opponent | off, or on with either test | P | N | N | N | PNNNLRNLLRLRNNL | 0 |

**What did not matter.** The vectors were the same in every one of these cases:
- whole vs comp mode;
- local vs global e.p. scope;
- 8-file flat or 8-file cylinder with files e–h empty;
- 5-file cylinder with the e-file empty.

**Race-node counts.**
- e.p. off: mine 224, cylcgt 224.
- e.p. on: mine 243, cylcgt 398. The difference is because cylcgt stores an e.p. flag after every double step; I store one only when a capture is possible. No value changes.

**Mechanism.** Take X = W a2 c2 / B b4 d7, White to move, and the move a2–a4.
- Textbook test: a4 has no black pawn ahead of it on the a- or b-file, and Black has no passed pawn. So the result is +BIG, and X = {256 | ±256}.
- Chess / e.p.-aware test: Black plays b4xa3 e.p. Black's a3 is passed and White's c2 is not, so the result is −BIG, and X = −3.
- I checked this two-ply argument by hand.
- It propagates to the root:
  - Black's 1...b5 is worth 0 under the textbook test but −2±1 under the e.p.-aware test.
  - By symmetry, White's c2–c4 is worth 0 against 2±1.
  - So the root changes from *2 to {2±1 | −2±1}.

**Interpretation.**
- In the passed-pawn = BIG model with e.p. off, G = *2; two implementations agree on this.
- With e.p. on, *2 survives only if a double step is allowed to win before the legal e.p. reply.
- So the A2 claim "*2 with or without en passant" depends on that convention. Unless the convention is justified, it should be withdrawn.
- No kings are modelled anywhere. An engine or tablebase check of the FEN should test the line ...b5–b4, a2–a4, bxa3 e.p.

## Part 2(b): every family position against cylcgt

**Families.**
- Boards: flat3, flat4, cyl3, cyl4, cyl5.
- Pawn counts (w,b) in {(1,1),(2,1),(1,2),(2,2)}; ranks 2–7; no passed pawn at the start.
- Positions: flat3 4,310; flat4 9,390; cyl3 6,210; cyl4 13,260; cyl5 22,025; total 55,195.

**cylcgt's prediction** for a position and X is `cgt.outcome(cgt.add(pawns.value(board, pos), X))`. `RACE_RULE` was set and `_value.cache_clear()` called for each rule. cylcgt gives the textbook outcome of every X on its own and raised no errors.

| My variant | Cases (position, rule) | Pairs (position, rule, X) | Cases differing | Pairs differing |
|---|---|---|---|---|
| e.p. off | 165,585 | 2,483,775 | 0 | 0 |
| e.p. on, textbook test (whole or comp, local or global scope) | 165,585 | 2,483,775 | 0 | 0 |
| e.p. on, e.p.-aware test | 165,585 | 2,483,775 | 13,176 | 109,157 |

**Cause of all 13,176 disagreements: the e.p. passer convention.**
- Switching only the passer test to textbook removes every one of them.
- All of them are `sum_safe` = True.

Minimal reproductions (3 files, flat, e.p. on):

| Rule | Position | cylcgt value | e.p.-aware value |
|---|---|---|---|
| mover | W a2 / B b4 | {+W \| ±+W} | 0 |
| count | W a2 b3 / B b4 | 257 | 0 |
| opponent | W a2 b2 / B a3 a4 | ±256 | −128±128 |

The same examples recur on the cylinders.

**How much the comparison actually tests.**
- **En passant generation, including across the seam.** Turning e.p. on changes the outcome vector in 6,764 cases under the textbook test, and cylcgt matches all of them.
- **Race counting.** Dropping the double-step credit from "count" changes 144 positions, and cylcgt agrees with counting it.
- **What the families cannot test:**
  - Local vs global e.p. scope gives identical vectors on every position, so these families cannot separate conventions for en passant inside sums.
  - Whole and comp mode are also identical everywhere. With at most 4 pawns there is never more than one component that can produce a passed pawn; two such components need 2+1+2 flat files or 6 cylinder files.

**Extra BIG-cancellation test** (`big_cancel.py`).
- 3,600 flat-5 positions with one W and one B pawn on files a–b and another pair on d–e; textbook test, "count".
- Comp mode agrees with cylcgt on 3,600/3,600.
- Whole mode differs from cylcgt on exactly the 100 positions cylcgt flags `sum_safe` = False, and agrees on all 3,500 flagged safe. Example: W a2 d2 / B b3 e3 is 0 in cylcgt but a first-player win when played out.
- So `sum_safe()` was exact on this family.

## Part 3: OpenCode (skipped)

About 15 minutes of probing, 23:00–23:19 CDT, opencode v2.0.25, prompt "Reply OK":

| Route | Result |
|---|---|
| omniroute/auto/* (best-coding, pro-coding, best-reasoning, coding:reliable, cheap) | `[400] Model is unavailable [oc/deepseek-v4-flash-free, oc/hy3-free, oc/north-mini-code-free]` |
| omniroute/aug/* (gpt5.5, kimi-k2.7, glm-5.2, gpt5.6-luna, gemini-3.1-pro-preview) and auto/glm | `Stream ended before producing a non-ping SSE event` (502) |
| omniroute/oc/big-pickle | Empty steps until timeout |
| omniroute/anthropic/claude-sonnet-5 | `No active credentials` |
| omniroute/oc/mimo-v2.5-free | 410, deprecated |
| opencode/*-free models | `Rate limit exceeded` |

The OmniRoute server itself answered `/v1/models` with HTTP 200. I did not try the separate aihubmix provider: it is not the OmniRoute route the task named, and it may bill.

**Ready for a rerun.**
- `opencode_spec.md`: the part-1 spec only, plus the required interface.
- `opencode_impl/opencode.json`: denies external_directory, webfetch and websearch; it parses.
- `run_opencode_impl.py`: runs test (a) plus a 500-position sample (seed 2026, × 6 rule/e.p. settings) against cylcgt and both of my variants. I validated it with `jsonl_adapter.py`: 3,006/3,006 lines agree with cylcgt, and 133 differ from the e.p.-aware variant, as expected.

## Limits on independence

- Both my solver and cylcgt were written by Claude models, so a misreading we share is possible.
- Before finishing the solver I read only README.md, RESEARCH_PLAN.md, notes/audit.md and the task. Afterwards, to classify the disagreements, I read cylcgt's docstrings and the source of passed(), moves(), _child() and sum_safe(). I never read crosscheck/.
- The e.p.-aware results come from one implementation only. Checks on them:
  - My brute-force vectors equal the outcomes cgt predicts from the hybrid values in every case shown.
  - The key two-ply line was checked by hand.
- The passed-pawn = BIG convention is assumed throughout.

## Reproduce

Run from `/Users/aritro/Downloads/Research/Chessendgames` with the prefix `PYTHONPATH=. .venv/bin/python`:
- `-m pytest -q sumtest/test_sumsolver.py`
- `-m sumtest.candidate`
- `-m sumtest.aware_value "W: a2 c2 / B: b7 d7" --files 4`, optionally with `--plain`, `--race mover` or `--no-ep`
- `-m sumtest.enum_positions --jobs 12 --epv off,plain,aware,plain-global,aware-global` (4 s)
- `-m sumtest.compare_cylcgt --jobs 12` (about 80 s)
- `-m sumtest.big_cancel`
- `-m sumtest.extra_checks`
- `-m sumtest.run_opencode_impl --impl sumtest/jsonl_adapter.py`

The data scripts skip outputs that already exist; delete `sumtest/data/*.gz` to recompute.

## Claims

| id | importance | worker status | adversarial verification | statement |
|---|---|---|---|---|
| C1 | headline | checked-two-ways | reproduce: confirmed; refute: confirmed; theory: partially-confirmed | My independent brute-force solver, using the textbook passed-pawn test, agrees with cylcgt on all 4,967,550 outcome predictions: 55,195 family positions x 3 race rules x e.p. on/off x 15 reference games X. With e.p. off the agreement is 2,483,775/2,483,775 with no extra assumption. |
| C2 | headline | checked-two-ways | reproduce: confirmed; refute: confirmed; theory: partially-confirmed | For W a2 c2 / B b7 d7 on a 4-file flat board, G+*2 is P (so G = *2) under race rules count and mover, both with e.p. off and with e.p. on under the textbook passer test. Full vector NNPNLRLLLRLRLNN, identical to *2's own. Under 'opponent', G+0 is P (G = 0) under every convention. |
| C3 | headline | computed-once | reproduce: confirmed; refute: confirmed; theory: confirmed | Under an e.p.-aware passed-pawn test (a pawn that can be captured en passant on the next move is not yet passed), G+*2 is N, so the candidate is NOT *2 under count or mover. Outcome vector NNNNNNNNNNLRNNN; the hybrid canonical value is {2±1 \| -2±1}, mean 0, temperature 2. The same holds with local or global e.p. scope, and on 8-file flat or cylinder boards with files e-h empty. |
| C4 | key | proved | reproduce: confirmed; refute: confirmed | Mechanism: in X = W a2 c2 / B b4 d7 with White to move, the textbook test scores a2-a4 as an immediate passed pawn (+BIG; X = {256 \| ±256}). In chess Black replies b4xa3 e.p., leaving Black a passed a-pawn while White's c2 is still blocked by d7 (-BIG; X = -3 under the aware test). Black's 1...b5 is worth 0 under the textbook test and -2±1 under the aware test. |
| C5 | key | checked-two-ways | not verified | All 13,176 (position, rule) disagreements (109,157 (position, rule, X) pairs) between my default e.p.-aware solver and cylcgt are one convention mismatch: cylcgt.pawns.passed() ignores pos.ep, and _child() resolves passed pawns before the opponent's legal e.p. capture can be played. None is a coding bug. All of them are sum_safe=True. |
| C6 | key | checked-two-ways | not verified | On 3,600 two-component flat-5 positions (one W and one B pawn on files a-b, another pair on d-e; textbook test; count rule), comp mode agrees with cylcgt on 3,600/3,600. Whole-board mode differs on exactly the 100 positions cylcgt flags sum_safe=False and agrees on all 3,500 flagged safe, with e.p. on and off. |
| C7 | minor | computed-once | not verified | The 2(b) families cannot test the e.p.-scope convention or BIG cancellation. Local and global e.p. scope give identical vectors everywhere, and so do whole and comp mode, because with at most 4 pawns two passer-capable components never occur. |
| C8 | minor | checked-two-ways | not verified | The comparison is sensitive to fine rule details. Switching e.p. on changes 6,764 of 165,585 case vectors under the textbook test. Dropping the double-step credit from the 'count' race changes 144 of 55,195 positions. cylcgt matches my choices in both. |
| C9 | minor | computed-once | not verified | Race-node counts for the candidate: 224 for both implementations with e.p. off. With e.p. on, mine is 243 and cylcgt's is 398, because cylcgt stores an e.p. flag after every double step (more distinct states). Values are unaffected. |
| C10 | key | computed-once | not verified | Part 3 could not run. Every OpenCode route failed non-interactively: omniroute auto/* returned 400 'Model is unavailable'; aug/* returned stream ended or 502; oc/big-pickle produced empty steps; anthropic had no credentials; the opencode free models were rate-limited. The spec, sandbox config and harness are ready. |

### How to reproduce each claim

- **C1**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.enum_positions --jobs 12 --epv off,plain,aware,plain-global,aware-global && PYTHONPATH=. .venv/bin/python -m sumtest.compare_cylcgt --jobs 12
  ```
- **C2**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.candidate
  ```
- **C3**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.aware_value "W: a2 c2 / B: b7 d7" --files 4
  ```
- **C4**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.aware_value "W: a2 c2 / B: b4 d7" --files 4 ; PYTHONPATH=. .venv/bin/python -m sumtest.aware_value "W: a2 c2 / B: b4 d7" --files 4 --plain ; PYTHONPATH=. .venv/bin/python -m sumtest.aware_value "W: a2 c2 / B: b5 d7" --files 4
  ```
- **C5**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.compare_cylcgt --jobs 12 ; PYTHONPATH=. .venv/bin/python -m sumtest.aware_value "W: a2 / B: b4" --files 3 --race mover
  ```
- **C6**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.big_cancel
  ```
- **C7**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.extra_checks
  ```
- **C8**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.extra_checks
  ```
- **C9**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m sumtest.candidate
  ```
- **C10**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames/sumtest/opencode_impl && opencode run --auto -m <model> "$(cat ../opencode_spec.md)" ; then from the root: PYTHONPATH=. .venv/bin/python -m sumtest.run_opencode_impl
  ```

## Bugs found

- cylcgt modelling defect (not a coding bug): pawns.passed() ignores pos.ep, so _child() declares a double-stepped pawn passed and ends the game before the opponent's legal en passant capture. This affects 13,176 of 165,585 (position, rule) cases in the families, and it is the reason the *2 candidate comes out as *2 with e.p. on. Minimal repro: 3-file flat board, e.p. on, rule mover, W a2 / B b4 has cylcgt value {+W | ±+W}, but 0 when the e.p. capture is respected.
- My own solver had two development bugs, both caught by self-tests before any comparison and fixed before the hashes were taken: (1) resolved +BIG states said Right also wins moving first; (2) a test helper used the wrong canonical double-up* ({0,up|0} instead of {0|up}).
- No coding bug found in cylcgt in the tested families. Its sum_safe() flag was exact on the extra 3,600-position BIG-cancellation family.
- Process: sumtest/REPORT.md was not written because the subagent harness blocks report files; its full content is in the summary field.

## Open questions

- Which passed-pawn convention should the project adopt with e.p. on: textbook (cylcgt) or e.p.-aware? The e.p.-aware test matches chess rules. I did not check how Elkies 1996 treats en passant.
- Does the candidate's line ...b5-b4, a2-a4, bxa3 e.p. occur with real kings in the proposed FEN 8/1p1p4/8/5Kp1/6Pk/8/P1P5/8? An engine or tablebase check is needed.
- Is there a *2 made of kings and pawns that survives under the e.p.-aware convention, or with e.p. irrelevant (for example, no double steps available)?
- The en passant inside sums question (local vs global e.p. right) is untested by these families; larger families are needed to separate the two.
- The second-model (OpenCode) implementation is still missing.

## Next steps

- Write sumtest/REPORT.md from the summary field (the subagent could not write report files).
- Decide the e.p. passer convention. If e.p.-aware is adopted, the cylcgt owner should add a flag, and RESEARCH_PLAN 1.3 should drop 'with or without en passant' from the *2 claim.
- Use the brute-force solver to search for *2 under the e.p.-aware convention: positions whose G+*2 outcome is P.
- Run an engine check on the critical e.p. line in the 8x8 embedding.
- Rerun Part 3 when an OmniRoute route works: one command with sumtest/opencode_spec.md, then sumtest.run_opencode_impl.
- Optionally rerun Codex's crosscheck/ on the e.p.-aware question to get a non-Claude second opinion.
