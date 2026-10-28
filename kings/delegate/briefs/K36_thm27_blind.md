# K36: blind proof of Theorem 2.7 (sufficiency of the local certificate LC_T, in P), then comparison

**Output directory:** `kings/delegate/out/K36/` (it exists and holds `blind_packet.md`). Write only there. Do **not**
edit any existing file. Do not run git.

Theorem 2.7 (a) and its window form (b) are labelled "PROVED after repair (in P)". The repair (K7) is one AI proof
(Claude family). Its first draft of (b) was false (no e.p. clause in (L2)), and the corrected text has not been read
again by anyone. You are an independent check from outside the Claude family; the order of work is fixed.

## Phase 1: prove it blind

Read **only** `kings/delegate/out/K36/blind_packet.md`: §1.2 (Definitions 1.1–1.5, the models C, P, D, F), Definition
2.1, Lemma 2.2, Definitions 2.5 and 2.6 (the certificate LC_T with (L1), (L2), (L3), the projection π and Q_Z), and the
statement of Theorem 2.7, without proofs. You may also read `kings/SPEC.md` and the header and move generator of
`kings/kpsolve.c` for the move rules. Do not open `kings/theory/LOOPY.md` or anything under `kings/delegate/out/K7/`,
`K3/` or `K24/` until Phase 1 is finished.

Write `PROOF.md`, your own complete proof of (a) and of (b). Cover explicitly: how s̄'s strategy is built from the local
win of (L1) and the property (L3); why every s move outside Z is accounted for by (L2) (context promotions, context
passers, and an e.p. right with its target off F_Z); checks, stalemate and mate; captures that change Q_Z; why the win
takes at most T moves after r; and where each hypothesis of (b) (chess-legal, empty buffer, no officer, s̄'s king on
F_Z, no s̄ context pawn attacking s's king) is used. If you find that a hypothesis is missing, give a counterexample and
check it with the P solver `kings/delegate/out/K7/scripts/draft/kp_p.c` (build privately with `cc -O2 -o
kings/delegate/out/K36/kpp ... -lpthread`, run with `--pmodel` through `kings/delegate/heavy.sh` at nice 15).

## Phase 2: compare

Only after `PROOF.md` is written, read LOOPY's proof of Theorem 2.7 (from "**Theorem 2.7" to the end of "**Remark (K3's
objection, answered)**") and the list "The conditions cannot be dropped". Write `FINDINGS.md`: a 5-line summary; where
your route differs; each step of LOOPY's proof marked SOUND, GAP (give the missing step) or FALSE (give a
counterexample); any test you ran (commands, counts); your recommended label.

## Rules

`delegate/COMMON.md`, rules 5 and 7. At most 2 heavy processes, always through `kings/delegate/heavy.sh`; under 3 GB
RSS; at most 20 minutes per run; no file over 50 MB; no installs, no network. Never use pkill, killall, `kill -- -1` or
any pattern kill; kill only PIDs you started and recorded. Delete binaries at the end.
