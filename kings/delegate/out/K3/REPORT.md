# K3: independent check of the repaired proofs in LOOPY.md

## 5-line summary

- Of the 17 results marked "PROVED after repair" (or "FALSE … → PROVED after repair"), 13 are SOUND: T1.11(b), T1.11(c), P1.13, T1.14(ii), T2.4, L2.9, P2.10(a), P3.2 (chess bridge), T3.3(b), T4.2(a)-(c), P4.3.
- 4 are GAP: the sharp form of T1.14 (no full proof written), T2.7 (passers created in the context are not ruled out by (L2), which counts promotions only), P11 (depends on heuristic Remark 2.11), and P12 (depends on T2.7).
- No repaired proof was found FALSE with a counterexample; the review counterexamples are all excluded by the repaired hypotheses (verified on `Kb2 Pc2 kc4 pc3` and P4).
- The repaired τ (either player) and hereditary (V4) close the holes named in REVIEWS R1/R2; abstract checks (cylcgt) confirm P1.13 and T1.11(b) regimes.
- Downgrades are listed in EDITS.md; LOOPY.md itself was not edited.

## Verdict table

| Result | Verdict | Reason | Counterexample |
|---|---|---|---|
| T1.11(b) | SOUND | τ now counts moves into ⊕/⊖ by either player; monotonicity step valid | none (review's y1/y2 now fails pairwise safety) |
| T1.11(c) | SOUND | M monotone under component deletion; race scores local | none |
| P1.13 | SOUND | regimes verified with cylcgt at B=4 | none |
| T1.14(ii) | SOUND | follows from T1.11(c) with hereditary (V4) | none |
| T1.14, sharp form | GAP | no complete proof written; conditions only | none |
| T2.4 | SOUND | normal-play (a)/(b) proved; (c) draw transfer valid | none |
| T2.7 | GAP | (L2) counts promotions only; a context passer within T ends the game in s's favour | none found; P4 is an (L2) failure, not a theorem break |
| L2.9 | SOUND | added hypothesis (no pawn on f±1) makes proof valid | without hypothesis: s-pawn capture lets s̄ leave f |
| P2.10(a) | SOUND | H ≥ 5 excludes the H=4 double-step exception | flat:4×4 / cyl:7×4 (review) |
| P3.2 (chess bridge) | SOUND | (V1a) added; proof of T1.14(i) applies | P2 + H* stalemate if White plays e3–e4 |
| T3.3(b) | SOUND | { \| ⊖} ⊞ on_D = (L,L) | none |
| T4.2(a) | SOUND | D-model; suicides deleted first | none |
| T4.2(b) | SOUND | D-model equivalence plus B > ℓ | none |
| T4.2(c) | SOUND | on_D exceeds every number (incl. negatives) by Thm 3.3(a) | none |
| P4.3 | SOUND | (H1) not in check, (H2) non-promoting reply | `Kb2 Pc2 kc4 pc3` (flat:4×4) |
| P11 | GAP | depends on heuristic Remark 2.11; passer nodes not certified | none |
| P12 | GAP | depends on T2.7, which is GAP | none |

## Reproduce commands

- Abstract/regime checks: `PYTHONPATH=. .venv/bin/python` with `cylcgt.cgt` (see EDITS/report scratch).
- Solver checks: `cc -O2 -o kings/delegate/out/K3/kp kings/kpsolve.c`; then
  `printf 'Kb2 Pc2 kc4 pc3 w -\nKa1 Pc2 kc4 pc3 w -\n' | kings/delegate/out/K3/kp --board flat:4x4 --ep on --promote QRBN --cap 1 --moves`.
- Position checks: `kings/kpsolve --board cyl:7x6 --ep on --promote QRBN --cap 1` on the §6 rows.
