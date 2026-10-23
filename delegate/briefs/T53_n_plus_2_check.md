# T53: non-Claude referee of the even n+2 ring family proof

Output directory: `research/ring_n_plus_2_check/`. Create it and write nothing anywhere else.

## Background

We study the whole-board pawn game on the n-file cylinder C_n:
- 8 ranks;
- race rule "count";
- e.p. on;
- a pawn that can still be taken e.p. is not passed;
- the game ends at the first passed pawn.

A *ring* has a pawn on every file. The project's library is `cylcgt` (`cylcgt/pawns.py`). For the whole-board game,
set `pawns.components = lambda b, p: [p]`.

T50 proved that two wall families with n+3 pawns are *2 for every n. See `research/ring_family_proof/proof.tex`, with
the referee report in `research/ring_family_proof_check/`.

New claim: the family below is *2 in the whole-board game for every even n ≥ 8.

`P_n = W5 B7 W4 W4B7 B6 W3B6 (W2 B4)^((n-6)/2)`, with n+2 pawns.

Notation:
- One token per file; file a comes first.
- `W4B7` means a white pawn on rank 4 and a black pawn on rank 7.
- So P_8 is `W a5 c4 d4 f3 g2 / B b7 d7 e6 f6 h4`.

The proof is in `research/ring_n_plus_2_proof/PROOF.md`. It reuses T50's Lemmas 1–3 and adds new finite checks:
- the base reduced graph at n0 = 18 has 813 nodes and no e.p. flag;
- every node agrees with the start outside files {0, 2, 3, 4, 5, 6};
- the insertion cut is c = 12;
- the cases n < 18 are checked directly.

## What to do

1. **Read** `PROOF.md`, and `research/ring_family_proof/proof.tex` (Lemmas 1–3 and the theorem's proof) as a referee
   looking for a gap. In particular, check that every hypothesis of Lemmas 2 and 3 holds for P_n. That includes the
   wall's phase and its ends next to the core, the cut c = 12, and the claim that files 8..17 stay pattern files in
   every node.
2. **Reproduce** with the project's scripts. Do not edit them. From the project root, run
   `sh research/ring_n_plus_2_proof/run_all.sh` under `nice -n 15`. Compare every number in `logs/` with `PROOF.md`.
3. **Independent check by method.** Write your own program in your directory, in any language. Use ONLY the rules
   above and `cylcgt.pawns.passed` for the passed test. Do NOT read or copy `rg.c`, `cylcgt`'s value code, or the
   `verify*` directories. With it:
   - compute G+*h for h = 0..3 for P_n, n = 8..24 (signature NNPN means *2);
   - for n = 8, 10, 12, also check one ring that is NOT claimed to be *2 (for example P_n with the B7 on file b moved to
     B6), so the program is shown to tell the difference.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git. Do not edit `paper/` or any other directory.
- Write `REPORT.md` in your output directory:
  - begin with a 5-line summary;
  - give a verdict (SOUND / GAP / FALSE) for the proof, with reasons;
  - give the reproduced numbers and the results of step 3.
