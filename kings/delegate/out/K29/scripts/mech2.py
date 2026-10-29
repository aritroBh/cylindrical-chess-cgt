#!/usr/bin/env python3
"""mech2.py BOARD ZS FZ RESULTS [OUT]
Classify the failure mechanism of every failing group of RESULTS (R lines of grp/grp2 --mode test, first failing context kept).
For the witness (Z + ctx), with White to move and with Black to move, kp_p --pmodel --moves (kpp) gives P value of every move
(White's view: W / L / D); kp --frozen --moves gives the value in the frozen model of the parked position (Psi).
For each side s to move with Phi(s) != Psi(s):
  A (Psi: s loses, Phi: s does not lose): 'escape'.  The moves of s that do not lose in P are classified:
      K>B  king step onto a buffer file (distance exactly 1 from F_Z): a sortie to the buffer
      K>Z  king step inside F_Z
      K>X  king step to any other file (cannot happen from F_Z in one move; listed for completeness)
      Pz   Z-pawn move or capture      Pc  context-pawn move or capture
  B (Psi: s wins or draws, Phi: s does worse): 'refuted'.  Every Psi-winning move m of s is played and the opponent's non-losing
      replies in P are classified in the same way (from the opponent's side), 'opp:' prefix.
Output lines: Z | ctx | s | Phi Psi | class | detail
"""
import sys, re, subprocess
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
board, zs, fz, fn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
kind, dims = board.split(':'); W, H = map(int, dims.split('x')); cyl = kind == 'cyl'
def inz(f):
    if cyl: return ((f - zs) % W) < fz
    return zs <= f < zs + fz
def fdist(f):
    best = 99
    for g in range(W):
        if inz(g):
            d = abs(f - g)
            if cyl: d = min(d, W - d)
            best = min(best, d)
    return best
def fl(c): return ord(c) - 97
MV = re.compile(r'^([KP])([a-h])(\d)([a-h])(\d)(=\w)?:([WLD])$')

def run(cmd, lines):
    out = subprocess.run(cmd, input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout
    res = {}
    for l in out.splitlines():
        if ' | ' not in l: continue
        pos, rest = l.split(' | ', 1)
        parts = rest.split()
        res[pos] = (parts[0] + parts[1] if len(parts) > 1 and parts[1] in 'WLD' else parts[0], parts[3:] if len(parts) > 3 else [])
    return res

def moves_of(pos, frozen=False):
    cmd = [D + 'bin/kp' if frozen else D + 'bin/kpp', '--board', board, '--ep', 'on', '--promote', 'Q', '--moves'] + (['--frozen'] if frozen else ['--pmodel'])
    out = subprocess.run(cmd, input=pos + '\n', capture_output=True, text=True).stdout
    for l in out.splitlines():
        segs = l.split(' | ')
        if len(segs) >= 3 and segs[0].strip().startswith('K'):
            return segs[2].split(), segs[1].split()
    return None, []

def apply(pos, mv):
    """apply move token (without value) to position string; returns new position string or None for promotions."""
    t = pos.split(); stm = t[-2]
    m = MV.match(mv + ':W')
    if not m or m.group(6): return None
    pc, f0, r0, f1, r1 = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
    a, b = f0 + r0, f1 + r1
    body = t[:-2]
    own = ('K' if stm == 'w' else 'k') if pc == 'K' else ('P' if stm == 'w' else 'p')
    opp_pawn = 'p' if stm == 'w' else 'P'
    new = []
    for x in body:
        if x == own + a: new.append(own + b); continue
        if x[0] in 'Pp' and x[1:] == b and x[0] == opp_pawn: continue   # captured
        new.append(x)
    # e.p. capture (pawn moved diagonally onto an empty square): remove the pawn behind
    if pc == 'P' and f0 != f1 and (opp_pawn + b) in body:
        pass
    elif pc == 'P' and f0 != f1:
        vr = int(r1) - 1 if stm == 'w' else int(r1) + 1
        new = [x for x in new if x != opp_pawn + f1 + str(vr)]
    ep = '-'
    if pc == 'P' and abs(int(r1) - int(r0)) == 2:
        mid = f0 + str((int(r0) + int(r1)) // 2)
        for df in (-1, 1):
            g = fl(f1) + df
            if cyl: g %= W
            if 0 <= g < W and (opp_pawn + chr(97 + g) + r1) in body: ep = mid
    return ' '.join(new + ['b' if stm == 'w' else 'w', ep])

def classify(mvs, stm):
    """mvs: list 'Xabcd:V' of the mover; returns the set of classes of the moves that do not lose for the mover."""
    lose = 'L' if stm == 'w' else 'W'
    cls = set(); det = []
    for x in mvs:
        m = MV.match(x)
        if not m or m.group(7) == lose: continue
        pc, f0, f1, v = m.group(1), fl(m.group(2)), fl(m.group(4)), m.group(7)
        if pc == 'K':
            c = 'K>B' if fdist(f1) == 1 else ('K>Z' if inz(f1) else 'K>X')
        else:
            c = 'Pz' if inz(f0) else 'Pc'
        cls.add(c); det.append(x)
    return cls, det

pk = 'K%s1 k%s%d' % (chr(97 + zs % W), chr(97 + zs % W), H)
for l in open(fn):
    m = re.match(r'R (.*?) \| contexts_checked (\d+) differ (\d+) parking_mismatch (\d+) \| first fail:(.*?) \| P=(\w\w) F=(\w\w)', l)
    if not m: continue
    z, ctx, ph, ps = m.group(1), m.group(5).strip(), m.group(6), m.group(7)
    for si, stm in enumerate('wb'):
        if ph[si] == ps[si]: continue
        pos = '%s %s %s -' % (z, ctx, stm); ppos = '%s %s %s -' % (pk, ctx, stm)
        mv, _ = moves_of(pos)
        lose = 'L' if stm == 'w' else 'W'; win = 'W' if stm == 'w' else 'L'
        if mv is None:
            print('%s | %s | %s | Phi=%s Psi=%s | ERROR no moves line' % (z, ctx, stm, ph, ps)); continue
        if ps[si] == lose:
            cls, det = classify(mv, stm)
            if not mv: cls = {'STALE'}   # the mover has no legal move at all: stalemate (a draw), the group's king lost its buffer squares
            print('%s | %s | %s | Phi=%s Psi=%s | A escape | %s | %s' % (z, ctx, stm, ph, ps, ','.join(sorted(cls)), ' '.join(det)))
        else:
            fmv, _ = moves_of(ppos, frozen=True)
            wins = [x for x in (fmv or []) if x.endswith(':' + win)]
            out = []; cls_all = set()
            for x in wins:
                p2 = apply(pos, x.split(':')[0])
                if p2 is None: out.append(x + '>promotes'); continue
                mv2, _ = moves_of(p2)
                if mv2 is None: out.append(x + '>?'); continue
                c2, d2 = classify(mv2, 'b' if stm == 'w' else 'w')
                if not mv2: c2 = {'STALE'}
                cls_all |= c2
                out.append('%s>[%s]' % (x.split(':')[0], ','.join(d2) or 'none'))
            print('%s | %s | %s | Phi=%s Psi=%s | B refuted | opp:%s | %s' % (z, ctx, stm, ph, ps, ','.join(sorted(cls_all)), ' '.join(out)))
