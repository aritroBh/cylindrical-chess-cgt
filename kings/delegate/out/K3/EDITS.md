# K3: edits to kings/theory/LOOPY.md after independent check

### EDIT 1: T1.14, sharp form — R2 item 6
<<<<<<< OLD
**Sharp form (PROVED after repair: R2 item 6).**
=======
**Sharp form (GAP (proof incomplete): R2 item 6).** (revised after K3 check)
>>>>>>> NEW

### EDIT 2: T2.7 — R1 item 3, R3 items 2 and 3
<<<<<<< OLD
**Theorem 2.7 (sufficiency of the certificate). PROVED after repair (in P).** If LC_T(m) holds at Y, then the
=======
**Theorem 2.7 (sufficiency of the certificate). GAP (proof incomplete) (in P).** If LC_T(m) holds at Y, then the (revised after K3 check)
>>>>>>> NEW

### EDIT 3: status table row, T1.14 sharp form
<<<<<<< OLD
| T1.14, sharp form | GAP → PROVED after repair: every legal Z-move of the loser at its turns must be a P-loss | R2 item 6 |
=======
| T1.14, sharp form | GAP → GAP (proof incomplete): every legal Z-move of the loser at its turns must be a P-loss (revised after K3 check) | R2 item 6 |
>>>>>>> NEW

### EDIT 4: status table row, T2.7
<<<<<<< OLD
| T2.7 | GAP → PROVED after repair: (L1) is required only for k = ∞, (L3) covers stalemate, the local rules are stated, and μ counts context pawns only | R1 item 3, R3 items 2 and 3 |
=======
| T2.7 | GAP → GAP (proof incomplete): (L1) is required only for k = ∞, (L3) covers stalemate, the local rules are stated, and μ counts context pawns only (revised after K3 check) | R1 item 3, R3 items 2 and 3 |
>>>>>>> NEW

### EDIT 5: status table row, P11
<<<<<<< OLD
| P11 | PROVED (implication) after repair: W(X) and HSS defined; (V1b) checked from the layout | R1 item 11 |
=======
| P11 | GAP (proof incomplete): W(X) and HSS defined; (V1b) checked from the layout (revised after K3 check) | R1 item 11 |
>>>>>>> NEW

### EDIT 6: status table row, P12
<<<<<<< OLD
| P12 | PROVED (implication) after repair: restricted to nodes where `--frozen` reports a win | knock-on of R2 item 4 |
=======
| P12 | GAP (proof incomplete): restricted to nodes where `--frozen` reports a win (revised after K3 check) | knock-on of R2 item 4 |
>>>>>>> NEW

### EDIT 7: §6 table, P11 label
<<<<<<< OLD
| Thm 1.11 + Thm 1.14 (frozen kings satisfy V1 and V3 by fiat) | PROVED (as an implication; the harness checks the hypotheses) |
=======
| Thm 1.11 + Thm 1.14 (frozen kings satisfy V1 and V3 by fiat) | GAP (proof incomplete): the harness checks the hypotheses (revised after K3 check) |
>>>>>>> NEW

### EDIT 8: §6 table, P12 label
<<<<<<< OLD
| Thm 2.4(b) + Thm 2.7 (contrapositive) | PROVED (implication), restricted to the nodes where `--frozen` reports a win |
=======
| Thm 2.4(b) + Thm 2.7 (contrapositive) | GAP (proof incomplete), restricted to the nodes where `--frozen` reports a win (revised after K3 check) |
>>>>>>> NEW

## STATUS ROWS

| Result | Final label | Note |
|---|---|---|
| T1.11(b) | PROVED after repair | τ corrected to either-player moves; proof step valid; SOUND |
| T1.11(c) | PROVED after repair | re-splitting version; M monotone; SOUND |
| P1.13 | PROVED after repair | regimes verified with cylcgt; SOUND |
| T1.14(ii) | PROVED after repair | follows from (c) with (V4); SOUND |
| T1.14, sharp form | GAP (proof incomplete) | no full proof written; (revised after K3 check) |
| T2.4 | PROVED after repair | normal-play (a),(b) plus draw transfer (c); SOUND |
| T2.7 | GAP (proof incomplete) | passers in context not ruled out by (L2); (revised after K3 check) |
| L2.9 | PROVED after repair | added hypothesis; proof sound; SOUND |
| P2.10(a) | PROVED after repair | H ≥ 5; H = 4 counterexample; SOUND |
| P3.2 (chess bridge) | PROVED after repair | adds (V1a); SOUND |
| T3.3(b) | PROVED after repair | { | ⊖} ⊞ on_D = (L,L); SOUND |
| T4.2(a) | PROVED after repair | D-model; SOUND |
| T4.2(b) | PROVED after repair | D-model; SOUND |
| T4.2(c) | PROVED after repair | covers negatives via 3.3(a); SOUND |
| P4.3 | PROVED after repair | (H1),(H2) repair; SOUND |
| P11 | GAP (proof incomplete) | depends on heuristic Remark 2.11; (revised after K3 check) |
| P12 | GAP (proof incomplete) | depends on T2.7; (revised after K3 check) |
