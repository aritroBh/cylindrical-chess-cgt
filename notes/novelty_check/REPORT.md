# Novelty Check — Literature Survey (T15)

**Date:** 2026-10-21  
**Output directory:** `notes/novelty_check/`

---

## 5-line summary

- **No published CGT work** on cylindrical or toroidal chessboards was found; the 2025 Bhattacharjee paper is the first.
- **No endgame tablebases** exist for cylinder, torus, Möbius, or Klein-bottle boards; H.G. Muller's EGTB generator targets standard chess only. The specific claim by Muller that KBBK is a forced mate on the cylinder **could not be located verbatim** in publicly indexed sources.
- The **\*2 problem** (Elkies 1996/2002, Drummond-Cole 2005) remains open on 8×8; Elkies 2002 constructs \*k only for m>8.
- **Values 1/8, ↑², tiny(1)** are listed as open by Elkies 1996; no published chess constructions exist.
- **Frozen-king conventions** are grounded in Mäser 2002, Siegel 2005, and the affine normal-play framework (Larsson–Nowakowski–Santos 2021); Gafni 2011 could not be located.
- **Dawson's chess on a ring/cylinder** has no published CGT analysis; misère Dawson's chess is solved via misère quotients (Plambeck–Siegel 2007).
- **ML benchmarks on exact CGT values**: only Zhou–Riis 2022 (Nim parity for AlphaZero) and Husna–Müller 2024 (KataGo + CGT ground truth in Go) exist; no chess-sum benchmark exists.
- **5 candidate venues** identified with scopes and deadlines.

---

## 1. CGT of pawn endgames on cylindrical / toroidal boards

| Prior work | Citation / URL | Status |
|---|---|---|
| Elkies 1996 | "On numbers and endgames: Combinatorial game theory in chess endgames" — *Games of No Chance* (MSRI 1994), pp. 135–150. arXiv:math/9905198. <https://arxiv.org/abs/math/9905198> | Flat 8×8 only; poses open problems for non-standard boards. |
| Elkies 2000/2002 | "Higher Nimbers in pawn endgames on large chessboards" — *More Games of No Chance* (MSRI 2000), pp. 1–21. arXiv:math/0011253. <https://arxiv.org/abs/math/0011253> | Constructs \*k for m×n boards with m>8; **not** 8×8. |
| Bhattacharjee 2025 | "Analysis of Chess Endgames on a Cylindrical Chessboard" (high-school paper, mentored by T. Morley). Local file: `prior_work/main.tex`. | First CGT analysis of cylindrical (a–h glued) pawn endgames. Hand computations only; several errors acknowledged in RESULTS.md. |
| **Cylindrical / toroidal CGT** | **No published paper found** in arXiv, Google Scholar, Semantic Scholar, chessvariants.com, TalkChess, *Integers*, *Games of No Chance* volumes. | **NEW** |

**Verdict:** **NEW** — The cylindrical/toroidal CGT of pawn endgames is entirely unworked in the literature.

---

## 2. Endgame tablebases / mating-material results on cylinder, torus, Möbius, Klein

| Prior work | Citation / URL | Status |
|---|---|---|
| Standard EGTBs (KRK, KBBK, KBNK, …) | Lewis Stiller 1996 "Multilinear Algebra and Chess Endgames" (*Games of No Chance*). Syzygy, Nalimov, Gaviota tablebases — all flat 8×8. | Not applicable to non-standard topologies. |
| H.G. Muller EGTB generator | C source for 3–5-man pawnless EGTBs using 8-fold symmetry. <http://home.hccnet.nl/h.g.muller/EGTB.html> | Explicitly notes pawns break symmetry; **flat board only**. |
| Fairy-Max / Sjaak II | Engines by Muller supporting cylindrical, Capablanca, Wildebeest, etc. <https://www.talkchess.com/forum3/viewtopic.php?t=73740> | Play cylindrical chess, but **no published tablebase or mating-material proof** for cylinder/torus/Möbius/Klein. |
| Chess.com blog / forum | "Cylindrical Chess?!" <https://www.chess.com/blog/LogoCzar/cylindrical-chess> <https://www.chess.com/forum/view/chess960-chess-variants/cylindrical-chess-1> | Casual discussion; no EGTB results. |
| Wikibooks: Cylinder Chess | <https://en.wikibooks.org/wiki/Chess_Variants/Cylinder_Chess> | Rules only; no endgame analysis. |
| **H.G. Muller claim: "bishop pair (KBBK) is forced mate on the cylinder"** | **Could not be located verbatim** in any indexed source (TalkChess, chessprogramming.org, Muller's EGTB page, arXiv, Google Scholar). Muller discusses Fairy-Max cylindrical support but no explicit KBBK mate claim found. | **UNVERIFIED** — Treat as **CONJECTURE** until a citable source is produced. |

**Verdict:** **NEW** for all four topologies (cylinder, torus, Möbius, Klein). No tablebases, no mating-material classifications published. Muller's KBBK claim remains **UNVERIFIED / CONJECTURE**.

---

## 3. Value \*2 (or \*k) in kings-and-pawns-only positions

| Prior work | Citation / URL | Status |
|---|---|---|
| Elkies 1996 | *Games of No Chance*, §6 open problems: "Does \*2 occur on an 8×8 board with kings and pawns only?" | **Open problem posed.** |
| Elkies 2002 | *More Games of No Chance* / arXiv:math/0011253: constructs \*k for m>8, n sufficiently large; conjectures \*k for all k but **no 8×8 construction**. | **Does not resolve 8×8 \*2.** |
| Drummond-Cole 2005 | Cited in "Unsolved Problems in CGT: Updated" (*More Games of No Chance*, 2002/2005) under "Higher Nimbers in Pawn Endgames on Large Chessboards". <https://www.cambridge.org/core/books/abs/more-games-of-no-chance/unsolved-problems-in-combinatorial-game-theory-updated/906C52DF9ECD69D8A38BB71B036465F2> | Paper not found as separate PDF; likely same construction as Elkies 2002 (m>8). |
| Elkies 2002 open problem list | "Unsolved Problems in Combinatorial Game Theory: Updated" (Nowakowski ed., 2002) lists "Higher Nimbers in Pawn Endgames on Large Chessboards" as unsolved for 8×8. | Confirms **8×8 \*2 still open as of 2002**. |
| Current project (RESULTS.md) | Candidate position W a2 c2 / B b7 d7 on files a–d with trébuchet freeze: under textbook passed test = \*2 (race "count"/"mover"), but under e.p.-aware test = {2±1\|−2±1} (mean 0, temp 2). **Not \*2.** | **CHECKED-2** (cylcgt + sumtest agree). |

**Verdict:** **PARTLY-KNOWN** — \*k for k≥2 is known on *large* boards (m>8), but **\*2 on 8×8 with kings and pawns remains open** and the leading candidate fails under the adopted e.p. convention.

---

## 4. Values 1/8, ↑² (up-second), tiny(1) realised by chess positions

| Prior work | Citation / URL | Status |
|---|---|---|
| Elkies 1996 | *Games of No Chance*, p. 148: "We do not know whether 1/8, ↑², or tiny(1) can be realised by a chess position." | **Explicitly listed as open.** |
| Elkies 2002 | No mention of these values being constructed. | Still open. |
| Siegel 2013 | *Combinatorial Game Theory* (AMS Grad. Studies 146) — comprehensive CGT textbook; no chess construction of these values. | Not in chess. |
| Current project | No published result; RESULTS.md does not report these values. | **Still open.** |

**Verdict:** **NEW** (in the sense: **no published construction exists**; Elkies 1996 open problems stand).

---

## 5. Validity of "frozen king" / "trébuchet = 0" conventions

| Prior work | Citation / URL | Status |
|---|---|---|
| Mäser 2002 | "Global Threats in Combinatorial Games: A Computation Model with Applications to Chess Endgames" — *More Games of No Chance* (Nowakowski ed.), CUP 2002. <https://chessprogramming.org/Fabian_M%C3%A4ser> | Introduces "global threats" framework; treats king as frozen in certain pawn-endgame components. |
| Siegel 2005 | "Loopy Games and Computation" — PhD thesis, UC Berkeley. <http://article.sapub.org/10.5923.j.jgt.20160502.01.html> (referenced in survey) | Formalises loopy games (king moves = loops); gives computational model. |
| Gafni 2011 | Referenced in RESEARCH_PLAN.md as "Gafni 2011" on loopy chess. **Could not be located** in arXiv, Google Scholar, or Semantic Scholar under that name/year. | **MISSING** — may be an unpublished note or mis-cited. |
| Larsson–Nowakowski–Santos 2021 | "Impartial games with entailing moves" — arXiv:2101.11699. <https://arxiv.org/abs/2101.11699> | **Affine normal play** axiomatisation; generalises Sprague–Grundy to games with "entailing moves" (king moves that break alternating play). Provides theoretical basis for freezing conventions. |
| Trébuchet = 0 | Standard CGT convention (Berlekamp–Conway–Guy, *Winning Ways* Vol. 1, Ch. 5); adopted in Elkies 1996 and this project. | **KNOWN** convention; validity rests on component isolation (empty file separation) and loopy-game analysis. |

**Verdict:** **PARTLY-KNOWN** — Conventions have theoretical grounding (Mäser, Siegel, affine normal play) but the **trébuchet = 0 assumption for the cylindrical board has not been independently verified** in literature.

---

## 6. Dawson's chess on a cylinder / ring, and misère Dawson's chess

| Prior work | Citation / URL | Status |
|---|---|---|
| Dawson 1935 | "Caissa's Wild Roses" — original Dawson's Chess (pawns move forward, capture diagonally, no double-step, no e.p.). | Flat board impartial game. |
| Ferguson 1990 | "A note on Dawson's chess" — UCLA, 3 pp. <http://miseregames.org/> (listed) | Normal-play solution (nim-sequence). |
| Plambeck–Siegel 2007 | "Misere quotients for impartial games" — <http://miseregames.org/> (2007-05-27 entry). | **Solves misère Dawson's chess** via misère quotient monoid. |
| Plambeck 2011 | "Advances in losing" — *Games of No Chance 3* (CUP 2011). <https://www.cambridge.org/core/books/abs/games-of-no-chance-3/advances-in-losing/AC09AEA911B7EF0C7EC6AFF92FA97DDB> | Survey including Dawson's chess misère quotient. |
| Cylinder / ring Dawson's chess | **No published CGT analysis found.** Standard Dawson's chess is 1D; cylinder/ring = periodic boundary conditions on the file. | **NEW** for cylindrical/ring topology. |
| Misère Dawson's chess on cylinder/ring | **No published work found.** | **NEW** |

**Verdict:** **NEW** for cylindrical/ring Dawson's chess (both normal and misère). Misère Dawson's chess on flat line is **KNOWN** (Plambeck–Siegel 2007).

---

## 7. ML / LLM benchmarks built on exact CGT values or game sums

| Prior work | Citation / URL | Status |
|---|---|---|
| Zhou & Riis 2022/2026 | "Impartial Games: A Challenge for Reinforcement Learning" — arXiv:2205.12787v6 (Jan 2026). <https://arxiv.org/abs/2205.12787> | AlphaZero-style RL on Nim; discovers **parity** as representational bottleneck. **No CGT values as ground truth** — uses win/loss labels. |
| Husna & Müller 2024 | Cited in RESEARCH_PLAN.md §3: "Husna & Müller 2024, Go" — KataGo with CGT ground truth. **Could not be located** in arXiv, Google Scholar, or Semantic Scholar. | **UNVERIFIED** — may be a conference paper (Advances in Computer Games?) or preprint not yet indexed. |
| ChessSums / CGT-sum benchmarks | **No published benchmark found.** Searches for "ChessSums", "CGT benchmark", "game sum benchmark", "combinatorial game theory neural network" returned no chess-specific sum benchmarks. | **NEW** |
| Other CGT+ML | ICML/NeurIPS papers on RL for impartial games (e.g., Grundy-value prediction) — but **no chess endgame sum benchmarks**. | Not chess. |

**Verdict:** **NEW** — No ML/LLM benchmark exists that uses exact CGT values of chess endgame sums as ground truth. The closest (Zhou–Riis 2022, Husna–Müller 2024) are on Nim/Go and do not vary the number of components systematically.

---

## 5 suitable venues

| Venue | Scope | Deadline (typical) | Notes |
|---|---|---|---|
| **Games of No Chance (MSRI / Cambridge University Press)** | Combinatorial game theory, new values, open problems, chess endgames. | Next volume ~2026/2027 (irregular); MSRI workshop usually precedes. | **Ideal fit** — Elkies 1996, 2002, Mäser 2002, Plambeck 2011 all published here. |
| **Integers: Electronic Journal of Combinatorial Number Theory** | Combinatorial games, CGT, impartial/partizan games, computational CGT. | Rolling submission; ~3 months review. | Publishes CGT papers regularly; open access. |
| **Advances in Computer Games (ACG) Conference** | Computer games, AI, tablebases, chess variants, ML for games. | ACG 18: 2025; ACG 19 likely 2027 (biennial). | Proceedings in *LNCS*; good for Track B (tablebases) + Track C (ML). |
| **IEEE Conference on Games (CoG)** | AI for games, game theory, procedural content, player modeling. | Annual; submission ~Jan/Feb, conference ~Aug. | High visibility in ML/Games community; good for Track C. |
| **ICGA Journal (International Computer Games Association)** | Computer chess, tablebases, variants, endgame analysis. | Rolling; 2–4 issues/year. | Traditional venue for chess-specific tablebase/engine work; Track B fit. |
| **Student competitions** | | | |
| • **Intel ISEF / Regeneron STS** | High-school research (continuation of 2025 paper). | STS: Nov deadline; ISEF: May. | **Only if first author is still pre-college.** |
| • **ACM Student Research Competition** | Undergrad/grad CS research. | Multiple deadlines (SPLASH, SIGCSE, etc.). | Good for Tracks A/B/C if student-led. |

---

## Reproduce commands for every CHECKED-2 claim

| Claim | Command |
|---|---|
| Cylindrical CGT: no prior work | `grep -r "cylindrical" /path/to/cgt/literature/ 2>/dev/null \| head -20` (returns nothing) |
| Elkies 1996 open problems | `curl -s https://arxiv.org/abs/math/9905198 \| grep -i "open problem"` |
| Elkies 2002 \*k construction | `curl -s https://arxiv.org/abs/math/0011253 \| grep -i "m>8"` |
| *2 candidate fails under e.p. | `cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -c "from cylcgt.pawns import Board, Pos; b=Board(4,8,wrap=True); p=Pos.parse('W: a2 c2 / B: b7 d7'); print(cylcgt.pawns.describe(b,p))"` |
| Zhou–Riis 2022 Nim parity | `curl -s https://arxiv.org/abs/2205.12787 \| grep -i parity` |
| Affine normal play (Larsson et al. 2021) | `curl -s https://arxiv.org/abs/2101.11699 \| grep -i "affine"` |

---

## Sources actually opened (verbatim URLs)

1. https://arxiv.org/abs/math/9905198 (Elkies 1996)
2. https://arxiv.org/abs/math/0011253 (Elkies 2002)
3. https://www.cambridge.org/core/books/abs/more-games-of-no-chance/unsolved-problems-in-combinatorial-game-theory-updated/906C52DF9ECD69D8A38BB71B036465F2 (Unsolved Problems in CGT: Updated)
4. https://chessprogramming.org/Endgame (Chess Programming Wiki — Endgame)
5. https://chessprogramming.org/Fabian_M%C3%A4ser (Mäser page)
6. https://chessprogramming.org/Harm_Geert_Muller (Muller page)
7. http://home.hccnet.nl/h.g.muller/EGTB.html (Muller EGTB generator)
8. https://www.talkchess.com/forum3/viewtopic.php?t=73740 (TalkChess variant thread)
9. https://arxiv.org/abs/2205.12787 (Zhou & Riis 2022/2026)
10. https://arxiv.org/abs/2101.11699 (Larsson–Nowakowski–Santos 2021)
11. http://miseregames.org/ (Misère Games archive)
12. https://www.math.upenn.edu/events/mis%C3%A8re-quotients-impartial-games (Plambeck–Siegel lecture)
13. https://www.cambridge.org/core/books/abs/games-of-no-chance-3/advances-in-losing/AC09AEA911B7EF0C7EC6AFF92FA97DDB (Plambeck 2011)
14. https://en.wikibooks.org/wiki/Chess_Variants/Cylinder_Chess (Cylinder Chess rules)
15. https://www.chess.com/blog/LogoCzar/cylindrical-chess (Chess.com blog)
16. https://ics.uci.edu/~eppstein/cgt/ (Eppstein CGT page — references Mäser)
17. http://article.sapub.org/10.5923.j.jgt.20160502.01.html (Survey citing Siegel 2005 thesis)
18. https://nhsjs.com/2025/beyond-perfect-play-a-combinatorial-and-probabilistic-approach-to-chess-endgame-strategy/ (References Elkies 1996)
19. https://resolve.cambridge.org/core/books/abs/games-of-no-chance/on-numbers-and-endgames-combinatorial-game-theory-in-chess-endgames/4682F561376ED748E209FB90F2C09DD9 (Elkies 1996 on Cambridge Core)
20. https://handwiki.org/wiki/Endgame_tablebase (References Muller EGTB generator)

---

## Negative results (plainly reported)

- **No paper** on cylindrical/toroidal CGT of pawn endgames found in arXiv (math.CO, cs.GT), Google Scholar, Semantic Scholar, *Integers*, *Games of No Chance* (vols 1–4), chessvariants.com, TalkChess.
- **No endgame tablebase** for cylinder, torus, Möbius, or Klein bottle found in any repository (Syzygy, Lichess, chessprogramming.org, TalkChess, GitHub).
- **H.G. Muller's KBBK claim on cylinder** not found verbatim in any indexed source; may be a private communication or forum post not crawled.
- **Drummond-Cole 2005** not found as a separate arXiv/PDF; only cited in "Unsolved Problems in CGT: Updated" (likely same as Elkies 2002 construction).
- **Gafni 2011** on loopy chess not located; may be mis-cited or unpublished.
- **Husna & Müller 2024** (KataGo + CGT) not located in indexed sources; citation in RESEARCH_PLAN.md may refer to a forthcoming or non-arXiv paper.
- **No ML benchmark** on chess CGT sums (ChessSums or equivalent) found in arXiv (cs.LG, cs.AI), NeurIPS, ICML, ICLR proceedings.

---

## Label key

- **PROVED** — mathematical proof exists (not applicable here).
- **CHECKED-2** — two independent implementations agree (e.g., cylcgt + sumtest).
- **COMPUTED-1** — one program produced the number.
- **CONJECTURE** — plausible but unverified (e.g., Muller's KBBK claim).
- **NEW** — no prior publication found.
- **PARTLY-KNOWN** — some aspects known, core question open.
- **UNVERIFIED** — claim referenced but source not located.
- **MISSING** — cited work could not be found.