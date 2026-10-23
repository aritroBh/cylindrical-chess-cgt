# K10v: independent check of Proposition 2.11 (frozen-king passer certificate)

**Output directory:** `kings/delegate/out/K10v/` (create it). Write only there. Do **not** edit any existing file.

## Read

- `kings/theory/LOOPY.md`: **Proposition 2.11**, Corollaries 2.11a and 2.11b, the remark on the count rule, and
  the list of examples after them. Search for "Proposition 2.11 (frozen-king passer certificate)". Also read the
  status rows R2.11 and P11, and the §6 row P11.
- `cylcgt/pawns.py`: `passed`, `promote_distance`, `ep_capturable` and `_child` (the race rule "count").
- `kings/kpsolve.c`: the header comment and `--frozen`.

**Independence.** Do not open anything in `kings/delegate/out/K10/`: not its scripts, its reports or its edits.
Write your own code.

## Task

1. **Re-derive the proof.** Go through Steps 0–5 of the proof of Proposition 2.11. For each step:
   - say SOUND, or give the missing step or a counterexample;
   - check the invariants (J_β), (J_ω) and (I1) under every kind of ω move: push, double step, capture into the
     strip from outside, capture out of the strip, and the e.p. capture offered at y;
   - check the claim of Step 4 that every ω move of the real play is a move of G_ω;
   - check the timing in Step 5 for both move orders.

   Then check Corollary 2.11a against cylcgt's `_child`: who is credited, for both move orders and for races.
   Check Corollary 2.11b for the layout `Ka1 ka6`, cyl:8×6, pawns on c–g.
2. **Independent computation.**
   - Write a checker (Python, at most about 250 lines, your own move generator). For a position y, a side to move
     s, a beneficiary β and a pawn p, it decides (H1)–(H5) exactly as LOOPY states them, including μ_ω computed
     by search over G_ω.
   - Self-test your `passed` against cylcgt's `passed` on random positions.
   - Build kpsolve: `nice -n 10 cc -O2 -o kings/delegate/out/K10v/kp kings/kpsolve.c -lpthread`. Batch positions
     on stdin: `nice -n 10 kings/delegate/out/K10v/kp --board cyl:7x6 --frozen --cap 1 --threads 2 < in.txt`.
     It prints `<pos> | X Y`: the two letters are results from **White's** point of view (W/L/D).
   - Run these, and for each, every instance where (H1)–(H5) hold must be a win for β in `--frozen`:
     - (a) cyl:6×6, all positions with `Ka1 ka6`, pawns on files c–e, at most 3 a side, both sides to move, both
       colours as β;
     - (b) cyl:7×6, the same layout with pawns on c–f, at most 2 a side, plus 20,000 random positions with 3 a side;
     - (c) cyl:8×6, 10,000 random positions with kings anywhere (legal, not in contact), at most 3 pawns a side,
       e.p. rights included where legal.
   - Report instances, certified instances, and violations, with up to 10 examples of each violation.
   - Also report, for each of (H2), (H3), (H4) and (H5), how many violations appear when that hypothesis is
     dropped. This is a control that your checker can see failures.
3. **Targeted search for counterexamples.** Look specifically at:
   - (H4) at its bound, ρ(q) = ρ(p) + 1;
   - an e.p. right at y, both for p's own pawns and for another β pawn;
   - ω captures that enter the strip;
   - β to move with an ω pawn at ρ(p) + 1 beside p.

   Report what you tried and what you found.

## Deliverables

`REPORT.md`, starting with a 5-line summary. Then:
- the per-step verdicts on the proof;
- the tables for 2(a)–(c);
- the targeted search;
- a recommended label for Proposition 2.11 and for P11.

Use CHECKED-2 only if both the proof check and the computation agree. Give exact commands.

## Rules

`delegate/COMMON.md`:
- rule 5 (labels, honesty);
- rule 7: one heavy process at a time, `nice -n 10`, under 3 GB RSS, at most 20 minutes per run, no file over
  50 MB, no git, no installs, no network.

Never use pkill, killall, `kill -- -1` or any pattern kill. Kill only PIDs you started and recorded.

When you are done, delete your own bulk files: the kpsolve input and output batches. Keep the scripts and a
summary JSON.
