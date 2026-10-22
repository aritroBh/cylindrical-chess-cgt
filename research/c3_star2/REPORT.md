# T33: report (agent text) with the verifier's findings

Written by the orchestrating session on 2026-10-22. The subagent could not write report files, so its
final message is reproduced verbatim under "Agent report". An independent Sonnet verifier then tried to refute
it; its verdict, summary and fix list come first and **take precedence over the agent text where they differ**.

## Verifier verdict: ACCEPT_WITH_FIXES

All reported values reproduce with a third, freshly written solver, but one headline claim is wrong and REPORT.md was never written. The C3 root W a2 a3 b2 / B b7 c6 c7 is *2 and the C4 root W a4 b2 c2 / B b6 c5 d6 d7 is *2 in the default setting. All 18 root cells across the 9 settings match cylcgt and the C solver. The claim "the decisive capture is c5xb6 e.p." is refuted by e.p. ablation, run in two implementations: the *2 needs both B b4xa3 and W b5xc6, and c5xb6 is irrelevant. The "33 disagreements" are a harness artifact: every one is a root that already has a one-sided passed pawn, and with no passer at the root 162 of 162 comparisons agree. The brief's REPORT.md is absent. The walk-throughs exist only in the agent's message, and the appendix data is in appendix_moves.txt. I confirmed the walk-through inequalities (domination and reversal), the e.p.-position values, and the reachability results (C3 unreachable, C4 history legal in 7 plies with one capture and no passed pawn). Findings are in research/c3_star2/VERIFY_T33.md and scripts and outputs are in research/c3_star2/verify_t33/.

### Fixes and problems found by the verifier

- REPORT.md was never written, though the T33 brief names it as the deliverable (walk-throughs plus appendix). The walk-throughs exist only in the agent's chat message. Items 2 and 3 of the brief (why the value is 0 with e.p. off; why the mover and opponent rules give what they give) are answered with values only, not explanations.
- Substantive error: 'The decisive capture is c5xb6 e.p.' is refuted. Disabling c5xb6 leaves the root at *2, and allowing only c5xb6 gives 0. The root is *2 exactly when both Black's b4xa3 and White's b5xc6 e.p. captures are legal. Without b4xa3 the root is up-arrow, without b5xc6 it is down-arrow, and the two together give *2. Shortest histories are 1.a3-a4 b7-b5 2.a4-a5 b5-b4 3.a2-a4 b4xa3 (6 plies) and 1.a3-a4 c6-c5 2.b2-b4 c5-c4 3.b4-b5 c7-c5 4.b5xc6 (7 plies). Only the narrower statement that c5xb6 is the first capture where on and off values differ (ply 5) is true.
- For C4 the e.p. question was not examined. Ablation shows the root keeps *2 only if both Black captures b4xc3 and c4xb3 are allowed. Each is individually needed, those two alone suffice, and White's a5xd6 and c5xd6 are irrelevant.
- Xcheck item 7 (417/450, 'did not determine which implementation is wrong') is misleading as stated. All 33 disagreements are roots that already have a one-sided passed pawn. The cyl_eval --eval mode never tests the root, while pawns.value returns +-BIG at once. With no passed pawn at the root, 162/162 comparisons agree. The harness should have excluded those roots.
- Label audit. The inequality and reversal steps labelled CHECKED-1 can be upgraded to CHECKED-2, since the headline ones were re-derived independently (the omitted replacement-set reductions stay unchecked). Capture uniqueness in item 6 is PROVED by a material and file-multiset argument, not just COMPUTED-1.
- The '(e.p. b3)' and '(e.p.)' tags on b2-b4 and c2-c4 in both walk-throughs are engine artifacts: the engine attaches an e.p. marker to every double step, but in those positions no Black pawn can capture, so en passant is irrelevant there. The tags should be dropped. The quoted value 3/2+-1/2 for W a2 a3 c5 / B b5 c7 holds only with the e.p. right pending (ep b6), and the report omits the marker.
- Walk-through A skips a step: the a2-a4 option in the replacement set of the a4xb5 reversal is not dominated by 0 or * and needs its own reversal (via b5xa4). 'White's options reduce to 0 and *' is true because the final equality is checked independently, but the text does not show this step.
- Reproducibility nits: the ep_diff.py docstring command omits the argument 5, so the default MAXPLY=4 reproduces nothing and the saved log needs 5. claims_z.py and ep_line.py have no saved logs.
- All three programs (cylcgt, frontier.c, my solver) implement the same model (count rule, per-component e.p. right, first passer ends the game), so CHECKED-2 means the implementations agree, not that the model equals real chess. This is a caveat on the labels, not an error.

### Claims the verifier recomputed

- **agrees.** Claim: C3 root = *2 (count rule, e.p. on, e.p.-aware test)
  Recomputed: verify_t33/mysolve.py (own solver, shares no code with cylcgt or frontier.c): G+*2 is a P-position, nimber 2. Also reproduces cylcgt and the C solver (cyl_eval rebuilt from source).
- **agrees.** Claim: C3 value is 0 with e.p. off; mover rule gives 0 under every e.p. setting; opponent rule gives *2 incl. e.p. off
  Recomputed: My solver gives 0 (count, e.p. off), 0,0,0 (mover: aware, textbook, off) and *2,*2,*2 (opponent). Matches settings.log and the C tsv.
- **agrees.** Claim: C4 root = *2 under count, mover and opponent with e.p. on; not a nimber with e.p. off under any rule (18/18 root cells agree with the C solver)
  Recomputed: My solver: *2 in all six e.p.-on cells (aware and textbook). With e.p. off there is no *k for k<16 under count, mover or opponent. The re-run C solver output is identical to eval_cyl_out.tsv.
- **agrees.** Claim: First e.p.-on/off difference is at ply 5 (c5xb6); in W a2 a3 c5 / B b5 c7 the value is 3/2+-1/2 on and 1* off; a5xb6 changes nothing
  Recomputed: Earliest ply per e.p. capture type: a5xb6 and c5xb6 at 5, B a4xb3/b4xa3/c4xb3/c4xa3 at 6, W a5xc6/b5xc6 at 7. The position equals {2|1} with the e.p. right pending and 1* without it. The a5xb6 position is 0 on and 0 off.
- **DISAGREES.** Claim: The decisive capture is c5xb6 e.p. (the reason the root is *2 rather than 0)
  Recomputed: Ablation over the 8 e.p. capture types in the C3 tree (my solver and cylcgt with a patched moves()): all but c5xb6 gives *2; only c5xb6 gives 0; all but B b4xa3 gives up-arrow; all but W b5xc6 gives down-arrow; only B b4xa3 gives down-arrow; only W b5xc6 gives up-arrow; only {B b4xa3, W b5xc6} gives *2. Exactly the 64 of 256 subsets containing both give *2.
- **agrees.** Claim: Random cross-check: 417/450 agree; the 33 disagreements are decisive values in random positions; cause not determined
  Recomputed: Same positions and seed, split by whether the root already has a passed pawn: no passer at root 162/162 agree; passer at root 255 agree and 33 disagree. cylcgt scores such a root as +-BIG immediately; cyl_eval --eval calls solve() on the root with no passed-pawn test. Harness artifact, not an engine disagreement.
- **agrees.** Claim: C3 position cannot arise from pawns on ranks 2 and 7 (PROVED); C4 arises in 7 plies with one capture B a7xd6 via 1.d4 b6 2.d5 c5 3.d6 axd6 4.a4, no passed pawn en route
  Recomputed: Own BFS: C3 0 hits in 2971 states. C4 minimum depth 7, same history; all 7 moves legal in my generator; no passed pawn after any move under the aware test. One capture follows from material (8 pawns to 7), and the final Black files {b,c,d,d} force a7xd6.
- **agrees.** Claim: Walk-through A reductions: b2-b3/b2-b4 dominated by a3-a4; b7-b6/b7-b5 dominated by c6-c5; a3-a4 reverses via b7-b5 (replies b2-b3=* and a4xb5); a4xb5 reverses via c6xb5 where b2-b4 is 0; c6-c5 reverses via b2-b4 (b7-b6=*, c5xb4); c5xb4 reverses via a3xb4 whose reply b7-b5 is 0
  Recomputed: Outcome classes R,R,L (White) and L,L,R (Black), none is 0 or *. Q1<=G, P1<=G, V>=G and Z>=G all true by explicit sum tests. b2-b3 reply is *; both b2-b4 replies in P1 and Z are 0. Omitted replies of Q1 (a2-a3, a4-a5, b2-b4) are each <= a4xb5. V's b7-b5, c5-c4 and c7-c6 options are each >= the c5xb4 position. Gap: the a2-a4 option inside the a4xb5 reversal is itself reversible (via b5xa4) and the walk-through skips it.
- **agrees.** Claim: Walk-through B reductions: b2-b3=*, c2-c4=0, c2-c3 and b2-b4 dominated, a4-a5 reversible via b6-b5, c5-c4=0, d6-d5 reversible via a4xd5 (replies b6-b5=*, others >=*), b6-b5 reversible via a4xb5
  Recomputed: All confirmed: W01=*, W05=0, W02 and W04 <= *, a4-a5 not <=0 or <=* and Ya<=*2, c5-c4=0, Yd>=*2 with replies *, >=*, >=*, and Yb a white-passer position >=*2 with dominated replies.

## Agent report (verbatim)

T33 is done. I did not write `REPORT.md`, because the subagent rules here forbid report files, so the report content is below. The files are in `/Users/aritro/Downloads/Research/Chessendgames/research/c3_star2/`.

1. C3 `W a2 a3 b2 / B b7 c6 c7` = *2 under count, e.p. on, aware test. CHECKED-2 (cylcgt and the independent C solver agree on the root); reduction steps CHECKED-1.
2. With e.p. off the value is 0. CHECKED-2. The first e.p.-on/off difference is at ply 5: White's c5×b6 e.p. after 1.b2-b4 c6-c5 2.b4×c5 b7-b5. COMPUTED-1.
3. Mover rule gives 0 under every e.p. setting; opponent rule gives *2, also with e.p. off. CHECKED-2.
4. C4 `W a4 b2 c2 / B b6 c5 d6 d7` = *2 under count and under mover/opponent with e.p. on. With e.p. off it is not a nimber under any rule. CHECKED-2 (18 of 18 root comparisons agree with the C solver).
5. The C3 position cannot arise from pawns on ranks 2 and 7. PROVED: six pawns forces no captures, so Black's a-pawn stays on the a-file, which the target lacks. A breadth-first search agrees. COMPUTED-1.
6. The C4 position arises in 7 plies with one capture, B a7×d6. PROVED by the explicit history; capture uniqueness COMPUTED-1.
7. Random cross-check: 417 of 450 comparisons agree. The 33 disagreements are decisive (±W) values in random positions, not the roots. I did not determine which implementation is wrong.
8. All domination and reversal inequalities are engine-checked only (CHECKED-1). The C4 a4-a5 reduction is not hand-checked.

**Walk-through A (C3, *2).** None of White's moves is 0 or * directly. b2-b3 and b2-b4 are dominated by a3-a4. a3-a4 reverses through b7-b5: White's replies are b2-b3 (*) and a4×b5, worth {+W|{0|⇓*}}. That reverses again through c6×b5, where b2-b4 (e.p. b3) is 0. So White's options reduce to 0 and *. On Black's side, b7-b6 and b7-b5 are dominated by c6-c5. c6-c5 reverses through b2-b4: Black has b7-b6 (*) and c5×b4. c5×b4 reverses through a3×b4 to {⇑*|0}, whose reply b7-b5 is 0. So Black's options reduce to 0 and *, giving G = {0,*|0,*} = *2.

**Walk-through B (C4, *2).** White's b2-b3 is * and c2-c4 (e.p.) is 0. c2-c3 and b2-b4 are dominated by b2-b3. a4-a5 reverses through b6-b5, and the engine reduces what it leaves, but that step is not hand-checked. Black's c5-c4 is 0. d6-d5 reverses through a4×d5, and its reply b6-b5 is *; the other replies (⇑*, 1/2±1/2) are dominated by it. b6-b5 reverses through a4×b5 to +W, dominated by 0 and *. So G = *2.

**E.p. off.** The decisive capture is c5×b6 e.p. In the position W a2 a3 c5 / B b5 c7, the value is 3/2±1/2 with e.p. on and 1* with it off. The reversal chain that carries this to the root is not traced. The other capture at that depth, a5×b6, changes nothing.

**Reachability.** C3 cannot arise (PROVED, above). C4 arises by 1.d2-d4 b7-b6 2.d4-d5 c7-c5 3.d5-d6 a7×d6 4.a2-a4. The a7×d6 capture is the only capture event on any history to the target (COMPUTED-1, `captures.py`). No intermediate position has a passed pawn.

Files (in `research/c3_star2/`):
- Logs: `settings.log`, `appendix_moves.txt`, `chains_c3.log`, `chains_c4.log`, `ep_diff.log`, `reach.log`, `captures.log`, `xcheck_cyl.log`, `eval_cyl_out.tsv`
- Scripts: `walk.py`, `chains.py`, `settings.py`, `appendix.py`, `ep_diff.py`, `reach.py`, `captures.py`, `xcheck_cyl.py`, `claims_b.py`, `claims_z.py`, `claims_c4.py`
- `cyl_eval.c` is `research/star2_frontier/frontier.c` with `--eval` accepting `--cylinder`; that is the only change.
