# Review of the delegated reports (Claude, 2026-10-21)

Every claim from an external agent is checked against data the project has already verified before it goes into
RESULTS.md or the paper.
- **Accepted:** consistent with that data, or re-checked here.
- **Rejected:** contradicted by a direct computation, shown below.
- **Pending:** not yet checked.

## T2: proof re-derivation (`verify_ext/qwen/`, kilo / Nemotron Ultra) — accepted, with one consequence

- 7 proofs VALID: L1.6, L2.1, L2.3, L3.3, L5.1–5.3, Theorem 1.14(i), Theorem 3.4.
- Theorem 2.7 VALID-WITH-REPAIR: the repair is the unlimited-pass condition (k = ∞).
- **Proposition 2.10(b) has a GAP.** The counterexample offered for "T ≥ 2 fails in some context" is a
  terminal position, because Black already has a passed pawn.
  - **Consequence:** the paper now states 2.10(b) as a conjecture (§kings).
  - **Follow-up:** construct a non-terminal context.
- Second-model status: these proofs now have one independent re-derivation, by a non-Claude model. A human read
  is still needed.

## T4: cylinder atlas under the e.p.-aware test (`atlas/cylinder/ep_aware/`) — partly rejected

- **Accepted** (consistent with the flat-board recompute):
  - 1,223,689 positions and 10,561 distinct values;
  - no \*k with k ≥ 2 anywhere;
  - the 4-file ring {3/2±1/2 | −3/2±1/2} becomes {2±1 | −2±1};
  - the 3-file ring values 3/4, −3/4 and 1/4±1/4 survive.
- **Rejected:** "0 outcome classes change".
  - Counterexample: `W a2 b3 / B b4` goes from +W (L) under the textbook test to 0 (P) under the e.p.-aware test,
    on F3, C3 and C4. Recomputed with cylcgt.
  - The flat census has 690 outcome changes with ≤ 5 pawns.
  - `analyze.py` never compares outcomes.
- **Pending:** the change counts of cylinder-only values (3-file 42→48, 4-file 13→8).

## T11: thermography and atomic weights (`research/thermo/`) — partly rejected

- **Rejected:** "atomic weight ±2 occurs only on 3-file cylinder rings (e.g. ⇑\*)". On one flat file,
  `W a2 / B a6` = ⇑\*, which is Elkies' 1996 example.
- **Rejected / inconsistent:** the summary says the maximum temperature without ±W is 3, but its own table lists
  5.5 on F3. One of the two is wrong; the textbook atlas has a maximum of 3 (`W a2 b4 / B a5 b7` = ±3).
- **Pending:** the atomic-weight implementation; check it on textbook values before using any number.

## T3: Elkies targets (`atlas/targets/final/`) — mostly rejected

- **Rejected:** tiny(1) "113 positions, 96 robust". The census has exactly 16 tiny(1) and 16 miny(1) under the
  e.p.-aware count rule. Its example `W a2 / B a6 a7` has value {−1 | {−1 | −5/2±1/2}}, not tiny(1).
  The tiny(2) row is a copy of the tiny(1) row. The value matching is broken.
- **Rejected:** "1/8 robust and reachable" for `W a2 a3 b2 / B a6 b5 b6`. This structure is unreachable: the
  a3 pawn can only come from b2, which is still occupied. The reachable 1/8 is its mirror,
  `W a2 b2 b3 / B a5 a6 b6` (atlas/flat8/rerun, with a hand-built capture history).
- **Accepted** (matches atlas/flat8/rerun):
  - 1/8 robust in 9/9 settings at one structure (and its mirror);
  - ↑²\* robust at `W a2 b2 b6 / B a6 b7 c5`;
  - no robust 1/16 or ↑².

## T7: referee review (`notes/ext_review_kilo/`) — accepted as advice

It is a synthesis with no new numbers. Its most-valuable-next suggestion is a dedicated 9-man solver for
candidates 3–5, plus integrating king moves into the oracle. Both are recorded as open problems.

## T1: independent re-check (`verify_ext/codex/`, Codex) — accepted

- A stdlib-only solver written from the rules; it imports none of `cylcgt/`, `sumtest/`, `lemmas/`,
  `crosscheck/` or `atlas/` (grep-checked).
- Agrees on all five headlines in all nine settings:
  - the textbook \*2 and its e.p.-aware value {2±1|−2±1};
  - 1/8 at `W a2 a3 b2 / B a6 b5 b6`;
  - {0,\*|↓} at `W a2 b2 b6 / B a6 b7 c5`;
  - no \*k with 2 ≤ k ≤ 292 among 793,299 labelled placements on widths 1–4.
- Re-run here: `selfcheck.py` gives 27 PASS (72 s).
- The birthday bound 292 (36 pawn moves + terminal 256) is correct for this model.
- **Consequence:** the headline values now have a non-Claude implementation (paper §methods).

## T10: KPK on the cylinder (`research/kp_tablebases/`) — per-position data accepted, summary statistics corrected

Check: `delegate/checks/kpk_crosscheck.py` (output in `kpk_crosscheck.out`). It enumerates every legal KPK
position, solves it with kpsolve (QRBN) and with the independent `atlas/cylinder/kpk` (Q only), and
compares the two.
- **Accepted:**
  - every kpsolve value in T10's result files is correct: cylinder 321,312/321,312 agree, flat 326,650 agree;
  - the 6 flat differences are rook-underpromotion positions that the Q-only solver cannot see;
  - 216 cylinder mutual zugzwangs.
- **Rejected — T10's generator** wrote every position where the pawn checks the black king with White to move
  (illegal) instead of Black to move. That drops 5,328 legal positions on the cylinder and 4,696 on the flat
  board.
- **Rejected — T10's percentages:** "WTM wins 76.35% (126,736/165,984)" divides by the Black-to-move count.
- **Correct figures (two solvers):**

  | board | White to move: legal | wins | Black to move: legal | wins |
  |---|---|---|---|---|
  | flat | 163,328 | 124,960 (76.51%) | 168,024 | 97,604 (58.09%) |
  | cylinder | 160,656 | 126,736 (78.89%) | 165,984 | 92,760 (55.88%) |

  - flat draw → cylinder win: 16,538 (T10: 16,518);
  - flat win → cylinder draw: 15,930 (T10: 15,282);
  - mutual zugzwangs: 160 flat, 216 cylinder.
- KPKP/KPPK: not done (T10 timed out). Still open.

## T6: ML on Dawson's chess (`ml/dawson/`) — accepted as a COMPUTED-1 negative result

The LSTM reaches 0.82 test accuracy on totals 31–80, against a majority baseline of about 0.79. Probes recover
win/loss of single strips but not Grundy values. Not re-run here. It does not affect any CGT claim.

## Killed at the free-model usage limit ("Too Many Requests") — relaunch needed

- **T12** (odd cylinders): a kpsolve9 vs kpsolve differential test had 0 differences on 20,000 positions per
  board. No REPORT.
- **T14** (Dawson variants): died in a 2-minute shell timeout. No REPORT.
- **T15** (novelty check): finished its research phase, then died while writing. No REPORT.
- **T8b:** validated its census (6,724 zeros, 4,042 stars, no \*2), then stopped while extending the scope (no error in the log).
