# T62: referee and repair the *3 family proof note (non-Claude)

Output: you may edit ONLY `research/ring_n_plus_2_proof/PROOF_Q.md`. Put any scripts and logs in
`research/ring_n_plus_2_check/q/` (create it). Write nothing else anywhere.

## Background

You refereed the *2 family proof `research/ring_n_plus_2_proof/PROOF.md` as T53. Your verdict was SOUND; see
`research/ring_n_plus_2_check/REPORT.md` and your `independent.py`.

A free agent then wrote `research/ring_n_plus_2_proof/PROOF_Q.md` for the *3 family:

  Q_n = W4 B7 (B4 W2)^((n-8)/2) W3B6 W3 W2B5 B5 W2 B4, n even ≥ 8, n+2 pawns, whole-board game.

The note uses the cut c = 9 and n0 = 22. The reduced game has 7968 nodes for n ≥ 18, and the zone is
{0,1,2,3, n-7..n-3, n-1}. Logs are in `research/ring_n_plus_2_proof/logs/` (`*_Q_*`).

The note is weaker than PROOF.md:
- it says "by inspection" where a check is needed (Lemma 2(b)'s windows at the wall ends);
- it mentions a "symmetric arc at the other end" that the proof does not need;
- it has a garbled line about Q_8;
- its C2'' row cites the cylcgt graph rebuild as a second program for the unreduced signatures, which it is not.

## What to do

1. Referee `PROOF_Q.md` against `PROOF.md` and `research/ring_family_proof/proof.tex`, looking for any real gap in the
   transfer to Q_n.
2. Repair `PROOF_Q.md` so that it is as precise as PROOF.md:
   - exact hypotheses H1–H8 for Q_n;
   - Lemma 2(b) at both wall ends, checked on the actual nodes;
   - the meaning of "= *3";
   - honest labels (which program checked what).
   Keep it under 130 lines.
3. Independent computation: extend your `independent.py` (copy it into `research/ring_n_plus_2_check/q/`) to compute
   the signature of G+*h, h = 0..4, for Q_n with n = 8..24. *3 means NNNPN. Also check one control that is not *3.
4. Append a section "Referee (T62)" to `PROOF_Q.md` with:
   - your verdict (SOUND / GAP / FALSE);
   - what you recomputed;
   - what you changed.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git. Do not edit `paper/`, `PROOF.md` or any other file.
