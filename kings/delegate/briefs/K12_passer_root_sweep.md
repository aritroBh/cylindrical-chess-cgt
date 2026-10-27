# K12: end-to-end sweep of P11's root clause (roots that already have a passer)

**Output directory:** `kings/delegate/out/K12/` (create it). Write only there. Do **not** edit any existing file.
Do not run git.

## Background

`kings/theory/LOOPY.md` proves Proposition 2.11, a passer certificate for the frozen-king model F
(`kpsolve --frozen`). Prediction P11 says `--frozen` = o(W(X)) for every root X of the layout whose passer and
race terminals are all certified. W(X) is the whole-board D-game, which ends at the first passer.

A second-round review found that P11 had left out roots X that **already** have a passer. There, W(X) ends at
the root, so Corollary 2.11a (which covers nodes reached by a move) says nothing. Example: on cyl:8×6,
`Ka1 ka6 Pc2 Pd4 pd3 b -` is a White win in W(X) (Pd4 is passed), but `--frozen` gives (L, L).

P11 now requires that such a root itself satisfy Proposition 2.11, with s the side to move and β the side W(X)
credits. The earlier end-to-end checks covered only roots **without** a passer. Your job is the sweep over roots
**with** a passer.

## Read

- `kings/theory/LOOPY.md`:
  - Proposition 2.11: search for "Proposition 2.11 (frozen-king passer certificate)". Read the Setting,
    Notation, G_ω, (H1)–(H5) and the Statement.
  - Corollaries 2.11a and 2.11b.
  - The status row P11 and the §6 row P11 (search for "| P11 | cyl:8x6").
- `cylcgt/pawns.py`: `value` (a single passer at the root gives ±BIG; a race at the root raises `RaceError`),
  `_child` (the count rule), `passed` with `PASSED_RESPECTS_EP = True`, `promote_distance`, `ep_capturable`.
- `kings/kpsolve.c`: the header comment and `--frozen`.

**Independence.** Do not open `kings/delegate/out/K10/`, `K10v/` or `K10r2/`. Write your own (H1)–(H5) checker,
with your own move generator and your own search for μ_ω over G_ω. You may import cylcgt for `passed`,
`promote_distance` and `value` only.

## Task

1. **The position class.** The layout is `Ka1` plus the black king on the top rank of the a-file, the b-file and
   the last file empty, and pawns only on files c … W−2. Take:
   - (a) cyl:6×6, files c–e, at most 3 pawns a side;
   - (b) cyl:7×6, files c–f, at most 3 a side (if this cannot finish inside the limits, use at most 2 a side and
     say so);
   - (c) cyl:8×6, files c–g, at most 2 a side.

   Use both sides to move, legal positions only (the side not to move is not in check), and e.p. rights wherever
   they are legal, as their own instances. State the class exactly in `REPORT.md`.
2. **Roots with a passer.** Enumerate every position of the class in which at least one side has a passer
   (cylcgt `passed`, e.p.-aware). Split them:
   - **single** (exactly one side has a passer), where o(W(X)) credits that side;
   - **race** (both sides have one). cylcgt has no root value here. Report race roots separately. For them, use
     Corollary 2.11a's rule with N the side to move: b = N if dp(N) ≤ dp(M), else b = M. Treat the result as an
     extension of the convention to the root, and label it as such.
3. **For every root:**
   - compute the `--frozen` result;
   - decide whether the root satisfies (H1)–(H5) for some pawn p of β (β the credited side, s the side to move);
   - classify the root:
     - certified and `--frozen` agrees: fine;
     - **certified and `--frozen` disagrees: a violation of Proposition 2.11.** Expect none. List every one in
       full;
     - uncertified and agrees;
     - uncertified and disagrees: P11's root clause is needed here. Give counts, and up to 20 examples;
     - for race roots, the same four classes.
4. **Controls.**
   - Self-test your `passed` against cylcgt's on every root.
   - Repeat the sweep with (H4) dropped, and again with (H5) weakened to μ_ω ≥ e. This shows that your checker
     can see failures.
5. **kpsolve.**
   - Build it privately: `cc -O2 -o kings/delegate/out/K12/kp kings/kpsolve.c -lpthread`.
   - Run every batch through the shared lock:
     `kings/delegate/heavy.sh kings/delegate/out/K12/kp --board cyl:6x6 --frozen --cap 1 --threads 2 < in.txt > out.txt`.
   - It prints `<pos> | A B`: two bounds, equal in `--frozen`, from White's point of view (W/L/D). Position
     syntax as in LOOPY's examples, e.g. `Ka1 ka6 Pc2 Pd4 pd3 b -` (e.p. square in place of the last `-`).
   - Keep input batches under 50 MB.

## Deliverable

`REPORT.md`, starting with a 5-line summary. Then:
- the exact class and the passed test used;
- a table per board: roots, single, race, certified, and each of the four classes;
- every violation, in full notation;
- examples;
- the controls;
- an exact reproduce command for every number;
- the recommended label for P11's root clause: CHECKED-2 if your counts are reproduced by a second implementation
  of your own (for example, μ_ω by a second, brute-force search), otherwise COMPUTED-1.

Keep the scripts and a summary JSON. Delete the kpsolve input and output batches when you are done.

## Rules

`delegate/COMMON.md`, rules 5 and 7. In addition:
- at most 2 heavy processes, always through `kings/delegate/heavy.sh`;
- under 3 GB RSS;
- at most 20 minutes per run;
- no file over 50 MB;
- no installs, no network.

Never use pkill, killall, `kill -- -1` or any pattern kill; kill only PIDs you started and recorded.
