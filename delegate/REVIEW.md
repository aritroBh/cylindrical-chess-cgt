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

## T31: odd-width paragraph (`notes/paper_drafts/odd_width.tex`). Accepted after checking.

Every number matches `research/odd_cylinders_verify/summary.txt`:
- 5,706 / 53.00% on C3;
- 16,008 / 65.87% / 208 zugzwangs on C4;
- 160,656 / 78.89% / 216 zugzwangs on C8;
- 79.41% and 79.94% for n = 9 and 10.

Rewritten into §X-A as Table VI plus the "Other widths" paragraph.

## T29 (first attempt): `notes/novelty2/REPORT.md` from the aborted aihubmix run. Not used.

It reads only repo text and runs no web searches, and it repeats the unverified Muller claim. The Kilo rerun
of T29 is pending.

## T26 (partial; Kilo stopped at its usage limit) and orchestrator follow-up: C6 nine-pawn rings

**T26's scans** (`research/star26_rings/*.summary.txt`, not pilots), default setting:

| Cylinder | Pawns | Rings | Default \*2 | Notes |
|---|---|---|---|---|
| C3 | 7 | 92,072 | 0 | |
| C3 | 8 | 235,720 | 4 | |
| C3 | 9 | 341,086 | 0 | Superseded: 470,832 after the scanner fix (below) |
| C3 | 10 | 372,595 | 0 | Superseded: 741,110 rings and 2 \*2 after the scanner fix (below) |
| C4 | 8 | 1,344,419 | 3 | One \*3, under opponent/e.p. off only |
| C4 | 9 | 4,890,628 | 0 | |

No \*k with k ≥ 3 in the default setting anywhere.

**C6, 9 pawns** (the n+3 prediction):
- **Splits 2+7, 7+2, 3+6 and 6+3** gave 0 \*2 (3+6 and 6+3 ran in the default setting only).
- **Split 4+5** (9,399,689 roots) failed in T26 and was run by the orchestrator in 4 chunks:
  - chunk 1 (6,121,447 roots) found 3 \*2 rings;
  - chunk 2 (456,170 roots) found 0;
  - chunk 3 has 0 roots;
  - chunk 0 (2,822,072 roots) segfaults in the scanner, even with a 64 MB stack. A Sonnet agent is fixing
    the bug (`research/star26_rings/BUGFIX_frontier_split1.md`).
- **Split 5+4** is the color reversal of 4+5 and has the same \*2 count.
- **cylcgt** (`delegate/checks/c6_star2_*.txt`) confirms all 3 hits as \*2 on C6 (count, e.p. on, e.p.-aware):
  - `W a4 c4 d2 e2 / B b6 b7 d6 e5 f6`;
  - `W a5 b3 d4 e2 / B c6 d7 e6 e7 f7`;
  - `W a5 c4 d4 e3 / B b7 d7 e4 e6 f7`.

  These values are CHECKED-2.
- **Conclusion:** with no ring \*2 on C6 up to 8 pawns (C1), the first ring \*2 on Cn has n+3 pawns for
  n = 3, …, 6. The minimality is C1. Paper §VIII and open problem 3 are updated.

## Scanner bug in `frontier_split1` (Sonnet agent; `research/star26_rings/BUGFIX_frontier_split1.md`). Accepted.

**The bug.** `solve()` held a pointer into the memo table across its recursive calls. A nested call could grow
the table and free the old one, so the later store wrote into freed memory. A second bug: `iw[8]`/`ib[8]`
overflowed for a side with 9 pawns.
- The orchestrator read the diff: the fix re-looks-up the slot just before the store and sizes the arrays 16.
- **Values were never wrong.** A lost store only drops a memo entry, which is recomputed. The fixed binary
  reproduces stored outputs byte for byte (C4 8-pawn 4+4; C6 chunks 1 and 2; one-line patches of the
  `star3_hunt` and `star2_width5` scanners reproduce their stored files).
- **What the bug did do.** It crashed runs, and the summaries of crashed runs read as "0 hits" (blank `rows`).
  Six such artifacts were found; blank `rows` with a log line `roots=0` are genuine empty splits, not crashes.

**Re-runs with the fixed binary** (`research/star26_rings/fixed_rerun/`):

| Run | Roots | Result |
|---|---|---|
| C6 p9 4+5, chunk 0 (32 sub-chunks; a second partition agrees) | 2,822,072 | 0 \*2, max nimber \*1 |
| C6 p9 5+4 (128 sub-chunks), default setting | 9,399,689 | 3 \*2: the color-reversed twins of the three 4+5 rings; outcome counts are the exact mirror of 4+5 |
| C3 p9 4+5 | 129,746 | 0 hits in all nine settings |
| C3 p10 5+5 | 205,280 | 2 \*2 in the default setting (twins of each other); \*3 in other settings, below |
| C3 p10 6+4 | 163,114 | 0 hits |
| C3 p10 1+9 and 9+1 | 2,681 each | 0 hits (the original 1+9 had 2,560 roots because of the array overflow) |

- **C6, 9 pawns, default setting:** exactly 6 ring \*2 (three and their twins), C1 for the count. cylcgt confirms
  the three 4+5 values (CHECKED-2). Paper §VIII updated.
- **C3, 10 pawns:** 741,110 rings, 2 default \*2: `W a2 a5 b2 b4 c2 / B a7 b5 b6 c4 c7` and
  `W a2 a5 b3 b4 c2 / B a7 b5 b7 c4 c7`. cylcgt gives \*2 for both, in the sum model and with splitting off
  (CHECKED-2). They do not change the six-pawn minimum on C3.

**\*3 on C3 with ten pawns (CHECKED-2; `delegate/checks/c3p10/`).** The fixed scanner and cylcgt, in the sum
model and with splitting off, agree on every case:
- count rule, e.p. off: `W a2 a3 b2 b3 c3 / B a6 a7 b6 b7 c6` and `W a2 a4 b2 b3 c3 / B a5 a7 b6 b7 c6`;
- opponent rule, e.p. on (textbook and e.p.-aware): `W a2 a3 b2 b3 c3 / B a6 a7 b6 c6 c7` and
  `W a2 a4 b2 b3 c3 / B a5 a7 b6 c6 c7`.

Each is its own color-reversed twin, up to the file symmetries of C3. All 14 nimber ≥ 2 hits of the 5+5 run
were recomputed, and cylcgt matches the scanner on each. No \*3 occurs in the default setting.

## Round 7 on Sonnet 5.5 / Haiku 5.5 (workflow `wf_8b421f7a`), each report checked by a Sonnet skeptic

Free providers were exhausted, so the eight pending briefs ran as Workflow agents. Subagents may not write report
files, so the orchestrator saved each final message with its verifier's findings first (the `REPORT*.md` files
named below). Seven verdicts were ACCEPT_WITH_FIXES; T32 was NO_REPORT, though the verifier refuted none of its claims.

| Task | Report | Outcome | Banked |
|---|---|---|---|
| T20b oracle for A, B | `research/star2_oracle/REPORT.md` | All 12 decisive 8-man end positions (24 sides) agree with the model. B's 14 sides are CHECKED-2 via the verifier's tablebase run. The bounds do not move: they are the trivial sandwich until 9–11-man sides are known. **B is A colour-reversed and mirrored**, so the two \*2 are one result up to symmetry. `apply.py` flip bug fixed. | Paper §VIII (mirror sentence), abstract, conclusion item 2 |
| T27 \*3, e.p. off | `research/star27_textbook3/REPORT.md` | 16 flat 6-file 8-pawn \*3 under count/e.p. off (8 up to colour reversal), confirmed by the scanner, cylcgt and the Codex solver. 12 are the candidate (\*2) plus a \* group. The aware test kills the count and mover ones. 122 opponent-rule cells are unchecked (C1). | Paper §VIII \*3 paragraph; T24 erratum |
| T30 proof audit | `notes/proof_audit2/REPORT.md` | Thm 3 GAP as printed (fixed in the paper); Prop 6 sound. The audit's "repo P2.10(a) H ≥ 5 false" is withdrawn: (L2) counts only the mover's pawns, which cannot be e.p.-capturable, so H ≥ 5 holds (kings session, 186d57a, exhaustive check). Six ranks are needed only for the either-colour form, so they are sufficient for Prop 6, not necessary.; Thm 8 sound with no sketch (added); Thm 10 sound with 2 minor gaps (fixed); Conj 4 follows from Thm 3 + Thm 10 with (E) (now a Corollary [AI]); Thm 21 needs one sentence (added). The "436,504 HSS positions" are samples, about 170k distinct. | Paper §IV, §V, §XI, intro; kings/ defects sent to the peer session |
| T34 ring minimum | `research/ring_min_independent/REPORT.md` | Independent C and Python solvers, plus the verifier's third solver and full cylcgt scans: C3 has no ring \*2 below 6 pawns (exactly 1 class at 6); C4 none below 7 (2 classes at 7, colour twins). | Paper §VIII ring minimum C1 → C2 |
| T29 novelty | `notes/novelty2/REPORT.md`, `VERIFY_T29.md` | \*2 on 8×8, n+3, KPK numbers: NOT FOUND elsewhere. KRK (cylinder) and KQK (torus) are known in prose; the HGM page says two bishops cannot mate, which our KBBK refutes. Elkies 1996 asks for a systematic e.p. treatment and constructs tiny-one with knights. T15 errors listed. | Paper: citations WikiCylinder and HGMCylinder, Elkies 1996 e.p. sentence, abstract wording |
| T33 C3 walk-through | `research/c3_star2/REPORT.md` | Both walk-throughs check out. Refuted: "c5×b6 decides". Ablation (two implementations, re-run by the orchestrator): the C3 ring is \*2 only with both B b4×a3 and W b5×c6 e.p.; without the first it is ↑, without the second ↓. C3 ring unreachable from the start; the C4 ring is reachable in 7 plies. | Paper §VIII e.p. sentence |
| T32 five-file legality | `research/five_file_legal/REPORT.md` | 11 of 21 sit beside T without conflict; 17 have push-only covering histories; strict-model histories for 8, 11, 13, 15 and 19 (an S1 history for #11 found by the verifier); #5 impossible under pawn-only captures. | No paper change (§IX's five-file \*2 is #6, legal) |
| T35 Möbius | `research/mobius/REPORT_T35.md` | KPK on the Möbius 8×8: 78.94% White-to-move wins (CHECKED-2, verifier's own solver). T9's pawn part ignored the seam, and its Part A counts are corrupted by a ray-array overflow (unverified). Corrected pawn values: 1,190/1,286 Möbius-only values, mostly ±BIG; 28/34 are BIG-free. | Paper conclusion item 5 |

**Review of the round-7 paper edits** (workflow `wf_f2d540b3`; 4 Sonnet lenses, one skeptic per finding; full
output in `delegate/checks/paper_review_r7.json`). 15 findings were confirmed and all were applied; 8 were rejected
as taste.
- **Overclaims fixed.** The abstract's bishop claim is now scoped to the cylinder and to opposite-colored bishops.
  The Corollary's BIG bound now matches Thm 10. Thm 3 now names X, the position with Z deleted, so the Corollary
  follows literally. The Dawson independence sentence is restricted to the game of whole sequences. The A/B
  twelve-end-position claim got a home in §IX with C1 and "queen promotions only". The Möbius board is defined.
  The abstract is back under 200 words.
- **New default-setting \*3 (found by the review, checked by the orchestrator).** Position A beside a one-file
  \* group, `W a4 b3 d2 d3 f4 / B a7 b7 c5 f6` on flat 6×8, is \*3 by cylcgt (sum and whole-board) and by the Codex
  solver (`delegate/checks/a_plus_star/`), so CHECKED-2: \*2 + \* = \*3 with nine pawns. Open problem 3 now asks
  for a single-component \*3, or one with fewer than nine pawns, in the default setting.

## C7 rings: \*2 at ten pawns and the first single-component default \*3 (orchestrator, round 9; in progress)

- **Scanner** (`research/star26_rings/c7/`, fixed2 build): about 200 of the 1,024 pieces of the 5+5 ten-pawn
  split are done. They give 63 roots of value \*2 and **8 of value \*3** in the default setting. Every \*3 root is
  a single component (cylcgt `components` gives 1). Example: `W a4 b2 d2 e2 f2 / B b3 c5 e4 f6 g7`.
- **Independent checks:**
  - T43's Codex-written solver agrees on all 62 hits it was given (57 \*2, 5 not \*2). With heaps up to 5 it
    gives \*3 for the two \*3 tested.
  - cylcgt whole-board gives \*3 for `W a4 b2 d2 e2 f2 / B b3 c5 e4 f6 g7`.
  - The scanner family's single-position evaluator (`research/c3_star2/cyl_eval`) also gives N,3.
  - In the sum model (splitting on) values can differ: that position is {0, \*2 | 0, \*} as a sum, while
    `W a2 a5 c4 e2 f2 / B a7 b4 d7 e5 g7` is \*3 in both models.
- **cylcgt cross-check of the first 15 \*2 hits (sum model):** 13 are \*2, one is the \*3 above, and
  `W a2 a6 b2 d3 f2 / B a7 c7 e5 e6 g4` is ↑\* as a sum. That one is \*2 as a whole board (T43, scanner); the
  cylcgt whole-board value is pending.
- **Pending:** all 8 \*3 through T43 and cylcgt in both models (`delegate/checks/c7_star3/`); minimality, i.e. no
  nine-pawn ring \*2 on C7, by the scanner (`c7/p9_*`) and by T43's solver (`delegate/checks/c7_epconv/enum9/`).
- **False alarm, recorded:** T43's 5 "disagreements" were \*3 lines, because the brief mislabelled the hits file.
  A re-run of piece c41 with both scanner builds reproduces N,3 exactly. The table-replacement change (fixed2)
  changes no value.

**C7 \*3 checks done (orchestrator).** All 8 ten-pawn \*3 rings found so far are \*3 in three programs:
- the scanner;
- T43's independent solver, extended to heaps up to 5 (`delegate/checks/c7_star3/t43_*.txt`): G + \*3 is a
  second-player win, and no other heap from 0 to 5 is;
- cylcgt as a whole-board game (`delegate/checks/c7p10/s3_*_nosplit.txt`).

As sums of components 6 of the 8 keep \*3; the other two are {0, \*2 | 0, \*} and {0, \* | 0, \*2}. Each \*3 is a
single component at the root. The paper (§VIII, intro, abstract, open problem 3) now states this as C2; open
problem 3 asks for a default \*3 with fewer than nine pawns, or a \*4 on eight ranks.
The ↑\*-as-a-sum ring `W a2 a6 b2 d3 f2 / B a7 c7 e5 e6 g4` is \*2 as a whole board (cylcgt), agreeing with the
scanner.

## T46 paper consistency audit (Kilo died at the sign-up wall; redone on Sonnet, `delegate/checks/t46_consistency_sonnet.json`)

20 findings were confirmed by skeptics and 3 rejected. One (open problem 3) was already handled by the C7 edit;
the other 19 are applied:
- the abstract now names the count rule, says "Tablebases" rather than "Four-man" (KRK has three men), and
  scopes "three programs" to the values;
- the intro says "with a legal pawn history" instead of "can arise in a game";
- the tiny(x) row is restricted to numbers x (tiny(1\*) does occur);
- the oracle definition now matches what was computed: N end positions are {+BIG | −BIG}, P ones are 0, and
  draws follow the draw treatment;
- labels: the n+3 sentence gets C1; the second candidate's oracle C2 → C1; the 1/8 proposition says "queen
  promotions only"; h ≈ 5–7 is Conj;
- the A/B history clause moved out of the C2 theorem ("checked by hand");
- A + \* is credited to two code bases, not three;
- engines: the conclusion no longer says the engines fail "on sums" by CGT class;
- the probe sentence now rests on the 0.82 versus 1.0 gap;
- odd widths: the zugzwang-share trend is stated from n = 4; the trébuchet and Ka3/Pa2/Ka5 claims are scoped to
  the widths checked (C2 to n = 8, C1 for 9–10); the a8=Q mate mechanism is corrected (a-file check);
- RESULTS 6b's "306 sides" is corrected to 302 (290 one-sided, 12 races).

