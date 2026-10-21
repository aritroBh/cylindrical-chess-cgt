# 5-line summary
- **Elkies *2 question (kings+pawns only on 8×8): still open.** The original candidate `W a2 c2 / B b7 d7` is not *2 in real chess under the adopted e.p.-aware convention; candidate `W a3 b3 c2 / B b5 b7 c6` (10 men) is refuted at the oracle level (G > 0 in both trees). The other 4 ten-man candidates remain undetermined; none embed in ≤7 men.
- **Convention change is decisive.** En passant-aware passed-pawn test (`PASSED_RESPECTS_EP=True`) kills the original *2 in the model ({2±1|−2±1} not *2) and matches real-chess oracle bounds; the old *2 survives only with the textbook (e.p.-ignoring) passer test.
- **Cylinder/tablebase work is solid.** 4-man tablebases on cylinder/torus verified by two solvers (607M values); cylinder *2 cannot be frozen on 8-file cylinder under enumerated ranges; paper re-audit found multiple errors in §7,8 and a small convention fix for §3.1.
- **Solver validated.** `cylcgt` agrees with an independent brute-force sumsolver on 4,967,550 outcome predictions; `sum_safe()` is a heuristic (replaced by hereditarily sum-safe) and e.p. scope inside sums has caveats.
- **Engines need larger sums.** Lc0 perfect on the CGT suite at 1k+ nodes; Stockfish shows class-based weakness at shallow depth on infinitesimals/nimbers but suite is tablebase-easy — the contrast requires ChessSums beyond 7 men.


## 1) Unverified / contradicted / overstated claims

| Claim | Status | Evidence / notes |
|---|---|---|
| Original *2 is robust under "with or without en passant" | **Overstated / false under adopted convention.** | `sumtest/`: under e.p.-aware passed test `G+*2` becomes N, value {2±1\|−2±1} (not *2). Mechanism: `b4xa3 e.p.` after `a2-a4` changes result. `realchess/`: e.p.-aware oracle excludes *2 under all treatments; textbook *2 excluded when draws count as wins for either side. ([RESULTS.md](../../RESULTS.md), [sumtest/REPORT.md](../../sumtest/REPORT.md) C2-C4, [realchess/REPORT.md](../../realchess/REPORT.md) C2-C4) |
| "Verified" status applied uniformly | **Needs qualification.** | RESULTS says "verified = two independent implementations agree and adversarial checkers could not break"; notes OpenCode route failed. Many headline numbers are **computed-once** or **checked-two-ways** on limited scope. Adversarial checkers were written by Claude models ([RESULTS.md](../../RESULTS.md)). |
| Cylinder *2/freeze claims | **Convention-dependent / not realizable on 8-file cylinder.** | No *k>=2 freezable on 8-file cylinder under enumerated range (0/40). Paper's cylinder trebuchet is mutual zugzwang only because of seam. Cylinder-only values not robust to race rule/e.p. ([atlas/cylinder/REPORT.md](../../atlas/cylinder/REPORT.md) C4,C7,C8). |
| Other *2 candidates (3-6) are real candidates | **Overstated / undetermined.** | *2 only under non-default race rule ("opponent") in most cases; tablebase contradicts opponent rule on decisive races (2/3-3/5). Real-chess oracle cannot be settled with ≤7-man tables; conditional fills flip (candidate 4 went *2 then non-*2). Candidate 2 refuted (G>0). ([realchess/certify/REPORT.md](../../realchess/certify/REPORT.md) C1,C5,C6). |
| Paper §8 (Dawson) is "correct" as stated | **Wrong / replaced.** | Move rule allows no first move; Grundy recurrence matches only at 31/300 (n<=300); cylinder outcomes wrong for 56 values. Replacement in `dawson/section8_corrected.tex`. ([RESULTS.md](../../RESULTS.md) §3, [dawson/REPORT.md](../../dawson/REPORT.md)) |
| Paper §7.2 king zugzwang is general | **Convention-limited.** | True only under convention; in real chess White to move draws with Kd5/Ke5/Kf5, only Black to move loses (confirmed by Lichess tablebase). ([RESULTS.md](../../RESULTS.md) §3) |
| Engine "solves suite easily" implies contrast is weak | **Potentially understated need.** | Stockfish/Lc0 do well on tablebase-easy suite; CGT-class effect seen at shallow depth for Stockfish (infinitesimals/nimbers worst). Real contrast needs larger sums beyond 7 men (ChessSums). ([RESULTS.md](../../RESULTS.md) §5) |

## 2) Decisive missing checks

| Gap | Why decisive | Suggested test |
|---|---|---|
| **Full independence of second implementation** | Many "checked-two-ways" share code paths (sumtest reuses cylcgt rules in places; adversarial checkers are Claude). OpenCode route failed. | Get a non-Claude implementation (Rust atlas planned) to recompute full value column (not just nimbers) on a large sample; run on disjoint codebase. ([atlas/flat8/REPORT.md](../../atlas/flat8/REPORT.md) C13/Open questions, [sumtest/REPORT.md](../../sumtest/REPORT.md) Limits) |
| **Real-chess proof for candidate 2 root / 9-man terminals** | Candidate 2 refuted at oracle level but full real-chess root proof incomplete (12 Black king-move positions 9-10 men unresolved; 1.a4 unresolved). | Use Stockfish-guided proof-number search down to 8-men tablebase; need 8-man/9-man coverage beyond Lichess look-ahead ("unknown" at 9 men). ([realchess/certify/REPORT.md](../../realchess/certify/REPORT.md) C10, Open questions) |
| **Settle candidates 3-5** | Depend on 9-man terminals; conditional fills are unstable (candidate 4 flipped). Race rule "opponent" contradicted by tablebase. | Need exact 9-man results (dedicated solver or expanded tablebase). Without this, cannot exclude/include *2 robustly. ([realchess/certify/REPORT.md](../../realchess/certify/REPORT.md) C5,C6) |
| **King moves in oracle tree** | Oracle ignores king resources; real king moves draw/win in places (6 proven draws, some best). | Integrate king-move analysis (kings/ models) into oracle; recheck candidates where king mobility matters. ([realchess/REPORT.md](../../realchess/REPORT.md) C8, [RESULTS.md](../../RESULTS.md) §1) |
| **e.p. scope in sums** | sumtest notes local/global e.p. scope identical in tested families (≤4 pawns) but theorem states sum exact only if no position with ≥2 components carries usable e.p. right (condition E). | Test multi-component positions with e.p. rights (the big_cancel family shows whole vs comp differs when sum_safe false; need cases with e.p.). ([sumtest/REPORT.md](../../sumtest/REPORT.md) Part 2b, [RESULTS.md](../../RESULTS.md) §4) |
| **Robustness across all conventions together** | Many "robust" claims tested subsets; cylinder-only values vanish under some race/e.p. setting. | Systematic 3×3 (count/mover/opponent × e.p. off/textbook/aware) on all candidates. ([atlas/cylinder/REPORT.md](../../atlas/cylinder/REPORT.md) C4, [atlas/flat8/REPORT.md](../../atlas/flat8/REPORT.md) C2,C6) |

## 3) Single most valuable next computation

**Compute exact real-chess results for all 9-man terminals needed by candidates 3-5 (and finish candidate 2's 9-10 man king lines).** 

Why: candidates 3-5 are the only remaining *2 claims not yet refuted; their fate turns on 9-man positions where Lichess gives "unknown" and tablebase ends. A dedicated 9-man solver (retrograde/proof search with queen promotion, leveraging 8-man tablebase at leaves) would resolve the question without guessing race rules or fill policies. This directly addresses Elkies' question with real chess.

## 4) Precise statement of what is and is not established about Elkies' question

**Established:**
- A *2 made *only* of kings and pawns on 8×8 is **not satisfied by `W a2 c2 / B b7 d7`** under the adopted e.p.-aware convention. Model value is {2±1\|−2±1} (not *2); real-chess oracle excludes *2 under all treatments and equals {2±1\|−2±1} when draws count as Black wins. Root is a win for side to move but not a *2.
- Within flat boards of ≤4 files and ≤6 pawns, **no candidate survives the e.p.-aware convention**; the original's *2 was an e.p. artifact. Three other *2s appear only under non-default settings.
- Candidate `W a3 b3 c2 / B b5 b7 c6` (10 men, trebuchet embedding) is **refuted at the oracle level**: G ≥ {0 \| {0 \| -2,-1±1}} > 0 in both trees for every terminal assignment.
- On cylinder/torus 4-man tablebases are solid; *2 cannot be frozen on 8-file cylinder in enumerated space.

**Not established:**
- Whether **any** *2 of kings and pawns exists on 8×8 remains open.** Candidates 3-5 (10 men) are *2 only under "opponent" race rule contradicted by tablebase; their real-chess values undetermined (need 9-man results). No 7-man-or-fewer embedding exists.
- The "draw = 0" / "Black must win" oracle values for original remain bounded but not pinned.
- Full real-chess proof for candidate 2's root strategy is incomplete.
- Robustness across all race/e.p. combinations for remaining candidates unproven.

**Bottom line:** Elkies' question is **still open**. The strong candidate was eliminated by the e.p.-aware passed-pawn convention; remaining candidates are either refuted or depend on unresolved 9-man real-chess results.

## 5) Paper outline (section titles + 2 lines each)

### Title (suggested)
*"Elkies' *2: Kings and Pawns on Flat and Cylindrical Chessboards"*

### Outline

**1. Introduction (1-2 paragraphs)**
- State Elkies' question (*2 position of kings and pawns only). 
- Outline scope: CGT model, conventions (passed pawns, e.p., races), flat/cylinder, real-chess certification.

**2. Conventions and Model (2-3 paragraphs)**
- Define Left/Right, normal play, BIG/passed pawns, race rules, **e.p.-aware passed test** (`PASSED_RESPECTS_EP`).
- Describe cylcgt API, disjunctive sums, king freeze assumption; note sum-safety caveats.

**3. Flat 8×8 Census (≤4 files, ≤6 pawns)**
- Report 231071 positions: only original *2 under textbook test; **none robust under e.p.-aware/count**. Document other targets (1/8, up-second*, tiny) and their robustness.
- Show e.p. artifact effect.

**4. Cylinder Boards and Freezes**
- 4-man tablebases verified; bishop-pair mate on cylinder contradicts Müller. 
- Show *2 cannot be frozen on 8-file cylinder; geometry prevents embedding. Paper trebuchet is seam-dependent zugzwang.

**5. Real-Chess Certification**
- Original candidate: root win for side to move but oracle value {2±1\|−2±1} in e.p.-aware tree, *2 excluded under all treatments; textbook *2 eliminated.
- Candidate 2 (10-man): **refuted** (G>0). Candidates 3-5: *2 only under opponent rule contradicted by tablebase, oracle undetermined pending 9-man results.
- Move tables agree with model where resolved.

**6. Solver Validation and Engines**
- Independent sumsolver agrees on 4.97M predictions; document sum_safe heuristic and fixes.
- Stockfish/Lc0 on CGT suite show class effects at shallow depth; need larger sums.

**7. Re-Audit of 2025 Paper**
- Correct errors (§7.1,7.2,7.3,§8 Dawson) and convention notes; give corrected verdicts.

**8. Discussion and Open Questions**
- Elkies' question remains open. Most promising path: 9-man exact results for remaining candidates.
- Lessons about convention sensitivity (e.p., race rules, king mobility).

**Appendices**
- A: Reproduce commands for all headline numbers
- B: Certificate FENs and race sets
- C: Corrected Dawson text reference
