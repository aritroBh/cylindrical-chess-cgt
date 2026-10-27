# K11: non-Claude re-derivation of Proposition 2.11 (frozen-king passer certificate) and of P11

**Output directory:** `kings/delegate/out/K11/` (create it). Write only there. Do **not** edit any existing file.
Do not run git.

You are the first referee of this proof from outside the Claude family. A Claude (Sonnet) agent wrote the proof.
Two more Sonnet reviewers found no error in it, and computations found no counterexample. What is missing is a
**written re-derivation** by a different model. A bare "SOUND" verdict is not enough: an earlier referee gave one
without a derivation, and it was not accepted.

## Read

- `kings/theory/LOOPY.md`:
  - **Proposition 2.11**: search for "Proposition 2.11 (frozen-king passer certificate)". Read the Setting,
    Notation, G_ω, (H1)–(H5), the Statement, and Steps 0–5 of the proof.
  - Corollaries 2.11a and 2.11b, the remark on the count rule, and the examples after them.
  - The status rows R2.11 and P11 (near the top), and the §6 row P11 (search for "| P11 | cyl:8x6").
  - Theorem 1.14 (search for "Theorem 1.14 (validity of the convention)"): hypotheses (V1)–(V4) and the proof of (i).
  - Theorem 1.11(c) and its hypothesis (HSS).
- `cylcgt/pawns.py`: `passed`, `PASSED_RESPECTS_EP`, `ep_capturable`, `promote_distance`, `_child`, the root
  terminal test, and the race rule "count".
- `kings/kpsolve.c`: the header comment, `--frozen`, and the move generator (e.p., checks, legality).

**Independence.** Do not open `kings/delegate/out/K10/`, `K10v/` or `K10r2/`. Write your own code.

## Task

1. **Write the proof yourself.**
   - In `REPORT.md`, write a complete proof of Proposition 2.11 in your own words. Do not paraphrase LOOPY's text.
   - For each of Steps 0–5, say whether your argument agrees with LOOPY's. Mark the step SOUND, GAP (give the
     missing step) or FALSE (give a counterexample).
   - Check each of these explicitly:
     - the invariants (J_β), (J_ω) and (I1) under every kind of ω move: push, double step, capture landing
       inside the strip (from outside it or within it), capture leaving the strip, and the e.p. capture offered
       at y;
     - that p is never captured, including en passant after its own double step;
     - king safety (Step 1): (H2) means β is never in check, and (H3) means ω always has a legal move;
     - Step 4: every ω move of the real play is a move of G_ω;
     - the timing in Step 5 for both move orders, e = d and e = d − 1;
     - why H ≥ 5 is needed;
     - the legality assumption on y.
2. **Corollaries.**
   - Check Corollary 2.11a against cylcgt: who is credited at a terminal reached by a move, for single passers and
     races under the count rule, in both move orders.
   - Check Corollary 2.11b for the layout `Ka1 ka6`, cyl:8×6, every pawn on c–g.
3. **P11 as now amended.**
   - Does Theorem 1.14(i), together with Corollary 2.11a at every terminal reached by a move and Proposition 2.11
     at a root that already has a passer, prove `--frozen` = o(W(X))?
   - Is any case still missing? For example: a root with a race, a root where the side to move is in check, a
     root with an e.p. right, terminals that are king moves, or the role of condition (E).
   - Give a counterexample for any gap, verified with kpsolve.
4. **Your own computation (small).**
   - Test any step you doubt. Use a checker of your own, at most about 250 lines.
   - Build kpsolve privately:
     `cc -O2 -o kings/delegate/out/K11/kp kings/kpsolve.c -lpthread`.
   - Run every batch through the shared lock:
     `kings/delegate/heavy.sh kings/delegate/out/K11/kp --board cyl:8x6 --frozen --cap 1 --threads 2 < in.txt > out.txt`.
     It prints `<pos> | A B`: two bounds, equal in `--frozen`, from White's point of view (W/L/D).
   - Report exact counts and exact commands.

## Deliverable

`REPORT.md`, starting with a 5-line summary. Then:
- your written proof;
- the per-step verdicts;
- the corollaries;
- P11;
- your computations;
- your recommended labels for Proposition 2.11 and P11.

## Rules

`delegate/COMMON.md`, rules 5 and 7. In addition:
- at most 2 heavy processes, always through `kings/delegate/heavy.sh`;
- under 3 GB RSS;
- at most 20 minutes per run;
- no file over 50 MB;
- no installs, no network.

Never use pkill, killall, `kill -- -1` or any pattern kill; kill only PIDs you started and recorded. When you
are done, delete your kpsolve input and output batches, and keep the scripts and a summary.
