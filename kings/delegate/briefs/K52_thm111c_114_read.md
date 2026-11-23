# K52: referee read of Theorem 1.11(c) and Theorem 1.14 as they now stand

**Output directory:** `kings/delegate/out/K52/` (exists). Write only there. Do **not** edit any existing file. Do not
run git.

Both theorems were changed on 2026-11-23 (commits 435ccdc7 and ef1314c3; `kings/delegate/out/S12A/REVIEW.md` and
`kings/delegate/out/T81L/REVIEW.md` say what changed). The changes were written and checked by models of one vendor.
You are the check from outside it.

Read in `kings/theory/LOOPY.md`: §1.1 (the promotion convention), §1.2 (Definitions 1.1–1.5), Definition 1.10,
Theorem 1.9, Theorem 1.11 (a)–(c) with proofs, §1.5 with (V1)–(V4) and the paragraph defining S and D, Theorem 1.14
(i), (ii), (iii) with proofs, and the sharp form after it. Read `cylcgt/pawns.py` (`value`, `_child`, `moves`,
`passed`) and `lemmas/common.py` (`threats`, `reachable`, `hereditarily_safe`) to see what the engine does.

1. **Theorem 1.11(c).** Mark every step of the proof SOUND, GAP or FALSE. Attack in particular: the hypotheses (HSS),
   (B), (E) and the passer-free root (is each needed, is the set sufficient?); the frontier step and its new
   parenthesis (re-split components inherit "no − threat"; threats by moves of either player in any order); the step
   "both models give the child" and its use of (E); the stated order of operations in S (test the moved component for
   passed pawns, score a race, split only if nobody is passed); the promotion convention on boards with 4 and 5 ranks.
   Is "whether (c) holds without (E): OPEN" right, or can you settle it (a counterexample, or a proof)?
2. **Theorem 1.14.** It is now stated per side to move. Mark every step of (i), (ii), (iii) SOUND, GAP or FALSE. Is the
   per-starter statement exactly what the proof gives? Does (ii) cite 1.11(c) with all of its hypotheses? Does any later
   use (the sharp form, the chess bridge after Proposition 3.2, Theorem 3.2‴, P11, P12) need both starters without
   assuming both?
3. **Tests.** Your own script, importing `cylcgt` read-only: for every passer-free root with at most 2 + 2 pawns on
   flat and cylinder boards of 3–4 files and 4–6 ranks that satisfies (HSS) and (E), compare o(S) with the whole-board
   result; then the same for roots that fail (E). Report counts and every disagreement, with the position.

Write `FINDINGS.md`: a 5-line summary; per step the verdict; each problem with the LOOPY line number, a counterexample
or the missing step, and replacement text; the test counts; your recommended label for each theorem.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Light computation only (minutes, under 1 GB). No file over 50 MB; no installs, no
network. Never use pkill, killall, `kill -- -1` or any pattern kill. Delete binaries at the end. The repository is
public: no personal data, relative paths only.
