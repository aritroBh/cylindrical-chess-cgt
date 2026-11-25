"""K63 copy of K59's copy (unchanged; VER is this directory) of the K48 referee's def48.py.
K48 referee: Definition 4.8 test of one group, from the --moves output of ref3m or kp_p --pmodel only.
Written by the referee from LOOPY Definition 4.8 (not from the investigator's verify_hit48.py).

usage: def48.py <ref3m|kpp> <cyl|flat> <W> <H> <shuttler w|b> "<pieces with shuttler on z0, no side/ep>" <z1> <logtag>

Reading of Definition 4.8 used here (S = shuttling side, F = freezing side; over: S = Black):
  K1: no F pawn attacks z0 or z1; no S pawn attacks the F king square f0.  K2: king distance(f0, z_i) >= 2.
  (1) both S-to-move roots legal; every S move other than the shuttle loses at once (value after = F wins);
      the shuttle z_a -> z_(1-a) is in the move list.
  (2) both F-to-move roots: F has a move that does not lose at once (a freeze).  A freeze that is a promotion: not exact.
  (3) every freeze, q with S to move (e.p. square set if the freeze is a double step): legal, S has a move, every S move
      loses at once.
  (4) the same q with F to move, no e.p.: legal, F has a move, every F move loses at once.
Values from the solvers are White's view (W, L, D, X = illegal).  Every solver call goes through kings/delegate/heavy.sh.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VER = os.path.dirname(HERE)
HEAVY = os.path.join(VER, '..', '..', 'heavy.sh')   # K59 copy: VER = kings/delegate/out/K59
BIN = os.path.join(VER, 'bin')

solver, kind, W, H, S, pieces, z1, tag = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
F = 'w' if S == 'b' else 'b'
calls = [0]

def board_arg():
    if solver == 'ref3m':
        return ('cyl:%dx%d' if kind == 'cyl' else 'pln:%dx%d') % (W, H)
    return ('cyl:%dx%d' if kind == 'cyl' else 'flat:%dx%d') % (W, H)

def run(lines):
    calls[0] += 1
    if solver == 'ref3m':
        cmd = [HEAVY, '/usr/bin/time', '-l', os.path.join(BIN, 'ref3m'), '--board', board_arg(), '--moves']
    else:
        cmd = [HEAVY, '/usr/bin/time', '-l', os.path.join(BIN, 'kp_p10'), '--board', board_arg(), '--pmodel', '--cap', '1',
               '--threads', '1', '--moves']
    base = os.path.join(VER, 'logs', 'grp', '%s_%s_%d' % (tag, solver, calls[0]))
    os.makedirs(os.path.dirname(base), exist_ok=True)
    with open(base + '.in', 'w') as f: f.write('\n'.join(lines) + '\n')
    with open(base + '.in') as fi, open(base + '.out', 'w') as fo, open(base + '.err', 'w') as fe:
        p = subprocess.Popen(cmd, stdin=fi, stdout=fo, stderr=fe)
        with open(os.path.join(VER, 'pids.log'), 'a') as pl: pl.write('%d heavy.sh %s %s call %d\n' % (p.pid, tag, solver, calls[0]))
        p.wait()
    res = {}
    for line in open(base + '.out'):
        line = line.rstrip('\n')
        if ' | ' not in line: continue
        parts = [x.strip() for x in line.split(' | ')]
        pos = parts[0]
        if solver == 'ref3m':
            t = parts[1].split(); val = t[0]; mv = t[1:]
        else:
            a, b = parts[1].split()
            if a != b: sys.exit('kp_p bounds differ at %s' % pos)   # cannot happen in the P model
            val = a
            mv = parts[2].split() if len(parts) > 2 else []
            if mv and mv[0] == 'A:': sys.exit('kp_p printed two move lists at %s' % pos)
        moves = []
        for m in mv:
            name, v = m.rsplit(':', 1); moves.append((name, v))
        res[pos] = (val, moves)
    return res

def sq(s): return ord(s[0]) - 97, int(s[1:]) - 1
def nm(f, r): return chr(97 + f) + str(r + 1)
def fdist(a, b):
    d = abs(a - b)
    return min(d, W - d) if kind == 'cyl' else d
def kdist(a, b):
    (fa, ra), (fb, rb) = sq(a), sq(b)
    return max(fdist(fa, fb), abs(ra - rb))
def pawn_attacks(pcs, col, target):
    ft, rt = sq(target)
    for s, p in pcs.items():
        if p == ('P' if col == 'w' else 'p'):
            f, r = sq(s)
            if r + (1 if col == 'w' else -1) == rt and fdist(f, ft) == 1: return True
    return False

def parse(pc):
    d = {}
    for t in pc.split(): d[t[1:]] = t[0]
    return d
def fmt(pcs, stm, ep='-'):
    key = lambda kv: ('KkPp'.index(kv[1]), kv[0])
    return ' '.join(p + s for s, p in sorted(pcs.items(), key=key)) + ' %s %s' % (stm, ep)

def apply(pcs, stm, mv):
    """apply a move given in solver notation; return (pieces, ep, is_promotion)."""
    if mv == 'promo' or '=' in mv or re.match(r'^P[a-j]\d[a-j]\d[QRBNqrbn]$', mv): return None, '-', True   # fixed: 'b' file letters are not bishops
    m = re.match(r'^([KP])([a-j]\d)([a-j]\d)$', mv)
    if not m: sys.exit('cannot read move %s' % mv)
    pt, fr, to = m.groups()
    q = dict(pcs)
    me = q.pop(fr)
    assert me.lower() == pt.lower() and (me.isupper() == (stm == 'w')), (mv, me)
    ff, rf = sq(fr); ft, rt = sq(to)
    if to in q: del q[to]
    elif pt == 'P' and ff != ft:                       # e.p.: the captured pawn stands beside, on the from rank
        del q[nm(ft, rf)]
    q[to] = me
    ep = '-'
    if pt == 'P' and abs(rt - rf) == 2: ep = nm(ff, (rf + rt) // 2)
    return q, ep, False

def loses(v, mover): return v == ('L' if mover == 'w' else 'W')

pcs0 = parse(pieces)
skey = 'k' if S == 'b' else 'K'; fkey = 'K' if S == 'b' else 'k'
z0 = [s for s, p in pcs0.items() if p == skey][0]
f0 = [s for s, p in pcs0.items() if p == fkey][0]
zs = [z0, z1]
fails = []
for z in zs:
    if pawn_attacks(pcs0, F, z): fails.append('K1: %s attacked by an F pawn' % z)
    if kdist(z, f0) < 2: fails.append('K2: dist(%s,%s) < 2' % (z, f0))
if pawn_attacks(pcs0, S, f0): fails.append('K1: F king square %s attacked by an S pawn' % f0)
if kdist(z0, z1) != 1: fails.append('z not adjacent')

def placed(za):
    q = {s: p for s, p in pcs0.items() if p != skey}
    q[za] = skey
    return q
roots = {}
for a in (0, 1):
    for stm in (S, F): roots[(a, stm)] = fmt(placed(zs[a]), stm)
R = run(list(roots.values()))
out = []
freezes = []
for a in (0, 1):
    pos = roots[(a, S)]; val, mv = R[pos]
    out.append('root %s : %s  %s' % (pos, val, ' '.join('%s:%s' % x for x in mv)))
    if val == 'X': fails.append('(1) root illegal: %s' % pos); continue
    shuttle = ('K%s%s' % (zs[a], zs[1 - a]))
    if shuttle not in [m for m, v in mv]: fails.append('(1) shuttle %s not legal at %s' % (shuttle, pos))
    for m, v in mv:
        if m != shuttle and not loses(v, S): fails.append('(1) %s does not lose at once (%s) at %s' % (m, v, pos))
    pos = roots[(a, F)]; val, mv = R[pos]
    out.append('root %s : %s  %s' % (pos, val, ' '.join('%s:%s' % x for x in mv)))
    if val == 'X': fails.append('(2) root illegal: %s' % pos); continue
    fz = [m for m, v in mv if not loses(v, F)]
    if not fz: fails.append('(2) no freeze at %s' % pos)
    for m in fz:
        q, ep, promo = apply(parse(' '.join(pos.split()[:-2])), F, m)
        if promo: fails.append('(2) freeze %s is a promotion at %s' % (m, pos)); continue
        freezes.append((pos, m, fmt(q, S, ep), fmt(q, F, '-')))
qlines = []
for f in freezes: qlines += [f[2], f[3]]
if qlines:
    Q = run(qlines)
    for root, m, qs, qf in freezes:
        vs, ms = Q[qs]; vf, mf = Q[qf]
        out.append('freeze %s at %s' % (m, root))
        out.append('  q S to move %s : %s  %s' % (qs, vs, ' '.join('%s:%s' % x for x in ms)))
        out.append('  q F to move %s : %s  %s' % (qf, vf, ' '.join('%s:%s' % x for x in mf)))
        if vs == 'X' or not ms: fails.append('(3) q illegal or no move: %s' % qs)
        for x, v in ms:
            if not loses(v, S): fails.append('(3) %s does not lose at once (%s) at %s' % (x, v, qs))
        if vf == 'X' or not mf: fails.append('(4) q illegal or no move: %s' % qf)
        for x, v in mf:
            if not loses(v, F): fails.append('(4) %s does not lose at once (%s) at %s' % (x, v, qf))
print('%s %s %s:%dx%d shuttler %s z=%s,%s f0=%s pieces "%s" freezes %s' % ('PASS' if not fails else 'FAIL', solver, kind, W, H, S, z0, z1, f0, pieces,
      ['%s at %s' % (m, ' '.join(r.split()[:2])) for r, m, _, _ in freezes]))
for x in fails: print('   ', x)
for x in out: print('      ', x)
