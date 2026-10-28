# K37: blind proof of Lemma 2.9 (blockade, under (B1)), then comparison

**Output directory:** `kings/delegate/out/K37/` (it exists and holds `blind_packet.md`). Write only there. Do **not**
edit any existing file. Do not run git.

Lemma 2.9 is labelled "PROVED after repair, under the hypothesis (B1)". K22 showed that the old statement was false
without an added hypothesis and proved it under the weaker (B1). That proof is one AI proof (Claude family), re-checked
by one referee of the same family. You are an independent check from outside the Claude family; the order of work is
fixed.

## Phase 1: prove it blind

Read **only** `kings/delegate/out/K37/blind_packet.md`: §1.2 (Definitions 1.1–1.5), Definition 2.1, Lemma 2.2,
Definitions 2.5 and 2.6 (the local game L_T(Q_Z), the readings (L1) and (L1_P)), and the statement of Lemma 2.9,
without proofs. You may also read `kings/SPEC.md` and the header and move generator of `kings/kpsolve.c` for move rules.
Do not open `kings/theory/LOOPY.md` or anything under `kings/delegate/out/K22/` until Phase 1 is finished.

Write `PROOF.md`, your own complete proof that s has a strategy in Q_Z against which no s̄ pawn ever promotes and s is
never mated. Cover explicitly: captures by and of s̄ pawns, including e.p. (an e.p. right carried by Q_Z was created by
s̄); s's king in check; what (B1) excludes and why one attacked s̄ pawn is harmless; s̄'s king approaching s's king; why
s may pass whenever needed; and boards with H = 4 and H ≥ 5. Test the lemma by brute force on small boards with your own
local-game solver written from Definition 2.6 (Python: `/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python`;
for example flat and cylinder boards of width 3–5 and height 5–6, all placements satisfying the hypotheses up to a
stated size). Report the generator, the counts and every counterexample. If the lemma is false, give the smallest
counterexample.

## Phase 2: compare

Only after `PROOF.md` is written, read LOOPY's proof of Lemma 2.9 and the Remark after it ("K22: the hypothesis (B1) is
needed, and it is not necessary"). Write `FINDINGS.md`: a 5-line summary; where your route differs; each step of
LOOPY's proof marked SOUND, GAP (give the missing step) or FALSE (give a counterexample); your tests (commands, counts);
your recommended label.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Runs over about one CPU-minute go through `kings/delegate/heavy.sh` (nice 15).
Under 3 GB RSS and under 20 minutes per run; no file over 50 MB; no installs, no network. Never use pkill, killall,
`kill -- -1` or any pattern kill; kill only PIDs you started and recorded.
