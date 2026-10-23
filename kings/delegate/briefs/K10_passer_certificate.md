# K10: a certificate for passers (Remark 2.11), and the status of P11

**Output directory:** `kings/delegate/out/K10/` (create it). Write only there. Do **not** edit
`kings/theory/LOOPY.md`; propose edits instead (format below).

## Read first

`kings/theory/LOOPY.md`:
- the status table, rows R2.11 and P11;
- Definitions 1.1–1.5, especially the promotion model P and the D-model, where a passer is a decisive event;
- Definition 2.6 (the certificate LC_T) and Theorem 2.7 with its proof. They are freshly repaired; this task
  is the analogue for passers;
- Corollary 2.8 (the square-rule form);
- **Remark 2.11** (GAP: why the certificate does not apply to passers as written);
- §6 row P11, and the rule "(V2) decisiveness" in Theorem 1.14.

Also read `cylcgt/pawns.py`: `passed`, `promote_distance`, the race rules and `PASSED_RESPECTS_EP`. In a
D-model sum, "a passer appears" is exactly cylcgt's `passed` becoming true for one side.

## Task

1. **Frozen-king passer certificate. State it and prove it, in P.** This is the model of
   `kpsolve --frozen`: any king move loses at once, and the first promotion wins. A move of σ, or a capture by
   σ̄, creates a passer for σ: a pawn p that `passed` (e.p.-aware) calls passed.
   - Give exact conditions under which σ then wins in P:
     - p's promotion distance d, counting the double step and own pawns in front;
     - the defender's fastest promotion μ, from σ̄'s pawn moves only, with σ's other pawns standing still
       (captures allowed, double steps and e.p. included);
     - who moves next;
     - no stalemate of σ̄: under `--frozen` a king move is legal but loses, so stalemate means no pawn move and
       no king move at all;
     - races: both sides passed.
   - Prove the conditions step by step. Show that:
     - no σ̄ pawn can ever block or capture p: say exactly which files and ranks "passed" rules out, including
       the cylinder wrap;
     - σ's strategy "push p every move" is legal and wins the count, with an exact parity argument;
     - e.p. cannot rescue σ̄ (a just-double-stepped p is not passed under the e.p.-aware test);
     - σ's own pawns cannot get in p's way.
   - Prove the conditions sharp with small examples. You may use kpsolve:
     `cc -O2 -o kings/delegate/out/K10/kp kings/kpsolve.c`, then
     `echo "<pos> w -" | nice -n 10 kings/delegate/out/K10/kp --board cyl:8x6 --frozen --cap 1 --threads 2`.
2. **Relation to the D-model and cylcgt's race rule "count".** Show where your condition coincides with the count
   rule (`RACE_RULE = "count"`, `promote_distance`) and where it differs.
3. **Real kings.** State the square-rule analogue: the defender's king cannot catch p. Model it on Corollary 2.8,
   with the passer owner as the punisher. Prove it, or say precisely what remains open.
4. **P11.** With item 1 proved, decide whether P11's theoretical backing is now complete in P (Theorem 1.11 +
   Theorem 1.14 + the frozen passer certificate, plus HSS for the o(S) part). Give the label P11 should carry.

## Deliverables

- `REPORT.md`, starting with a 5-line summary: the statements, proofs, sharpness examples (with kpsolve
  commands) and proposed labels.
- `EDITS.md` with exact edits to `kings/theory/LOOPY.md` in the format below. Mark every change
  "(revised after K10, 2026-10-22)". Edit only:
  - Remark 2.11, which you may turn into a Proposition followed by a remark;
  - the status rows R2.11 and P11;
  - the §6 row P11;
  - the §0 table row for 2.11, if one exists.

  Each OLD block must be copied exactly from the file and occur exactly once in it:

      ### EDIT n: <title>
      <<<<<<< OLD
      <exact text>
      =======
      <replacement>
      >>>>>>> NEW

- Check the edits with
  `python3 kings/delegate/apply_edits.py kings/theory/LOOPY.md kings/delegate/out/K10/LOOPY_preview.md kings/delegate/out/K10/EDITS.md`
  and report "applied n, rejected 0".

## Rules

Follow `delegate/COMMON.md`:
- rule 5 (labels: say exactly what is PROVED and what is not);
- rule 7 (one process at a time, under `nice -n 10` and 3 GB). Never use pkill, killall or any pattern kill.
