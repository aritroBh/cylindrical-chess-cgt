#!/usr/bin/env python3
"""Small, independent array-board check of C solver's current hit snapshot."""
from functools import lru_cache
from pathlib import Path
import sys

ROWS = 6
EMPTY, WHITE, BLACK = 0, 1, 2
NO_EP = -1


def parse(text):
    board = [EMPTY] * 42
    side = WHITE
    for token in text.replace("/", " / ").split():
        if token == "/":
            side = BLACK
        elif token.startswith("W:"):
            side = WHITE
            token = token[2:]
        elif token.startswith("B:"):
            side = BLACK
            token = token[2:]
        if len(token) == 2 and "a" <= token[0] <= "g" and "2" <= token[1] <= "7":
            sq = (ord(token[0]) - ord("a")) * ROWS + int(token[1]) - 2
            if board[sq]:
                raise ValueError(f"overlap at {token}")
            board[sq] = side
    return tuple(board)


def passer_distances(board, turn, ep):
    dirs = {WHITE: 1, BLACK: -1}
    distances = {}
    victim = NO_EP if ep == NO_EP else ep - dirs[turn]
    for side in (WHITE, BLACK):
        enemy = BLACK if side == WHITE else WHITE
        direction = dirs[side]
        best = None
        for sq, piece in enumerate(board):
            if piece != side or (side != turn and sq == victim):
                continue
            file, rank = divmod(sq, ROWS)
            blocked = False
            for df in (-1, 0, 1):
                nf = (file + df) % 7
                rr = rank + direction
                while 0 <= rr < ROWS:
                    if board[nf * ROWS + rr] == enemy:
                        blocked = True
                        break
                    rr += direction
                if blocked:
                    break
            if not blocked:
                dist = rank + 1 if side == BLACK else 6 - rank
                best = dist if best is None else min(best, dist)
        distances[side] = best
    return distances


def race_winner(board, turn, ep, mover):
    d = passer_distances(board, turn, ep)
    w, b = d[WHITE], d[BLACK]
    if w is not None and b is None:
        return WHITE
    if b is not None and w is None:
        return BLACK
    if w is not None and b is not None:
        other = BLACK if mover == WHITE else WHITE
        return other if d[other] <= d[mover] else mover
    return None


def outcomes(board):
    @lru_cache(maxsize=2_000_000)
    def win(pos, turn, ep, heap):
        own, enemy = (WHITE, BLACK) if turn == WHITE else (BLACK, WHITE)
        direction = 1 if turn == WHITE else -1
        for src, piece in enumerate(pos):
            if piece != own:
                continue
            file, rank = divmod(src, ROWS)
            nr = rank + direction
            if not 0 <= nr < ROWS:
                continue
            forward = file * ROWS + nr
            moves = []
            if pos[forward] == EMPTY:
                moves.append((forward, False, False))
                start = 0 if turn == WHITE else 5
                nr2 = rank + 2 * direction
                if rank == start and pos[file * ROWS + nr2] == EMPTY:
                    moves.append((file * ROWS + nr2, False, True))
            for df in (-1, 1):
                dest = ((file + df) % 7) * ROWS + nr
                if pos[dest] == enemy:
                    moves.append((dest, False, False))
                elif dest == ep:
                    moves.append((dest, True, False))
            for dest, ep_capture, double in moves:
                nxt = list(pos)
                nxt[src], nxt[dest] = EMPTY, own
                next_ep = NO_EP
                if ep_capture:
                    nxt[dest - direction] = EMPTY
                if double:
                    df = dest // ROWS
                    rr = dest % ROWS
                    if any(nxt[((df + x) % 7) * ROWS + rr] == enemy for x in (-1, 1)):
                        next_ep = dest - direction
                nxt = tuple(nxt)
                winner = race_winner(nxt, enemy, next_ep, turn)
                if winner is not None:
                    if winner == turn:
                        return True
                elif not win(nxt, enemy, next_ep, heap):
                    return True
        for smaller in range(heap):
            winner = race_winner(pos, enemy, NO_EP, turn)
            if winner is not None:
                if winner == turn:
                    return True
            elif not win(pos, enemy, NO_EP, smaller):
                return True
        return False

    p = []
    for heap in range(3):
        p.append(not win(board, WHITE, NO_EP, heap) and not win(board, BLACK, NO_EP, heap))
    return tuple(p), win.cache_info()


def main(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        if "\t" not in line or not line.startswith("W:"):
            continue
        pos, claimed = line.split("\t", 1)
        py_p, info = outcomes(parse(pos))
        py_star = py_p[2] and not py_p[0] and not py_p[1]
        c_star = "star2=1" in claimed
        if py_star != c_star:
            rows.append((pos, claimed, py_p, py_star, info.currsize))
    print(f"independent_part1 mismatches={len(rows)}")
    for pos, claimed, py_p, py_star, states in rows:
        print(f"{pos}\tC={claimed}\tPython_P={py_p}\tPython_star2={int(py_star)}\tcache={states}")
    return bool(rows)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
