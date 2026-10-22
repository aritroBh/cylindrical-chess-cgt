"""Verifier A, module 4: the chess variant (T = 0, stalemate = draw) and the kpsolve cross-check."""
import subprocess
from collections import deque


def chess_variant(G):
    """Exact chess results over G: returns list of 'W'/'D'/'L' (White's view) per node.

    Mover with no move: lost if in check (checkmate), drawn if not (stalemate).
    """
    n = G.n
    out = []
    wins = []
    for player in (0, 1):
        win = bytearray(n)
        cnt = [len(G.succ[x]) for x in range(n)]
        q = deque()
        for x in range(n):
            if G.stm[x] != player and cnt[x] == 0 and G.incheck[x]:
                win[x] = 1
                q.append(x)
        while q:
            u = q.popleft()
            for p in G.pred[u]:
                if win[p]:
                    continue
                if G.stm[p] == player:
                    win[p] = 1
                    q.append(p)
                else:
                    cnt[p] -= 1
                    if cnt[p] == 0:
                        win[p] = 1
                        q.append(p)
        wins.append(win)
    for x in range(n):
        assert not (wins[0][x] and wins[1][x])
        out.append('W' if wins[0][x] else 'L' if wins[1][x] else 'D')
    return out


def pos_line(G, pos):
    g = G.solver.g
    stm, wk, bk, offs, wp, bp, ep = pos
    toks = ['K' + g.sqname(wk), 'k' + g.sqname(bk)]
    for i in range(g.N):
        if wp >> i & 1:
            toks.append('P' + g.sqname(i))
        if bp >> i & 1:
            toks.append('p' + g.sqname(i))
    for c, ty, s in offs:
        ch = 'QRBN'[ty]
        toks.append((ch if c == 0 else ch.lower()) + g.sqname(s))
    return ' '.join(toks) + (' w' if stm == 0 else ' b') + ' -'


def run_kpsolve(G, kp_path, lines, threads=2):
    cmd = ['nice', '-n', '10', kp_path, '--board', G.board, '--ep', 'on', '--promote', 'QRBN',
           '--cap', '1', '--threads', str(threads)]
    p = subprocess.run(cmd, input='\n'.join(lines) + '\n', capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError('kp failed: ' + p.stderr[:500])
    res = []
    for ln in p.stdout.splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        left, right = ln.rsplit('|', 1)
        a, b = right.split()
        res.append((left.strip(), a, b))
    return res
