# A8: explicit kings. When does "pawn components + a frozen trébuchet" give the chess result?

Research item A8 ([RESEARCH_PLAN.md](../RESEARCH_PLAN.md), Track A).

The convention behind `cylcgt` (and the 2025 paper):
- it values pawn components under normal play, with a passed pawn worth ±BIG;
- it treats the king group, the trébuchet, as the game 0.

This item puts the kings back and asks when that is right.

## Claim labels

Every claim below carries one label.

- **PROVED**: a proof is written out (in [theory/LOOPY.md](theory/LOOPY.md), or here). One model wrote it.
  An adversarial reviewer has checked it (§7), but no human has yet.
- **CHECKED-2**: computed by two independent implementations that agree, or by our solver and the Lichess
  tablebase.
- **COMPUTED-1**: computed once, by `kings/kpsolve` only. Its correctness rests on the checks in §2.
- **INFERENCE**: our reading of data, not a theorem.

## 1. Answers, in brief

**Is the convention right?** Often not, on small boards.
- Across the three sweeps, 159 of 500 testable components mismatch.
- In 107 of them the kings alone are the cause.
- The other 52 (all on the 7×6 board) are failures of the pawn convention itself: en passant, and passed
  pawns that do not actually win the race.

**Real values with explicit kings.**
- `kings/kpsolve` computes exact win/draw/loss for both sides to move, with real chess rules: kings,
  pawns, en passant, all four promotions, stalemate, and no 50-move rule.
- **CHECKED-2:**
  - It agrees with an independent Python solver on every one of 1,418,480 positions on 3- to 5-file
    boards (§2).
  - It is consistent with the Lichess tablebase on all 45 positions we could compare: 42 agree exactly, and
    in the other 3 (which need a second promotion) the true value lies inside kpsolve's bounds (§2).

**When the frozen-trébuchet assumption is exact** (Theorem 1.14 and §2 of [theory/LOOPY.md](theory/LOOPY.md)).
The convention gives the chess result when four conditions hold. With (V1)–(V3) the result is the
normal-play result of the pawn components: Theorem 1.14(i), **PROVED** and confirmed by a referee. The step
to cylcgt's BIG arithmetic, 1.14(ii), needs the corrected (V4) below (§7). The conditions:
- **(V1)** the kings never interact with the pawn components, and nobody is stalemated;
- **(V2)** every "decisive event" (a new passed pawn) really wins;
- **(V3)** every move inside the king group is decisively punished;
- **(V4)** no two components carry passed-pawn threats of opposite sign (counting a passer created by
  *either* side's move, a correction from the review in §7), and BIG exceeds every tempo count.

(V3) has a checkable local certificate: the punisher promotes within T moves even if the defender may
pass, and the defender cannot promote anywhere in T moves (Theorem 2.7). Its proof has a gap that the referees
say can be repaired with an unlimited-pass argument (§7).
- With **T = 1** the certificate holds in every context (Proposition 2.10a).
- With **T ≥ 2** it fails in some context (Proposition 2.10b), so the zero is context-dependent.
- The real trébuchets have T of about 5–7. Their zero is therefore valid only beside slow or locked
  components.

**Spare king tempo moves.** A king that can shuttle forever without loss is not 0 but a loopy game:
`on` = {on | } for White, `off` = { | off} for Black, or `dud` when both sides can shuttle.
- `on` exceeds every number, BIG included, so the BIG convention breaks completely there.
- The correct rule uses terminal outcomes (Theorem 3.4; **PROVED**, and it survived every referee):
  - with only White able to pass, Black wins iff Black can force a decisive event against a passing White,
    and otherwise White wins;
  - with both able to pass, a side wins iff it can force a decisive event against a passing opponent, and
    otherwise the game is a draw.
- Finite, non-reversible spare moves are integers (Theorem 4.2).
- **COMPUTED-1:** kpsolve confirms the theory's predictions for groups that realise `on` and `off` (§5).

**Where frozen kings give the wrong outcome.** Every case is listed in
[results/FAILURES.md](results/FAILURES.md). The main ones:
- **The 7.2 king group** (Ke6 Pd7 / Kd8 Pe7) is not a mutual zugzwang in real chess. White to move draws
  (Kd5, Ke5 or Kf5: d7 falls, but the White king blockades the e-pawn). **CHECKED-2** on the ordinary board
  (kpsolve and Lichess); **COMPUTED-1** on the cylinder, where the move values are identical.
- **Small-board sweeps:** 159 of 500 testable components mismatch (§4).
  - 107 are king effects: the frozen-king control matches cylcgt, and real chess does not.
  - 52 fail even with frozen kings: 18 through en passant, 34 because a passed pawn is not an immediate
    win.
  - **COMPUTED-1**, with the frozen-king control described below.
- **The \*2 candidate's tree and the engine suite:** on the ordinary 8×8 board, 8 positions from Lichess
  7-man data (**CHECKED-2** by the tablebase itself), plus 2 more from 8-man categories (lower confidence).

## 2. Method and checks

### The solver

- **Code and rules:** `kings/kpsolve.c`; rules in [SPEC.md](SPEC.md).
- **Layers.** Positions are grouped by pawn structure and officer types. Pawn moves, captures and promotions
  leave a layer and never return, so layers are solved children first.
- **Inside a layer.** Only kings and officers move, and those moves are reversible. Every placement of them
  is solved together by counting retrograde analysis. Unresolved positions are draws: infinite play is a
  draw.
- **Officer cap.** To bound the work, at most C promoted pieces may exist (`--cap`). A promotion beyond the
  cap is scored once as a White win (bound A) and once as a Black win (bound B). Values are monotone in
  terminal outcomes, so the true value lies between the bounds, and is exact when they agree. Every result
  quoted here is exact unless it is marked as bounds.

### Checks

| Check | Result | Label |
|---|---|---|
| Independent reference solver `kings/ref/` (Python), written from SPEC.md alone by another agent that never saw kpsolve | **0 differences on 1,418,480 positions** in 18 runs: boards flat and cyl from 3×5 to 5×5 (4×4, 4×5, 5×4, 3×5, 3×6, 5×5); K+P vs K, K+P vs K+P, K+2P vs K, K+2P vs K+P; caps 1 and 2; e.p. on and off; identical bounds wherever the cap applies ([results/crosscheck.txt](results/crosscheck.txt)) | CHECKED-2 |
| The reference solver's own tests | 56 pass, including a naive second move generator and a brute-force solver on 16 configurations | — |
| Lichess tablebase, cached records of ≤4 men (flat 8×8) | 37 positions: 34 agree exactly; 3 hit a second promotion, and the true draw lies inside kpsolve's bounds ([results/lichess_check_2-4_cap1.txt](results/lichess_check_2-4_cap1.txt)) | CHECKED-2 |
| Lichess tablebase, the paper's king groups (flat 8×8; 5 new requests) | 8 of 8 agree ([results/king_groups_lichess.txt](results/king_groups_lichess.txt)) | CHECKED-2 |
| Frozen-king control: `kpsolve --frozen` (king moves lose at once, promotion wins) against cylcgt | Identical on all 52 non-race components of the 6×6 and 5×6 sweeps. On 7×6, identical on 396 of 448; the 52 others are convention failures (e.p., passer races), explained in §4 | CHECKED-2 (two different programs) |
| kpsolve tests (`kings/test_kpsolve.py`) | 10 pass: mate, stalemate, illegal positions, wrap captures, the rook stopping at its own square, e.p. on and off, all four promotions, frozen mode = cylcgt | — |
| Underpromotion | The reference solver found a 4×4 position where only promotion to a rook wins; kpsolve agrees. On the 6×6 cylinder sweep, every exact all-promotions result equals the queen-only result (42 of 42) | CHECKED-2 / COMPUTED-1 |

**Limits.**
- Both solvers and every reviewer here are Claude models. The non-Claude ground truth is the Lichess
  tablebase, which covers only the ordinary board.
- The main sweeps use queen-only promotion with cap 2. The underpromotion check above is the evidence that
  this changes nothing there.

## 3. The paper's king groups on the full 8×8 board

Each group stands alone on an empty board. The convention reads every group as 0, so the side to move loses.

| Group | Board | White to move | Black to move | Verdict | Label |
|---|---|---|---|---|---|
| 5.1 trébuchet Kh5 Pa4 / Kb4 Pa5 | cylinder | Black wins | White wins | **real mutual zugzwang** (theory prediction P6) | CHECKED-2 (kpsolve and the main session's `atlas/cylinder/kpk`) |
| \*2 candidate's trébuchet Kf5 Pg4 / Kh4 Pg5 | flat (also cyl) | Black wins | White wins | **real mutual zugzwang** | CHECKED-2 (Lichess) |
| 7.2 Ke6 Pd7 / Kd8 Pe7 | flat and cyl | **draw** (Kd5, Ke5 or Kf5; Kf7 loses) | White wins (Kc7 forced) | **not a zugzwang**: frozen for Black only (P7) | CHECKED-2 flat, COMPUTED-1 cyl |
| 7.3 as drawn Kg8 Pf7 / Kf6 Pg7 | flat and cyl | White wins | White wins | decided: f7–f8=Q cannot be stopped (P8) | CHECKED-2 flat |
| 7.3 with the audit's conjectured kings Kg6 Pf7 / Kf8 Pg7 | flat and cyl | **draw** | White wins | not a zugzwang (the 7.2 pattern) | CHECKED-2 flat |

**Consequences.**
- The audit's "7.2's king group is a mutual zugzwang" holds only inside the convention, where "drops a pawn"
  means "loses". In chess White drops d7 and still draws.
- For sums, Theorem 2.4(b) needs the freeze only for the side that loses the pawn part. So 7.2 + H is still
  a White win whenever White wins H. When Black wins H, the convention's verdict is not certified: White
  sorties with the king and blockades (**PROVED**, theory §5.2).
- Source: [results/king_groups_8x8.txt](results/king_groups_8x8.txt) (every move with its value).

## 4. Sweeps: every small pawn component beside a trébuchet

**Setup** ([experiment.py](experiment.py)). Every pawn component P with up to 2 pawns a side, on the free
files of a small board, stands beside the board's trébuchet Z.
- **Cylinder:** the 5.1 pattern across the seam.
- **Ordinary board:** the \*2 pattern on the last three files.

Empty buffer files separate P from Z. Pawns change file only by capturing, so P and Z interact only through
the kings (Lemma 2.2). Each Z was checked to be a real mutual zugzwang on its own board. 6-rank boards,
queen-only promotion, cap 2, e.p. on.

The convention's prediction is cylcgt's outcome class of P alone:
- L: White wins either way;
- R: Black wins either way;
- N: the side to move wins;
- P: the side to move loses.

### Results

| Board | P on files | Components | Races at start | Testable | Match | Mismatch | Mismatch with the frozen-king control matching cylcgt (a king effect) |
|---|---|---|---|---|---|---|---|
| 6×6 cylinder | d | 42 | 16 | 26 | 13 | 13 | 13 |
| 5×6 ordinary | a | 42 | 16 | 26 | 23 | 3 | 3 |
| 7×6 cylinder | d, e | 812 | 358 | 448 (6 more undetermined) | 305 | 143 | 91 |
| **all** | | 896 | 390 | 500 | 341 | 159 | 107 |

**Diagnosis of every mismatching side** ([analyze.py](analyze.py), using kpsolve's value for every move):

| Board | Mismatching sides | "Escape": only king moves reach the real result | "King refutes": every pawn move the convention counts as winning is refuted by a king move |
|---|---|---|---|
| 6×6 cylinder | 20 | 12 | 8 |
| 5×6 ordinary | 3 | 3 | 0 |
| 7×6 cylinder | deferred: the move-level rerun needs about 9 GB and waits for a free machine. The sweep's own split (91 king effects, 52 convention failures) is in the table above | | |

**Example** (6×6 cylinder; Z = Pa3 / pa4, Kf4, kb3; P = W d2 / B d3).
- The convention says 0: the side to move loses.
- Real chess: a draw either way. White to move draws only with Kf4–e4, abandoning a3 and heading for d3.
  Black to move draws with Kb3–b2 or Kb3–c2.

**The 52 mismatches on 7×6 where frozen kings also disagree with cylcgt.** These are failures of the pawn
convention, not of the kings. They are attributed by re-scoring the convention ([conventions.py](conventions.py)):
- **18 are en passant.** Under the e.p.-aware passed test, the convention agrees with the frozen-king solver.
- **34 are "a passed pawn wins at once" failing.** In each, cylcgt's value contains ±BIG, while with frozen
  kings the result is decided by the real promotion race (theory condition (V2)).
- In 21 of the 52 the free kings change the result once more (real ≠ frozen).

Under the e.p.-aware convention the 7×6 mismatch count drops from 143 to 138.

### Observations (INFERENCE)

- **On the 1-file boards every mismatch is a king effect.** The frozen-king control reproduces cylcgt
  exactly on all 52 non-race components of the 6×6 and 5×6 sweeps. On 7×6 it reproduces cylcgt on 396 of
  448; the 52 others are convention failures, as above.
- **Only a king near the component breaks the convention.**
  - On the 5×6 ordinary board White's trébuchet king stands two files from P and Black's four. All three
    mismatches have White to move.
  - On the 6×6 cylinder both kings are two files away, and both sides fail.
  - The ordinary 8×8 data is consistent with this, but weak evidence. In the \*2 layout White's king on f5
    is two files from the d-file and Black's on h4 four, and the king failures found in the \*2 tree all
    have White to move. But 271 of the 275 engine-suite positions have White to move by construction, so
    the suite says nothing about the asymmetry (a point from the data review, §7).

  This matches the certificate's condition (L2): a defender whose king is close to the component can
  counter-attack faster than the trébuchet punishes.
- **e.p. and the passed test.** cylcgt's textbook passed test and the e.p.-aware test (a pawn that can still
  be taken e.p. is not passed) give identical verdicts on the 1-file boards ([conventions.py](conventions.py);
  our reimplementation of the e.p.-aware rule, not the branch code).
  - On the 7×6 board, where e.p. is possible inside P, the e.p.-aware test changes 5 verdicts, each one to a
    match.
  - In the \*2 tree, 7 of the 14 convention failures are e.p. cases, which the e.p.-aware test removes
    (`kings/data/DATA.md`).

## 5. The theory's predictions, tested

[theory/LOOPY.md](theory/LOOPY.md) §6 made concrete predictions before any of these were run.
kpsolve then solved them; the full table is [results/PREDICTIONS.md](results/PREDICTIONS.md).

**Score.**
- **Theory:** 25 of 28 exactly determined predictions hold: 22 of 25 in
  [results/PREDICTIONS.md](results/PREDICTIONS.md), plus P6, P7 and P8 on 8×8. The 3 that fail are all P4,
  which the theory had labelled a CONJECTURE.
- **Literal cylcgt:** 16 of 22 (cylcgt on the whole pawn set, kings ignored). It gives no prediction for P5
  and P8, which it scores as races at move 0.

**Which baseline.** The theory's own "naive convention" column reads the king group as 0 and values only
the rest with cylcgt. The theory review (§7) pointed out that this is a strawman: literal cylcgt calls the
shuttle groups' pawns passed and so scores P2, P3 and P10 correctly, for the wrong reason. So the fair
comparison is with literal cylcgt.

| Prediction | Position family | Theory | Literal cylcgt | kpsolve |
|---|---|---|---|---|
| P1a, P1b | stalemate traps: the only escape square is covered | (D, D) | (W, W); (L, L): **wrong** | (D, D) both |
| P2 | Z_onT1 `Ka5 Pb4 Pc5 / kc6 pb5` (White king shuttles a5–a6: `on`) in 5 contexts | (W, W) in all 5 | (W, W): right (c5 counted as passed) | (W, W) in all 5 |
| P3 | Z_offT1 (the colour-reversed `off` group) in 5 contexts | (L, L) in all 5 | (L, L): right | (L, L) in all 5 |
| P4 | Z_T, a frozen trébuchet (Ka4 Pb3 / kc3 pb4), in 6 contexts | equal to cylcgt (CONJECTURE) | same as the theory | equal in 3 of 6; **both wrong in 3 of 6** |
| P5 | 6-rank 7.2 analogue `Kc4 Pb5 / kb6 pc5`: bare, and + Hp1 | (D, W); (W, W) | race: no prediction | (D, W); (W, W) |
| P6, P7, P8 | 5.1, 7.2, 7.3 on 8×8 (§3); 6-rank 7.3 analogue | (L, W); (D, W); (W, W) | 7.2 and 7.3 have both pawns passed: race | as the theory predicts |
| P9 | `Ka5 Pb4 Pc5 Pe2 / kc6 pb5 pf3` | (W, L) | (W, W): **wrong** | (W, L) |
| P10 | Z_onT1 + k Black tempo units, k = 0, 1, 2 (8×6 cylinder) | (W, W) for every k | (W, W) | (W, W) for k = 0, 1, 2 |

**The P4 failures.**
- P4 is a frozen trébuchet (Ka4 Pb3 / Kc3 Pb4) whose punishment takes several moves (T > 1). The theory
  conjectured that the convention holds beside every one-file tempo context; kpsolve refutes this in 3 of
  the 6.
- Mechanism, from kpsolve's move values
  ([results/theory_P4_cap2_moves.txt](results/theory_P4_cap2_moves.txt)): after White's 1.e3–e4 locks the
  context, the convention says Black is in zugzwang and loses. Instead Black plays Kc3–d3 or Kc3–d4: the
  king abandons b4, walks to the locked e-pawns, and draws.
- In H0 with Black to move, Kd3 or Kd2 draws the same way.
- This is the king interacting with the context, condition (V1a), failing. It is exactly what
  Proposition 2.10(b) warns of: a group whose punishment needs T ≥ 2 moves has a context-dependent zero.
- **COMPUTED-1** (cap 2, exact).

**What this shows.**
- **Where the theory adds something,** it is right:
  - stalemate (P1), which literal cylcgt gets wrong;
  - the blockade escapes in 7.2 and its 6-rank analogue (P5, P7), which cylcgt cannot score at all;
  - a context that changes who wins (P9).
- **Where both are wrong** (P4), the cause is a king walking from a slowly punished trébuchet to the context.
- **Labels.**
  - The predictions are proved only in the theory's promotion model, where the first promotion wins.
    The review found that the bridge from that model to chess (assumption (A_Q)) is false in general, so
    each prediction needs kpsolve's chess check.
  - kpsolve's agreement confirms these positions (**COMPUTED-1**). It does not prove the general theorems,
    some of which need repair (§7).

## 6. Positions where frozen kings give the wrong outcome

The full list is in [results/FAILURES.md](results/FAILURES.md):
- the sweeps, with each side's real best moves or refutations;
- the paper's king groups;
- the 8 positions on the ordinary 8×8 board from the \*2 tree and the engine suite.

The ordinary-board cases are:

| Source | Position | What happens |
|---|---|---|
| \*2 terminal | W a5 / B b7 c5 | White to move draws with Ke4 or Ke5: the king gives up g4 and catches the c-pawn |
| \*2 node | W a5 c3 / B b7 d5 | White to move draws; both pawn moves lose, so a king move draws |
| \*2 terminal (probable) | W c4 / B a6 d6 | White to move draws; the drawing move is not recorded |
| suite cgt055 | W c5 / B c6 c7 | Ke6 draws (convention: White loses) |
| suite cgt120 | W c3 d4 / B d5 | Ke5 or Ke6 wins (convention: White loses) |
| suite cgt123 | W b3 c4 / B c5 | all five king moves draw (convention: White loses) |
| suite cgt262, cgt270 | W c4 d3 / B c5; W c3 d4 / B d5 (B4-trébuchet) | Kg6 draws (convention: White loses) |
| \*2 terminal (data review) | W a4 c4 / B b6 d4 | White to move wins by Ke4 (convention: Black wins); Lichess 8-man category, lower confidence |
| \*2 node (data review) | W a5 c5 / B b7 d7 | White to move draws by Kg6 or Kf6 (convention: White loses); lower confidence |

## 7. Adversarial checks

Every deliverable was given to independent referees (Claude models) told to break it. Their reports are in
[theory/REVIEWS.md](theory/REVIEWS.md) (theory), and are summarised for the rest.

| Target | Referees | Outcome |
|---|---|---|
| Reference solver `kings/ref/` | 1 | No defect. The referee wrote a **third** solver of its own (dict boards, plain repeated passes, no counters) and compared all 282,816 input lines of 19 material sets with `kings/ref/`, with **0 differences**. Its harness caught a deliberately broken control (1,488 differences). Minor defects: random-test seeds were not reproducible (fixed), and input leniencies were documented. |
| kpsolve (indirectly) | 2 | Two referees ran kpsolve on 25 hand-analysed positions of their own (stalemates, mates across the seam, e.p. pins, underpromotion, 4-rank double steps). All agree with their analysis. |
| Data extraction `kings/data/` | 1 | Every count matches the sources. It found two frozen-king failures the extraction had missed, double counting, and some over-labelled claims. All are recorded in the erratum at the end of [data/DATA.md](data/DATA.md) and added to [results/FAILURES.md](results/FAILURES.md). |
| Theory [theory/LOOPY.md](theory/LOOPY.md) | 4 (one general, three on separate theorem clusters) | **Sound:** Lemmas 1.6, 1.7; Theorems 1.9, 1.11(a), 1.14(i), 3.3, 3.4 (the loopy outcome rules, including draws); Corollaries 2.8, 3.5; Propositions 1.12, 2.10(b), 4.5, 4.6; the applications in §5 (label slips only). **False as stated, with a known repair:** Theorem 1.11(b) (the threat set missed suicides), Proposition 1.13, Theorem 2.4 for drawish contexts, Proposition 2.10(a) on 4-rank boards, Proposition 4.3, and the promotion-to-chess bridge (A_Q). **Gaps:** Theorems 1.14(ii), 2.7 (the pass-budget step; repairable with an unlimited-pass argument), 4.2; Lemma 2.9 (a hidden hypothesis); Remark 2.11. **Revision (2026-10-21):** the note was revised against all four reports by three external models (kilo minimax, opencode nemotron, opencode best-free; 64 edits, `kings/delegate/out/K1a..K1c/`). It now opens with a status table giving every result's final label. The repaired proofs are written but not yet independently re-checked (task K3). |
| This report | — | The literal-cylcgt baseline in §5 and the weakened 8×8 asymmetry claim in §4 come from these reviews. |

**What the reviews change in the conclusions.**
- **No computed result changed.**
- The general validity theorem stands in its main part, 1.14(i): with frozen kings, decisive events and no
  stalemate, the result is the normal-play result.
- The parts that tie it to cylcgt's BIG arithmetic, 1.14(ii), and the certificate for slow punishments,
  2.7, need the repairs listed.
- The loopy rules for spare tempo, Theorem 3.4, survived every check.
- In the revised note, "PROVED after repair" marks a proof written by an external model and read once by
  the integrator. Treat it as unverified until K3 reports.

## 8. Open questions

- **8-rank sweeps.** The sweeps use 6 ranks to fit the compute. On 8 ranks the trébuchet's punishment is
  slower (T ≈ 5–7) and the kings are further from the component, so the convention should fail less often.
  The ordinary-board data suggests the same.
- **The paper's full positions.** 7.2 with its {a,b,h} pawns has 10 men on 8×8, out of reach for an exhaustive
  solve here. Theory §5.2 says it is still a White win when White wins the pawn part.
- **`dud`.** No small king-and-pawn group with both kings able to shuttle and no pawn break was found
  (CONJECTURE, theory §5.3).
- **Gafni's K+P vs K values without edges** (plan A8) were not re-examined.

## 9. Reproduce

Run from the project root, one command per block.

Build the solver and run its tests:

```bash
cc -O2 -o kings/kpsolve kings/kpsolve.c && .venv/bin/python -m pytest -q kings/test_kpsolve.py
```

Run one sweep (about 5 minutes on an idle machine for the 6×6 board):

```bash
python3 kings/experiment.py --board cyl:6x6 --promote Q --cap 2
```

Diagnose its mismatches:

```bash
python3 kings/analyze.py kings/results/exp_cyl6x6_epon_Q.jsonl
```

Cross-check against the reference solver:

```bash
python3 kings/crosscheck.py --board cyl:4x5 --material KPK KPKP KPPK --cap 1
```

Check against cached Lichess results:

```bash
python3 kings/lichess_check.py --max-men 4
```

Regenerate the failure list:

```bash
python3 kings/failures.py
```
