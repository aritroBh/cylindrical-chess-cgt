# Fixes to apply after wf_80655679 finishes (verified by Claude, 20:30)

1. 08_star2, Position A: "a7--a6 and b7--b5 are dominated" is wrong. Both are reversible: white's replies are
   worth 2 (after a7-a6, value {2|0}) and 3 (after b7-b5), both >= *2. They reverse out to nothing. c5-c4 gives
   white +BIG (d3xc4 frees the d2 pawn).
   Position B: "d2--d3 and c2--c4 are dominated" is also wrong. d2-d3 = {0|-2} and c2-c4 have black replies
   (-2 and -3) <= *2, so they are reversible too. a6-a5 = {{1*|*}|-W} reverses through {1*|*} to * (check).
   Candidate: "a2--a4 and d7--d5 (still to *) dominated or reversible": * is dominated by {3|1} for white. OK.
2. 12_engines: Lc0 is perfect at all four budgets, 10^3 to 10^6 nodes (233/233 best moves and evals), and it
   calls all 17 tablebase draws from 1k nodes on (kings session, engine/runs/lc0/analysis.md). The fact sheet says
   10^3 to 10^5.
3. 04_kings: kings/ is committed (3024df6). Cite only plain-PROVED items (T1.14(i), T3.4, C3.5) and computed
   results. Not "PROVED after repair".
4. 08_star2 five files: all three flat 5-file witnesses are CHECKED-2 at count/aware (cylcgt + Codex
   whole-board), see delegate/checks/star2_frontier_check{,2}.out. The draft says [C2]; OK.
5. Drummond-Cole: "needs officers" is backed by notes/lit_cgt_chess.md (full text read). OK.
6. T22 census not done: "exactly two" stays [C1]. OK as drafted.
7. 09_real, "Towards a real-chess 1/8": NEW RESULT (20:35). The 9-man kpsolve finished. All 6 sides of the three
   9-man end positions are exact and match the model. Bounds are now 0 <= O <= 1/8. The one open side is
   `W b2 b5 / B a5 b4`, Black to move (cap-2 run going). If it is a White win, O = 1/8 exactly. Queen-only
   promotion caveat stays. Prop. "Status of 1/8" and the abstract ("four decisive end positions remain") must
   be updated: "one decisive side remains".
8. 09_real, "the five-file witnesses have 12": only witness 1 (W a3 b3 c2 e2 / B a6 c5 d5 e3, the figure)
   sits cleanly beside the trebuchet. In witness 3 the black e6 pawn checks the king on f5. In witness 2,
   black e4 touches it (Kxe4 is legal). Say "the five-file witness of Fig. X has 12 men", and in 08 do not
   claim that every five-file witness embeds.
9. 04_kings / 13_verify, from kings/ commit 54d57b1:
   - K3 (one free model) checked the 17 "PROVED after repair" items: 13 sound, 4 downgraded to GAP (sharp
     T1.14, T2.7, P11, P12), none false. Any of these that the paper cites must be labelled "checked by AI
     models, human check pending". Not [P].
   - K2 (a non-Claude referee) recomputed every number in kings/REPORT.md and confirmed them all.
   - The 1.4M-position cross-check validates the solver, not the theory predictions. The predictions are [C1].
