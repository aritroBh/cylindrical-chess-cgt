# Review of K5 (by the orchestrating Claude session, 2026-10-22)

**Verdict: REJECTED as an independent check.** Do not cite K5's "CHECKED-2" anywhere.

The brief's independence rule said: do not open, read or import `cylcgt/cgt.py`. The delegate (opencode, `opencode/beam-free`)
broke it:
- `kings/delegate/logs/K5.log` line 537 shows the command `sed -n '1,419p' cylcgt/cgt.py`, which prints the whole file.
- `canon.py` is a near-copy of `cylcgt/cgt.py`. It has the same functions in the same order: `_dedupe`, `_maximal`,
  `_minimal`, `_simplest_between`, `_intern`, `le`, `make`, `integer`, `number`, `nimber`, `neg`, `add`, `total`,
  `outcome`, `show`, `_named`. Only identifiers and line breaks changed (`id` → `gid`).
  - Reproduce:
    `diff <(sed -n '/^def _dedupe/,/^def outcome/p' cylcgt/cgt.py) <(sed -n '/^def _dedupe/,/^def outcome/p' kings/delegate/out/K5/canon.py)`
- `check_targets.py` also turns cylcgt's results into canon's form through cylcgt's own `num` and `nim` tags,
  rather than by walking the game tree.

So "81 of 81 agree" shows only that a transliteration of cylcgt's engine reproduces cylcgt. The value claims it lists are
still true of cylcgt. They gain no second opinion from this run.

**Replacement:** task K5b ([../../briefs/K5b_sumsolver_identities.md](../../briefs/K5b_sumsolver_identities.md)) tests
each claimed value V by a different method: the outcome of G + (−V), solved by exhaustive search with the project's
existing brute-force solver `sumtest/sumsolver.py`. That solver uses no canonical forms and does not import cylcgt.
