# K13b: check the rewritten one-sided chess bridge (post-commit check of 774036f)

**Output:** `kings/delegate/out/K13/CHECK_774036f.md`. Write only that file. Do not edit any other file. You may run
`git show 774036f` and `git diff 774036f~1 774036f` (read-only); no other git command.

Commit 774036f integrates your K13 report (`kings/delegate/out/K13/REPORT.md`) into `kings/theory/LOOPY.md`. The
integrator rewrote the one-sided chess bridge after Proposition 3.2 (search for "**Chess bridge**"), following your
"GAP in the printed bridge wording", and edited six status and label passages.

Check, and write a short verdict for each point (OK / PROBLEM with the exact fix):
1. The rewritten bridge: are its four hypotheses exactly what the sharp form of Theorem 1.14 needs for D = G ⊞ on_D
   (search "Theorem 1.14, sharp form" for (S1)–(S3), and "Theorem 3.2‴" for the two-sided analogue)? Is each of
   (S1), (S2), (S3) in its proof correctly discharged? Is anything still missing or too strong (for example checks,
   e.p., a Black move that is neither a context move nor a Z-move, a White promotion, a pass at a node where Σ is
   rank-lowering)?
2. Does any edited sentence say more than your report supports, or misstate it?
3. Does any other passage of LOOPY.md still rely on the old wording ("every legal chess move of the side to move is
   one of the D-options") or on the bridge being proved by "the proof of Theorem 1.14(i)"? Give line numbers.
4. Is every markdown table row in the diff still the same number of cells as its header?

Start the file with a 3-line summary. No computations are needed.
