# T51: referee the proof that the wall rings are *2 for every n (non-Claude check)

Output directory: `research/ring_family_proof_check/` (create it; write nothing anywhere else).

## Background

A Claude agent (T50) wrote `research/ring_family_proof/proof.tex`. It claims that in the **whole-board game**
(cylcgt with `pawns.components = lambda b, p: [p]`; RACE_RULE "count"; e.p. on; PASSED_RESPECTS_EP True) two
ring families with n+3 pawns are *2 on every cylinder C_n:
- O_n for odd n ≥ 5: files `W23B4, B5, W2B5, (W3, B5)^k` with n = 2k + 3;
- E_n for even n ≥ 6: files `B5, W2B5, W35B6, W2, (B4, W2)^(m+1)` with n = 2m + 6.

Here `W23B4` means white pawns on ranks 2 and 3 and a black pawn on rank 4 of that file. E_8 is
`W b2 c3 c5 d2 f2 h2 / B a5 b5 c6 e4 g4`.

The proof has three hand lemmas, then two finite checks:
- Lemma 1: reduction. Poisoned moves may be deleted.
- Lemma 2: every wall-pawn move is lost or poisoned.
- Lemma 3: insertion. Adding two wall files maps the reduced game onto itself.
- The finite checks are the base graphs, with 144 nodes (O, n = 17) and 104 nodes (E, n = 16), and all n < n0.

## What to do

1. **Read** `proof.tex`, all of it, line by line, as a referee trying to find a gap. Check in particular:
   - Lemma 2(a): a lapsing e.p. flag, and the white double step 2→4 landing beside a B4.
   - Lemma 2(b): the "two ranks further on" geometry, the capture into a passed pawn, and whether the capturer
     really has no enemy pawn on its three files, both after a step and after a double step.
   - Lemma 3(iii): whether a reply by a pawn near the cut can produce a terminal that the lemma misses. This
     includes races under the count rule.
   - The induction in the proof of the theorem: does every node of the reduced game of G_n really keep files
     c-4..c+5 as pattern files?
2. **Reproduce** the computational claims with T50's own scripts, without editing them: run
   `sh research/ring_family_proof/run_all.sh quick` from the project root, under `nice -n 15`, with its output
   redirected into your directory. Compare every number in the logs with the claims in `proof.tex`: 144 and 104
   nodes; 209/246 and 177/97 edges; the pumping check from 17 to 61 and from 16 to 60; the 113 rings up to n = 61.
3. **Independent check by method.** Write your own small Python script, in your directory, that uses ONLY
   `cylcgt.pawns.Board`, `Pos.parse` and `cylcgt.pawns.passed` (or the e.p.-aware passed test) plus your own move
   generator. Do NOT read or copy `rg.c` or the game-value code in `cylcgt/`. The script should:
   - for O_n and E_n with n ≤ 13, list every wall-pawn move from the start position;
   - for each such move, check the claim of Lemma 2(b) that the opponent then has a capture that gives him a
     passed pawn, and that the mover has none.
   Report every exception.

## Rules

- Follow delegate/COMMON.md.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start
  and stop only those, by PID.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git. Do not edit `paper/` or `research/ring_family_proof/`.
- Write `REPORT.md` in your output directory. Begin it with a 5-line summary. Then give the verdict (SOUND /
  GAP / FALSE) for each lemma, with your reasons, the reproduced numbers, and the results of step 3.
