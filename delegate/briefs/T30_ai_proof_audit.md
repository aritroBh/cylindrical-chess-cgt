# T30: independent audit of the paper's [AI]-labelled proofs (no compute)

**Output directory:** `notes/proof_audit2/`.

**Read:**
- `paper/ieee/sections/04_kings.tex`: Theorem 3, Conjectures 4, 5 and 7, Proposition 6, Theorem 8;
- `paper/ieee/sections/05_sums.tex`: Definition 9, Theorem 10, Propositions 11 and 12;
- the full proofs in `kings/theory/`, `notes/lemmas.md` and `kings/REPORT.md`.

**For each [AI] statement:**
1. Restate it precisely.
2. Check the full repository proof line by line: SOUND, GAP (say exactly where) or FALSE (give a
   counterexample).
3. Check that the paper's short proof sketch matches the full proof and does not claim more.
4. Rate how confident you are, and why.

Also check that every [P] in the paper is really proved in the text (Theorem 2, Theorem 21, Lemma 18).

**Deliverable:** `REPORT.md` with one table: statement | verdict | where | fix.
Be adversarial: default to GAP when a step is not justified.
