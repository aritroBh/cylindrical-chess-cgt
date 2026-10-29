#!/usr/bin/env python3
"""agentB/depth3.py BOARD ZS FZ 'Z tokens' : independent check that no sortie of the bare group Z is punished within 2 punisher moves.
For each side s to move and each legal move m (legal moves and their values from ref3m --moves, the K23 referee's solver, written from
SPEC.md; positions after a move from mech2.apply):  W3(m) = 'the punisher wins within 3 plies after m' is decided by a depth-3 search:
   exists r (a promotion; or after which s has no legal move and is mated; or after which every legal reply q of s is not a promotion and
   leaves the punisher a promotion at once).  L(m) <= 2 iff W3(m).   Prints one line per move: m  W3  and a summary.
A mated s is recognised by ref3m's value of the position (no legal moves and value L for s); a stalemate is not a win."""
import sys, subprocess, importlib.util
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
board, zs, fz, z = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
rb = board.replace('flat:', 'flat') if board.startswith('flat') else board
sys.argv = ['mech2', board, zs, fz, '/dev/null']
spec = importlib.util.spec_from_file_location('mech2', D + 'scripts/mech2.py'); m2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m2)
cache = {}
def moves(pos):
    """ref3m --moves: (header value from White's view for the stated side to move, [move tokens without value])"""
    if pos in cache: return cache[pos]
    out = subprocess.run([D + 'bin/ref3m', '--board', rb, '--moves'], input=pos + '\n', capture_output=True, text=True).stdout
    for l in out.splitlines():
        if ' | ' in l:
            p, rest = l.split(' | ', 1); t = rest.split()
            cache[pos] = (t[0], [x.split(':')[0] for x in t[1:]]); return cache[pos]
    raise RuntimeError('no output for ' + pos)
def promo(tok): return '=' in tok or tok.startswith('promo')
def W3(X, stm):      # X: position with the punisher to move (stm = punisher colour letter)
    other = 'b' if stm == 'w' else 'w'
    v, rs = moves(X)
    for r in rs:
        if promo(r): return True
        Y = m2.apply(X, r)
        if Y is None: print('APPLY NONE', X, r, file=sys.stderr); continue
        vY, qs = moves(Y)
        if not qs:
            lose_for_s = 'W' if stm == 'w' else 'L'      # White's view: punisher White wins -> W
            if vY == lose_for_s: return True            # s mated
            continue
        ok = True
        for q in qs:
            if promo(q): ok = False; break
            Zp = m2.apply(Y, q)
            vz, ps = moves(Zp)
            if not any(promo(p) for p in ps): ok = False; break
        if ok: return True
    return False
tot = 0; fast = 0
for stm in 'wb':
    pos = '%s %s -' % (z, stm)
    v, ms = moves(pos)
    for m in ms:
        X = m2.apply(pos, m)
        punisher = 'b' if stm == 'w' else 'w'
        w3 = W3(X, punisher); tot += 1; fast += w3
        print('%s to move %s : punished within 2 punisher moves: %s' % (stm, m, w3))
print('SUMMARY %s | moves %d | punished within 2 punisher moves: %d' % (z, tot, fast))
