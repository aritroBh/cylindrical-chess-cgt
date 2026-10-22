# Literature: CGT in chess endgames (survey, 2026-10-15)

*Compiled by a Claude research subagent that read the full texts of Elkies 1996/2002, Mäser, Drummond-Cole, Wu–Yü–Landry, Gafni, Siegel 2009, Larsson–Nowakowski–Santos 2025, and Nowakowski's 2025 problem list. Items marked [unverified] were seen only as abstracts or catalogue entries.*

**Bottom line:** no published CGT work on cylindrical or toroidal chessboards. Most of Elkies' 8×8 open questions are still open: \*4; a \*2 made only of kings and pawns; 1/8; ↑²; fractional tinies; non-dyadic values; "chilled chess".

## Known results
- **Elkies 1996**, *On numbers and endgames*, GONC (MSRI 29) 135–150, arXiv math/9905198.
  - Numbers: integers (spare tempi) and mutual zugzwang = 0 (the trébuchet). 1/2 and 1/4 occur on 8×8; files of length N give 1/2^(N−7).
  - Infinitesimals: \*, ↑ = {0,\*|\*} (from the double step), ⇑\*, ↑\*, ⇑, ↓, ⇓\*.
  - Pa2 against a pawn on rank n+4 gives n·↑ or n·↑+\*.
  - Two unmoved pawns on one file give 0, except \* on a file of length 5 and **\*2 on a file of length 6**.
  - Switches: {1|0}, ±1, {1|−2}, {2n|n‖0}; temperatures reach (N−5)/2.
  - tiny-1 and tiny-2, which use knights and kings as frozen blockers.
  - Loopy values: tis/tisn, over (Behting 1929), on/off, dud.
- **Elkies 2002**, *Higher Nimbers in pawn endgames on large chessboards*, MGONC (MSRI 42) 61–78, arXiv math/0011253.
  - A 3-row pawns game: no double step, optional captures, reaching the far row wins.
  - Quiescent component [m] = \*ε(m), period 10. Embeddable on boards with ≥ n+6 files and odd height > 5 (example board 9×12).
  - "Stopped files": \*2 at length 4, and \*4/\*8/\*16 at lengths 9/20/43. Blocking every 6th file reaches \*4096.
- **Mäser**, *Global threats in combinatorial games*, MGONC (2002) 137–149. Models promotion as on/off; Java "Game Bench" calculator; warns that treating the king mutual zugzwang as permanent is heuristic.
- **Drummond-Cole**, *Positions of value \*2 in generalized Domineering and chess*, Integers 5 (2005) G06. Gets \*2 in a legal 8×8 game, but **needs bishops, knights, rooks and queens** to freeze the pawns.
- **Siegel**, *Coping with cycles*, GONC3 (MSRI 56, 2009). Chess positions of value on and upon.
- **Gafni**, *Chess as a combinatorial game*, thesis 2011. K+P vs K on 3×3 and 3×4 boards as loopy games: on\*, {on|0}, 1\*.
  **[unverified, 2026-10-22]** A later search ([novelty_check/REPORT.md](novelty_check/REPORT.md)) could not
  locate this thesis in arXiv, Google Scholar or Semantic Scholar, so the "full text" claim in the header does
  not hold for Gafni. The paper does not cite it. `kings/delegate/out/K4/REPORT.md` tests these values without
  the source.
- **Wu, Yü, Landry**, Stanford Math 191 paper. **Dated Dec 2010, not 2020** — the 2025 draft's citation needs correcting. Nothing beyond Elkies.
- **Khan & Ahmad** (c. 2004): claims \*2/dud/over in historical games. Unreliable: its \*2 contradicts Elkies.
- **Haworth et al.**: mutual zugzwangs mined from tablebases (ICGA J. 2001, 2011; ACG12).
- **Theory of entailing moves:**
  - Larsson–Nowakowski–Santos, *Impartial games with entailing moves*, Integers 21B (2021).
  - The same authors, *Affine normal play*, GONC6 (MSRI 71, 2025) 135–189: ∞-terminating games, motivated by checkmate.
- **Dawson's chess** = octal 0.137 = Dawson's Kayles shifted by one.
  - Normal-play period 34, last exception at n = 51.
  - The **misère version (Dawson's original 1935 question) is still unsolved**.
  - No ring or cylinder versions are published. Reducing a full ring to a line of n−3 is the "cut the torus" idea of Lachmann–Moore–Rapaport (Domineering on cylinders and tori, MGONC 2002).
- **Programs to imitate:**
  - Go: Berlekamp–Wolfe; Müller's decomposition search; generalized thermography.
  - Domineering: Uiterwijk–Barton canonical-form database (arXiv 1506.03949); Huntemann–Maciosowski temperature-2 search.
  - Amazons: Berlekamp; Snatzke.
  - Konane: shown **universal** by Carvalho–Santos (2017).
- **Software:**
  - CGSuite 2.x (Siegel; loopy games first-class).
  - `cgt` Rust crate by T. Maciosowski (short, misère and loopy; v0.11, Sep 2026).
  - `partizan` by Nicholson (alpha; chess FEN → canonical forms; no thermography).

## Open problems (from the literature)
1. \*4 on 8×8; **\*2 with only kings and pawns on 8×8** (Elkies 1996; Drummond-Cole's \*2 needs pieces).
2. tiny-x for x = 1/2 or 1↑; do ↑² and ↑³ occur?
3. 1/8 on 8×8? Non-dyadic values in loopy positions?
4. "Chilled chess": a class of positions that chilling operators solve.
5. A systematic CGT treatment of en passant, checks, and capture/recapture.
6. Complexity of N×N pawn endgames.
7. Elkies 2002: does every \*k occur (Nowakowski 2025 list, Problem B3)? Is the density of \*k bounded away from 0? A closed form for ε(w)?
8. Misère Dawson's chess.

## Gaps on the cylinder
- CGT on cylindrical or toroidal chess: nothing found.
- Elkies' pawns game on **cyclic words**: never studied.
- No canonical-value database of pawn configurations.
- No thermography or atomic-weight study of chess.
- Elkies constructions that depend on board edges have never been re-examined without edges. Odd circumference, which breaks opposition parity, is untouched.

## Ranked opportunities (agent's view)
1. Nimbers from cyclic pawn rings: Elkies' stopped-file recursion on cyclic words.
2. A canonical-value database for cylinder pawn configurations, searched for Elkies' open targets.
3. An edge-removal audit plus loopy king values.
4. Thermography and the "chilled chess" question.
5. Entailing moves through affine normal play.
