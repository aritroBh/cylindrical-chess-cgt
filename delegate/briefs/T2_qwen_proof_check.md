# T2 (qwen): second-model re-derivation of the proofs

Output: `verify_ext/qwen/PROOFS.md` (the report; also write a short `verify_ext/qwen/REPORT.md` that points to it).

The project's rule: one model wrote each proof, and a second model must re-derive it before it is published.

For each statement below, do four things:
- restate it precisely;
- re-derive the proof in your own words;
- name every step you could not justify;
- give a verdict: VALID, VALID-WITH-REPAIR (give the repair) or GAP (give a counterexample idea or the missing lemma).

Statements:
- `notes/lemmas.md`: L1.6 (decomposition under condition (E)), L2.1 (the HSS theorem), L2.3 (sum model = whole-board game when nothing splits), L3.3 (the freeze lemma) and L5.1 (the Dawson ring reduction: R_n = mex{g(n-3)}).
- `kings/theory/LOOPY.md`: Theorem 1.14(i), Theorem 2.7 (the referees noted a gap fixable by an unlimited-pass argument; check whether the repair works), Proposition 2.10 and Theorem 3.4.

You may run small Python checks (`.venv/bin/python`) to test a step. Do not edit the source files.
