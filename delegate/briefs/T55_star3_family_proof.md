# T55: write the proof note for the *3 ring family Q_n (n+2 pawns, every even n ≥ 8)

Output: `research/ring_n_plus_2_proof/PROOF_Q.md` (new file), plus scratch files in
`research/ring_n_plus_2_proof/t55/` (create it). Write nothing else anywhere.

## Background

We work in the whole-board pawn game on the n-file cylinder C_n:
- 8 ranks;
- race rule "count";
- e.p. on;
- a pawn that can still be taken e.p. is not passed;
- the game ends at the first passed pawn.

The proof that a related family is *2 is complete and refereed. Read these first, in full:
- `research/ring_n_plus_2_proof/PROOF.md`. It proves P_n = W5 B7 W4 W4B7 B6 W3B6 (W2 B4)^((n-6)/2) is *2. Read
  especially its section 2 (the repaired "pattern file" definition), §2b (Lemma 3 (ii)–(iii) written out) and its
  H-items, H8 included.
- `research/ring_family_proof/proof.tex`, T50's Lemmas 1–3.
- `research/ring_n_plus_2_check/REPORT.md`, the Codex referee's verdict: SOUND.

The new claim:

  Q_n = W4 B7 (B4 W2)^((n-8)/2) W3B6 W3 W2B5 B5 W2 B4, n even ≥ 8, n+2 pawns, is *3 in the whole-board game.

Notation: one token per file, file 0 first, as in rg.c. Q_8 = W a4 c3 d3 e2 g2 / B b7 c6 e5 f5 h4 is the ten-pawn
*3 ring on C8. The scanner, cylcgt (sum and whole-board) and rg all agree on it.

Evidence (`research/ring_n_plus_2_proof/logs/`):
- `unreduced_Q_8_60.txt`: signature NNNP (= *3) for every even n from 8 to 60;
- `pump_Q_8_60.txt`: the reduced graph has 7968 nodes for n ≥ 18, no e.p. flag, zone {0,1,2,3, n-7..n-3, n-1};
- `pump_Q_fixc9.txt`: with the cut c = 9, R_{n+2} = ins_9(R_n) for n = 22..58;
- `reduced_cyl_Q.txt`: the cylcgt-based rebuild is identical to rg's graph for n = 8..24.

## What to do

1. Write `PROOF_Q.md`, mirroring `PROOF.md`. Handle these two differences explicitly:
   - **The target is *3.** State what "= *3" means, as H8 does for *2:
     - G+*3 is a P-position;
     - G+*h is N for h = 0, 1, 2 by direct check;
     - G+*h is N for h > 3, via the heap move to G+*3.
   - **The zone has two parts.** Here the wall (files 2..n-7) has core files on BOTH ends. Check:
     - with c = 9 and n0 = 22, files c-4..c+5 = 5..14 are exact pattern files in every node of R_n for n ≥ 22;
     - ins_9(start_n) = start_{n+2};
     - Lemma 2(b)'s windows hold at both wall ends.
2. Re-run `sh research/ring_n_plus_2_proof/run_all.sh` (about 3 minutes). Compare every Q number with the logs.
3. Write your own short check in `t55/`: for every node of R_22, assert that files 5..14 equal the start. Build R_22
   with the project's `graph.py`/`fam.py`, or with your own code.
4. Begin `PROOF_Q.md` with:
   - a 5-line summary;
   - a claims table with labels: PROVED [AI] (given the lemmas), CHECKED-2, COMPUTED-1.

   Keep it under 120 lines. Name any gap honestly.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git. Do not edit `paper/`, `PROOF.md`, or any directory other than the two named above.
