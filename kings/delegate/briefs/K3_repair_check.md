# K3: independent check of the repaired proofs in the A8 theory note

**Output directory:** `kings/delegate/out/K3/` (create it). Write only there.

`kings/theory/LOOPY.md` was revised by other AI models in answer to four referee reports
(`kings/theory/REVIEWS.md`). Its "Status after review" table, near the top, marks several results
**PROVED after repair**: the proof was rewritten, but nobody has checked the new proof. You are that check.
Assume each repaired proof is wrong until you have verified every step.

## For every result marked "PROVED after repair" (and every "FALSE as originally stated → … PROVED after repair")

1. Find the result and its proof in the note.
2. Check the following:
   - the statement now avoids the counterexample or defect the review item names;
   - every step follows, with no hidden hypothesis;
   - the proof is complete, not a sketch;
   - the label is right.
3. Try to break it: build a counterexample. Abstract games may be brute-forced in Python. Chess positions
   may be solved with the project's exact solver: build it with
   `cc -O2 -o kings/delegate/out/K3/kp kings/kpsolve.c`, then run
   `echo "<position> w -" | kings/delegate/out/K3/kp --board cyl:7x6 --cap 1 --threads 2`. Keep runs small
   (at most 5 pawns, boards up to 7×6): the machine is shared.
4. Give a verdict:
   - **SOUND**;
   - **GAP**: say what is missing;
   - **FALSE**: give a counterexample.

Pay most attention to these, which carry the note's main conclusions:
- Theorems 1.11(b), 1.11(c) and 1.14(ii);
- the sharp form of 1.14;
- Theorem 2.4(c);
- Theorem 2.7;
- Lemma 2.9;
- Theorem 4.2;
- Propositions 3.2 and 4.3;
- P11 and P12.

## Deliverables

- `kings/delegate/out/K3/REPORT.md`: a 5-line summary, then a table with one row per result (result,
  verdict, reason, counterexample if any).
- `kings/delegate/out/K3/EDITS.md`: exact edits that downgrade every label you could not verify. Use the
  format of `kings/delegate/briefs/K1_common_edits.md`: OLD copied exactly from LOOPY.md and unique in it,
  each change marked "(revised after K3 check)". Do not edit LOOPY.md itself.
