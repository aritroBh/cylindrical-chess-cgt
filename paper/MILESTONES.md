# Checkpoints, not a finish line

Each checkpoint banks something in the paper. The work does not stop at any of them. When one lands:
1. verify it (the review rule: nothing goes in on one unchecked run);
2. update the paper and RESULTS.md;
3. commit locally (never push);
4. start the next round.

Status: ✅ banked · 🔄 running · ⏳ waiting (quota or owner) · ⬜ not started

## Paper track (IEEE / arXiv)

| # | Checkpoint | Who | Status |
|---|---|---|---|
| P1 | One continuous IEEE draft (`paper/ieee/`): the 2025 text as the base, errors fixed in place, new results continued, verified figures | Claude workflows | ✅ 13 pages, `paper/Bhattacharjee_Cylinder_Chess_IEEE.pdf` (f11104a) |
| P2 | Adversarial reviews (facts recomputed, flow and voice, IEEE production) and a revision | the same workflows, 2 check rounds | ✅ REVIEW_LOG.md |
| P3 | Independent outside review and revision | T17 (facts) and T18 (style) on free models, launched 23:58 | 🔄 |
| P4 | Overleaf / arXiv package: zip, figures as PDF, `.bbl` included, a clean build from a fresh folder | — | ⬜ |
| P5 | Repository link | private repo github.com/aritroBh/cylindrical-chess-cgt created and main pushed (Aritro approved, 2026-10-21) | ✅ |
| P6 | Human read of every proof by Aritro; mentor review when Aritro decides | Aritro | ⏳ |

## Research track (each result → paper section)

| # | Checkpoint | Trigger / check | Paper | Status |
|---|---|---|---|---|
| R1 | \*2 with 7 pawns (model) | three programs agree | §VIII | ✅ |
| R2 | **1/8 certified in real chess** | 9-man done (all 6 sides exact, all match the model) → bounds [0, 1/8]. Last side `W b2 b5 / B a5 b4`, Black to move: cap-2 run → then QRBN rerun | §IX, abstract | 🔄 one side left |
| R3 | Real-chess oracle of the 7-pawn \*2 positions | T20 on Codex since 22:33, resuming from the decisive 8-man end positions | §IX | 🔄 Codex |
| R4 | The rest of the \*2 search: flat width 5 with 8 pawns | T21: 21 \*2 at count/aware. All 21 use all five files, no mirror pairs. cylcgt agrees on 15 (incl. the paper's 3), disagrees on 6. Third-program arbitration of the 6 is running (`delegate/checks/w5_arbiter/`). The paper says "three"; fix it to "at least 15" once the arbiter is done | §VIII | 🔄 arbiter |
| R5 | Independent 7-pawn census (raises "exactly two" to [C2]) | T22 died after widths 1–3 (0 hits) with its one width-4 hit unsaved; T22b reruns it in resumable chunks | §VIII | 🔄 |
| R6 | KPKP and KPPK on the cylinder | T23 died again (kilo 503); relaunched on opencode best-free | §X | 🔄 |
| R7 | ↑²\* and tiny(1) in real chess | `realchess/targets18/run_r7.sh`: 15 end positions (one 8-man, 14 9-man; the 10-man ones later), one at a time after the 1/8 cap-2 run, results in `r7/` | §IX | 🔄 queued |
| R8 | Odd-width cylinders | T25: T12 (a) and (d) confirmed [C2]; (b) and (c) refuted, with spot checks by the orchestrator | §IV/§X | ✅ verified, not yet in paper |
| R9 | Dawson variants | T14 | §XI | 🔄 |
| R10 | Möbius strip and Klein bottle; ML on ChessSums | T9 and T5 ended without reports; relaunch when a plan resets | §X, §XII | ⏳ |
| R11 | Prop. 2.10(b) in a non-terminal context | settled in kings/ (LOOPY.md: PROVED, reviewer-confirmed; context dependence for T ≥ 2 supported by P4) | §IV | ✅ AI-reviewed |
| R12 | Larger \*k; fewest pawns for \*2 on each cylinder | T24 + orchestrator split completion: first ring \*2 on Cn has n+3 pawns for n = 3, 4, 5 [values C2, minimality C1]. Added to §VIII, intro, abstract | §VIII | ✅ |

| R13 | Does n+3 continue (C6 with 9 pawns, C7 with 10)? First \*3 on narrow cylinders | T26 + T43 (Codex) + orchestrator. n+3 holds for n = 3–7; C7: no nine-pawn ring \*2 (two programs), 63 ten-pawn \*2. **Default-setting single-component \*3**: 8 ten-pawn C7 rings (three programs). C8 open | §VIII | ✅ |
| R14 | A \*3 under count with e.p. OFF on six files (T24: 16 hits at C/off, 26 count/mover rows) | T27: cylcgt + whole-board solver | §VIII | 🔄 |

## Plans and quotas (2026-10-21, 7 PM)

| Plan | Status |
|---|---|
| Codex | back at 10:31 PM |
| Antigravity (agy) | back in about 46 h |
| Cursor | out until 11/9, every model |
| Muse | billing error |
| Qwen | not signed in |
| OpenCode / Kilo free models | working (Kilo is rate-limited at times) |

Use free models for research scripts and reviews, and Codex for writing and revision once it is back.
