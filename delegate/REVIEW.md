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

## T1b: second re-check (`verify_ext/omniroute/`, free model) — agrees, but not independent

It agrees on all five headlines and gets the same census count, 793,299. Its log shows it read
`verify_ext/codex/solver.py` and `selfcheck.py` before writing its own solver, so it is not counted as an
independent implementation.

## T13: engines on ChessSums (`engine/runs/chesssums/`) — accepted as COMPUTED-1, with the stated caveat

- On a 200-position subset, Stockfish 19 picks a move in the winning set 26.5–28.0% of the time (55, 53, 55, 56 of 200), from 1k to
  1M nodes; Lc0 does so 32.5–33.5% of the time.
- Both drop sharply with the number of components.
- The ground truth is the CGT model under a frozen king group with 15–20 men. "Wrong" engine moves are
  therefore wrong only relative to the model, not shown to be wrong in real chess. The report says this
  (§6).
- Not re-run here.

## T8: the \*2 frontier (`research/star2_frontier/`, Codex) — main finding accepted and re-checked

- **Accepted: \*2 returns with 7 pawns** under the paper's main convention (count rule, e.p.-aware test, e.p.
  on).
  - Positions: `W a4 b3 d2 d3 / B a7 b7 c5` and `W b4 c2 d2 / B a6 a7 c6 d5`.
  - Three solvers give \*2: T8's C solver, cylcgt on 4 and 8 files, and the Codex whole-board Python solver
    (`delegate/checks/star2_seven.out`).
  - Both are also \*2 under count/textbook, mover/textbook and mover/aware. They are not \*2 with e.p. off,
    nor under the opponent rule.
- **Accepted: 8-pawn hits.** Every T8 hit at count/e.p.-aware on flat boards of width ≤ 4 (2 with 7 pawns, 4 with
  8 pawns) is \*2 in cylcgt (`delegate/checks/star2_caware_check.out`). The three flat 5-file 8-pawn witnesses
  are \*2 in cylcgt. In the Codex solver, `W a3 b3 c2 e2 / B a6 c5 d5 e3` and `W a4 b3 c2 d2 / B a7 b6 c7 e4`
  are \*2 too (`star2_frontier_check.out`, which then hit its timeout). The third, `W a6 b4 c4 e3 /
  B a7 c7 d6 e6`, is \*2 in both as well (`star2_frontier_check2.out`). So all three are CHECKED-2 at
  count/aware.
  - The other DIFFER flags in `star2_frontier_check.out` are display formats (`{1 | 0, *}` = `{1|0,*}`;
    ⇓\* = {↓|0}) or the known sum-versus-whole-board difference (mover and opponent rules). None is at
    count/aware.
- **Not checked independently:** the claim "no other \*2" in T8's new scopes (5.5M + 2.2M roots). It rests on
  one implementation (COMPUTED-1). The old scope, ≤ 6 pawns, is CHECKED-2 (three implementations).
- **Mostly not robust:** the 14 C5-ring hits at count/aware are all \*2 on the 5-file cylinder (cylcgt, full
  run of `star2_caware_check.out`). On the flat 8-file board, 11 of them have other values. The other 3 stay \*2
  on the flat board, and they are the three flat 5-file witnesses above.
- **Explained: the opponent-rule "discrepancy" T8 reported.**
  - It is a difference of definition, not a bug: cylcgt adds up components (Elkies' sum model), while the
    Codex solvers end the whole game at the first passed pawn.
  - With splitting switched off, cylcgt equals the Codex solver on every disagreeing case tested.
  - Example: `W a3 b3 c2 e2 / B a6 c5 d5 e3` under opponent/aware is ⇑ as a sum of components and \*2 on the
    whole board.
  - The two models agree on every headline value: 1/8 and ↑²\* in all nine settings; the 7-pawn \*2 at
    count/aware.
- **Real chess:** these are model values. Their real-chess oracle values are open (milestone M4).

## T15: novelty and literature (`notes/novelty_check/`) — accepted with corrections

- **Accepted:** no published CGT of pawn endgames on cylinder or torus boards was found, and no tablebases for
  those boards.
- **Rejected / removed: the Muller claim.** It could not be located (T15 marks it UNVERIFIED). The paper no
  longer mentions it.
- **Mäser 2002** ("Global Threats in Combinatorial Games ...", More Games of No Chance) exists. Its pages still need
  checking against the volume.
- **Flagged:** T15 gives Elkies 2002 as pp. 1–21, but the volume lists pp. 61–78 (our bib). Re-check before
  submission.
- Its claims about what Elkies left open are not used without a source check.

## T12: odd-width cylinders (`research/odd_cylinders/`) — pending verification

- All claims are COMPUTED-1 by a free model, using kpsolve.
- Headline: parity of n does not affect the trébuchet or opposition for n ≥ 4, and on C3 every KPK position is a
  draw.
- It needs an independent check before any use (milestone M7). Its sweeping statement "direct opposition is
  always a draw" is suspicious.

## T25: skeptical re-check of T12, odd-width cylinders (`research/odd_cylinders_verify/`)

Accepted. Two of T12's four claims are refuted.

- **(a) Trébuchet:** CONFIRMED (CHECKED-2). It is a mutual zugzwang on every Cn×R with n = 4–9 and R = 5–8
  (84/84), and illegal on C3 (14/14 placements have adjacent kings).
- **(b) "Direct opposition is always a draw, diagonal a White win":** REFUTED.
  - On C8×8, of 4,288 direct-opposition triples, 984 are draws, 2,584 are White wins either way and 200 are
    mutual zugzwangs.
  - Orchestrator spot check (`kings/kpsolve --promote QRBN`): `Ka3 Pa2 ka5` is D/D on the flat 8×8 board but
    D (White to move) and W (Black to move) on cyl:8x8 and cyl:5x8, so it is a mutual zugzwang that exists only
    on the cylinder.
- **(c) "Every K+P vs K on C3 is a draw":** REFUTED.
  - White to move wins 53% of positions on C3×8.
  - Orchestrator spot check: `Ka1 Pa7 ka3` on cyl:3x8 is W, because a8=Q mates along the wrapped diagonals.
- **(d) No odd/even effect for n ≥ 4:** CONFIRMED (CHECKED-2) for n ≤ 10.
  - The statistics are monotone in n.
  - The only even-only effect is the opposite-file relation (d = n/2).
  - The n = 4 outlier is a 4-cycle effect.
- **Side result:** independently confirms the cylinder KPK rate of 78.89% (White to move), against T10's 76.35%.
  This is the correction already recorded under T10.

## T24: the \*3 hunt and the cylinder minimum for \*2 (`research/star3_hunt/`). Partly accepted.

- **Cosmetic bug in the scanner logs.** frontier_split's log line hard-codes "flat". The `cylinder_*` runs did
  pass `--cylinder` (`run_scans.sh`), and their values match cylcgt's cylinder values, not the flat ones.
  - Example: `W a2 a3 b2 / B b7 c6 c7` is 0 flat (cylcgt and Codex) and \*2 on C3 (cylcgt).
- **Incomplete splits.** T24 scanned only one split per pawn count. The orchestrator added every other 6- and
  7-pawn split on C3 and C4 (`research/star3_hunt_extra/`).
- **Result (default setting), the first ring \*2 on Cn:**

  | Cylinder | Pawns | Positions | Programs |
  |---|---|---|---|
  | C3 | 6 | `W a2 a3 b2 / B b7 c6 c7` | cylcgt and C scanner |
  | C4 | 7 | `W a4 b2 c2 / B b6 c5 d6 d7`, plus its color-reversed twin `W a4 b2 b3 d3 / B a7 c5 d7` | C scanner; the first also cylcgt |
  | C5 | 8 | the 14 known rings | known before T24 |

  - **Labels:** values CHECKED-2; minimality COMPUTED-1 (atlas ≤5 pawns + C scan).
  - **Pattern:** n+3 pawns for n = 3, 4, 5.
  - **Settings:** the C3 ring is 0 with e.p. off and 0 under the mover rule.
- **REJECTED: T24's "no \*3 under count or mover" headline.** Its own table shows \*3 under count/textbook
  and mover/textbook on flat 6×8 with 8 pawns (16 and 14 positions). The headline holds only for the
  e.p.-aware test.
  - These \*3s are unverified. They are probably e.p. artifacts, like the textbook \*2.
  - Next: verify one with cylcgt and Codex, and check its value under the e.p.-aware test.

## T17 and T18: outside fact and style reviews of the finished paper (`notes/ieee_review/`). Checked; one change.

### T17 (fact check)

**Its two "WRONG" walk-throughs are themselves wrong.** Recomputed with cylcgt at count/aware on 4 files:

| Position | Line | Value reached |
|---|---|---|
| A | d3–d4, c5×d4, b3–b4 | \* (`W a4 b4 d2 / B a7 b7 d4`), as the paper says |
| B | a6–a5, b4×a5, c6–c5 | \* (`W a5 c2 d2 / B a7 c5 d5`) |

For B, the intermediate values are {{1\*|\*}|−W} and then {1\*|\*}.

Its other items refer to text that no longer exists or are mistaken:
- "306 sides": the paper now says 302.
- "conditional only on the king freeze": gone.
- The minimax-winners sentence: already fixed.
- "2,483,775 is for one race rule": wrong. 55,195 × 3 × 15 = 2,483,775, all three rules.
- "every king move loses": supported by RESULTS.md row 30, checked two ways.

**Applied:** the abstract now reads "hinges on one side of one end position".

### T18 (style)

Its report mostly copies the old REVIEW_FINDINGS list. None of the phrases it quotes is still in the
sections, and its font claim is wrong (pdffonts shows NimbusRomNo9L, a Times clone).

**Real but up to the author:** the affiliation, city and country in the byline, which the repo does not
record.

## The 21 five-file \*2 positions: settled (orchestrator, 2026-10-22 00:50)

**Scan.** T21's scan of the ordinary 5-file board with 8 pawns finds 21 positions of value \*2 in the default
setting. All 21 use every file, and no two are mirror images.

**Sum model.** cylcgt agrees on 15 of the 21 and disagrees on 6.

**The 6 disputed positions** (`delegate/checks/w5_arbiter/`, `out_*.txt` and `nosplit_*.txt`) are \*2 in two
other programs:
- the independent whole-board solver (`verify_ext/codex`);
- cylcgt with component splitting switched off.

So the disagreement is the known sum-vs-whole-board difference.

**Result.**
- All 21 are \*2 as whole-board games: CHECKED-2, with scan completeness COMPUTED-1.
- 15 are \*2 as sums.
- The paper's three ring-derived positions are \*2 in both models.

**Paper:** §VIII-D rewritten; §IX no longer says "the one of the three".
