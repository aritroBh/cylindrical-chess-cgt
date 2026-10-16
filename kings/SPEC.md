# Explicit king-and-pawn solver: rules and file formats

Two solvers must implement this spec: the C solver `kings/kpsolve.c` and an independent Python
reference solver `kings/ref/`. They are compared position by position, so every rule below is
binding. Neither may read the other's code.

## Board

- W files (2 to 8) by H ranks (4 to 8). Files are named a, b, c, ... and ranks 1, 2, ..., H.
- **flat:** an ordinary board.
- **cyl:** a cylinder. File a and the last file are glued. Ranks are not glued.

## Pieces and moves

- White uses upper case `K Q R B N P`; Black uses lower case `k q r b n p`.
- Queens, rooks, bishops and knights are called *officers*.
- Each side has exactly one king.

Standard chess moves, with these clarifications:

1. **Wraparound (cyl only).**
   - Every horizontal or diagonal step wraps from the last file to file a and back.
   - This applies to kings, knights, sliders and pawn captures. For example, on a cylinder of
     width 5, a white pawn on e2 captures on a3 and on d3.
2. **Sliders.**
   - A slider moves along a ray until it hits the board edge (top or bottom rank), the first
     occupied square, or its own starting square.
   - It may capture an enemy non-king piece on the first occupied square. It never moves through
     a piece.
   - When a ray wraps all the way round and returns to the starting square, the ray stops there.
     There is no null move.
   - On a cylinder the leftward and rightward rays along a rank can reach the same square. That
     is one move, not two.
3. **Pawns.**
   - White pawns move towards rank H; Black pawns move towards rank 1.
   - Single step to an empty square.
   - Double step from the pawn's second rank (rank 2 for White, rank H−1 for Black) if both
     squares are empty.
   - A pawn captures diagonally forward. It may capture enemy pawns and enemy officers, never the
     king.
   - A white pawn may never stand on rank 1 or rank H; a black pawn may never stand on rank H or
     rank 1.
4. **Promotion.**
   - A pawn reaching the last rank must promote to one piece of the allowed promotion set.
   - The default set is Q, R, B, N; option `--promote` can restrict it, for example to `Q`.
   - Each allowed piece is a separate move.
5. **En passant** (option `--ep on|off`, default on).
   - Right after a pawn double-steps, the opponent may capture it en passant on their very next
     move only.
   - The capture works exactly as in chess, diagonally across the seam on a cylinder.
   - A position therefore carries an e.p. target square or `-`.
   - With `--ep off` there is no en passant at all.
6. **Kings.**
   - A king moves one step in any direction, with wraparound on a cylinder.
   - It may capture an enemy pawn or officer.
7. **Legality.**
   - A move may not leave the mover's own king attacked.
   - Kings may never be adjacent; this follows from that rule.
   - A position is **illegal** if two pieces share a square, the kings are adjacent, a pawn stands
     on its first or last rank, or the side *not* to move is in check.
   - Illegal input positions are reported as `X`.
8. **Results.**
   - Checkmate (no legal move, and in check) is a loss for the side to move.
   - Stalemate (no legal move, not in check) is a draw.
   - There is no 50-move rule and no castling.
   - A game that can go on forever under best play is a draw. The value is the usual retrograde
     least fixed point:
     - won if some move reaches a lost position;
     - lost if every move reaches a won position;
     - everything else is drawn.

## The officer cap and bounds

Exactness can be expensive, so the solvers take `--cap C`, default 1. This is the maximum number of
officers (both colours together) a position may hold.

- A promotion that would create officer number C+1 is a **capped promotion**.
- The solver computes two bounds.
  - **Bound A:** every capped promotion counts as an immediate win for **White**, whoever promoted.
  - **Bound B:** every capped promotion counts as an immediate win for **Black**.
- Results are monotone in terminal values, so A ≥ true value ≥ B from White's point of view.
- When A and B agree, the value is **exact**.
- Input positions may hold at most C officers.

## Position format (one per line)

```
<piece tokens> <side to move> <e.p. target>
```

- Piece tokens are a piece letter and a square, separated by spaces, in any order, for example
  `Ke1 ke3 Pa2 Pb3 pc4 Qd5`.
- The side to move is `w` or `b`.
- The e.p. target is the square that was skipped by the double step (as in FEN), or `-`.
- A line starting with `#` is a comment.

Example (5x5 cylinder): `Kc1 kc5 Pa2 pe4 w -`

## Command line

```
<solver> --board cyl:7x6 --ep on --promote QRBN --cap 1 < positions.txt > results.txt
```

The same interface applies to `kings/kpsolve` and to `python3 -m kings.ref.solve`.

## Output format (one line per input line, same order; comments are copied)

```
<the input position exactly as given> | <A> <B>
```

- `<A>` and `<B>` are each `W` (White wins), `D` (draw), `L` (Black wins) or `X` (illegal).
- They are given from **White's** point of view, whoever is to move.
- Exact when A == B.
