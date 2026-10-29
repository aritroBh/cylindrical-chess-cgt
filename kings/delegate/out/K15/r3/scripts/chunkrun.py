#!/usr/bin/env python3
"""K15 r3: run kp_p (--pmodel, r3 build) over a file of positions in chunks, each run under ulimit -t 58 / nice 15 (a chunk that does not finish is halved; single positions that still
do not finish are reported MISSING).  usage: chunkrun.py BOARD IN OUT [CH=4] [--moves]"""
import sys, subprocess, os, resource
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
board, inf, outf = sys.argv[1:4]; CH = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 4
mv = '--moves' in sys.argv
lines = [l.strip() for l in open(inf) if l.strip()]
def pre(): resource.setrlimit(resource.RLIMIT_CPU, (58, 58)); os.nice(15)
res = {}
def go(ls):
    p = subprocess.run([os.path.join(R3, 'bin', 'kpp'), '--board', board, '--ep', 'on', '--cap', '0', '--pmodel'] + (['--moves'] if mv else []), input='\n'.join(ls) + '\n', capture_output=True, text=True, preexec_fn=pre)
    for l in p.stdout.splitlines():
        if ' | ' in l: res[l.split(' | ')[0].strip()] = l
    rest = [l for l in ls if l not in res]
    if rest:
        if len(rest) == 1: return
        h = len(rest) // 2; go(rest[:h]); go(rest[h:])
for i in range(0, len(lines), CH): go(lines[i:i + CH])
with open(outf, 'w') as f:
    for l in lines: f.write(res.get(l, l + ' | MISSING') + '\n')
print(sum(1 for l in lines if l in res), 'of', len(lines), 'done')
