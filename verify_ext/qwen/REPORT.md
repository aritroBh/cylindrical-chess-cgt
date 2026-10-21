# T2 (qwen) Verification Report

**Output directory:** `verify_ext/qwen/`

## Summary

Re-derived 9 proofs from `notes/lemmas.md` (L1.6, L2.1, L2.3, L3.3, L5.1–5.3) and `kings/theory/LOOPY.md` (Theorem 1.14(i), Theorem 2.7, Proposition 2.10, Theorem 3.4). Each proof was restated precisely, re-derived in my own words, unjustified steps identified, and a verdict given.

## Verdicts

| Source | Statement | Verdict |
|---|---|---|
| `notes/lemmas.md` | L1.6 (Theorem 1.6: decomposition under (E)) | **VALID** |
| `notes/lemmas.md` | L2.1 (Theorem 2.1: HSS theorem) | **VALID** |
| `notes/lemmas.md` | L2.3 (Theorem 2.3: no split ⇒ S=W) | **VALID** |
| `notes/lemmas.md` | L3.3 (Theorem 3.3: freeze lemma) | **VALID** |
| `notes/lemmas.md` | L5.1–5.3 (Dawson ring reduction) | **VALID** |
| `kings/theory/LOOPY.md` | Theorem 1.14(i) (P(X)=D(X)) | **VALID** |
| `kings/theory/LOOPY.md` | Theorem 2.7 (local certificate LC_T) | **VALID-WITH-REPAIR** (unlimited-pass condition k=∞ in L1 is the repair) |
| `kings/theory/LOOPY.md` | Proposition 2.10 (universal punishments) | **GAP** — counterexample for T≥2 is a terminal context, not non-terminal |
| `kings/theory/LOOPY.md` | Theorem 3.4 (outcome rules with passes) | **VALID** |

## Key Findings

1. **All `notes/lemmas.md` proofs are valid.** The structural lemmas (components, HSS, freeze, Dawson ring) are correctly proved. The HSS condition is exactly what replaces the flawed `sum_safe()` heuristic.

2. **Theorem 2.7's repair works.** The referee's gap (needing unlimited-pass argument) is fixed by requiring (L1) to hold for *every* pass budget k ∈ {0,1,2,…,∞}, which the current statement does.

3. **Proposition 2.10(b) has a gap.** The claimed counterexample for T ≥ 2 (`W: (f,H−2); B: (f,H−1), (f+1,H−1)`) is a terminal position (Black has passed pawns), not a non-terminal context. The claim may still be true but needs a different construction.

4. **Theorem 3.4 is solid.** The fixed-point derivations for `on_D`, `off_D`, `dud_D` are rigorous and match the least-fixed-point semantics of loopy games.

## Full Details

See `verify_ext/qwen/PROOFS.md` for the complete re-derivations, step-by-step justifications, and exact locations of any gaps.