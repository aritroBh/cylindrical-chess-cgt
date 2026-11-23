# T83 — Re-read of two FINAL proof texts after their fixes (kings appendix A.10 to A.17; Möbius note)

Output directory: `delegate/out/T83/` (create it). Write `REPORT.md` there and any programs. Do not edit
anything else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs
you started and recorded yourself. At most 1 process at a time, under 3 GB, `nice -n 15` if your sandbox allows
it; total compute budget about 30 minutes. Other people's jobs run on this machine: leave them alone.
Do not copy raw terminal transcripts into your report, and do not write anything from your own memory of other
projects or any personal identifier (names, email addresses, home paths outside this repository) into it.

## Why
Both texts below were written by an AI model of one vendor, refereed (one of them by you, in an earlier run),
and then EDITED to apply the referees' fixes. Nobody from a different vendor has read the final wording. Your
job is to referee the texts exactly as they now stand, line by line, as a hostile reader. Do not assume an
earlier report was applied correctly; an edit may have introduced a new error. Form your own verdict first; only
then, if you wish, compare with the earlier reports (`delegate/out/T81/REPORT.md`, `delegate/out/T82/REPORT.md`).

## Text 1: `dist/tog/supp_src/s12a_core.tex`, items A.10 to A.17 (parts A.III and A.IV)
The self-contained proofs of: the buffer lemma (A.10), the validity theorem in chess (A.11) with remarks (A.12),
its corollary for the sum model (A.13), a proposition with a counterexample (A.14), the certificate (C1) to (C3)
with a remark on the paper's wording (A.15), the certificate theorem in the promotion game (A.16) and a remark
(A.17). They use A.1 to A.9 of the same file (definitions, Lemma A.2 on promotion and the potential, Theorem A.7
on sum safety); take A.1 to A.9 as given unless a use of them is wrong. Conventions fixed earlier in the file: in
the pawn games W and S a pawn that reaches its last rank stays a pawn and is passed under every test; part A.III
assumes at least five ranks.
For each item say CORRECT AS IT STANDS, CORRECT WITH A FIX (exact replacement LaTeX), or GAP / WRONG (smallest
counterexample or missing case). Check in particular:
1. A.11: every step of the strategy argument; the last paragraph on termination and on promotions before the
   first decisive event (it cites Lemma A.2(a) and A.2(c)); whether (V1) to (V3) as stated in this file are
   exactly what the proof uses; Remark A.12(a) to (d).
2. A.13: its statement is now per side to move, with a displayed example (king group `W Kb6 c7 / B Ka8 a5`,
   empty context) said to satisfy the hypotheses with Black to move only. Verify the example move by move
   (legal moves, checks, mate) and the claim about the empty sum.
3. (C1) to (C3) and A.16 after the rewording of (C3) ("a winning move of the local game ... with the moves that
   remain") and of Steps 1 to 4: is the guided strategy well defined at every turn; does Step 2 really show a
   winning move exists and is legal in the real position; do Steps 3 and 4 still follow; is any step still
   phrased for a single fixed strategy in a way that no longer matches (C3)?
4. A.15 quotes the 10-page paper's one-sentence definition of the certificate. Compare with the sentence in
   `dist/tog/sections/04_kings.tex` (search "certificate of horizon") and say whether A.15 describes it
   correctly and whether the paper's sentence is a fair summary of (C1) to (C3).
5. The last paragraph ("Where to find the longer treatment"): only for internal consistency of the numbering it
   quotes from the rest of Section S12 (`dist/tog/supp/s12.tex`): do the cited items exist there?

## Text 2: `dist/tog/supp_src/s15_note5.md` (the Möbius note as typeset in the supplement)
It proves that three families of pawn rings on the Möbius strip have value *2 for every width (rules in its
section 1). You refereed its source `research/mobius_rings_proof/PROOF.md` before; two wording fixes were then
applied and the note was cleaned for typesetting (program names and paths removed). Check that the typeset text
is still a complete and correct proof: the definition of pattern files (one wall, one phase), the view lemma V,
Lemmas 1 to 3, the invariant and the step, the theorem, and that every finite fact the proof uses (C1 at m = 5;
C2 for m < 5) is stated with its numbers and labelled honestly (how many independently written programs).
Report any sentence that the clean-up made false, ambiguous or unsupported (for example a reference to a
program or table that is no longer in the text). No recomputation is needed; if you still have a doubt about a
number, recompute only that one with your own code.

## Report
`delegate/out/T83/REPORT.md`: first line a verdict per text (FINAL TEXT SOUND / SOUND WITH FIXES / GAP). Then
Text 1 items in order and Text 2 sections in order, each finding as `file:line` with severity (BLOCKER, MAJOR,
MINOR) and the exact replacement text. Say plainly what you did not check.
