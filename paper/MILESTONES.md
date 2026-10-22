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
| P1 | One continuous IEEE draft (`paper/ieee/`): the 2025 text as the base, errors fixed in place, new results continued, verified figures | Claude workflow (paid plans were out) | 🔄 |
| P2 | Adversarial reviews (facts recomputed, flow and voice, IEEE production) and a revision | the same workflow | 🔄 |
| P3 | Independent outside review and revision | Codex at 10:31 PM: T17/T18 on free models, then T19 on Codex | ⏳ |
| P4 | Overleaf / arXiv package: zip, figures as PDF, `.bbl` included, a clean build from a fresh folder | — | ⬜ |
| P5 | Repository link: confirm the URL; create the private GitHub repo only with Aritro's OK | Aritro | ⏳ |
| P6 | Human read of every proof by Aritro; mentor review when Aritro decides | Aritro | ⏳ |

## Research track (each result → paper section)

| # | Checkpoint | Trigger / check | Paper | Status |
|---|---|---|---|---|
| R1 | \*2 with 7 pawns (model) | three programs agree | §VIII | ✅ |
| R2 | **1/8 certified in real chess** | `realchess/targets18/kp_eighth_{9man,cap2}.out` → `apply_kpsolve.py` pinned → QRBN rerun | §IX, abstract | 🔄 kpsolve |
| R3 | Real-chess oracle of the 7-pawn \*2 positions | T20 (`research/star2_oracle/`) | §IX | 🔄 free model; Codex retry later |
| R4 | The rest of the \*2 search: flat width 5 with 8 pawns | T21 (`research/star2_width5/`) | §VIII | 🔄 |
| R5 | Independent 7-pawn census (raises "exactly two" to [C2]) | T22 (`research/star2_seven_check/`) | §VIII | 🔄 |
| R6 | KPKP and KPPK on the cylinder | T23 (`research/kpkp/`) | §X | 🔄 |
| R7 | ↑²\* and tiny(1) in real chess | `to_kpsolve.py` → kpsolve, after R2 frees the CPU | §IX | ⬜ |
| R8 | Odd-width cylinders | T12 report landed; needs an independent check | §IV | ⏳ verify |
| R9 | Dawson variants | T14 | §XI | 🔄 |
| R10 | Möbius strip and Klein bottle; ML on ChessSums | T9 and T5 ended without reports; relaunch when a plan resets | §X, §XII | ⏳ |
| R11 | Prop. 2.10(b) in a non-terminal context | — | §IV | ⬜ |
| R12 | Larger \*k: a \*3 at count / e.p.-aware? Thermography of the new \*2 neighbourhood | — | §VIII | ⬜ |

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
