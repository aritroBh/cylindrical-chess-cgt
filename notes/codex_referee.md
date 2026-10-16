> Independent referee report by Codex (gpt-6-luna, max reasoning), 2026-10-15. Unverified model output: where it conflicts with `cylcgt`, the solver wins (see RESEARCH_PLAN.md §1 for the three known Codex errors: 4.3 a6xh5 exists, Kh5-g5 drops a4, 3.1 has no h4 pawn).


## Part A — Referee report

The central issue is the terminal rule. Conway short games use normal play: a player unable to move loses. “A pawn has passed, so its owner wins immediately” is a player-labelled terminal outcome; it is not automatically the CGT value \(0\). The paper needs an operational definition of “passed,” must say whether a passer ends the whole game, and must resolve positions with passers for both sides. CGT has extensions for such outcomes, but they are not ordinary short-game values; one treatment explicitly adds “victorious positions” and changes the outcome model. [Weimerskirch, *Generalized misère play*](https://library.slmath.org/books/Book70/files/1023.pdf)

Likewise, kings make the games potentially loopy. The king positions in 5.1, 7.2, and 7.3 cannot be treated as independent zero games without proving they are frozen. A draw or infinite-play rule is needed before assigning game values.

| Position | Referee finding |
|---|---|
| **2.1, ZeroGame1** | Correct: the pawns on e4/e5 are mutually blocked and neither can capture. The value is \(0\). |
| **2.2, ZeroGame2** | White’s pawn on h1 is illegal. If treated as an abstract movable pawn, the position has a second-player-win outcome: after h1–h2, Black can capture across the wrap with a3xh2; after h4–h3, White can capture across the wrap with a2xh3. That outcome alone does **not** establish CGT value \(0\) under the immediate-passer rule. |
| **2.3, ZeroGame3** | White’s c1 pawn is illegal. The diagram is not the frozen position 2.1: it has White c1,d2 and Black c4,d3, with moves such as c1–c2 (if the illegal pawn is allowed) and c4–c3. |
| **3.1, “1”** | White’s h1 pawn is illegal. The a- and h-file pawns interact: White a3xh4 and Black h4xa3 are both legal wrap captures. The claimed \(\{0\mid\}\) tree omits these moves, so the diagram does not establish value \(1\). |
| **3.2, “2”** | White’s h1 pawn is illegal. The diagram changes several pawns from 3.1; it does not merely move one pawn back. The a/h seam also permits interactions omitted from the claimed \(\{0,1\mid\}\) tree. I could not settle a canonical value under the paper’s terminal rule. |
| **4.1, StarGame1** | Correct: either pawn’s move leaves the other blocked, so \(*=\{0\mid0\}\). |
| **4.2, UpGame1** | The diagram is \(0\), not \(\uparrow\). White e3–e4 and Black e6–e5 are the only initial moves; each leads to \(*\). Thus the root is \(\{*\mid *\}\), which reduces to \(0\). The abstract reversibility reduction from \(\{0,*\mid *\}\) to \(\{0\mid *\}=\uparrow\) is beside the point: the diagram has no White move to \(0\). Its color-swapped version is also \(0\), not \(\downarrow\). |
| **4.3, “Tiny 1”** | The board has legal moves W h4–h5, W h4xa5, and B a5xh4. After h4–h5, Black has no pawn move while White retains moves such as h5–h6 and h5xa6. This is not the claimed branch where White’s advance gives Black a passed pawn. The diagram does not realize the stated Tiny form; I did not settle its full canonical value. |
| **5.1, Trebuchet \(0\)** | The pawns are blocked, but the kings are mobile. Kh5–g5 is a safe White move; Black also has safe moves such as Kb4–c4. King play can affect the pawns and can repeat, so this is not an isolated short \(0\) game. |
| **7.1, puzzle total** | The c-file component does match \(\{1\mid-1\}=\pm1\). The f-file component also matches \(\{\{2\mid1\}\mid0\}\) when Black’s legal f7–f5 double-step is included. The a/h component is not established: W a5xh6 and B h6xa5 are legal wrap captures, as is W h3–h4. I could not settle that component or the total. If a passed pawn ends the whole game, summing local components is invalid anyway. |
| **7.2, \(0\pm1\)** | The kings are not the 5.1 Trebuchet and cannot be assigned value \(0\) by reference to it. White d7 is already a pawn-passed pawn under the usual pawn-only test; if that means an immediate win, the listed game tree never starts, even though the black king occupies d8. White a2–a4 and b2–b4, and Black b7–b5 and h7–h5, are also legal double-steps omitted from the analysis. The written line has Black play b5 twice. No short CGT sum is justified. |
| **7.3, “2”** | White a5 is already passed under the usual pawn test, and f7–f8 promotes immediately if White moves first. Calling a5–a6 a promotion is also incorrect; promotion is on rank 8. The diagram has illegal White pawns on a1, c1, g1, and h1. The king game is not a Trebuchet summand. The claimed value \(2\) is false under the stated rules. |

The number-avoidance principle applies to a **disjunctive sum** with a genuine number component; it does not validate a decomposition when captures cross between components or a pawn win terminates the whole board. “Move to the component with highest temperature” is not a general rule. The half-spread formula applies to a simple switch with numerical endpoints; move choice in a sum depends on the full game and strategy. Also, an outcome such as “White wins regardless of who starts” does not determine an exact value such as \(1\).

### Dawson’s Chess and the ring

The written rule—remove a pawn only when both neighbors are already empty—permits no first move from a full ring \(C_n\), \(n\ge3\); that position has Grundy value \(0\).

Standard Dawson’s Chess, octal \(0.137\), removes the selected pawn **and its occupied neighbors**. On a path, endpoint moves remove two pawns, while an isolated pawn can be removed alone. The paper’s recurrence omits those moves; its triplet-only recurrence is not \(0.137\). The correct path values start \(g_0=0,\ g_1=g_2=1\), with
\[
g_n=\operatorname{mex}\!\left(\{g_{n-2}\}\cup
\{g_a\oplus g_b:a+b=n-3\}\right),\quad n\ge3.
\]
For the intended closed-neighborhood rule on a full ring, each move removes three consecutive pawns and leaves a path of length \(n-3\), so \(R_n=\operatorname{mex}\{g_{n-3}\}\). Thus \(R_8=0\), since \(g_5=3\). This ring formula is right only for the corrected rule and path sequence. The standard rule and the sequence are documented in [Weimerskirch](https://library.slmath.org/books/Book70/files/1023.pdf) and [OEIS A002187](https://oeis.org/A002187).

## Part B — Ranked research directions

Novelty should be topology-specific. Elkies already exhibited fractions, switches, tinies, and loopy games in chess endgames, and later constructed higher nimbers on large flat pawn boards while raising questions about nonstandard boards. Avoid claiming “CGT applied to chess” as new. [Elkies 1999](https://arxiv.org/abs/math/9905198), [Elkies 2000](https://arxiv.org/abs/math/0011253)

1. **Certified exact-value atlas for cylinder pawn games — M.**  
   **Question:** Which canonical forms occur with at most \(k\) pawns on an \(n\)-file cylinder? **Method/success:** Specify terminal rules, enumerate small positions modulo file rotation, canonicalize options, and publish replayable move-tree certificates; prove completeness for one bounded class. **Novelty/risk:** A topology-specific value atlas is a credible contribution; CGT endgame databases already exist for other games, so the solver alone is not the result. Immediate-passer terminals must be excluded or formally extended. [Domineering database precedent](https://arxiv.org/abs/1506.03949)

2. **Flat vs cylinder vs torus realizability — L.**  
   **Question:** Does wrapping enable or forbid specific nimbers, dyadic numbers, switches, ups, or tinies as width changes? **Method/success:** Search small witnesses, then prove a repeatable construction or obstruction for one named family. **Novelty/risk:** Elkies already did large-board nimbers; focus on a theorem for a bounded family and compare flat, \(n\)-cylinder, and torus. A complete classification is out of scope.

3. **Exact thermographs for cylinder pawn components — M.**  
   **Question:** Which independent pawn subgames change temperature or mean under wraparound? **Method/success:** Generate only components with verified noninteraction; compute canonical forms and thermographs, then prove a structural explanation for one topology-induced change. **Novelty/risk:** Useful mathematical output, but a discovered hot component does not imply a simple “play the hottest” strategy. Component independence and terminal rules are the main risks.

4. **Loopy king endgames on cylinder and torus — L.**  
   **Question:** Are KBBK, KBNK, or KNNK wins when the board has no corners; is KQK winning on a torus? **Method/success:** Build a four-piece retrograde solver with check legality and infinite play/repetition explicitly treated; publish WDL classifications and witness lines. **Novelty/risk:** Likely topology-specific, but not a Conway short-game value. Agree on draw rules before computing.

5. **A correct Ring Dawson sequence — S–M.**  
   **Question:** What Grundy values arise on \(C_n\) under the actual “remove pawn and occupied neighbors” rule? **Method/success:** Enumerate small cycles, prove the \(R_n=\mathrm{mex}\{g_{n-3}\}\) reduction for full rings, and tabulate values. **Novelty/risk:** The paper’s path/ring conflation is a good student-sized correction; graph versions may already exist, so novelty must be a new cycle result, not the label “ring.”

6. **Cylinder move-generation patch for Fairy-Stockfish — L.**  
   **Question:** Can wraparound move generation be added without changing orthodox behavior? **Method/success:** Patch pawn attacks, en passant, king steps, sliders, and bitboard masks; differentially compare against a simple reference generator on exhaustive reduced positions. **Novelty/risk:** Fairy-Stockfish has configurable variants but no cylinder topology option in its public config; standard Stockfish file masks stop at a/h. Treat the engine as infrastructure, not the paper’s main theorem. [Fairy-Stockfish](https://github.com/fairy-stockfish/Fairy-Stockfish/blob/master/src/variants.ini), [Stockfish bitboards](https://github.com/official-stockfish/Stockfish/blob/master/src/bitboard.cpp)

7. **Cylinder-trained NNUE evaluation — M.**  
   **Question:** Do exact cylinder endgame labels improve held-out WDL calibration or fixed-node play? **Method/success:** Train a small evaluator from solver/tablebase positions; compare against material, a flat-trained net, and an untrained baseline. **Novelty/risk:** Keep claims to low-material endgames and calibration. The official NNUE training material documents CUDA-specific optimization, so benchmark a CPU/MPS path early on the M4 Pro. [Stockfish NNUE docs](https://official-stockfish.github.io/docs/nnue-pytorch-wiki/docs/nnue.html)

8. **Cyclic-file-equivariant value network — M.**  
   **Question:** Does hard-wiring \(C_8\) file-shift equivariance improve data efficiency over ordinary CNNs and rotation augmentation? **Method/success:** Train on exact values, test unseen file shifts and widths, and report invariance checks plus held-out accuracy at equal data/parameter budgets. **Novelty/risk:** Equivariant networks for games already exist; the novel target is the cylinder’s cyclic translation symmetry. [Finite-group equivariant games](https://arxiv.org/abs/2009.05027)

9. **Compositional generalization on CGT sums — M.**  
   **Question:** Can a model trained on isolated components predict exact values of unseen sums? **Method/success:** Hold out combinations of certified independent components, then compare predicted canonical value and winning move against symbolic addition. **Novelty/risk:** Strong test of compositional reasoning; falsely treating wrap-coupled pawns as independent would poison the labels.

10. **Solver-certified adversarial benchmark for engines, LLMs, and RL — M.**  
    **Question:** Can Stockfish, Lc0, LLMs, or self-play RL solve short positions whose winning moves depend on exact CGT arithmetic? **Method/success:** Publish certified positions with legal moves, values, and proof trees; score value accuracy, strategy, and certificate validity separately. **Novelty/risk:** Nim already exposes weaknesses of generic self-play RL, so the contribution must be the partizan arithmetic and verifiable rewards, not another chess QA set. [RL on impartial games](https://arxiv.org/abs/2205.12787)