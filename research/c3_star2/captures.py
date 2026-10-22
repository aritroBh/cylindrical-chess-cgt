"""All capture events that lie on some history from the ranks-2-and-7 start to the C4 target (T33 item 6).
Forward search, then backward search from the target keys, both over the full game graph (no promotion,
count pruning as in reach.py). Prints each distinct capture event with the number of histories it lies on
(state count) and one example history for each event."""
from collections import defaultdict, deque
from cylcgt import pawns
from research.c3_star2.reach import label, legal_child


def graph(files, start, tcount, prune_passed):
    board = pawns.Board(files, 8, True, True)
    key0 = (start.white, start.black, start.ep, "W")
    succ = defaultdict(list)
    seen = {key0}
    q = deque([key0])
    while q:
        key = q.popleft()
        w, b, ep, side = key
        pos = pawns.Pos(w, b, ep)
        if prune_passed and (pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B")):
            continue
        for ch in pawns.moves(board, pos, side):
            if not legal_child(board, ch, side):
                continue
            if len(ch.white) + len(ch.black) < tcount:
                continue
            nxt = "B" if side == "W" else "W"
            ck = (ch.white, ch.black, ch.ep, nxt)
            succ[key].append((ck, label(pos, ch, side)))
            if ck not in seen:
                seen.add(ck)
                q.append(ck)
    return key0, succ, seen


def main(files, start_text, target_text, prune_passed):
    start = pawns.Pos.parse(start_text)
    target = pawns.Pos.parse(target_text)
    tcount = len(target.white) + len(target.black)
    key0, succ, seen = graph(files, start, tcount, prune_passed)
    tgt = {k for k in seen if (k[0], k[1]) == (target.white, target.black)}
    pred = defaultdict(list)
    for u, outs in succ.items():
        for v, lab in outs:
            pred[v].append((u, lab))
    # co-reachable: states from which a target state is reachable
    co = set(tgt)
    q = deque(tgt)
    while q:
        v = q.popleft()
        for u, _ in pred[v]:
            if u not in co:
                co.add(u)
                q.append(u)
    events = defaultdict(lambda: [0, None])
    for u, outs in succ.items():
        if u not in co:
            continue
        for v, lab in outs:
            if v in co and "x" in lab:
                events[lab][0] += 1
    print(f"files {files}, target {target_text}, prune_passed={prune_passed}: "
          f"target keys {len(tgt)}, co-reachable states {len(co)}")
    for lab, (cnt, _) in sorted(events.items()):
        print(f"  capture event {lab}: on {cnt} transitions of histories to the target")
    if not events:
        print("  no capture event lies on any history")


if __name__ == "__main__":
    main(4, "W: a2 b2 c2 d2 / B: a7 b7 c7 d7", "W: a4 b2 c2 / B: b6 c5 d6 d7", False)
    main(4, "W: a2 b2 c2 d2 / B: a7 b7 c7 d7", "W: a4 b2 c2 / B: b6 c5 d6 d7", True)
