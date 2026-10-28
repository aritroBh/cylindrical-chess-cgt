# K35: blind proof of Theorem 2.11K (real-king square rule with a no-stalemate clause), then comparison

**Output directory:** `kings/delegate/out/K35/` (it exists and holds `blind_packet.md`). Write only there. Do **not**
edit any existing file. Do not run git.

Theorem 2.11K (K16) is labelled PROVED in P. It is one AI proof (Claude family), read step by step by one referee of the
same family. Nobody outside the Claude family has re-derived it. You are that check; the order of work is fixed.

## Phase 1: prove it blind

Read **only** `kings/delegate/out/K35/blind_packet.md` (the setting, notation, (H1)–(H5) and statement of Proposition
2.11, the P model, and the statement of Theorem 2.11K, without proofs), plus `cylcgt/pawns.py` (`passed`,
`ep_capturable`, `promote_distance`) and the header and move generator of `kings/kpsolve.c` if you need move rules.
Do not open `kings/theory/LOOPY.md` or anything under `kings/delegate/out/K10*/`, `K11*/`, `K16/` until Phase 1 is
finished. You may cite the statement of Proposition 2.11 (it was re-derived blind earlier, K11b) but not its proof;
if you need one of its proof steps, prove it yourself.

Write `PROOF.md`, your own complete proof that β wins P from (y, s) by Π under the hypotheses of Theorem 2.11K, and
your own proof that (H3K) implies (NS). Cover: why no ω pawn can capture or block p; why ω's king cannot capture p
(the role of (SQ), including the square skipped by a double step); why β is never in check and every push is legal;
why ω always has a legal move or is mated; why ω cannot promote first, given that ω's king may capture β's other
pawns; and e.p.

If you think the statement is false, give a counterexample and check it with kp_p (`--pmodel`). Build it privately:
`cc -O2 -o kings/delegate/out/K35/kpp kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread`; run batches through
`kings/delegate/heavy.sh` at nice 15. Optionally test the statement on random positions of cyl:6×6 or 7×6 with your own
hypothesis checker (report the generator and counts).

## Phase 2: compare

Only after `PROOF.md` is written, read LOOPY's block from "**Real-king square rule" to the end of the Theorem 2.11K
bullet (including its proof and "(H3K) ⟹ (NS)"). Write `FINDINGS.md`: a 5-line summary; where your route differs;
each step of LOOPY's proof (F1)–(F3), Steps 1–5 and (H3K) ⟹ (NS) marked SOUND, GAP (give the missing step) or FALSE
(give a counterexample); your tests; your recommended label.

## Rules

`delegate/COMMON.md`, rules 5 and 7. At most 2 heavy processes, always through `kings/delegate/heavy.sh`; under 3 GB
RSS; at most 20 minutes per run; no file over 50 MB; no installs, no network. Never use pkill, killall, `kill -- -1` or
any pattern kill; kill only PIDs you started and recorded. Delete binaries at the end.
