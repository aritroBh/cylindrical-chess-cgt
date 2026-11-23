# T82 — Referee: proof that three Möbius ring families are *2 for every width

Output directory: `delegate/out/T82/` (create it). Write `REPORT.md` there and your programs. Do not edit
anything else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs
you started and recorded yourself. At most 2 processes at once, each under 3 GB, `nice -n 15` if your sandbox
allows it; total compute budget about 90 minutes. Other people's jobs run on this machine: leave them alone.
Do not copy raw terminal transcripts into your report, and do not write anything from your own memory of other
projects or any personal identifier (names, email addresses, home paths outside this repository) into it.

## What to referee

`research/mobius_rings_proof/PROOF.md` (written by one AI model, not yet read by anyone else). It claims: in the
whole-board pawn game on the Möbius strip with n files and 8 ranks (rules in its section 1 and in
`research/mobius_rings/REPORT.md`, "Rules as implemented"), the rings

- F1(m) = `(B4 W2)^m B6 W2 W3 B6 B7 W3 B7 W5`, n = 2m+8, m >= 1,
- F2(m) = F1(m) followed by `B7`, n = 2m+9, m >= 1,
- F3(m) = `B6 W2 W3 B6 B7 W3 (B7 W5)^m W6B7`, n = 2m+7 (n+1 pawns), m >= 0,

have value *2 (same outcome as *2 + *h against every nim-heap *h). Ring notation: one entry per file, left to
right; the seam joins the last file to the first, with ranks flipped r -> 9-r and pawn direction reversed.

The proof is an induction on m by inserting two wall files (Lemma 3), with base m = 5 from one computation (C1)
and m < 5 by direct computation (C2).

## Tasks

A. **Read the hand proofs as a hostile referee** (sections 1, 3, 4, 6: view lemma V, Lemmas 1, 2, 3, the step,
   the theorem). For each lemma say CORRECT, CORRECT WITH A FIX (give the exact replacement text), or GAP / WRONG
   (give the smallest counterexample or the missing case). Check in particular:
   1. Lemma 2(b): is the reply capture always legal and is the capturer always passed, for both moves W2->3 and
      W2->4 (en passant) and for B4->3, in both wall types, and in both window orientations (j-1..j+3 and
      j-3..j+1)? Does X really have no passed pawn after the reply?
   2. Lemma 3 (ii) and (iii): the bookkeeping of which files a far move or a far reply can change (including a
      capture across the seam and an en passant capture), and whether files c, c+1 stay pattern files so that
      the insertion commutes with the move. Is every pawn either "central"/"near" or "far" in each case, with
      no file falling between the two definitions?
   3. The cut for F1 and F2 is c = 4, so the arc is files 0..9 and its end file 0 is a seam neighbour. Does any
      step use a view of file 0 as if it were a chart view? Would c = 5 (base m = 6) be needed instead?
   4. The step in section 4: does the invariant I_m (no flag in any reduced node; every node equals the start
      outside the zone) really carry from m to m+1, and is ins_c(start_m) = start_{m+1} for the stated cut?
   5. Lemma 1 (reduction) and the last paragraph of the theorem (h >= 3).
B. **Recompute the base independently.** Write your own program from the rules text (PROOF.md section 1 and
   `research/mobius_rings/REPORT.md`); do NOT read, import or run `research/mobius_rings_proof/mgame.py`,
   `rgraph.py`, or any solver under `research/mobius_rings*/`. For each family at m = 5 (and, if cheap, m = 0..7)
   build the reduced game (nodes reachable from the start by K-moves; classes T, L, P, K as defined in
   section 1) and report: number of nodes, K-edges, T-moves, nodes with an e.p. flag, nodes with a passed pawn,
   the set of files that ever differ from the start (the zone), and the outcome string of R + *h for h = 0..4.
   PROOF.md section 5 claims for m = 5: F1 435 / 1118 / 404, zone {10..15}; F2 417 / 1082 / 356, zone {10..15};
   F3 435 / 1112 / 428, zone {0..5}; 0 flagged, 0 with a passer; NNPNN. State agree or disagree for each number.
   If your counts differ, find out whether it is a convention (e.g. how T-moves or edges are counted) or a
   real difference, and say which.
C. **Solve the unreduced game** F(m) + *h, h = 0..3, for as many small m as your budget allows (at least
   m = 0, 1, 2 for each family), and compare with: F1(0) RNRR, F2(0) NNRR, all others NNPN.
D. **Attack Lemma 3.** With your own program, sample random strip positions that satisfy its hypotheses (no
   passed pawn, no flag, ten consecutive chart files c-4..c+5 holding an alternating W2/B4 or B7/W5 wall,
   anything on the other files) and test its conclusion (K-children and T-flag of ins_c(p) are the images of
   those of p). Report the number tested, how many had a pawn able to capture across the seam, and every
   failure. Then weaken one hypothesis (for example a wall of 6 files) and report whether failures appear, to
   show the test can fail.

## Report

`delegate/out/T82/REPORT.md`: a verdict line first (PROOF HOLDS / HOLDS WITH FIXES / DOES NOT HOLD), then tasks
A to D in order, each finding as `PROOF.md:line` with the exact replacement text where a fix is needed, then the
exact commands to rerun your programs. Say plainly what you did not check.
