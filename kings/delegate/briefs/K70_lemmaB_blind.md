# K70: blind hand proof of a king-and-pawn lemma (two pawns against one, first promotion wins)

**Output directory:** `kings/delegate/out/K70/` (create it if it does not exist). Write only there. Do **not** edit any
existing file. Do not run git.

A lemma about a small pawn ending is needed for a theorem in a theory note. Two programs agree on it; no hand proof
exists. You are an independent check from outside the vendor that proposed it. Everything you need is in this file.
Prove the lemma by hand, or refute it with a concrete line of play.

**Read only:** this file; and `delegate/COMMON.md`, rules 5 and 7 only (ignore its "Read first" list). **Do not open**,
at any time during this task: `kings/theory/`, `kings/delegate/out/` other than `kings/delegate/out/K70/`,
`kings/delegate/briefs/` other than this file, `kings/REPORT.md`, `kings/CHECKLIST.md`, `notes/`, `RESULTS.md`,
`RESEARCH_PLAN.md`, `paper/`, `dist/`, `realchess/`, or the git history. They contain material on this lemma that
would make your check not blind.

## 1. The game P

Ordinary 8×8 chessboard, kings and pawns only, with the moves of chess: a king steps to an adjacent square not
attacked by the enemy; a pawn steps one square forward to an empty square, or two from its home rank (White rank 2,
Black rank 7) through an empty square, and captures one square diagonally forward, also en passant; a side may not
leave its own king attacked; a side in check must get out of it. White moves up the board, Black down.

The game P differs from chess only at the end: **the first promotion wins for the promoter and ends the play** (the
pawn reaches the last rank: rank 8 for White, rank 1 for Black; nothing is played after it). Checkmate loses for the
mated side. Stalemate is a draw. Infinite play is a draw. A position is a *Black win* if Black can force, in finitely
many moves, a Black promotion or a mate of White.

## 2. The lemma

Black: king b6, pawns b7 and c6. White: a king, and one pawn γ on c2, c3 or c4. **White to move.**

**Lemma B (full form).** For each of the three squares of γ and every square s of the White king that is empty and not
adjacent to b6 (54 squares each, 162 positions; the White king may stand in check on d5), the position is a Black
win in P, with one exception: γ on c4 and the White king on b4, which is a draw.

**Lemma B (the part that is needed).** The same for the White king on
S = {b2, c2, d2, e2, f2, b3, c3, d3, e3, f3, e4, f4, e5, f5, e6, f6} (minus γ's own square).

Remarks that are not proofs. White can promote only after a capture, since γ is on the c file below pc6. Two
programs report up to about 20 Black moves to the promotion with best defence. The exception shows that the lemma is
not trivial: with γ on c4 the squares b5 and d5 are taken from the Black king.

## 3. What to deliver

1. A hand proof of the needed part, and of the full form if you can: a plan for Black stated as rules ("zones" of the
   White king, key squares, the order of pawn moves), and for each White defence a reason why the plan still works.
   Case lists are fine when each case is closed by an argument in the text. Prove the exception too (why White
   holds with Kb4 and γ on c4, and why it is the only such square), or say that you did not.
2. You may write and run small programs (a retrograde solver for P on this material is a few dozen lines) to find
   the plan and to test every claim before you write it. The proof itself must be checkable without a computer. Do
   not close a branch with "the program confirms"; if a branch stays open, say exactly which positions are left.
3. If the lemma is false anywhere, give the position and White's line.

Label each statement PROVED (complete hand proof in the text), PARTIAL (say what is missing) or COMPUTED (only your
program says so).

## 4. Rules

- Toy computations only: nothing over 500 MB or over a few minutes.
- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
- No network, no downloads. No binaries left behind, no absolute home paths in text files.

## 5. Files

- `kings/delegate/out/K70/PROOF.md`: summary first (what is PROVED, PARTIAL, COMPUTED), then the proof.
- `kings/delegate/out/K70/REPORT.md`: five lines: verdict, the weakest step, what your program checked.
- `kings/delegate/out/K70/src/`: any program you used.
