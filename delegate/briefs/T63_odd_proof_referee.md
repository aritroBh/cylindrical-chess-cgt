# T63: non-Claude referee of the odd n+2 family proof (R_n *2, Qo_n *3)

Output: put all scripts and logs in `research/ring_n_plus_2_check/odd/` (create it) and write `REPORT.md` there.
Do NOT edit `research/ring_n_plus_2_proof/PROOF_odd.md` or any other file.

## Background

You refereed the even families as T53 (P_n, *2) and T62 (Q_n, *3), both SOUND. See
`research/ring_n_plus_2_check/REPORT.md` and `research/ring_n_plus_2_check/q/`.

New claim, written and checked so far only by Claude models (`research/ring_n_plus_2_proof/PROOF_odd.md`). In the
whole-board game with race rule count, e.p. on, and an e.p.-capturable pawn not counted as passed:

  R_n  = W5 B7 (W2 B4)^((n-11)/2) W2 W3B6 W3 W2B5 B5 W2 B4    is *2 for every odd n >= 11
  Qo_n = W4 B7 (W2 B4)^((n-11)/2) W2 W3B6 W3 W2B5 B5 W2 B4    is *3 for every odd n >= 11

Each has n+2 pawns, and both families fail at n = 9.

The proof is T50's insertion argument with cut c = 6 and base n0 = 19:
- The reduced graphs have 429 (R) and 1287 (Qo) nodes for every odd n >= 11.
- Files 2..n-8 are pattern files in every node.
- n = 11..17 are checked directly.

Logs: `research/ring_n_plus_2_proof/logs/pump_R_fixc.txt` and `pump_Qo_fixc.txt`. Checks:
`research/ring_n_plus_2_proof/odd/`.

## What to do

1. **Referee.** Read PROOF_odd.md against PROOF.md (section 2b), PROOF_Q.md and `research/ring_family_proof/proof.tex`,
   looking for a real gap. In particular check:
   - the wall's odd length, which starts and ends with W2;
   - Lemma 2(b) at both wall ends (left window 2..6, right window 7..11 at n = 19);
   - the cut c = 6, whose arc 2..11 touches neither zone;
   - the e.p. convention (inert flags dropped).
2. **Independent computation.** Copy your `independent.py` into `research/ring_n_plus_2_check/odd/` and compute the
   signature of G+*h, h = 0..4, for R_n and Qo_n with odd n = 9..23. *2 means NNPN·, *3 means NNNP·.
   - Also check one control that is not the claimed value.
   - If your engine can, rebuild the reduced graph at n = 19 and compare node counts.
3. **REPORT.md.**
   - Begin with a 5-line summary.
   - Give a verdict (SOUND / GAP / FALSE) with reasons.
   - List what you recomputed, and any fixes PROOF_odd.md needs (as text; do not edit it).

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git. Do not edit `paper/`, the `PROOF*.md` files or any other directory.
