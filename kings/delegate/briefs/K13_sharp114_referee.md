# K13: non-Claude re-check of the sharp form of Theorem 1.14 (the simulation lemma)

**Output directory:** `kings/delegate/out/K13/` (create it). Write only there. Do **not** edit any existing file.
Do not run git.

The sharp form of Theorem 1.14 is labelled "PROVED after repair, not yet independently re-checked".

- A free model drafted it.
- Two AI reviewers found real errors: the draft claimed that the D-winner never moves in Z, and it never fixed
  what D(X) is on Z.
- A Sonnet agent rewrote it as a simulation lemma (an induction on the rank of the D-win), and the integrator
  read the rewrite.
- Nobody outside the Claude family has checked it.

You are that check. A written argument is required; a bare verdict is not accepted.

## Read

- `kings/theory/LOOPY.md`:
  - §1.2 (the four models C, P, D and F), §1.3 (Lemmas 1.6 and 1.7);
  - **Theorem 1.14** (search for "Theorem 1.14 (validity of the convention)"): (V1)–(V4) and the proof of (i);
  - **Theorem 1.14, sharp form** (search for "Theorem 1.14, sharp form"): the definition of a σ-certified set N,
    conditions (S1), (S2) and (S3), the proof by induction on the D-rank, and the remarks and table after it;
  - its uses:
    - the chess bridge of Proposition 3.2 (search for "Chess bridge");
    - Corollary 2.7′ (search for "C2.7′" in the status table, then its statement in §2);
    - the status rows "T1.14, sharp form" and "C2.7′".
- `kings/kpsolve.c`: the header comment, `--frozen`, and the cap semantics.

## Task

1. **Re-derive the sharp form in your own words.**
   - In `REPORT.md`, write a complete proof. Do not paraphrase LOOPY.
   - Check the definition of D(X) on Z.
   - Check that the D-rank is well defined: D is short, so the induction is well founded.
   - Check that (S1) lets the winner move in Z, and that the simulation handles it.
   - Check that (S2) covers every legal move of the loser: a D-move, or a P-loss.
   - Check that (S3) excludes stalemate exactly where it is needed.
   - Check what happens at a node where the loser is in check.
   - Mark each step of LOOPY's proof SOUND, GAP (give the missing step) or FALSE (give a counterexample).
2. **The uses.**
   - Does the chess bridge of Proposition 3.2 follow from the sharp form? Here D = G ⊞ on_D, and White's shuttle
     moves are moves in Z.
   - Does Corollary 2.7′ follow?
   - Say exactly which hypothesis is checked where.
3. **Small computations (optional, but welcome).**
   - On a small board (cyl:5×5 or 6×5, or flat 5×5), build a σ-certified set for a few positions. The kings may
     move: take a pawn position whose kings have a safe shuttle, or `--frozen` positions. Check that the
     theorem's conclusion holds (a P-win for σ).
   - Try to build a position that meets the hypotheses but where the conclusion fails.
   - Build kpsolve privately: `cc -O2 -o kings/delegate/out/K13/kp kings/kpsolve.c -lpthread`.
   - Run batches through the lock: `kings/delegate/heavy.sh kings/delegate/out/K13/kp --board ... < in > out`.
   - The P model with real kings is the C model with "the first promotion wins". A private build of it is
     `kings/delegate/out/K7/scripts/draft/kp_p.c`; you may compile and use it, but do not read the rest of `K7/`.

## Deliverable

`REPORT.md`, starting with a 5-line summary. Then:
- your proof;
- the per-step verdicts;
- the uses;
- your computations, with exact commands and counts;
- your recommended label.

## Rules

`delegate/COMMON.md`, rules 5 and 7. In addition:
- at most 2 heavy processes, always through `kings/delegate/heavy.sh`;
- under 3 GB RSS;
- at most 20 minutes per run;
- no file over 50 MB;
- no installs, no network.

Never use pkill, killall, `kill -- -1` or any pattern kill; kill only PIDs you started and recorded.
