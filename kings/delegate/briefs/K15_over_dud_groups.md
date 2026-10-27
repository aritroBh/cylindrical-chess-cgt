# K15: search for over-type and dud-type king groups on the cylinder (Conjecture 4.7, open question 2)

**Output directory:** `kings/delegate/out/K15/` (create it). Write only there. Do **not** edit any existing file.
Do not run git.

## Background

`kings/theory/LOOPY.md` models king-and-pawn groups ("king groups" Z) as games. A group can be:
- frozen (value 0);
- `on` or `off`: one side has a safe king shuttle, which works as an endless pass;
- `dud`: both sides can pass;
- `over` = {0 | over}: Right can pass forever, and Left has exactly one move that takes away the shuttle and
  leaves a mutual zugzwang.

Read:
- §3: Definition 3.1, Proposition 3.2, Theorem 3.4 and Corollary 3.5;
- §4: Definition 4.4, Propositions 4.5 and 4.6, the "Chess reading of over", and **Conjecture 4.7**;
- §8 open question 2;
- Appendix A, "Group search".

The search behind Conjecture 4.7 covered only placements of ≤ 2 + 2 pawns on 3 (or 4) files of the 8×6 and 7×6
cylinders, with no passer at the root. It found no dud and no over group. Conjecture 4.7 says that over is
realisable on the cylinder with wider groups. Open question 2 asks whether dud groups exist without a pawn break.

## Task

1. **Classifier.**
   - Write your own classifier: Python with your own move generator, or C.
   - It places the two kings and the pawns of a candidate group on a few files of a cylinder, with no passer at
     the root (cylcgt `passed`, e.p.-aware).
   - It decides by one-ply tests whether each side has a safe shuttle and whether the group is frozen. A shuttle
     is safe when it is a non-capturing king move inside the group, legal in every context, and leads to a
     position where the same holds.
   - It labels each placement frozen, on, off, dud or over (or "other").
   - State the tests exactly in `REPORT.md`.
2. **Search.**
   - (a) ≤ 3 + 2 and ≤ 2 + 3 pawns on 3 files, and ≤ 3 + 3 on 3 files.
   - (b) ≤ 2 + 2 and ≤ 3 + 2 on 4 files.
   - Boards: cyl:8×6 and cyl:7×6. If cyl:8×8 fits inside the limits, add it.
   - Report counts per class.
3. **Confirmation.** For every dud or over candidate (up to 50 per class, chosen to be diverse):
   - put the group beside 3–6 small contexts G: a tempo pawn pair on separate files, a mutual zugzwang, a
     one-move context;
   - solve the whole position with kpsolve (exact, cap 2 where it fits, else cap 1) on the full board;
   - compare with the prediction of Theorem 3.4 (or Proposition 4.6 for over) for G ⊞ dud_D or G ⊞ over_D;
   - report agreements and disagreements.
4. **Build kpsolve privately:** `cc -O2 -o kings/delegate/out/K15/kp kings/kpsolve.c -lpthread`.
   - Run every batch through the shared lock:
     `kings/delegate/heavy.sh kings/delegate/out/K15/kp --board cyl:8x6 --cap 2 --threads 2 < in.txt > out.txt`.
   - It prints `<pos> | A B`: lower and upper results from White's point of view (W/L/D). With real kings, A
     and B differ when the cap is too small; then report the pair.
   - Check its memory on one position before you batch. Cap 2 on cyl:7×6 can need about 9 GB, which is too
     much: use cap 1 there.

## Deliverable

`REPORT.md`, starting with a 5-line summary. Then:
- the tests;
- the search counts per board and class;
- every dud and over candidate found, in full notation (or the first 50, with the count);
- the confirmation table;
- your verdict on Conjecture 4.7 and on open question 2. Label each PROVED / CHECKED-2 / COMPUTED-1 /
  CONJECTURE.

A clean "none found" is a valid result. State its boundary exactly.

## Rules

`delegate/COMMON.md`, rules 5 and 7. In addition:
- at most 2 heavy processes, always through `kings/delegate/heavy.sh`;
- under 3 GB RSS;
- at most 20 minutes per run;
- no file over 50 MB;
- no installs, no network.

Never use pkill, killall, `kill -- -1` or any pattern kill; kill only PIDs you started and recorded. Delete
bulk input and output batches when done; keep the scripts and a summary JSON.
