#!/usr/bin/env python3
# K31 task 1: single blocked pair (white pawn a<r>, black pawn a<r+1>) on cyl:WxH, free board.
# Runs K20's kg (kg_wide for > 64 squares) and the referee's lk; compares class counts and the +1/-1 root sets.
import subprocess, sys, re, json, os
D = os.path.dirname(os.path.abspath(__file__)) + '/..'
BIN = D + '/bin'
def run(cmd, env=None):
    p = subprocess.run(['nice', '-n', '15'] + cmd, capture_output=True, text=True, env=env)
    return p.stdout
def lk_counts(board, r):
    out = run([BIN + '/lk', 'classify', board, 'a%d' % r, 'free'])
    cls = {}
    for line in out.splitlines():
        m = re.match(r'  (\S+)\s+(\d+)\s+e\.g\.', line)
        if m: cls[m.group(1).split('=')[0]] = cls.get(m.group(1).split('=')[0], 0) + int(m.group(2))
        m = re.match(r'  (\S+)\s+(\d+)\s*$', line)
    roots = int(re.search(r'roots (\d+) races (\d+)', out).group(1))
    races = int(re.search(r'races (\d+)', out).group(1))
    pos = {}
    for cl in ('+1', '-1'):
        o = run([BIN + '/lk', 'classify', board, 'a%d' % r, 'free', 'dump=' + cl])
        pos[cl] = sorted(l.split(' :: ')[1] for l in o.splitlines() if l.startswith('DUMP ' + cl + ' ::'))
    return roots, races, cls, pos
def kg_counts(board, r, exe):
    W, H = map(int, board.split(':')[1].split('x'))
    rf = '/tmp/k31_%s_%d.roots' % (board.replace(':', '_'), r)
    run([exe, '--board', board, '--only', 'a%d' % r, '--maxpairs', '1', '--roots', rf])
    cls = {}; pos = {'+1': [], '-1': []}; n = 0
    for line in open(rf):
        parts = line.rstrip('\n').split('|'); c, p = parts[0], parts[1]; nm = '|'.join(parts[2:-2])
        if 'P' not in p: continue   # pawnless roots are not in lk's root set
        n += 1
        nm = nm.split('=')[0]
        cls[nm] = cls.get(nm, 0) + 1
        if nm in pos: pos[nm].append(p)
    os.remove(rf)
    for k in pos: pos[k].sort()
    return n, cls, pos
def main():
    Ws = range(int(sys.argv[1]), int(sys.argv[2]) + 1)
    Hs = range(int(sys.argv[3]), int(sys.argv[4]) + 1)
    out = sys.argv[5]
    withkg = len(sys.argv) < 7 or sys.argv[6] != 'nokg'
    f = open(out, 'a')
    for H in Hs:
        for W in Ws:
            board = 'cyl:%dx%d' % (W, H)
            for r in range(2, H - 1):
                roots, races, cls, pos = lk_counts(board, r)
                rec = {'board': board, 'W': W, 'H': H, 'rank': r, 'roots': roots, 'races': races,
                       'lk_p1': len(pos['+1']), 'lk_m1': len(pos['-1']),
                       'lk_classes': {k: v for k, v in cls.items() if k in ('+1','-1','0','*','tis','tisn','{1|0}','{0|-1}','on','off','dud','{on|off}')}}
                if withkg:
                    exe = BIN + ('/kg' if W * H <= 64 else '/kgw')
                    if W * H <= 127:
                        n, kc, kp = kg_counts(board, r, exe)
                        rec['kg_exe'] = os.path.basename(exe); rec['kg_roots'] = n
                        rec['kg_p1'] = len(kp['+1']); rec['kg_m1'] = len(kp['-1'])
                        rec['agree_sets'] = (kp['+1'] == pos['+1'] and kp['-1'] == pos['-1'])
                        names = rec['lk_classes'].keys() | {k for k in kc if k in rec['lk_classes'] or k in ('+1','-1','0','*','tis','tisn','{1|0}','{0|-1}','on','off','dud','{on|off}')}
                        rec['agree_classes'] = all(kc.get(k, 0) == rec['lk_classes'].get(k, 0) for k in names)
                        rec['kg_classes'] = {k: kc.get(k, 0) for k in sorted(names)}
                f.write(json.dumps(rec) + '\n'); f.flush()
                print(board, r, rec['lk_p1'], rec['lk_m1'], rec.get('kg_p1'), rec.get('kg_m1'), rec.get('agree_sets'), rec.get('agree_classes'), flush=True)
main()
