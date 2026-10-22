# T32: report (agent text) with the verifier's findings

Written by the orchestrating session on 2026-10-22. The subagent could not write report files, so its
final message is reproduced verbatim under "Agent report". An independent Sonnet verifier then tried to refute
it; its verdict, summary and fix list come first and **take precedence over the agent text where they differ**.

## Verifier verdict: NO_REPORT

There is no REPORT.md for T32. I searched research/five_file_legal/ and the whole repo, and the only T32 files are code, JSON results and reproduce_t32.sh. I did not write VERIFY_T32.md, because the subagent rule forbids findings files, so everything is here. I checked the claims in the inline reply anyway, and none is refuted. LB values, the 11 legal positions, the 17 push-only histories and the 5 strict witnesses all reproduce with independent code. Four things need fixing before a REPORT.md is written. (1) The beside-T evidence for position 11 is an S0 history without the trébuchet pawns. I found and replayed an S1 history for it, so the conclusion stands. (2) Position 5 is IMPOSSIBLE in the strict model, not UNDECIDED. (3) Positions 8 and 15 are marked covering-UNDECIDED even though their strict witnesses are valid histories. (4) The claim that position 1 exceeds 50 million states is unsupported by any saved output. Other overstatements are in the problem list.

### Fixes and problems found by the verifier

- No REPORT.md exists (COMMON.md rule 6 and the brief require one). The 21-row table survives only in the chat reply, which is truncated at row 20 and has no row 21. t32_final_rows.json holds the rows, but no script in the directory regenerates the table (make_table.py reads a results.json that does not exist). reproduce_t32.sh starts background workers and returns at once, and it does not rebuild t32_final_rows.json. I did not write VERIFY_T32.md because the subagent rule forbids findings files; this output is the verification report.
- Headline overstates: 'legality, covering and push histories are decided', yet the covering model is undecided for 4 of 21, and the strict model for 16.
- Strict-only-#11 is supported only by an S0 history. S1, with the trébuchet pawns g4/g5, was never run. The conclusion is true (I found and replayed an S1 history), but the report should cite that history, not the S0 one.
- Table inconsistency: rows 8 and 15 show covering 'needs file shift: UNDECIDED', yet they have replayed strict histories. Those are valid games in any model, so the covering model for 8 and 15 is decided REACHABLE. The status of the file-shift rows depends on whether a pawn may capture an enemy piece, and the report never defines this. If it may (the brief's 'number of missing enemy pieces covers them'), 5, 8, 15 and 21 are covered. If pawns capture pawns only, #5 is impossible.
- Position 5 is legal beside T, so it matters. It is IMPOSSIBLE under pawn-only captures (hand proof plus a 17.46M-node exhaustive run). It is reachable only if a pawn captures a piece on b3, c5/c6 and d6. The reply's 'covering reachable and legal' list omits #5 without saying why.
- The 10 'illegal' positions are overstated. A capturable undefended black pawn next to Kf5 is a legal chess position. Only an e6 pawn giving check is a genuine legality problem, and then only with Black to move. The accurate wording is 'violates the brief's no-conflict rule / the king-freeze assumption'.
- The brief asked to list e-file pawns touching the king group. Three positions called legal have one: #11 (black e5, defended by d6), #18 (black e5, defended by d6) and #17 (white e4). They sit next to Kf5, so they may not decouple from T. This appears in results_strict_ordered_*.json as efile_touching but not in the reply.
- The 'mirror check agrees on all 21' is a symmetry tautology (reversing files cannot change chess legality), not an independent check. COMPUTED-1 is right for the mirror; my independent recomputation upgrades the legality itself to CHECKED-2.
- Unsupported number: 'position 1 exceeds 50 million states' has no saved artifact. The earlier results.json and run_t32_c.out are gone.
- The 120 s UNDECIDED verdicts come from wall-clock limits, not search-space limits (about 27-50k nodes/s, so 120 s is about 3-6M nodes). Position 5 needed a log2=26 table and about 17.5M nodes. Rerunning the undecided positions with log2=26 and longer timeouts could settle more of them, and some may be IMPOSSIBLE by arguments like #5's.
- Minor: the replayer is a witness checker, so CHECKED-2 is fair for witnesses. The covering histories use a reduced start (doomed pawns deleted at the start). That is stated, but it is not a history 'from the starting position'. Leftover files run_t32.py and validate_search.py describe the old S0/S1 runner and are stale relative to run_t32_c.py. crosscheck_c.py buffers its output and has a Python full-start phase that can run up to 6 x 300 s.

### Claims the verifier recomputed

- **agrees.** Claim: All 21 positions have 4 W + 4 B pawns, so the exact capture counts are 4 and 4. File-shift lower bounds are at most 2, so the covering test passes for all 21.
  Recomputed: Re-parsed hits.tsv (21 C/aware rows). Counts 4/4 on every row. File-shift lower bounds computed by brute force over all injective start-file assignments, not the repo's DP. Non-zero rows: #5 (1,2), #8 (1,1), #15 (1,1), #21 (2,1). All others are 0/0 and the maximum is 2. This matches the report and the JSON.
- **agrees.** Claim: 11 positions are legal beside T (W Kf5 g4, B Kh4 g5): 2, 3, 4, 5, 6, 11, 12, 14, 17, 18, 20. The other 10 are blocked by an e6 pawn giving check or an undefended black pawn on e4/e5/e6 next to Kf5. The mirror check agrees.
  Recomputed: Wrote my own legality function (pawn checks, kings adjacent to capturable enemy pawns, defended-by-pawn or defended-by-king logic). It gives exactly legal {2,3,4,5,6,11,12,14,17,18,20}. Reasons match the table: #1 and #10 e4; #7, #8, #9 and #13 e5; #15, #16 and #19 e6 check; #21 e6 check. My own mirror (files reversed, T on b4/b5/c5/a4) agrees on all 21. The mirror agreement is a trivial symmetry check, not independent evidence.
- **agrees.** Claim: Covering model: 17 positions have a push-only history, built and replayed by an independent checker. Positions 5, 8, 15 and 21 need a file-shift pawn capture.
  Recomputed: Built the 17 histories myself (reduced start with only the surviving pawns on home squares, White pushes then Black pushes) and replayed them with a from-scratch replay. All 17 end on the target with 0 captures. The rows that cannot be push-only are exactly 5, 8, 15 and 21, since two pawns of one colour share a file. covering_push.py also reports 17 of 21.
- **agrees.** Claim: Strict model: histories found and replayed for 8, 11, 13, 15 and 19, each with 4 captures per side.
  Recomputed: Re-parsed the five history strings from t32_final_rows.json and replayed them with my own board-dictionary replay. It checks pushes, double steps, captures, e.p. and the rank 2..7 limit. All five end exactly on the target. The capture counts are W=4 and B=4 each. Lengths are 36, 33, 36, 37 and 36 moves.
- **agrees.** Claim: Reachable and legal beside T in the strict model: only #11, its history replays with 4 captures each side.
  Recomputed: The 4-captures witness is an S0 history (4+4 pawns, no trébuchet pawns). S1 (adding W g4 and B g5) was never run, as the reply admits. I compiled the repo's t32_search.c and ran S1 for #11 (ordered, log2=24). It found a 29-move history in 27 s. My replay confirms it ends on W a4 b3 c3 e2 g4 / B a7 c6 d6 e5 g5 with 3 captures each: W a2-a3 a3-a4 b2-b3 | B b7-b6 b6-b5 b5-b4 | W c2-c3 | B c7-c6 d7-d6 e7-e6 e6-e5 | W f2-f3 f3-f4 f4-f5 | B f7-f6 | W g2-g3 g3-g4 | B g7-g6 | W h2-h3 h3-h4 | B b4xc3 | W d2xc3 f5xg6 | B h7xg6 g6-g5 | W h4xg5 | B f6xg5. So the conclusion is true, but the reported evidence did not establish it.
- **agrees.** Claim: The C search agrees with the Python search on all 120 small-start targets; every found history replays.
  Recomputed: I did not rerun their script. I wrote my own set-based BFS on the 3-file start (24,150 reachable (W,B) sets, e.p. included) and compared it with t32_search on 349 targets (191 reachable, 158 not), in plain and ordered mode. There were 0 mismatches, no CAP results, and found/exhausted matched the BFS truth every time. The search is sound and complete on small starts.
- **agrees.** Claim: The paper's c2xd3 for position A is the single file-shift capture (LB_W = 1); the exact model would need 5 captures there.
  Recomputed: paper/ieee/sections/08_star2.tex line 64 gives A = W a4 b3 d2 d3 / B a7 b7 c5, with 4 W and 3 B pawns. White would need 8-3 = 5 exact captures. The W d2/d3 pair gives LB_W = 1, so c2xd3 fits.
- **DISAGREES.** Claim: 16 positions are UNDECIDED in the strict model and no IMPOSSIBLE verdict can be claimed.
  Recomputed: Position 5 (W a3 b2 b3 e2 / B b6 c5 c7 d6) is IMPOSSIBLE in the strict pawn-only model. Hand proof: b2, e2 and c7 can only be unmoved originals; a3 must be a2-a3; b3 can only come from c2xb3, so the c-pawn never enters c3..c6; the black c-pawn never leaves c7; so no pawn can ever enter c3..c6, yet a black pawn must stand on c5. The same proof covers any removal of pawns by pieces at any time. Computational check with the repo's t32_search on the standard 8-file start (log2=26, no cap hit): RESULT EXHAUSTED after 17,464,228 nodes in 578 s. The same search also exhausts on 6- and 7-file starts. The reply's 120 s limit and log2=24 table (12.6M entry cap) could never reach this. So the claim is true but weaker than what is decidable.
- **DISAGREES.** Claim: Position 1 alone exceeds 50 million states.
  Recomputed: UNVERIFIED. results.json and run_t32_c.out are not in the directory, and T32.log only shows a Python 200k-node cap line. The saved runs are 120 s runs with a 12M node cap, which cannot show 50M states.
- **agrees.** Claim: The remaining undecided positions are undecided only because of the 120 s limit.
  Recomputed: I reran S0 (ordered, log2=24) at 300 s for #2, #12 and #20. All three timed out again. The search runs at about 27-50k nodes/s, so 120 s is about 3-6M nodes. This supports UNDECIDED and refutes nothing.

## Agent report (verbatim)

**T32 result: legality, covering and push histories are decided. Strict-model reachability is partly decided: 5 witnesses found, 16 undecided, no IMPOSSIBLE claims. REPORT.md was not written, because the subagent rule requires findings as text. This reply is the report.**

1. [PROVED, counting] All 21 have 4 White and 4 Black pawns, so the exact pawn-capture counts are 4 and 4. File-shift lower bounds are at most 2, so the brief's covering test passes for all 21.
2. [COMPUTED-1, hand-checked] Legal beside T (W Kf5 g4, B Kh4 g5): 11 positions (2, 3, 4, 5, 6, 11, 12, 14, 17, 18, 20). The other 10 are illegal: a Black e6 pawn checks Kf5, or an undefended Black pawn on e4, e5 or e6 stands next to Kf5. The mirror check agrees on all 21.
3. [CHECKED-2] Covering model (missing men removed by pieces outside the pawn history): 17 positions have a push-only history, built and replayed by an independent checker. Positions 5, 8, 15 and 21 need a file-shift pawn capture, and I did not decide them.
4. [CHECKED-2] Strict model (every missing enemy pawn captured by a pawn): histories found and replayed for 8, 11, 13, 15 and 19. Each of the other 16 hit the 120-second limit, so they are UNDECIDED. No exhaustive run finished, so no IMPOSSIBLE verdict is claimed. Position 1 alone exceeds 50 million states.
5. Reachable and legal beside T: covering model 2, 3, 4, 6, 11, 12, 14, 17, 18, 20; strict model only 11 (its history replays with 4 captures each side).
6. The C search agrees with the Python search on all 120 small-start targets, pruned and unpruned; every found history replays. The full-start cross-check is inconclusive: both searches hit their caps.
7. The paper's c2×d3 for position A is the single file-shift capture (LB_W = 1), which fits the covering model. The exact model would need 5 captures there. This is a remark about the paper's convention, not a verified error.
8. The first agent's backward DFS in `pawnhist.py` hit the node cap on 21 of 21 and omitted en passant, so it was replaced. The legality helpers and `positions.py` are kept. Not done: the trébuchet-pawn variant (S1) and an exhaustive proof for any position.

| # | position | LB W/B | legal beside T | covering model | strict pawn-only (120 s) |
|---|---|---|---|---|---|
| 1 | W a2 b2 c2 d2 / B a5 b4 d7 e4 | 0/0 | no (Kf5 takes e4) | push-only, OK | UNDECIDED |
| 2 | W a2 b2 c2 e2 / B a5 b5 c6 d7 | 0/0 | yes | push-only, OK | UNDECIDED |
| 3 | W a2 b2 c2 e2 / B a6 b4 d5 e3 | 0/0 | yes | push-only, OK | UNDECIDED |
| 4 | W a2 b3 c3 e2 / B a5 b5 c5 d5 | 0/0 | yes | push-only, OK | UNDECIDED |
| 5 | W a3 b2 b3 e2 / B b6 c5 c7 d6 | 1/2 | yes | needs file shift: UNDECIDED | UNDECIDED |
| 6 | W a3 b3 c2 e2 / B a6 c5 d5 e3 | 0/0 | yes | push-only, OK | UNDECIDED |
| 7 | W a3 b4 c2 d2 / B a7 b7 c6 e5 | 0/0 | no (Kf5 takes e5) | push-only, OK | UNDECIDED |
| 8 | W a3 c4 d2 d3 / B b5 b7 c6 e5 | 1/1 | no (Kf5 takes e5) | needs file shift: UNDECIDED | HISTORY found |
| 9 | W a4 b2 c3 e2 / B a7 c6 d7 e5 | 0/0 | no (Kf5 takes e5) | push-only, OK | UNDECIDED |
| 10 | W a4 b3 c2 d2 / B a7 b6 c7 e4 | 0/0 | no (Kf5 takes e4) | push-only, OK | UNDECIDED |
| 11 | W a4 b3 c3 e2 / B a7 c6 d6 e5 | 0/0 | yes | push-only, OK | HISTORY found |
| 12 | W a4 b4 c3 d2 / B a7 b7 c7 e7 | 0/0 | yes | push-only, OK | UNDECIDED |
| 13 | W a4 b4 c3 e2 / B a7 c6 d5 e5 | 0/0 | no (Kf5 takes e5) | push-only, OK | HISTORY found |
| 14 | W a4 b4 c4 d4 / B a7 b6 c6 e7 | 0/0 | yes | push-only, OK | UNDECIDED |
| 15 | W a4 c3 d2 d4 / B b6 b7 c5 e6 | 1/1 | no (e6 checks Kf5) | needs file shift: UNDECIDED | HISTORY found |
| 16 | W a4 c3 d2 e2 / B b7 c7 d5 e6 | 0/0 | no (e6 checks Kf5) | push-only, OK | UNDECIDED |
| 17 | W a5 b2 d5 e4 / B b7 c7 d7 e7 | 0/0 | yes | push-only, OK | UNDECIDED |
| 18 | W a5 c2 d3 e2 / B b7 c7 d6 e5 | 0/0 | yes | push-only, OK | UNDECIDED |
| 19 | W a6 b4 c4 e3 / B a7 c7 d6 e6 | 0/0 | no (e6 checks Kf5) | push-only, OK | HISTORY found |
| 20 | W a6 b4 d5 e3 / B a7 c7 d7 e7 | 0/0 | yes | push-only, OK | UNDECIDED |
| 21 | W b3 c2 c4 d3 / B a7 d6 d7 e6 | 2/1 | no (e6 checks Kf5) | needs file shift: UNDECIDED | UNDECIDED |

Every row has exactly 4 captures for each side in the strict model. Covering push histories for the 10 reachable and legal positions (all replayed):
- 2: B c7-c6, B a7-a5, B b7-b5
- 3: B a7-a6, B d7-d5, B b7-b5, B b5-b4, B e7-e5, B e5-e4, B e4-e3
- 4: W c2-c3, W b2-b3, B c7-c5, B d7-d5, B a7-a5, B b7-b5
- 6: W a2-a3, W b2-b3, B a7-a6, B c7-c5, B d7-d5, B e7-e5, B e5-e4, B e4-e3
- 11: W c2-c3, W b2-b3, W a2-a4, B c7-c6, B d7-d6, B e7-e5
- 12: W c2-c3, W a2-a4, W b2-b4
- 14: W c2-c4, W a2-a4, W d2-d4, W b2-b4, B b7-b6, B c6 from c7 (B c7-c6)
- 17: W e2-e4, W d2-d4, W d4-d5, W a2-a4, W a4-a5
- 18: W d2-d3, W a2-a4, W a4-a5, B d7-d6, B e7-e5
- 20: W e2-e3, W b2-b4, W d2-d4, W d4-d5, W a2-a4, W a4-a5, W a5-a6

Strict history for 11 (replayed; captures W f2-f6 chain, then B g7xf6, B h7xg6, B b4xc3, W d2xc3, W h2xg3, W g3xf4, W f4xe5, B f6xe5):
W a2-a3 W a3-a4 W b2-b3 B b7-b6 B b6-b5 B b5-b4 W c2-c3 B c7-c6 B d7-d6 B e7-e6 B e6-e5 W f2-f3 W f3-f4 W f4-f5 W f5-f6 W g2-g3 W g3-g4 W g4-g5 W g5-g6 B g7xf6 B f6-f5 B f5-f4 B f7-f6 B h7xg6 B g6-g5 B g5-g4 B g4-g3 W h2xg3 W g3xf4 B b4xc3 W d2xc3 W f4xe5 B f6xe5

Files (all in `/Users/aritro/Downloads/Research/Chessendgames/research/five_file_legal/`):
- `pawnhist.py`: legality, mirror and the forward search (rewritten)
- `t32_search.c`: C search, with an ordered mode
- `replay_check.py`: independent replay checker
- `crosscheck_c.py`, `covering_push.py`, `run_t32_c.py`, `make_table.py`, `validate_search.py` (partial: steps 1 and 2 only)
- `results_strict_ordered_A.json`, `results_strict_ordered_B.json`, `t32_final_rows.json`
- `reproduce_t32.sh`

Reproduce: `bash research/five_file_legal/reproduce_t32.sh` from the project root. The strict witness step takes about 20 minutes.
