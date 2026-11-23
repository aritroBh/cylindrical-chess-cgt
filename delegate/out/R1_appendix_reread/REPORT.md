SOUND WITH FIXES (all findings MINOR and about wording; no mathematical error found in A.1 to A.9 under the last-rank convention)

# Re-read of `dist/tog/supp_src/s12a_core.tex`, A.1 to A.9 (plus the A.2(c) citation in A.III)

Referee R1, 2026-11-23. Every step below was re-derived by hand; check 6 was also run as an independent brute force (own code, no repository solver imported).
Note: `dist/tog/supp/s12.tex` is a copy of this file (line numbers there are this file's +1). Any edit below must be made in both.

## Summary of findings

| # | Location | Severity | Kind |
|---|----------|----------|------|
| F1 | s12a_core.tex:30-31, 35 (A.1) | MINOR | "before the first promotion" does not literally cover pawn-game play after a promoting move, which A.6 uses |
| F2 | s12a_core.tex:63 (A.2(c) proof) | MINOR | "The last move was the opponent's" presumes a last move; the needed fact is about who created the right |
| F3 | s12a_core.tex:271-272 (A.11 proof) | MINOR | A.2(c) is cited for a claim that follows from A.2(a) and the definition of an event; the real role of (c) is unstated |
| F4 | s12a_core.tex:15, 18 | MINOR (optional) | H = 3 is degenerate (only the empty X is passer-free); the "no pawn on its own first rank" invariant is stated as a fact but not as an invariant |

No BLOCKER, no MAJOR.

## Check 1. Definitions on every H >= 3, flat and cylinder

Re-derived facts (all heights H >= 3, both board types):

- **No pawn on its own first rank, forever.** Pawns only move forward (step, double step, capture, e.p. all advance the mover by 1 or 2 ranks), so a white pawn never reaches rank 1 and a black pawn never reaches rank H. The stipulation at line 18 is therefore an invariant of all play once it holds at X. (F4 suggests saying so, because A.2(a) uses it at every position, not only at X.)
- **A pawn on its last rank cannot move or be captured.** A white pawn on rank H has no square ahead; a capture of it needs a black pawn on rank H+1. E.p. of it needs it to have just double stepped to rank H (possible only for H = 4) with a black pawn beside it on rank 4 = H, black's first rank: impossible. Symmetrically for black on rank 1.
- **A last-rank pawn is never "beside" a double-stepped enemy pawn.** A white double step lands on rank 4, a black one on rank H-3. A white last-rank pawn (rank H) is beside a rank-H-3 black pawn only if H = H-3: never. A black last-rank pawn (rank 1) is beside a rank-4 white pawn only if 4 = 1: never.
- **A last-rank pawn never affects another pawn's passed status.** "Ahead" of a black pawn is lower ranks; a white pawn on rank H is never lower than a black pawn (black pawns stand on ranks <= H-1). Same for black on rank 1. And in W and S it never coexists with play: its arrival ends W (A.2(a)) or freezes the component in S. In N(X) (play past passed pawns) it is an inert blocker on its own file only.
- **Components.** A last-rank pawn keeps its file occupied; it does not change component structure. A.1's first sentence holds for every pawn move in pawn-only play, including after promotions (see F1 on the wording of the second sentence).
- **Phi.** A promoted pawn contributes 0. A step lowers the mover's Phi by 1, a double step by 2, a capture or e.p. capture by 1 (the capturer advances one rank), and a capture lowers the opponent's Phi by the victim's distance (>= 0). So every pawn move of t lowers Phi_t by >= 1 and no move raises either Phi. Correct.
- **A.9 bound.** On ranks 2..H-1 a white pawn needs H-r steps: H-2, ..., 1, sum (H-1)(H-2)/2 per file; black symmetric. A pawn on rank H contributes 0 and X has none (it would be passed). N(X) <= max_t Phi_t(X) because each move of t lowers Phi_t >= 1 and Phi_t >= 0, also in sequences that continue past passed and promoted pawns. 8 * 7 * 6 / 2 = 168 < 256. Correct.
- **W(X), Reach(X), S(D), threats, HSS, (E).** All well formed for H >= 3. On H = 3 there are no double steps (rank 4 does not exist), every white pawn is on rank 2 with only rank 3 ahead, where no black pawn can stand, so every pawn is passed: the only passer-free X is the empty board, and W, S and the theorem are trivially consistent there (W: mover has no move, loses; S = 0). On H = 4 a double step reaches the last rank and promotes; e.p. is impossible (the capturer would stand on its own first rank), so every right is unusable and (E) holds automatically. No definition breaks.

Findings: F1, F4 (wording only).

## Check 2. A.2(a) on all tests, H = 3 and H = 4

- **Textbook / e.p. off.** No square lies ahead of a last-rank pawn, so it passes. Correct.
- **E.p.-aware (Definition def:epaware: passes textbook and "cannot be captured en passant on the opponent's next move").** A last-rank pawn could be e.p.-capturable only if it just double stepped onto the last rank, which needs H = 4, and then the capturer would stand beside it on rank 4 = its own first rank. The proof at lines 59-60 says exactly this. Correct, including H = 4.
- **H = 3.** Pawns move (a step from rank 2 to rank 3 promotes), but no double step exists. A white pawn on rank 2 next to a black pawn on rank 2 is degenerate but harmless: both pass the textbook test (nothing ahead of either), so such a position is a race and is never a passer-free X. A.2(a) holds trivially.
- **Is H >= 3 the right bound?** Yes. Nothing in A.1 to A.9 needs more; H = 3 is vacuous, H = 4 is non-trivial and correct (brute force below covers H = 3, 4, 5, 6). There is no counterexample to report. H = 2 would put every pawn on its last rank and is correctly excluded.

No finding beyond the optional F4.

## Check 3. Promotions inside W and S: A.4 to A.7

I looked for every step that silently assumed "no promotion occurs".

- **A.4.** (a) uses only (E) and the definition of S(D). (b): Y in Reach has no passed pawn; a pawn of D passing the textbook test in Y would fail only the e.p. clause, giving a usable right at a multi-component Y, against (E); D is unchanged by mu, so in Y' no pawn of D passes the textbook test. A freshly promoted pawn is the pawn moved by mu, hence in C', never in D. Correct; no promotion assumption.
- **A.5.** A promoting move by sigma-bar gives sigma-bar a passed pawn (A.2(a)), so the one-move sequence mu is a threat for sigma-bar: covered by the first case ("alone or in a race"). A promoting move by sigma-bar that also gives sigma a passed pawn (a race) is likewise excluded. Correct.
- **A.6.** Can Black promote? Every Black move is in a summand descended from a component without a threat for Black (A.5 induction); a promotion would make a Black passed pawn, i.e. a threat for Black. So Black never promotes and never creates a race after mu; every component Black freezes has only a White passed pawn and is +BIG. The question "if Black's move creates a race in which White wins" therefore cannot arise after mu. It can arise at mu itself, and there it is handled correctly by A.7: example on four ranks (flat), `W b2 / B a3`, Black to move: a3-a1 (double step, promotes); b2 is then passed too (a3 no longer ahead), a race; under the opponent rule White wins, W ends with winner White, S(C') = +BIG by the same local rule, and A.6 is applied with sigma = White. Consistent.
  Black never captures e.p. (White makes no pawn move after mu; a right of Y made by White lies in C, now frozen, or in some D != C and is unusable by (E)). Black's moves after mu are legal whole-board pawn moves on files of components other than C (separation by empty files, see F1 for the wording of A.1), so prefixing the play X -> Y and mu (which may be a promotion; N allows play past passed pawns, and a promoted pawn is inert) gives a sequence from X: at most N(X) Black moves. Frozen last-rank pawns contribute 0 to Phi and do not move, so the bound is unaffected. White needs k or k+1 <= N(X)+1 <= BIG moves. Correct.
- **A.7.** "The moves of S_Y are exactly the legal moves of W at Y": Y in Reach has no passed pawn, so no summand is frozen; every legal pawn move, promoting ones included, is a move in one component (A.1) and an option of that S(D); e.p. uses Y's right, which S_Y puts in the component of the double-stepper. Correct with promotions. Case "Y' ends W": if mu promotes, the passed pawn is the moved pawn, in C'; every other passed pawn of Y' is in C' by A.4(b) (pawns of D != C are not even textbook-passed). S(C') = sigma*BIG because the race rule is local and the mover is the same; a promoted pawn counts 0 moves under the count rule, consistently in W and S. HSS plus "mu alone is a threat of C for sigma" gives A.6's hypothesis. Correct.

No finding.

## Check 4. A.2(c), its two remarks, and its use in A.III

- **Proof of (c).** For H >= 5 a double step reaches rank 4 (white) or H-3 (black), not the last rank; a capture onto the last rank needs an enemy pawn on its own first rank; an e.p. capture lands on rank 3 or H-2. So a promoting move is a step from rank H-1. That pawn has only the last rank ahead, which holds no enemy pawn, so it passes the textbook test. The e.p. clause concerns only the pawn whose double step created the right, which by hypothesis belongs to the side not to move. So the pawn is passed, contradicting "no passed pawn". Correct (F2 is a wording point for the case without a right).
- **Remark, four ranks, `W a2 / B b3`.** a2 has b3 ahead on a neighbouring file; b3 has a2 ahead on a neighbouring file. No pawn is passed under any test. a2-a4 (a3, a4 empty) reaches rank 4 = H and promotes. Verified. (After it b3 is passed too, so this is a race; the remark does not need that.)
- **Remark, five ranks, `W a2 b2 / B b4`, after a2-a4.** a4: textbook-passed (a5, b5 empty) but b4 stands beside it, so it fails the e.p.-aware test; b2 has b4 ahead on its file; b4 has b2 ahead on its file. No pawn passed. a4-a5 promotes; White can play it only on a second consecutive move, i.e. in a sum where the component keeps White's right. The position satisfies the hypothesis of (c) for Black to move (right made by White) and Black has no promoting move, as (c) says. With the textbook test or e.p. off the position after a2-a4 already has a passed pawn, so the remark correctly names the e.p.-aware test. Verified.
- **Use in A.III (lines 215, 271-272).** The only citation of A.2(c) is at line 272. At every Y in R(Q) the context X_Y has no passed pawn (non-decisive context moves keep it so) and, in chess, any right was created by the previous move, i.e. by the side not to move; Z-pawn rights concern Z-pawns, not X_Y. So (c) applies to X_Y and the side to move has no promoting context move at any Y in R(Q). The sentence "In this part H >= 5, so that Lemma A.2(c) applies" is enough.
  However, the claim at lines 271-272 ("no promotion occurs before the event") follows already from A.2(a) and the definition of a decisive event (a Z-pawn promotion is a Z-move; a context promotion makes a passed pawn and is itself an event). What (c) really gives is that no decisive *context* move is a promotion, so the move sets compared in (V1), and the moves of (V2), are pawn moves that leave pawns (a chess promotion yields a piece and four distinct moves, W yields a pawn). Without H >= 5, A.11 would remain true but (V1) would fail at every Y with a promoting context move. See F3.

## Check 5. Internal consistency after the edits

- No occurrence of "H >= 6", "H \ge 6", "no promotion occurs" (other than line 271, A.III, correct in context), or "unpromoted" in the file or anywhere under `dist/tog` (`.tex`).
- "ranks 2 to H-1" occurs only at line 206 (A.9), where it is correct (X has no last-rank pawn).
- Every citation of A.2 parts matches the new lemma: A.2(a) at lines 70, 82, 96 (promoting move makes a passed pawn / ends W / freezes), A.2(b) at lines 81, 96, 104, 270, A.2(c) at lines 215, 272. No citation of the old "(a) no promoting move".
- Line 26-27 (convention), line 119 (A.3: "a pawn on its last rank stays a pawn and so counts as passed"), lines 69-70 and 96-97 agree with one another.
- The convention is stated for "the pawn games W and S" (line 26); N(X) and threat sequences are also pawn-only play and implicitly use the same convention (a promoted pawn stays and is inert). Nothing contradicts this, but A.1's wording does not quite cover it: F1.
- Line 98 example re-checked: `W b2 d6 / B c7`, eight ranks, no passed pawn; after c7xd6 both b2 and d6 are passed, each needs 5 moves (b2-b4 counts as one), tie to the side that did not move, White. Correct.

## Check 6. Independent brute force

Own Python script (session scratch only, not committed), no repository code imported. Rules implemented from `dist/tog/sections/02_rules.tex` and A.I/A.II: e.p.-aware test (textbook plus "the pawn that made the current right has no enemy pawn beside it"), count rule (fewer moves to promote on an empty board, double step as one move, tie to the side that did not move), mover and opponent rules, textbook and e.p.-off tests. W: exact minimax with immediate end on any passed pawn. S: exact play of the sum (components with their own rights, BIG = 256 as an integer summand), moved component tested **before** splitting, last-rank pawn stays and is passed. Reach, threats (either side, any order, stop at first passed pawn, race = both), HSS and (E) as defined at lines 83 and 107-112. Roots: all placements with at most the stated number of pawns per side on ranks 2..H-1, no passed pawn, with no right or any consistent right (then only the historically compatible side to move); otherwise both starters.

Results (cases = root x starter):

| Boards | Pawns | Settings | Cases | Satisfy HSS+(E) | Disagree under hypotheses | Fail HSS / (E) | Disagree outside hypotheses |
|---|---|---|---|---|---|---|---|
| flat 2,3 files x 3,4,5 ranks; cylinder 3 files x 3,4,5 | <= 2+2 | all 9 | 81 runs | all | 0 | 0 / 0 | 0 |
| flat 4x4, 4x5, 4x6 | <= 2+2 | all 9 | 106 / 806-926 / 3878-4038 per setting | all | 0 | 0 / 0 | 0 |
| flat 5x4 | <= 2+2 | all 9 | 176 per setting | 168 | 0 | 8 / 0 | 8 |
| flat 5x5 | <= 2+2 | all 9 | 1392-1572 per setting | 1320-1500 | 0 | 72 / 0 | 32-40 |
| flat 3x5, 3x6, 4x5; cylinder 4x5 | <= 3+3 | e.p.-aware, count | 1460 / 12528 / 5982 / 8714 | 1460 / 12528 / 5710 / 8714 | 0 | 0 / 272 (flat 4x5) | 0 |

Sensitivity controls: (i) the H = 3 runs contain only the empty root, as derived in check 2; (ii) the split-first mutant of S (re-split, then freeze each piece) disagrees with W on 98 (flat 5x5), 204 (flat 5x6) and 320 (flat 4x5, 3+3) hypothesis-satisfying cases, so the checker detects the order-of-operations error the appendix warns about; (iii) every disagreement of the correct S with W occurs on roots that fail HSS, so the hypothesis is doing real work. Conclusion: no counterexample to Theorem A.7 on these boards, under all nine settings, with promotions inside W and S.

## Findings with replacement LaTeX

### F1. s12a_core.tex:30-31 and :35, MINOR

The second sentence of A.1 is restricted to "before the first promotion". Under the last-rank convention, play in W, S, N(X) and threat sequences contains promotions but never a non-pawn piece, and A.6 needs component separation after a promoting move mu (Black's later moves are whole-board legal moves on other files). The first sentence of A.1 covers this, so nothing is false, but line 40 cites A.1 for "play with pawns only" while A.1's conclusion is literally scoped to before a promotion. No counterexample.

Replace lines 30-31 by:
```latex
\textbf{A.1 Lemma (files).} \emph{A pawn changes file only by a capture, and it then lands on a file that held an enemy
pawn just before the move. Hence, in play in which kings are the only pieces other than pawns (all play in $W$, $S$, the
move bound and the threats below, where a promoted pawn stays a pawn, and chess before the first promotion), no pawn ever
enters a file that holds no pawn.}
```
and line 35 by:
```latex
on the file of the captured pawn $q$. Kings are never captured, so in such play the only capturable pieces are pawns.
```

### F2. s12a_core.tex:63, MINOR

"The last move was the opponent's" presumes a last move (a root position need not have one) and is not quite the needed fact. Replace lines 63-64 (from "The last move" to the end of the proof) by:
```latex
it, and it holds no enemy pawn, so the pawn passes the textbook test. The e.p.\ clause concerns only the pawn whose double
step created the right, and by hypothesis that pawn belongs to the side not to move, so the pawn is passed.
```

### F3. s12a_core.tex:271-272, MINOR

The cited lemma part does not match the claim. Replace "The play is never stalemate (V1), and no promotion occurs before the event (Lemma~A.2(c))." by:
```latex
The play is never stalemate (V1). No promotion occurs before the event: a Z-pawn promotion is a Z-move, and a context
promotion makes a passed pawn (Lemma~A.2(a)) and so is itself an event. Moreover at each $Y\in\mathrm{R}(Q)$ the context
$X_Y$ has no passed pawn and its right, if any, was made by the side not to move, so by Lemma~A.2(c) no context move at $Y$
promotes; the moves compared in (V1) and (V2) are pawn moves that leave pawns.
```
Line 215 can stay as it is.

### F4. s12a_core.tex:15 and :18, MINOR (optional)

Nothing is wrong. Two clarifications a hostile reader will ask for. Replace "No pawn stands on its own first rank." (line 18) by:
```latex
No pawn stands on its own first rank; since pawns only move forward, this holds in all play.
```
and optionally append to line 15, after "$H\ge 3$ ranks.":
```latex
(On three ranks every pawn is passed, so the results below are about the empty position only; on four ranks a double step
promotes and no e.p.\ capture is possible.)
```

## What I did not check

- A.8, A.10, A.12 and A.14 to A.17 were read only for consistency with the convention and for stale references, not re-proved. A.11 was checked only at the A.2(c) citation and the promotion sentence. The A.13 example (`W Kb6 c7 / B Ka8 a5`) was checked by hand quickly and holds; A.14 was not re-verified.
- Main-text labels (`\ref{...}`) and LaTeX compilation were not checked. The sync of `dist/tog/supp/s12.tex` was checked only for the A.2 citations (identical).
- Brute force: no boards wider than 5 files or taller than 6 ranks; at most 2+2 pawns on most boards, 3+3 only on four boards with the default setting; cylinders only with 3 and 4 files. The race rule's count is my reading of 02_rules.tex (empty-board distance, double step as one move, tie to the non-mover); the engine's own count was not compared.
