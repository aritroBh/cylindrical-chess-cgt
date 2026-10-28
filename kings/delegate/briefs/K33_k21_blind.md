# K33: blind proofs of the K21 sum theorems (Lemma 3.8a, Theorems 3.7, 3.8, 3.11), then comparison

**Output directory:** `kings/delegate/out/K33/` (it exists and holds `blind_packet.md`). Write only there. Do **not**
edit any existing file. Do not run git.

The K21 theorems on sums with loopy components are labelled PROVED. Each is one AI proof (Claude family), re-derived by
one referee of the same family. Nobody outside the Claude family has checked them. You are that check, and the order of
work is fixed.

## Phase 1: prove them blind

Read **only** `kings/delegate/out/K33/blind_packet.md`. It holds Definitions 1.1–1.4, 1.10 and 3.1, the statement of
Theorem 1.11 (the short case), the conventions of the loopy section, and the statements of Theorem 3.7, Lemma 3.8a,
Theorem 3.8 (main statement) and Theorem 3.11, without proofs. Do not open `kings/theory/LOOPY.md` or anything under
`kings/delegate/out/K21/` until Phase 1 is finished. KNOWN results of loopy CGT (Siegel, *Combinatorial Game Theory*,
2013, ch. VI) may be cited by name.

Write `PROOF.md` with your own complete proofs of:
1. Theorem 3.7 (the loopy bridge);
2. Lemma 3.8a (subadditivity of the reserve, and monotonicity in the number of tokens);
3. Theorem 3.8 (the reserve criterion: the stated bounds imply first-event dominance);
4. Theorem 3.11 (the sandwich), both chains and the two equalities W(K ⊞ off) = W(K ⊞ dud) and
   L(K ⊞ on) = L(K ⊞ dud).

Be explicit about the points where loopy games differ from short ones:
- every "wins" is a forced win in finitely many moves, i.e. membership in a least fixed point; say what you induce on;
- infinite play is a draw;
- the first decisive event ends the whole sum;
- a suicide (an option to the opponent's terminal) counts as an event.

If you think a statement is false, give the smallest counterexample you can find. Check it by a small brute-force
program written from the definitions (Python is fine: `/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python`).
Also run a random test of each statement on small loopy games (at most 4 nodes per component, two or three components,
B from 1 to 4). Report the number of instances and the exact generator.

## Phase 2: compare

Only after `PROOF.md` is written, read `kings/theory/LOOPY.md` from "**Sums with loopy components" to the end of the
proof of Corollary 3.11a, and `kings/delegate/out/K21/VERIFY.md` section 1. Write `FINDINGS.md`:
- a 5-line summary;
- where your route differs from LOOPY's;
- each proof step of LOOPY for Theorem 3.7, Lemma 3.8a, Theorem 3.8 and Theorem 3.11 marked SOUND, GAP (give the
  missing step) or FALSE (give a counterexample);
- Theorem 3.8 (a)–(c) and Corollary 3.8b: do they follow as LOOPY says;
- your random tests (commands, counts);
- your recommended labels.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Runs over about one CPU-minute go through `kings/delegate/heavy.sh` (nice 15).
Under 3 GB RSS and under 20 minutes per run. No file over 50 MB. No installs, no network. Never use pkill, killall,
`kill -- -1` or any pattern kill. Kill only PIDs you started and recorded.
