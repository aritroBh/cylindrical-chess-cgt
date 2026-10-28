# K33 report

## Summary

1. **PROVED:** I independently re-derived the loopy bridge, reserve subadditivity/monotonicity, reserve criterion, and sandwich.
2. Every LOOPY proof step for those results is **SOUND**; no gap or counterexample was found.
3. Theorem 3.8(a)–(c), Corollary 3.8b, and Corollary 3.11a follow with the stated scope.
4. **COMPUTED-1:** seeded random checks passed 1,185 reserve implications and all sampled bridge, criterion, and sandwich checks.
5. Recommended status: keep the theorems **PROVED**; keep this run's counts **COMPUTED-1**.

## Deliverables

- [`PROOF.md`](PROOF.md): blind Phase 1 proof.
- [`FINDINGS.md`](FINDINGS.md): Phase 2 comparison, proof-step verdicts, corollaries, test counts, and recommended labels.
- [`random_tests.py`](random_tests.py): stdlib fixed-point checker and exact random generator.

## Reproduction

From the project root, run:

```sh
PYTHONPATH=. .venv/bin/python kings/delegate/out/K33/random_tests.py
```

The fixed seed is `330027`. It generates 500 pairs for Lemma 3.8a, 240 component tuples for Theorems 3.7 and 3.8, and 300 `(K,S)` pairs for Theorem 3.11. Full generator details and per-statement counts are in [`FINDINGS.md`](FINDINGS.md); the command prints the exact counts as JSON.

## Label boundary

The proof check is an independent Codex-family derivation; it supports **PROVED** labels. The random checker is one implementation, so its numbers are **COMPUTED-1**, not **CHECKED-2**. The Research Plan's human-review gate remains separate.
