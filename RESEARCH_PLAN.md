# Research Plan: Cylindrical Chess Endgames, Exactly and with Learning

*Continuation of "Analysis of Chess Endgames on a Cylindrical Chessboard" (A. Bhattacharjee, mentored by T. Morley, June 2025). Drafted 2026-10-15 by Claude (Opus) with Codex (gpt-6-luna) and three research subagents.*

---

## 0. Summary

The 2025 paper applied Elkies-style combinatorial game theory (CGT) to pawn endgames on an 8×8 board whose a- and h-files are glued. Its hand computations stop where game trees get large, and several are wrong (§1).

The literature search (§2) found **no published CGT work on cylindrical or toroidal chessboards**, and **no published tablebases for them**. Elkies' own open problems about the 8×8 board are mostly still open.

The continuation is a **machine-verified research program** with three tracks:

1. **Exact mathematics (Track A).** A verified CGT engine for pawn endgames on cylinders, flat boards and tori of any width. It will (a) prove the structural lemmas the paper assumes, (b) map which values occur only on a cylinder, (c) attack Elkies' open problems (\*2 from kings and pawns alone on 8×8, \*4, 1/8, ↑²), and (d) extend the analysis to king moves (loopy games) and temperature.
2. **The first cylinder and torus tablebases (Track B).** They settle "with no corners, what mates still work?" and supply ground truth. A 4-man prototype already answers part of this (§1.3).
3. **Learning against exact truth (Track C).**
   - Sums of many small games are trivial for CGT but exponential for search. That makes them a principled adversarial benchmark for Stockfish, Leela and LLMs. The closest prior work (Husna & Müller 2024, Go) never varied the number of components.
   - The same positions test whether neural nets and RL-trained LLMs learn the algebra of sums.

Each track can yield its own paper. Targets: *Integers* / *Games of No Chance 7* (A), *ICGA Journal* / *Advances in Computer Games* (B), and a NeurIPS/ICLR workshop (C).

---

## 1. What exists after today

### 1.1 Tools built this session
| Path | What it is | Status |
|---|---|---|
| `cylcgt/cgt.py` | Exact canonical-form CGT: numbers, nimbers, ↑-family, tinies, switches, sums, outcome classes, thermographs (mean, temperature) | Unit-tested (`tests/`) |
| `cylcgt/pawns.py` | Pawn-only positions on any W-file board, flat or cylindrical; double steps; wrap-around en passant; decomposition into independent components; explicit race rule; `sum_safe()` flag | Cross-checked (below) |
| `cylcgt/verify_paper.py` | Recomputes every pawn-only claim of the 2025 paper | Output in `notes/verify_paper_output.txt` |
| `cylcgt/explore.py` | Exhaustive enumeration of value spectra, cylinder vs flat | Prototype (~0.6 ms per position) |
| `cylcgt/dawson.py` | Dawson's chess solved directly from the pawn rules, flat and ring | Prototype |
| `crosscheck/` | **Independent** whole-board minimax written by Codex (it does not use `cylcgt`) | **All 1070 single-component positions agree; 99.5% of sums agree** |
| `tablebase/egt_prototype.c` | 4-man retrograde DTM solver for plane, cylinder and torus | Reproduces known flat-board maxima |

**Cross-check, in detail.** Run on 3,028 random and paper positions:
- After one bug fix (a passed pawn must end the whole game before splitting into components), single components agree **100% (1070/1070)**.
- The 10 remaining disagreements, all in multi-component sums, are the known "+BIG and −BIG cancel" limitation. Details are in `crosscheck/REPORT_after_fix.md`.

### 1.2 Audit of the 2025 paper (full table: `notes/audit.md`)
- **Correct:** 2.1, 2.2, 3.2, 4.1, 4.3 (tiny-1), the 7.1 c-file (±1), and the 7.1 f-file ({{2|1}|0}, mean = temperature = 3/4).
- **Correct only because of wrap-around en passant**, which the paper never mentions: 3.1 is `1` with e.p. and `2` without.
- **Wrong:**
  - **4.2 as drawn is `0`, not ↑.** The diagram is one rank off: W e2 / B e5 gives ↑.
  - **The 7.1 a/h component is a hot game, `{win | *}`, not `1`.** The wrap captures a5×h6 and h6×a5 were missed.
  - **7.2's pawn group is not ±1**, and its value depends on en passant. Its analysis also omits the double steps and plays ...b5 twice.
  - **7.3 is already decided at move 0** by the passed pawns on a5 and f7.
- **Modelling gaps:**
  - The "trebuchet" king groups in 7.2 and 7.3 are not mutual zugzwangs: both kings have spare tempo moves.
  - Pawns stand on the 1st rank, which is illegal.
  - Races and en passant inside sums are left undefined.
  - §8's Dawson rule permits no first move. The correct model is octal 0.137, and the paper's path recurrence omits the end moves.
  - The Wu–Yü–Landry citation is dated 2020 but is from 2010.
- **Model errors we caught:** Codex's referee report wrongly says that 4.3 has no black reply (a6×h5 exists), that Kh5–g5 is "safe" in the trebuchet (it drops a4), and that 3.1 has a pawn on h4. This is why every claim is machine-checked.

### 1.3 First new results (preliminary; each needs the verification protocol in §4)
1. **Candidate \*2 made only of kings and pawns on an 8×8 board.**
   - On files a–d with the e-file empty, `W a2 c2 / B b7 d7` has value **\*2** = {0,\*|0,\*}, with or without en passant.
   - Elkies (1996) left open whether \*2 occurs on 8×8. Drummond-Cole (2005) found one, but it needs bishops, knights, rooks and queens to freeze the pawns.
   - If this survives with real kings (the trebuchet on the g-file, kings on f/h) under engine and tablebase verification, **it answers an open question.**
   - Risk: the "passed pawn = win" convention may not survive real king play.
2. **Values that occur only on the cylinder.** Exhaustive 2-vs-2 enumeration on 3–5 files finds values that never occur on flat strips of the same width, e.g. 1/4±1/4, 3/4, and {3/2±1/2 | −3/2±1/2}. Some flat-only values (including that \*2) disappear on the cylinder.
3. **Mating material without corners** (4-man tablebase; one implementation; the flat-board sanity check passes):

| Material | Flat 8×8 | Cylinder 8×8 | Torus 8×8 |
|---|---|---|---|
| KQK | win, mate in ≤ 10 | win, mate in ≤ 10 | **no mate exists** |
| KRK | win, 16 | **draw** (2.8% of positions won) | no mate exists |
| KBBK, opposite colours | win, 19 | **win, 14**, all positions won | draw |
| KBNK | win, 33 | **draw** (0.024%) | draw |
| KNNK | draw | draw | draw |

   The cylinder result for the bishop pair contradicts a published claim by H.G. Muller. The KBNK result is new as far as we found.

---

## 2. Literature: what is done and what is open
*Full notes: `notes/lit_cgt_chess.md`, `notes/lit_cylinder.md`, `notes/lit_ml.md`, `notes/codex_referee.md`.*

**Known**
- **Elkies 1996** (GONC; arXiv math/9905198): numbers including 1/2 and 1/4 on 8×8; \*, ↑, ⇑\*, tiny-1/2, switches; loopy values (on, off, over, dud).
- **Elkies 2002** (MGONC; arXiv math/0011253): \*2, \*4, ..., \*4096 on large boards via a 3-row pawns game with "stopped files".
- **Mäser 2002:** promotion modelled as on/off.
- **Drummond-Cole 2005:** \*2 on 8×8, but it needs pieces.
- **Siegel:** loopy theory; chess positions of value on and upon.
- **Gafni 2011:** loopy K+P vs K on tiny boards.
- **Affine normal play** (Larsson–Nowakowski–Santos 2025): theory for game-ending moves such as checkmate.
- **Dawson's chess** = octal 0.137 (period 34). The misère version is still unsolved.
- **Software:**
  - CGSuite: loopy games are first-class.
  - Rust crate `cgt`.
  - Nicholson's `partizan`: alpha-stage chess FEN → canonical forms. **This is the closest existing tool and must be checked before we build B1/C1.**

**Open problems we can attack**
- \*2 from kings and pawns alone on 8×8.
- \*4 on 8×8.
- 1/8 on 8×8.
- ↑² and ↑³.
- tiny-½.
- "Chilled chess".
- A systematic treatment of en passant, checks and captures.
- Elkies' "does every \*k occur?" (Nowakowski 2025, B3).
- Density of \*k.

**Cylinder and torus**
- Rules exist (Pritchard ECV; Wikipedia), but conventions vary: castling, and the "rook goes round the rank" null move. The null move must be banned before building tablebases, because a free pass destroys zugzwang.
- Mating-material claims are scattered and unproven.
- No tablebases, no perft numbers, no strong engine. Fairy-Stockfish declined support (issue #753). There is an unofficial 2026 copy, mtaktikos/CylindricalChess, with loop-based sliders.
- The only CGT work on cylinders is Domineering (Lachmann–Moore–Rapaport), and it determines only the winner.

**ML**
- Zhou & Riis (*Machine Learning*, 2026): AlphaZero fails Nim parity. But their "partizan" control was a sum of integers, so **whether nimbers or infinitesimals drive the difficulty is untested.**
- Husna & Müller (CG 2024): KataGo against CGT ground truth in Go. The number of components was not varied.
- Missing entirely:
  - an RL-with-verifiable-rewards (RLVR) environment for CGT;
  - a train-on-components / test-on-sums study;
  - an LLM evaluation on zugzwang.
- Tooling: `mlx-lm-lora` 5.8 has GRPO with custom reward functions, which fits the M4 Pro.

---

## 3. Research program

**Ground rule:** every computational claim is double-implemented, and every proof is checked by two models and by a human (§4).

### Track A: Exact CGT of cylinder pawn endgames

| ID | Question | Method | Done when |
|---|---|---|---|
| A0 | **Fix the model** | Write the rules down precisely: passed pawn = ±BIG versus Mäser's on/off; race semantics; en passant inside sums; legal versus generalised positions; `sum_safe` positions only in published sums. Long term, adopt *affine normal play* (∞-terminal games) so that "first passer wins" is exact rather than approximate. | A "Conventions" section; solver flags; 100% agreement with the cross-check on single components ✅ |
| A1 | **Structural lemmas** | (i) **Empty-file invariance:** an empty file stays empty, so components separated by one are exact summands. (ii) **Embedding:** a cylinder position with an empty file equals a flat position on ≤ 7 files, so every new phenomenon lives in **ring components** (all files occupied). (iii) Symmetries: cyclic shifts and reflection, and colour reversal giving −G. | Written proofs, checked by enumeration |
| A2 | **Resolve the \*2 candidate** | Embed `W a2 c2 / B b7 d7` with real kings (a g-file trebuchet). Verify: (1) the CGT value on the 8-file board; (2) every option's chess outcome, by Stockfish search and, for 8 men, Lichess's Op1 partial 8-man tablebase if it covers the position; (3) a sum test on a wider cylinder or a 10-file board, where \*2 + \* must be a first-player win. Then compare with Elkies' and Drummond-Cole's conventions. | A legal 8×8 king-and-pawn position certified \*2, or a precise reason why the convention fails |
| A3 | **Value atlas** | Enumerate all positions up to k pawns on n-file cylinders, flat strips and tori (n = 3…8, heights 6–10), modulo symmetry. Tabulate canonical values, outcome classes and temperatures, and diff cylinder against flat. Port the hot loop to Rust (or reuse the `cgt` crate). Publish move-tree certificates. | A public dataset; a table of values realisable only on C_n; minimal witnesses |
| A4 | **Elkies' open targets** | Search the atlas (and targeted constructions) for \*4, 1/8, ↑², tiny-½ on 8×8 and on 8-file cylinders. Run Elkies' 2002 stopped-file pawns game on **cyclic words**: rotations make distinct options, which may give higher nimbers on smaller boards. | Any one solved open problem ⇒ paper |
| A5 | **Closed forms** | Values of one- and two-file structures as functions of gaps; the effect of double steps; behaviour as width n grows, with odd n breaking opposition parity. | Proved formulas matching the data |
| A6 | **Dawson's chess on a ring** (repairs §8) | Solve directly from the pawn rules (`dawson.py`). Prove the reduction from a ring to a path of length n−3. Then attack the **misère** ring version: Dawson's misère problem is unsolved for paths, and the ring may be tractable via misère quotients. | Theorem plus table; misère results as a bonus |
| A7 | Temperature | Compute thermographs of all atlas components. Measure how often "play the hottest move" fails in sums. Find the maximum temperature as a function of circumference and height, and compare with Elkies' (N−5)/2. | Statistics plus counterexamples |
| A8 | **Kings: loopy CGT** | Model trebuchets and opposition on cylinders as loopy games (on, off, over, stoppers) using CGSuite. State exactly when "pawns only + a frozen trebuchet = chess" is valid, checking against Track B. Re-examine Gafni's K+P vs K values without edges. | Rigorous validity conditions; 7.2 and 7.3 as worked counterexamples |
| A9 (stretch) | Formalisation | Formalise A1 and the core canonical-form lemmas in Lean 4 (Mathlib `SetTheory.PGame`). | Proofs compile |

### Track B: Cylinder and torus tablebases, and an engine

| ID | Question | Method | Done when |
|---|---|---|---|
| B0 | **Rules decision** | Fix the rules: no rook "pass" around the rank, no castling in endgames, en passant across the seam, no 50-move rule for DTM tables. | Written spec |
| B1 | Fast move generator | Bitboards: leaper shifts rotate within each rank byte; rank sliders use a [file][occupancy] table; diagonal helices use a kindergarten multiply. Legality = pseudo-legal moves plus an "is the king attacked" test, because there are two routes between squares. Check against Nicholson's `partizan` and the mtaktikos copy. | **Publish cylinder perft numbers**, matching an independent mailbox generator and Jocly/Ludii |
| B2 | **Tablebases** | Independently re-implement the 4-man results of §1.3, then extend to all 5-man and pawnless 6-man endgames. On the cylinder there are 138 pawnless king-pair classes, and a 6-man table is about 2×10⁹ positions, which fits in 48 GB. Report maximal DTM, mutual-zugzwang counts against Haworth's flat-board numbers, the KPK and KPKP rules without rook pawns, and the torus. | A table of every "can X force mate?" answer, plus public files |
| B3 | Cylinder engine | Fairy-Stockfish (or the mtaktikos copy) with B1's slider tables and two-route pins and checks; probe our own tablebases in search; train NNUE with variant-nnue tools. | Perft-clean; beats the baseline; plays over UCI |
| B4 | Bridge CGT ↔ chess | Confirm every king-dependent claim from Track A with B2 or B3. | Every published position engine- or tablebase-certified |

### Track C: ML, RL and LLMs against exact ground truth

| ID | Hypothesis | Method | Metric |
|---|---|---|---|
| C1 | **ChessSums: engines and LLMs fail on sums, and the \*-part drives it** | Build legal standard-board positions from k certified components (integers, \*, ↑, switches, 0) plus a locked king zugzwang. Keep more than 7 men so Syzygy cannot shortcut. Run Stockfish 17/18 (node sweeps), Lc0 (Metal backend) and LLMs (GPT-6 via Codex, Claude, Qwen and others via opencode). | Accuracy vs k; the growth exponent of nodes-to-solve; the "parity gap" = accuracy on integer sums minus accuracy on nimber sums |
| C2 | **Compositional generalisation** | Train on k ≤ 2, test on k = 3–8. Compare a CNN, a circular-padded CNN (exactly equivariant on the cylinder), a transformer, and Deep Sets with a structured latent (a Z₂^m part for nimbers and a real part for numbers). | Accuracy at k = 8 relative to k = 2; does the learned sum obey G + (−G) = 0? |
| C3 | AlphaZero on Dawson's chess and cylinder pawn games | OpenSpiel or our own PyTorch on MPS; exact values from A3 and A6. Extends Zhou & Riis to partizan sums. | Elo vs "expert" accuracy by value class |
| C4 | **RLVR for Conway arithmetic** | GRPO on Qwen 0.5–3B with `mlx-lm-lora`, using our engine as the reward. Tasks: nim-sums, canonical forms, comparisons, temperatures, chess position → value. | Exact match on held-out, larger instances; transfer to C1 |
| C5 (stretch) | Neural or LLM proposers for rare values | A model proposes, the exact engine verifies; hunt for A4's targets faster than enumeration. | New witnesses |

### Track D: Writing and release
- **Paper 1** (about week 6): "Combinatorial game values of pawn endgames on cylindrical boards." Corrects the 2025 paper and covers A0–A7, plus A2 if it holds.
- **Paper 2** (about week 8): "Endgame tablebases and perft for cylinder and torus chess" (B0–B2).
- **Paper 3** (about week 10): "ChessSums: sums of games as an adversarial benchmark for chess engines and LLMs" (C1–C4).
- **Release:**
  - `cylcgt` on PyPI.
  - The atlas and tablebases on Hugging Face.
  - An interactive explorer: click a position, see its value, thermograph and best move.

---

## 4. Who does what, and the verification protocol

| Agent | Role |
|---|---|
| Claude (this session, Opus) | Architecture, CGT engine, proofs, integration, writing; final arbiter |
| Codex CLI (gpt-6-luna, max reasoning) | Independent re-implementations (it already wrote `crosscheck/`), referee reports, Rust/C++ move generator, second tablebase |
| cursor-agent / opencode / Qwen Code | Parallel experiment runners and code reviewers; contestants in the LLM benchmark |
| Claude subagents | Literature, data analysis, figures |
| You and Prof. Morley | Priorities, proof review, chess intuition, checking positions on a real board |

**A claim is publishable only if:**
1. Two independent implementations agree.
2. Any king-dependent claim is engine- or tablebase-certified.
3. A second model plus a human have re-derived any proof.
4. Sums use only `sum_safe` positions, or exact whole-board search.

---

## 5. Timeline (≈10 weeks, tracks in parallel)

| Week | Track A | Track B | Track C |
|---|---|---|---|
| 0 (today) | Engine ✅, audit ✅, cross-check ✅, \*2 lead | 4-man prototype ✅ | Literature ✅ |
| 1 | A0, A1, **A2 (\*2)** | B0, B1 + perft | Install Stockfish/Lc0; C1 generator |
| 2–3 | A3 atlas (Rust), A6 Dawson | B2 4–5-man (independent) | C1 engine and LLM runs |
| 4–5 | A4 open targets, A5, A7 | B2 6-man pawnless | C2 |
| 6 | **Paper 1 draft**, A8 | B3 start | C3 |
| 7–8 | A8 + B4 bridge | **Paper 2 draft** | C4 GRPO |
| 9–10 | Revisions | B3 NNUE (stretch) | **Paper 3 draft** |

---

## 6. Setup (needs your OK)
- A Python 3.12 venv (`.venv`, **done**) plus `python-chess`, `numpy`, `torch` (MPS), `mlx`, `mlx-lm-lora`, `matplotlib`.
- `brew install stockfish lc0`; `rustup` (for B1/B2/A3); CGSuite (Java) for loopy cross-checks.
- `git init` the project so every result traces to a commit.
- Optional paid GPU time for C4, only if MLX is too slow. I will ask before any spending.
- Codex usage limit: it hit its quota today, resetting about 02:21. Long Codex jobs need to be scheduled around that.

## 7. Risks
| Risk | Mitigation |
|---|---|
| "Passed pawn = win" diverges from chess in sums (+BIG and −BIG cancel) | `sum_safe` flag ✅; exact whole-board search; affine normal play in A0; tablebase bridge B4 |
| The \*2 candidate fails with real kings | Still a clean negative result; the cylinder-only atlas and ring theory remain new |
| Someone publishes first (Nicholson's `partizan` is active) | Check it in week 1; move fast on A2 and the B2 tables, which are the most original pieces |
| Python is too slow for the 8-file atlas | Symmetry, components, Rust, 14 cores |
| ML results are negative | Still publishable (extends Zhou & Riis); the benchmark itself is a contribution |
| Model errors | Already observed (Codex's referee); the protocol in §4 |

## 8. Decisions for you
1. **Order:** lead with the \*2 candidate and the cylinder tablebases (fastest route to a striking, verifiable result), or with the ChessSums benchmark?
2. **Conventions:** keep "passed pawn = immediate win" (the paper's convention, simple), or move to Mäser on/off or affine normal play (rigorous, slower)?
3. **Installs:** OK to install Stockfish, Lc0, Rust, PyTorch and MLX, and to `git init`?
4. **Mentor loop:** send Prof. Morley the audit and each paper draft?

## 9. Next steps once approved
1. A2: certify or refute the \*2 candidate with real kings.
2. B2: independently replicate the 4-man cylinder and torus tables (Codex, after its quota resets).
3. A1 proofs, and the Rust port for the A3 atlas.
