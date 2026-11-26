"""K67: classification of exact over groups (brief question 2), with the K65 referee's programs and K65's def48.py.
Per group (list lines "name|pieces with the Black king on z0|z0|z1"):
  1. Definition 4.8 again: def48.py from ref3m and from kp_p --pmodel (def48.py calls heavy.sh itself; src/wd.sh watches
     the def48.py tree).
  2. ax65 (Definition 4.8, (B1) beside -1 at every non-shuttle Black root move, Aux, ladders T_0..T_8) via src/run.sh.
  3. pk_sum beside -1 ((B1)) and pk_sum -aux at the same moves (inputs x_m from ax65's lines), via src/run.sh.
  4. Where ax65 says Aux is lost: pk_sum -ladder N for N = 0, 1, ... at x_m (White to move) and both roots (Black to
     move), u_0 = T-state 1, until x_m is not a White win (at most N = 8).
Stops at once if logs/STOP exists (any watchdog kill).  Writes logs/cls/<name>.sum (one block per group).
usage: python3 src/classify.py <group list>"""
import os, re, subprocess, sys
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(K)
def stop():
    if os.path.exists('logs/STOP'): print('STOP present: classification halted'); sys.exit(1)
def run(name, args, inp=None):
    stop()
    env = dict(os.environ)
    if inp: env['IN'] = inp
    subprocess.run(['zsh', 'src/run.sh', name] + args, env=env)
    stop()
    rc = open('logs/%s.rc' % name).read().split()[0]
    if rc != 'rc=0': print('nonzero', name, rc)
    return open('logs/%s.out' % name).read()
def def48(nm, pcs, z1, s):
    out = 'logs/grp/%s_def48_%s.txt' % (nm, s)
    if os.path.exists(out) and open(out).read().startswith(('PASS', 'FAIL')): return open(out).read().split('\n')[0]
    stop(); os.makedirs('logs/grp', exist_ok=True)
    with open(out, 'w') as fo:
        p = subprocess.Popen(['python3', 'src/def48.py', s, 'flat', '8', '8', 'b', pcs, z1, nm], stdout=fo, stderr=subprocess.STDOUT,
                             env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    open('pids.log', 'a').write('%d def48.py %s %s\n' % (p.pid, nm, s))
    w = subprocess.Popen(['zsh', 'src/wd.sh', str(p.pid), '%s_def48_%s' % (nm, s)])
    open('pids.log', 'a').write('%d wd.sh %s_def48_%s\n' % (w.pid, nm, s))
    p.wait(); w.wait(); stop()
    return open(out).read().split('\n')[0]
for line in open(sys.argv[1]):
    if not line.strip(): continue
    nm, pcs, z0, z1 = line.strip().split('|')
    S = ['%s  %s  /%s' % (nm, pcs, z1)]
    for s in ('ref3m', 'kpp'):
        S.append('  def48 %s: %s' % (s, def48(nm, pcs, z1, s).split(' flat')[0]))
    ax = run('g/' + nm, ['bin/ax65', 'flat:8x8', pcs, z0, z1])
    S += ['  ax65: ' + l for l in ax.splitlines() if l.startswith(('DEFINITION', '(B1)', 'ABORT', 'stable', 'ladder layers'))]
    b1 = re.findall(r'^B1 (\S+)\s+x_m = (.*?) : beside -1 (not a White win|WHITE WIN)', ax, re.M)
    aux = dict(re.findall(r'^AUX (\S+)\s+: White (WINS|does NOT win)', ax, re.M))
    lad = dict(re.findall(r'^LADDER (\S+)\s+: (.*)$', ax, re.M))
    if not b1:
        S.append('  no bad moves read from ax65 (see logs/g/%s.out)' % nm)
    else:
        xm = 'in/xm_%s.txt' % nm
        open(xm, 'w').write(''.join('%s 1\n' % x for _, x, _ in b1))
        pb = run('pk/B1_' + nm, ['bin/pk_sum', '-T', '2|/;/0'], xm).splitlines()
        pa = run('pk/aux_' + nm, ['bin/pk_sum', '-aux'], xm).splitlines()
        pbv = [l.split()[-3] for l in pb if '(configs' in l]; pav = [l.split()[-3] for l in pa if '(configs' in l]
        nfail = 0; dis = 0
        for i, (mv, x, v) in enumerate(b1):
            a1 = 'W' if v == 'WHITE WIN' else 'N'; p1 = 'W' if pbv[i] == 'W' else 'N'
            a2 = 'W' if aux.get(mv) == 'WINS' else 'N'; p2 = 'W' if pav[i] == 'W' else 'N'
            dis += (a1 != p1) + (a2 != p2); nfail += a1 == 'N'
            S.append('  %-14s x_m=%-40s B1 ax65=%s pk_sum=%s(%s)  Aux ax65=%s pk_sum=%s(%s)  ladder(ax65): %s' % (mv, x, a1, p1, pbv[i], a2, p2, pav[i], lad.get(mv, '-')))
        S.append('  bad moves %d, (B1) fails at %d, Aux lost at %d, disagreements ax65/pk_sum %d' % (len(b1), nfail, sum(1 for mv, _, _ in b1 if aux.get(mv) != 'WINS'), dis))
        for i, (mv, x, v) in enumerate(b1):
            if aux.get(mv) == 'WINS': continue
            root = lambda z: ' '.join(('k' + z) if t[0] == 'k' else t for t in pcs.split())
            lf = 'in/lad_%s_%s.txt' % (nm, mv.replace('@', '_'))
            open(lf, 'w').write('%s 1\n%s b - 1\n%s b - 1\n' % (x, root(z0), root(z1)))
            for N in range(0, 9):
                o = run('pk/lad_%s_%s_T%d' % (nm, mv.replace('@', '_'), N), ['bin/pk_sum', '-ladder', str(N)], lf)
                vals = [l.split()[-3] for l in o.splitlines() if '(configs' in l]
                S.append('  pk_sum ladder at %s beside T_%d: x_m %s, root %s (Black to move) %s, root %s %s' % (mv, N, vals[0], z0, vals[1], z1, vals[2]))
                if vals[0] != 'W': S.append('  => N* at %s = %d (pk_sum); ax65: %s' % (mv, N, lad.get(mv, '-'))); break
    os.makedirs('logs/cls', exist_ok=True)
    open('logs/cls/%s.sum' % nm, 'w').write('\n'.join(S) + '\n')
    print('\n'.join(S), flush=True)
