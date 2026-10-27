# K11b: blind proof of Proposition 2.11 (frozen-king passer certificate), then comparison

**Output directory:** `kings/delegate/out/K11b/` (create it). Write only there. Do **not** edit any existing
file. Do not run git.

An earlier attempt (K11) was rejected: it copied the note's proof almost word for word. This time the order of
work is fixed.

## Phase 1: prove it blind

Read only the following:

1. In `kings/theory/LOOPY.md`, from the line starting "*Setting.* F is the frozen promotion model" down to the
   line "**Statement.** Under (H1)–(H5), β wins F …". That is the Setting, the Notation, the ω-only game G_ω, and
   the hypotheses (H1)–(H5). Find it with `grep -n "Setting.\* F is the frozen" kings/theory/LOOPY.md` and
   `grep -n "Statement.\*\* Under (H1)" kings/theory/LOOPY.md`, then print only that line range.
   **Do not print or read anything after the Statement line**, or anything between the Proposition's title and
   the Setting, until Phase 1 is finished.
2. `cylcgt/pawns.py`: `passed`, `ep_capturable`, `promote_distance`.
3. `kings/kpsolve.c`: the header comment and the move generator. Check how `--frozen`, e.p., checks and
   stalemate work.

Then write `PROOF.md`, your own complete proof of the Statement. Make it detailed enough that a referee can check
every case:
- what can and cannot happen to p: captured, blocked, taken en passant;
- why β's moves are always legal;
- why ω always has a legal move;
- a bound on how fast ω can promote, and why it applies in the real play;
- the timing for both sides to move.

Where you need a hypothesis, say which one. If you think the Statement is false, give a counterexample and
check it with kpsolve. If you think a hypothesis is not needed, say so and test it.

Build kpsolve privately: `cc -O2 -o kings/delegate/out/K11b/kp kings/kpsolve.c -lpthread`. Run every batch
through the shared lock:

```
kings/delegate/heavy.sh kings/delegate/out/K11b/kp --board cyl:8x6 --frozen --cap 1 --threads 2 < in.txt > out.txt
```

It prints `<pos> | A B`: two bounds, equal in `--frozen`, from White's point of view (W/L/D). Example position:
`Ka1 ka6 Pc2 Pd4 pd3 b -` (an e.p. square replaces the last `-`).

## Phase 2: compare

Only after `PROOF.md` is written, read LOOPY's proof (Steps 0–5), Corollaries 2.11a and 2.11b, the status rows
R2.11 and P11, and the §6 row P11. Write `REPORT.md`:
- a 5-line summary;
- where your proof and LOOPY's differ in route;
- whether LOOPY's proof has a step yours does not need, or a gap yours avoids. Mark each of Steps 0–5 SOUND,
  GAP (give the missing step) or FALSE (give a counterexample);
- Corollary 2.11a against cylcgt's `_child` (race rule "count");
- whether P11 as amended (Corollary 2.11a at terminals reached by a move, Proposition 2.11 at a root that
  already has a passer) is complete;
- your recommended labels.

Do not open `kings/delegate/out/K10*/`, `K11/` or `K12/`.

## Rules

`delegate/COMMON.md`, rules 5 and 7. In addition:
- at most 2 heavy processes, always through `kings/delegate/heavy.sh`;
- under 3 GB RSS;
- at most 20 minutes per run;
- no file over 50 MB;
- no installs, no network.

Never use pkill, killall, `kill -- -1` or any pattern kill; kill only PIDs you started and recorded. Delete
your kpsolve batches when done.
