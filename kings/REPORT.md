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
    boards (§2). This checks the solver; the theory's predictions rest on kpsolve alone (COMPUTED-1, §5).
  - It is consistent with the Lichess tablebase on all 45 positions we could compare: 42 agree exactly, and
    in the other 3 (which need a second promotion) the true value lies inside kpsolve's bounds (§2).

**When the frozen-trébuchet assumption is exact** (Theorem 1.14 and §2 of [theory/LOOPY.md](theory/LOOPY.md)).
The convention gives the chess result when four conditions hold. With (V1)–(V3) the result is the
normal-play result of the pawn components: Theorem 1.14(i), **PROVED** and confirmed by a referee. The step
to cylcgt's BIG arithmetic, 1.14(ii), needs the corrected (V4) below (§7). The conditions:
- **(V1)** the kings never interact with the pawn components, nobody is stalemated, and en passant obeys
  condition (E) of L1.6 in `notes/lemmas.md` (Theorem 1.14 states (E) inside (V1)(a));
- **(V2)** every "decisive event" (a new passed pawn) really wins;
- **(V3)** every move inside the king group is decisively punished;
- **(V4)** no two components carry passed-pawn threats of opposite sign (counting a passer created by
  *either* side's move, a correction from the review in §7), and BIG exceeds every tempo count.

(V3) has a checkable local certificate: the punisher promotes within T moves even if the defender may
pass, and the defender cannot promote anywhere in T moves (Theorem 2.7).
- **Theorem 2.7 is PROVED after repair, in the promotion model P** (task K7, 2026-10-22). P is chess in which
  the first promotion wins. The bound μ ≥ T + 1 on the defender's counter-promotion is exact there.
- **It does not give a chess win, and no margin on μ does.** Examples on the 7×6 cylinder, each a Black win in
  P (kpsolve, cap 2):
  - `Kb4 ka1 Pe4 pa2` with Kb4–c5 meets the horizon-1 certificate, yet the chess result is a draw;
  - `Kc5 ka3 Pe2 pc4` with Kc5–d5 meets the horizon-2 certificate, yet White wins in chess.
- A chess conclusion therefore needs the per-position check (A_Q).
- See LOOPY.md, "What Theorem 2.7 does not give". The repaired proof was checked only by AI reviewers.
- With **T = 1**, condition (L2) of the certificate holds in every chess-legal context without a passer, on
  boards with at least 5 ranks, provided the defender has no king-group pawn one move from promotion
  (Proposition 2.10a). (L1) must still be checked for the group, and (L3) in each context.
  (Wording corrected after the main project's T30 proof audit, `notes/proof_audit2/REPORT.md`: the earlier
  sentence claimed the whole certificate.)
- With **T ≥ 2**, (L2) fails in some context on boards at least |F_Z| + 4 files wide (Proposition 2.10b),
  so the zero is not certified in every context. That it is actually context-dependent is a CONJECTURE, supported by P4.
- The real trébuchets have T of about 5–7. Their zero is therefore certified only beside slow or locked
  components.

**Spare king tempo moves.** A king that can shuttle forever without loss is not 0 but a loopy game:
`on` = {on | } for White, `off` = { | off} for Black, or `dud` when both sides can shuttle.
- `on` exceeds every number, BIG included, so the BIG convention breaks completely there.
- The correct rule uses terminal outcomes (Theorem 3.4; **PROVED**, and no referee broke it; all referees were AI
  models). Its chess consequences hold where the promotion-to-chess hypothesis (A_Q) holds, which kpsolve
  checks position by position:
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
| 7×6 cylinder | deferred: an exact per-move tally needs cap 2 (about 9 GB), above the shared machine's 4 GB per-process rule. A cap-1 variant was validated on 6×6 and found unreliable ([results/analyze_7x6.log](results/analyze_7x6.log)). The sweep's own split (91 king effects, 52 convention failures) is in the table above | | |

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
  Proposition 2.10(b) warns of. That proposition shows the certificate cannot cover a group whose punishment
  needs T ≥ 2 moves in every context; P4 shows this group's zero fails in some contexts. That it happens for
  every such group is a CONJECTURE.
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
| Theory [theory/LOOPY.md](theory/LOOPY.md) | 4 Claude referees, then K3 (an external model) on the repairs | **Sound:** Lemmas 1.6, 1.7; Theorems 1.9, 1.11(a), 1.14(i), 3.3, 3.4 (the loopy outcome rules, including draws); Corollaries 2.8, 3.5; Propositions 1.12, 2.10(b), 4.5, 4.6; the applications in §5 (label slips only). **False as stated, with a known repair:** Theorem 1.11(b) (the threat set missed suicides), Proposition 1.13, Theorem 2.4 for drawish contexts, Proposition 2.10(a) on 4-rank boards, Proposition 4.3, and the promotion-to-chess bridge (A_Q). **Gaps in the reviewed version:** Theorems 1.14(ii), 2.7 (the pass-budget step; repairable with an unlimited-pass argument), 4.2; Lemma 2.9 (a hidden hypothesis); Remark 2.11. **Revision (2026-10-21):** the note was revised against all four reports by three external models (kilo minimax, opencode nemotron, opencode best-free; 64 edits, `kings/delegate/out/K1a..K1c/`). It now opens with a status table giving every result's final label. K3 then checked the repairs: 13 of 17 sound, 4 downgraded to GAP. **Final labels** (LOOPY's status table): 1.14(ii), 4.2 and Lemma 2.9 (with its added hypothesis) are PROVED after repair; after K7 and K9 (2026-10-22) Theorem 2.7, P12 (in P) and the sharp form of 1.14 are PROVED after repair, and after K10 P11 is PROVED in P in a conditional form (every passer and race terminal certified by the new Proposition 2.11, a root with a passer included, frozen kings; one AI proof, not re-derived by a second model); the real-king square rule is a CONJECTURE. **T30 proof audit (main project, 2026-10-22, `notes/proof_audit2/REPORT.md`):** the proof of Proposition 2.10(a) lacked a step for en passant; it is added, and H ≥ 5 stands under both passed tests. (The audit read 2.10(a) as false on 5 ranks, but its example concerns a pawn of the side not to move, which (L2) does not count; the stronger either-colour statement does need 6 ranks.) The proof of Theorem 2.3 had been overwritten by a misanchored edit (restored, and the edit moved to §1.4). A count in Theorem 1.11(b)–(c) was one short and the canonical form of 0 was misstated (fixed; conclusions unchanged). The §0 summary labels now match the status table. The kings/ side session wrote these fixes. Two Sonnet reviewers read the first draft, which led to the correction of the audit's reading of 2.10(a). Two more read the revised text, and their remaining wording points were applied. K3 saw none of them, and its SOUND verdicts on 1.11(b) and 2.10(a) predate them. |
| This report | — | The literal-cylcgt baseline in §5 and the weakened 8×8 asymmetry claim in §4 come from these reviews. |

**What the reviews change in the conclusions.**
- **No computed result changed.**
- The general validity theorem stands in its main part, 1.14(i): with frozen kings, decisive events and no
  stalemate, the result is the normal-play result.
- The step to cylcgt's BIG arithmetic, 1.14(ii), holds with the corrected (V4): PROVED after repair, and K3
  found the repair sound. The certificate for slow punishments, Theorem 2.7, is PROVED after repair in P (K7),
  but gives no chess win without (A_Q).
- The loopy rules for spare tempo, Theorem 3.4, were found sound by every theory referee (all AI models).
  In chess they are confirmed on the positions kpsolve solved (§5), not in general.
- In the revised note, "PROVED after repair" marks a proof written by an external model, read by the
  integrator, and then checked by another external model (K3). K3 found 13 of the 17 repairs sound, and
  downgraded 4 to GAP: the sharp form of 1.14, Theorem 2.7, and predictions P11 and P12.
  - K7 (2026-10-22) later repaired Theorem 2.7 and P12, in P. A Sonnet agent drafted the repair, and two rounds of
    three Sonnet reviewers checked it. The first round refuted a window form, which was then fixed.
    K36 (2026-10-28, Codex) proved Theorem 2.7 blind and then audited the corrected text. It found one repairable gap, a
    citation of Lemma 2.2 outside its setup, now repaired by a sentence; every other step is SOUND.
  - K9 repaired the sharp form of 1.14. A free model drafted it, and Sonnet reviewers and a fixer rewrote it as a
    simulation lemma. K13 (2026-10-27, Codex, outside the Claude family) re-derived it in its own words (0.76% of its
    5-grams and none of its 8-grams occur in LOOPY's sharp-form section; `kings/delegate/out/K13/overlap.py`) and found
    every step SOUND. It also found that the hypothesis (V1a) of the one-sided chess bridge after Proposition 3.2 was
    worded too broadly: it excluded the Black Z-moves that the punishment hypothesis is meant to cover. The bridge now
    has scoped hypotheses, as the two-shuttle bridge Theorem 3.2‴ already had, and an explicit proof by the sharp form
    of Theorem 1.14. A second Codex check (K13b) made its terminal moves, the e.p. flag under the shuttle and its
    no-stalemate condition exact.
  - K10 (2026-10-22) gave P11 its missing piece, a passer certificate with frozen kings (Proposition 2.11). A free
    model drafted it, and two Sonnet reviewers found it FALSE: an opponent pawn that captures a pawn on a
    neighbouring file can stop the passer, and the draft also mishandled checks, kings on the path, one move
    order, races and en passant. A Sonnet agent rebuilt it with five hypotheses (H1)–(H5), and the integrator read the proof and
    re-ran its examples. It was checked on 954,392 + 60,000 positions with side to move against `kpsolve --frozen`, with 0
    violations. P11 is now PROVED in P in a conditional form: every passer and race terminal must be certified,
    and a root that already has a passer must itself satisfy Proposition 2.11.
    Without that it is false (`Ka1 ka6 Pc2 Pc3 pd3 pd4 w -`). With real kings nothing is proved; the square rule is
    a CONJECTURE. K10v (opencode beam-free, independent code) re-checked the computation: 0 violations in
    146,328 certified instances (119,654 positions with side to move) + 5,716 with an e.p. right (CHECKED-2). Its proof verdict "SOUND" came without a written derivation, so
    it was no re-derivation.
    In a second round two fresh Sonnet reviewers (`kings/delegate/out/K10r2/`) read the proof and found no error in
    its steps, and their own code found 0 violations in 5,730,596 certified positions with side to move on cylinders
    plus 434,429 on flat boards. They found one real gap in P11's statement: it left out a root that already has a
    passer (`Ka1 ka6 Pc2 Pd4 pd3 b -` is a White win in W(X) and (L, L) in `--frozen`). P11 now requires that root
    to be certified too. Their other fixes (y must be legal, the HSS definition in §6, the layout premise of
    Corollary 2.11b, count units) are applied in LOOPY. No model outside the Sonnet family had re-derived the proof.
    K11b (2026-10-27, Codex) did, blind: it read only the statement, the definitions and the code, wrote its own proof
    (13% word overlap with LOOPY's, against 96% for the rejected K11 copy), then compared and found Steps 0–5 SOUND.
    It also noted that W(X) is undefined at a root race (`value()` raises RaceError), so the root clause needs the
    count-rule convention that K12 used.
    K12 (2026-10-27) swept the root clause: 716,962 roots with a passer on cyl:6×6, 7×6 and 8×6, with 0 certified
    violations. 20,376 of them are uncertified roots where the credit is wrong, and the clause is what excludes them.
    The integrator re-ran 6×6 without e.p. rights with separate code and the K10r2 hypothesis checker: the same
    76,744 roots and 0 certified disagreements (CHECKED-2 there; `kings/delegate/out/K12/REVIEW.md`). The same recheck
    on 7×6 (515,780 roots) and 8×6 (68,036) also finds 0 certified disagreements; only the 56,402 roots with an e.p.
    right rest on K12 alone.
  - K19 (2026-10-27) re-computed the §5 scratch claims with new code (local game, μ, a P solver); a Sonnet referee
    used its own code again. §5.1 (L1) and (L3), §5.2, §5.5, §5.6, P5–P7 are now CHECKED-2. Two corrections: Black's
    move list in §5.1 had Kb5 for Kb3, and Kd4/Kd5 in §5.5 lose against every finite budget checked (T = 6 + k) but
    not against unlimited passes. Unbounded "no win" claims rest on K19's fixed point alone and are COMPUTED-1.
  - K23 (2026-10-27) showed that the zero of a frozen group depends on the context, in P. Z_T acts as 0 beside
    {Pe3, pe4} and not beside {Pe2, pe3} on cyl:7×6, by a one-tempo race; the same holds for the §5.1 group on
    cyl:8×8 (new prediction P13). It is CHECKED-2: three implementations agree (the kpsolve family, the agent's
    `pk2.c`, and the referee's `ref3.cpp`, written from SPEC). The general statement is open question 6. P4's chess
    refutations are not P effects.
  - K14 (2026-10-27) proved a two-sided Proposition 3.2′ (two shuttling kings act as dud_D in the D-model) and a chess
    bridge, Theorem 3.2‴, conditional on (Pun). Its referee found **Z_B** on flat 7×6, which refutes K14's own "no
    exactly frozen group" (the search had a move-count cut-off): White king b2/c3, Black king a4/b5, pawns Pa3 Pb4 pb3
    pc4. In P every non-shuttle move loses by force, CHECKED-2 (kp_p and `ref3`; PROVED by hand since K27). Beside 660 contexts its P result
    equals the dud prediction (COMPUTED-1). In chess it is not exactly two-shuttle: Kc3–d2 from (c3, b5) draws (K28).
    K34 (2026-10-28, Codex) proved Proposition 3.2′, Lemma 3.2″ and Theorem 3.2‴ again from the statements alone and found
    every step SOUND, the e.p. and bridge steps under their stated hypotheses. Its one objection, about the G = 0 shuttle deletions, came from a script that did not test what it
    reported, and the integrator's own computation confirms the note.
  - K22 (2026-10-27) showed that Lemma 2.9 is false without its added hypothesis (counterexamples on flat:4×5, cyl:7×6
    and flat:3×5) and proved it under the weaker hypothesis (B1).
    K37 (2026-10-28, Codex) audited that proof and found it SOUND; it is an audit, not a second proof (its blind
    attempt had a gap).
  - K17 (2026-10-27) showed that the clause "no checks" of (V1a) in Theorem 1.14 is needed: cyl:6×6
    `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -` (a Z-pawn check) is a White win in P but outcome N in D (CHECKED-2, three P solvers).
    In the structured class of Definition 2.1, (V1a) can fail only by such a check or by the e.p. clause (E)
    (Proposition 1.15, PROVED). For (E) a bounded search found no isolated counterexample, so "(E) is needed" stays a
    CONJECTURE.
  - K18 (2026-10-27) tested tempo matching (§8 open question 1) in P. As worded it is FALSE: 42 of 2,305 legal cases
    fail (CHECKED-2 for the ES and ES7 cases), the smallest `Ka1 Pa2 kc1 pa3` with the sortie Ka1–h1 and context
    `Pe2 Pg2 pf4`. It held in all 292 promotion-free cases that were tested (a CONJECTURE beyond them). Proposition 8.1 (tempo pairing)
    is PROVED after repair: the first referee found an e.p. gap, the fix added (P1e), and a second referee re-derived it.
  - K30 (2026-10-28): a hand proof that White cannot win 7.2 with White to move (P7 w), in P and in chess, on both
    8×8 boards; the referee re-derived it and reproduced its counts (open question 7).
  - K31 (2026-10-28): a single blocked pair on cyl:W×H has king-tempo roots +1 and −1 exactly when W is even and
    W ≥ 6 (CHECKED-2 for W·H ≤ 127, a CONJECTURE in general); two +1 roots add like the integer 2.
  - K32 (2026-10-28): the conjecture λ(S) = ⌈−RS(S)⌉ or one more fails exactly for finite RS ≥ 2; a corrected
    relation between reserves and Siegel's stops is PROVED from a KNOWN fact about stoppers.
  - K24 (2026-10-27) added Lemma 2.7a (PROVED): a draw in both promotion models EPW and EPB is a chess draw. It
    settles the chess w-entries of P5 and P7 as draws without relying on kpsolve, and four P solvers agree on P5–P7.
  - K16 (2026-10-27): the real-king square rule of Remark 2.11 is FALSE as stated, because ω can be stalemated
    (CHECKED-2 counterexamples). A corrected Theorem 2.11K, with a king-restricted timing condition and a no-stalemate
    condition, is PROVED in P, and 7.6 · 10⁸ certified instances give 0 violations.
    K35 (2026-10-28, Codex) audited the note's proof step by step from outside the Claude family and found every step SOUND.
    Its own blind proof missed one case, which the note's Step 2 covers.
  - K20 (2026-10-27): finite king tempo exists when the opponent is not frozen. On flat:6×6, `Kc3 ka4 Pa2 pa3 Pc4 pc5`
    is +1 in the D-model sum battery (CHECKED-2); Proposition 4.3 holds only against a frozen opponent.
  - K21 (2026-10-27): a sum theorem for loopy components. The reserve criterion T3.8 strictly extends Theorem 1.11(b)
    to arbitrary loopy components, and the sandwich T3.11 bounds every group between off/dud and on (PROVED, one AI
    proof each, re-derived by the referee). K33 (2026-10-28, Codex) proved T3.7, Lemma 3.8a, T3.8 and T3.11 again from
    the statements alone and found every step of the note's proofs SOUND.
  - K27 (2026-10-27): Z_B is exactly two-shuttle in P, and this is now PROVED by hand. Each of the 26 non-shuttle moves
    has a certificate (286 entries in all) and loses within 11 plies. The referee parsed every certificate with its own
    move generator, and four solvers agree on the numbers (CHECKED-2). The mirror group follows by a rank-flip and
    colour-swap symmetry. In chess, 21 of the 26 deviations lose (CHECKED-2: kpsolve and the referee's `ownchess`). Five
    were not settled at cap 1; K28 settled them (next bullet).
  - K28 (2026-10-28): the five deviations solved at cap 2 (exact, A = B) and with a capture refinement at cap 1. Four lose
    and **Kc3–d2 from (c3, b5) draws**: its child `Kd2 Pa3 Pb4 kb5 pb3 pc4 b -` is exactly D (kq3 at cap 2; kpsolve with
    White held to one queen gives the lower bound D; `ownref` with the refinement agrees). So Z_B is **not** exactly
    two-shuttle in chess, CHECKED-2 (no hand proof of the draw). The referee re-ran every solver except kpsolve at cap 2 on
    the four 3-pawn positions, which it read from the investigator's log. Open: chess contexts of Z_B.
  - K15b and K26 (2026-10-29) answer open question 2 in P: dud groups with no pawn break exist on the cylinder.
    K26's search of three-file groups with no cut-off finds Z_B on cyl:7×6 and cyl:8×6 and a new passer-free group
    Z_C (`Pa2 Pc4 / pa3 pc5`, kings c2/c3 and a4/a5) on cyl:8×6, with mirrors; both are exactly two-shuttle in P
    (CHECKED-2 for width ≤ 8). K15 finds G8a and G8b on cyl:8×6 (re-solved by its referee K15b; two blocked pairs on files a and e, no pawn move),
    exactly two-shuttle in P (CHECKED-2) and with the same 72 move values in chess at cap 2 (COMPUTED-1). Z_C is not
    dud_D beside every context. The two searches agree where their scopes overlap. Neither finds an over group, so the
    second half of Conjecture 4.7 has no support (COMPUTED-1). Both referees accepted with fixes; the merged edits were
    checked three ways (`kings/delegate/out/K15K26/MERGE_NOTES.md`).
  - K29 (2026-10-29) answers open question 6 for a bounded context class. Of 1,236 bare groups (446 classes) on four
    boards, 269 classes fail somewhere; on cyl:7×6 four classes, `Kb3 Pa2 Pc2 kb1 pa3 pc3` among them, act as 0 beside
    all 885 contexts of at most two pawns a side, with an exact-P punishment of at least 2 moves on both sides
    (CHECKED-2: two solver pairs, and the referee re-solved all 60 groups). Two of the four fail beside the larger
    context `Pf2 pf3 pf4 pf5`, so the zero depends on the context class. The T of Definition 2.6 was not computed, so
    the CONJECTURE of Proposition 2.10(b) is not refuted. Two referees; their replacement edits were applied.
  - K38 (2026-10-29) proves by hand that P5 (`Kc4 Pb5 kb6 pc5`, White to move) is a draw in P, EPW, EPB and chess on
    cyl:7×6 and flat 7×6, without Lemma 2.7a: K30's argument for position 7.2, moved two files left and two ranks down.
    Its blockade invariant (296 positions per board) and Lemma K′ were checked by two move generators, and the chess
    values by kpsolve and the referee's own solver (CHECKED-2). The referee re-derived every case; its edits were applied.
  - K40 (2026-10-29) answers open question 5 (Gafni's K+P v K without edges) on cyl:W×H, 3 ≤ W ≤ 8, H ∈ {6, 7, 8}: under normal play, on 3 and
    5–8 files every position has the signature of a win, of on, or of dud, and no number or infinitesimal occurs
    (CHECKED-2 for H = 6, 8, two sum solvers, 71,842,272 results; COMPUTED-1 for H = 7). Black never wins, by hand. The atlas table differs from P only where
    the atlas scores a capturable promotion as a draw. The 4-file cylinders differ. The referee's edits were applied.
  - K41 (2026-10-29) checked the commits for K28, K15b+K26 and K29 against their sources: every edit was applied exactly,
    and six wording and scope points were fixed (`kings/delegate/out/K41/CHECK.md`).
  - K39 (2026-10-29) takes the dud groups to chess on the cylinder. Neither Z_B (cyl:7×6, cyl:8×6) nor Z_C (cyl:8×6) is
    exactly two-shuttle in chess: their roots are D, but some deviations also draw (for Z_B, Kc3–d2 and the wrap move
    Ka4–g5/h5; for Z_C eight king moves), CHECKED-2 with three solvers. Beside 8 small chess contexts on flat 7×6, Z_B
    matches dud_D at the 60 roots that cap 1 decides; 4 roots and the rest of the context class were not run. The
    referee's corrected edits were applied.
  - K42 (2026-11-22) settles open question 1 in its promotion-free form: it is FALSE in P (CHECKED-2 for the counterexamples;
    the totals, 68,395 failures in 6,033,423 sortie and context pairs on cyl:7×6, 8×6 and 9×6, every one using the king that
    made the sortie, are COMPUTED-1).
    Proposition 8.1′ (PROVED, re-derived by the referee) keeps what survives. The referee's own solver reproduced the lists.
  - K43 (2026-11-22) extends the search for over groups: no exact over or under group with at most 3 + 3 pawns on four
    files, every king placement, cyl:6×6 to 9×6, flat 7×6 and 8×6 (CHECKED-2, 6.4 billion placements per orientation).
    These are four adjacent files; K45 then found exact groups on a five-file span. Two new lemmas, 4.10 (with the referee's added condition) and 4.11.
  - K44 (2026-11-22) extends the king fights of open question 3: the local king game LK reaches over and under on cyl:10×6
    and wider with three blocked pairs, and a three-pair +1 and -1 root on every width 7 to 12, new on 7, 9 and 11 (CHECKED-2, four implementations).
    These are values of a king fight, not groups of Definition 4.8 in P. The referee's edits were applied, one merged by
    hand with K43's.
  - K45 (2026-11-23) realises the over half of Conjecture 4.7 in the sense of Definition 4.8: exact over groups, and their
    mirrors, exact under groups, exist in plain P on cyl:8×6 and every wider cylinder searched, with 3 + 3 pawns on files a, b
    and e (`Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5`, Black's king shuttling d4–d5); on cyl:10×6 also a 2 + 3 group. None exists with
    at most 2 + 2 pawns, nor on cyl:6×6 or 7×6 (CHECKED-2, two implementations plus the referee's own solver). K44's king-fight
    roots are not such groups: their freezes are king moves that White can undo.
  - K47 (2026-11-23) tests the cyl:8×6 group in sums: as the P game of its own pieces it is **not equal to over**. Against
    275 test games it differs from over at 38 of 1,100 results, always in Black's favour, beside \*, ↓, under and sums
    containing them (CHECKED-2, three solvers). A move that loses in P alone, through a zugzwang up to 25 plies later, can win
    when the mover has a tempo elsewhere, so Definition 4.8 does not force the value over. Its freeze at the d4 root is a
    mutual zugzwang on every cyl:W×6, W ≥ 8 (PROVED by hand, after a referee repair). The group's value is not identified;
    a group with the value over is still not known (`kings/delegate/out/K47/REVIEW.md`).
  - K48 (2026-11-23) takes the same group to chess and to other boards (CHECKED-2). In chess on cyl:8×6 at promotion cap 1
    its d4 freeze still wins and the position after it is an exact mutual zugzwang; the d5 root is undecided, so exactness
    in chess is open. The wrap is not needed: on flat 8×6 the group and its two translates are, up to left-right
    reflection, the only exact groups of Definition 4.8 in the searched range, and translates are exact on flat 9×6 and
    10×6. On cyl:8×7 there are four other exact groups. No value in sums was computed for any of these
    (`kings/delegate/out/K48/REVIEW.md`).
  - K55 (2026-11-23) runs the other exact groups of K45 in sums. The 3 + 3 pawn group gives the same 38 differences from
    over on cyl:9×6 and 10×6. The 2 + 3 group of cyl:10×6 (`Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5`) has the results of over
    against all 752 test games tried (CHECKED-2, and a third solver on the decisive tests): a finite battery, not a proof.
    The difference is one move: in the 3 + 3 group 1…e5–e4 wins as soon as Black has a spare move, and the 2 + 3 group
    has no such move (COMPUTED-1). The value of the 3 + 3 group is not identified: none of over 3,000 candidates
    survives, and the group is not a stopper (`kings/delegate/out/K55/REVIEW.md`).
  - K56 (2026-11-23) gives a criterion that does force the results of over. Lemma 4.13 (PROVED by hand, re-derived by the
    referee): a group that is tempo-exact (Definition 4.12: Black's losing root moves still lose when Black has one spare
    move; White's lose against any number of spare moves, or after a Black pass in reply) has the results of over beside
    every finite test game, with or without terminals. No known group meets it: all nine exact groups fail on White's side,
    and the 3 + 3 group also on Black's, at 1…e5–e4. So the lemma has no instance yet and whether the 2 + 3 group is over
    stays open (`kings/delegate/out/K56/REVIEW.md`).
  - K57 (2026-11-23) settles the 2 + 3 group in sums. Proposition 4.14 (PROVED): over ≥ 0 in D-sums. Lemma 4.15 (PROVED): an
    exact group of Definition 4.8 has the results of over beside every finite test game if one condition holds on Black's
    side, (B1): after every non-shuttle Black root move White still wins when Black has one spare move elsewhere. Nothing
    more is needed on White's side. Corollary 4.16 (PROVED given CHECKED-2 computations): the 2 + 3 group
    `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` of cyl:10×6 has the results of over beside every finite test game. Both general
    statements were re-derived by an independent referee and proved again blind by Codex (K58); the referee recomputed (B1)
    with its own code and found 0 differences from over on 12,000 abstract groups. The 3 + 3 group fails (B1) at
    1…e5–e4. Not claimed: equality with over as a game, P contexts, chess (`kings/delegate/out/K57/REVIEW.md`).
  - K60 (2026-11-23) gives the exact condition. Theorem 4.18 (PROVED, re-derived by the referee; part (c) uses the known
    determinacy of Büchi games): an exact over group has the results of over beside every finite D-game iff, after every
    non-shuttle Black root move, White wins the position beside under when an infinite play counts for White only if
    White passed infinitely often. One short test game decides (Corollary 4.19), and (B1) is the case where White never
    passes. An abstract exact group fails (B1) and still has the results of over; no known real group does. The 3 + 3
    group fails the exact condition only at 1…e5–e4 (CHECKED-2). Open: a test family that does not depend on the group
    (`kings/delegate/out/K60/REVIEW.md`).
  - K61 (2026-11-24): Codex (gpt-6.2-astra) proved Theorem 4.18 and Corollary 4.19(i) blind, from the definitions and
    the statements only. Its proof of part (c) does not use the determinacy theorem. It also shows that the proofs
    need the e.p. right to add moves only, as it does in chess: in an abstract group where the absence of a right
    makes a move legal, the statements fail (`kings/delegate/out/K61/PROOF.md`; not refereed separately).
  - K59 (2026-11-23, refereed 2026-11-24): groups with the results of over on a flat board. Corollary 4.17 (PROVED
    given CHECKED-2 computations): five exact over groups on flat 8×7, with no wrap, have the results of over beside
    every finite D-game; the smallest has 2 + 2 pawns, `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6`. Four of them are also exact
    with (B1) on flat 8×8, the ordinary chessboard. The four cyl:8×7 groups of K48 have the results of over too
    (Corollary 4.16, (B1) now by two programs). The referee wrote a third solver and found no error; one wording
    correction (five placements, four shapes) (`kings/delegate/out/K59/REVIEW.md`).
  - K62 (2026-11-24, refereed): is there a test for the results of over that does not depend on the group?
    Theorem 4.20 (PROVED): the ladder T_b, b the number of boards of the group, decides (T_{b−1} in chess), so one
    ladder decides every group on one board size (Corollary 4.23). Theorem 4.22 (PROVED): no finite set of finite
    D-games decides for every abstract exact over group; the group Λ_N passes every D-game with at most N positions
    and fails one with N + 1. Proposition 4.21: every ladder length occurs. For king-and-pawn groups the question
    is open; the only real group that fails needs a ladder of length 2 (`kings/delegate/out/K62/REVIEW.md`).
  - K64 (2026-11-24): Codex (gpt-6.2-astra) proved Theorem 4.20 (a), (c), (d) and Theorem 4.22 blind, from the
    definitions and the statements only, with no repair (`kings/delegate/out/K64/PROOF.md`; not refereed separately).
  - K63 (2026-11-24, refereed): the 2 + 2 over group F2 on the ordinary 8×8 board. In chess it is not an exact over
    group (KNOWN, Syzygy tablebases): White Ka4, Pb2, Pf5 against Black Kc4, pb6, pf6 is a draw with Black to move,
    and the position after the freeze b2–b3 is a draw with Black to move. Only the freeze b2–b4 survives: after it
    (White Ka4, Pb4, Pf5; Black Kc4, pb6, pf6) the side to move loses. F1 behaves the same way; F3 and F4 keep the
    other freeze. Beside pawns on file h in P the D-sum prediction holds in 271 of 283 contexts; the 12 failures
    have a blocked White pawn on h2 that the Black king can win (CHECKED-2). So the results of over in D-sums carry
    over neither to chess nor to P contexts (`kings/delegate/out/K63/REVIEW.md`).
  - K65 (2026-11-25, refereed; the referee's own findings checked again by K66 with a third program): census of
    exact over groups on the flat 8×8 board, file classes {b,c,f} and {b,e,f}, at most 3 + 3 pawns: 38 groups, 26 up
    to symmetry, four with 2 + 2 pawns. (B1) holds for 27. Seven of the other 11 have the results of over all the
    same (first real examples; Corollary 4.19), three fail with ladder length 2, and one,
    `Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7`, has ladder length 3 (Proposition 4.24; the question is now length 4).
    In chess, by the tablebase, five of the 19 groups with at most seven men are exact over groups, for example
    `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` (`kings/delegate/out/K65/REVIEW.md`).
  - K68 (2026-11-25, refereed): the first real exact over group with a proof by hand, up to one computed lemma
    (Proposition 4.25). For `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` on the flat 8×8 board one White plan of eight moves
    (king to e5, d6, c7, takes b7, then the b-pawn promotes) proves that every bad Black move loses, that both
    freezes win, and (B1). That every other White move loses is reduced by hand to a two-pawns-against-one ending
    (Black Kb6, pb7, pc6 against a king and a c-pawn; 42 positions used), which three programs agree on and nobody
    has proved by hand. The referee re-derived every step and withdrew one false chess fact from the proof; the
    chess values stay KNOWN from the tablebase (`kings/delegate/out/K68/REVIEW.md`).
    For the lemma a model of another vendor, working blind, wrote a certificate: a table of 486 rows in which
    every White reply leads to a lower row (K70). Two separately written checkers accept every row and a referee
    checked 42 rows by hand without finding an error (K73); the full check by hand, about 40,000 replies, has
    not been done, so the lemma stays computed (`kings/delegate/out/K70/REVIEW.md`). Changing the reduction does
    not avoid the lemma (K71, unrefereed: 14 positions left).
  - K67 (2026-11-26, refereed by K77): the other two file classes of the shape on flat 8×8, {a,b,e} and
    {a,d,e}, hold 10 and 3 exact over groups (two search programs agree on every counter and group). With K65
    the four classes hold 48 distinct groups, 27 up to symmetry. Ten are new, with one new shape (`Ka5 kc4/kc5
    Pa4 Pa6 Pb2 pa7`, six men). Of the 48, 34 have (B1), 9 more have the results of ω because White wins Aux,
    and 5 fail condition (C): one needs the ladder T_3, four T_2. No group needs a longer ladder. Two of the new
    groups are exact over groups in chess, so seven in all, but they are only two shapes
    (`kings/delegate/out/K67/REVIEW.md`).
  - K72 (2026-11-26, refereed by K74): real over groups beside real pawns. The five seven-man groups that are
    exact in chess were put, in P, beside every context of at most 2 + 2 pawns on one separated file of the same
    8×8 board (283 contexts a file, three solvers agree on all 24,904 positions). Only one, C125_10 (White Kc5,
    Pb6, Pf2, Pf6 against Black Ke5/Ke6, pb7, pf7; file h), has the predicted result in all 283; even it fails
    in 3 of all 729 placements on h (smallest: four White pawns h3–h6 against h7). The other four fail with one
    pawn a side already. Every failing context of at most 2 + 2 pawns has pawns of both colours. Mechanisms: a
    king leaves the group and wins a context pawn (the Black king as in F2, or, new, the White king, which
    breaks the mutual zugzwang after the freeze), or a context pawn takes a buffer square from a group king. No
    theorem is contradicted: the theorems are about D-sums with an abstract game, and the kings are not kept
    apart by the buffer file (`kings/delegate/out/K72/REVIEW.md`).
  - Theorem 1.11(c) repaired (2026-11-23): its proof used the e.p. condition (E) without assuming it, and its frontier
    step used an unproved inheritance of threats by re-split components. (E) is now a hypothesis (every use already had
    it through Theorem 1.14), and the inheritance is proved. Found while the paper's proofs appendix was written and
    refereed (`kings/delegate/out/S12A/REVIEW.md`).
  - Foundations stated after a Codex report on the same appendix (2026-11-23, `kings/delegate/out/T81L/REVIEW.md`): the
    promotion convention (a pawn on its last rank stays and is passed), the order of operations in the sum model (test
    for passed pawns before splitting), threats by moves in any order, a passer-free root for Theorem 1.11(c), and
    Theorem 1.14 restated per side to move, since its hypotheses can hold for one starter only. 16 edits, refereed.
  - Theorem 2.7's timing clause corrected (2026-11-23, `kings/delegate/out/T83L/REVIEW.md`): the punisher wins by a
    promotion or a mate no later than its T-th move after the reply, and the reply itself may already mate (a context
    pawn can cover a square beside the king, so a real mate need not be a local mate). The win in P was not affected.
    Found by a Codex re-read of the paper's appendix.
  - Codex checks from outside the Claude family (2026-11-23, model gpt-6.2-astra): K51 proved Theorem 3.4 blind (it holds;
    one proof sentence was false and is corrected); K53 proved Proposition 2.10(a) blind (every step sound); K52 read
    Theorems 1.11(c) and 1.14 (both hold). After K52 the tempo step of 1.11(c)'s proof is replaced by a refereed
    argument, (E) is shown necessary by a counterexample on flat 5×7 (`W a4 b3 e2 / B a5 b4 e4` after a2–a4), threats
    for pawn positions are defined as the code checks them, and Theorem 1.14(i) requires a root before the first
    decisive event (`kings/delegate/out/K52/REVIEW.md`).
    K54 (Codex) then read the new proof of 1.11(c) and the corrected Theorem 2.7 as printed: every step sound, a few
    wording fixes applied (`kings/delegate/out/K54/REVIEW.md`).
  - K49 (2026-11-23) reduces K40's classes for K+P v K on the cylinder to one lemma (Lemma P: if White wins the bare
    normal-play game with Black to move, she wins it with White to move). Given it, the classes are proved by hand
    against every integer and every terminal-free test game, not only up to 12 spare moves. Lemma P is PROVED for the
    pawn one step from promotion and computed below that (CHECKED-2 on 16 boards); it fails on 4-file cylinders. The ON
    class is not one game: two positions on cyl:8×8 separate two types. The referee's corrected edits were applied.
  - So no result of the note is still GAP.
  - The T30 fixes of 2026-10-22 came later. They were reviewed by Sonnet reviewers in two rounds, not by K3 (see the Theory row
  above).
- A non-Claude referee (K2, kilo nemotron, `kings/delegate/out/K2/REPORT.md`) recomputed every number in
  this report from the raw files and confirmed all of them. It also re-ran the cross-check and the 8×8 king
  groups, with identical results.
  - Its own mini-solver disagreed with kpsolve on 3 of 20 random 4×4 positions. The independent reference
    solver sides with kpsolve on all 3, so the mini-solver was wrong.
  - Its wording criticisms are reflected in §1 and §7.

## 8. Open questions

- **8-rank sweeps.** The sweeps use 6 ranks to fit the compute. On 8 ranks the trébuchet's punishment is
  slower (T ≈ 5–7) and the kings are further from the component, so the convention should fail less often.
  The ordinary-board data suggests the same.
- **The paper's full positions.** 7.2 with its {a,b,h} pawns has 10 men on 8×8, out of reach for an exhaustive
  solve here. Theory §5.2 says it is still a White win when White wins the pawn part.
- **`dud`.** Answered in P by K15b and K26 (above): Z_B, Z_C, G8a and G8b are dud groups with no pawn break; in chess
  Z_B and Z_C are not exactly two-shuttle (K28, K39).
- **Opposition on cylinders** (plan A8) is covered by the main project's tasks T12 and T25, not by this
  report. [research/odd_cylinders_verify/REPORT.md](../research/odd_cylinders_verify/REPORT.md) checks it
  with kpsolve and `kings/ref` together (CHECKED-2: 1,058,628 cylinder positions, 0 disagreements).
  - "Direct opposition is always a draw" is refuted: of the 4,288 direct-opposition triples on C8×8, 984 are
    draws and 200 are mutual zugzwangs.
  - `Ka3 Pa2 ka5` is a draw on the flat board and a mutual zugzwang on every cylinder.
  - The paper gives the table in §X-A (Table VI).
- **Gafni's K+P vs K values without edges** (plan A8). Answered on cyl:3–8 × 6–8 by K40 (above). Earlier, task K4 ([delegate/out/K4/REPORT.md](delegate/out/K4/REPORT.md)).
  The thesis itself was not located (`notes/novelty_check/REPORT.md`). So K4 computed the same kind of object
  under a stated convention: normal play, so a stalemate loses; infinite play draws; a test-game move is illegal
  while in check.
  - **Scope.** K+P vs K on flat and cylinder boards 3×4, 4×4, 3×5, 4×5 and 5×5: 20,556 quiet placements, each
    summed with 16 test games and compared with 26 candidate values. The 3×3 board is outside SPEC.
  - **Checks (CHECKED-2).** With stalemate a draw, the solver agrees with kpsolve on 294,749 positions (0
    differences). Two independent re-implementations reproduce every placement (0 differences).
  - **No number or infinitesimal occurs.** Every placement is a decisive White win, on (tied with on + \*),
    off, dud, or unmatched. off is exactly the White-stalemated pattern, so it is an artefact of the convention.
  - **Edges.** 12.5%–20.5% of the placements change class when the edges go, and on is more frequent on the
    cylinder at every size.
  - **Tempo.** Task K6 ([delegate/out/K6/REPORT.md](delegate/out/K6/REPORT.md)) extends this to 27 boards,
    CHECKED-2 by an independent pipeline.
    - On cylinders of 3 and 5–8 files, with 4–6 ranks, no finite test game or integer n ∈ [−10, 10] changes any
      result.
    - The 4-file cylinders and every flat board have some tempo-sensitive placements. Their thresholds lie at
      n ∈ {−3, …, 0}, deepening by one with each extra rank.
    - K4's odd-width explanation is withdrawn. Sensitivity coincides with White being stalemated in
      front of its own pawn (CONJECTURE).
    - Task K8 ([delegate/out/K8/REPORT.md](delegate/out/K8/REPORT.md); CHECKED-2 by K8v) confirms all 8 new
      predictions of that pattern, which now holds on 38 boards. It also shows that the insensitivity comes from
      the stalemate-loses convention.
      - Under chess's stalemate rule, 5- to 7-file cylinders are sensitive too. Only 3-file cylinders stay
        insensitive.
      - Only Black's stalemate rule decides which placements are sensitive; White's never changes the set.
      - Every kpsolve mutual zugzwang is sensitive to one spare move (PROVED). Most sensitive placements are
        not zugzwangs.
    - So "no finite king tempo" fails as a whole-board statement, though Proposition 4.3 is not tested by this.
  - **Gafni.** His reported values (a second-hand summary) do not appear: on + \* only as a tie with on, and no
    {on | 0} or 1 + \*. That is no contradiction, because his conventions are unknown.
- **CGSuite modelling** (plan A8) is open. It needs CGSuite and a Java runtime to be installed, which needs
  the user's approval; neither is installed. A partial stand-in, task K5b, checks cylcgt's canonical forms by
  a different method. For each value V it plays G + (−V) out with the brute-force solver `sumtest/sumsolver.py`,
  which computes no canonical forms; G = V exactly when that sum is a second-player win (𝓟).
  - The targets were 1/8 (three positions), 1/16, ↑², ↑²\*, tiny(1), the 4-pawn \*2 candidate and the C3 ring
    \*2, each under 9 settings (race rule × e.p. treatment).
  - **CHECKED-2:** all 39 claimed values hold. cylcgt's own value holds at 72 of the 81 target × setting pairs,
    with 0 failures; the other 9 contain ±BIG and were not tested.
  - An auditor recomputed everything with its own script and found 0 differences. Results:
    [delegate/out/K5b/REPORT.md](delegate/out/K5b/REPORT.md).
  - Caveat: sumsolver was also written by a Claude model. So the check is independent of cylcgt's code but
    not of the model family, and a rules misreading shared by both programs would not be caught.
  - The first attempt, K5, is rejected. Its "independent" engine copied `cylcgt/cgt.py`
    ([delegate/out/K5/REVIEW.md](delegate/out/K5/REVIEW.md)).

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
