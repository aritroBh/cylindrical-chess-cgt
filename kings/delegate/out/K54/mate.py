"""Independent flat-board king/pawn move lists and the two local certificates."""
from collections import deque
import chess  # second move generator, also checks structural position validity

files = "abcdefgh"


def step(sq, dx, dy):
    x, y = files.index(sq[0]) + dx, int(sq[1]) + dy
    return files[x]+str(y) if 0 <= x < 8 and 1 <= y <= 8 else None


def attacked(board, sq, white):
    for src, pc in board.items():
        if pc.isupper() != white:
            continue
        if pc.lower() == "k":
            if sq in (step(src,x,y) for x in (-1,0,1) for y in (-1,0,1) if x or y):
                return True
        elif pc.lower() == "p" and sq in (step(src,x,1 if white else -1) for x in (-1,1)):
            return True
    return False


def moves(board, white):
    # ponytail: only pre-promotion K/P positions here, with no e.p. entitlement.
    # Promotions are terminal; the queen-capture check below is geometric.
    for src, pc in board.items():
        if pc.isupper() != white:
            continue
        dy = 1 if white else -1
        if pc.lower() == "k":
            dests = [step(src,x,y) for x in (-1,0,1) for y in (-1,0,1) if x or y]
        else:
            one = step(src,0,dy)
            dests = [step(src,x,dy) for x in (-1,1) if step(src,x,dy) in board]
            if one and one not in board:
                dests.append(one)
                two = step(src,0,2*dy)
                if src[1] == ("2" if white else "7") and two not in board:
                    dests.append(two)
        for dst in dests:
            if dst is None or (dst in board and (board[dst].isupper() == white or board[dst].lower()=="k")):
                continue
            child = board.copy()
            del child[src]
            child[dst] = pc
            king = next(s for s,p in child.items() if p == ("K" if white else "k"))
            if not attacked(child,king,not white):
                yield src+dst,child


def mu(board):
    if "p" not in board.values():
        return "infinity"
    queue, seen = deque([(board,0)]), set()
    while queue:
        pos,depth = queue.popleft()
        key = tuple(sorted(pos.items()))
        if key in seen:
            continue
        seen.add(key)
        for u,child in moves(pos,False):
            if pos[u[:2]]=="p" and u[-1]=="1":
                return depth+1
            queue.append((child,depth+1))
    return "infinity"


for variant in (False,True):
    start = dict(a6="K",b6="P",b7="P",d6="P",a7="p")
    start.update(dict(b8="k",a3="p") if variant else dict(a8="k",e7="p"))
    native = chess.Board(None)
    for sq, pc in start.items():
        native.set_piece_at(chess.parse_square(sq),chess.Piece.from_symbol(pc))
    native.turn = chess.BLACK
    assert native.is_valid()
    m = "a3a2" if variant else "a8b8"
    y_moves = dict(moves(start,False))
    assert set(y_moves) == ({"a3a2","a7b6"} if variant else {"a8b8"})
    assert attacked(start,"b8" if variant else "a8",True) == (not variant)
    pre = y_moves[m]
    white_options = dict(moves(pre,True))
    assert not any(pre[u[:2]]=="P" and u[-1]=="8" for u in white_options)
    q = white_options["b6a7"]
    assert attacked(q,"b8",True) and not list(moves(q,False))
    local = {s:p for s,p in q.items() if s[0] in "ab" or p.lower()=="k"}
    defenses = dict(moves(local,False))
    assert attacked(local,"b8",True) and set(defenses)=={"b8c7"}
    after = dict(moves(defenses["b8c7"],True))["a7a8"]
    assert not attacked(after,"a8",False)  # even a pseudo-capture of the new queen is impossible
    # Cross-check the geometric enumeration against a separate legal-move generator.
    assert {u.uci() for u in native.legal_moves} == set(y_moves)
    native.push_uci(m)
    assert {u.uci() for u in native.legal_moves} == set(white_options)
    native.push_uci("b6a7")
    assert native.is_checkmate()
    for square in list(native.piece_map()):
        if chess.square_file(square) > 1:
            native.remove_piece_at(square)
    assert native.is_check() and {u.uci() for u in native.legal_moves} == set(defenses)
    native.push_uci("b8c7")
    native.push_uci("a7a8q")
    assert not any(u.to_square == chess.A8 for u in native.legal_moves)
    distance = mu({s:p for s,p in q.items() if p=="k" or s[0] not in "ab"})
    assert distance==("infinity" if variant else 5)
    print("variant" if variant else "original", "Y valid", True,"Y",list(y_moves),
          "White promotions before r: none; r b6a7 mate; local",list(defenses),
          "a7a8=Q safe; T=1; mu",distance)

    if not variant:
        # Removing d6 realizes the other end of the T=1 window in the real game.
        live = {s:p for s,p in q.items() if s!="d6"}
        replies = dict(moves(live,False))
        assert set(replies)=={"b8c7"}
        assert "a7a8" in dict(moves(replies["b8c7"],True))
        print("without d6: r checks, Kc7 forced, White wins on subsequent move 1")

# An on-group right can expire on a context move (LOOPY line 1182).
b = chess.Board("8/1P2p3/K7/8/1pk5/8/P7/8 b - - 0 1")
assert b.is_valid()
b.push_uci("c4c5")
b.push_uci("a2a4")
assert b.has_legal_en_passant()
local = b.copy()
local.remove_piece_at(chess.E7)
for reply in [*local.legal_moves, chess.Move.null()]:
    after = local.copy()
    after.push(reply)
    after.push_uci("b7b8q")
    assert not any(u.to_square == chess.B8 for u in after.legal_moves)
b.push_uci("e7e6")
assert b.ep_square is None
print("context push e7-e6 clears the previous projected a3 right")
