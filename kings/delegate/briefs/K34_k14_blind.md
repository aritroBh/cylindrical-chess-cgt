# K34: blind proofs of the K14 two-shuttle results (Proposition 3.2′, Lemma 3.2″, Theorem 3.2‴), then comparison

**Output directory:** `kings/delegate/out/K34/` (it exists and holds `blind_packet.md`). Write only there. Do **not**
edit any existing file. Do not run git.

Proposition 3.2′ (two shuttling kings act as dud_D) and its chess bridge, Theorem 3.2‴, are labelled PROVED (the
bridge conditional on its hypotheses). Each proof is one AI proof (Claude family), re-checked by one referee of the
same family. Nobody outside the Claude family has checked them. You are that check, and the order of work is fixed.

## Phase 1: prove them blind

Read **only** `kings/delegate/out/K34/blind_packet.md`. It holds §1.2 (Definitions 1.1–1.5), Definition 2.1,
Lemma 2.2, Definition 2.5, Definition 3.1, Proposition 3.2, the setting and statement of the sharp form of Theorem
1.14, and the statements of Proposition 3.2′, Lemma B, Lemma 3.2″ and Theorem 3.2‴, without proofs. Do not open
`kings/theory/LOOPY.md` or anything under `kings/delegate/out/K14/` until Phase 1 is finished. You may cite Lemma 2.2,
Proposition 3.2 and the sharp form of Theorem 1.14 as given (they were checked elsewhere).

Write `PROOF.md` with your own complete proofs of:
1. Proposition 3.2′, every part, including the inequalities when one side has further Z-moves and the claim that a win
   needs only the states in which the winner's king stands still;
2. Lemma B;
3. Lemma 3.2″;
4. Theorem 3.2‴ (a) win transfer and (b) exactness, from the sharp form of Theorem 1.14.

Be explicit about:
- what you induce on (stages of least fixed points; D may be loopy);
- e.p. rights across a Z-move;
- check, checkmate and stalemate;
- which hypothesis is used at which step.

If you think a statement is false, give the smallest counterexample you can find, and check it by a brute-force program
written from the definitions (Python: `/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python`). For
Proposition 3.2′, also run a random test on small D-games G (at most 5 positions, loopy allowed): compare r(G ⊞ Z) with
r(G ⊞ dud_D) for a two-shuttle Z built as a 4-state D-game. Report the number of instances and the exact generator.

## Phase 2: compare

Only after `PROOF.md` is written, read `kings/theory/LOOPY.md` from "**Proposition 3.2′" to the end of the proof of
Theorem 3.2‴ (the line before "**Which hypotheses hold"). Then write `FINDINGS.md`:
- a 5-line summary;
- where your route differs;
- each proof step of LOOPY marked SOUND, GAP (give the missing step) or FALSE (give a counterexample);
- your random tests (commands, counts);
- your recommended labels.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Runs over about one CPU-minute go through `kings/delegate/heavy.sh` (nice 15).
Under 3 GB RSS and under 20 minutes per run. No file over 50 MB. No installs, no network. Never use pkill, killall,
`kill -- -1` or any pattern kill. Kill only PIDs you started and recorded.
